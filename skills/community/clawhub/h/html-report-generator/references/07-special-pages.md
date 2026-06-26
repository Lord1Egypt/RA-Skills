# 07 · 特殊页面规范

> 封面/目录/章节分隔/结尾页是报告叙事的骨架，缺一不可。
> **这类页面内容极少、视觉权重极高**，与内容页规则完全不同。

---

## 🤖 特殊页面识别规则

每份报告必须包含：
```
P00（可选）：封面页       — 第一印象，定义报告气质
P01：        执行摘要页   — 内容起点（此后为内容页）
章节节点处：  章节分隔页   — 每个主要章节前插入（可选，长报告用）
最后一页：    结尾页       — 结束信号，留联系方式或行动召唤
```

---

## 一、封面页（Cover Page）

### 设计原则

```
- 文字极少（标题 + 副标题 + 日期/机构，≤5个元素）
- 视觉占主导（大面积背景 + 装饰图形 ≥ 70% 面积）
- 定义整份报告的气质（必须与后续页 Tc 模板一致）
- 禁止任何卡片、网格布局、SVG图表
```

### 四区调整（封面专用）

```
封面四区可以合并或重新分配：
方案A：Header 0px + Content 700px + Summary 0px + Footer 20px（全屏沉浸）
方案B：Header 0px + Content 650px + Summary 50px + Footer 20px
方案C：保持标准四区（72+580+48+20），但内容区做全屏视觉处理
```

### 封面变体 CV1 · 居中英雄型（暗色系）

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  width: 1017px; height: 720px;
  min-width: 1017px; max-width: 1017px;
  min-height: 720px; max-height: 720px;
  overflow: hidden;
  background: var(--bg);
  font-family: 'PingFang SC','Microsoft YaHei',sans-serif;
}
:root {
  --p: #3b82f6; --bg: #050a18; --t: #e2e8f0; --mt: #94a3b8; --dt: #475569;
}
/* 装饰光晕 */
.glow-1 {
  position:absolute; width:600px; height:600px;
  top:-150px; left:-100px; border-radius:50%; pointer-events:none;
  background: radial-gradient(ellipse, rgba(59,130,246,0.08) 0%, transparent 65%);
}
.glow-2 {
  position:absolute; width:500px; height:500px;
  bottom:-100px; right:-80px; border-radius:50%; pointer-events:none;
  background: radial-gradient(ellipse, rgba(139,92,246,0.07) 0%, transparent 65%);
}
/* 噪点纹理 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:1;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
}
/* 顶部细线装饰 */
.top-line {
  position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg, transparent, var(--p), transparent);
}
/* 中心内容区 */
.cover-center {
  position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  text-align:center; z-index:2; width:750px;
}
.eyebrow {
  font-size:10px; letter-spacing:3px; text-transform:uppercase;
  color:var(--p); margin-bottom:20px;
  display:flex; align-items:center; justify-content:center; gap:10px;
}
.eyebrow::before, .eyebrow::after {
  content:''; height:1px; width:40px;
  background: linear-gradient(90deg, transparent, var(--p));
}
.eyebrow::after { transform:scaleX(-1); }
.main-title {
  font-size:52px; font-weight:800; letter-spacing:-2px; line-height:1.05;
  color: var(--t); margin-bottom:16px;
}
.main-title span { color:var(--p); }
.sub-title {
  font-size:14px; font-weight:300; color:var(--mt);
  letter-spacing:0.3px; line-height:1.6; margin-bottom:32px;
}
.meta-row {
  display:flex; align-items:center; justify-content:center; gap:20px;
  font-size:10px; color:var(--dt); letter-spacing:1px;
}
.meta-dot { width:3px; height:3px; border-radius:50%; background:var(--dt); }
/* 底部装饰线 */
.bottom-bar {
  position:absolute; bottom:0; left:0; right:0; height:20px;
  display:flex; align-items:center; padding:0 25px;
  justify-content:space-between; z-index:2;
}
.progress-track {
  width:120px; height:2px; background:rgba(255,255,255,0.05); border-radius:1px;
}
.progress-fill { width:10%; height:100%; background:var(--p); border-radius:1px; }
</style>
</head>
<body>
  <div class="glow-1"></div>
  <div class="glow-2"></div>
  <div class="top-line"></div>

  <div class="cover-center">
    <div class="eyebrow">RESEARCH REPORT · 2025</div>
    <div class="main-title">报告<span>主标题</span><br>第二行标题</div>
    <div class="sub-title">副标题描述，简洁表达报告核心价值主张，不超过两行</div>
    <div class="meta-row">
      <span>机构/作者名</span>
      <div class="meta-dot"></div>
      <span>2025年3月</span>
      <div class="meta-dot"></div>
      <span>共 10 页</span>
    </div>
  </div>

  <div class="bottom-bar">
    <span style="font-size:9px;color:var(--dt);letter-spacing:1px;">CONFIDENTIAL</span>
    <div class="progress-track"><div class="progress-fill"></div></div>
    <span style="font-size:9px;color:var(--dt);font-family:monospace;">COVER</span>
  </div>
