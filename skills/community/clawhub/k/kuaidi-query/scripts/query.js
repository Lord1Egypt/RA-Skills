#!/usr/bin/env node

/**
 * 快递查询脚本
 * 基于 Track123 API 实现实时物流信息查询
 * 
 * 支持：顺丰、圆通、中通、韵达、申通、EMS、京东、极兔等 200+ 家快递公司
 * 国际快递：DHL、FedEx、UPS、TNT 等
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');

// 配置路径 (在 skill 根目录)
const SKILL_ROOT = path.join(__dirname, '..');
const CONFIG_PATH = path.join(SKILL_ROOT, 'config.json');
const CACHE_PATH = path.join(SKILL_ROOT, '.cache.json');

// Track123 API 基础地址
const API_BASE = 'https://api.track123.com/gateway/open-api/tk/v2';

// 缓存时长 (毫秒)
const CACHE_DURATION = 3600000;

// 快递公司代码映射
const CARRIER_MAP = {
  // 国内快递
  'sf': { code: 'sfex', name: '顺丰速运', nameEn: 'SF Express' },
  'sf-express': { code: 'sfex', name: '顺丰速运', nameEn: 'SF Express' },
  'shunfeng': { code: 'sfex', name: '顺丰速运', nameEn: 'SF Express' },
  'yto': { code: 'yto', name: '圆通速递', nameEn: 'YTO Express' },
  'yuantong': { code: 'yto', name: '圆通速递', nameEn: 'YTO Express' },
  'zto': { code: 'zto', name: '中通快递', nameEn: 'ZTO Express' },
  'zhongtong': { code: 'zto', name: '中通快递', nameEn: 'ZTO Express' },
  'yunda': { code: 'yunda', name: '韵达速递', nameEn: 'Yunda Express' },
  'yundaex': { code: 'yunda', name: '韵达速递', nameEn: 'Yunda Express' },
  'sto': { code: 'sto', name: '申通快递', nameEn: 'STO Express' },
  'shentong': { code: 'sto', name: '申通快递', nameEn: 'STO Express' },
  'ems': { code: 'ems', name: '邮政 EMS', nameEn: 'EMS' },
  'youzheng': { code: 'ems', name: '邮政 EMS', nameEn: 'EMS' },
  'jd': { code: 'jd', name: '京东快递', nameEn: 'JD Express' },
  'jingdong': { code: 'jd', name: '京东快递', nameEn: 'JD Express' },
  'jt': { code: 'jt', name: '极兔速递', nameEn: 'J&T Express' },
  'jitu': { code: 'jt', name: '极兔速递', nameEn: 'J&T Express' },
  'cs': { code: 'cs', name: '菜鸟直送', nameEn: 'Cainiao Direct' },
  
  // 国际快递
  'dhl': { code: 'dhl', name: 'DHL', nameEn: 'DHL' },
  'fedex': { code: 'fedex', name: 'FedEx', nameEn: 'FedEx' },
  'ups': { code: 'ups', name: 'UPS', nameEn: 'UPS' },
  'tnt': { code: 'tnt', name: 'TNT', nameEn: 'TNT' },
  'sfint': { code: 'sfint', name: '顺丰国际', nameEn: 'SF International' },
  
  // 特殊命令
  'auto': { code: 'auto', name: '自动识别', nameEn: 'Auto Detect' },
  'carriers': { code: 'carriers', name: '快递公司列表', nameEn: 'Carrier List' }
};

/**
 * 加载配置
 */
function loadConfig() {
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      throw new Error('配置文件不存在：' + CONFIG_PATH + '\n请先复制 config.example.json 为 config.json 并填写 Track123 API Key');
    }
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  } catch (error) {
    console.error('❌ 配置加载失败:', error.message);
    process.exit(1);
  }
}

/**
 * 加载缓存
 */
function loadCache() {
  try {
    if (!fs.existsSync(CACHE_PATH)) {
      return {};
    }
    const cache = JSON.parse(fs.readFileSync(CACHE_PATH, 'utf-8'));
    const now = Date.now();
    const validCache = {};
    
    for (const [key, data] of Object.entries(cache)) {
      if (now - data.timestamp < data.duration) {
        validCache[key] = data;
      }
    }
    
    fs.writeFileSync(CACHE_PATH, JSON.stringify(validCache, null, 2));
    return validCache;
  } catch (error) {
    return {};
  }
}

/**
 * 保存缓存
 */
