// ============================================================
// 网易云音乐 · 动态头像一键脚本（浏览器 Console 版）
//
// 用法:
//   1. 浏览器登录 https://music.163.com
//   2. 打开任意 music.163.com 页面（顶层页面，不要停在别的站点）
//   3. F12 → Console → 整段粘贴 → 回车 → 选择动图
//
// 原理:
//   网页版「更换头像」上传完会调 /upload/img/op 做服务端裁切，
//   该接口会把动图重编码成静态 JPEG。本脚本跳过这一步，
//   直接把动图原始字节传上 NOS，再用原始 docId 设头像。
//
// 注意: 只用于自己的账号。
// ============================================================
(async () => {
  const RISK_KEY = 'bd5d2f973ef74cd2a61325a412ae54d9'; // WM.getToken 的 key
  const log = (...a) => console.log('%c[动态头像]', 'color:#c20c0c;font-weight:bold', ...a);

  // 取能发请求的 window：音乐站是 iframe 套壳，优先用 iframe 内部
  const f = document.querySelector('#g_iframe');
  const W = (f && f.contentWindow) || window;

  const pickFile = () => new Promise((resolve) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/webp,image/gif,image/*';
    input.style.cssText = 'position:fixed;left:20px;top:20px;z-index:99999';
    input.onchange = () => resolve(input.files[0]);
    document.body.appendChild(input);
    input.click();
  });

  const file = await pickFile();
  if (!file) return log('没有选文件，已退出');
  log('选中', file.name, (file.size / 1024).toFixed(1) + ' KB', file.type || '(无 type)');
  if (file.size > 5 * 1024 * 1024) return log('❌ 超过 5MB 硬限制，先压缩');

  // ---- 1. 申请 NOS 上传凭证 ----
  const q = new URLSearchParams({
    filename: 'a.jpg', ext: 'jpg', type: 'image', bucket: 'yyimgs',
    local: 'false', nos_product: '0',
    return_body: JSON.stringify({ code: 200, size: '$(ObjectSize)' })
  });
  const alloc = await (await W.fetch('/api/nos/token/alloc', {
    method: 'POST', credentials: 'include',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: q.toString()
  })).json();
  if (alloc.code !== 200) return log('❌ 取上传凭证失败', alloc);

  const { bucket, objectKey, docId, token } = alloc.result;
  log('凭证 OK  docId=' + docId);

  // ---- 2. 直传 NOS（关键：不调 /upload/img/op） ----
  let host = 'https://nosup-hz1.127.net';
  try {
    const lbs = await (await W.fetch('https://wanproxy.127.net/lbs?version=1.0&bucketname=' + bucket)).json();
    if (lbs.upload && lbs.upload[0]) host = lbs.upload[0];
  } catch (e) { /* 用默认节点 */ }
  if (!/^https?:/.test(host)) host = 'https://' + host;

  const putUrl = host + '/' + bucket + '/' + objectKey + '?offset=0&complete=true&version=1.0';
  const up = await W.fetch(putUrl, {
    method: 'POST',
    headers: { 'x-nos-token': token, 'Content-Type': file.type || 'image/webp' },
    body: file
  });
  const upText = await up.text();
  log('NOS 上传', up.status, upText.slice(0, 200));
  if (up.status !== 200) return log('❌ 上传失败');

  // ---- 3. 用原始 docId 设为头像 ----
  const getToken = (k) => new Promise((r) => {
    const wm = W.WM || window.WM;
    if (!wm || !wm.getToken) return r('');
    wm.getToken(k, r);
  });
  const checkToken = await getToken(RISK_KEY);
  if (!checkToken) return log('❌ 拿不到 checkToken，风控 key 可能轮换了，去 grep pt_profile_update.js 里的 WM.getToken("');

  const body = new URLSearchParams({ imgid: docId, checkToken });
  const res = await (await W.fetch('/api/user/avatar/upload/v1', {
    method: 'POST', credentials: 'include',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  })).json();
  log('设头像结果', res);

  if (res.code !== 200) return log('❌ 设头像失败');

  // ---- 4. 验证：抓字节确认还是动图 ----
  const url = res.url;
  log('✅ 头像已提交: ' + url);
  const buf = await (await W.fetch(url, { cache: 'no-store' })).arrayBuffer();
  const u = new Uint8Array(buf);
  const magic = String.fromCharCode(u[0], u[1], u[2], u[3]);
  let frames = 0;
  if (magic === 'RIFF' && String.fromCharCode(u[8], u[9], u[10], u[11]) === 'WEBP') {
    const dv = new DataView(buf);
    let i = 12;
    while (i + 8 <= buf.byteLength) {
      const id = String.fromCharCode(u[i], u[i + 1], u[i + 2], u[i + 3]);
      const sz = dv.getUint32(i + 4, true);
      if (id === 'ANMF') frames++;
      i += 8 + sz + (sz & 1);
    }
  }
  log('回读魔数=' + magic + '  动画帧数=' + frames + '  体积=' + buf.byteLength);
  if (frames > 1) {
    log('🎉 动图保住了。刷新个人主页 / 重开客户端查看（URL 后缀是 .jpg 但内容是 WebP，正常）');
  } else {
    log('⚠️ 回读不是动画（帧数=' + frames + '），检查源文件是否真的多帧，或是否误走了 UI 上传');
  }
})();
