#!/usr/bin/env node
/**
 * mtunion-product-ai-all-guide 统一入口脚本
 * 
 * 跨平台（macOS / Windows）统一调度，AI 只需执行:
 *   node run.js <command> [options]
 * 
 * 子命令:
 *   init                          环境初始化（Python检查 + npm检查 + pt-passport安装）
 *   get-device-token              获取设备标识
 *   get-token                     获取缓存的用户Token
 *   auth-get-code                 获取授权链接
 *   auth-poll-token               轮询授权结果
 *   qrcode <url>                  获取二维码图片URL（服务端生成）
 *   hotword --city-id <id>        热搜词查询
 *   search --keyword <kw> --lat <lat> --lng <lng> --token <t> --city-id <id>
 *   location --token <t>          获取用户近期位置
 *   location-by-address --address <addr>  根据地址获取经纬度
 *   order --product-id <pid> --poi-id <pid> --token <t> --city-id <id> --uuid <u>
 *   issue --token <t>             领取优惠券（纯 Node.js 实现，含 AIGuard 签名）
 *   coupon-status                 查询今日领券状态
 *   logout                        退出登录
 *   clear-device-token            清除设备标识
 * 
 * 所有命令输出 JSON 到 stdout，错误信息输出到 stderr。
 */

const { execSync, execFileSync, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const https = require('https');

// -- 全局常量 --
const SCRIPTS_DIR = __dirname;
const SKILL_DIR = path.dirname(SCRIPTS_DIR);
const CLIENT_ID = '578aafab312b44f1b76b0529b06bb0c6';
const PT_PASSPORT_BIN = path.join(SCRIPTS_DIR, 'node_modules', '.bin', 'pt-passport');
const PYTHON = findPython();

// -- Token 存储路径（统一使用 ~/.xiaomei-workspace/）--
const AUTH_DIR = path.join(require('os').homedir(), '.xiaomei-workspace');
if (!fs.existsSync(AUTH_DIR)) { fs.mkdirSync(AUTH_DIR, { recursive: true }); }
const CHILD_ENV = Object.assign({}, process.env, {
  PT_PASSPORT_AUTH_FILE: path.join(AUTH_DIR, 'mt_passport_auth.json'),
  XIAOMEI_AUTH_FILE: path.join(AUTH_DIR, 'auth_tokens.json')
});

// -- 领券相关常量 --
const COUPON_BASE_URL = 'https://media.meituan.com';
const COUPON_ISSUE_PATH = '/fulishemini/couponActivity/aiSendCouponDistribution';
const CONFIG_FILE = path.join(SCRIPTS_DIR, 'config.json');

// -- 工具函数 --

function findPython() {
  for (const cmd of ['python3', 'python']) {
    try {
      const ver = execSync(cmd + ' --version', { encoding: 'utf-8', timeout: 10000, stdio: 'pipe' }).trim();
      if (ver && !ver.startsWith('Python 2.')) return cmd;
    } catch (_) { /* ignore */ }
  }
  return 'python3';
}

function out(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

function fail(error, extra) {
  out(Object.assign({ ok: false, error: error }, extra || {}));
  process.exit(1);
}

/** 执行 Python 脚本，返回解析后的 JSON */
function runPython(scriptName, args) {
  const scriptPath = path.join(SCRIPTS_DIR, scriptName);
  const cmdArgs = [scriptPath].concat(args);
  try {
    const result = spawnSync(PYTHON, cmdArgs, {
      encoding: 'utf-8',
      timeout: 30000,
      stdio: ['pipe', 'pipe', 'pipe'],
      cwd: SCRIPTS_DIR,
      env: CHILD_ENV
    });
    const stdout = (result.stdout || '').trim();
    if (result.status !== 0) {
      try { return JSON.parse(stdout); } catch (_) {}
      return { ok: false, error: 'SCRIPT_ERROR', message: (result.stderr || stdout || 'Unknown error').trim() };
    }
    try { return JSON.parse(stdout); } catch (_) {
      return { ok: false, error: 'PARSE_ERROR', message: 'Invalid JSON from script', raw: stdout };
    }
  } catch (e) {
    return { ok: false, error: 'EXEC_ERROR', message: e.message };
  }
}

/** 执行 pt-passport CLI 命令，返回原始 stdout */
function runPassport(args) {
  try {
    const result = spawnSync(PT_PASSPORT_BIN, args, {
      encoding: 'utf-8',
      timeout: 120000,
      stdio: ['pipe', 'pipe', 'pipe'],
      env: CHILD_ENV,
      shell: true
    });
    return {
      exitCode: result.status,
      stdout: (result.stdout || '').trim(),
      stderr: (result.stderr || '').trim()
    };
  } catch (e) {
    return { exitCode: 1, stdout: '', stderr: e.message };
  }
}

/** 解析 --key value 形式的命令行参数 */
function parseArgs(argv) {
  const args = {};
  const positional = [];
  for (var i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
        args[key] = argv[++i];
      } else {
        args[key] = 'true';
      }
    } else {
      positional.push(argv[i]);
    }
  }
  return { args: args, positional: positional };
}

