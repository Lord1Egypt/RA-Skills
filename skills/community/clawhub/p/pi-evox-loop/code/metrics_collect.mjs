import fs from 'node:fs';
import path from 'node:path';
// 公共仓库：禁止硬编码私有绝对路径，全部改为可配置环境变量（带合理默认值）。
//   EVOX_ROOT         部署根目录，默认 $HOME/pi-evox-lab
//   EVOX_STORE_DIR    基因库目录，默认 $HOME/.evomap/assets
//   EVOX_HERMES_USAGE Hermes 使用统计文件，默认 $HOME/.hermes/skills/.usage.json
const HOME = process.env.HOME || (process.env.USERPROFILE || '/root');
const ROOT = process.env.EVOX_ROOT || path.join(HOME, 'pi-evox-lab');
const STORE = process.env.EVOX_STORE_DIR || path.join(HOME, '.evomap', 'assets');
const LOG = path.join(ROOT, 'exp/metrics/metrics.log');
// 与 evolver-recall.mjs 对齐：命中/召回埋点统一走 EVOX_HITS_DIR，缺省回退 cwd/experiments，
// 避免 metrics_collect 在 WORKDIR≠$HOME/pi-evox-lab（如 Windows 工作副本）时读到错误路径，
// 导致 recallCalls/hits 计数恒为 0（实际埋点文件已在 cwd/experiments/ 正常增长）。
const HITS_DIR = process.env.EVOX_HITS_DIR || path.join(process.cwd(), 'experiments');
const countLines = (p) => { try { return fs.readFileSync(p,'utf8').split('\n').filter(l=>l.trim()).length; } catch { return 0; } };
// 追加式台账 ⇒ 审核态以「每个 assetId 的最后一条状态」为准（last-write-wins）。
// 修复（2026-09-23）：旧实现对「历史行」计数（l.includes('"state":"approved"')），会把「已 approved
// 后又 quarantine」的资产仍计为 approved，导致 approved 高报、quarantined 少报（实测生产库 23 vs 13）。
const latestReview = () => {
  const latest = new Map();
  try {
    for (const l of fs.readFileSync(path.join(STORE,'review.jsonl'),'utf8').split('\n')) {
      const s = l.trim(); if (!s) continue;
      try { const r = JSON.parse(s); if (r && r.assetId) latest.set(String(r.assetId), r.state); } catch { /* 坏行跳过 */ }
    }
  } catch { /* 台账不存在 → 空 */ }
  return latest;
};
const review = latestReview();
const countLatest = (kw) => [...review.values()].filter(s=>typeof s==='string' && s.toLowerCase().includes(kw)).length;
const genes = countLines(path.join(STORE,'genes.jsonl'));
const approved = countLatest('approv');
const quarantined = countLatest('quarant');
const hits = countLines(path.join(HITS_DIR,'hits.jsonl'));
const recallCalls = countLines(path.join(HITS_DIR,'recall_calls.jsonl'));
let hermes = 'absent';
try {
  const u = JSON.parse(fs.readFileSync(process.env.EVOX_HERMES_USAGE || path.join(HOME, '.hermes/skills/.usage.json'),'utf8'));
  const e = u['pi-evox-loop'];
  hermes = e ? 'view='+(e.view_count??0)+' use='+(e.use_count??0)+' last='+(e.last_used_at??'never') : 'absent';
} catch {}
const ts = new Date().toISOString();
const line = ts+' genes='+genes+' approved='+approved+' quarantined='+quarantined+' hits='+hits+' recallCalls='+recallCalls+' hermes=['+hermes+']';
fs.mkdirSync(path.dirname(LOG), {recursive:true});
fs.appendFileSync(LOG, line+'\n');
console.log(line);
