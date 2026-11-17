#!/usr/bin/env node
/**
 * 咪咕旅游资源查询 - 客户端脚本
 *
 * 用法：
 *   node migu_attraction_client.mjs --action top --city 成都市 [--area 武侯区] [--limit 10] [--json]
 *   node migu_attraction_client.mjs --action nearby --city 成都市 --area 武侯区 --names "成都武侯祠博物馆,锦里古街" [--json]
 *
 * 接口：
 *   POST https://gulangyu.migudm.cn/gallery/api/v1/attraction/top
 *   POST https://gulangyu.migudm.cn/gallery/api/v1/attraction/nearby
 */

const BASE = 'https://gulangyu.migudm.cn/gallery/api/v1/attraction';

const HEADERS = {
  'Content-Type': 'application/json',
  'X-APP-From': '10',
  'X-App-Version': '0.6.4',
  'Origin': 'https://gulangyu.migudm.cn',
  'Referer': 'https://gulangyu.migudm.cn/',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
};

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        out[key] = true;
      } else {
        out[key] = next;
        i++;
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}

const CITY_SUFFIXES = ['市', '区', '县', '州', '盟', '旗', '地区', '自治州', '自治县'];

/** 用户常直接说“成都”，接口需要“成都市”。缺后缀时补“市”。 */
function normalizeCity(city, noNormalize) {
  const c = String(city || '').trim();
  if (noNormalize) return c;
  if (!c) return c;
  if (CITY_SUFFIXES.some((s) => c.endsWith(s))) return c;
  return c + '市';
}

async function post(path, body) {
  const url = `${BASE}/${path}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`接口返回非 JSON（HTTP ${res.status}）：${text.slice(0, 300)}`);
  }
  if (json.success === false || (json.code !== undefined && json.code !== '0' && json.code !== 0)) {
    throw new Error(`接口报错：${json.msg || text.slice(0, 300)}（code=${json.code}）`);
  }
  return json.data;
}

function fmtRating(r) {
  if (r === null || r === undefined || r === '' || r === 'null') return '暂无评分';
  return `⭐${r}`;
}

function renderTop(city, area, limit, list) {
  const lines = [];
  const scope = area ? `${city} · ${area}` : city;
  lines.push(`## ${scope} 热门景点 Top${limit}`);
  lines.push('');
  if (!list || list.length === 0) {
    lines.push('（没有查询到景点，请确认城市/区县名称，例如「成都市」「武侯区」）');
    return lines.join('\n');
  }
  lines.push('| # | 景点 | 评分 | 级别 | 所在区县 | 营业时间 |');
  lines.push('|---|------|------|------|----------|----------|');
  list.forEach((it, i) => {
    lines.push(
      `| ${i + 1} | ${it.name || '-'} | ${fmtRating(it.rating)} | ${it.level || '-'} | ${it.area || '-'} | ${it.open || '待定'} |`
    );
  });
  return lines.join('\n');
}

function renderNearby(city, area, map) {
  const lines = [];
  lines.push(`## ${city} · ${area} 景点周边酒店 & 美食`);
  const keys = Object.keys(map || {});
  if (keys.length === 0) {
    lines.push('');
    lines.push('（没有查询到周边信息，请确认景点名称与所在城市/区县是否匹配）');
    return lines.join('\n');
  }
  for (const name of keys) {
    const d = map[name] || {};
    lines.push('');
    lines.push(`### 🎫 ${name}`);
    lines.push('');
    lines.push('**🏨 周边酒店**');
    lines.push('');
    lines.push('| 酒店 | 评分 | 类型 | 人均/参考价 | 距离 |');
    lines.push('|------|------|------|-------------|------|');
    const hotels = d.hotels || [];
    if (hotels.length === 0) lines.push('| 暂无 | - | - | - | - |');
    hotels.forEach((h) => {
      lines.push(
        `| ${h.name || '-'} | ${fmtRating(h.rating)} | ${h.level || '-'} | ${h.price && h.price !== '0' ? h.price + '元' : '待定'} | ${h.distance || '-'} |`
      );
    });
    lines.push('');
    lines.push('**🍜 周边美食**');
    lines.push('');
    lines.push('| 美食 | 评分 | 类型 | 人均 | 距离 |');
    lines.push('|------|------|------|------|------|');
    const foods = d.foods || [];
    if (foods.length === 0) lines.push('| 暂无 | - | - | - | - |');
    foods.forEach((f) => {
      lines.push(
        `| ${f.name || '-'} | ${fmtRating(f.rating)} | ${f.level || '-'} | ${f.price && f.price !== '0' ? f.price + '元' : '待定'} | ${f.distance || '-'} |`
      );
    });
  }
  return lines.join('\n');
}

function usage() {
  return [
    '咪咕旅游资源查询',
    '',
    '  景点 Top 查询：',
    '    node migu_attraction_client.mjs --action top --city 成都市 [--area 武侯区] [--limit 10] [--json]',
    '',
    '  周边酒店/美食查询：',
    '    node migu_attraction_client.mjs --action nearby --city 成都市 --area 武侯区 \\',
    '      --names "成都武侯祠博物馆,锦里古街" [--json]',
    '',
    '参数：',
    '  --action   top | nearby（必填）',
    '  --city     城市，可省略“市”后缀（自动补全）',
    '  --area     区县（top 选填；nearby 必填）',
    '  --limit    top 查询返回数量，默认 10',
    '  --names    nearby 的景点名称，逗号分隔（必填）',
    '  --json     输出原始 JSON',
  ].join('\n');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || args.h) {
    console.log(usage());
    return;
  }
  const action = args.action;
  const city = normalizeCity(args.city, args['no-normalize']);
  const area = args.area ? String(args.area).trim() : '';
  const asJson = !!args.json;

  if (action === 'top') {
    if (!city) throw new Error('缺少 --city（例如：--city 成都市）');
    const limit = args.limit ? parseInt(args.limit, 10) : 10;
    const body = { city, top: Number.isFinite(limit) && limit > 0 ? limit : 10 };
    if (area) body.area = area;
    const data = await post('top', body);
    if (asJson) {
      console.log(JSON.stringify({ action, request: body, data }, null, 2));
    } else {
      console.log(renderTop(city, area, body.top, data));
    }
    return;
  }

  if (action === 'nearby') {
    if (!city) throw new Error('缺少 --city（例如：--city 成都市）');
    if (!area) throw new Error('缺少 --area（例如：--area 武侯区）');
    const names = String(args.names || '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    if (names.length === 0) throw new Error('缺少 --names（例如：--names "成都武侯祠博物馆,锦里古街"）');
    const body = { city, area, names };
    const data = await post('nearby', body);
    if (asJson) {
      console.log(JSON.stringify({ action, request: body, data }, null, 2));
    } else {
      console.log(renderNearby(city, area, data));
    }
    return;
  }

  console.error('缺少或无效的 --action，可用值：top | nearby\n');
  console.error(usage());
  process.exitCode = 2;
}

main().catch((e) => {
  console.error('[migu-attraction-query] 出错：' + e.message);
  process.exitCode = 1;
});