function saveCache(key, data, duration = CACHE_DURATION) {
  const cache = loadCache();
  cache[key] = {
    data,
    timestamp: Date.now(),
    duration
  };
  fs.writeFileSync(CACHE_PATH, JSON.stringify(cache, null, 2));
}

/**
 * 检查缓存
 */
function checkCache(key) {
  const cache = loadCache();
  const cached = cache[key];
  if (!cached) return null;
  
  // 检查缓存是否过期
  const age = Date.now() - cached.timestamp;
  if (age >= cached.duration) {
    return null;
  }
  
  return cached.data;
}

/**
 * Track123 API - 导入运单
 */
async function importTracking(trackingNumber, carrierCode) {
  const config = loadConfig();
  const apiSecret = config.track123.api_secret;
  
  if (!apiSecret || apiSecret === 'your_track123_api_key_here') {
    throw new Error('Track123 API Key 未配置\n请先配置 config.json 中的 track123.api_secret');
  }
  
  const url = `${API_BASE}/track/import`;
  const params = [{
    trackNo: trackingNumber,
    courierCode: carrierCode || ''
  }];
  
  try {
    const response = await axios.post(url, params, {
      headers: {
        'Track123-Api-Secret': apiSecret,
        'Content-Type': 'application/json'
      },
      timeout: 10000
    });
    
    return response.data;
  } catch (error) {
    console.error('[DEBUG] Import Error:', error.response?.data);
    throw error;
  }
}

/**
 * Track123 API - 查询物流
 */
async function queryRealtime(trackingNumber, carrierCode, language = 'zh') {
  const config = loadConfig();
  const apiSecret = config.track123.api_secret;
  
  if (!apiSecret || apiSecret === 'your_track123_api_key_here') {
    throw new Error('Track123 API Key 未配置\n请先配置 config.json 中的 track123.api_secret');
  }
  
  const url = `${API_BASE}/track/query`;
  const params = {
    trackNos: [trackingNumber]
  };
  
  try {
    const response = await axios.post(url, params, {
      headers: {
        'Track123-Api-Secret': apiSecret,
        'Content-Type': 'application/json'
      },
      timeout: 10000
    });
    
    return response.data;
  } catch (error) {
    console.error('[DEBUG] Query Error:', error.response?.data);
    throw error;
  }
}

/**
 * Track123 API - 自动识别快递公司
 */
async function detectCarrier(trackingNumber) {
  const config = loadConfig();
  const apiSecret = config.track123.api_secret;
  
  if (!apiSecret || apiSecret === 'your_track123_api_key_here') {
    throw new Error('Track123 API Key 未配置');
  }
  
  const url = `${API_BASE}/courier/detection`;
  const params = {
    number: trackingNumber
  };
  
  try {
    const response = await axios.post(url, params, {
      headers: {
        'Track123-Api-Secret': apiSecret,
        'Content-Type': 'application/json'
      },
      timeout: 10000
    });
    
    return response.data;
  } catch (error) {
    console.error('[DEBUG] Detection Error:', error.response?.data);
    throw error;
  }
}

/**
 * Track123 API - 获取快递公司列表
 */
async function getCarriers(language = 'zh') {
  const config = loadConfig();
  const apiSecret = config.track123.api_secret;
  
  if (!apiSecret || apiSecret === 'your_track123_api_key_here') {
    throw new Error('Track123 API Key 未配置');
  }
  
  const url = `${API_BASE}/courier/list`;
  const params = {
    language: language
  };
  
  const response = await axios.get(url, {
    params,
    headers: {
      'Track123-Api-Secret': apiSecret
    },
    timeout: 10000
  });
  return response.data;
}

/**
 * 自动识别快递公司 (基于运单号规则)
 */
function identifyCarrier(trackingNumber) {
  const rules = [
    { pattern: /^SF\d{12,15}$/i, code: 'sfex', name: '顺丰速运' },
    { pattern: /^1\d{10,12}$/i, code: 'yto', name: '圆通速递' },
    { pattern: /^ZT\d{10,12}$/i, code: 'zto', name: '中通快递' },
    { pattern: /^YD\d{10,12}$/i, code: 'yunda', name: '韵达速递' },
    { pattern: /^ST\d{10,12}$/i, code: 'sto', name: '申通快递' },
    { pattern: /^EM\d{10,12}$/i, code: 'ems', name: '邮政 EMS' },
    { pattern: /^1\d{13}$/i, code: 'jd', name: '京东快递' },
    { pattern: /^J\d{12}$/i, code: 'jt', name: '极兔速递' },
    { pattern: /^1Z\d{16}$/i, code: 'ups', name: 'UPS' },
    { pattern: /^[\w]{2}\d{9,12}$/i, code: 'dhl', name: 'DHL' }
  ];
  
  for (const rule of rules) {
    if (rule.pattern.test(trackingNumber)) {
      return { code: rule.code, name: rule.name };
    }
  }
  
  return null;
}

