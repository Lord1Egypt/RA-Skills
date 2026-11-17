/**
 * 蓝奏云下载器 - 纯 Node.js 实现，零外部依赖，纯本地解析（不调用任何第三方服务）
 * 用法: node download.js <蓝奏云分享链接> [输出文件路径] [密码] [--select 目标...] [--insecure]
 *   密码可选，若不提供且链接需要密码，会报错提示
 *   文件夹分享自动识别（蓝奏云分享仅含单层文件，子文件夹不参与分享；t==1 推广条目自动跳过）
 *   --select 支持文件名精确匹配 / * 通配符 / 多目标逗号分隔
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const vm = require('vm');
const url = require('url');
const path = require('path');
const zlib = require('zlib');

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';

// TLS 证书校验：默认开启严格校验。蓝奏云个别镜像域证书异常时，可用 `--insecure`
// 或环境变量 LANZOU_INSECURE_TLS=1 显式关闭（⚠️ 关闭后下载内容可被中间人篡改，自担风险）。
const INSECURE_TLS = process.argv.includes('--insecure') || process.env.LANZOU_INSECURE_TLS === '1';

// 连接复用：蓝奏云下载域（developer*.lanrar.com 等）对「每次新建连接」的请求会判定为
// 网络异常，返回「系统发现您的网络异常，需要验证后下载文件」页；复用 TCP 连接（keep-alive）
// 后直链会直接返回文件流。这是下载能成功的关键，勿改为默认 agent。
const keepAliveHttps = new https.Agent({ keepAlive: true, maxSockets: 4, keepAliveMsecs: 15000 });
const keepAliveHttp = new http.Agent({ keepAlive: true, maxSockets: 4, keepAliveMsecs: 15000 });

// ─── 批量路由用：--list（只解析清单、不下载） ───────────────
let LIST_ONLY = false;
function emitList(items) {
  console.log('__LANZOU_LIST__' + JSON.stringify(items));
}

// ─── 工具函数 ───────────────────────────────────────────────

/**
 * 去除 JavaScript 注释（块注释和行注释）。
 * 注意：必须先保护协议里的 `://`（如 'https://apifile.lanzouw.com/ajaxfile.php'），
 * 否则 `//` 会被当成行注释删掉，导致从 JS 里提取 URL 时得到 "https:" 之类的残缺值。
 */
const URL_SLASH_TOKEN = '@@__URL_SLASH__@@';
function stripJsComments(code) {
  const guarded = code.replace(/([A-Za-z][A-Za-z0-9+.-]*:)\/\//g, '$1' + URL_SLASH_TOKEN);
  return guarded
    .replace(/\/\*[\s\S]*?\*\//g, '')  // 去除 /* ... */
    .replace(/\/\/.*$/gm, '')          // 去除 //
    .split(URL_SLASH_TOKEN).join('//');
}

function request(method, targetUrl, opts = {}) {
  const { cookieJar = {}, body, redirectCount = 0, encoding = null } = opts;
  if (redirectCount > 8) return Promise.reject(new Error('重定向次数过多'));

  return new Promise((resolve, reject) => {
    const u = new URL(targetUrl);
    const mod = u.protocol === 'https:' ? https : http;
    const headers = {
      'User-Agent': UA,
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      ...opts.headers,
    };

    // 组装 Cookie
    const mergedCookies = { ...cookieJar };
    if (headers['Cookie']) {
      headers['Cookie'].split(';').forEach(p => {
        const eq = p.indexOf('=');
        if (eq > 0) mergedCookies[p.substring(0, eq).trim()] = p.substring(eq + 1).trim();
      });
    }
    const cookieStr = Object.entries(mergedCookies).map(([k,v]) => `${k}=${v}`).join('; ');
    if (cookieStr) headers['Cookie'] = cookieStr;

    if (body) {
      headers['Content-Length'] = Buffer.byteLength(body);
    }

    const reqOpts = {
      hostname: u.hostname,
      port: u.port || (u.protocol === 'https:' ? 443 : 80),
      path: u.pathname + u.search,
      method,
      headers,
      agent: u.protocol === 'https:' ? keepAliveHttps : keepAliveHttp,
      rejectUnauthorized: !INSECURE_TLS,
    };

    const req = mod.request(reqOpts, (res) => {
      // 解析 set-cookie
      const setCookies = res.headers['set-cookie'];
      if (setCookies) {
        setCookies.forEach(c => {
          const semi = c.indexOf(';');
          const pair = semi > 0 ? c.substring(0, semi) : c;
          const eq = pair.indexOf('=');
          if (eq > 0) mergedCookies[pair.substring(0, eq).trim()] = pair.substring(eq + 1).trim();
        });
      }

      // 处理重定向
      if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location) {
        const loc = new URL(res.headers.location, targetUrl).href;
        return resolve(request(method, loc, { ...opts, cookieJar: mergedCookies, redirectCount: redirectCount + 1 }));
      }

      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        let raw = Buffer.concat(chunks);
        const ce = res.headers['content-encoding'];
        if (ce === 'gzip') raw = zlib.gunzipSync(raw);
        else if (ce === 'deflate') raw = zlib.inflateSync(raw);

        let text = raw.toString('utf8');

        // 非文本内容检测
        if (text.length > 0 && text.length < raw.length * 0.8) {
          text = '';
        }

        resolve({
          status: res.statusCode,
          headers: res.headers,
          body: text,
          raw,
          cookies: mergedCookies,
          url: targetUrl,
        });
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('请求超时')); });
    if (body) req.write(body);
    req.end();
  });
}

