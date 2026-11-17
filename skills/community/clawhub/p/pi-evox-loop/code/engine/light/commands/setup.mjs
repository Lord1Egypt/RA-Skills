#!/usr/bin/env node
/**
 * setup.mjs — 安装配置与自检域（doctor / info / snippet / license / install* / config / starter / gene / demo）
 *
 * 0.34 从 light-cli.mjs 机械拆分：case 块原样搬运，块级作用域与 break 语义不变。
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { STORE_DIR, readGenes, readReview, approvedAssetIds } from '../store.mjs';
import { loadIdentity } from '../identity.mjs';
import { signLicense, verifyLicense } from '../identity.mjs';
import { positional, fail, runInstallSnippet, procedureText, autoApproveState, installHooks, CONFIG_FILE, readConfig, writeConfig, loopHealth, argOf, doctor } from '../shared.mjs';

// 迁移后位置：code/engine/light/commands/ —— 原「code/」为基准的根目录常量
const __here = path.dirname(fileURLToPath(import.meta.url));
const __CODE_DIR = path.resolve(__here, '../../..');
const __SKILL_ROOT = path.resolve(__here, '../../../..');

export async function run(cmd, rest, ctx) {
  const {
    SKILL_VERSION, flag, positional, fail, explainErr, printEvidence, runInstallSnippet, procedureText, autoApproveState, installHooks, CONFIG_FILE, readConfig, writeConfig, loopHealth, argOf, usage, doctor
  } = ctx;
  switch (cmd) {
  case 'doctor': {
    doctor();
    break;
  }
  case 'info': {
    const genes = readGenes(); const review = readReview(); const approved = approvedAssetIds();
    console.log(`库路径      : ${STORE_DIR}`);
    console.log(`基因总数    : ${genes.length}`);
    console.log(`台账记录    : ${review.length}`);
    console.log(`已审核(可注入): ${approved.size}`);
    // B：闭环健康度——把「静默失效」变成屏幕上明明白白的一句话
    console.log('');
    console.log(loopHealth(genes, approved));
    break;
  }
  case 'snippet': {
    // 给**没有钩子机制**的 Agent 用：输出一段可直接粘进 AGENTS.md / CLAUDE.md / 系统提示的操作规程。
    console.log(procedureText());
    break;
  }
  case 'license': {
    // 0.25 维1：license 签发（维护者）/验证（用户）。token=Ed25519 签名的 JSON 载荷。
    const sub2 = positional[0] || '';
    if (sub2 === 'issue') {
      const to = argOf(rest, '--to') || 'unnamed';
      const tier = argOf(rest, '--tier') || 'team-monthly';
      const days = parseInt(argOf(rest, '--days') || '30', 10) || 30;
      const id = loadIdentity();
      const payload = { iss: 'pi-evox-loop', sub: to, tier, iat: new Date().toISOString(), exp: new Date(Date.now() + days * 86400000).toISOString() };
      const token = signLicense(payload, id.privateKey);
      console.log(`[gene-share] license token 已签发（keyid=${id.keyId}）：`);
      console.log(token);
      console.log(`  载荷: sub=${to} tier=${tier} exp=${payload.exp.slice(0, 10)}`);
      console.log('  （分发给购买方；对方用 license verify <token> 验证；公钥随包分发 assets/issuer-pub.pem）');
    } else if (sub2 === 'verify') {
      const token = positional[1] || argOf(rest, '--token');
      if (!token) fail('用法: light-cli.mjs license verify <token>', { errCode: 'E_USAGE' });
      // 发行方公钥：.pem（ClawHub/GitHub 已发版）或 .txt（skillhub 禁 .pem 扩展名）双兼容
      const assetsDir = path.join(__SKILL_ROOT, 'assets');
      let pub = null;
      for (const ext of ['.pem', '.txt']) {
        try { pub = fs.readFileSync(path.join(assetsDir, 'issuer-pub' + ext), 'utf8'); break; } catch {}
      }
      const r = pub ? verifyLicense(token, pub) : { ok: false, reason: 'assets/issuer-pub.pem 缺失（发行方公钥未随包分发）' };
      if (r.ok) {
        const p2 = r.payload;
        const expired = p2.exp && Date.parse(p2.exp) < Date.now();
        console.log(`[gene-share] ✓ 签名有效：sub=${p2.sub} tier=${p2.tier} exp=${String(p2.exp || '').slice(0, 10)}${expired ? '（已过期）' : ''}`);
        process.exit(expired ? 1 : 0);
      } else {
        console.error(`[gene-share] ✗ 验证失败：${r.reason}`);
        process.exit(1);
      }
    } else {
      console.log('用法: light-cli.mjs license issue --to <购买方> --tier <team-monthly|team-annual|team-lifetime> [--days N]');
      console.log('      light-cli.mjs license verify <token>');
    }
    break;
  }
  case 'install': {
    // 0.23 U2：一键宿主接入——自动定位各宿主的指令文件并写入五触发点规程。
    // 纪律同 install-snippet：默认演练，--yes 才写入；幂等（evox-procedure:v1 标记）。
    const host = (positional[0] || argOf(rest, '--host') || '').toLowerCase();
    const HOSTS = {
      'claude-code': () => path.join(os.homedir(), '.claude', 'CLAUDE.md'),
      'claude': () => path.join(os.homedir(), '.claude', 'CLAUDE.md'),
      'cursor': () => path.join(process.cwd(), '.cursor', 'rules', 'pievox.md'),
      'codex': () => path.join(os.homedir(), '.codex', 'AGENTS.md'),
      'agents-md': () => path.join(process.cwd(), 'AGENTS.md'),
      'windsurf': () => path.join(process.cwd(), '.windsurf', 'rules', 'pievox.md'),
    };
    if (!host || !HOSTS[host]) {
      console.log('[gene-share] 用法: light-cli.mjs install <host> [--yes] [--file <覆盖路径>]');
      console.log('  支持: ' + Object.keys(HOSTS).join(' | '));
      console.log('  注: openclaw/hermes 走钩子，请用 install-hooks；其余宿主为规程文件接入。');
      process.exit(1);
    }
    const auto = HOSTS[host]();
    const fi = rest.indexOf('--file');
    const target = fi >= 0 ? rest[fi + 1] : auto;
    if (!target) { console.log(`[gene-share] ${host} 宿主走钩子接入：light-cli.mjs install-hooks`); process.exit(1); }
    console.log(`[gene-share] 宿主 ${host} → ${target}`);
    // 复用 install-snippet 的写入管线（直接落进同名 case 的共享函数）
    runInstallSnippet(['--file', target, ...(rest.includes('--yes') ? ['--yes'] : [])]);
    break;
  }
  case 'install-snippet': {
    // 0.17.0：把操作规程写进指定项目的 AGENTS.md/CLAUDE.md（0.23 起管线抽为 runInstallSnippet，install --host 共用）。
    runInstallSnippet(rest);
    break;
  }
  case 'install-hooks': {
    // A：自动接线（**用户自主选择**）。默认只做 dry-run 展示「会做什么」，
    // 必须显式加 --yes 才真正写入；写入前自动备份宿主配置。
    const r = await installHooks({ args: rest, yes: rest.includes('--yes') });
    console.log(r.text);
    if (r.wrote) console.log('\n[pi-evox] 已写入。按宿主要求重启/刷新后生效（OpenClaw 通常需重启网关，Hermes 需刷新 allowlist）。');
    else console.log('\n[pi-evox] 未做任何改动（演练模式）。确认无误后加 --yes 才会写入。');
    process.exit(r.code);
    break;
  }
  case 'config': {
    // C 的开关：查看 / 修改「自己沉淀的基因是否自动通过审核」（默认开）
    // 注意：开关名以 `--` 开头，不能只看 positional（它会被过滤掉）
    const i = rest.indexOf('--auto-approve');
    const cur = readConfig();
    const def = typeof cur.autoApprove === 'boolean' ? cur.autoApprove : true;
    if (i < 0) {
      console.log(`配置文件    : ${CONFIG_FILE}`);
      console.log(`autoApprove : ${def}（自己沉淀的基因${def ? '自动通过，立即可注入' : '需人工 approve'}）`);
      console.log(`当前判定    : ${autoApproveState(rest)}`);
      break;
    }
    const v = String(rest[i + 1] || 'on').toLowerCase();
    if (v !== 'on' && v !== 'off') fail('用法: light-cli.mjs config --auto-approve on|off', { errCode: 'E_ARGS' });
    const on = v === 'on';
    writeConfig({ autoApprove: on });
    console.log(`[pi-evox] autoApprove 已设为 ${on}${on ? '' : '（此后沉淀需人工 approve）'}`);
    break;
  }
  case 'starter': {
    // D：一键装载起步基因包（让新用户第一次任务就能命中）
    const file = path.join(__CODE_DIR, '..', 'assets', 'starter-genes.jsonl');
    if (!fs.existsSync(file)) fail(`未找到起步包：${file}`, { code: 1, errCode: 'E_NOTFOUND' });
    console.log(`[pi-evox] 装载起步基因包（${file}）…`);
    const { runGene } = await import('../../.././gene_share.mjs');
    const code = runGene(['import', file, '--tier', 'official']);
    if (code === 0) console.log('\n[pi-evox] 起步包已装载。现在跑一次召回试试：\n  node code/evolver-recall.mjs --query "读取中文日志报 UnicodeDecodeError"');
    process.exit(code);
    break;
  }
  case 'gene': {
    // 共享基因库（0.14.9）：export / submit / import，全部经脱敏闸门
    const { runGene } = await import('../../.././gene_share.mjs');
    const __rg = runGene(rest);
    if (__rg && typeof __rg.then === 'function') __rg.then((c) => process.exit(typeof c === 'number' ? c : 0));
    else process.exit(typeof __rg === 'number' ? __rg : 0);
    break;
  }
  case 'demo': {
    // 0.23 U2：90 秒自演示——新用户零文档成本看到「经验继承」的完整瞬间。
    // 只读设计（不加 --yes 不改任何用户状态；库空时提示先跑 starter）。
    const { spawnSync: ss } = await import('node:child_process');
    const self = process.argv[1];
    console.log('── Pi EvoX demo：90 秒看懂经验继承 ──');
    console.log('[1/3] 环境自检');
    let r = ss(process.argv[0], [self, 'doctor'], { encoding: 'utf8' });
    if (r.status !== 0) { console.log(r.stdout || 'doctor 未通过——先解决环境问题'); process.exit(r.status || 1); }
    console.log('[2/3] 模拟一个编码报错（对靶召回）');
    r = ss(process.argv[0], [path.join(path.dirname(self), 'evolver-recall.mjs'), '--error', "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4"], { encoding: 'utf8' });
    const recallOut = (r.stdout || '');
    console.log(recallOut.trim().split('\n').slice(0, 6).join('\n'));
    const hit = /\[#\d+\|/.test(recallOut);
    console.log(hit
      ? '  ↑ 上面的编号修法就是本机经验库对靶命中的结果——**下次同类报错，agent 会直接看到它**。'
      : '  ↑ 本次无命中（库空或未对靶）——先跑 `starter` 装起步包，或沉淀一条自己的修法（`draft --error`）。');
    console.log('[3/3] 下一步');
    console.log('  - 看全库：light-cli.mjs info / timeline');
    console.log('  - 接入宿主：light-cli.mjs install <claude-code|cursor|codex|agents-md>');
    console.log('  - 沉淀你的第一条：light-cli.mjs draft --error "<真实报错>"');
    break;
  }
    default:
      return false;
  }
  return true;
}
