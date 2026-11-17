#!/usr/bin/env node
// map.mjs — 生成并在地图（高德地图）上可视化聚合决策房源
// 用法:
//   node scripts/map.mjs        # 生成单文件静态页面 data/map.html
//   npm run map                 # 快捷方式
//
// 页面是纯静态的：数据内联进 HTML，不起任何本地服务，也不接受写请求。
// 要改需求画像，在页面里导出 YAML，然后让 agent 写回 config/profile.yml。

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { collectReports, parseWatchlist, effectiveProvenance, num } from './lib/data.mjs';
import { parseProfile } from './lib/profile.mjs';
import { loadGeoCache } from './lib/geo.mjs';
import { decide, isUserExcluded } from './lib/decision.mjs';
import { renderMapHtml } from './lib/map-html.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const GEO_CACHE_PATH = join(ROOT, 'data', 'geo-cache.json');
const PROFILE_PATH = join(ROOT, 'config', 'profile.yml');
const DEFAULT_OUT_PATH = join(ROOT, 'data', 'map.html');

// 命令行参数解析
const args = process.argv.slice(2);
const isHelp = args.includes('--help') || args.includes('-h');

if (isHelp) {
  console.log(`
house-ops 地图决策中枢

用法:
  node scripts/map.mjs        # 生成静态页面 data/map.html
  npm run map                 # 快捷方式

选项:
  --out <file>   自定义生成的 HTML 输出路径 (默认: data/map.html)
  --help, -h     查看帮助说明

页面是纯静态的：数据内联在 HTML 里，不起本地服务、不接受写请求。
要修改需求画像，请在页面里导出 YAML，再交给 agent 写回 config/profile.yml。
`);
  process.exit(0);
}

// --serve 已移除：本地服务会暴露画像数据，改为纯静态页面（迁移期给出明确提示）
if (args.includes('--serve')) {
  console.log('⚠️  --serve 已移除：地图现在是纯静态页面，不再启动本地服务。');
  console.log('    直接打开生成的 data/map.html 即可；修改画像请在页面导出 YAML 后交给 agent。');
  process.exit(1);
}

let outPath = DEFAULT_OUT_PATH;
const outIdx = args.indexOf('--out');
if (outIdx !== -1 && args[outIdx + 1]) {
  outPath = resolve(process.cwd(), args[outIdx + 1]);  // resolve：绝对路径按绝对语义处理
}

// 聚合数据加载
async function loadFullData() {
  let geoCache = await loadGeoCache(GEO_CACHE_PATH);
  if (Object.keys(geoCache).length === 0) {
    geoCache = await loadGeoCache(join(ROOT, 'data', '.geo-cache.json'));
  }

  const [reports, watchlist, rawProfile] = await Promise.all([
    collectReports(join(ROOT, 'reports')),
    parseWatchlist(join(ROOT, 'data', 'watchlist.md')),
    readFile(PROFILE_PATH, 'utf8').catch(() => ''),
  ]);

  const parsedProfile = parseProfile(rawProfile);

  // 备注与地理坐标补充到报告列表中
  // 真实性（ADR-0002）：⛔作废报告已在 data 层过滤不上图；真实性折叠唯一出口 effectiveProvenance
  const watchMap = new Map((watchlist || []).map(w => [w.no, w]));
  const mergedReports = reports
    .map(r => {
      const w = watchMap.get(r.report_no);
      const key = [r.city, r.district, r.community].filter(Boolean).join('·');
      const coords = r.coords || geoCache[key] || geoCache[r.community] || null;
      const wScore = w ? num(w.score) : null;
      const note = w ? w.note : '';
      return {
        ...r,
        coords,
        score_global: (w && wScore != null) ? wScore : (r.score_global ?? null),
        risk_tier: r.risk_tier ?? (w?.risk ?? ''),
        watchlist_note: note,
        user_excluded: isUserExcluded(note),
        authenticity: effectiveProvenance(r, w),
      };
    })
    // 决策分层服务端预计算（scripts/lib/decision.mjs 唯一实现），页面 JS 只渲染
    .map(h => ({ ...h, decision: decide(h) }));

  return {
    reports: mergedReports,
    watchlist: watchlist || [],
    // 工作锚点由画像驱动（buyer.work_location_coords = [经度, 纬度]，intake 采集或地图页写入）；
    // 未设置时地图不绘制锚点与通勤圈，不内置任何默认位置
    workAnchor: {
      coords: (parsedProfile && parsedProfile.buyer && parsedProfile.buyer.work_location_coords) || null,
      label: (parsedProfile && parsedProfile.buyer && parsedProfile.buyer.work_location) || '',
    },
    profile: parsedProfile,
    rawYaml: rawProfile,
    geoCache,
    amapKey: process.env.AMAP_KEY || '',
    amapSecurity: process.env.AMAP_SECURITY || '',
  };
}

async function main() {
  const data = await loadFullData();
  const html = renderMapHtml({ initialData: data });

  // 确保目录存在并写入静态 HTML
  await mkdir(dirname(outPath), { recursive: true });
  await writeFile(outPath, html, 'utf8');
  console.log(`✅ 地图决策页面已生成: ${outPath}`);
  console.log(`💡 直接在浏览器中打开该文件即可；房源数据有更新时重新运行 npm run map。`);
  console.log(`🔒 页面纯静态：不起本地服务，也不接受任何写请求。`);
}

main().catch(err => {
  console.error('生成地图失败:', err);
  process.exit(1);
});
