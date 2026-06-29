#!/usr/bin/env node
/**
 * render-itinerary-map.js
 * 将行程节点渲染为高德地图可视化链接
 * 使用 curl（无 npm 依赖）
 *
 * 用法:
 * node scripts/render-itinerary-map.js --stops="成都|广元|昭化古城|明月峡|剑阁县" [--city=广元] [--region=四川省广元市] [--routeType=driving]
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// 高德 Web Service Key 读取
// 仅从环境变量或全局配置读取，不跨 skill 读取凭据
function getAmapKey() {
  const envKey = process.env.AMAP_WEBSERVICE_KEY;
  if (envKey) return envKey;

  return null;
}

// 地理编码：调用高德 API（4 策略兜底）
// region 为省市区县前缀，用于消除重名歧义（如 "北京市延庆区" 确保 "姜庄子村" 定位到正确的那个）
// city   为城市范围，作为 region 未命中时的二级兜底
async function geocode(address, key, region, city) {
  // 单次地理编码调用
  function tryGeocode(addr, cityParam) {
    const cityQuery = cityParam ? `&city=${encodeURIComponent(cityParam)}` : '';
    const url = `https://restapi.amap.com/v3/geocode/geo?address=${encodeURIComponent(addr)}&output=json&key=${key}${cityQuery}`;
    try {
      const res = execSync(`curl -s "${url}"`, { timeout: 10000 });
      const data = JSON.parse(res.toString());
      if (data.status === '1' && data.geocodes && data.geocodes.length > 0) {
        const loc = data.geocodes[0].location; // "经度,纬度"
        return loc.split(',').map(Number); // [lng, lat]
      }
    } catch (e) { /* ignore */ }
    return null;
  }

  let result;

  // 策略1（最高优先级）: region + address，消除重名歧义
  if (region) {
    result = tryGeocode(`${region}${address}`, region);
    if (result) return result;
  }

  // 策略2: city + address，城市级兜底
  if (city) {
    result = tryGeocode(`${city}${address}`, city);
    if (result) return result;
  }

  // 策略3: 裸 address 重试
  result = tryGeocode(address);
  if (result) return result;

  // 策略4: address + 后缀（景区/古镇/古城/国家公园/自然保护区）逐个重试
  const suffixes = ['景区', '古镇', '古城', '国家公园', '自然保护区'];
  for (const suffix of suffixes) {
    result = tryGeocode(`${address}${suffix}`);
    if (result) return result;
  }

  return null;
}

// 解析命令行参数
function parseArgs() {
  const args = {};
  process.argv.slice(2).forEach(arg => {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      args[key] = value || true;
    }
  });
  return args;
}

// ── 直接坐标模式：从 GPX/KML 提取的 GPS 坐标无需地理编码 ──

/**
 * 使用直接 GPS 坐标渲染地图（无需地理编码，精度最高）
 * --coords 接受 lat,lng 格式（GPX/KML 标准），内部转为 lng,lat 供高德 API 使用
 */