/** 读取 config.json */
function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch (_) {
    return {};
  }
}

/** 金额分转元 */
function fenToYuan(fen) {
  if (!fen) return '0';
  var yuan = parseInt(fen, 10) / 100;
  return yuan === Math.floor(yuan) ? String(Math.floor(yuan)) : yuan.toFixed(1);
}

/** 毫秒时间戳转 YYYY-MM-DD */
function formatTimestampMs(tsMs) {
  if (!tsMs) return '-';
  try {
    var d = new Date(parseInt(tsMs, 10));
    var year = d.getFullYear();
    var month = String(d.getMonth() + 1).padStart(2, '0');
    var day = String(d.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
  } catch (_) {
    return String(tsMs);
  }
}

/** 格式化单张券信息 */
function formatCoupon(c) {
  var priceLimit = c.priceLimit;
  var couponValue = c.couponValue || 0;
  var discountInfo = '';
  if (priceLimit && priceLimit > 0) {
    discountInfo = '\u6ee1' + fenToYuan(priceLimit) + '\u5143\u51cf' + fenToYuan(couponValue) + '\u5143';
  }
  var start = c.couponStartTime;
  var end = c.couponEndTime;
  var validPeriod = '';
  if (start && end) {
    validPeriod = formatTimestampMs(start) + ' \u81f3 ' + formatTimestampMs(end);
  }
  return {
    name: c.couponName || '',
    discount_info: discountInfo,
    valid_period: validPeriod,
    priceLimit: priceLimit,
    couponValue: couponValue,
    tabName: c.tabName || ''
  };
}

/** 获取今天的日期字符串 YYYY-MM-DD */
function getTodayStr() {
  var d = new Date();
  var year = d.getFullYear();
  var month = String(d.getMonth() + 1).padStart(2, '0');
  var day = String(d.getDate()).padStart(2, '0');
  return year + '-' + month + '-' + day;
}

// -- CLIGuard 签名集成 --

/**
 * 加载 cliguard.js 模块
 * 优先从 vendor/cliguard/js/ 加载，fallback 到 ~/.cliguard/cliguard-updates/
 */
function loadCliguard() {
  var vendorPath = path.join(SCRIPTS_DIR, 'vendor', 'cliguard', 'js', 'cliguard.js');
  var updatePath = path.join(
    require('os').homedir(), '.cliguard', 'cliguard-updates', 'core', 'cliguard.js'
  );

  if (fs.existsSync(vendorPath)) {
    return require(vendorPath);
  }
  if (fs.existsSync(updatePath)) {
    return require(updatePath);
  }
  return null;
}

/**
 * 对 URL 注入公共参数（csecplatform, csecversion 等）
 */
function addCommonParams(urlStr) {
  try {
    var cliguard = loadCliguard();
    if (!cliguard || typeof cliguard.addCommonParams !== 'function') {
      return urlStr;
    }
    var result = cliguard.addCommonParams(urlStr);
    return (result && result.url) ? result.url : urlStr;
  } catch (e) {
    process.stderr.write('[run.js:addCommonParams] warning: ' + e.message + '\n');
    return urlStr;
  }
}

/**
 * 生成 AIGuard 签名 headers
 */
function makeSignHeaders(method, urlStr, bodyHash) {
  try {
    var cliguard = loadCliguard();
    if (!cliguard || typeof cliguard.signRequest !== 'function') {
      return {};
    }
    return cliguard.signRequest(method.toUpperCase(), urlStr, bodyHash || '') || {};
  } catch (e) {
    process.stderr.write('[run.js:makeSignHeaders] warning: ' + e.message + '\n');
    return {};
  }
}

// -- HTTPS 请求工具 --

/**
 * 发起 HTTPS POST 请求（Promise 版）
 */
function httpsPost(urlStr, bodyObj, extraHeaders) {
  return new Promise(function (resolve, reject) {
    var bodyStr = JSON.stringify(bodyObj);
    var bodyBuf = Buffer.from(bodyStr, 'utf-8');

    // 计算 body hash（取前 16200 字节，与 Python SDK 一致）
    var hashSlice = bodyBuf.slice(0, 16200);
    var bodyHash = crypto.createHash('md5').update(hashSlice).digest('hex');

    // 注入公参
    var signedUrl = addCommonParams(urlStr);

    // 生成签名 headers
    var sigHeaders = makeSignHeaders('POST', signedUrl, bodyHash);

    var parsed = new URL(signedUrl);
    var options = {
      hostname: parsed.hostname,
      port: parsed.port || 443,
      path: parsed.pathname + parsed.search,
      method: 'POST',
      headers: Object.assign({
        'Content-Type': 'application/json',
        'Content-Length': bodyBuf.length,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest'
      }, sigHeaders, extraHeaders || {})
    };

    var req = https.request(options, function (res) {
      var chunks = [];
      res.on('data', function (chunk) { chunks.push(chunk); });
      res.on('end', function () {
        var body = Buffer.concat(chunks).toString('utf-8');
        try {
          resolve({ status: res.statusCode, data: JSON.parse(body) });
        } catch (_) {
          resolve({ status: res.statusCode, data: null, raw: body });
        }
      });
    });

    req.on('error', function (e) { reject(e); });
    req.setTimeout(15000, function () {
      req.destroy();
      reject(new Error('TIMEOUT'));
    });

    req.write(bodyBuf);
    req.end();
  });
}

// -- 子命令实现 --

var commands = {};

// -- 状态文件路径 --
var STATE_FILE = path.join(AUTH_DIR, '.state.json');

/** 读取本地状态文件，返回对象（文件不存在时返回空对象） */
function readState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  } catch (_) {
    return {};
  }
}

