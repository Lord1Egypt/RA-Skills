#!/usr/bin/env node
/**
 * 美团返利助手 — run.js
 *
 * 统一入口，所有操作通过子命令调用：
 *   init         环境初始化
 *   config       查看配置（隐藏 secret）
 *   query-coupon 商品/优惠券查询（核心功能）
 *   referral-link 生成推广链接
 */

const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const https = require('https');

// ── 常量 ────────────────────────────────────────────────────
const SCRIPTS_DIR = __dirname;
const SKILL_DIR = path.dirname(SCRIPTS_DIR);
const CONFIG_FILE = path.join(SCRIPTS_DIR, 'config.json');

// ── 工具函数 ─────────────────────────────────────────────────
function out(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

function fail(error, extra) {
  out(Object.assign({ ok: false, error }, extra || {}));
  process.exit(1);
}

function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch (_) {
    fail('CONFIG_ERROR', { message: '无法加载 config.json，请检查配置文件' });
  }
}

// ── Ca Gateway 签名 ──────────────────────────────────────────
/**
 * 美团 CPS Ca Gateway 签名算法：
 *   stringToSign = METHOD + "\n" + Content-MD5 + "\n" + SignedHeaders + URLPath
 *   SignedHeaders = "S-Ca-App:APPKEY\nS-Ca-Timestamp:TIMESTAMP\n"
 *   signature = Base64(HMAC-SHA256(secret, stringToSign))
 */
function caSign(appkey, secret, method, pathStr, bodyStr) {
  const ts = String(Date.now());
  const md5Raw = crypto.createHash('md5').update(bodyStr, 'utf-8').digest();
  const contentMD5 = md5Raw.toString('base64');
  const signedHeaders = 'S-Ca-App:' + appkey + '\n' + 'S-Ca-Timestamp:' + ts + '\n';
  const stringToSign = method + '\n' + contentMD5 + '\n' + signedHeaders + pathStr;
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(stringToSign, 'utf-8');
  const signature = hmac.digest('base64');
  return { ts, contentMD5, signature, stringToSign };
}

/**
 * 发送 Ca Gateway 签名的 POST 请求
 */
function caPost(appkey, secret, host, pathStr, bodyObj) {
  return new Promise(function (resolve, reject) {
    const bodyStr = JSON.stringify(bodyObj);
    const { ts, contentMD5, signature } = caSign(appkey, secret, 'POST', pathStr, bodyStr);

    const options = {
      hostname: host.replace(/^https?:\/\//, '').split('/')[0],
      port: 443,
      path: pathStr,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
        'S-Ca-App': appkey,
        'S-Ca-Timestamp': ts,
        'S-Ca-Signature-Headers': 'S-Ca-Timestamp,S-Ca-App',
        'Content-MD5': contentMD5,
        'S-Ca-Signature': signature
      },
      timeout: 15000
    };

    const req = https.request(options, function (res) {
      let data = '';
      res.on('data', function (c) { data += c; });
      res.on('end', function () {
        try {
          resolve(JSON.parse(data));
        } catch (_) {
          resolve({ raw: data, httpStatus: res.statusCode });
        }
      });
    });
    req.on('error', function (e) { reject(e); });
    req.on('timeout', function () { req.destroy(); reject(new Error('Request timeout')); });
    req.write(bodyStr);
    req.end();
  });
}

// ── 城市编码（常用城市）─────────────────────────────────────────
const CITY_MAP = {
  '北京': '010', '上海': '021', '广州': '020', '深圳': '0755',
  '杭州': '0571', '成都': '028', '重庆': '023', '武汉': '027',
  '南京': '025', '苏州': '0512', '西安': '029', '长沙': '0731',
  '天津': '022', '郑州': '0371', '青岛': '0532', '厦门': '0592',
  '合肥': '0551', '济南': '0531', '昆明': '0871', '福州': '0591',
  '东莞': '0769', '佛山': '0757', '大连': '0411', '沈阳': '024',
  '无锡': '0510', '宁波': '0574', '温州': '0577', '贵阳': '0851',
  '南宁': '0771', '哈尔滨': '0451', '石家庄': '0311', '太原': '0351',
  '珠海': '0756', '常州': '0519', '泉州': '0595', '南通': '0513'
};

