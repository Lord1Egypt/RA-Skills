/**
 * 蓝奏云下载器 - 纯 Node.js 实现，零外部依赖
 * 用法: node download.js <蓝奏云分享链接> [输出文件路径] [密码]
 *   密码可选，若不提供且链接需要密码，会报错提示
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const vm = require('vm');
const url = require('url');
const path = require('path');
const zlib = require('zlib');

// ─── 工具函数 ───────────────────────────────────────────────

/** 去除 JavaScript 注释（块注释和行注释） */
function stripJsComments(code) {
  return code
    .replace(/\/\*[\s\S]*?\*\//g, '')  // 去除 /* ... */
    .replace(/\/\/.*$/gm, '');          // 去除 //
}

function request(method, targetUrl, opts = {}) {
  const { cookieJar = {}, body, redirectCount = 0, encoding = null } = opts;
  if (redirectCount > 8) return Promise.reject(new Error('重定向次数过多'));

  return new Promise((resolve, reject) => {
    const u = new URL(targetUrl);
    const mod = u.protocol === 'https:' ? https : http;
    const headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
      rejectUnauthorized: false,
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

function streamDownload(targetUrl, filePath, opts = {}) {
  return new Promise(async (resolve, reject) => {
    try {
      let currentUrl = targetUrl;
      const baseHeaders = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': opts.referer || '',
      };

      for (let i = 0; i < 5; i++) {
        const u = new URL(currentUrl);
        const hdrs = { ...baseHeaders };

        const resp = await new Promise((res, rej) => {
          const mod = u.protocol === 'https:' ? https : http;
          const ro = {
            hostname: u.hostname,
            port: u.port || (u.protocol === 'https:' ? 443 : 80),
            path: u.pathname + u.search,
            method: 'GET',
            headers: hdrs,
            rejectUnauthorized: false,
          };
          const r = mod.request(ro, (rs) => res(rs));
          r.on('error', rej);
          r.setTimeout(15000, () => { r.destroy(); rej(new Error('超时')); });
          r.end();
        });

        if ([301, 302, 303, 307, 308].includes(resp.statusCode) && resp.headers.location) {
          currentUrl = new URL(resp.headers.location, currentUrl).href;
          continue;
        }

        if (resp.statusCode >= 400) {
          reject(new Error(`下载失败: HTTP ${resp.statusCode}`));
          return;
        }

        const file = fs.createWriteStream(filePath);
        resp.pipe(file);
        file.on('finish', () => resolve(file.bytesWritten));
        file.on('error', reject);
        return;
      }
      reject(new Error('重定向次数过多'));
    } catch (e) {
      reject(e);
    }
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
  const fidMatch = body.match(/ajaxm\.php\?file=(\d+)/);
  if (!fidMatch) return { needsPwd: true, fullDownUrl: null, fileName: null, error: '无法提取文件 ID' };
  const fid = fidMatch[1];
  console.log(`  fid: ${fid}`);

  // 提取 kdns
  const kdnsMatch = body.match(/var\s+kdns\s*=\s*(\d+)/);
  const kdns = kdnsMatch ? kdnsMatch[1] : '1';
  console.log(`  kdns: ${kdns}`);

  // 提取 sign（去除 JS 注释后匹配）
  const downPStart = body.indexOf('function down_p()');
  const downPEnd = body.indexOf('</script>', downPStart);
  let downPBody = body.substring(downPStart, downPEnd);
  downPBody = stripJsComments(downPBody);

  const signMatch = downPBody.match(/sign':'([^']+)'/);
  if (!signMatch) return { needsPwd: true, fullDownUrl: null, fileName: null, error: '无法提取 sign 参数' };
  const sign = signMatch[1];
  console.log(`  sign: ${sign.substring(0, 16)}...`);

  // POST 密码
  const pwdUrl = new URL(`/ajaxm.php?file=${fid}`, lanzouUrl).href;
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

  try {
    const json = JSON.parse(pwdResp.body);
    console.log(`  服务器响应: zt=${json.zt}`);

    if (json.zt !== 1) {
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

// ─── 主流程 ──────────────────────────────────────────────────

async function download(lanzouUrl, outputPath = null, password = null) {
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

  // Step 3: 密码处理（如果需要）
  let fullDownUrl = null;
  let fileName = null;

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

    // Step 4: 请求 iframe 获取 AJAX 参数
    console.log('\n[4/5] 请求 AJAX 参数...');
    const iframeUrl = new URL(iframeSrc, resp.url).href;
    const iframeResp = await request('GET', iframeUrl, {
      cookieJar: cookies,
      headers: { 'Referer': resp.url },
    });

    const iframeBody = iframeResp.body;
    const ajaxMatch = iframeBody.match(/var\s+ajaxdata\s*=\s*'([^']*)'/);
    const signMatch = iframeBody.match(/var\s+wp_sign\s*=\s*'([^']*)'/);
    const kdnsMatch = iframeBody.match(/var\s+kdns\s*=\s*(\d+)/);

    if (!ajaxMatch || !signMatch) throw new Error('无法提取 AJAX 参数');
    const ajaxdata = ajaxMatch[1];
    const wpSign = signMatch[1];
    const kdns = kdnsMatch ? parseInt(kdnsMatch[1]) : 1;
    console.log(`  ajaxdata: ${ajaxdata}, kdns: ${kdns}`);

    // POST 获取真实下载地址
    const ajaxUrl = new URL(`/ajaxm.php?file=${fid}`, resp.url).href;
    const postData = new URLSearchParams({
      action: 'downprocess',
      websignkey: ajaxdata,
      signs: ajaxdata,
      sign: wpSign,
      websign: '',
      kd: String(kdns),
      ves: '1',
    }).toString();

    const ajaxResp = await request('POST', ajaxUrl, {
      cookieJar: cookies,
      headers: {
        'Referer': iframeUrl,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: postData,
    });

    let ajaxBody = ajaxResp.body;
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

  // Step 5: 流式下载
  const targetFile = outputPath || path.join(process.cwd(), fileName || 'download.zip');
  const dir = path.dirname(targetFile);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  console.log(`\n[5/5] 下载文件 → ${targetFile}`);
  const size = await streamDownload(fullDownUrl, targetFile, {
    referer: lanzouUrl,
  });

  const sizeMB = (size / (1024 * 1024)).toFixed(1);
  console.log(`\n✅ 下载完成: ${path.basename(targetFile)} (${sizeMB} MB)`);
  console.log(`   路径: ${targetFile}`);
  return targetFile;
}

// ─── 入口 ────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('用法: node download.js <蓝奏云链接> [输出文件路径] [密码]');
  console.error('  密码可选，若链接需要密码而未提供，会报错提示');
  process.exit(1);
}

const inputUrl = args[0];
const outputFile = args[1] || null;
const password = args[2] || null;

download(inputUrl, outputFile, password).catch(err => {
  console.error(`\n❌ 错误: ${err.message}`);
  process.exit(1);
});
