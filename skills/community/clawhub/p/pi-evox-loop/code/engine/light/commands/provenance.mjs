#!/usr/bin/env node
/**
 * provenance.mjs — 签名与 provenance 域（shareable / identity / verify / resign / gene-pull-trust）
 *
 * 0.34 从 light-cli.mjs 机械拆分：case 块原样搬运，块级作用域与 break 语义不变。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { STORE_DIR, readGenes, readReview } from '../store.mjs';
import { signGene, verifyGene, loadIdentity, privateKeyPath } from '../identity.mjs';
import { positional, fail } from '../shared.mjs';

// 迁移后位置：code/engine/light/commands/ —— 原「code/」为基准的根目录常量
const __here = path.dirname(fileURLToPath(import.meta.url));
const __CODE_DIR = path.resolve(__here, '../../..');
const __SKILL_ROOT = path.resolve(__here, '../../../..');

export async function run(cmd, rest, ctx) {
  const {
    SKILL_VERSION, flag, positional, fail, explainErr, printEvidence, runInstallSnippet, procedureText, autoApproveState, installHooks, CONFIG_FILE, readConfig, writeConfig, loopHealth, argOf, usage, doctor
  } = ctx;
  switch (cmd) {
  case 'shareable': {
    // 0.22：设置 shareable 并【重新签名】——0.21 签名链要求基因 deposit 后不可变，
    // 但工作流天然会在 approve 后补标 shareable（变更即签名失效，自家闸门会拦）。
    // 因此：持钥人的授权变更（shareable 标记）必须走本命令重签，而不是直接改文件。
    const id = positional[0];
    if (!id) fail('shareable 需传入 <gene_id>', { hint: 'node code/light-cli.mjs shareable <gene_id>', errCode: 'E_USAGE' });
    const { withLock } = await import('../../.././engine/light/store.mjs');
    const genes = readGenes();
    const g = genes.find((x) => x.id === id || x.asset_id === id);
    if (!g) fail(`找不到基因: ${id}`, { code: 1, errCode: 'E_NOTFOUND' });
    withLock(STORE_DIR, () => {
      g.shareable = true;
      signGene(g); // 变更后重签（签名域含 shareable）
      const lines = genes.map((x) => JSON.stringify(x)).join('\n') + '\n';
      fs.writeFileSync(path.join(STORE_DIR, 'genes.jsonl'), lines);
    });
    // 回读验证
    const back = readGenes().find((x) => x.id === id);
    const v = verifyGene(back);
    console.log(`[gene-share] ${id}: shareable=true 已重签 — ${v.status}（${v.why}）`);
    if (v.status !== 'verified') process.exitCode = 1;
    break;
  }
  case 'identity': {
    // 0.21：本机签名身份（Ed25519 keypair，~/.evomap/identity/，私钥 0600 不出本机）
    const id = loadIdentity();
    console.log(`[gene-share] 本机身份 keyid=${id.keyId}`);
    console.log(`  私钥: ${privateKeyPath()}（0600，绝不出本机）`);
    console.log(`  公钥: 随基因 {pubkey} 字段出入池，供他机验签`);
    break;
  }
  case 'verify': {
    // 0.21：验签（本地库基因；入池导入时的验签在 gene import 内自动执行）
    const id = positional[0];
    if (!id) fail('verify 需传入 <gene_id>', { hint: 'node code/light-cli.mjs verify <gene_id>', errCode: 'E_USAGE' });
    const g = readGenes().find((x) => x.id === id || x.asset_id === id);
    if (!g) fail(`找不到基因: ${id}`, { code: 1, errCode: 'E_NOTFOUND' });
    const v = verifyGene(g);
    console.log(`[gene-share] ${g.id}: ${v.status} — ${v.why}`);
    if (!v.ok) process.exitCode = 1;
    break;
  }
  case 'resign': {
    // 0.31：把 v1 规范化的存量签名升级为 v2（v2 把**嵌套字段**纳入签名域，修复嵌套篡改仍验签通过）。
    // 默认演练（只打印将重签的条目，绝不落盘）；--yes 才真正写库。
    // 只处理「本机身份签署 + 当前验签通过 + 仍是 v1」的基因 —— 已篡改或他机签署的不动。
    const yes = rest.includes('--yes');
    const id = loadIdentity();
    const genes = readGenes();
    const todo = genes.filter((g) => g.sig && g.keyid === id.keyId
      && Number(g.sig_v || 1) < 2 && verifyGene(g).status === 'verified');
    console.log(`[gene-share] 待升级签名 ${todo.length} 条（本机身份 ${id.keyId}，共 ${genes.length} 条基因）`);
    for (const g of todo.slice(0, 10)) console.log(`  ${g.id}  ${String(g.summary || '').slice(0, 50)}`);
    if (todo.length > 10) console.log(`  … 另 ${todo.length - 10} 条`);
    if (!yes) {
      console.log('  （演练模式：加 --yes 才会写入 genes.jsonl）');
      break;
    }
    const { withLock } = await import('../../.././engine/light/store.mjs');
    let n = 0;
    withLock(STORE_DIR, () => {
      for (const g of todo) { signGene(g); n++; }
      const lines = genes.map((x) => JSON.stringify(x)).join('\n') + '\n';
      fs.writeFileSync(path.join(STORE_DIR, 'genes.jsonl'), lines);
    });
    // 回读验证：重签后必须全部 verified
    const after = readGenes().filter((g) => todo.some((t) => t.id === g.id));
    const stillBad = after.filter((g) => verifyGene(g).status !== 'verified');
    console.log(`[gene-share] 已重签 ${n} 条（v2）；回读验签失败 ${stillBad.length} 条`);
    if (stillBad.length) process.exitCode = 1;
    break;
  }
  case 'gene-pull-trust': {
    // 0.30 B-3：池内基因的信任分布（single-source / cross-source / unknown-source）
    // **不阻断拉取**（池里 99% 是单源，阻断=把池拉空）——只做可见化：拉之前先知道信谁。
    const { readGenes, readReview } = await import('../../.././engine/light/store.mjs');
    const lww = {};
    for (const r of readReview()) lww[r.assetId] = String(r.state || '').toLowerCase();
    const genes = readGenes().filter((g) => g.shareable === true && lww[g.asset_id] === 'approved');
    const dist = { 'single-source': 0, 'cross-source': 0, 'unknown-source': 0 };
    for (const g of genes) {
      const sm = (g.generation_meta || {}).source_model || '';
      const sh = (g.generation_meta || {}).source_host || '';
      if (sm && sh) dist['single-source']++; else dist['unknown-source']++;
    }
    const total = genes.length || 1;
    console.log('[gene-share] 池内信任分布（0.30）：');
    console.log(`  single-source（仅一个源验证过）: ${dist['single-source']}（${Math.round(dist['single-source'] / total * 100)}%）`);
    console.log(`  unknown-source（无溯源字段）  : ${dist['unknown-source']}（${Math.round(dist['unknown-source'] / total * 100)}%）`);
    console.log('  提示：单源基因换一个模型/宿主可能失效；关键修法看 report 的 L4 跨源率再决定是否扩散到更多宿主。');
    break;
  }
    default:
      return false;
  }
  return true;
}
