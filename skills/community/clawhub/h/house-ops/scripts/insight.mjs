#!/usr/bin/env node
// insight.mjs — 物理交叉验证：日照 / 交通噪音 / 通勤 / 建筑轮廓（零依赖，Node ≥18）
// 所有输出均为 [推算] 档位：用于排除与排序，最终以带看实测为准。
// 方法论与精度评估（2026-09-09 实测）见 modes/scan.md「物理交叉验证」节。
//
// 子命令:
//   sun    --lat 31.23 --spacing 45 --south-floors 18 --floors 6-8 [--date 2027-01-20]
//          大寒日/冬至日照估算：正午+9/15时太阳高度角 → 各楼层遮挡判定（GB 50180 大寒日≥2h）
//   noise  --lat 31.05 --lng 121.24 [--radius 300]
//          OSM 道路/铁路等级 + 线声源衰减模型 → 昼间 dB 估算与 GB 3096 限值对照
//   spacing --lat 31.05 --lng 121.24 [--radius 400]
//          Overpass API 建筑轮廓表（距离/层数）——OSM 层数标注率低，输出供人工对照
//   commute --from 121.592,31.252 --to 121.2386,31.0542 [--peak 1.6]
//          OSRM 免费实例车行时间 × 高峰系数（公共交通不可用，走浏览器高德）

import { num } from './lib/data.mjs';
const SUN_TAB = { '2027-01-20': '大寒日', '2026-12-21': '冬至日' };
const D2R = Math.PI / 180;