async function renderWithCoords(args, key) {
  // 解析坐标：优先用 | 分隔，回退到 , 分隔
  const rawCoords = args.coords.includes('|')
    ? args.coords.split('|')
    : args.coords.split(',');

  // --coords 使用 lat,lng 格式（GPX 标准），内部转为 [lng, lat] 供高德 API
  const coords = rawCoords.map(s => {
    const parts = s.trim().split(',');
    if (parts.length < 2) return null;
    // parts[0]=lat, parts[1]=lng → 转为 [lng, lat]
    const lat = parseFloat(parts[0]);
    const lng = parseFloat(parts[1]);
    if (isNaN(lat) || isNaN(lng)) return null;
    // 自动检测：如果第一个值 > 90（不可能是纬度），说明用户传了 lng,lat 格式
    // 此时直接使用原顺序（兼容旧格式）
    if (Math.abs(lat) > 90 && Math.abs(lng) <= 90) {
      return [lat, lng]; // 已经是 lng,lat
    }
    return [lng, lat]; // lat,lng → lng,lat
  }).filter(Boolean);

  // 解析名称（可选）
  let names = [];
  if (args.names) {
    const rawNames = args.names.includes('|')
      ? args.names.split('|')
      : args.names.split(',');
    names = rawNames.map(s => s.trim()).filter(Boolean);
  }

  if (coords.length < 2) {
    console.error('\n❌ 有效坐标不足，无法生成路线图');
    process.exit(1);
  }

  // 解析路线类型：支持逗号分隔的逐段路线类型
  let routeTypes = [];
  if (args.routeType) {
    routeTypes = args.routeType.split(',').map(s => s.trim()).filter(Boolean);
  }
  const defaultRouteType = routeTypes[0] || 'driving';

  console.log(`\n🗺️  正在渲染行程地图（GPS 直连模式，无需地理编码）...`);
  console.log(`⚠️  隐私提示：精确 GPS 坐标将通过网络发送给高德地图（Amap）API 以生成地图链接。`);
  console.log(`📍 GPS 坐标点: ${coords.length}`);
  if (routeTypes.length > 0) {
    console.log(`🛣️  路线类型: ${routeTypes.join(', ')}`);
  } else {
    console.log(`🛣️  路线类型: ${defaultRouteType} (默认)`);
  }
  console.log('');

  const mapTaskData = [];

  // 所有坐标点日志
  for (let i = 0; i < coords.length; i++) {
    const name = names[i] || `节点${i + 1}`;
    console.log(`  [${i + 1}/${coords.length}] ${name}: ${coords[i][1]?.toFixed(4) || '—'}, ${coords[i][0]?.toFixed(4) || '—'} (lat,lng)`);
  }

  if (coords.length > 2) {
    // GPX 轨迹模式：起点+终点 POI，polyline 轨迹线，单条路线规划
    const firstName = names[0] || '起点';
    const lastName = names[names.length - 1] || '终点';

    // 起点 POI
    mapTaskData.push({
      type: 'poi',
      lnglat: coords[0],
      sort: '起点',
      text: firstName,
      remark: 'GPX/KML 实测起点'
    });

    // 终点 POI
    mapTaskData.push({
      type: 'poi',
      lnglat: coords[coords.length - 1],
      sort: '终点',
      text: lastName,
      remark: 'GPX/KML 实测终点'
    });

    // Polyline 轨迹线（全部坐标点，GPX 实际轨迹）
    mapTaskData.push({
      type: 'polyline',
      path: coords,
      strokeColor: '#52c41a',
      strokeWeight: 4,
      strokeOpacity: 0.6,
      remark: `GPX 轨迹 (${coords.length}个点)`
    });

    // 路线规划：起点 → 终点
    const segRouteType = routeTypes[0] || defaultRouteType;
    mapTaskData.push({
      type: 'route',
      routeType: segRouteType,
      start: coords[0],
      end: coords[coords.length - 1],
      lineStyle: segRouteType === 'walking' ? 'dashed' : 'solid',
      remark: `轨迹路线: ${firstName} → ${lastName} (${segRouteType})`
    });
  } else {
    // 简单双点模式：两个 POI + 一条路线
    for (let i = 0; i < coords.length; i++) {
      const name = names[i] || `节点${i + 1}`;
      mapTaskData.push({
        type: 'poi',
        lnglat: coords[i],
        sort: `第${i + 1}站`,
        text: name,
        remark: 'GPX/KML 实测坐标'
      });
    }
    const poiCount = mapTaskData.length;
    for (let i = 0; i < poiCount - 1; i++) {
      const start = mapTaskData[i];
      const end = mapTaskData[i + 1];
      const segRouteType = routeTypes[i] || defaultRouteType;
      mapTaskData.push({
        type: 'route',
        routeType: segRouteType,
        start: start.lnglat,
        end: end.lnglat,
        lineStyle: segRouteType === 'walking' ? 'dashed' : 'solid',
        remark: `第${i + 1}段: ${start.text} → ${end.text} (${segRouteType})`
      });
    }
  }

  const baseUrl = 'https://a.amap.com/jsapi_demo_show/static/openclaw/travel_plan.html';
  const dataStr = encodeURIComponent(JSON.stringify(mapTaskData));
  const mapLink = `${baseUrl}?data=${dataStr}`;

  console.log('\n' + '═'.repeat(70));
  console.log('\n✅ 行程地图生成成功！（GPS 直连模式）\n');
  console.log('📋 数据摘要:');
  mapTaskData.filter(d => d.type === 'poi').forEach((poi, i) => {
    console.log(`   ${i + 1}. ${poi.text} (${poi.lnglat[0].toFixed(4)}, ${poi.lnglat[1].toFixed(4)}) ${poi.remark}`);
  });
  console.log(`\n🔗 地图链接:\n   ${mapLink}\n`);
  console.log('═'.repeat(70));

  if (process.env.OUTPUT_JSON) {
    console.log('\n---JSON---');
    console.log(JSON.stringify({ mapTaskData, mapLink }, null, 2));
  }
}

