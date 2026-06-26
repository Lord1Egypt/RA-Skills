# 日报生成 HTML 输出规范

> 本文件定义新建日报 HTML 的必要模板元素，供 Claude Code / AI 助手生成新日报时参照。

---

## 必需结构

### 1. `<html>` 根元素
必须包含 `data-theme="dark"` 属性（默认深色），以支持主题切换：

```html
<html lang="zh-CN" data-theme="dark">
```

---

### 2. CSS 变量（`:root`）与字体规范

**字体：** 统一使用系统字体栈，不指定中文特定字体：

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
}
```

**CSS 变量（必须声明）：**

```css
:root {
  --bg-primary:    <深色背景值>;
  --bg-card:       <卡片深色背景值>;
  --bg-card-hover: <卡片悬浮深色背景值>;
  --border:        <边框深色值>;
  --text-primary:  <主文字深色值>;
  --text-secondary:<次文字深色值>;
  /* accent 色根据当日配色主题设置 */
}
```

**各元素字号参考（基于 16px body）：**

| 元素 | 字号 |
|---|---|
| `body` / 正文段落 | `16px` |
| `.newspaper-title` | `28px` |
| `.issue-info` / `.stats-badge` | `11px` |
| `.section-title` / `.block-title` | `15px` |
| `blockquote` / `.analysis-box` | `12px` |
| `.chat-sender` / `.bubble-sender` | `11px` |
| `footer` | `13px` |

---

### 3. 亮色主题 CSS 覆盖（必须包含，放在 `</style>` 前）

```css
/* ── 主题切换按钮 ── */
.theme-btn {
  padding: 5px 14px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 11px;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.theme-btn:hover {
  color: var(--text-primary);
  background: var(--bg-card-hover);
}
/* ── 亮色主题变量覆盖 ── */
[data-theme="light"] {
  --bg-primary:    #f5f3ee;
  --bg-card:       #ffffff;
  --bg-card-hover: #edeae0;
  --border:        #d4cfc0;
  --text-primary:  #1e1b14;
  --text-secondary:#6b6555;
}
[data-theme="light"] blockquote {
  background: rgba(0,0,0,0.04);
  color: #3a3525;
}
[data-theme="light"] .analysis-box {
  background: rgba(0,0,0,0.04);
  color: #3a3525;
}
[data-theme="light"] .newspaper-header {
  background: linear-gradient(135deg, #f0ede2, #f7f5ee);
}
[data-theme="light"] .block-teacher {
  background: linear-gradient(135deg, #f0ede2, #edeae0);
}
```

---

### 4. 主题切换按钮 HTML（放在 `<div class="header-top">` 末尾，`</div>` 前）

```html
<div class="header-top">
  <span class="issue-info">...</span>
  <h1 class="newspaper-title">...</h1>
  <span class="stats-badge">...</span>
  <button class="theme-btn" id="themeToggle" onclick="toggleTheme()">☀️ 明亮</button>
</div>
```

> 按钮文字：`☀️ 明亮` = 当前深色（点击切换亮色）；`🌙 暗黑` = 当前亮色（点击切换深色）

---

### 5. FOUC 防闪烁脚本（放在 `<head>` 内，`<style>` 之前）

```html
<script>
  /* 防闪烁：阻塞执行，在样式渲染前设定主题 */
  (function () {
    const t = localStorage.getItem('pusa-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', t);
  })();
</script>
```

---

### 6. 主题切换 JavaScript（放在 `</body>` 前，独立 `<script>` 块）

```html
<script>
  /* ── 主题切换 ── */
  (function () {
    /* data-theme 已在 <head> 设置，这里只更新按钮图标 */
    const saved = localStorage.getItem('pusa-theme') || 'dark';
    document.addEventListener('DOMContentLoaded', function () {
      const btn = document.getElementById('themeToggle');
      if (btn) btn.textContent = saved === 'dark' ? '☀️ 明亮' : '🌙 暗黑';
    });
  })();
  function toggleTheme() {
    const html = document.documentElement;
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('pusa-theme', next);
    const btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = next === 'dark' ? '☀️ 明亮' : '🌙 暗黑';
  }
  /* 接收父页面（index.html）的主题同步消息 */
  window.addEventListener('message', function (e) {
    if (e.data && e.data.type === 'pusa-theme') {
      const theme = e.data.theme;
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('pusa-theme', theme);
      const btn = document.getElementById('themeToggle');
      if (btn) btn.textContent = theme === 'dark' ? '☀️ 明亮' : '🌙 暗黑';
    }
  });
</script>
```

**localStorage key**：`pusa-theme`（所有页面统一，浏览器记忆主题偏好）

---

## 布局规范：瀑布流（Masonry Layout）

### 7. 瀑布流布局 CSS

日报采用 **三栏瀑布流布局**，内容自动分配到最短的列，确保视觉平衡：

```css
.newspaper-grid {
  column-count: 3;
  column-gap: 32px;
  max-width: 1600px;
  margin: 24px auto;
  padding: 0 40px;
}

@media (max-width: 1200px) {
  .newspaper-grid {
    column-count: 1;
    padding: 0 20px;
  }
}

section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  break-inside: avoid;  /* 关键：防止section被截断 */
}
```

**核心原理：**
- `column-count: 3` — 三栏布局
- `break-inside: avoid` — 防止内容块在列中间断开
- 浏览器自动将后续 `<section>` 填充到最短的列

---

### 8. HTML 结构要求

**✅ 正确的扁平结构：**

```html
<main class="newspaper-grid">
  <section class="block-announcement">...</section>
  <section class="block-honor">...</section>
  <section class="block-teacher">...</section>
  <section class="block-hot">...</section>  <!-- 话题1 -->
  <section class="block-hot">...</section>  <!-- 话题2 -->
  <section class="block-hot">...</section>  <!-- 话题3 -->
  <section class="block-ai">...</section>
  <section class="block-community">...</section>
</main>
```

**❌ 错误的嵌套结构：**

```html
<!-- 不要这样写！ -->
<main class="newspaper-grid">
  <aside class="col-left">
    <section>...</section>
    <section>...</section>
  </aside>
  <article class="col-center">
    <section>...</section>
  </article>
  <aside class="col-right">
    <section>...</section>
  </aside>
</main>
```

**原则：** `<main class="newspaper-grid">` 下只能有平级的 `<section>` 元素，不允许额外的包裹层。

---

### 9. 内容拆分规则（视觉平衡策略）

**核心目标：** 确保瀑布流三列高度接近，避免某列过长或过短。

#### 拆分判断标准

| 板块类型 | 何时拆分 | 拆分方式 |
|---------|---------|---------|
| **热议话题** | 超过 **3 个话题** | 每个话题独立成一个 `<section class="block-hot">` |
| **AI资讯** | 超过 **4 条资讯** | 拆分成多个 `<section class="block-ai">`，每个包含2-3条 |
| **社群动态** | 内容高度超过 **800px**（约50行）| 拆分成"新成员"和"今日氛围"两个section |
| **师说** | 超过 **2 位老师发言** | 每位老师独立成一个 `<section class="block-teacher">` |

#### 拆分示例：热议话题

**原结构（不拆分，当话题 ≤ 3 个时）：**

```html
<section class="block-hot">
  <h2 class="block-title"><span class="icon">🔥</span>热议话题</h2>
  <div class="hot-topic">...</div>  <!-- 话题1 -->
  <div class="hot-topic">...</div>  <!-- 话题2 -->
  <div class="hot-topic">...</div>  <!-- 话题3 -->
</section>
```

**拆分后（当话题 > 3 个时）：**

```html
<!-- 话题1 -->
<section class="block-hot">
  <h2 class="block-title">
    <span class="icon">🔥</span>
    <span class="author-tag">作者</span>话题标题
    <span class="heat-stats">👥 15人参与</span>
  </h2>
  <!-- 话题内容 -->
</section>

<!-- 话题2 -->
<section class="block-hot">
  <h2 class="block-title">
    <span class="icon">🔥</span>
    <span class="author-tag">作者</span>话题标题
    <span class="heat-stats">💬 8人参与</span>
  </h2>
  <!-- 话题内容 -->
</section>

<!-- 话题3、4、5... 以此类推 -->
```

**删除多余样式：** 拆分后不再需要 `.hot-topic` / `.hot-topic-title` 样式，直接用 `section` + `h2.block-title`。

#### 经验法则

- **每个 section 的理想高度：** 400-800px（约30-60行内容）
- **拆分时机：** 生成HTML后，如发现某个section明显过长（>1000px 或 >80行），应考虑拆分
- **优先拆分：** 热议话题（最容易过长）> AI资讯 > 社群动态

---

## 注意事项

- **accent 颜色**（蓝/绿/橙/紫/金）在亮色背景下保持不变，无需覆盖。
- 若日报中有硬编码深色背景的 class（如 `.block-teacher`），需在亮色覆盖块中单独处理。
- `index.html` 的主题按钮放在 `.nav-btns` 内，`toggleTheme()` 额外用 postMessage 同步 iframe：
  ```javascript
  const iframe = document.querySelector('#iframeContainer iframe');
  if (iframe && iframe.contentWindow) {
    try { iframe.contentWindow.postMessage({ type: 'pusa-theme', theme: next }, '*'); } catch(e) {}
  }
  ```
  `iframe.onload` 中也同步：
  ```javascript
  iframe.onload = () => {
    const theme = document.documentElement.getAttribute('data-theme');
    try { iframe.contentWindow.postMessage({ type: 'pusa-theme', theme }, '*'); } catch(e) {}
  };
  ```