// NOAA 简化太阳位置算法（2026-09-09 实测 vs 公开天文值误差 <0.3°）
function noonElevationAndDecl(latDeg, dateStr) {
  const d = (new Date(dateStr + 'T12:00:00+08:00') - new Date('2000-01-01T12:00:00Z')) / 86400000;
  const g = ((357.529 + 0.98560028 * d) % 360) * D2R;
  const q = (280.459 + 0.98564736 * d) % 360;
  const L = (q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * D2R;
  const e = (23.439 - 0.00000036 * d) * D2R;
  const dec = Math.asin(Math.sin(e) * Math.sin(L)) * 180 / Math.PI;
  const latR = latDeg * D2R;
  const elev = Math.asin(Math.sin(latR) * Math.sin(dec * D2R) + Math.cos(latR) * Math.cos(dec * D2R)) * 180 / Math.PI;
  return { dec, elev };
}
// 任意时刻太阳高度角（时角 ω = 15°×(小时-12)）
function elevationAt(latDeg, dec, hour) {
  const latR = latDeg * D2R;
  const w = (hour - 12) * 15 * D2R;
  return Math.asin(Math.sin(latR) * Math.sin(dec * D2R) + Math.cos(latR) * Math.cos(dec * D2R) * Math.cos(w)) * 180 / Math.PI;
}


// Overpass 多镜像轮询（主站限频时自动降级，全部失败才报错）
const OVERPASS_MIRRORS = [
  'https://overpass-api.de/api/interpreter',
  'https://overpass.kumi.systems/api/interpreter',
  'https://overpass.private.coffee/api/interpreter',
];
async function overpassQuery(query, attempts = 2) {
  let lastErr;
  for (let round = 0; round < attempts; round++) {
    if (round > 0) await new Promise(r => setTimeout(r, 1500 * round)); // 退避：1.5s / 3s
    for (const base of OVERPASS_MIRRORS) {
      try {
        const res = await fetch(`${base}?data=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const text = await res.text();
        if (text.trim().startsWith('<')) throw new Error('非 JSON 响应（限频页）');
        return JSON.parse(text);
      } catch (err) { lastErr = err; }
    }
  }
  throw lastErr ?? new Error('全部镜像失败');
}
function argVal(argv, key, dflt = null) {
  const i = argv.indexOf(key);
  if (i < 0) return dflt;
  const v = argv[i + 1];
  return v && !v.startsWith('--') ? v : dflt;
}

// ---------- sun ----------
function cmdSun(argv) {
  const lat = num(argVal(argv, '--lat')) ?? 31.23;
  const spacing = num(argVal(argv, '--spacing'));
  const southFloors = num(argVal(argv, '--south-floors'));
  const floors = String(argVal(argv, '--floors', '1-1'));
  const date = argVal(argv, '--date', '2027-01-20');
  const label = SUN_TAB[date] ?? `自定义日期 ${date}`;
  if (!spacing || !southFloors) {
    console.error('用法: node scripts/insight.mjs sun --lat 31.23 --spacing 45 --south-floors 18 --floors 6-8 [--date 2027-01-20]');
    process.exit(1);
  }
  const fm = floors.match(/(\d+)(?:-(\d+))?/);
  const f1 = num(fm?.[1]) ?? 1;
  const f2 = num(fm?.[2]) ?? f1;
  const { dec, elev: noonElev } = noonElevationAndDecl(lat, date);
  const Hs = southFloors * 3; // 南楼高度（3m/层，估）
  const shadowLen = Hs / Math.tan(noonElev * D2R);

  console.log(`【推算】${label} 日照估算（上海 φ=31.23N，南楼 ${southFloors}F≈${Hs}m，楼间距 ${spacing}m，本套 ${f1}${f2 !== f1 ? '-' + f2 : ''} 层）`);
  console.log(`  ${label}正午太阳高度角 ${noonElev.toFixed(1)}°，南楼影长 ${shadowLen.toFixed(0)}m`);
  console.log(`  GB 50180 标准：大寒日日照 ≥2 小时（有效日照带 8:00-16:00）`);
  const hours = [9, 10, 11, 12, 13, 14, 15];
  console.log('  楼层  9时   12时   15时   估算日照');
  for (let f = f1; f <= f2; f++) {
    const sill = (f - 1) * 3 + 0.9; // 窗台高（估）
    let lit = 0;
    const marks = hours.map((h) => {
      const elev = elevationAt(lat, dec, h);
      const shadeTop = Hs - spacing * Math.tan(elev * D2R); // 该时刻遮挡线高度
      const shaded = shadeTop > sill;
      if (!shaded) lit++;
      return shaded ? '□' : '■';
    }).join('');
    const band = lit >= 5 ? '充足' : lit >= 3 ? '尚可' : lit >= 2 ? '临界(≈2h)' : '不足(<2h)';
    console.log(`  ${String(f).padStart(3)}F  ${marks}    ${band}`);
  }
  console.log('  □=被南楼遮挡 ■=有日照；[推算]档位——楼间距建议卫星图复核，最终带看实测');
}

// ---------- noise ----------
const NOISE_REF = [ // [OSM highway 正则, 基准 dB@20m, 名称]
  [/^motorway|^motorway_link/, 75, '高速/快速路'],
  [/^trunk/, 73, '国道/主干道'],
  [/^primary/, 70, '主干道'],
  [/^secondary/, 65, '次干道'],
  [/^tertiary/, 60, '支路'],
];
const RAILWAY_DB = 78; // 铁路基准 dB@20m
const GB3096 = [ ['4a类(主干道旁)', 70], ['3类(工业区)', 65], ['2类(居住)', 60] ];

function cmdNoise(argv) {
  const lat = num(argVal(argv, '--lat'));
  const lng = num(argVal(argv, '--lng'));
  const radius = num(argVal(argv, '--radius')) ?? 300;
  if (!lat || !lng) { console.error('用法: node scripts/insight.mjs noise --lat 31.05 --lng 121.24 [--radius 300]'); process.exit(1); }
  const q = `[out:json][timeout:25];(way["highway"~"motorway|trunk|primary|secondary|tertiary"](around:${radius},${lat},${lng});way["railway"~"rail|light_rail"](around:${radius},${lat},${lng}););out geom;`;
  console.log(`【推算】交通噪音评估（${lat},${lng} 半径 ${radius}m，简化线声源模型 ±5dB）`);
  overpassQuery(q).then(d => {
    const ways = (d.elements ?? []).filter(e => e.type === 'way' && e.geometry);
    const rows = [];
    for (const w of ways) {
      const t = w.tags ?? {};
      const la1 = lat * D2R, lo1 = lng * D2R;
      let best = 1e9;
      for (const pt of w.geometry) {
        const la2 = pt.lat * D2R, lo2 = pt.lon * D2R;
        const a = Math.sin((la2 - la1) / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin((lo2 - lo1) / 2) ** 2;
        best = Math.min(best, 2 * 6371000 * Math.asin(Math.sqrt(a)));
      }
      const isRail = Boolean(t.railway);
      const ref = NOISE_REF.find(([re]) => re.test(t.highway ?? ''));
      const db20 = isRail ? RAILWAY_DB : (ref ? ref[1] : null);
      if (db20 == null) continue;
      const db = Math.round(db20 - 10 * Math.log10(Math.max(best, 20) / 20)); // 线声源：距离倍增约 -3dB
      rows.push({ kind: isRail ? '铁路/轨道' : (ref ? ref[2] : t.highway), name: t.name ?? '无名', dist: Math.round(best), db });
    }
    if (!rows.length) { console.log('  ✅ 半径内未发现主干道以上道路或铁路——噪音预期良好（仍需带看实测）'); return; }
    rows.sort((a, b) => a.dist - b.dist);
    const worst = rows.reduce((a, b) => (b.db > a.db ? b : a), rows[0]);
    console.log('  最近噪音源（按距离排序，最多 6 条）:');
    for (const r of rows.slice(0, 6)) console.log(`    ${r.kind}「${r.name}」 ${r.dist}m ≈ ${r.db}dB(昼间推算)`);
    const gb = GB3096.find(([, lim]) => worst.db <= lim);
    console.log(`  主导源: ${worst.kind} ${worst.db}dB → ${gb ? gb[0] : '超 4a 类限值'}（昼间限值 ${gb ? gb[1] : 70}dB）`);
    console.log('  ⚠ 规划中道路/铁路不在 OSM——政府公示另行核查；噪音敏感户带看分贝计实测');
  }).catch((e) => { console.error('⛔ Overpass 查询失败:', e.message); process.exit(1); });
}

// ---------- spacing ----------
function cmdSpacing(argv) {
  const lat = num(argVal(argv, '--lat'));
  const lng = num(argVal(argv, '--lng'));
  const radius = num(argVal(argv, '--radius')) ?? 400;
  if (!lat || !lng) { console.error('用法: node scripts/insight.mjs spacing --lat 31.05 --lng 121.24 [--radius 400]'); process.exit(1); }
  const q = `[out:json][timeout:25];(way["building"](around:${radius},${lat},${lng}););out geom;`;
  console.log(`【推算】${lat},${lng} 半径 ${radius}m 建筑轮廓（OSM 覆盖度有限——层数标注常缺失，间距建议高德卫星图测距复核）`);
  overpassQuery(q).then(d => {
    const ways = (d.elements ?? []).filter(e => e.type === 'way' && e.geometry);
    const la1 = lat * D2R, lo1 = lng * D2R;
    const rows = [];
    for (const w of ways) {
      let best = 1e9;
      for (const pt of w.geometry) {
        const la2 = pt.lat * D2R, lo2 = pt.lon * D2R;
        const a = Math.sin((la2 - la1) / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin((lo2 - lo1) / 2) ** 2;
        best = Math.min(best, 2 * 6371000 * Math.asin(Math.sqrt(a)));
      }
      const lv = w.tags?.['building:levels'];
      rows.push({ dist: Math.round(best), levels: lv ? Number(lv) : null, name: w.tags?.name ?? '' });
    }
    rows.sort((a, b) => a.dist - b.dist);
    console.log(`  轮廓 ${rows.length} 条，含层数标注 ${rows.filter(r => r.levels).length} 条:`);
    for (const r of rows.slice(0, 12)) console.log(`    ${r.dist}m | ${r.levels ? r.levels + '层≈' + r.levels * 3 + 'm' : '层数未知'} | ${r.name || '(无名)'}`);
  }).catch((e) => { console.error('⛔ Overpass 查询失败:', e.message); process.exit(1); });
}

// ---------- commute ----------
function cmdCommute(argv) {
  const from = argVal(argv, '--from');
  const to = argVal(argv, '--to');
  const peak = num(argVal(argv, '--peak')) ?? 1.6;
  const parseLL = (s) => { const [lng, lat] = String(s ?? '').split(',').map(Number); return (Number.isFinite(lat) && Number.isFinite(lng)) ? `${lng},${lat}` : null; };
  const a = parseLL(from), b = parseLL(to);
  if (!a || !b) { console.error('用法: node scripts/insight.mjs commute --from lng,lat --to lng,lat [--peak 1.6]'); process.exit(1); }
  const url = `http://router.project-osrm.org/route/v1/driving/${a};${b}?overview=false`;
  console.log(`【推算】车行通勤（OSRM 自由流 × 高峰系数 ${peak}；公共交通请走浏览器高德）`);
  fetch(url).then(r => r.json()).then(d => {
    const r0 = d.routes?.[0];
    if (!r0) { console.error('⛔ OSRM 未返回路线'); process.exit(1); }
    const km = r0.distance / 1000;
    const free = r0.duration / 60;
    console.log(`  距离 ${km.toFixed(1)}km · 自由流 ${free.toFixed(0)} 分钟 · 早高峰估算 ${Math.round(free * peak)} 分钟`);
  }).catch((e) => { console.error('⛔ OSRM 查询失败:', e.message); process.exit(1); });
}

// 任意日期/时刻的太阳高度角（度）：dateStr=YYYY-MM-DD，hour=当地时(24h 制)
export function solarElevation(latDeg, dateStr, hour = 12) {
  const { dec } = noonElevationAndDecl(latDeg, dateStr);
  return elevationAt(latDeg, dec, hour);
}
export function noiseLevelAt(db20, distM) {          // 线声源距离衰减
  return Math.round(db20 - 10 * Math.log10(Math.max(distM, 20) / 20));
}

const [cmd, ...argv] = process.argv.slice(2);
const main = { sun: cmdSun, noise: cmdNoise, spacing: cmdSpacing, commute: cmdCommute };
if (process.argv[1] && import.meta.url === (await import('node:url')).pathToFileURL(process.argv[1]).href) {
  if (!cmd || !main[cmd]) {
    console.error('用法: node scripts/insight.mjs <sun|noise|spacing|commute> …（详见本文件头注释与 modes/scan.md「物理交叉验证」）');
    process.exit(1);
  }
  main[cmd](argv);
}

