---
name: html2screenshot
description: HTML 网页长截图技能。将任意 HTML（文件路径、URL 或 HTML 字符串）转换为完整长图（PNG），不失真不变形。触发词：html截图、网页截图、长截图、完整页面截图、把网页转成图片。
author: keling
version: 1.0.0
triggers:
  - html截图
  - 网页截图
  - 长截图
  - 完整页面截图
  - 把网页转成图片
  - 截取整个页面
---

# HTML 长截图技能

## 概述

将任意 HTML 网页（完整文档或片段）转换为完整长图（PNG），不失真、不变形。

**核心能力**：
- 📐 自适应页面尺寸，自动捕获整个页面
- 📱 支持 mobile / desktop 多种 viewport
- 🖼️ PNG 高清输出，2x deviceScaleFactor
- 🌐 内置 HTTP 服务，浏览器直接访问预览+下载

---

## 使用方式

### HTTP 服务（推荐）

**启动服务**（后台常驻）：
```bash
NODE_PATH=/Users/zhangyao/.local/lib/node_modules \
node ~/.openclaw/workspace/skills/html2screenshot/server.cjs &
```

**访问**：http://192.168.40.121:3134

- 左侧粘贴 HTML，可调 viewport 宽/高/缩放
- 点击「截图」生成 PNG，右侧预览
- 点击预览图即可下载原图
- `Ctrl+Enter` 快捷截图

**检查服务状态**：
```bash
lsof -i :3134 | grep LISTEN
```

---

### 文件路径截图

用户提供 HTML 文件路径时，用 Puppeteer 直接截图：

```bash
NODE_PATH=/Users/zhangyao/.local/lib/node_modules node - <<'EOF'
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const html = fs.readFileSync('/Users/zhangyao/Downloads/xxx.html', 'utf8');
  const OUTPUT = '/tmp/screenshot.png';

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  await page.setContent(html, { waitUntil: 'load' });

  const dims = await page.evaluate(() => ({
    width: Math.ceil(document.body.scrollWidth),
    height: Math.ceil(document.body.scrollHeight),
  }));

  await page.setViewport({ width: dims.width, height: dims.height, deviceScaleFactor: 2 });
  await page.evaluate(() => window.stop());

  await page.screenshot({ type: 'png', fullPage: true }).then(s => {
    fs.writeFileSync(OUTPUT, s);
    console.log('✅ Done: ' + OUTPUT + ' ' + (s.length/1024).toFixed(0) + 'KB');
  });

  await browser.close();
})();
EOF
```

---

## API：POST /capture

**Request**：
```json
{
  "html": "<!DOCTYPE html>...",
  "viewport": { "width": 390, "height": 844 },
  "deviceScaleFactor": 2
}
```

**Response**：PNG 二进制

---

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `width` | 1280 | viewport 宽度（px） |
| `height` | 800 | viewport 高度（px） |
| `deviceScaleFactor` | 2 | 缩放倍数（1=1x, 2=2x高清） |
| `fullPage` | true | 截取整个可滚动区域 |

---

## 依赖

- **Puppeteer**：`/Users/zhangyao/.local/lib/node_modules/puppeteer`
- **Chrome**：系统已装 `/Applications/Google Chrome.app`
- **Node**：v25.8.1

---

## 注意事项

- Chrome 路径写死在脚本里：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- `networkidle0` 超时问题：改用 `waitUntil: 'load'`
- 大页面截图较慢（数秒），等待时显示 "⏳ 渲染中"