// ══════════════════════════════════════════════════════════════
// 子命令实现
// ══════════════════════════════════════════════════════════════

var commands = {};

/**
 * init — 环境检查
 */
commands.init = function () {
  // Node.js >= 18 检查
  var nodeVer = process.version.match(/^v(\d+)\./);
  if (!nodeVer || parseInt(nodeVer[1]) < 18) {
    return fail('NODE_VERSION_LOW', { message: '当前 Node.js 版本过低，需要 >= 18' });
  }
  out({ ok: true, skill_dir: SKILL_DIR });
};

/**
 * config — 查看当前配置（隐藏 secret）
 */
commands.config = function () {
  var config = loadConfig();
  out({
    ok: true,
    appkey: config.appkey,
    secret: config.secret ? config.secret.slice(0, 4) + '****' + config.secret.slice(-4) : '',
    host: config.host,
    paths: config.paths
  });
};

/**
 * query-coupon — 商品/优惠券查询（核心功能）
 *
 * 选项：
 *   --scene <dine-in|delivery>  业务场景: dine-in=到店餐饮(默认), delivery=外卖
 *   --platform <1|2>           1=到家, 2=到店（一般由 --scene 自动设置）
 *   --biz-line <1|2|3|4|5>     到店:1=到餐,2=到综,3=酒店,4=门票; 到家:1=外卖,5=医药（由 --scene 自动设置）
 *   --keyword <text>           搜索关键词
 *   --city <name>              城市名（如"北京"）
 *   --city-id <id>             城市编码
 *   --lat <float>              纬度（十进制）
 *   --lng <float>              经度（十进制）
 *   --price-min <int>          最低价格（元）
 *   --price-max <int>          最高价格（元）
 *   --commission-min <int>     最低佣金（元）
 *   --commission-max <int>     最高佣金（元）
 *   --sort <1|2|3|6>           排序:1=售价,2=销量,3=佣金,6=距离（默认2）
 *   --order <1|2>              1=升序,2=降序（默认2）
 *   --page <int>               页码（默认1）
 *   --page-size <int>          每页条数（默认10）
 *   --list-topic <2|3|5>       榜单:2=今日必推,3=同城热销,5=实时热销
 *   --category-id <int>        品类ID
 *   --search-id <string>       分页标识（翻页用）
 *   --product-ids <list>       商品ID列表（逗号分隔，最多20个）
 */

// 场景 → platform/bizLine 映射
var SCENE_MAP = {
  'dine-in':  { platform: 2, bizLine: 1, label: '到店餐饮' },
  'delivery': { platform: 1, bizLine: 1, label: '外卖' }
};