/**
 * 打开一个流式 GET 请求（自动跟随重定向）。
 * - 复用 keep-alive 连接（下载域对新建连接会要求「网络异常验证」）
 * - 跨域跳转（如跳到 CDN）时清除 Referer，防防盗链断流
 * - 带上 cookieJar（下载域可能下发/要求 cookie，含反爬 cookie）
 */
function openStream(targetUrl, cookieJar = {}, referer = '') {
  const follow = (url, redirects) => {
    if (redirects > 8) return Promise.reject(new Error('重定向次数过多'));
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    const headers = {
      'User-Agent': UA,
      'Accept': '*/*',
      'Accept-Language': 'zh-CN,zh;q=0.9',
    };
    if (referer && redirects === 0) headers['Referer'] = referer;
    const ck = Object.entries(cookieJar).map(([k, v]) => `${k}=${v}`).join('; ');
    if (ck) headers['Cookie'] = ck;

    return new Promise((res, rej) => {
      const r = mod.request({
        hostname: u.hostname,
        port: u.port || (u.protocol === 'https:' ? 443 : 80),
        path: u.pathname + u.search,
        method: 'GET',
        headers,
        agent: u.protocol === 'https:' ? keepAliveHttps : keepAliveHttp,
        rejectUnauthorized: !INSECURE_TLS,
      }, (rs) => res(rs));
      r.on('error', rej);
      r.setTimeout(30000, () => { r.destroy(); rej(new Error('超时')); });
      r.end();
    }).then((rs) => {
      if ([301, 302, 303, 307, 308].includes(rs.statusCode) && rs.headers.location) {
        return follow(new URL(rs.headers.location, url).href, redirects + 1);
      }
      return rs;
    });
  };
  return follow(targetUrl, 0);
}

/** 把响应体读成字符串（仅用于体积很小的 HTML 反爬/验证页；按 content-encoding 解压） */
function readBody(resp) {
  return new Promise((res, rej) => {
    const chunks = [];
    resp.on('data', (c) => chunks.push(c));
    resp.on('end', () => {
      let raw = Buffer.concat(chunks);
      const ce = resp.headers['content-encoding'];
      try {
        if (ce === 'gzip') raw = zlib.gunzipSync(raw);
        else if (ce === 'deflate') raw = zlib.inflateSync(raw);
        else if (ce === 'br') raw = zlib.brotliDecompressSync(raw);
      } catch (e) { /* 解压失败则按原文处理 */ }
      res(raw.toString('utf8'));
    });
    resp.on('error', rej);
  });
}

