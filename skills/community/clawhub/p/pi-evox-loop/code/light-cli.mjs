#!/usr/bin/env node
// 0.42 O07：默认不向用户暴露堆栈，仅在 EVOX_DEBUG=1 时输出诊断（必须位于 shebang 之后）。
process.on('uncaughtException', (e) => {
  console.error('[pi-evox] E_INTERNAL：命令执行异常，请重试或检查输入；恢复建议：先运行 node code/light-cli.mjs doctor');
  if (process.env.EVOX_DEBUG === '1') console.error(e && e.stack ? e.stack : e);
  process.exit(1);
});
/**
 * light-cli.mjs — 内置 light 后端命令行（零 npm 依赖）
 *
 * 0.34 重构：本文件只负责「解析 argv → 派发到 engine/light/commands/<域>.mjs」。
 * 命令实现与共享 helpers 均已下沉，主入口保持精简。
 *
 * 用法：
 *   node code/light-cli.mjs distill --signals bash,encoding-error \
 *        --strategy "..." --summary "..."
 *   node code/light-cli.mjs approve <gene_id>
 *   node code/light-cli.mjs list
 *   node code/light-cli.mjs info
 */
import * as shared from './engine/light/shared.mjs';

const [cmd, ...rest] = process.argv.slice(2);
const ctx = { ...shared, rest };

const LOADERS = {
  distill: () => import('./engine/light/commands/deposit.mjs'),
  'fix-signals': () => import('./engine/light/commands/deposit.mjs'),
  draft: () => import('./engine/light/commands/deposit.mjs'),
  approve: () => import('./engine/light/commands/review.mjs'),
  quarantine: () => import('./engine/light/commands/review.mjs'),
  list: () => import('./engine/light/commands/review.mjs'),
  feedback: () => import('./engine/light/commands/review.mjs'),
  shareable: () => import('./engine/light/commands/provenance.mjs'),
  identity: () => import('./engine/light/commands/provenance.mjs'),
  verify: () => import('./engine/light/commands/provenance.mjs'),
  resign: () => import('./engine/light/commands/provenance.mjs'),
  'gene-pull-trust': () => import('./engine/light/commands/provenance.mjs'),
  timeline: () => import('./engine/light/commands/forensics.mjs'),
  evidence: () => import('./engine/light/commands/forensics.mjs'),
  harvest: () => import('./engine/light/commands/forensics.mjs'),
  session: () => import('./engine/light/commands/forensics.mjs'),
  report: () => import('./engine/light/commands/forensics.mjs'),
  'export-evidence': () => import('./engine/light/commands/forensics.mjs'),
  stats: () => import('./engine/light/commands/forensics.mjs'),
  doctor: () => import('./engine/light/commands/setup.mjs'),
  info: () => import('./engine/light/commands/setup.mjs'),
  snippet: () => import('./engine/light/commands/setup.mjs'),
  license: () => import('./engine/light/commands/setup.mjs'),
  install: () => import('./engine/light/commands/setup.mjs'),
  'install-snippet': () => import('./engine/light/commands/setup.mjs'),
  'install-hooks': () => import('./engine/light/commands/setup.mjs'),
  config: () => import('./engine/light/commands/setup.mjs'),
  starter: () => import('./engine/light/commands/setup.mjs'),
  gene: () => import('./engine/light/commands/setup.mjs'),
  demo: () => import('./engine/light/commands/setup.mjs'),
};

if (!cmd) {
  ctx.usage();
  process.exit(0);
}

const loader = LOADERS[cmd];
if (!loader) {
  ctx.fail(`未知命令：${cmd}`, { hint: '运行不带参数查看完整用法', errCode: 'E_USAGE' });
  ctx.usage();
  process.exit(0);
}

await (await loader()).run(cmd, rest, ctx);