commands['query-coupon'] = function (argv) {
  var config = loadConfig();
  var queryPath = config.paths.query_coupon;

  var body = {};

  // ── 场景路由：--scene 优先于 --platform/--biz-line ──
  var scene = argv['scene'] || 'dine-in';
  var sceneConfig = SCENE_MAP[scene] || SCENE_MAP['dine-in'];
  var defaultPlatform = argv['platform'] !== undefined ? parseInt(argv['platform']) : sceneConfig.platform;
  var defaultBizLine  = argv['biz-line'] !== undefined ? parseInt(argv['biz-line']) : sceneConfig.bizLine;

  // 判断查询模式
  var hasKeyword = !!argv['keyword'];
  var hasProductIds = !!argv['product-ids'];
  var hasListTopic = !!argv['list-topic'];

  // ── 模式1: 商品ID批量查询（优先级最高） ──
  if (hasProductIds) {
    body.productViewSignList = argv['product-ids'].split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    body.platform = defaultPlatform;
    body.bizLine = defaultBizLine;
  }
  // ── 模式2: 榜单查询 ──
  else if (hasListTopic) {
    body.platform = defaultPlatform;
    body.bizLine = defaultBizLine;
    body.listTopiId = parseInt(argv['list-topic']);
    // 榜单模式支持城市/位置筛选
    if (argv['city-id']) body.cityId = argv['city-id'];
    else if (argv['city'] && CITY_MAP[argv['city']]) body.cityId = CITY_MAP[argv['city']];
    if (argv['lat'] !== undefined) body.latitude = Math.round(parseFloat(argv['lat']) * 1000000);
    if (argv['lng'] !== undefined) body.longitude = Math.round(parseFloat(argv['lng']) * 1000000);
    if (argv['sort']) body.sortField = parseInt(argv['sort']);
  }
  // ── 模式3: 关键词搜索 ──
  else if (hasKeyword) {
    body.searchText = argv['keyword'];
    body.platform = defaultPlatform;
    body.bizLine = defaultBizLine;
    // 关键词搜索不传 cityId（会导致报错），仅支持分页和排序
    if (argv['sort']) body.sortField = parseInt(argv['sort']);
  }
  // ── 模式4: 全量列表 ──
  else {
    body.platform = defaultPlatform;
    body.bizLine = defaultBizLine;
    body.listTopiId = 3; // 默认同城热销
    if (argv['city-id']) body.cityId = argv['city-id'];
    else if (argv['city'] && CITY_MAP[argv['city']]) body.cityId = CITY_MAP[argv['city']];
  }

  // 以下参数各模式通用
  if (!hasProductIds) {
    // 价格筛选
    if (argv['price-min']) body.priceFloor = parseInt(argv['price-min']);
    if (argv['price-max']) body.priceCap = parseInt(argv['price-max']);
    // 佣金筛选
    if (argv['commission-min']) body.commissionFloor = parseInt(argv['commission-min']);
    if (argv['commission-max']) body.commissionCap = parseInt(argv['commission-max']);
    // 排序
    if (argv['order']) body.ascDescOrder = parseInt(argv['order']);
    // 品类（仅榜单模式）
    if (argv['category-id'] && hasListTopic) body.categoryId = parseInt(argv['category-id']);
    // 经纬度（榜单模式已处理，这里补充非榜单模式明确传入的场景）
    if (!hasListTopic && argv['lat'] !== undefined) body.latitude = Math.round(parseFloat(argv['lat']) * 1000000);
    if (!hasListTopic && argv['lng'] !== undefined) body.longitude = Math.round(parseFloat(argv['lng']) * 1000000);
  }

  // 分页
  body.pageNo = parseInt(argv['page']) || 1;
  body.pageSize = parseInt(argv['page-size']) || 10;
  if (argv['search-id']) body.searchId = argv['search-id'];

  caPost(config.appkey, config.secret, config.host, queryPath, body)
    .then(function (res) {
      if (res.code === 0) {
        // 整理结果
        var coupons = (res.data || []).map(function (item) {
          var detail = item.couponPackDetail || {};
          var brand = item.brandInfo || {};
          var comm = item.commissionInfo || {};
          var poi = item.availablePoiInfo || {};
          var label = item.productLabel || {};

          return {
            productViewSign: detail.productViewSign || '',
            skuViewId: detail.skuViewId || '',
            name: detail.name || '',
            brandName: brand.brandName || '',
            brandLogoUrl: brand.brandLogoUrl || '',
            sellPrice: detail.sellPrice || 0,
            originalPrice: detail.originalPrice || 0,
            headUrl: detail.headUrl || '',
            saleVolume: detail.saleVolume || '',
            saleStatus: detail.saleStatus,
            commissionPercent: comm.commissionPercent || '0',
            commission: comm.commission || '0',
            availablePoiNum: poi.availablePoiNum || 0,
            availableCityNum: item.availableCityNum || 0,
            // 标签
            historyPriceLabel: (label.pricePowerLabel || {}).historyPriceLabel || '',
            beatMTLabel: (label.pricePowerLabel || {}).beatMTLabel || '',
            productRankLabel: label.productRankLabel || '',
            dianPingRankLabel: label.dianPingRankLabel || '',
            // 原始响应引用
            platform: item.platform || body.platform || 0,
            bizLine: item.bizLine || body.bizLine || 0,
            categoryName: item.categoryName || ''
          };
        });

        out({
          ok: true,
          success: true,
          scene: scene,
          sceneLabel: sceneConfig.label,
          couponCount: coupons.length,
          coupons: coupons,
          hasNext: res.hasNext || false,
          searchId: res.searchId || '',
          _rawCode: res.code,
          _rawMessage: res.message
        });
      } else {
        out({
          ok: false,
          success: false,
          code: res.code,
          message: res.message || '查询失败'
        });
      }
    })
    .catch(function (err) {
      out({ ok: false, success: false, error: 'NETWORK_ERROR', message: '网络请求失败: ' + err.message });
    });
};