function streamDownload(targetUrl, filePath, opts = {}) {
  const cookieJar = { ...(opts.cookieJar || {}) };
  return new Promise((resolve, reject) => {
    const doAttempt = async (attempt, acwTries) => {
      const resp = await openStream(targetUrl, cookieJar, opts.referer || '');

      // 收集下载域下发的 cookie（后续重试带上）
      (resp.headers['set-cookie'] || []).forEach((c) => {
        const pair = c.split(';')[0];
        const eq = pair.indexOf('=');
        if (eq > 0) cookieJar[pair.slice(0, eq).trim()] = pair.slice(eq + 1).trim();
      });

      const ct = String(resp.headers['content-type'] || '');

      // HTML 响应 = 反爬挑战页或「网络异常验证」页，按类型处理
      if (ct.includes('text/html')) {
        const html = await readBody(resp);
        if (html.includes("arg1='")) {
          if (acwTries >= 3) throw new Error('反爬未通过: acw_sc__v2 校验失败');
          console.log(`    ℹ 下载域反爬挑战，重新计算 cookie 后重试 (${acwTries + 1}/3)`);
          computeAcw(html, cookieJar);
          return doAttempt(attempt, acwTries + 1);
        }
        if (html.includes("'file':'") || html.includes('ajax.php')) {
          throw new Error('下载域要求「网络异常验证」（连接未复用或 IP 被限流时触发），请重试；仍失败请更换网络或浏览器下载');
        }
        throw new Error(`下载链接返回 HTML 页面而非文件（链接可能失效或触发风控）：${html.replace(/\s+/g, ' ').slice(0, 200)}`);
      }

      if (resp.statusCode >= 400) {
        resp.resume();
        throw new Error(`下载失败: HTTP ${resp.statusCode}`);
      }

      const total = parseInt(resp.headers['content-length'] || '0', 10);
      let written = 0;
      const file = fs.createWriteStream(filePath);
      await new Promise((res, rej) => {
        const onError = (e) => { file.destroy(); rej(e); };
        resp.on('error', onError);
        resp.on('aborted', () => onError(new Error('连接被服务器中断')));
        file.on('error', onError);
        resp.on('data', (c) => { written += c.length; });
        file.on('finish', () => {
          if (total > 0 && written !== total) {
            file.destroy();
            rej(new Error(`下载不完整: 期望 ${total} 字节, 实际 ${written} 字节`));
            return;
          }
          res(written);
        });
        resp.pipe(file);
      });
      return written;
    };

    const run = async () => {
      let lastErr = null;
      for (let i = 0; i < 3; i++) {
        try {
          return await doAttempt(0, 0);
        } catch (e) {
          lastErr = e;
          // CDN 断流/超时/大小不符属于常态，自动重试；其他错误直接抛出
          const retryable = /中断|超时|不完整|ECONNRESET|socket hang up|EPIPE/i.test(e.message);
          if (!retryable || i === 2) throw e;
          console.log(`    ⚠ 下载中断 (${e.message})，自动重试 ${i + 1}/2 ...`);
        }
      }
      throw lastErr;
    };

    run().then(resolve).catch(reject);
  });
}

// ─── 密码处理 ───────────────────────────────────────────────

/**
 * 检测页面是否需要密码，如果需要则提交密码并获取真实下载地址
 * @returns {{ needsPwd: boolean, fullDownUrl: string | null, fileName: string | null, error: string | null }}
 */