/** 写入本地状态文件（合并更新） */
function writeState(patch) {
  var current = readState();
  var updated = Object.assign({}, current, patch);
  fs.writeFileSync(STATE_FILE, JSON.stringify(updated, null, 2), 'utf-8');
}

/**
 * init - 环境初始化
 */
commands.init = function () {
  if (!fs.existsSync(SCRIPTS_DIR) || !fs.statSync(SCRIPTS_DIR).isDirectory()) {
    fail('PATH_NOT_FOUND');
  }

  var pyVer = '';
  try {
    pyVer = execSync(PYTHON + ' --version', { encoding: 'utf-8', timeout: 10000, stdio: 'pipe' }).trim();
  } catch (_) { /* ignore */ }

  if (!pyVer) fail('PYTHON_NOT_FOUND');
  if (pyVer.startsWith('Python 2.')) fail('PYTHON_VERSION_2');

  var nodeMajor = parseInt(process.versions.node.split('.')[0], 10);
  if (nodeMajor < 18) {
    fail('NODE_VERSION_LOW', { current: String(nodeMajor), required: '>=18' });
  }

  try {
    execSync('npm --version', { encoding: 'utf-8', timeout: 10000, stdio: 'pipe' });
  } catch (_) {
    fail('NPM_NOT_FOUND');
  }

  var tgzFiles = fs.readdirSync(SCRIPTS_DIR)
    .filter(function (f) { return f.startsWith('mtuser-pt-passport-') && f.endsWith('.tgz'); })
    .sort()
    .map(function (f) { return path.join(SCRIPTS_DIR, f); });

  if (tgzFiles.length === 0) fail('TGZ_NOT_FOUND');

  var tgzFile = tgzFiles[tgzFiles.length - 1];
  var bundleVersion = path.basename(tgzFile).replace('mtuser-pt-passport-', '').replace('.tgz', '');

  var localVersion = '';
  try {
    var res = spawnSync(PT_PASSPORT_BIN, ['--version'], { encoding: 'utf-8', timeout: 10000, stdio: 'pipe', shell: true });
    localVersion = (res.stdout || '').trim().split('\n').pop();
  } catch (_) { /* not installed */ }

  if (localVersion !== bundleVersion) {
    try {
      execSync('npm install "' + tgzFile + '" --prefix "' + SCRIPTS_DIR + '" --save-exact --force', { encoding: 'utf-8', timeout: 60000, stdio: 'pipe' });
    } catch (_) {
      fail('INSTALL_FAILED');
    }
  }

  // CLIGuard 检查
  var cliguard = loadCliguard();
  var cliguardOk = !!(cliguard && typeof cliguard.signRequest === 'function');

  var state = readState();
  out({
    ok: true,
    scripts_dir: SCRIPTS_DIR,
    skill_dir: SKILL_DIR,
    tos_accepted: state.tos_accepted === true,
    cliguard_available: cliguardOk
  });
};

