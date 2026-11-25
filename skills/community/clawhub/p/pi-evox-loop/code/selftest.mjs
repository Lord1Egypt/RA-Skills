// selftest.mjs — 脱敏随包自检（D06 / J14）
// 随包发布，不含任何恶意样本原文；只验证「扫描器在线 + 合法文本零误杀」并产出可验证制品（stdout JSON）。
// 与完整回归的关系（0.43 O03 明示）：本文件 = 快速哨兵自检；完整逐条断言（31 恶意 + 11 合法）
// injection-regression 完整套件按设计不随包分发（发布门禁每版实测）；本文件是快速哨兵——文档引用的回归数字以门禁用 injection-regression 套件实测为准。
// 用法: node code/selftest.mjs   → 退出码 0 = 全绿；2 = 自检失败（验收项应 hold delivery）。
import crypto from 'node:crypto';
import { injectionScan, scanAll, splitAvoidFix } from './injection_scan.mjs';

const LEGIT = [
  '请帮我把 GBK 编码的日志文件解码为 UTF-8 并统计行数',
  'The JSON payload is malformed; parse it defensively and report the field',
  'Run node --check on every .mjs file before publishing',
];
const genes = LEGIT.map((summary) => ({ summary, strategy: [], signals_match: [] }));
const falsePositives = scanAll(genes).length;
// 哨兵：函数仍引用规则表（被改空的扫描器会是恒真 stub）；完整恶意样本验证在本地 C38 套件。
const guardOnline = typeof injectionScan === 'function' && typeof splitAvoidFix === 'function'
  && /PATTERNS/.test(injectionScan.toString());
const payload = {
  tool: 'pi-evox selftest', version: '0.44.0', guard_online: guardOnline,
  legit_samples: genes.length, false_positives: falsePositives,
  sentinel: 'rules referenced; no malicious samples shipped',
};
payload.sha256 = crypto.createHash('sha256').update(JSON.stringify(payload)).digest('hex').slice(0, 16);
console.log(JSON.stringify(payload, null, 2));
// 制品 = stdout（结果 + 哨兵 + 哈希 + 退出码）；不写文件 → 无运行时埋点残留。
process.exit(guardOnline && falsePositives === 0 ? 0 : 2);
