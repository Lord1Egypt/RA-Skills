---
name: parcel-station-route-qr
description: "Add shelf route guidance and QR code scanning to a parcel station chatbot."
---

# Parcel Station: Route Guidance + QR Scanner

为快递驿站聊天系统添加**货架指路引擎**和**二维码扫码功能**。

## 前置条件

- Node.js 18+
- 已有 Express + JSON DB 的驿站聊天系统（如 `parcel-station-chat` skill）
- AI API Key（GPT-5.5 或兼容 OpenAI API）

## 关键文件

| 文件 | 说明 |
|------|------|
| `server.js` | Express 服务 + AI 对话 + 路线引擎 |
| `public/index.html` | 前端界面（菜鸟蓝白风格） |
| `public/libs/jsqr.min.js` | QR 解码库 |
| `public/gen-cert.js` | HTTPS 自签名证书生成 |
| `public/cert.pem` / `key.pem` | 生成的证书文件 |

## 1. 货架路线引擎

### 数据结构

```javascript
const SHELF_GUIDES = {
  1: '进门右手边，架子上有蓝色指示牌「自助取件1号货架」',
  2: '进门右手边，走到中间',
  3: '进门右手边，走到中间再往前一点',
  4: '进门往右走，左手边，出库仪旁边',
  5: '进门往右走，左手边，走到中间',
  6: '进门往右走，左手边，走到中间再往前一点',
  7: '一进门右手边门旁边',
  8: '进门往右走，一直走到底最里面',
  9: '进门往左走，出库仪后面',
  10: '进门往左走，正对着你',
  11: '进门往左走，冰箱旁边',
};
```

### 路线生成函数

```javascript
function getRouteGuide(shelfNumber, shelfLevel) {
  var guide = SHELF_GUIDES[shelfNumber] || '请查看第' + shelfNumber + '号货架';
  guide += '，从上往下数第' + shelfLevel + '排';
  // 特殊货架备注
  if (shelfNumber === 5) guide += '（注意：5号货架只有3排）';
  if (shelfNumber === 6) guide += '（6号货架有5排）';
  if (shelfNumber === 7 && shelfLevel === 4) guide += '。\uD83D\uDCE6 如果架子上没有，朝消防栓旁边的墙角看——7-4的大件包裹有时会放在那里喔！';
  if (shelfNumber === 9) guide += '（9号货架有5列）';
  if (shelfNumber === 11) guide += '（11号货架只有1排，都是大件，一眼就能看到！）';
  return guide;
}
```

### 系统提示词（SYSTEM_PROMPT）更新

在 SYSTEM_PROMPT 中加入完整货架信息，让 AI 能够基于数据指路。示例见 `server.js` 第 42-73 行。

## 2. QR 扫码功能

### 依赖安装

```bash
npm install selfsigned
```

### jsQR 库

从 CDN 下载到本地，避免国内访问问题：

```bash
# URL:
# https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js
# → 下载到 public/libs/jsqr.min.js
```

### 前端扫码弹窗

见 `public/index.html` 中：
- `.scanner-modal` — 全屏扫码界面
- `openScanner()` — 开启摄像头实时扫码
- `scanFromFile()` — 拍照/文件二维码解码（HTTP 降级方案）
- `scanLoop()` — 逐帧解码循环

### 工作流程

```
用户点击扫码图标 → openScanner()
  ├─ 成功 getUserMedia → 实时视频流 + scanLoop 逐帧解码 → 自动发送
  └─ 失败（HTTP环境） → 显示"拍照识别二维码"按钮 → capture相机 → jsQR解码
       ├─ 识别成功 → 关闭弹窗 → 自动发送
       └─ 识别失败 → 留在弹窗 → "请重新拍照"
```

## 3. HTTPS 配置（可选，用于移动端实时扫码）

### 生成自签名证书

```javascript
// gen-cert.js
const selfsigned = require('selfsigned');  // npm install selfsigned

const attrs = [
  { name: 'commonName', value: 'parcel-station.local' },
  { name: 'organizationName', value: 'Station Name' }
];
const opts = {
  days: 365, keySize: 2048,
  extensions: [
    { name: 'subjectAltName', altNames: [
      { type: 2, value: 'localhost' },
      { type: 7, ip: '127.0.0.1' },
      { type: 7, ip: '192.168.XXX.XXX' }  // 替换为实际局域网IP
    ]}
  ]
};
const pems = await selfsigned.generate(attrs, opts);
fs.writeFileSync('cert.pem', pems.cert);
fs.writeFileSync('key.pem', pems.private);
```

### 双端口服务（HTTP + HTTPS）

```javascript
const http = require('http');
const https = require('https');
const fs = require('fs');
const app = express();

// HTTP 日常测试
http.createServer(app).listen(3000, () => { ... });

// HTTPS 扫码用
const opts = { cert: fs.readFileSync('cert.pem'), key: fs.readFileSync('key.pem') };
https.createServer(opts, app).listen(3443, () => { ... });
```

⚠️ 手机首次打开 HTTPS 会显示"连接不是私密"警告，需点击「高级→继续访问」。

## 4. UI 主题（菜鸟蓝白风）

| 元素 | 颜色 |
|------|------|
| 主色 | `#1a73e8` |
| 深色 | `#0d5bbd` / `#0948a0` |
| 底色 | `#e8f4fd → #f0f6fa` 渐变 |
| 用户气泡 | 蓝渐变 `#1a73e8 → #0d5bbd` |
| 机器人气泡 | 白底 + 蓝色边框 |
| 按钮 | 蓝色药丸形圆角 24px |

## 5. 注意事项 / 踩坑记录

### 浏览器安全限制
- `getUserMedia` 需要 HTTPS 或 localhost
- 通过 IP 地址访问（如 192.168.x.x）必须用 HTTPS
- 自签名证书首次需要跳过警告

### PowerShell 文件写入
- `Set-Content` 会吃掉反引号 `（PowerShell 转义符）
- `Out-File` / `>` 会用 GBK 重编码中文 → 乱码
- **解决方案**：用 OpenClaw `write` 工具或 Node.js `fs.writeFileSync()`

### jsQR 兼容性
- 128KB 大小，纯 JS，支持主流浏览器
- 从 Canvas RasterData 解码
- 支持文件图片和实时视频帧

### 多个文件输入不要重ID
- 扫码弹窗内和聊天输入栏的文件 input 用不同的 id
- `scannerFileInput`（扫码弹窗）和 `imgInput`（聊天栏）