/**
 * 格式化物流状态 (Track123 状态码)
 */
function formatStatus(status) {
  const statusMap = {
    '001': '待揽收',
    '002': '已揽收',
    '003': '运输中',
    '004': '派送中',
    '005': '已签收',
    '006': '异常',
    '007': '已退回',
    'unknown': '未知',
    'pending': '待揽收',
    'picked_up': '已揽收',
    'in_transit': '运输中',
    'out_for_delivery': '派送中',
    'delivered': '已签收',
    'exception': '异常',
    'returned': '已退回'
  };
  return statusMap[status] || status;
}

/**
 * 格式化输出
 */
function formatOutput(result, carrier, format = 'text', language = 'zh') {
  if (format === 'json') {
    return JSON.stringify(result, null, 2);
  }
  
  if (format === 'compact') {
    const latest = result.tracks && result.tracks.length > 0 
      ? result.tracks[0] 
      : { description: '暂无物流信息' };
    return `📦 ${result.tracking_number} (${carrier.name}) - ${formatStatus(result.status)}\n最新：${latest.checkpoint_time || ''} ${latest.tracking_detail || latest.description || ''}`;
  }
  
  // 文本格式
  let output = `📦 ${carrier.name} ${carrier.nameEn || ''}\n`;
  output += `运单号：${result.tracking_number || 'N/A'}\n`;
  output += `状态：${formatStatus(result.status || 'unknown')}\n`;
  
  if (result.status_description) {
    output += `说明：${formatStatus(result.status_description)}\n`;
  }
  
  if (result.origin_info || result.destination_info) {
    output += `\n📍 路线:\n`;
    if (result.origin_info) {
      output += `始发：${result.origin_info.city || ''} ${result.origin_info.state || ''} ${result.origin_info.country || ''}\n`;
    }
    if (result.destination_info) {
      output += `目的：${result.destination_info.city || ''} ${result.destination_info.state || ''} ${result.destination_info.country || ''}\n`;
    }
  }
  
  if (result.weight) {
    output += `重量：${result.weight}\n`;
  }
  
  if (result.signed_by) {
    output += `签收：${result.signed_by}\n`;
  }
  
  if (result.tracks && result.tracks.length > 0) {
    output += `\n🚚 物流轨迹:\n`;
    result.tracks.forEach((track, index) => {
      const time = track.checkpoint_time || track.time || '未知时间';
      const desc = track.tracking_detail || track.description || track.detail || '无详情';
      const location = track.location || track.city || '';
      
      output += `${time} ${desc}\n`;
      if (location) {
        output += `   📍 ${location}\n`;
      }
    });
  } else {
    output += `\n⚠️ 暂无物流轨迹信息\n`;
  }
  
  return output.trim();
}

/**
 * 显示快递公司列表
 */
function displayCarriers(carriers) {
  let output = '📦 支持的快递公司:\n\n';
  output += '| 代码 | 中文名 | 英文名 |\n';
  output += '|------|--------|--------|\n';
  
  carriers.forEach(c => {
    output += `| ${c.code} | ${c.name} | ${c.name_en || c.name_en} |\n`;
  });
  
  return output;
}

/**
 * 主查询函数
 */