/**
 * get-device-token - 获取设备标识
 */
commands['get-device-token'] = function () {
  var result = runPython('auth.py', ['get-device-token']);
  if (result.success && result.device_token) {
    out({ ok: true, device_token: result.device_token });
  } else if (result.device_token) {
    out({ ok: true, device_token: result.device_token });
  } else {
    fail('DEVICE_TOKEN_FAILED', { detail: result });
  }
};

/**
 * get-token - 获取缓存的用户 Token
 */
commands['get-token'] = function () {
  var res = runPassport(['get-token', '--client_id', CLIENT_ID]);
  if (res.exitCode === 0 && res.stdout) {
    out({ ok: true, token: res.stdout });
  } else {
    out({ ok: false, error: 'NO_TOKEN', message: 'Token not found or expired' });
  }
};

/**
 * auth-get-code - 获取授权链接
 */
commands['auth-get-code'] = function () {
  var res = runPassport(['auth', 'get-code', '--client_id', CLIENT_ID]);
  var stdout = res.stdout;

  var tokenMatch = stdout.match(/Token:\s*(.+)/);
  if (tokenMatch) {
    out({ ok: true, type: 'token', token: tokenMatch[1].trim() });
    return;
  }

  var linkMatch = stdout.match(/AUTH_LINK:\s*(.+)/);
  if (linkMatch) {
    out({ ok: true, type: 'auth_link', url: linkMatch[1].trim() });
    return;
  }

  var errorMatch = stdout.match(/code=(\d+)\s*message=(.*)/);
  if (errorMatch) {
    out({ ok: false, error: 'AUTH_ERROR', code: errorMatch[1], message: errorMatch[2].trim() });
    return;
  }

  out({ ok: false, error: 'UNKNOWN', raw: stdout, stderr: res.stderr });
};

/**
 * auth-poll-token - 轮询授权结果
 */
commands['auth-poll-token'] = function () {
  var res = runPassport(['auth', 'poll-token', '--client_id', CLIENT_ID]);
  var stdout = res.stdout;

  var tokenMatch = stdout.match(/Token:\s*(.+)/);
  if (res.exitCode === 0 && tokenMatch) {
    out({ ok: true, token: tokenMatch[1].trim() });
    return;
  }

  var errorMatch = stdout.match(/code=(\d+)\s*message=(.*)/);
  if (errorMatch) {
    out({ ok: false, error: 'POLL_ERROR', code: errorMatch[1], message: errorMatch[2].trim() });
    return;
  }

  out({ ok: false, error: 'POLL_FAILED', raw: stdout, stderr: res.stderr });
};

/**
 * qrcode - 通过服务端接口获取二维码图片 URL
 * 用法: node run.js qrcode <url>
 * 调用 https://click.meituan.com/cps/ai/product/getQrCodeImage
 * POST, body: { originalUrl: url }, 含 cliguard 签名
 */
commands.qrcode = function (argv) {
  var url = argv[0] || '';

  if (!url) {
    out({ ok: false, type: 'skip' });
    return;
  }

  if (url.indexOf('npay.meituan.com') !== -1) {
    out({ ok: false, type: 'skip', message: '支付二维码已由order命令返回payQrCodeImage字段，请直接展示该图片，禁止调用qrcode命令' });
    return;
  }

  var apiUrl = 'https://click.meituan.com/cps/ai/product/getQrCodeImage';
  var body = { originalUrl: url, clientSource: 'qclaw-connector' };

  httpsPost(apiUrl, body)
    .then(function (resp) {
      var data = resp.data;
      if (data && data.data) {
        out({ ok: true, type: 'image', imageUrl: data.data });
      } else {
        out({ ok: false, type: 'skip', message: 'No image returned', raw: data });
      }
    })
    .catch(function (e) {
      out({ ok: false, type: 'skip', message: e.message });
    });
};

/**
 * hotword - 热搜词查询
 */
