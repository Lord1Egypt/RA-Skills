# 微贴图设计规范

一键把微信公众号文章转成微贴图（微信公众号贴图） + 发布文案。HTML 模板 + 视觉组件部分

---

## 环境变量

本技能所使用到的环境变量在 `local/.env` 中配置。

支持的环境变量如下：

- `OUTPUT_DIR`：输出目录，用于放置收集到的素材、生成的文章、排版预览、封面图、微贴图轮播图等文件。
- `ARCHIVE_DIR`：存档目录，用于归档历史文档文件。
- `BRAND_NAME`：品牌名称，用于在生成的文章中显示品牌名称。
- `BRAND_LOGO_DARK`：品牌logo（深色），用于在生成的文章中显示品牌logo。
- `BRAND_LOGO_LIGHT`：品牌logo（浅色），用于在生成的文章中显示品牌logo。
- `WECHAT_ID`：微信公众号ID，用于发布文章。
- `WECHAT_SLOGON`：微信公众号标语，用于在文章中显示。
- `WECHAT_APPID`：微信公众号AppID，用于发布文章时的认证。
- `WECHAT_APPSECRET`：微信公众号AppSecret，用于发布文章时的认证。
- `MD_FORMATTER_DIR`：Markdown格式化工具目录，用于格式化Markdown文章。

---

## 尺寸

- 显示尺寸：`720 x 540 px`
- 导出尺寸：`1440 x 1080 px`（2x 缩放）
- 比例：4:3（公众号配图标准）

---

## 卡片设计原则

- 每张卡只讲 **1 个重点**
- 信息密度适中，留白充足
- 暗底页和浅底页 **交替出现**
- 文字要大、要粗、要少
- 数据可视化优先（数字大、表格清晰、SVG 图示）

---

