/**
 * 测试密码提交
 */
const https = require('https');
const http = require('http');
const fs = require('fs');
const vm = require('vm');
const zlib = require('zlib');

function request(method, targetUrl, opts = {}) {
  const { cookieJar = {}, body, redirectCount = 0 } = opts;
  if (redirectCount > 8) return Promise.reject(new Error('重定向次数过多'));

  return new Promise((resolve, reject) => {
    const u = new URL(targetUrl);
    const mod = u.protocol === 'https:' ? https : http;
    const headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    };

    const mergedCookies = { ...cookieJar };
    const cookieStr = Object.entries(mergedCookies).map(([k,v]) => `${k}=${v}`).join('; ');
    if (cookieStr) headers['Cookie'] = cookieStr;

    if (body) headers['Content-Length'] = Buffer.byteLength(body);

    const reqOpts = {
      hostname: u.hostname,
      port: u.port || (u.protocol === 'https:' ? 443 : 80),
      path: u.pathname + u.search,
      method,
      headers,
      rejectUnauthorized: false,
    };

    const req = mod.request(reqOpts, (res) => {
      const setCookies = res.headers['set-cookie'];
      if (setCookies) {
        setCookies.forEach(c => {
          const semi = c.indexOf(';');
          const pair = semi > 0 ? c.substring(0, semi) : c;
          const eq = pair.indexOf('=');
          if (eq > 0) mergedCookies[pair.substring(0, eq).trim()] = pair.substring(eq + 1).trim();
        });
      }

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
        resolve({ status: res.statusCode, headers: res.headers, body: text, raw, cookies: mergedCookies, url: targetUrl });
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('请求超时')); });
    if (body) req.write(body);
    req.end();
  });
}

async function main() {
  const url = 'https://wwapw.lanzouu.com/iW7UV3td6cqf';
  const password = '1234';

  // Step 1+2: 反爬
  console.log('反爬...');
  let resp = await request('GET', url);
  let cookies = resp.cookies;
  let body = resp.body;

  const arg1Match = body.match(/var arg1='([^']+)'/);
  const scriptMatch = body.match(/<script>([\s\S]*?)<\/script>/);
  const fakeDoc = { cookie: '', location: { reload: () => {} } };
  const ctx = vm.createContext({
    document: fakeDoc, Date: Date,
    console: { log: () => {}, error: () => {}, warn: () => {} },
  });
  vm.runInContext(scriptMatch[1], ctx, { timeout: 5000 });
  const parts = fakeDoc.cookie.split(';')[0].split('=');
  if (parts.length >= 2) cookies[parts[0].trim()] = parts.slice(1).join('=').trim();

  resp = await request('GET', url, { cookieJar: cookies });
  body = resp.body;

  // 检测密码
  const hasPwd = body.includes('passwddiv');
  console.log(`需要密码: ${hasPwd}`);

  if (hasPwd) {
    // 提取 fid
    const fidMatch = body.match(/ajaxm\.php\?file=(\d+)/);
    const fid = fidMatch ? fidMatch[1] : null;
    console.log(`fid: ${fid}`);

    // 提取 kdns
    const kdnsMatch = body.match(/var\s+kdns\s*=\s*(\d+)/);
    const kdns = kdnsMatch ? kdnsMatch[1] : '1';
    console.log(`kdns: ${kdns}`);

    // 提取 sign - 先去除 JS 注释，再取最后一个 sign
    const downPStart = body.indexOf('function down_p()');
    const downPEnd = body.indexOf('</script>', downPStart);
    let downPBody = body.substring(downPStart, downPEnd);
    console.log('=== 原始 down_p 函数 ===');
    console.log(downPBody);
    // 去除 /* ... */ 块注释
    downPBody = downPBody.replace(/\/\*[\s\S]*?\*\//g, '');
    // 去除 // 行注释
    downPBody = downPBody.replace(/\/\/.*$/gm, '');
    console.log('=== 去除注释后 ===');
    console.log(downPBody);
    const signMatches = [...downPBody.matchAll(/sign':'([^']+)'/g)];
    console.log('所有 sign 匹配:', signMatches.map(m => m[1].substring(0, 20) + '...'));
    const sign = signMatches.length > 0 ? signMatches[signMatches.length - 1][1] : null;
    console.log(`选用 sign: ${sign?.substring(0, 30)}... (${sign?.length} 字符)`);

    // POST 密码
    const pwdUrl = new URL(`/ajaxm.php?file=${fid}`, url).href;
    console.log(`POST: ${pwdUrl}`);

    const postData = new URLSearchParams({
      action: 'downprocess',
      sign: sign,
      kd: kdns,
      p: password,
    }).toString();

    const pwdResp = await request('POST', pwdUrl, {
      cookieJar: cookies,
      headers: {
        'Referer': url,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: postData,
    });

    console.log(`密码响应状态: ${pwdResp.status}`);
    console.log(`密码响应头: ${JSON.stringify(pwdResp.headers)}`);
    console.log(`密码响应体: "${pwdResp.body.substring(0, 500)}"`);
    console.log(`密码响应 raw 长度: ${pwdResp.raw.length}`);

    try {
      const json = JSON.parse(pwdResp.body);
      console.log(`zt: ${json.zt}, dom: ${json.dom}, url: ${json.url}, inf: ${json.inf}`);
    } catch (e) {
      console.log(`JSON 解析失败: ${e.message}`);
      console.log(`raw 前100字节 hex: ${pwdResp.raw.slice(0, 100).toString('hex')}`);
    }
  }
}

main().catch(e => console.error(e.message));
