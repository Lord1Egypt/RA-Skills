# 渲染 MP4

环境：Node ≥18 + ffmpeg（PATH 里可调用）。缺 playwright → `npm i -g playwright && playwright install chromium`；缺 ffmpeg → winget install Gyan.FFmpeg 或下载 gyan.dev full build。

## 步骤

1. 在 index.html 同目录建 `render.js`：

```js
// 用法: node render.js   （需先 npx playwright install chromium）
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + require('path').resolve('index.html'));
  // 若动画不自动播、由时钟驱动，可注入 seek 函数；推荐源码内提供 window.seek(t)
  await page.evaluate(() => window.seek && window.seek(0));
  await page.screenshot({ path: 'frames/f0000.png' });
  const FPS = 30, DUR = 8;
  for (let i = 1; i <= FPS * DUR; i++) {
    await page.evaluate(t => window.seek(t), i / FPS);
    // 两位序号不够 240 帧用，这里固定四位
    await page.screenshot({ path: `frames/f${String(i).padStart(4, '0')}.png` });
  }
  await browser.close();
})();
```

> 关键点：源码里实现 `window.seek(tSeconds)`，让整个画面状态由参数 t 决定（纯函数式），截图就能逐帧确定。这比靠 requestAnimationFrame 抓帧稳定得多。

2. 建帧目录并逐帧截图：`mkdir frames && node render.js`
3. 合成 MP4：

```
ffmpeg -y -framerate 30 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart output.mp4
```

4. 渲染完删掉 frames/ 中间产物（用户确认后）。

## 兜底

- 装不了 playwright：让动画在浏览器全屏播放，用 Win+G（Xbox Game Bar）或 OBS 录屏 8 秒。
- 动画用了随机数：随机种子固定（seeded random），保证 seek 可复现。