async function query(trackingNumber, carrierCode, options = {}) {
  const { format = 'text', useCache = true, language = 'zh' } = options;
  
  // 显示快递公司列表
  if (carrierCode === 'carriers') {
    const result = await getCarriers(language);
    if (result.code === 200 && result.data) {
      return displayCarriers(result.data);
    } else {
      throw new Error('获取快递公司列表失败：' + (result.message || '未知错误'));
    }
  }
  
  // 检查缓存
  const cacheKey = `${carrierCode}:${trackingNumber}:${language}`;
  if (useCache) {
    const cached = checkCache(cacheKey);
    if (cached) {
      return formatOutput(cached, CARRIER_MAP[carrierCode] || { name: carrierCode, nameEn: '' }, format, language);
    }
  }
  
  let result = null;
  let carrier = null;
  
  try {
    // 自动识别
    if (carrierCode === 'auto') {
      const identified = identifyCarrier(trackingNumber);
      if (identified) {
        carrierCode = identified.code;
        carrier = CARRIER_MAP[identified.code] || { name: identified.name, nameEn: '' };
      } else {
        throw new Error('无法识别快递公司，请指定快递公司代码\n可用代码：sf, yto, zto, yunda, sto, ems, jd, jt, dhl, fedex, ups, tnt, auto, carriers');
      }
    } else {
      carrier = CARRIER_MAP[carrierCode];
      if (!carrier) {
        throw new Error('未知的快递公司代码：' + carrierCode + '\n可用代码：sf, yto, zto, yunda, sto, ems, jd, jt, dhl, fedex, ups, tnt, auto, carriers');
      }
    }
    
    // 先导入运单（Track123 要求）
    const importResult = await importTracking(trackingNumber, carrierCode);
    
    if (importResult.code !== '00000') {
      throw new Error('导入运单失败：' + (importResult.msg || '未知错误'));
    }
    
    // 查询物流
    const apiResult = await queryRealtime(trackingNumber, carrierCode, language);
    
    if (apiResult.code !== '00000') {
      throw new Error('查询失败：' + (apiResult.msg || '未知错误'));
    }
    
    if (!apiResult.data || !apiResult.data.accepted) {
      throw new Error('未找到物流信息，请确认运单号是否正确');
    }
    
    // 构建结果
    const content = apiResult.data.accepted.content;
    const latest = content && content.length > 0 ? content[0] : null;
    
  
    
    // 提取物流轨迹 - Track123 的轨迹在 localLogisticsInfo.trackingDetails 里
    let tracks = [];
    if (latest && latest.localLogisticsInfo && latest.localLogisticsInfo.trackingDetails) {
      tracks = latest.localLogisticsInfo.trackingDetails.map(t => ({
        checkpoint_time: t.eventTime || '',
        tracking_detail: t.eventDetail || '',
        location: t.address || ''
      })).reverse(); // 按时间倒序，最早的在前面
    }
    
    const queryResult = {
      tracking_number: latest ? latest.trackNo : trackingNumber,
      carrier: {
        code: carrierCode,
        name: carrier.name,
        nameEn: carrier.nameEn
      },
      status: latest ? latest.trackingStatus : 'unknown',
      status_description: latest ? latest.trackingStatus : '',
      origin: null,
      destination: null,
      weight: null,
      signed_by: null,
      tracks: tracks
    };
    
    // 保存到缓存
    saveCache(cacheKey, queryResult);
    
    return formatOutput(queryResult, carrier, format, language);
    
  } catch (error) {
    console.error('❌ 查询失败:', error.message);
    throw error;
  }
}

/**
 * 命令行处理
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('📦 快递查询 - 基于 Track123 API');
    console.log('\n用法：node scripts/query.js <快递公司代码> <运单号> [选项]');
    console.log('\n快递公司代码：');
    console.log('  国内：sf, yto, zto, yunda, sto, ems, jd, jt, cs');
    console.log('  国际：dhl, fedex, ups, tnt, sfint');
    console.log('  特殊：auto (自动识别), carriers (显示所有快递公司)');
    console.log('\n示例：');
    console.log('  node scripts/query.js sf SF1234567890123');
    console.log('  node scripts/query.js auto 12345678901234');
    console.log('  node scripts/query.js dhl 1234567890');
    console.log('\n选项：');
    console.log('  --format <text|json|compact>  输出格式 (默认：text)');
    console.log('  --cache                       使用缓存 (默认：开启)');
    console.log('  --no-cache                    强制刷新缓存');
    console.log('  --lang <zh|en|ru>            返回语言 (默认：zh)');
    process.exit(1);
  }
  
  const carrierCode = args[0];
  const trackingNumber = args[1];
  const options = {
    format: args.includes('--format') ? args[args.indexOf('--format') + 1] || 'text' : 'text',
    useCache: !args.includes('--no-cache'),
    language: args.includes('--lang') ? args[args.indexOf('--lang') + 1] || 'zh' : 'zh'
  };
  
  query(trackingNumber, carrierCode, options)
    .then(result => console.log(result))
    .catch(error => {
      process.exit(1);
    });
}

main();
