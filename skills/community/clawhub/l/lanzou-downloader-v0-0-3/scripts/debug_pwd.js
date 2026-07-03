/**
 * 临时调试脚本：dump 密码页 HTML
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

  console.log('Step 1: 访问分享页...');
  let resp = await request('GET', url);
  let cookies = resp.cookies;
  let body = resp.body;

  console.log('Step 2: 反爬...');
  const arg1Match = body.match(/var arg1='([^']+)'/);
  const scriptMatch = body.match(/<script>([\s\S]*?)<\/script>/);

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
    }
  }

  resp = await request('GET', url, { cookieJar: cookies });
  body = resp.body;

  console.log(`  状态: ${resp.status}, 大小: ${body.length}`);
  fs.writeFileSync('/sandbox/workspace/pwd_page_debug.html', body);
  console.log('HTML 已保存到 /sandbox/workspace/pwd_page_debug.html');
}

main().catch(e => console.error(e.message));