commands.hotword = function (argv) {
  var parsed = parseArgs(argv);
  if (!parsed.args['city-id']) fail('MISSING_PARAM', { param: 'city-id' });
  var result = runPython('hotword.py', ['--city-id', parsed.args['city-id']]);
  out(Object.assign({ ok: !!result.success }, result));
};

/**
 * search - 商品搜索
 */
commands.search = function (argv) {
  var parsed = parseArgs(argv);
  var args = parsed.args;
  var required = ['keyword', 'lat', 'lng', 'token', 'city-id'];
  for (var ri = 0; ri < required.length; ri++) {
    if (!args[required[ri]]) fail('MISSING_PARAM', { param: required[ri] });
  }

  var pyArgs = [
    '--keyword', args['keyword'],
    '--lat', args['lat'],
    '--lng', args['lng'],
    '--token', args['token'],
    '--city-id', args['city-id']
  ];

  if (args['page']) { pyArgs.push('--page', args['page']); }
  if (args['page-size']) { pyArgs.push('--page-size', args['page-size']); }
  if (args['query-id']) { pyArgs.push('--query-id', args['query-id']); }
  if (args['request-id']) { pyArgs.push('--request-id', args['request-id']); }
  if (args['max-distance-km']) { pyArgs.push('--max-distance-km', args['max-distance-km']); }

  var result = runPython('product_search.py', pyArgs);
  out(Object.assign({ ok: !!result.success }, result));
};

/**
 * location - 获取用户近期位置
 */
commands.location = function (argv) {
  var parsed = parseArgs(argv);
  if (!parsed.args['token']) fail('MISSING_PARAM', { param: 'token' });
  var result = runPython('get_user_recent_location.py', ['--token', parsed.args['token']]);
  out(Object.assign({ ok: !!result.success }, result));
};

/**
 * location-by-address - 根据地址获取经纬度
 */
commands['location-by-address'] = function (argv) {
  var parsed = parseArgs(argv);
  if (!parsed.args['address']) fail('MISSING_PARAM', { param: 'address' });
  var result = runPython('get_location_by_address.py', ['--address', parsed.args['address']]);
  out(Object.assign({ ok: !!result.success }, result));
};

/**
 * order - 下单
 */
commands.order = function (argv) {
  var parsed = parseArgs(argv);
  var args = parsed.args;
  var required = ['product-id', 'poi-id', 'token', 'city-id', 'uuid'];
  for (var ri = 0; ri < required.length; ri++) {
    if (!args[required[ri]]) fail('MISSING_PARAM', { param: required[ri] });
  }

  var pyArgs = [
    '--product-id', args['product-id'],
    '--poi-id', args['poi-id'],
    '--token', args['token'],
    '--city-id', args['city-id'],
    '--uuid', args['uuid']
  ];

  if (args['lat']) { pyArgs.push('--lat', args['lat']); }
  if (args['lng']) { pyArgs.push('--lng', args['lng']); }
  if (args['quantity']) { pyArgs.push('--quantity', args['quantity']); }

  var result = runPython('order.py', pyArgs);
  out(Object.assign({ ok: !!result.success }, result));
};

/**
 * tos-accept - 记录用户已接受服务协议
 */
commands['tos-accept'] = function () {
  writeState({ tos_accepted: true });
  out({ ok: true });
};

/**
 * logout - 退出登录
 */
commands.logout = function () {
  var result = runPython('auth.py', ['logout']);
  out(Object.assign({ ok: !!result.success }, result));
};

/**
 * clear-device-token - 清除设备标识
 */
commands['clear-device-token'] = function () {
  var result = runPython('auth.py', ['clear-device-token']);
  out(Object.assign({ ok: !!result.success }, result));
};

/**
 * issue - 领取优惠券（纯 Node.js 实现）
 * 用法: node run.js issue --token <user_token>
 * 
 * 返回格式（成功）:
 *   { ok: true, coupon_count: N, coupons: [...] }
 * 
 * 返回格式（失败）:
 *   { ok: false, error: "<ERROR_TYPE>", message: "..." }
 * 
 * 副作用：成功时自动更新 .state.json 中的 coupon_claimed_date 和 coupon_claimed_coupons
 */