/**
 * referral-link — 生成推广链接
 *
 * 选项：
 *   --product-view-sign <id>   商品ID（从 query-coupon 结果获取）
 *   --platform <1|2>           与商品匹配的平台
 *   --biz-line <1-5>           与商品匹配的业务线
 *   --text <url>               要转换的原始链接
 *   --act-id <id>              活动物料ID
 *   --link-type <1-6>          链接类型:1=H5长链,2=短链,3=deeplink,4=小程序路径,5=团口令,6=小程序码
 *   --sid <string>             二级渠道标识
 */
commands['referral-link'] = function (argv) {
  var config = loadConfig();
  var referralPath = config.paths.referral_link;

  var body = {};

  if (argv['product-view-sign']) {
    body.productViewSign = argv['product-view-sign'];
    if (argv['platform']) body.platform = parseInt(argv['platform']);
    if (argv['biz-line']) body.bizLine = parseInt(argv['biz-line']);
  }
  if (argv['text']) body.text = argv['text'];
  if (argv['act-id']) body.actId = argv['act-id'];

  // 链接类型
  if (argv['link-type']) {
    var lt = parseInt(argv['link-type']);
    body.linkType = lt;
    // 支持逗号分隔的多类型
    if (String(argv['link-type']).indexOf(',') !== -1) {
      body.linkTypeList = String(argv['link-type']).split(',').map(function (s) { return parseInt(s.trim()); });
      delete body.linkType;
    }
  }

  if (argv['sid']) body.sid = argv['sid'];

  if (!body.productViewSign && !body.text && !body.actId) {
    return fail('MISSING_PARAMS', {
      message: '请提供 --product-view-sign、--text 或 --act-id 之一'
    });
  }

  caPost(config.appkey, config.secret, config.host, referralPath, body)
    .then(function (res) {
      if (res.code === 0) {
        out({
          ok: true,
          success: true,
          referralLink: res.data || '',
          referralLinkMap: res.referralLinkMap || {},
          productViewSign: res.productViewSign || '',
          skuViewId: res.skuViewId || '',
          _rawCode: res.code
        });
      } else {
        out({
          ok: false,
          success: false,
          code: res.code,
          message: res.message || '取链失败'
        });
      }
    })
    .catch(function (err) {
      out({ ok: false, success: false, error: 'NETWORK_ERROR', message: '网络请求失败: ' + err.message });
    });
};

/**
 * city-lookup — 城市编码查询
 */
commands['city-lookup'] = function (argv) {
  var name = argv['name'] || argv._extra && argv._extra[0];
  if (name && CITY_MAP[name]) {
    out({ ok: true, city: name, cityId: CITY_MAP[name] });
  } else if (name) {
    out({ ok: false, message: '未找到城市"' + name + '"，请尝试使用城市编码' });
  } else {
    out({ ok: true, cities: Object.keys(CITY_MAP).map(function (k) { return { name: k, cityId: CITY_MAP[k] }; }) });
  }
};

// ══════════════════════════════════════════════════════════════
// 命令行解析 & 入口
// ══════════════════════════════════════════════════════════════

function parseArgv(args) {
  var cmd = null;
  var params = {};
  var extra = [];
  var i = 0;

  for (; i < args.length; i++) {
    var arg = args[i];
    if (!cmd && !arg.startsWith('--')) {
      cmd = arg;
      continue;
    }
    if (arg.startsWith('--')) {
      var key = arg.slice(2);
      // 检查下一个参数是否是值
      if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        params[key] = args[i + 1];
        i++;
      } else {
        params[key] = 'true';
      }
    } else {
      extra.push(arg);
    }
  }

  if (extra.length > 0) params._extra = extra;
  return { cmd: cmd, params: params };
}

// 主入口
var parsed = parseArgv(process.argv.slice(2));
var cmd = parsed.cmd || 'init';

if (commands[cmd]) {
  commands[cmd](parsed.params);
} else {
  out({
    ok: false,
    error: 'UNKNOWN_COMMAND',
    message: '未知命令: ' + cmd,
    availableCommands: Object.keys(commands)
  });
  process.exit(1);
}
