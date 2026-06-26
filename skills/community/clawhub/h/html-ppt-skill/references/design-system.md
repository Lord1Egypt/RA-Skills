# HTML PPT Design System

设计组件库与预设主题，供 SKILL.md 引用。

---

## 目录
1. [预设颜色主题](#预设颜色主题)
2. [通用 CSS 组件](#通用-css-组件)
3. [背景装饰模式](#背景装饰模式)
4. [布局模板代码](#布局模板代码)
5. [动画效果库](#动画效果库)

---

## 预设颜色主题

### 🌑 深空暗黑（科技/互联网）
```css
--c-bg: #0D0F14; --c-surface: #151820;
--c-accent: #4F8EF7; --c-accent2: #A78BFA;
--c-text: #F0F2F8; --c-muted: rgba(240,242,248,0.45);
```

### 🏮 金墨（中国文化/历史/政府）
```css
--c-bg: #1A1209; --c-surface: #251A0D;
--c-accent: #D4A017; --c-accent2: #C0392B;
--c-text: #FAF5E8; --c-muted: rgba(250,245,232,0.5);
--f-display: 'ZCOOL XiaoWei', serif;
```

### 🌿 自然绿（环保/农业/医疗）
```css
--c-bg: #0A1A0F; --c-surface: #0F2415;
--c-accent: #34D399; --c-accent2: #6EE7B7;
--c-text: #ECFDF5; --c-muted: rgba(236,253,245,0.5);
```

### ☁️ 纯白简约（学术/报告/通用）
```css
--c-bg: #FFFFFF; --c-surface: #F8F9FA;
--c-border: rgba(0,0,0,0.08);
--c-accent: #2563EB; --c-accent2: #7C3AED;
--c-text: #111827; --c-muted: #6B7280;
```

### 🔥 暖橙（创业/品牌/活力）
```css
--c-bg: #0F0A06; --c-surface: #1A1208;
--c-accent: #F97316; --c-accent2: #FBBF24;
--c-text: #FFF7ED; --c-muted: rgba(255,247,237,0.5);
```

### 🧊 冰蓝（金融/咨询/企业）
```css
--c-bg: #F0F4F8; --c-surface: #FFFFFF;
--c-border: rgba(30,64,175,0.1);
--c-accent: #1E40AF; --c-accent2: #0EA5E9;
--c-text: #0F172A; --c-muted: #475569;
```

---

## 通用 CSS 组件

### 基础排版
```css
/* 超大展示标题 */
.title-xl {
  font-family: var(--f-display);
  font-size: 6.5vw; line-height: 1.1;
  letter-spacing: 0.04em;
}
/* 页面主标题 */
.title-lg {
  font-family: var(--f-serif, var(--f-body));
  font-size: 3.8vw; line-height: 1.25; font-weight: 700;
}
/* 章节标题 */
.title-md {
  font-size: 2.4vw; line-height: 1.3; font-weight: 700;
}
/* 正文 */
.body-text {
  font-size: 1.2vw; line-height: 1.9; color: var(--c-muted); font-weight: 300;
}
/* 小标签 */
.label {
  font-size: 0.85vw; letter-spacing: 0.35em; text-transform: uppercase;
  color: var(--c-accent); font-weight: 500; margin-bottom: 1%;
}
```

### 分割线
```css
.divider {
  width: 5vw; height: 2px;
  background: linear-gradient(90deg, var(--c-accent), transparent);
  margin: 1.5% 0;
}
```

### 卡片
```css
.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  padding: 2% 2.5%;
  transition: border-color 0.3s;
}
.card:hover { border-color: rgba(79,142,247,0.3); }
/* 顶部强调线变体 */
.card-accent { border-top: 2px solid var(--c-accent); }
```

### 数据统计
```css
.stat-num {
  font-family: var(--f-display);
  font-size: 5vw; color: var(--c-accent); line-height: 1;
}
.stat-label {
  font-size: 0.9vw; color: var(--c-muted);
  letter-spacing: 0.15em; margin-top: 0.3vw;
}
```

### 列表
```css
.bullet-list { list-style: none; display: flex; flex-direction: column; gap: 0.8%; }
.bullet-list li {
  font-size: 1.15vw; color: var(--c-muted);
  padding-left: 1.4vw; position: relative; line-height: 1.7;
}
.bullet-list li::before {
  content: ''; position: absolute; left: 0; top: 0.65vw;
  width: 0.4vw; height: 0.4vw;
  border-radius: 50%; background: var(--c-accent);
}
```

### 进度条
```css
/* 容器 */
.progress-bar-bg {
  height: 0.35vw; background: rgba(255,255,255,0.08); border-radius: 2px;
}
/* 填充：用 style="width:75%" 控制百分比 */
.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--c-accent), var(--c-accent2));
  border-radius: 2px;
}
```

### 图标圆
```css
.icon-circle {
  width: 4vw; height: 4vw; border-radius: 50%;
  background: rgba(79,142,247,0.12);
  border: 1px solid rgba(79,142,247,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8vw; flex-shrink: 0;
}
```

### 页码
```css
.slide-num {
  position: absolute; bottom: 2.2%; right: 3%;
  font-size: 0.9vw; color: rgba(255,255,255,0.2);
  letter-spacing: 0.15em; z-index: 10;
}
```

### 高亮文字
```css
.hl        { color: var(--c-accent); }
.hl-2      { color: var(--c-accent2); }
.hl-gold   { color: #F5C842; }
```

---

## 背景装饰模式

### 网格背景
```html
<div style="position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.03) 1px,transparent 1px);
  background-size:4vw 4vw;pointer-events:none;"></div>
```

### 光晕装饰（Glow）
```html
<!-- 蓝色光晕 -->
<div style="position:absolute;width:25vw;height:25vw;
  border-radius:50%;background:var(--c-accent);
  filter:blur(6vw);opacity:0.2;top:-5vw;left:-5vw;pointer-events:none;"></div>
```

### 大字背景水印
```html
<div style="position:absolute;right:4%;top:50%;transform:translateY(-50%);
  font-family:var(--f-display);font-size:18vw;
  color:rgba(79,142,247,0.05);line-height:1;pointer-events:none;">关键词</div>
```

### 斜线装饰分割
```html
<div style="position:absolute;right:0;top:0;bottom:0;width:35%;
  background:linear-gradient(135deg,transparent 50%,rgba(79,142,247,0.06) 50%);
  pointer-events:none;"></div>
```

### 圆点阵列
```html
<div style="position:absolute;inset:0;
  background-image:radial-gradient(rgba(255,255,255,0.08) 1px,transparent 1px);
  background-size:2.5vw 2.5vw;pointer-events:none;"></div>
```

---

## 布局模板代码

### 封面页
```html
<section class="slide" id="slide-1">
  <!-- 背景 -->
  <div class="grid-bg"></div>
  <div class="glow" style="width:30vw;height:30vw;top:-8vw;left:-6vw;background:var(--c-accent);filter:blur(6vw);opacity:0.25;position:absolute;border-radius:50%;pointer-events:none;"></div>

  <div style="position:relative;z-index:2;padding:4% 6%;height:100%;display:flex;flex-direction:column;justify-content:center;gap:1.5%;">
    <p class="label">副标题标签 · 年份</p>
    <h1 class="title-xl">主标题<br><span class="hl">关键词</span></h1>
    <div class="divider"></div>
    <p class="body-text" style="max-width:40vw;">一句话描述演示内容，简洁有力。</p>
  </div>
  <span class="slide-num">01 / N</span>
</section>
```

### 双栏内容页
```html
<section class="slide" id="slide-N">
  <div style="position:relative;z-index:2;padding:4% 6%;height:100%;display:flex;flex-direction:column;justify-content:center;gap:1.5%;">
    <p class="label">章节名</p>
    <h2 class="title-lg">页面标题</h2>
    <div class="divider"></div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3%;flex:1;align-items:center;">
      <div><!-- 左列内容 --></div>
      <div><!-- 右列内容 --></div>
    </div>
  </div>
  <span class="slide-num">N / Total</span>
</section>
```

### 四格卡片页
```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5% 2%;">
  <div class="card" style="display:flex;align-items:flex-start;gap:1.2vw;">
    <div class="icon-circle">🔍</div>
    <div>
      <p style="font-size:1.3vw;font-weight:500;color:var(--c-text);margin-bottom:0.4vw;">小标题</p>
      <p class="body-text">描述文字。</p>
    </div>
  </div>
  <!-- 复制3次 -->
</div>
```

### 数据统计页
```html
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2%;">
  <div class="card card-accent" style="text-align:center;">
    <div class="stat-num">99%</div>
    <p class="stat-label">指标说明</p>
  </div>
  <!-- 复制N次 -->
</div>
```

### 时间线页（横向）
```html
<div style="display:flex;align-items:flex-start;gap:0;position:relative;margin-top:3%;">
  <!-- 连接线 -->
  <div style="position:absolute;top:1vw;left:1vw;right:1vw;height:2px;background:linear-gradient(90deg,var(--c-accent),var(--c-accent2));z-index:0;"></div>
  <!-- 节点（重复） -->
  <div style="flex:1;position:relative;z-index:1;text-align:center;padding:0 1%;">
    <div style="width:2vw;height:2vw;border-radius:50%;background:var(--c-accent);border:3px solid var(--c-bg);margin:0 auto 1vw;"></div>
    <p style="font-size:0.9vw;color:var(--c-accent);">年份</p>
    <p style="font-size:1vw;font-weight:600;color:var(--c-text);margin:0.3vw 0;">标题</p>
    <p class="body-text" style="font-size:0.95vw;">描述</p>
  </div>
</div>
```

---

## 动画效果库

### 入场动画（加在 .slide 的直接子元素）
```css
@keyframes fadeUp {
  from { opacity:0; transform:translateY(1.5vw); }
  to   { opacity:1; transform:none; }
}
/* 用法：style="animation: fadeUp 0.8s 0.2s both" */
/* 叠加延迟：每个元素 delay + 0.15s 产生错落感 */
```

### 脉冲光圈
```css
@keyframes pulse-ring {
  0%   { transform:scale(1); opacity:0.6; }
  100% { transform:scale(1.8); opacity:0; }
}
```

### 无限滚动背景网格
```css
@keyframes gridDrift {
  from { transform:translateY(0); }
  to   { transform:translateY(4vw); }
}
/* background-size 与 animation 步长一致 */
```

---

## 导航组件完整代码

```css
/* 右侧导航点 */
#nav-dots {
  position:fixed; right:1.5vw; top:50%; transform:translateY(-50%);
  display:flex; flex-direction:column; gap:8px; z-index:1000;
}
.dot {
  width:6px; height:6px; border-radius:50%;
  background:rgba(255,255,255,0.25); cursor:pointer;
  transition:all 0.3s; border:none; padding:0;
}
.dot.active { background:var(--c-accent); transform:scale(1.4); }

/* 底部箭头 */
#nav-arrows {
  position:fixed; bottom:2.5vw; left:50%; transform:translateX(-50%);
  display:flex; gap:16px; z-index:1000;
}
.arrow-btn {
  width:36px; height:36px; border:1px solid rgba(255,255,255,0.2);
  background:rgba(255,255,255,0.05); backdrop-filter:blur(8px);
  color:rgba(255,255,255,0.6); cursor:pointer; font-size:14px;
  border-radius:50%; transition:all 0.2s;
  display:flex; align-items:center; justify-content:center;
}
.arrow-btn:hover { background:rgba(79,142,247,0.2); border-color:var(--c-accent); color:var(--c-accent); }
```

```javascript
// 完整导航 JS
const slides = Array.from(document.querySelectorAll('.slide'));
const dotsContainer = document.getElementById('nav-dots');

slides.forEach((_, i) => {
  const btn = document.createElement('button');
  btn.className = 'dot' + (i === 0 ? ' active' : '');
  btn.title = `第 ${i+1} 页`;
  btn.addEventListener('click', () => goTo(i));
  dotsContainer.appendChild(btn);
});

const dots = () => Array.from(dotsContainer.querySelectorAll('.dot'));
let current = 0;

function goTo(i) {
  i = Math.max(0, Math.min(slides.length-1, i));
  slides[i].scrollIntoView({ behavior:'smooth' });
  dots().forEach((d,idx) => d.classList.toggle('active', idx===i));
  current = i;
}

document.addEventListener('keydown', e => {
  if (['ArrowDown','ArrowRight','PageDown'].includes(e.key)) { e.preventDefault(); goTo(current+1); }
  if (['ArrowUp','ArrowLeft','PageUp'].includes(e.key))      { e.preventDefault(); goTo(current-1); }
});

document.getElementById('btn-up').addEventListener('click', () => goTo(current-1));
document.getElementById('btn-dn').addEventListener('click', () => goTo(current+1));

new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting) {
      current = slides.indexOf(en.target);
      dots().forEach((d,i) => d.classList.toggle('active', i===current));
    }
  });
}, { threshold:0.6 }).observe = (() => {
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        current = slides.indexOf(en.target);
        dots().forEach((d,i) => d.classList.toggle('active', i===current));
      }
    });
  }, { threshold:0.6 });
  slides.forEach(s => io.observe(s));
})();
```