commands.issue = function (argv) {
  var parsed = parseArgs(argv);
  if (!parsed.args['token']) fail('MISSING_PARAM', { param: 'token' });

  var token = parsed.args['token'];
  var config = loadConfig();
  var aiScene = config.aiScene || '';

  var body = {
    token: token,
    aiScene: aiScene,
    version: 2,
    clientSource: 'qclaw-connector'
  };

  var fullUrl = COUPON_BASE_URL + COUPON_ISSUE_PATH;

  httpsPost(fullUrl, body)
    .then(function (resp) {
      var data = resp.data;
      if (!data) {
        out({ ok: false, error: 'PARSE_ERROR', message: 'Invalid response from server', http_status: resp.status });
        return;
      }

      var code = data.code;
      var msg = data.msg || '';
      var respData = data.data || {};

      if (code === 200) {
        // 领券成功
        var couponList = respData.couponList || [];
        var formattedCoupons = couponList.map(formatCoupon);

        // 更新 .state.json
        writeState({
          coupon_claimed_date: getTodayStr(),
          coupon_claimed_coupons: formattedCoupons
        });

        out({
          ok: true,
          coupon_count: formattedCoupons.length,
          coupons: formattedCoupons
        });

      } else if (code === 1014) {
        // 今日已领取
        writeState({ coupon_claimed_date: getTodayStr() });
        out({
          ok: false,
          error: 'ALREADY_RECEIVED',
          message: '\u60a8\u4eca\u5929\u5df2\u7ecf\u9886\u53d6\u8fc7\u4e86\uff0c\u6bcf\u5929\u53ea\u80fd\u9886\u53d6\u4e00\u6b21\uff0c\u660e\u5929\u518d\u6765\u54e6\uff5e'
        });

      } else if (code === 401) {
        out({ ok: false, error: 'RE_LOGIN', message: '\u767b\u5f55\u5df2\u8fc7\u671f\uff0c\u8bf7\u91cd\u65b0\u767b\u5f55' });

      } else if (code === 509 || code === 50200) {
        out({ ok: false, error: 'RATE_LIMIT', message: '\u8bf7\u6c42\u8fc7\u4e8e\u9891\u7e41\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5' });

      } else if (code === 9999) {
        out({ ok: false, error: 'SYSTEM_ERROR', message: '\u7cfb\u7edf\u5f02\u5e38\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5' });

      } else {
        out({ ok: false, error: 'UNKNOWN_ERROR', message: '\u672a\u77e5\u9519\u8bef\uff08code=' + code + '\uff0cmsg=' + msg + '\uff09' });
      }
    })
    .catch(function (e) {
      if (e.message && e.message.indexOf('TIMEOUT') >= 0) {
        out({ ok: false, error: 'TIMEOUT', message: '\u8bf7\u6c42\u8d85\u65f6\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5' });
      } else {
        out({ ok: false, error: 'NETWORK_ERROR', message: '\u7f51\u7edc\u5f02\u5e38\uff1a' + e.message });
      }
    });
};

/**
 * coupon-status - 查询今日领券状态
 * 读取 .state.json 中的 coupon_claimed_date 判断今天是否已领
 */
commands['coupon-status'] = function () {
  var state = readState();
  var today = getTodayStr();
  var claimed = state.coupon_claimed_date === today;
  out({
    ok: true,
    claimed_today: claimed,
    claimed_date: state.coupon_claimed_date || null,
    coupons: claimed ? (state.coupon_claimed_coupons || []) : []
  });
};

// -- 入口 --

var allArgs = process.argv.slice(2);
var command = allArgs[0];
var commandArgs = allArgs.slice(1);

if (!command || command === '--help' || command === '-h') {
  console.log('Usage: node run.js <command> [options]\n\nCommands:\n  init                     Environment setup (returns tos_accepted field)\n  tos-accept               Mark TOS as accepted (writes to local .state.json)\n  get-device-token         Get device token\n  get-token                Get cached user token\n  auth-get-code            Get auth link\n  auth-poll-token          Poll auth result\n  qrcode <url>             Get QR code image URL (server-side)\n  hotword --city-id <id>   Hot search words\n  search --keyword <kw> --lat <lat> --lng <lng> --token <t> --city-id <id>\n  location --token <t>     Get recent location\n  location-by-address --address <addr>\n  order --product-id <pid> --poi-id <pid> --token <t> --city-id <id> --uuid <u>\n  issue --token <t>        Claim daily coupon\n  coupon-status            Check today\'s coupon claim status\n  logout                   Logout\n  clear-device-token       Clear device token');
  process.exit(0);
}

if (!commands[command]) {
  fail('UNKNOWN_COMMAND', { command: command, available: Object.keys(commands) });
}

commands[command](commandArgs);