## 页面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>公众号贴图图片 - [主题]</title>
<style>
  /* === 基础 === */
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #111;
    display: flex; flex-direction: column; align-items: center;
    padding: 30px 20px 80px;
    padding-top: 70px; /* 为工具栏留空 */
    font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  }

  .brand { position: absolute; top: 20px; left: 20px; display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; letter-spacing: 1px; }
  .brand svg { width: 20px; height: 20px; }
  .brand.dark { color: rgba(255,255,255,0.5); }
  .brand.light { color: rgba(26,51,40,0.4); }

  /* === 卡片 === */
  .slide {
    width: 540px; height: 720px;
    position: relative; overflow: hidden;
    border-radius: 8px; margin-bottom: 40px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
  }

  /* === 暗底 === */
  .bg-dark {
    position: absolute; inset: 0; background: #1A3328;
  }
  .bg-dark::after {
    content: ''; position: absolute; inset: 0;
    background:
      radial-gradient(circle at 80% 15%, rgba(255,255,255,0.03) 0%, transparent 50%),
      radial-gradient(circle at 20% 85%, rgba(0,0,0,0.08) 0%, transparent 50%);
  }

  /* === 浅底 === */
  .bg-light { position: absolute; inset: 0; background: #F2EDE3; }

  /* === 内容层 === */
  .content {
    position: absolute; inset: 0; padding: 50px 40px;
    display: flex; flex-direction: column; z-index: 2;
  }

  /* === 下载工具栏 === */
  .toolbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: rgba(17,17,17,0.95); backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding: 12px 20px; display: flex; align-items: center;
    justify-content: center; gap: 12px;
  }
  .toolbar .btn {
    background: #1A3328; color: #F2EDE3; border: none;
    padding: 10px 24px; border-radius: 8px; font-size: 14px;
    font-weight: 600; cursor: pointer;
  }
  .toolbar .btn.accent { background: #C44536; }
</style>
</head>
<body>

<!-- 工具栏 -->
<div class="toolbar">
  <button class="btn accent" onclick="downloadAll()">全部下载 (ZIP)</button>
  <button class="btn" onclick="downloadOne()">下载当前</button>
  <span class="progress" id="progress"></span>
</div>

<!-- 第 1 张 · 封面 -->
<div class="slide">...</div>

<!-- 第 2-N 张 · 内容 -->
<div class="slide">...</div>

<!-- CDN + 下载脚本 -->
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>
<script>
const SCALE = 2;
async function renderSlide(s) {
  return html2canvas(s, { scale: SCALE, useCORS: true, backgroundColor: null, width: 540, height: 720, logging: false });
}
function canvasToBlob(c) { return new Promise(r => c.toBlob(r, 'image/png')); }

async function downloadAll() {
  const slides = document.querySelectorAll('.slide');
  const progress = document.getElementById('progress');
  const zip = new JSZip();
  for (let i = 0; i < slides.length; i++) {
    progress.textContent = `渲染第 ${i+1}/${slides.length} 张...`;
    const canvas = await renderSlide(slides[i]);
    zip.file(`公众号贴图-${String(i+1).padStart(2,'0')}.png`, await canvasToBlob(canvas));
  }
  progress.textContent = '打包中...';
  saveAs(await zip.generateAsync({type:'blob'}), '公众号贴图-全部.zip');
  progress.textContent = `${slides.length} 张已下载`;
}

async function downloadOne() {
  const slides = document.querySelectorAll('.slide');
  const vc = window.innerHeight / 2;
  let idx = 0, min = Infinity;
  slides.forEach((s,i) => {
    const d = Math.abs(s.getBoundingClientRect().top + 360 - vc);
    if (d < min) { min = d; idx = i; }
  });
  const canvas = await renderSlide(slides[idx]);
  saveAs(await canvasToBlob(canvas), `公众号贴图-${String(idx+1).padStart(2,'0')}.png`);
}
</script>
</body>
</html>
```

---

### 品牌角标 Brand SVG

每页左上角必须有品牌角标。使用环境变量 `BRAND_LOGO_DARK` 或者 `BRAND_LOGO_LIGHT` 地址的 SVG 图标作为 Brand SVG。

- 暗底版：使用 `BRAND_LOGO_DARK` 作为 Brand SVG。
- 浅底版：使用 `BRAND_LOGO_LIGHT` 作为 Brand SVG。

**注意：品牌角标必须将环境变量的内容原封不动的插入到 HTML 中，不能有任何修改。**

---

## 常用视觉组件

### 信息行（暗底）

```html
<div style="display:flex;align-items:center;padding:12px 16px;border-radius:8px;margin-bottom:8px;background:rgba(255,255,255,0.06);">
  <div style="font-size:13px;font-weight:700;min-width:70px;color:#C44536;">标签</div>
  <div style="font-size:13px;color:rgba(255,255,255,0.7);flex:1;">内容文字</div>
</div>
```

### 信息行（浅底）

同上，`background: rgba(26,51,40,0.06)`，文字色 `color: #555`。

### 步骤序号

```html
<div style="display:flex;gap:14px;margin-bottom:14px;">
  <div style="width:28px;height:28px;border-radius:50%;background:#C44536;color:#F2EDE3;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;">1</div>
  <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.8);">
    <strong style="color:#F2EDE3;">步骤标题</strong><br>步骤说明
  </div>
</div>
```

### 大数字

```html
<div style="display:flex;align-items:baseline;gap:14px;">
  <div style="font-size:64px;font-weight:900;color:#C44536;">22</div>
  <div style="font-size:22px;font-weight:800;color:#F2EDE3;">个 Skill</div>
</div>
```

### 2x2 卡片网格

```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
  <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:14px;">
    <div style="font-size:20px;margin-bottom:6px;">emoji</div>
    <div style="font-size:13px;color:#F2EDE3;font-weight:700;">标题</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.4);line-height:1.6;">说明文字</div>
  </div>
  <!-- 重复 3 个 -->
</div>
```

### 引用块

```html
<div style="border-left:3px solid #C44536;padding:12px 16px;margin:12px 0;background:rgba(255,255,255,0.04);border-radius:0 8px 8px 0;">
  <p style="font-size:14px;color:rgba(255,255,255,0.6);line-height:1.8;font-style:italic;">"引用文字"</p>
</div>
```

### CTA 链接框

```html
<div style="border:1px solid rgba(255,255,255,0.2);border-radius:10px;padding:16px 20px;text-align:center;margin-top:12px;">
  <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-bottom:6px;letter-spacing:2px;">标签</div>
  <div style="font-size:13px;color:#C44536;font-weight:600;word-break:break-all;">链接文字</div>
</div>
```

### 代码预览框（模拟终端）

```html
<div style="background:#1A3328;border-radius:10px;padding:16px;font-family:'SF Mono','Menlo',monospace;">
  <div style="display:flex;gap:6px;margin-bottom:10px;">
    <div style="width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.15);"></div>
    <div style="width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.15);"></div>
    <div style="width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,0.15);"></div>
    <span style="font-size:9px;color:rgba(255,255,255,0.3);margin-left:6px;">文件名.md</span>
  </div>
  <div style="font-size:10px;line-height:1.8;color:rgba(255,255,255,0.4);">代码内容</div>
</div>
```

### 流程图（转化类）

```html
<div style="display:flex;align-items:center;justify-content:center;gap:12px;">
  <div style="background:rgba(255,255,255,0.1);border-radius:8px;padding:12px 16px;text-align:center;">
    <div style="font-size:24px;">emoji</div>
    <div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:4px;">步骤1</div>
  </div>
  <div style="color:rgba(255,255,255,0.3);font-size:18px;">→</div>
  <div style="background:rgba(196,69,54,0.2);border:1px solid rgba(196,69,54,0.3);border-radius:8px;padding:12px 16px;text-align:center;">
    <div style="font-size:24px;">emoji</div>
    <div style="font-size:12px;color:#C44536;margin-top:4px;font-weight:600;">最终结果</div>
  </div>
</div>
```

### SVG 数据可视化

对于有数据、对比、地图、流程等内容，用 inline SVG 绘制可视化图表。SVG 渲染清晰度高，适合 html2canvas 导出。
