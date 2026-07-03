/**
 * 使用原生 Node.js http 模块直接 POST 密码（更底层调试）
 */
const https = require('https');
const http = require('http');
const zlib = require('zlib');
const vm = require('vm');

function rawRequest(method, targetUrl, opts = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(targetUrl);
    const mod = u.protocol === 'https:' ? https : http;
    const reqOpts = {
      hostname: u.hostname,
      port: u.port || (u.protocol === 'https:' ? 443 : 80),
      path: u.pathname + u.search,
      method,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        ...opts.headers,
      },
      rejectUnauthorized: false,
    };
    
    let cookieJar = opts.cookieJar || {};
    if (Object.keys(cookieJar).length > 0) {
      reqOpts.headers['Cookie'] = Object.entries(cookieJar).map(([k,v]) => `${k}=${v}`).join('; ');
    }
    
    const req = mod.request(reqOpts, (res) => {
      // Parse set-cookie
      const setCookies = res.headers['set-cookie'];
      if (setCookies) {
        setCookies.forEach(c => {
          const semi = c.indexOf(';');
          const pair = semi > 0 ? c.substring(0, semi) : c;
          const eq = pair.indexOf('=');
          if (eq > 0) cookieJar[pair.substring(0, eq).trim()] = pair.substring(eq + 1).trim();
        });
      }
      
      // Follow redirect
      if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location) {
        const loc = new URL(res.headers.location, targetUrl).href;
        console.log(`  重定向: ${loc}`);
        return resolve(rawRequest('GET', loc, { ...opts, cookieJar }));
      }
      
      const chunks = [];
      res.on('data', c => {
        console.log(`  收到数据块: ${c.length} 字节`);
        chunks.push(c);
      });
      res.on('end', () => {
        let raw = Buffer.concat(chunks);
        console.log(`  总数据: ${raw.length} 字节`);
        const ce = res.headers['content-encoding'];
        if (ce === 'gzip') raw = zlib.gunzipSync(raw);
        else if (ce === 'deflate') raw = zlib.inflateSync(raw);
        let text = raw.toString('utf8');
        resolve({ status: res.statusCode, headers: res.headers, body: text, raw, cookies: cookieJar, url: targetUrl });
      });
      res.on('error', reject);
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('timeout')); });
    if (opts.body) req.write(opts.body);
    req.end();
  });
}

async function main() {
  const url = 'https://wwapw.lanzouu.com/iW7UV3td6cqf';
  const password = '1234';

  console.log('===== Step 1: GET 分享页 =====');
  let resp = await rawRequest('GET', url);
  let cookies = resp.cookies;
  let body = resp.body;
  console.log(`状态: ${resp.status}, 大小: ${body.length}`);

  // 反爬
  console.log('\n===== Step 2: 反爬 =====');
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
  console.log(`acw_sc__v2: ${cookies['acw_sc__v2']?.substring(0, 12)}...`);

  resp = await rawRequest('GET', url, { cookieJar: cookies });
  cookies = resp.cookies;
  body = resp.body;

  // 提取参数
  const fidMatch = body.match(/ajaxm\.php\?file=(\d+)/);
  const fid = fidMatch[1];
  const kdnsMatch = body.match(/var\s+kdns\s*=\s*(\d+)/);
  const kdns = kdnsMatch ? kdnsMatch[1] : '1';
  
  const downPStart = body.indexOf('function down_p()');
  const downPEnd = body.indexOf('</script>', downPStart);
  let downPBody = body.substring(downPStart, downPEnd);
  downPBody = downPBody.replace(/\/\*[\s\S]*?\*\//g, '');
  downPBody = downPBody.replace(/\/\/.*$/gm, '');
  const signMatch = downPBody.match(/sign':'([^']+)'/);
  const sign = signMatch[1];
  
  console.log(`fid: ${fid}, kdns: ${kdns}, sign: ${sign.substring(0, 20)}...`);

  // POST 密码
  console.log('\n===== Step 3: POST 密码 =====');
  const postData = `action=downprocess&sign=${encodeURIComponent(sign)}&kd=${kdns}&p=${password}`;
  console.log(`POST 数据: ${postData.substring(0, 80)}...`);

  const pwdUrl = new URL(`/ajaxm.php?file=${fid}`, url).href;
  const pwdResp = await rawRequest('POST', pwdUrl, {
    cookieJar: cookies,
    headers: {
      'Referer': url,
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Requested-With': 'XMLHttpRequest',
      'Origin': new URL(url).origin,
    },
    body: postData,
  });

  console.log(`状态: ${pwdResp.status}`);
  console.log(`响应头 content-type: ${pwdResp.headers['content-type']}`);
  console.log(`响应体: "${pwdResp.body.substring(0, 200)}"`);
  console.log(`raw 长度: ${pwdResp.raw.length}`);
  
  if (pwdResp.body) {
    try {
      const json = JSON.parse(pwdResp.body);
      console.log(`✅ JSON 解析成功: zt=${json.zt}, dom=${json.dom}, url=${json.url}, inf=${json.inf}`);
    } catch (e) {
      console.log(`JSON 解析失败: ${e.message}`);
    }
  }
}

main().catch(e => console.error('错误:', e.message));