// 主函数
async function main() {
  const args = parseArgs();

  // ── GPS 直连模式（GPX/KML 提取的坐标，最高精度） ──
  if (args.coords) {
    const key = getAmapKey();
    if (!key) {
      console.error('❌ 未找到高德 Web Service Key');
      console.log('请设置环境变量: export AMAP_WEBSERVICE_KEY=你的Key');
      process.exit(1);
    }
    return renderWithCoords(args, key);
  }

  if (!args.stops) {
    console.error('❌ 缺少参数: --stops（节点列表，逗号或竖线分隔）');
    console.log('\n用法:');
    console.log('node render-itinerary-map.js --stops="成都,广元,昭化古城" [--city=广元] [--region=四川省广元市] [--routeType=driving]');
    console.log('node render-itinerary-map.js --coords="115.4,40.2|115.5,40.3" --names="起点|终点" [--routeType=driving]');
    console.log('\n地理编码模式参数:');
    console.log('  --stops     行程节点列表（必填，中文名称，用逗号或竖线分隔）');
    console.log('  --city       城市范围，用于提高地理编码精度（可选）');
    console.log('  --region     省市区县前缀（如 北京市延庆区），用于消除重名歧义（推荐）');
    console.log('  --routeType  路线类型: driving/walking/riding/transfer（默认: driving）');
    console.log('\nGPS 直连模式参数（GPX/KML）：');
    console.log('  --coords     GPS坐标列表（lat,lng 格式，用 | 分隔，无需地理编码）');
    console.log('               示例: --coords="40.566,115.746|40.575,115.755|40.554,115.775"');
    console.log('               也支持 lng,lat 格式（自动识别第一个值 > 90 时视为 lng,lat）');
    console.log('  --names      对应的节点名称列表（可选，用 | 或逗号分隔，默认自动编号）');
    console.log('  --routeType  路线类型（可逗号分隔指定每段类型）: driving/walking/riding/transfer');
    process.exit(1);
  }

  const key = getAmapKey();
  if (!key) {
    console.error('❌ 未找到高德 Web Service Key');
    console.log('请设置环境变量: export AMAP_WEBSERVICE_KEY=你的Key');

    process.exit(1);
  }

  const rawStops = args.stops.includes('|')
    ? args.stops.split('|')
    : args.stops.split(',');
  const stops = rawStops.map(s => s.trim()).filter(Boolean);
  // 解析路线类型：支持逗号分隔的逐段路线类型
  let routeTypes = [];
  if (args.routeType) {
    routeTypes = args.routeType.split(',').map(s => s.trim()).filter(Boolean);
  }
  const defaultRouteType = routeTypes[0] || 'driving';
  const region = args.region || '';
  const city = args.city || '';

  if (stops.length < 2) {
    console.error('❌ 节点数量不足，至少需要 2 个节点');
    process.exit(1);
  }

  console.log(`\n🗺️  正在渲染行程地图...`);
  console.log(`⚠️  隐私提示：行程站点名称将通过网络发送给高德地图（Amap）API 进行地理编码。`);
  console.log(`📍 节点数量: ${stops.length}`);
  if (region) console.log(`📍 定位范围: ${region}`);
  if (city) console.log(`🏙️  城市范围: ${city}`);
  if (routeTypes.length > 0) {
    console.log(`🛣️  路线类型: ${routeTypes.join(', ')}`);
  } else {
    console.log(`🛣️  路线类型: ${defaultRouteType} (默认)`);
  }
  console.log('');

  const mapTaskData = [];

  // 逐个地理编码并添加 POI 标记
  for (let i = 0; i < stops.length; i++) {
    const name = stops[i];
    process.stdout.write(`  [${i + 1}/${stops.length}] 地理编码: ${name} ... `);
    const coord = await geocode(name, key, region, city);
    if (coord) {
      mapTaskData.push({
        type: 'poi',
        lnglat: coord,
        sort: `第${i + 1}站`,
        text: name,
        remark: ''
      });
      console.log(`✅ ${coord[0].toFixed(4)}, ${coord[1].toFixed(4)}`);
    } else {
      console.log(`⚠️  未找到坐标`);
    }
  }

  if (mapTaskData.length < 2) {
    console.error('\n❌ 有效坐标不足，无法生成路线图');
    process.exit(1);
  }

  // 添加路线段（相邻节点之间，仅连接原始 POI）
  const poiCount = mapTaskData.length;
  for (let i = 0; i < poiCount - 1; i++) {
    const start = mapTaskData[i];
    const end = mapTaskData[i + 1];
    const segRouteType = routeTypes[i] || defaultRouteType;
    mapTaskData.push({
      type: 'route',
      routeType: segRouteType,
      start: start.lnglat,
      end: end.lnglat,
      lineStyle: segRouteType === 'walking' ? 'dashed' : 'solid',
      remark: `第${i + 1}段: ${start.text} → ${end.text} (${segRouteType})`
    });
  }

  // 生成可视化链接
  const baseUrl = 'https://a.amap.com/jsapi_demo_show/static/openclaw/travel_plan.html';
  const dataStr = encodeURIComponent(JSON.stringify(mapTaskData));
  const mapLink = `${baseUrl}?data=${dataStr}`;

  console.log('\n' + '═'.repeat(70));
  console.log('\n✅ 行程地图生成成功！\n');
  console.log('📋 数据摘要:');
  mapTaskData.filter(d => d.type === 'poi').forEach((poi, i) => {
    console.log(`   ${i + 1}. ${poi.text} (${poi.lnglat[0].toFixed(4)}, ${poi.lnglat[1].toFixed(4)})`);
  });
  console.log(`\n🔗 地图链接:\n   ${mapLink}\n`);
  console.log('═'.repeat(70));

  if (process.env.OUTPUT_JSON) {
    console.log('\n---JSON---');
    console.log(JSON.stringify({ mapTaskData, mapLink }, null, 2));
  }
}

main().catch(err => {
  console.error('\n❌ 执行失败:', err.message);
  process.exit(1);
});
