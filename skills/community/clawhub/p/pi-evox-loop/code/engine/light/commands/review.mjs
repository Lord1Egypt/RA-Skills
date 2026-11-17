#!/usr/bin/env node
/**
 * review.mjs — 审核与台账域（approve / quarantine / list / feedback）
 *
 * 0.34 从 light-cli.mjs 机械拆分：case 块原样搬运，块级作用域与 break 语义不变。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as ledger from '../ledger.mjs';
import { readGenes } from '../store.mjs';
import { SKILL_VERSION, flag, positional, fail, printEvidence, argOf } from '../shared.mjs';

// 迁移后位置：code/engine/light/commands/ —— 原「code/」为基准的根目录常量
const __here = path.dirname(fileURLToPath(import.meta.url));
const __CODE_DIR = path.resolve(__here, '../../..');
const __SKILL_ROOT = path.resolve(__here, '../../../..');

export async function run(cmd, rest, ctx) {
  const {
    SKILL_VERSION, flag, positional, fail, explainErr, printEvidence, runInstallSnippet, procedureText, autoApproveState, installHooks, CONFIG_FILE, readConfig, writeConfig, loopHealth, argOf, usage, doctor
  } = ctx;
  switch (cmd) {
  case 'approve': {
    const id = positional[0];
    if (!id) fail('approve 需传入 <gene_id>', { hint: '先运行 node code/light-cli.mjs list 查看可用 gene_id', errCode: 'E_USAGE' });
    // 0.22 触发点绑死：approve 前自动跑 evidence（0.20.3 建了取证机制却没人用——
    // 用户 2026-10-17 问「有没有 timeline 回溯」才发现审 6 条基因全部没跑）。
    // 机制必须绑在动作节点上，而不是依赖"记得"（本项目的核心设计哲学）。
    // --skip-evidence 显式跳过（理由写入台账备注），用于已知无证据的共享池/起步包来源。
    const skipEvidence = rest.includes('--skip-evidence');
    const gForEv = readGenes().find((x) => x.id === id || x.asset_id === id);
    if (gForEv && !skipEvidence) {
      console.log('[gene-share] 审核取证（approve 前自动执行，0.22）：');
      printEvidence(gForEv);
      console.log('');
    }
    const r = ledger.approve(id);
    console.log(r.ok ? `✓ 已审核通过${r.alreadyApproved ? '（此前已通过）' : ''}：${r.assetId}` : `✗ ${r.reason}`);
    process.exit(r.ok ? 0 : 1);
    break;
  }
  case 'quarantine': {
    const id = positional[0];
    if (!id) fail('quarantine 需传入 <gene_id>', { hint: '先运行 node code/light-cli.mjs list 查看可用 gene_id', errCode: 'E_USAGE' });
    const r = ledger.quarantine(id, flag('reason', 'manually quarantined'));
    console.log(r.ok ? `✓ 已隔离：${r.assetId}` : `✗ ${r.reason}`);
    process.exit(r.ok ? 0 : 1);
    break;
  }
  case 'list': {
    // 0.24 场景过滤：list --scene <名> 只看该场景（category 受控词表）
    const sceneFilter = argOf(rest, '--scene') || null;
    const rows = ledger.list().filter((r) => !sceneFilter || r.category === sceneFilter);
    if (sceneFilter && !rows.length) { console.log(`（场景 ${sceneFilter} 下无基因；可用场景见 docs/overview.md 或池镜像）`); break; }
    if (!rows.length) { console.log('（台账为空）'); break; }
    console.log('state       | id                        | category | strategy（截断）' + (sceneFilter ? `  [场景: ${sceneFilter}]` : ''));
    for (const r of rows) {
      console.log(`${String(r.state).padEnd(11)} | ${String(r.id || r.assetId).padEnd(25)} | ${String(r.category || '-').padEnd(8)} | ${r.strategy}`);
    }
    break;
  }
  case 'feedback': {
    // 0.22 外部实例版：外部用户反馈入口（本地留痕 + 引导到 GitHub Discussions）。
    // 隐私纪律：只写用户主动输入的文本；无任何自动遥测；默认不出网。
    const text = rest.join(' ').trim();
    if (!text) fail('feedback 需传入反馈文本', { hint: 'node code/light-cli.mjs feedback "<你的反馈>"', errCode: 'E_USAGE' });
    const hitsDir = process.env.EVOX_HITS_DIR || path.join(__SKILL_ROOT, 'experiments');
    const { withLock } = await import('../../.././engine/light/store.mjs');
    withLock(hitsDir, () => {
      fs.mkdirSync(hitsDir, { recursive: true });
      fs.appendFileSync(path.join(hitsDir, 'feedback.jsonl'), JSON.stringify({
        ts: new Date().toISOString(), version: SKILL_VERSION, agent: 'light-cli',
        text: String(text).slice(0, 1000),
      }) + '\n');
    });
    console.log('[gene-share] 感谢反馈！已本地留痕（experiments/feedback.jsonl）。');
    console.log('  想让作者和其他用户看到？欢迎提交到 GitHub Discussions（Q&A / Show and tell）：');
    console.log('  https://github.com/stwhwing/pi-evox-lab/discussions');
    console.log('  或用起来后报告你的实例（帮我们达成 1.0 的外部实例判据）：');
    console.log('  https://github.com/stwhwing/pi-evox-lab/issues/new?template=adoption-report.yml');
    break;
  }
    default:
      return false;
  }
  return true;
}
