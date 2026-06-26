---
name: html-ppt
description: >
  制作以 HTML 为载体的幻灯片演示文稿（代替传统 PPT/PPTX）。每张幻灯片严格遵循 16:9
  比例，使用 CSS scroll-snap 实现翻页，支持键盘/滚轮操作，并可通过浏览器打印导出 PDF。
  每当用户提到"做 PPT"、"做幻灯片"、"做演示文稿"、"写 PPT"、"制作 slides"、"deck"
  等关键词时，必须触发本 skill，优先以 HTML 形式交付，而非生成 .pptx 文件。
  即使用户只说"帮我做个介绍某主题的 PPT"而未指明格式，也应主动采用本 skill 的方案。
---

# HTML PPT Skill

用 HTML + CSS 制作媲美专业设计软件的幻灯片，视觉效果远超传统 PPT 工具。

## 核心规范（必须遵守）

### 1. 比例与分页

```css
/* 每张幻灯片：宽 = 100vw，高 = 56.25vw（即 9/16）*/
.slide {
  width: 100vw;
  height: 56.25vw;
  overflow: hidden;
  scroll-snap-align: start;
  scroll-snap-stop: always;
}

/* body 开启强制对齐 */
body {
  scroll-snap-type: y mandatory;
  overflow-y: scroll;
  height: 100%;
}
html { height: 100%; }
```

**原理**：`56.25vw = 9/16 × 100vw`，无论屏幕分辨率如何，每页都精确为 16:9。

### 2. 打印 / 导出 PDF

```css
@media print {
  html, body { height: auto; overflow: visible; scroll-snap-type: none; }
  #nav-dots, #nav-arrows { display: none !important; }
  .slide {
    width: 297mm;
    height: 167.0625mm;   /* 297 × 9/16 = 167.0625 */
    page-break-after: always;
    break-after: page;
    scroll-snap-align: none;
  }
}
```

用户按 **Ctrl+P → 另存为 PDF** 即可导出，每页精确对应一张幻灯片。

### 3. 导航 JS（标准实现，每次必须包含）

```javascript
const slides = Array.from(document.querySelectorAll('.slide'));
let current = 0;

function goTo(i) {
  i = Math.max(0, Math.min(slides.length - 1, i));
  slides[i].scrollIntoView({ behavior: 'smooth' });
  current = i;
  updateDots(i);
}

// 键盘支持
document.addEventListener('keydown', e => {
  if (['ArrowDown','ArrowRight','PageDown'].includes(e.key)) { e.preventDefault(); goTo(current+1); }
  if (['ArrowUp','ArrowLeft','PageUp'].includes(e.key))      { e.preventDefault(); goTo(current-1); }
});

// IntersectionObserver 同步当前页
const io = new IntersectionObserver(entries => {
  entries.forEach(en => { if (en.isIntersecting) { current = slides.indexOf(en.target); updateDots(current); }});
}, { threshold: 0.6 });
slides.forEach(s => io.observe(s));
```

---

## 标准文件结构

每次生成的 HTML 文件必须包含以下部分：

```
<head>
  Google Fonts 引入（选择与主题匹配的中文字体）
  <style>
    1. CSS 变量（颜色、字体）
    2. 核心框架（slide 比例、scroll-snap、body）
    3. 导航组件样式（dots、arrows）
    4. 通用设计组件（见下方）
    5. @media print
  </style>
</head>
<body>
  <nav id="nav-dots">（自动生成）</nav>
  <div id="nav-arrows">↑ ↓ 按钮</div>

  <section class="slide" id="slide-1"> ... </section>
  <section class="slide" id="slide-2"> ... </section>
  ...

  <script> 导航逻辑 </script>
</body>
```

---

## 设计规范

详细设计组件库见 `references/design-system.md`。

### 字体选择原则
- **中文展示字体**：`ZCOOL XiaoWei`（庄重）、`Ma Shan Zheng`（书法）、`Long Cang`（手写）
- **中文正文字体**：`Noto Serif SC`（衬线）、`Noto Sans SC`（无衬线）
- **英文展示字体**：`Playfair Display`、`Cormorant Garamond`、`Space Mono`
- **禁止使用**：Arial、Inter、Roboto、system-ui（太通用，无设计感）

### 颜色主题选择
根据演示主题选择合适的色系，参考 `references/design-system.md` 中的预设主题。

### 每张幻灯片的尺寸感知
- 字体大小使用 `vw` 单位（如 `3.5vw`），随屏幕等比缩放
- 间距使用 `%` 或 `vw` 单位，避免固定 `px`
- 内容区 padding 建议：`4% 6%`

---

## 典型页面类型

| 页面类型 | 适用场景 | 布局要点 |
|----------|----------|----------|
| 封面页   | 第一页   | 大标题居中或左对齐，背景有视觉冲击力 |
| 目录页   | 第二页   | 2×2 或 1×N 卡片网格列举章节 |
| 双栏内容页 | 文字+图/列表 | `grid-template-columns: 1fr 1fr` |
| 全图页   | 视觉冲击 | 图片铺满，文字叠加半透明遮罩 |
| 数据页   | 展示指标 | 大数字 + 进度条 + 说明文字 |
| 时间线页 | 历史/流程 | 横向或纵向时间轴 |
| 引用页   | 金句/观点 | 超大引号装饰，居中排版 |
| 结尾页   | 致谢/Q&A  | 简洁有力，附联系方式或行动引导 |

---

## 工作流程

接到 PPT 制作需求时，按以下步骤执行：

1. **理解需求**：主题、受众、页数、风格偏好（科技/商务/学术/文化）
2. **选定主题**：从 `references/design-system.md` 选择或创建配色方案
3. **规划页面**：确定每页类型和内容大纲
4. **逐页编写**：每张 `.slide` 按内容量和页面类型选择合适布局
5. **检查清单**（完成后必须自查）：
   - [ ] 每页都有 `class="slide"` 和 `id="slide-N"`
   - [ ] 每页底部有页码 `<span class="slide-num">N / Total</span>`
   - [ ] body 有 `scroll-snap-type: y mandatory`
   - [ ] 包含键盘导航 JS
   - [ ] 包含 `@media print` 样式
   - [ ] 所有字体大小用 `vw` 单位（非 `px`）
   - [ ] 文件输出到 `/mnt/user-data/outputs/` 并调用 `present_files`

---

## 快速参考：CSS 变量模板

```css
:root {
  /* 根据主题替换以下变量 */
  --c-bg:      #0D0F14;       /* 背景色 */
  --c-surface: #151820;       /* 卡片背景 */
  --c-border:  rgba(255,255,255,0.08);
  --c-accent:  #4F8EF7;       /* 主强调色 */
  --c-accent2: #A78BFA;       /* 副强调色 */
  --c-text:    #F0F2F8;       /* 主文字色 */
  --c-muted:   rgba(240,242,248,0.45); /* 次要文字 */

  --f-display: 'ZCOOL XiaoWei', serif;
  --f-body:    'Noto Sans SC', sans-serif;

  /* 固定不变 */
  --slide-w: 100vw;
  --slide-h: 56.25vw;
}
```