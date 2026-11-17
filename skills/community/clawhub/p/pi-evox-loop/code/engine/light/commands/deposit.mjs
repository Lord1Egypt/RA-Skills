#!/usr/bin/env node
/**
 * deposit.mjs — 沉淀域（distill / fix-signals / draft）
 *
 * 0.34 从 light-cli.mjs 机械拆分：case 块原样搬运，块级作用域与 break 语义不变。
 */
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { depositionGate } from '../guards.mjs';
import * as distill from '../distill.mjs';
import { readGenes, readReview, appendDeposit, sourceInfo, isApprovedState } from '../store.mjs';
import { signGene } from '../identity.mjs';
import { proposeFromError } from '../distill.mjs';
import { flag, fail, autoApproveState } from '../shared.mjs';

// 迁移后位置：code/engine/light/commands/ —— 原「code/」为基准的根目录常量
const __here = path.dirname(fileURLToPath(import.meta.url));
const __CODE_DIR = path.resolve(__here, '../../..');
const __SKILL_ROOT = path.resolve(__here, '../../../..');

export async function run(cmd, rest, ctx) {
  const {
    SKILL_VERSION, flag, positional, fail, explainErr, printEvidence, runInstallSnippet, procedureText, autoApproveState, installHooks, CONFIG_FILE, readConfig, writeConfig, loopHealth, argOf, usage, doctor
  } = ctx;
  switch (cmd) {
  case 'distill': {
    const errorText = flag('error');
    const proposed = errorText ? proposeFromError(errorText, { tool: flag('tool', ''), context: flag('context', '') }) : null;
    // 信号：--signals 显式优先，缺省时由错误文本自动抽取（引导式）
    let signalsArg = flag('signals');
    if (proposed) {
      const auto = new Set(proposed.signals);
      if (signalsArg) for (const s of signalsArg.split(',').map((s) => s.trim()).filter(Boolean)) auto.add(s);
      signalsArg = [...auto].join(',');
    }
    const strategy = flag('strategy') || (proposed ? proposed.strategy : undefined);
    if (!strategy) fail('缺少 --strategy（写可执行修法：具体参数/命令/编码）', { hint: '参考上方用法示例；或从错误文本引导：node code/light-cli.mjs draft --error "<错误文本>"', errCode: 'E_USAGE' });
    const signals = (signalsArg || 'manual').split(',').map((s) => s.trim()).filter(Boolean);
    // ── 内容去重（2026-09-18 实测补充）──────────────────────────────────────
    // asset_id **不是内容派生**的：同一条 strategy 连跑两次 distill 会得到两个不同 sha256，
    // 故 store 那层「按 asset_id 去重」在本场景形同虚设，重复沉淀会不断堆积（周常重扫尤甚）。
    // 这里按「归一化 strategy」判重：命中即跳过 —— **不写基因，也不写台账**
    // （写台账会把已 approved 的资产重新打回 quarantined，等于悄悄撤销审核）。
    const { appendGene, appendReview, readGenes } = await import('../../.././engine/light/store.mjs');
    const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim().toLowerCase();
    const target = norm(strategy);
    if (readGenes().some((g) => norm((g.strategy || []).join(' ')) === target)) {
      console.log('[pi-evox] 跳过：库中已存在相同 strategy 的基因（内容去重）');
      break;
    }
    const { gene, raw } = distill.distillManual({
      category: flag('category', 'repair'),
      signals,
      strategy,
      summary: flag('summary') || (proposed ? proposed.summary : undefined),
      antiPatterns: proposed ? proposed.antiPatterns : [],
      source: proposed ? 'light-manual-guided' : 'light-manual',
      shareable: rest.includes('--shareable'),
    });
    if (!gene) { console.log(raw); break; }
    // 只在真正写入时登记 quarantined（等待审核）
    const dgate = depositionGate((gene.strategy || []).join('\n'));
    if (!dgate.ok) fail('沉淀质检未通过：' + dgate.reason, { code: 1, hint: 'gate=' + dgate.kind + '；沉淀要写 AVOID(什么坑)+FIX(怎么避开)，不是日志复述', errCode: 'E_GUARD' });
    // 0.29 B-1 溯源：记录「哪台机器、哪个模型」沉积了这条——同源沉积是单作危机的根因
    gene.generation_meta = { ...(gene.generation_meta || {}),
      source_model: sourceInfo().model || os.hostname().slice(0, 80),
      source_host: sourceInfo().host || os.hostname().slice(0, 80) };
    signGene(gene); // 0.21 provenance：落库即签（Ed25519，本机身份）
    const written = appendGene(gene);
    if (written) {
      appendDeposit({ gene_id: gene.id, category: gene.category || 'repair', scene: gene.category, state: autoApproveState(rest), source: 'distill' });
      const st = autoApproveState(rest);
      appendReview({ assetId: gene.asset_id, state: st, reason: st === 'approved' ? (process.stdout.isTTY ? 'auto-approved (own library)' : 'auto-approved (explicit --auto-approve)') : (process.stdout.isTTY ? 'manually distilled — review before use' : 'non-interactive deposit — review before use') });
    }
    console.log(raw + (written ? '' : '\n（asset 已存在，跳过重复写入）'));
    if (written) {
      const st = autoApproveState(rest);
      console.log(st === 'approved'
        ? `\n✓ 已入库并自动通过（立即可注入）：${gene.id}${process.stdout.isTTY ? '' : '（显式 --auto-approve）'}`
        : `\n已入库【待审/隔离，不会注入】：${gene.id}\n   审核：node code/light-cli.mjs approve ${gene.id}`);
    }
    break;
  }
  case 'fix-signals': {
    // 0.28 S-4：清洗存量基因里的"死中文 signal"（>2 字中文在 CJK bigram 分词下永不可命中）
    const { readGenes, appendGene, appendReview } = await import('../../.././engine/light/store.mjs');
    const { signGene } = await import('../../.././engine/light/identity.mjs');
    const { deadCjkSignals, expandTrigger, aliasStats } = await import('../../.././engine/light/aliases.mjs');
    const apply = rest.includes('--apply');
    const genes = readGenes();
    // 只统计**活跃**基因（台账 LWW 状态为 approved/quarantined 之外的已批准集合）——
    // 历史被隔离的旧版本仍在文件里（审计留痕），但它们不参与召回，不该计入体检指标。
    const { readReview } = await import('../../.././engine/light/store.mjs');
    const lww = {};
    for (const r of readReview()) lww[r.assetId] = String(r.state || '').toLowerCase();
    const active = genes.filter((g) => isApprovedState(lww[g.asset_id]));
    let touched = 0, fixed = 0;
    for (const g0 of active) {
      const dead = deadCjkSignals(g0.signals_match);
      if (!dead.length) continue;
      touched++;
      const tokens = new Set();
      let added = 0;
      for (const s0 of g0.signals_match) {
        // 「展开」= **替换**：多字中文 signal 本身不可命中，保留它只会让死信号永远归不了零
        if (deadCjkSignals([s0]).length) {
          const ex = expandTrigger(s0);
          for (const t of ex.tokens) { if (!tokens.has(t)) { tokens.add(t); added++; } }
        } else {
          tokens.add(s0);
        }
      }
      if (!added) continue;
      fixed++;
      if (!apply) continue;
      const g = JSON.parse(JSON.stringify(g0));
      g.signals_match = [...tokens];
      g.scope = { ...(g.scope || {}), signals: [...tokens].map((s) => `capability:${s}`) };
      const crypto = await import('node:crypto');
      const digest = crypto.createHash('sha256').update(JSON.stringify({ strategy: g.strategy, signals: g.signals_match, at: Date.now() })).digest('hex');
      g.asset_id = 'sha256:' + digest;
      g.id = 'gene_manual_' + digest.slice(0, 8);
      delete g.sig; delete g.keyid; delete g.pubkey; delete g.signed_at;
      signGene(g);
      if (appendGene(g)) {
        appendReview({ assetId: g.asset_id, state: 'approved', reason: '0.28 fix-signals：死中文 signal 展开为可命中的 token（重签）' });
        appendReview({ assetId: g0.asset_id, state: 'quarantined', reason: `0.28 fix-signals：被展开版取代（原 ${dead.length} 个死中文 signal）` });
      }
    }
    const st = aliasStats();
    console.log(`[gene-share] 死中文 signal 体检（活跃集 ${active.length} 条）：${touched} 条含死 signal，可展开 ${fixed} 条`);
    // 去重：同一策略文本在活跃集里可能有多版本（历史展开留下的）——保留 signals 最全的一版，其余隔离
    const byStrategy = new Map();
    for (const g of active) {
      const key = (g.strategy || []).join(' ').replace(/\s+/g, ' ').trim().slice(0, 80);
      if (!byStrategy.has(key)) byStrategy.set(key, []);
      byStrategy.get(key).push(g);
    }
    let dupGroups = 0, dupQuarantined = 0;
    for (const [, list] of byStrategy) {
      if (list.length < 2) continue;
      dupGroups++;
      // 保留规则：**先看死信号数**（少者优先），再看 signals 完整度（多者优先）——
      // 只按"signals 最多"保留会选中"追加版"（信号多但仍含死信号），把修复抵消掉。
      const keep = list.reduce((a, b) => {
        const da = deadCjkSignals(a.signals_match).length, db = deadCjkSignals(b.signals_match).length;
        if (db !== da) return db < da ? b : a;
        return (b.signals_match || []).length > (a.signals_match || []).length ? b : a;
      });
      for (const g of list) {
        if (g.asset_id === keep.asset_id) continue;
        if (!apply) { dupQuarantined++; continue; }
        appendReview({ assetId: g.asset_id, state: 'quarantined', reason: '0.28 fix-signals：同内容旧版本（保留 signals 最全的一版）' });
        dupQuarantined++;
      }
    }
    if (dupGroups) console.log(`  同内容重复：${dupGroups} 组，${apply ? '已隔离' : '待隔离'} ${dupQuarantined} 条旧版本`);
    console.log(`  概念表：${st.concepts} 概念 / ${st.enTokens} 英文 token / ${st.zhPhrases} 中文短语（${st.zhBigrams} 个 bigram 索引）`);
    if (!apply) console.log('  （预览模式；加 --apply 执行展开+重签+旧版隔离）');
    else console.log('  ✓ 已执行：展开并重签，旧 asset_id 已隔离');
    break;
  }
  case 'draft': {
    // 引导式草稿：从错误直接生成可编辑的 distill 草稿（预填 AVOID + anti_patterns），人只补 FIX。
    const errorText = flag('error');
    if (!errorText) fail('draft 需至少 --error "<错误文本>" 以自动抽信号', { hint: '用法：light-cli.mjs draft --error "<错误文本>" [--context "<在做什么>"] [--tool <工具名>] [--commit]', errCode: 'E_USAGE' });
    const proposed = proposeFromError(errorText, { tool: flag('tool', ''), context: flag('context', '') });
    // 0.28 S-2：--trigger "<动手前的措辞>"（可多次）——把触发短语按概念表展开成 signals
    //（英文 canonical + 中文 bigram 别名双写），使**预防型基因在动手前就能被召回**。
    const triggerPhrases = [];
    for (let i = 0; i < rest.length; i++) {
      if (rest[i] === '--trigger' && rest[i + 1]) triggerPhrases.push(rest[i + 1]);
    }
    let triggerInfo = null;
    if (triggerPhrases.length) {
      const { expandTrigger } = await import('../../.././engine/light/aliases.mjs');
      const tokens = new Set(proposed.signals);
      const hitConcepts = new Set();
      for (const ph of triggerPhrases) {
        const ex = expandTrigger(ph);
        for (const t of ex.tokens) tokens.add(t);
        for (const c of ex.concepts) hitConcepts.add(c);
      }
      proposed.signals = [...tokens];
      triggerInfo = { phrases: triggerPhrases, concepts: [...hitConcepts] };
    }
    // 人可补 --strategy 覆盖（写完整的 AVOID+FIX）；缺省用预填占位符（需审核前补全）。
    const strategy = flag('strategy') || proposed.strategy;
    console.log('【引导草稿】从错误自动生成（预填 AVOID，请补 FIX 后审核）：');
    console.log(`  signals_match : ${proposed.signals.join(', ')}`);
    if (triggerInfo) console.log(`  触发词展开    : ${triggerInfo.phrases.join(' / ')} → 概念 ${triggerInfo.concepts.join(', ') || '（无匹配概念，仅取原文 token）'}`);
    console.log(`  anti_patterns : ${proposed.antiPatterns.length ? proposed.antiPatterns.join(', ') : '（空·该信号族无无歧义单 token）'}`);
    console.log(`  负经验标签    : ${proposed.antiTag}`);
    console.log(`  summary       : ${proposed.summary}`);
    console.log(`  strategy      : ${strategy}`);
    if (rest.includes('--commit')) {
      const { appendGene, appendReview, readGenes } = await import('../../.././engine/light/store.mjs');
      const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim().toLowerCase();
      if (readGenes().some((g) => norm((g.strategy || []).join(' ')) === norm(strategy))) {
        console.log('\n[pi-evox] 跳过：库中已存在相同 strategy 基因已存在（内容去重）');
        break;
      }
      const { gene, raw } = distill.distillManual({
        category: 'repair', signals: proposed.signals, strategy,
        summary: proposed.summary, antiPatterns: proposed.antiPatterns, source: 'light-manual-guided',
        shareable: rest.includes('--shareable'),
      });
      if (!gene) { console.log(raw); break; }
      // 0.17.0 沉淀质检：占位符未填 / retry 日志复述 / 旁白开场 → **拒绝入库**（fail-closed），
      // 把召回侧的守卫前移到生产侧——autoApprove 的安全性由此成立。
      const gate = depositionGate((gene.strategy || []).join('\n'));
      if (!gate.ok) fail('沉淀质检未通过：' + gate.reason, { code: 1, hint: 'gate=' + gate.kind + '；修正后重新 distill/draft --commit', errCode: 'E_GUARD' });
      // 0.29 B-1 溯源：记录「哪台机器、哪个模型」沉积了这条——同源沉积是单作危机的根因
    gene.generation_meta = { ...(gene.generation_meta || {}),
      source_model: sourceInfo().model || os.hostname().slice(0, 80),
      source_host: sourceInfo().host || os.hostname().slice(0, 80) };
    signGene(gene); // 0.21 provenance：落库即签（Ed25519，本机身份）
      const written = appendGene(gene);
      if (written) { appendDeposit({ gene_id: gene.id, category: gene.category || 'repair', scene: gene.category, state: autoApproveState(rest), source: 'draft' });
      appendReview({ assetId: gene.asset_id, state: autoApproveState(rest), reason: autoApproveState(rest) === 'approved' ? 'auto-approved (own library)' : 'guided draft — review before use' }); }
      console.log(`\n${raw}${written ? '' : '\n（asset 已存在，跳过）'}`);
      if (written) {
        const st2 = autoApproveState(rest);
        console.log(st2 === 'approved'
          ? `✓ 已入库并自动通过（立即可注入）：${gene.id}${process.stdout.isTTY ? '' : '（显式 --auto-approve）'}`
          : `已入库【待审/隔离，不会注入】：${gene.id}\n   审核：node code/light-cli.mjs approve ${gene.id}`);
      }
    } else {
      console.log('\n未加 --commit：补全 strategy 里的 FIX 后，运行上面等价的 distill 命令（或加 --strategy 与 --commit 直接落库为待审草稿）。');
      console.log(`  node code/light-cli.mjs distill --signals "${proposed.signals.join(',')}" --strategy "${strategy}" --summary "${proposed.summary}"`);
    }
    break;
  }
    default:
      return false;
  }
  return true;
}
