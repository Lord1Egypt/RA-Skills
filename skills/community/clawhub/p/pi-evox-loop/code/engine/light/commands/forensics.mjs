#!/usr/bin/env node
/**
 * forensics.mjs — 取证与报表域（timeline / evidence / harvest / session / report / export-evidence / stats）
 *
 * 0.34 从 light-cli.mjs 机械拆分：case 块原样搬运，块级作用域与 break 语义不变。
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { depositionGate } from '../guards.mjs';
import { STORE_DIR, readGenes, readReview, isApprovedState } from '../store.mjs';
import { verifyGene } from '../identity.mjs';
import { proposeFromError } from '../distill.mjs';
import { positional, fail, printEvidence, argOf } from '../shared.mjs';

// 迁移后位置：code/engine/light/commands/ —— 原「code/」为基准的根目录常量
const __here = path.dirname(fileURLToPath(import.meta.url));
const __CODE_DIR = path.resolve(__here, '../../..');
const __SKILL_ROOT = path.resolve(__here, '../../../..');

export async function run(cmd, rest, ctx) {
  const {
    SKILL_VERSION, flag, positional, fail, explainErr, printEvidence, runInstallSnippet, procedureText, autoApproveState, installHooks, CONFIG_FILE, readConfig, writeConfig, loopHealth, argOf, usage, doctor
  } = ctx;
  switch (cmd) {
  case 'timeline': {
    // 0.18：四账本按时间合并 → 单任务时间线 Markdown。
    // 方法论致谢：灵感来自 Perplexity 开源的 numbat（endpoint 行为审计器的 timeline 取证重建，
    // github.com/perplexityai/numbat，Apache-2.0）——「把账本变成监控录像」；实现为本机账本自有格式。
    const hitsDir = process.env.EVOX_HITS_DIR || path.join(__SKILL_ROOT, 'experiments');
    const lastN = parseInt(argOf(rest, '--last') || '50', 10) || 50;
    const files = [
      ['召回', path.join(hitsDir, 'recall_calls.jsonl')],
      ['注入', path.join(hitsDir, 'pending_injections.jsonl')],
      ['回填', path.join(hitsDir, 'hits.jsonl')],
      ['工具错误', path.join(hitsDir, 'error_candidates.jsonl')],
    ];
    const events = [];
    for (const [kind, f] of files) {
      try {
        for (const l of fs.readFileSync(f, 'utf8').split('\n')) {
          const t = l.trim(); if (!t) continue;
          let r; try { r = JSON.parse(t); } catch { continue; }
          const ts = r.ts || r.at || '';
          if (!ts) continue;
          const gid = r.gene_id || (r.assetId ? (readGenes().find((x) => x.asset_id === r.assetId) || {}).id || r.assetId : '') || '';
          const detail = r.note || r.query || r.snippet || r.error || r.reason || '';
          events.push({ ts, kind, gid: String(gid).slice(0, 28), detail: String(detail).slice(0, 90) });
        }
      } catch { /* 缺文件跳过 */ }
    }
    events.sort((a, b) => String(a.ts).localeCompare(String(b.ts)));
    const shown = events.slice(-lastN);
    console.log(`## 经验库时间线（最近 ${shown.length}/${events.length} 条，来源: ${hitsDir}）`);
    console.log('');
    console.log('| 时间 | 类型 | 基因 | 详情 |');
    console.log('|---|---|---|---|');
    for (const e of shown) console.log(`| ${e.ts} | ${e.kind} | ${e.gid || '-'} | ${e.detail || '-'} |`);
    if (!shown.length) console.log('（无事件——先跑一次 recall 产生埋点）');
    break;
  }
  case 'evidence': {
    const id = positional[0];
    if (!id) fail('evidence 需传入 <gene_id>', { hint: 'node code/light-cli.mjs evidence <gene_id>', errCode: 'E_USAGE' });
    const g = readGenes().find((x) => x.id === id || x.asset_id === id);
    if (!g) fail(`找不到基因: ${id}`, { code: 1, hint: '先 list 查看可用 gene_id', errCode: 'E_NOTFOUND' });
    printEvidence(g);
    break;
  }
  case 'harvest': {
    // 0.18：error_candidates → 沉淀建议清单（半自动沉淀的消费端；Layer 2 hook 负责捕获，本命令负责盘点）。
    // 0.19：--done/--dismiss <N> 把第 N 条移入 error_candidates.done.jsonl（保留审计痕迹），
    //   未处理列表只减不增——否则候选只累积不消费（41 条实证），nudge 也永远提醒。
    const hitsDir = process.env.EVOX_HITS_DIR || path.join(__SKILL_ROOT, 'experiments');
    const f = path.join(hitsDir, 'error_candidates.jsonl');
    const doneF = path.join(hitsDir, 'error_candidates.done.jsonl');
    let rows = [];
    try {
      rows = fs.readFileSync(f, 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
    } catch { /* 无候选 */ }
    rows = rows.filter((r) => r.kind !== 'beat');
    const doneIdx = rest.indexOf('--done') >= 0 ? rest.indexOf('--done') : rest.indexOf('--dismiss');
    if (doneIdx >= 0) {
      const isDismiss = rest[doneIdx] === '--dismiss';
      const num = parseInt(rest[doneIdx + 1], 10);
      const shown = rows.slice(-(parseInt(argOf(rest, '--last') || '10', 10) || 10));
      const target = shown[num - 1];
      if (!target) fail(`harvest ${isDismiss ? '--dismiss' : '--done'} 编号 #${num} 不存在（当前未处理 ${rows.length} 条，--last 窗口 ${shown.length} 条）`, { code: 1, errCode: 'E_NOTFOUND' });
      const { withLock } = await import('../../.././engine/light/store.mjs');
      withLock(hitsDir, () => {
        fs.mkdirSync(hitsDir, { recursive: true });
        fs.appendFileSync(doneF, JSON.stringify({ ...target, done_at: new Date().toISOString(), done_action: isDismiss ? 'dismissed' : 'harvested' }) + '\n');
        fs.writeFileSync(f, rows.filter((r) => r !== target).map((r) => JSON.stringify(r)).join('\n') + (rows.length > 1 ? '\n' : ''));
      });
      console.log(`[gene-share] #${num} 已${isDismiss ? '驳回（不留基因）' : '标记已收获'} → ${doneF}；未处理剩 ${rows.length - 1} 条`);
      break;
    }
    console.log(`[gene-share] 沉淀候选 ${rows.length} 条（来源 ${f}）`);
    if (!rows.length) { console.log('  无候选——Layer 2 hook 捕获的工具错误会出现在这里。'); break; }
    const shown = rows.slice(-(parseInt(argOf(rest, '--last') || '10', 10) || 10));
    shown.forEach((r, i) => {
      const fam = proposeFromError(r.snippet || '', {});
      console.log(`${i + 1}. [${r.ts || '?'}] ${r.tool || '?'} | 家族: ${fam.family} | ${String(r.snippet || '').slice(0, 80)}`);
      console.log(`   → node code/light-cli.mjs draft --error ${JSON.stringify(String(r.snippet || '').slice(0, 120))} --tool ${JSON.stringify(r.tool || '')} --context "来自 error_candidates" --commit`);
    });
    console.log('  原则：候选只是线索；FIX 必须由你补全成可执行修法（占位符会被 depositionGate 拒绝）。');
    console.log(`  处理完毕：harvest --done <N>（已沉淀）或 harvest --dismiss <N>（无价值驳回，留痕）`);
    break;
  }
  case 'session': {
    // 0.27 会话围栏（让 T1 召回与收尾沉淀"跑不掉"）：open=开围栏并自动召回；close=收围栏（沉淀或显式声明无坑）
    const hitsDir = process.env.EVOX_HITS_DIR || path.join(__SKILL_ROOT, 'experiments');
    const sessionsFile = path.join(hitsDir, 'sessions.jsonl');
    const sub = positional[0] || '';
    const taskName = positional.slice(1).join(' ') || argOf(rest, '--task') || 'untitled';
    const readSessions = () => { try { return fs.readFileSync(sessionsFile, 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean); } catch { return []; } };
    const writeSession = (rec) => { try { fs.mkdirSync(hitsDir, { recursive: true }); fs.appendFileSync(sessionsFile, JSON.stringify({ ts: new Date().toISOString(), ...rec }) + '\n'); return true; } catch { return false; } };
    if (sub === 'open') {
      writeSession({ kind: 'session-open', task: taskName, cwd: process.cwd() });
      console.log('[session] 围栏已开：' + taskName);
      console.log('[session] → 自动执行 T1 召回（真实任务，落生产账本）：');
      const r = spawnSync(process.argv[0], [path.join(__CODE_DIR, 'evolver-recall.mjs'), '--query', taskName, '--record', taskName + '：session open 自动召回'], { encoding: 'utf8' });
      process.stdout.write(r.stdout || '');
      if (r.stderr) process.stderr.write(r.stderr);
      console.log('[session] 提醒：收尾务必 `session close "<本轮结论>"`（踩坑先 draft 沉淀，无坑也要声明）——门禁会校验');
      break;
    }
    if (sub === 'close') {
      const note = positional.slice(1).join(' ') || argOf(rest, '--note') || '';
      if (!note) fail('用法: light-cli.mjs session close "<本轮结论/无踩坑声明>"（必填——闭门账必须写结论）', { errCode: 'E_USAGE' });
      const since = Date.now() - 12 * 3600000;
      let deposits = 0;
      try { deposits = fs.readFileSync(path.join(hitsDir, 'deposits.jsonl'), 'utf8').split('\n').filter(Boolean).filter((l) => { try { return (Date.parse(JSON.parse(l).ts) || 0) >= since; } catch { return false; } }).length; } catch {}
      writeSession({ kind: 'session-close', task: taskName, note, depositsInWindow: deposits });
      console.log(`[session] 围栏已关：${taskName}`);
      console.log(`  结论: ${note}`);
      console.log(`  近 12h 沉淀事件: ${deposits} 条${deposits === 0 ? '（若本轮踩坑请先 draft --commit 再关门）' : ' ✓'}`);
      break;
    }
    const rows = readSessions();
    console.log('[session] 会话围栏（最近 10 条）：');
    for (const r of rows.slice(-10)) console.log(`  ${(r.ts || '').slice(0, 19).replace('T', ' ')} | ${r.kind} | ${r.task}${r.note ? ' | ' + r.note : ''}`);
    if (!rows.length) console.log('  （空——本项目任务请先 `light-cli.mjs session open "<任务名>"`）');
    break;
  }
  case 'report': {
    // 0.25 维4：效果量化周报——从生产账本聚合 L1 活性/L2 回填/L3 家族复发雏形。
    const jsonOut = rest.includes('--json');
    const days = parseInt(argOf(rest, '--days') || '7', 10) || 7;
    const since = Date.now() - days * 86400000;
    const hitsDir = process.env.EVOX_HITS_DIR || path.join(__SKILL_ROOT, 'experiments');
    const readJ = (f) => { try { return fs.readFileSync(path.join(hitsDir, f), 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean); } catch { return []; } };
    const tsOf = (r) => Date.parse(r.ts || r.at || 0) || 0;
    const inWin = (r) => tsOf(r) >= since;
    const recalls = readJ('recall_calls.jsonl').filter(inWin);
    const pend = readJ('pending_injections.jsonl').filter(inWin);
    const deps = readJ('deposits.jsonl').filter(inWin);
    const verifs = readJ('verifications.jsonl').filter(inWin);
    const errs = readJ('error_candidates.jsonl').filter(inWin);
    const allErrs = readJ('error_candidates.jsonl');
    const targeted = recalls.filter((r) => r.targeted).length;
    const injectedTotal = recalls.reduce((a, r) => a + (r.injected || 0), 0);
    const sceneDist = {};
    for (const d of deps) { const sc = d.category || 'repair'; sceneDist[sc] = (sceneDist[sc] || 0) + 1; }
    // L3 雏形：错误家族复发（本窗 vs 全量家族分布）
    const famOf = (r) => { try { let raw = r.snippet || r.error || ''; try { const j = JSON.parse(raw); raw = [j.stderr, j.stdout, j.message, j.error].filter(Boolean).join(' '); } catch {} return proposeFromError(String(raw).slice(0, 300), { tool: r.tool || '', context: '' }).family; } catch { return 'unknown'; } };
    const famWin = {};
    for (const e of errs) { const f = famOf(e); famWin[f] = (famWin[f] || 0) + 1; }
    const famAll = {};
    for (const e of allErrs) { const f = famOf(e); famAll[f] = (famAll[f] || 0) + 1; }
    // 0.29 L4：异源复现率（B-1 溯源 + B-3 池信任分级的度量出口）
    const srcKey = (r) => `${r.source_model || 'unknown-model'}|${r.source_host || 'unknown-host'}`;
    const geneSrc = {};
    for (const h of readJ('hits.jsonl')) {
      if (!geneSrc[h.gene_id]) geneSrc[h.gene_id] = new Set();
      geneSrc[h.gene_id].add(srcKey(h));
    }
    for (const d of deps) {
      if (!geneSrc[d.gene_id]) geneSrc[d.gene_id] = new Set();
      geneSrc[d.gene_id].add(srcKey(d));
    }
    const crossSrc = Object.entries(geneSrc).filter(([, v]) => v.size >= 2).length;
    const singleSrc = Object.entries(geneSrc).filter(([, v]) => v.size === 1).length;
    const negated = pend.filter((r) => r.outcome === 'negated');
    const causeMatrix = {};
    for (const r of negated) { const c = r.because || 'unknown'; causeMatrix[c] = (causeMatrix[c] || 0) + 1; }
    const rep = {
      window_days: days, generated_at: new Date().toISOString(),
      L1_activity: { recall_calls: recalls.length, targeted, injections: injectedTotal, deposits: deps.length, by_scene: sceneDist },
      L2_relevance: { pending_injections: pend.length, verifications: verifs.length, backfill_rate: pend.length ? Math.round((verifs.length / pend.length) * 100) + '%' : 'n/a' },
      L3_families: { window: famWin, all_time: famAll },
      L4_heterogeneity: {
        genes_with_evidence: Object.keys(geneSrc).length,
        cross_source: crossSrc, single_source: singleSrc,
        cross_source_rate: Object.keys(geneSrc).length ? +(crossSrc / Object.keys(geneSrc).length).toFixed(3) : null,
        negate_causes: causeMatrix,
        note: 'cross_source = the same gene reproduced by >=2 distinct (model|host) pairs - the direct monoculture metric',
      },
    };
    if (jsonOut) { console.log(JSON.stringify(rep, null, 2)); break; }
    console.log(`[gene-share] 效果周报（近 ${days} 天，账本: ${hitsDir}）`);
    console.log(`  L1 活性：召回 ${recalls.length} 次（对靶 ${targeted}）｜注入 ${injectedTotal} 条次｜沉淀 ${deps.length} 条${Object.keys(sceneDist).length ? '（' + Object.entries(sceneDist).map(([k, v]) => k + '×' + v).join(', ') + '）' : ''}`);
    console.log(`  L2 相关性：注入待回填 ${pend.length}｜验证记录 ${verifs.length}｜回填率 ${rep.L2_relevance.backfill_rate}`);
    const famEntries = Object.entries(famWin).sort((a, b) => b[1] - a[1]);
    console.log(`  L3 错误家族（本窗）: ${famEntries.length ? famEntries.map(([k, v]) => k + '×' + v).join(', ') : '无'}`);
    console.log(`  L4 异源复现：有证据基因 ${rep.L4_heterogeneity.genes_with_evidence} 条｜跨源 ${rep.L4_heterogeneity.cross_source}｜单源 ${rep.L4_heterogeneity.single_source}｜跨源率 ${rep.L4_heterogeneity.cross_source_rate}｜negate 根因分布 ${JSON.stringify(rep.L4_heterogeneity.negate_causes)}`);
    console.log('  注：L4 的 cross_source 是「单作危机」的直接指标——单源占比高说明修法只被一个（模型|宿主）验证过，换环境可能失效。');
    break;
  }
  case 'export-evidence': {
    // 0.23：本地证据自审查包——把门禁/签名/时间线/审核台账导出为可审查集合（任何团队审计自己的库用）。
    const dest = argOf(rest, '--out') || path.join(os.homedir(), '.evomap', `evidence-export-${Date.now()}`);
    fs.mkdirSync(dest, { recursive: true });
    const hitsDir = process.env.EVOX_HITS_DIR || path.join(__SKILL_ROOT, 'experiments');
    let copied = 0;
    for (const f of ['error_candidates.jsonl', 'recall_calls.jsonl', 'pending_injections.jsonl', 'hits.jsonl', 'review.jsonl', 'genes.jsonl']) {
      try { fs.copyFileSync(path.join(hitsDir, f), path.join(dest, f)); copied++; } catch {}
      try { fs.copyFileSync(path.join(STORE_DIR, f), path.join(dest, f)); copied++; } catch {}
    }
    // 签名验证摘要
    const genes = readGenes();
    const signed = genes.filter((g) => g.sig);
    const bad = signed.filter((g) => verifyGene(g).status !== 'verified');
    fs.writeFileSync(path.join(dest, 'signature-summary.json'), JSON.stringify({
      exported_at: new Date().toISOString(), genes_total: genes.length,
      signed: signed.length, signature_failures: bad.length, failure_ids: bad.map((g) => g.id),
    }, null, 2));
    console.log(`[gene-share] 证据包已导出 → ${dest}（文件 ${copied} | 基因 ${genes.length} | 签名失败 ${bad.length}）`);
    break;
  }
  case 'stats': {
    // 0.23：本地使用统计——recall/命中/回填率（从本地台账读，无外发）
    const hitsDir = process.env.EVOX_HITS_DIR || path.join(__SKILL_ROOT, 'experiments');
    const count = (f) => { try { return fs.readFileSync(path.join(hitsDir, f), 'utf8').split('\n').filter(Boolean).length; } catch { return 0; } };
    const rc = count('recall_calls.jsonl'), pi = count('pending_injections.jsonl'), hf = count('hits.jsonl');
    const genes = readGenes();
    const lww = {}; for (const r of readReview()) lww[r.assetId] = r.state;
    const approved = genes.filter((g) => isApprovedState(lww[g.asset_id])).length;
    console.log(`[gene-share] 本地使用统计（${hitsDir}）：`);
    console.log(`  召回调用 ${rc} | 注入待回填 ${pi} | 回填 ${hf} | 回填率 ${pi ? Math.round((hf / pi) * 100) : '—'}%`);
    console.log(`  库: ${genes.length} 条（已审核 ${approved}）`);
    console.log('  注：回填=调用方确认注入有效；不回填的注入不计入效果统计。');
    break;
  }
    default:
      return false;
  }
  return true;
}