async function handlePassword(lanzouUrl, cookies, body, password) {
  const hasPwd = body.includes('passwddiv');
  if (!hasPwd) return { needsPwd: false, fullDownUrl: null, fileName: null, error: null };

  if (!password) {
    return { needsPwd: true, fullDownUrl: null, fileName: null, error: '此链接需要密码，请在命令中提供密码参数' };
  }

  console.log('\n[3/6] 检测到密码保护，提交密码...');

  // 提取 fid
  const fidMatch = body.match(/ajax(?:m|file)\.php\?file=(\d+)/);
  if (!fidMatch) return { needsPwd: true, fullDownUrl: null, fileName: null, error: '无法提取文件 ID' };
  const fid = fidMatch[1];
  console.log(`  fid: ${fid}`);

  // 提取 kdns
  const kdnsMatch = body.match(/var\s+kdns\s*=\s*(\d+)/);
  const kdns = kdnsMatch ? kdnsMatch[1] : '1';
  console.log(`  kdns: ${kdns}`);

  // 提取 sign / 提交地址（兼容旧版 ajaxm.php 与新版 apifile.woozooo.com/ajaxfile.php）
  const downPStart = body.indexOf('function down_p()');
  const downPEnd = downPStart >= 0 ? body.indexOf('</script>', downPStart) : -1;
  const scope = (downPStart >= 0 && downPEnd > downPStart) ? body.substring(downPStart, downPEnd) : body;

  let sign = null;
  const litSign = scope.match(/['"]sign['"]\s*:\s*'([^']+)'/);
  if (litSign) sign = litSign[1];
  if (!sign) {
    const varNameM = scope.match(/['"]sign['"]\s*:\s*([A-Za-z_$][\w$]*)/);
    if (varNameM) {
      const re = new RegExp('var\\s+' + varNameM[1] + "\\s*=\\s*'([^']+)'", 'g');
      const vals = [...scope.matchAll(re)].map((m) => m[1]).filter(Boolean);
      if (vals.length) sign = vals[vals.length - 1];
    }
  }
  if (!sign) {
    const vals = [...body.matchAll(/var\s+(?:isngis|sign)\s*=\s*'([^']+)'/g)].map((m) => m[1]).filter(Boolean);
    if (vals.length) sign = vals[vals.length - 1];
  }
  if (!sign) return { needsPwd: true, fullDownUrl: null, fileName: null, error: '无法提取 sign 参数' };
  console.log(`  sign: ${sign.substring(0, 16)}...`);

  // POST 密码（优先用页面声明的完整 ajax 地址，如 https://apifile.woozooo.com/ajaxfile.php?file=xxx）
  let pwdUrl = null;
  const ajaxUrlM = scope.match(/['"](https?:\/\/[^'"]+\/ajax(?:m|file)\.php\?file=\d+)['"]/i);
  if (ajaxUrlM) pwdUrl = ajaxUrlM[1];
  if (!pwdUrl) pwdUrl = new URL(`/ajaxm.php?file=${fid}`, lanzouUrl).href;
  console.log(`  提交地址: ${pwdUrl.substring(0, 60)}...`);
  const postData = new URLSearchParams({
    action: 'downprocess',
    sign: sign,
    kd: kdns,
    p: password,
  }).toString();

  console.log(`  提交密码到: ${pwdUrl}`);
  const pwdResp = await request('POST', pwdUrl, {
    cookieJar: cookies,
    headers: {
      'Referer': lanzouUrl,
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: postData,
  });
  // 把密码校验过程中下发的 cookie 合并回会话（下载阶段需要带同一会话）
  Object.assign(cookies, pwdResp.cookies || {});

  try {
    const json = JSON.parse(pwdResp.body);
    console.log(`  服务器响应: zt=${json.zt}`);

    if (String(json.zt) !== '1') {
      return { needsPwd: true, fullDownUrl: null, fileName: null, error: `密码错误或验证失败: ${json.inf || '未知原因'}` };
    }

    const dom = json.dom.replace(/\\\//g, '/');
    const fileUrl = json.url.replace(/\\\//g, '/');
    const fullDownUrl = dom + '/file/' + fileUrl;
    const fileName = json.inf || null;

    console.log(`  文件名: ${fileName}`);
    console.log(`  下载地址: ${fullDownUrl.substring(0, 80)}...`);

    return { needsPwd: true, fullDownUrl, fileName, error: null };
  } catch (e) {
    console.error('  密码响应:', pwdResp.body.substring(0, 300));
    return { needsPwd: true, fullDownUrl: null, fileName: null, error: `密码验证响应解析失败: ${e.message}` };
  }
}

// ─── 文件夹分享下载（本地解析，单层）────────────────────────

/** 执行反爬 JS，计算 acw_sc__v2 并合并进 cookieJar */
function computeAcw(body, cookieJar) {
  const scriptMatch = body.match(/<script>([\s\S]*?)<\/script>/);
  if (!scriptMatch || !body.includes('arg1=')) return cookieJar;
  const fakeDoc = { cookie: '', location: { reload: () => {} } };
  const ctx = vm.createContext({ document: fakeDoc, Date, console: { log: () => {}, error: () => {}, warn: () => {} } });
  try { vm.runInContext(scriptMatch[1], ctx, { timeout: 5000 }); } catch (e) {}
  if (fakeDoc.cookie) {
    const parts = fakeDoc.cookie.split(';')[0].split('=');
    if (parts.length >= 2) cookieJar[parts[0].trim()] = parts.slice(1).join('=').trim();
  }
  return cookieJar;
}

/** 带反爬自动重试的请求：响应为反爬页时计算 cookie 重试一次 */
async function reqWithAcw(method, url, opts = {}) {
  let resp = await request(method, url, opts);
  if (resp.body.includes('arg1=')) {
    const newCookies = computeAcw(resp.body, { ...opts.cookieJar });
    resp = await request(method, url, { ...opts, cookieJar: newCookies });
    if (resp.body.includes('arg1=')) throw new Error(`反爬未通过: ${url.substring(0, 60)}`);
  }
  return resp;
}

/**
 * 从 iframe 页 JS 中提取实际 ajax 接口地址。
 * v1.0.11 修复：
 *   1) 不再使用 stripJsComments —— 直接在原始 iframeBody 上匹配，避免字符串里的 `https://`
 *      被当行注释删掉（旧逻辑会得到 "https:"，只能回退已废弃的 /ajaxm.php → 404）。
 *   2) 优先提取 domain1/domain2 的完整地址（新版蓝奏云其本身即完整 URL，自带 ?file=xxx），
 *      调用方不再用 searchParams.set('file') 覆盖，避免文件 ID 丢失。
 * 找不到时回退 /ajaxm.php。
 */
function extractAjaxPath(iframeBody, fid) {
  // 校验：候选值必须像 URL/路径（不含空白、非残缺值）
  const plausible = (v) => !!v && v.length > 3 && !/\s/.test(v) && (v.includes('/') || v.includes('?'));

  const candidates = [];
  // $.ajax({ url: '...' }) 的字面量地址（直接在原始 JS 上匹配，不做注释剥离）
  const m1 = iframeBody.match(/\$\.ajax\(\s*\{[^}]*?url\s*:\s*['"]([^'"]+)['"]/);
  if (m1) candidates.push(m1[1]);
  // domain1 / domain2 声明的地址
  const m2 = iframeBody.match(/var\s+domain1\s*=\s*['"]([^'"]+)['"]/);
  if (m2) candidates.push(m2[1]);
  const m3 = iframeBody.match(/var\s+domain2\s*=\s*['"]([^'"]+)['"]/);
  if (m3) candidates.push(m3[1]);
  // 其它指向 ajax 的 url 字面量
  const m4 = iframeBody.match(/url\s*:\s*['"]([^'"]*ajax[^'"]*)['"]/);
  if (m4) candidates.push(m4[1]);

  // 优先：自带 file 参数的完整地址 —— 直接采用，避免后续再被覆盖
  const withFile = candidates.find((v) => plausible(v) && /[?&]file=/.test(v));
  if (withFile) return withFile;

  // 其次：任意有效地址；缺 file 参数时补上（不覆盖已有值）
  const base = candidates.find(plausible);
  if (base) {
    if (fid && !/[?&]file=/.test(base)) {
      return base + (base.includes('?') ? '&' : '?') + 'file=' + fid;
    }
    return base;
  }
  return '/ajaxm.php';
}

/** 解析文件夹内单个文件的直链并下载 */
async function downloadFile(fileId, baseOrigin, cookies, outPath) {
  try {
    const pageUrl = `${baseOrigin}/${fileId}`;
    const resp = await reqWithAcw('GET', pageUrl, { cookieJar: cookies });
    const body = resp.body;
    if (body.includes('arg1=')) throw new Error(`文件 ${fileId}: 反爬未通过`);
    const fnM = body.match(/src="([^"]*\/fn\?[^"]+)"/);
    if (!fnM) throw new Error(`文件 ${fileId}: 未找到下载入口`);
    const fnPath = fnM[1];
    // 提取真实 fid（POST 下载地址时使用）
    const fidMatch = body.match(/var\s+fid\s*=\s*(\d+)/);
    const fid = fidMatch ? fidMatch[1] : null;
    const fnResp = await reqWithAcw('GET', `${baseOrigin}${fnPath}`, { cookieJar: resp.cookies, headers: { 'Referer': pageUrl } });
    const fnBody = fnResp.body;
    const wpM = fnBody.match(/var\s+wp_sign\s*=\s*'([^']+)'/);
    const adM = fnBody.match(/var\s+ajaxdata\s*=\s*'([^']+)'/);
    const kdM = fnBody.match(/var\s+kdns\s*=\s*(\d+)/);
    if (!wpM || !adM) throw new Error(`文件 ${fileId}: fn 页参数提取失败`);
    const postData = new URLSearchParams({
      action: 'downprocess', websignkey: adM[1], signs: adM[1],
      sign: wpM[1], websign: '', kd: kdM ? kdM[1] : '1', ves: '1',
    }).toString();
    // ajax 接口路径从 fn 页 JS 动态提取（写死 /ajaxm.php 在某些域名会 zt=0）
    const ajaxUrl = new URL(extractAjaxPath(fnBody, fid), baseOrigin);
    const ajax = await reqWithAcw('POST', ajaxUrl.href, {
      cookieJar: fnResp.cookies,
      headers: {
        'Referer': `${baseOrigin}${fnPath}`, 'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest',
      },
      body: postData,
    });
    let json;
    try { json = JSON.parse(ajax.body); } catch (e) { throw new Error(`文件 ${fileId}: ajax 响应非 JSON`); }
    if (json.zt !== 1) throw new Error(`文件 ${fileId}: zt=${json.zt} ${json.inf || ''}`);
    const dom = json.dom.replace(/\\\//g, '/');
    const fileUrl = json.url.replace(/\\\//g, '/');
    const fullUrl = dom + '/file/' + fileUrl;
    const size = await streamDownload(fullUrl, outPath, { referer: fullUrl, cookieJar: ajax.cookies });
    return { name: json.inf || String(fileId), size };
  } catch (e) {
    throw e;
  }
}

// ─── 文件夹分享（单层 + 选择性下载）────────────────────────

/** 从文件夹分享页 HTML 提取 filemoreajax 参数（fid/uid/puid/t/k） */
function extractFolderParams(body) {
  const fidM = body.match(/filemoreajax\.php\?file=(\d+)/);
  const uidM = body.match(/'uid':'(\d+)'/);
  const puidM = body.match(/'puid':'([^']+)'/);
  const tM = body.match(/var\s+\w+\s*=\s*'(\d{8,})'/);
  const kM = body.match(/var\s+\w+\s*=\s*'([a-f0-9]{32})'/);
  return {
    fid: fidM ? fidM[1] : null,
    uid: uidM ? uidM[1] : '',
    puid: puidM ? puidM[1] : '',
    t: tM ? tM[1] : '',
    k: kM ? kM[1] : '',
  };
}

/** 清理列表项名称（去 HTML 标签） */
function cleanItemName(n) {
  return (n.name_all || '').replace(/<[^>]+>/g, '').trim();
}

/** 正则转义（用于通配符匹配） */
function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** 匹配 --select 段与列表条目（按 id 短码 / 名称 / * 通配符） */
function matchItem(item, seg) {
  if (!seg) return false;
  if (item.id === seg) return true;
  const name = cleanItemName(item);
  if (name === seg) return true;
  if (seg.includes('*')) {
    const re = new RegExp('^' + seg.split('*').map(escapeRegExp).join('.*') + '$');
    return re.test(name) || re.test(item.id);
  }
  return false;
}

/**
 * 列出文件夹某一层（filemoreajax，自动翻页）。
 * @returns {{ files: Array, folders: Array }} t==0 为文件、t==1 为子文件夹
 */
async function listFolder(baseOrigin, referer, params, cookies, pwd) {
  const PAGE_SIZE = 50;
  const all = [];
  let page = 1;
  while (page <= 50) {
    const postData = new URLSearchParams({
      lx: '2', fid: params.fid, uid: params.uid, puid: params.puid,
      pg: String(page), rep: '0', t: params.t, k: params.k, up: '1', ls: '1', pwd: pwd || '',
    }).toString();
    let listJson;
    try {
      const listResp = await reqWithAcw('POST', `${baseOrigin}/filemoreajax.php?file=${params.fid}`, {
        cookieJar: cookies,
        headers: {
          'Referer': referer, 'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest',
        },
        body: postData,
      });
      listJson = JSON.parse(listResp.body);
      if (String(listJson.zt) !== '1') throw new Error(`zt=${listJson.inf || '未知'}`);
    } catch (e) {
      if (page === 1) throw e;
      console.log(`  第 ${page} 页获取失败 (${e.message})，停止翻页`);
      break;
    }
    const items = (listJson.text || []).filter(n => n.id && n.id !== '-1');
    all.push(...items);
    if (items.length < PAGE_SIZE) break;
    page++;
  }
  return { files: all.filter(n => n.t != 1), folders: all.filter(n => n.t == 1) };
}

/**
 * 收集文件夹分享中的文件（蓝奏云分享仅单层，子文件夹/推广条目不参与下载）。
 * @param {string} baseOrigin 分享域名源
 * @param {string} folderUrl  当前文件夹页面 URL
 * @param {Object} cookies    cookie jar
 * @param {string} body       当前文件夹页面 HTML
 * @param {string} pwd        当前文件夹密码
 * @param {Array|null} select --select 目标数组（文件名精确匹配，支持 * 通配）
 * @param {Array} results     收集结果 [{id,name,relDir,size}]
 * @param {string} relDir     相对输出根目录
 */
async function collectFolder(baseOrigin, folderUrl, cookies, body, pwd, select, results, relDir) {
  const params = extractFolderParams(body);
  if (!params.fid) throw new Error('未找到文件夹 ID');
  const list = await listFolder(baseOrigin, folderUrl, params, cookies, pwd);

  // select 目标拆段：'a/b.zip' -> ['a','b.zip']
  const selSegs = (select || []).map(s => s.split('/').filter(Boolean));

  // ── 文件（t==0）：匹配末级目标 ──
  for (const f of list.files) {
    if (select && !selSegs.some(segs => segs.length === 1 && matchItem(f, segs[0]))) continue;
    results.push({ id: f.id, name: cleanItemName(f) || f.id, relDir, size: f.size || '' });
  }

  // ── 子文件夹（t==1）──
  // 蓝奏云分享只含单层文件，子文件夹不参与分享（alist 官方文档确认）。
  // 列表中的 t==1 条目是蓝奏云插入的推广/广告内容（页面 JS 标记为 s_ad 推广），一律跳过不下载。
  for (const folder of list.folders) {
    const fname = cleanItemName(folder) || folder.id;
    console.log(`  ⏭ 跳过推广条目: ${fname}`);
  }
}

/** 文件夹分享：解析（单层）→ 选择性下载 */
async function folderDownload(lanzouUrl, cookies, body, password, outputPath, selectTargets) {
  const baseOrigin = new URL(lanzouUrl).origin;
  console.log('\n[3/6] 检测到文件夹分享，解析文件列表...');
  if (!password && body.includes('passwddiv')) throw new Error('此文件夹需要密码，请提供密码参数');

  const results = [];
  await collectFolder(baseOrigin, lanzouUrl, cookies, body, password || '', selectTargets, results, '');

  if (!results.length) throw new Error('没有匹配到任何文件（检查 --select 目标是否正确）');
  const mode = selectTargets ? '选择性' : '全部';
  console.log(`  [${mode}] 共 ${results.length} 个文件:`);
  results.forEach(r => console.log(`    - ${r.relDir ? r.relDir + '/' : ''}${r.name} (${r.size})`));

  if (LIST_ONLY) {
    emitList(results.map(r => ({ name: r.name, relDir: r.relDir || '', size: r.size || '', id: r.id, folder: true })));
    return null;
  }

  const outDir = outputPath || path.join(process.cwd(), 'lanzou_folder');
  fs.mkdirSync(outDir, { recursive: true });

  let ok = 0, fail = 0;
  for (const f of results) {
    const dir = path.join(outDir, f.relDir);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const safeName = f.name.replace(/[\\/:*?"<>|]/g, '_');
    const outFile = path.join(dir, safeName);
    console.log(`\n  ▶ ${f.relDir ? f.relDir + '/' : ''}${f.name} ...`);
    try {
      const info = await downloadFile(f.id, baseOrigin, cookies, outFile);
      console.log(`    ✅ 完成 (${(info.size / 1048576).toFixed(1)} MB)`);
      ok++;
    } catch (e) {
      console.log(`    ❌ 失败: ${e.message}`);
      fail++;
    }
  }
  console.log(`\n✅ 文件夹下载完成: ${ok} 成功, ${fail} 失败`);
  console.log(`   输出目录: ${outDir}`);
  return outDir;
}

// ─── 主流程 ──────────────────────────────────────────────────


async function download(lanzouUrl, outputPath = null, password = null, selectTargets = null) {
  console.log(`蓝奏云下载器启动`);
  console.log(`链接: ${lanzouUrl}`);
  if (password) console.log(`密码: ${'*'.repeat(password.length)}`);

  // Step 1: 访问分享页
  console.log('\n[1/5] 访问分享页...');
  let resp = await request('GET', lanzouUrl);
  console.log(`  状态: ${resp.status}, 大小: ${resp.body.length} 字节`);

  let cookies = resp.cookies;
  let body = resp.body;

  // Step 2: JS 反爬验证
  if (body.includes('arg1=')) {
    console.log('\n[2/5] 检测到 JS 反爬验证，计算 cookie...');
    const arg1Match = body.match(/var arg1='([^']+)'/);
    if (!arg1Match) throw new Error('无法提取 arg1');
    const arg1 = arg1Match[1];
    console.log(`  arg1: ${arg1.substring(0, 8)}... (${arg1.length} 字符)`);

    const scriptMatch = body.match(/<script>([\s\S]*?)<\/script>/);
    if (!scriptMatch) throw new Error('无法提取 JS 脚本');

    const fakeDoc = { cookie: '', location: { reload: () => {} } };
    const ctx = vm.createContext({
      document: fakeDoc,
      Date: Date,
      console: { log: () => {}, error: () => {}, warn: () => {} },
    });

    vm.runInContext(scriptMatch[1], ctx, { timeout: 5000 });

    if (fakeDoc.cookie) {
      const parts = fakeDoc.cookie.split(';')[0].split('=');
      if (parts.length >= 2) {
        cookies[parts[0].trim()] = parts.slice(1).join('=').trim();
        console.log(`  acw_sc__v2: ${cookies['acw_sc__v2']?.substring(0, 12)}...`);
      }
    } else {
      throw new Error('JS 执行后未获取到 cookie');
    }

    resp = await request('GET', lanzouUrl, { cookieJar: cookies });
    body = resp.body;
    console.log(`  重试后状态: ${resp.status}, 大小: ${body.length} 字节`);
  } else {
    console.log('\n[2/5] 无需 JS 反爬');
  }

  // Step 3: 文件夹分享检测（lx=2 目录，单层 + 选择性下载）
  if (body.includes('filemoreajax')) {
    return await folderDownload(lanzouUrl, cookies, body, password, outputPath, selectTargets);
  }

  // Step 3: 密码处理（如果需要）
  let fullDownUrl = null;
  let fileName = null;

  try {
    const pwdResult = await handlePassword(lanzouUrl, cookies, body, password);
    if (pwdResult.error) throw new Error(pwdResult.error);
    if (pwdResult.fullDownUrl) {
      // 密码流程：直接跳到下载
      fullDownUrl = pwdResult.fullDownUrl;
      fileName = pwdResult.fileName;
    } else {
      // 无密码流程：继续解析 iframe
      console.log('\n[3/5] 解析下载页...');
      const iframeMatch = body.match(/<iframe[^>]*src=["']([^"']*)["']/i);
      if (!iframeMatch) throw new Error('未找到 iframe 下载入口');
      const iframeSrc = iframeMatch[1];
      console.log(`  iframe: ${iframeSrc.substring(0, 50)}...`);

      const fidMatch = body.match(/var\s+fid\s*=\s*(\d+)/);
      const fid = fidMatch ? fidMatch[1] : null;
      console.log(`  fid: ${fid}`);

      const titleMatch = body.match(/<title>([^<]+)<\/title>/);
      fileName = titleMatch ? titleMatch[1].replace(' - 蓝奏云', '').trim() : null;
      if (fileName) console.log(`  文件: ${fileName}`);

      // Step 4: 请求 iframe 获取 AJAX 参数（带反爬自动重试，iframe 页也可能有 arg1= 反爬）
      console.log('\n[4/5] 请求 AJAX 参数...');
      const iframeUrl = new URL(iframeSrc, resp.url).href;
      const iframeResp = await reqWithAcw('GET', iframeUrl, {
        cookieJar: cookies,
        headers: { 'Referer': resp.url },
      });
      cookies = iframeResp.cookies;

      const iframeBody = iframeResp.body;
      const ajaxMatch = iframeBody.match(/var\s+ajaxdata\s*=\s*'([^']*)'/);
      const signMatch = iframeBody.match(/var\s+wp_sign\s*=\s*'([^']*)'/);
      const kdnsMatch = iframeBody.match(/var\s+kdns\s*=\s*(\d+)/);

      if (!ajaxMatch || !signMatch) throw new Error('无法提取 AJAX 参数');
      const ajaxdata = ajaxMatch[1];
      const wpSign = signMatch[1];
      const kdns = kdnsMatch ? parseInt(kdnsMatch[1]) : 1;
      console.log(`  ajaxdata: ${ajaxdata}, kdns: ${kdns}`);

      // POST 获取真实下载地址（ajax 路径从 iframe JS 动态提取，不写死 /ajaxm.php）
      const ajaxUrl = new URL(extractAjaxPath(iframeBody, fid), resp.url);
      const postData = new URLSearchParams({
        action: 'downprocess',
        websignkey: ajaxdata,
        signs: ajaxdata,
        sign: wpSign,
        websign: '',
        kd: String(kdns),
        ves: '1',
      }).toString();

      const ajaxResp = await request('POST', ajaxUrl.href, {
        cookieJar: iframeResp.cookies,
        headers: {
          'Referer': iframeUrl,
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: postData,
      });

      let ajaxBody = ajaxResp.body;
      cookies = ajaxResp.cookies;
      try {
        const json = JSON.parse(ajaxBody);
        console.log(`  zt: ${json.zt}, dom: ${json.dom}`);

        if (json.zt !== 1) throw new Error(`服务器返回 zt=${json.zt}（非成功状态）`);

        const dom = json.dom.replace(/\\\//g, '/');
        const fileUrl = json.url.replace(/\\\//g, '/');
        fullDownUrl = dom + '/file/' + fileUrl;
        console.log(`  下载地址: ${fullDownUrl.substring(0, 80)}...`);
      } catch (e) {
        console.error('  AJAX 响应:', ajaxBody.substring(0, 500));
        throw new Error(`解析下载地址失败: ${e.message}`);
      }
    }
  } catch (e) {
    throw e;
  }

  if (LIST_ONLY) {
    emitList([{ name: fileName || 'download', relDir: '', size: '', id: '', folder: false }]);
    return null;
  }

  // Step 5: 流式下载
  const targetFile = outputPath || path.join(process.cwd(), fileName || 'download.zip');
  const dir = path.dirname(targetFile);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  console.log(`\n[5/5] 下载文件 → ${targetFile}`);
  const size = await streamDownload(fullDownUrl, targetFile, {
    referer: lanzouUrl,
    cookieJar: cookies,
  });

  const sizeMB = (size / (1024 * 1024)).toFixed(1);
  console.log(`\n✅ 下载完成: ${path.basename(targetFile)} (${sizeMB} MB)`);
  console.log(`   路径: ${targetFile}`);
  return targetFile;
}

// ─── 入口 ────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args.length < 1 || !args.some(a => !a.startsWith('--'))) {
  console.error('用法: node download.js <蓝奏云链接> [输出文件路径] [密码] [--select 目标1,目标2]');
  console.error('  密码可选，若链接需要密码而未提供，会报错提示');
  console.error('  --select: 只下载指定文件（文件名精确匹配或 * 通配），逗号分隔多个');
  console.error('    示例: --select "ima.plus-skill-v1.0.11.zip"  --select "*.pdf,*.zip"');
  console.error('  --list: 只解析并输出文件清单（JSON，前缀 __LANZOU_LIST__），不下载');
  console.error('  --insecure: 关闭 HTTPS 证书校验（仅镜像域证书异常时临时使用，有中间人风险）');
  process.exit(1);
}

let inputUrl = null, outputFile = null, password = null, selectTargets = null;
const positional = [];
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--select') {
    selectTargets = (args[++i] || '').split(',').map(s => s.trim()).filter(Boolean);
  } else if (a === '--list') {
    LIST_ONLY = true;
  } else if (a === '--insecure') {
    // 已由顶部 INSECURE_TLS 处理，这里仅消费参数，避免被当作位置参数
  } else {
    positional.push(a);
  }
}
inputUrl = positional[0];
outputFile = positional[1] || null;
password = positional[2] || null;

if (selectTargets) console.log(`--select: ${selectTargets.join(', ')}`);

download(inputUrl, outputFile, password, selectTargets).catch(err => {
  console.error(`\n❌ 错误: ${err.message}`);
  process.exit(1);
});