</body>
</html>
```

---

---

## 二、目录页（Table of Contents）

### 设计原则

```
- 清晰列出全部章节（≤12项），每项含序号 + 标题 + 页码
- 用视觉手段暗示内容结构（分组/色条/进度感）
- 不需要三层内容结构，不需要SVG图表
- 当前章节（若有）可高亮显示
```

### 目录变体 TC1 · 数字序号型（暗色）

```html
<style>
.toc-container {
  display:grid; grid-template-columns:1fr 1fr;
  gap:6px 30px; padding-top:10px; height:100%;
}
.toc-item {
  display:flex; align-items:center; gap:12px;
  padding:10px 14px; border-radius:6px;
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.05);
  transition:none;
}
.toc-item.active {
  background:var(--pm); border-color:var(--bd);
}
.toc-num {
  font-size:22px; font-weight:800; color:var(--p);
  opacity:0.4; letter-spacing:-1px; line-height:1;
  flex-shrink:0; width:32px;
}
.toc-item.active .toc-num { opacity:1; }
.toc-info { flex:1; }
.toc-label { font-size:9px; color:var(--dt); letter-spacing:1px; text-transform:uppercase; }
.toc-title { font-size:12px; font-weight:600; color:var(--t); margin-top:2px; }
.toc-pg {
  font-size:11px; color:var(--dt); font-family:monospace;
  flex-shrink:0;
}
</style>

<!-- HTML -->
<div class="toc-container">
  <div class="toc-item active">
    <div class="toc-num">01</div>
    <div class="toc-info">
      <div class="toc-label">OVERVIEW</div>
      <div class="toc-title">执行摘要</div>
    </div>
    <div class="toc-pg">P.01</div>
  </div>
  <!-- 重复 × N -->
</div>
```

---

## 三、章节分隔页（Chapter Divider）

### 设计原则

```
- 用于长报告（≥8页）中章节间的视觉休息
- 内容极少：章节序号 + 章节名 + 简短描述（≤30字）
- 视觉冲击力强：大字号/大色块/满版装饰
- 不使用卡片布局，不使用SVG图表
```

### 章节分隔变体 CD1 · 数字冲击型

```html
<style>
.chapter-bg-num {
  position:absolute; font-size:320px; font-weight:900;
  letter-spacing:-16px; line-height:1;
  color:rgba(255,255,255,0.03);
  right:-20px; top:50%; transform:translateY(-50%);
  pointer-events:none; z-index:0;
}
.chapter-content {
  position:absolute; left:60px; top:50%;
  transform:translateY(-50%); z-index:2;
}
.chapter-tag {
  font-size:9px; letter-spacing:3px; text-transform:uppercase;
  color:var(--p); margin-bottom:16px;
  display:flex; align-items:center; gap:8px;
}
.chapter-tag::after { content:''; height:1px; width:30px; background:var(--p); }
.chapter-num {
  font-size:80px; font-weight:900; letter-spacing:-4px; line-height:1;
  background:linear-gradient(135deg, var(--t) 30%, var(--p));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text; margin-bottom:12px;
}
.chapter-name {
  font-size:36px; font-weight:700; color:var(--t);
  letter-spacing:-1px; line-height:1.1; margin-bottom:14px;
}
.chapter-desc { font-size:12px; color:var(--mt); line-height:1.6; max-width:420px; }
</style>
```

---

## 四、结尾页（End / Thank You Page）

### 设计原则

```
- 明确的结束信号（"谢谢" / "Q&A" / "联系我们"）
- 可选：关键结论的一句话总结
- 可选：联系方式/二维码/行动号召
- 风格与封面呼应（使用相同气质）
```

### 结尾变体 EP1 · 感谢+联系型

```html
<style>
.end-center {
  position:absolute; top:50%; left:50%;
  transform:translate(-50%,-50%);
  text-align:center; z-index:2; width:700px;
}
.end-thanks {
  font-size:64px; font-weight:900; letter-spacing:-3px; line-height:1;
  color:var(--t); margin-bottom:8px;
}
.end-thanks span { color:var(--p); }
.end-sub { font-size:13px; color:var(--mt); margin-bottom:32px; }
.end-contacts {
  display:flex; justify-content:center; gap:24px; flex-wrap:wrap;
}
.end-contact-item {
  display:flex; align-items:center; gap:8px;
  background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
  border-radius:6px; padding:8px 16px;
  font-size:11px; color:var(--mt);
}
.end-contact-icon { width:14px; height:14px; border-radius:50%; background:var(--p); flex-shrink:0; }
</style>

<div class="end-center">
  <div class="end-thanks">感谢<span>聆听</span></div>
  <div class="end-sub">期待与您深入探讨 · 欢迎提问</div>
  <div class="end-contacts">
    <div class="end-contact-item">
      <div class="end-contact-icon"></div>
      <span>name@company.com</span>
    </div>
    <div class="end-contact-item">
      <div class="end-contact-icon"></div>
      <span>+86 138-0000-0000</span>
    </div>
  </div>
</div>
```

---

## 特殊页面质量检查

```
□ 报告首页是封面页（Cover），而非直接从内容页开始？
□ 封面文字元素 ≤ 5 个（标题/副标题/日期/机构/页码）？
□ 封面视觉装饰面积 ≥ 60%（非纯文字）？
□ 封面气质与后续页 Tc 模板一致？
□ 结尾页是明确的结束信号，而非内容页突然结束？
□ 章节分隔页（如有）字数 ≤ 30 字？
□ 特殊页不包含卡片网格布局和SVG数据图表？
```
