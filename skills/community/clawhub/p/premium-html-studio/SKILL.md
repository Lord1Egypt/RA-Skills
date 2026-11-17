---
name: premium-html-studio
description: "Generate professional-grade single-file HTML technical docs and proposals (方案) with two premium design systems. (1) International: Playfair Display + Inter + JetBrains Mono, indigo/purple palette, Stripe/Linear/Apple Docs quality for API docs, architecture, workflow analysis, research reports. (2) Chinese Technical Spec style (中文技术规格, Multi-ES style): Noto Sans SC + Noto Serif SC + JetBrains Mono, deep-purple gradient cover with KPI stats, numbered Part dividers, vertical pipeline flow charts with colored stage bars, data-flow funnel, tinted callouts — ideal for Chinese 流程详解/模式详解/链路图/节点拆解/参数说明 docs. Pairs with Prism.js syntax highlighting, layered shadows, gradient accents, publication-quality SVG diagrams. Triggers on: 技术文档, HTML 文档, 技术方案, 项目方案, 架构方案, 设计方案, 实施方案, 研究报告, 流程详解, 模式详解, 链路图, 流程图, 节点详解, pipeline 说明, proposal, premium docs, 专业文档, 漂亮的页面, 生成 HTML, make a professional HTML doc, write a proposal, generate a doc like Multi-ES, 按 Multi-ES 样式."
---

# Premium HTML Docs & Proposals

Generate professional, publication-quality HTML documentation pages AND structured proposals with a sophisticated design system.

## Complete Examples

Before diving into the design system, here are 3 complete working examples you can use as starting points:

### Example 1: Technical Documentation

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Redis 缓存层技术方案</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400;1,700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
<style>
  :root {
    --bg: #fafaf9;
    --surface: #ffffff;
    --border: #e5e7eb;
    --text: #111827;
    --text-muted: #6b7280;
    --brand: #059669;
    --brand-dark: #047857;
    --brand-light: #d1fae5;
    --brand-soft: #ecfdf5;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
    --shadow-brand: 0 8px 24px rgba(5,150,105,0.20), 0 2px 8px rgba(5,150,105,0.10);
    --sp-1: 4px; --sp-2: 8px; --sp-3: 12px; --sp-4: 16px;
    --sp-5: 24px; --sp-6: 32px; --sp-7: 48px; --sp-8: 64px;
    --r-sm: 6px; --r-md: 10px; --r-lg: 14px; --r-xl: 20px;
    --ease: cubic-bezier(0.16, 1, 0.3, 1);
    --font-display: 'Playfair Display', Georgia, serif;
    --font-body: 'Inter', 'PingFang SC', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
  }
  [data-theme="dark"] {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --text-muted: #8b949e;
    --brand: #10b981;
    --brand-dark: #059669;
    --brand-light: #064e3b;
    --brand-soft: #022c22;
  }
  * { box-sizing: border-box; }
  body {
    font-family: var(--font-body);
    background: var(--bg);
    color: var(--text);
    line-height: 1.65;
    margin: 0;
    transition: background 0.3s var(--ease), color 0.3s var(--ease);
  }
  .container { max-width: 1280px; margin: 0 auto; padding: 0 var(--sp-5) var(--sp-7); }
  header.doc-header {
    background: linear-gradient(135deg, var(--brand-dark) 0%, var(--brand) 100%);
    color: white;
    padding: var(--sp-8) var(--sp-7) var(--sp-6);
    text-align: center;
    max-width: 1280px;
    margin: var(--sp-5) auto var(--sp-5);
    border-radius: var(--r-xl);
    box-shadow: var(--shadow-brand);
  }
  .eyebrow {
    font-family: var(--font-mono);
    font-size: 0.78em;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: var(--sp-3);
    display: inline-block;
    padding: 4px 14px;
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    backdrop-filter: blur(10px);
  }
  h1 {
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 3em;
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin: 0 0 var(--sp-3);
  }
  h1 em { font-style: italic; color: #fde68a; }
  section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: var(--sp-6) var(--sp-7);
    margin-bottom: var(--sp-5);
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.3s var(--ease);
  }
  section:hover { box-shadow: var(--shadow-md); }
  h2 {
    font-family: var(--font-display);
    font-size: 1.75em;
    font-weight: 800;
    margin: 0 0 var(--sp-5);
    padding-bottom: var(--sp-3);
    border-bottom: 2px solid var(--border);
    color: var(--text);
  }
  pre[class*="language-"] {
    background: #1e1e1e !important;
    border-radius: var(--r-md);
    padding: var(--sp-5) !important;
    margin: var(--sp-4) 0 var(--sp-5);
    font-size: 0.85em !important;
    box-shadow: var(--shadow-md);
  }
  .theme-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2em;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s var(--ease);
    z-index: 1000;
  }
  .theme-toggle:hover {
    transform: scale(1.1);
    box-shadow: var(--shadow-md);
  }
  @media (max-width: 900px) {
    .container { padding: 0 var(--sp-4) var(--sp-6); }
    section { padding: var(--sp-5); }
  }
  @media (max-width: 600px) {
    body { font-size: 15px; }
    h1 { font-size: 2em; }
    section { padding: var(--sp-4); }
  }
  @media print {
    .theme-toggle { display: none; }
    section { break-inside: avoid; }
  }
</style>
</head>
<body>
  <button class="theme-toggle" onclick="toggleTheme()" aria-label="切换深色模式">🌓</button>
  <div class="container">
    <header class="doc-header">
      <span class="eyebrow">Technical Proposal · v1.0</span>
      <h1>Redis 缓存层 · <em>技术方案</em></h1>
    </header>
    <section>
      <h2>背景</h2>
      <p>当前系统直接查询数据库，响应时间 200-500ms，需要优化到 50ms 以内。</p>
    </section>
    <section>
      <h2>方案</h2>
      <p>引入 Redis 作为缓存层，预计提升 8-10 倍性能。</p>
    </section>
  </div>
  <script>
    function toggleTheme() {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
    }
  </script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
</body>
</html>
```

### Example 2: API Documentation with Tabs

[See existing: `docs/llm_prompt_engineering.html`]

### Example 3: Architecture Diagram

[See existing: `docs/redis-cache-proposal.html`]

## Dark Mode Support

All premium HTML documents support dark mode out of the box:

```css
/* Light mode (default) */
:root {
  --bg: #fafaf9;
  --surface: #ffffff;
  --text: #111827;
}

/* Dark mode */
[data-theme="dark"] {
  --bg: #0d1117;
  --surface: #161b22;
  --text: #c9d1d9;
}
```

**Toggle button:**
```html
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">🌓</button>
<script>
function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
}
</script>
```

## Accessibility (WCAG Compliance)

All generated documents must meet WCAG 2.1 AA standards:

### ARIA Labels
```html
<!-- Tab buttons -->
<button class="tab active" data-tab="en" 
        aria-selected="true" 
        aria-controls="tab-en"
        role="tab">English</button>

<!-- Callouts -->
<div class="callout danger" role="alert">
  <div class="callout-title">⚠️ Warning</div>
</div>

<!-- Theme toggle -->
<button aria-label="Toggle dark mode">🌓</button>
```

### Keyboard Navigation
```css
/* Focus indicators */
.tab:focus, button:focus {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

/* Tab navigation */
.tabs {
  display: flex;
  gap: var(--sp-1);
}
.tab:focus-visible {
  outline: 2px solid var(--brand);
}
```

### Color Contrast
- **Normal text**: Minimum 4.5:1 contrast ratio
- **Large text** (18px+ or 14px+ bold): Minimum 3:1
- **UI components**: Minimum 3:1

### Screen Reader Support
```html
<!-- Decorative icons -->
<span aria-hidden="true">🌐</span> English

<!-- Meaningful icons -->
<button aria-label="Search documentation">
  <svg aria-hidden="true">...</svg>
</button>
```

## Custom Brand Colors

Support 5 brand color presets:

```css
/* Emerald (default) */
:root { --brand: #059669; --brand-dark: #047857; }

/* Indigo */
:root { --brand: #4338ca; --brand-dark: #3730a3; }

/* Purple */
:root { --brand: #7c3aed; --brand-dark: #6d28d9; }

/* Sunset */
:root { --brand: #ea580c; --brand-dark: #c2410c; }

/* Ocean */
:root { --brand: #0284c7; --brand-dark: #0369a1; }
```

**Usage:**
```html
<link rel="stylesheet" href="styles-emerald.css">
<!-- or -->
<link rel="stylesheet" href="styles-indigo.css">
```

## Motion System

### Transition Timings
```css
:root {
  --transition-fast: 150ms ease-out;
  --transition-normal: 300ms ease-in-out;
  --transition-slow: 500ms ease-in-out;
}
```

### Hover Effects
```css
/* Cards */
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-fast), 
              box-shadow var(--transition-fast);
}

/* Buttons */
button:hover {
  transform: scale(1.02);
  transition: transform var(--transition-fast);
}

/* Links */
a:hover {
  color: var(--brand);
  transition: color var(--transition-fast);
}
```

### Scroll Animations
```javascript
// Fade in on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('fade-in');
    }
  });
});

document.querySelectorAll('.reveal').forEach(el => {
  observer.observe(el);
});
```

## Extended Responsive Breakpoints

Support 4 breakpoints for all screen sizes:

```css
/* Mobile (< 600px) */
@media (max-width: 600px) {
  body { font-size: 15px; }
  h1 { font-size: 2em; }
  .container { padding: 0 var(--sp-4) var(--sp-6); }
  section { padding: var(--sp-4); }
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
}

/* Tablet (600px - 900px) */
@media (min-width: 601px) and (max-width: 900px) {
  .container { padding: 0 var(--sp-4) var(--sp-6); }
  section { padding: var(--sp-5); }
  .grid-3, .grid-4 { grid-template-columns: 1fr 1fr; }
}

/* Desktop (900px - 1440px) - default */
/* No media query needed */

/* Large Desktop (> 1440px) */
@media (min-width: 1441px) {
  .container { max-width: 1440px; }
  h1 { font-size: 3.5em; }
}

/* Ultra-wide (> 1920px) */
@media (min-width: 1921px) {
  .container { max-width: 1600px; }
  body { font-size: 18px; }
}
```

## Print Styles

Optimize documents for printing:

```css
@media print {
  /* Hide interactive elements */
  .theme-toggle, .tabs, button { display: none; }
  
  /* Optimize for paper */
  body {
    font-size: 12pt;
    color: black;
    background: white;
  }
  
  /* Page breaks */
  section {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  
  h2 {
    break-after: avoid;
    page-break-after: avoid;
  }
  
  /* Links */
  a {
    text-decoration: underline;
    color: black;
  }
  
  a[href^="http"]:after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #666;
  }
  
  /* Images */
  img {
    max-width: 100%;
    page-break-inside: avoid;
  }
  
  /* Page margins */
  @page {
    margin: 2cm;
  }
  
  /* Print-only content */
  .print-only {
    display: block !important;
  }
  
  .no-print {
    display: none !important;
  }
}
```

**Print-only content:**
```html
<div class="print-only" style="display: none;">
  <p>Printed on: <span id="print-date"></span></p>
  <script>
    document.getElementById('print-date').textContent = new Date().toLocaleDateString();
  </script>
</div>
```

## Extended Code Block Languages

Support 15+ programming languages:

```html
<!-- Include Prism.js with all languages -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
```

**Supported languages:**
- Python, JavaScript, TypeScript, SQL, JSON, YAML, TOML
- Bash, Shell, PowerShell
- Go, Rust, Java, C, C++, C#
- HTML, CSS, SCSS
- Markdown, JSX, TSX

**Usage:**
```html
<pre class="code" data-lang="typescript">
<code class="language-typescript">
const greeting: string = "Hello";
console.log(greeting);
</code>
</pre>
```

**Autoloader configuration:**
```html
<script>
Prism.plugins.autoloader.languages_path = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";
</script>
```

## Collapsible Sections (Accordion)

For long documents, use collapsible sections:

```html
<details class="collapsible">
  <summary class="collapsible-header">
    <span class="collapsible-icon">▶</span>
    <span>点击展开详细内容</span>
  </summary>
  <div class="collapsible-content">
    <p>折叠的内容...</p>
  </div>
</details>
```

**CSS:**
```css
.collapsible {
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  margin: var(--sp-4) 0;
  overflow: hidden;
}

.collapsible-header {
  padding: var(--sp-3) var(--sp-4);
  background: var(--surface);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  font-weight: 600;
  transition: background var(--transition-fast);
}

.collapsible-header:hover {
  background: var(--primary-light);
}

.collapsible-icon {
  transition: transform var(--transition-fast);
  font-size: 0.8em;
}

details[open] .collapsible-icon {
  transform: rotate(90deg);
}

.collapsible-content {
  padding: var(--sp-4);
  background: var(--bg);
  border-top: 1px solid var(--border);
}

/* Accessibility */
.collapsible-header:focus {
  outline: 2px solid var(--brand);
  outline-offset: -2px;
}
```

**JavaScript for smooth animation:**
```javascript
document.querySelectorAll('.collapsible').forEach(details => {
  details.addEventListener('toggle', () => {
    const content = details.querySelector('.collapsible-content');
    if (details.open) {
      content.style.maxHeight = content.scrollHeight + 'px';
    } else {
      content.style.maxHeight = '0';
    }
  });
});
```

## Relaxed SVG Rules

### Allowed Patterns

**✅ L-shape paths (simple connections):**
```svg
<path d="M100 100 L100 150 L200 150" stroke="#000" stroke-width="2" fill="none"/>
```

**✅ Bezier curves (complex flows):**
```svg
<!-- Organic flows, S-curves -->
<path d="M100 100 C150 150, 200 50, 250 100" stroke="#000" stroke-width="2" fill="none"/>
```

**✅ Curved arrows (when L-shape is impractical):**
```svg
<path d="M100 100 Q150 150, 200 100" stroke="#000" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
```

**✅ Rounded rectangles:**
```svg
<rect x="50" y="50" width="100" height="80" rx="8" fill="#fff" stroke="#000"/>
```

### Guidelines for Bezier Curves

When using Bezier curves (`C`, `Q`):

1. **Keep control points reasonable**
   ```svg
   <!-- ✓ GOOD: Smooth, natural curve -->
   <path d="M100 100 C150 120, 200 80, 250 100"/>
   
   <!-- ✗ BAD: Extreme control points -->
   <path d="M100 100 C500 500, -200 -200, 250 100"/>
   ```

2. **Use for organic flows, not simple connections**
   ```svg
   <!-- ✓ Use Bezier for: Process flows, timelines -->
   <path d="M50 100 C150 100, 200 150, 300 150"/>
   
   <!-- ✗ Use L-shape for: Simple A→B connections -->
   <path d="M50 100 L150 100 L150 150 L300 150"/>
   ```

3. **Test across browsers**
   ```html
   <!-- Add browser-specific fallbacks if needed -->
   <style>
   @supports not (d: path('M0 0')) {
     /* Fallback for older browsers */
   }
   </style>
   ```

### Arrow Markers

```svg
<defs>
  <!-- Straight arrow -->
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" 
          markerWidth="6" markerHeight="6" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#000"/>
  </marker>
  
  <!-- Curved arrow (for Bezier paths) -->
  <marker id="arrow-curved" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M0,2 L8,5 L0,8 z" fill="#000"/>
  </marker>
</defs>
```

## Diagram-as-Code (Mermaid Integration)

Use Mermaid for flowcharts, sequence diagrams, and more:

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({ 
  startOnLoad: true,
  theme: 'default',
  flowchart: { useMaxWidth: true }
});
</script>
```

**Flowchart:**
```html
<div class="mermaid">
graph TD
    A[用户请求] --> B{缓存命中?}
    B -->|是| C[返回缓存数据]
    B -->|否| D[查询数据库]
    D --> E[写入缓存]
    E --> C
</div>
```

**Sequence Diagram:**
```html
<div class="mermaid">
sequenceDiagram
    participant U as 用户
    participant C as 客户端
    participant R as Redis
    participant D as 数据库
    
    U->>C: 发起请求
    C->>R: 查询缓存
    alt 缓存命中
        R-->>C: 返回数据
    else 缓存未命中
        R-->>C: 未命中
        C->>D: 查询数据库
        D-->>C: 返回数据
        C->>R: 写入缓存
        C-->>U: 返回结果
    end
</div>
```

**Supported diagram types:**
- Flowcharts (graph)
- Sequence diagrams
- Gantt charts
- Class diagrams
- State diagrams
- Entity relationship diagrams
- Pie charts
- Git graphs

## Client-Side Search

Add search functionality for long documents:

```html
<!-- Include FlexSearch -->
<script src="https://cdn.jsdelivr.net/npm/flexsearch@0.7.31/dist/flexsearch.bundle.js"></script>

<!-- Search input -->
<div class="search-container">
  <input type="text" id="search-input" placeholder="搜索文档..." aria-label="搜索">
  <div id="search-results" class="search-results"></div>
</div>
```

**CSS:**
```css
.search-container {
  position: relative;
  max-width: 600px;
  margin: var(--sp-5) auto;
}

#search-input {
  width: 100%;
  padding: var(--sp-3) var(--sp-4);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  font-size: 1em;
  transition: border-color var(--transition-fast);
}

#search-input:focus {
  outline: none;
  border-color: var(--brand);
  box-shadow: 0 0 0 3px var(--brand-soft);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  margin-top: var(--sp-2);
  max-height: 400px;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  display: none;
}

.search-results.active {
  display: block;
}

.search-result-item {
  padding: var(--sp-3) var(--sp-4);
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.search-result-item:hover {
  background: var(--primary-light);
}

.search-result-item:last-child {
  border-bottom: none;
}
```

**JavaScript:**
```javascript
const index = new FlexSearch.Document({
  document: {
    id: 'id',
    index: ['title', 'content']
  }
});

// Index all sections
document.querySelectorAll('section').forEach((section, i) => {
  const title = section.querySelector('h2')?.textContent || '';
  const content = section.textContent;
  index.add({ id: i, title, content });
});

// Search on input
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');

searchInput.addEventListener('input', (e) => {
  const query = e.target.value;
  if (query.length < 2) {
    searchResults.classList.remove('active');
    return;
  }
  
  const results = index.search(query);
  searchResults.innerHTML = results.map(r => {
    const section = document.querySelectorAll('section')[r.id];
    const title = section.querySelector('h2').textContent;
    return `<div class="search-result-item" onclick="scrollToSection(${r.id})">
      <strong>${title}</strong>
      <p>${section.textContent.substring(0, 100)}...</p>
    </div>`;
  }).join('');
  
  searchResults.classList.add('active');
});

function scrollToSection(id) {
  document.querySelectorAll('section')[id].scrollIntoView({ behavior: 'smooth' });
  searchResults.classList.remove('active');
  searchInput.value = '';
}
```

## Form Components

For interactive documentation:

```html
<!-- Text input -->
<div class="form-group">
  <label for="input-name">名称</label>
  <input type="text" id="input-name" class="form-input" placeholder="输入名称">
</div>

<!-- Select -->
<div class="form-group">
  <label for="select-lang">语言</label>
  <select id="select-lang" class="form-select">
    <option value="en">English</option>
    <option value="zh">中文</option>
  </select>
</div>

<!-- Checkbox -->
<div class="form-group">
  <label class="form-checkbox">
    <input type="checkbox">
    <span>启用深色模式</span>
  </label>
</div>
```

**CSS:**
```css
.form-group {
  margin: var(--sp-4) 0;
}

.form-group label {
  display: block;
  margin-bottom: var(--sp-2);
  font-weight: 600;
  color: var(--text);
}

.form-input, .form-select {
  width: 100%;
  padding: var(--sp-2) var(--sp-3);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  font-size: 0.95em;
  transition: border-color var(--transition-fast);
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: var(--brand);
  box-shadow: 0 0 0 3px var(--brand-soft);
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  cursor: pointer;
}

.form-checkbox input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}
```

## PDF Export Guide

### Browser Print (Recommended)

1. Open HTML in browser
2. Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (Mac)
3. Select "Save as PDF" as destination
4. Enable "Background graphics" option
5. Click "Save"

### Print-Optimized CSS

```css
@media print {
  /* Hide interactive elements */
  .theme-toggle, .search-container, .tabs, button, nav {
    display: none !important;
  }
  
  /* Optimize for paper */
  body {
    font-size: 11pt;
    line-height: 1.5;
    color: #000;
    background: #fff;
  }
  
  /* Page setup */
  @page {
    size: A4;
    margin: 2cm;
  }
  
  /* Section breaks */
  section {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  
  h2, h3 {
    break-after: avoid;
    page-break-after: avoid;
  }
  
  /* Links */
  a {
    color: #000;
    text-decoration: underline;
  }
  
  a[href^="http"]:after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #666;
  }
  
  /* Images */
  img {
    max-width: 100%;
    break-inside: avoid;
    page-break-inside: avoid;
  }
  
  /* Code blocks */
  pre {
    font-size: 9pt;
    break-inside: avoid;
    page-break-inside: avoid;
  }
  
  /* Print-only content */
  .print-only {
    display: block !important;
  }
  
  .no-print {
    display: none !important;
  }
}
```

**Print-only footer:**
```html
<div class="print-only" style="display: none; text-align: center; margin-top: 2cm; font-size: 9pt; color: #666;">
  <p>Generated by Premium HTML Studio · <span id="print-date"></span></p>
  <script>
    document.getElementById('print-date').textContent = new Date().toLocaleDateString();
  </script>
</div>
```

## Internationalization (i18n) System

Systematic multi-language support:

```html
<!-- Language switcher -->
<div class="lang-switcher">
  <select id="lang-select" aria-label="选择语言">
    <option value="en">English</option>
    <option value="zh">中文</option>
    <option value="ja">日本語</option>
  </select>
</div>

<!-- Multi-language content -->
<section>
  <h2>
    <span data-lang="en">Background</span>
    <span data-lang="zh" hidden>背景</span>
    <span data-lang="ja" hidden>背景</span>
  </h2>
  <p>
    <span data-lang="en">Current system latency is 200-500ms.</span>
    <span data-lang="zh" hidden>当前系统延迟为 200-500ms。</span>
    <span data-lang="ja" hidden>現在のシステムレイテンシは 200-500ms です。</span>
  </p>
</section>
```

**CSS:**
```css
.lang-switcher {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
}

#lang-select {
  padding: var(--sp-2) var(--sp-3);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  background: var(--surface);
  cursor: pointer;
}

[data-lang] {
  display: none;
}

[data-lang].active {
  display: inline;
}
```

**JavaScript:**
```javascript
const langSelect = document.getElementById('lang-select');

function switchLanguage(lang) {
  // Hide all languages
  document.querySelectorAll('[data-lang]').forEach(el => {
    el.classList.remove('active');
    el.hidden = true;
  });
  
  // Show selected language
  document.querySelectorAll(`[data-lang="${lang}"]`).forEach(el => {
    el.classList.add('active');
    el.hidden = false;
  });
  
  // Save preference
  localStorage.setItem('preferred-lang', lang);
}

langSelect.addEventListener('change', (e) => {
  switchLanguage(e.target.value);
});

// Load saved preference
const savedLang = localStorage.getItem('preferred-lang') || 'en';
langSelect.value = savedLang;
switchLanguage(savedLang);
```

## Code Diff Component

Show code changes:

```html
<div class="code-diff">
  <div class="diff-header">
    <span class="diff-file">config.py</span>
    <span class="diff-stats">+3 -1</span>
  </div>
  <div class="diff-content">
    <div class="diff-line diff-old">
      <span class="diff-line-num">-</span>
      <code>timeout = 30</code>
    </div>
    <div class="diff-line diff-new">
      <span class="diff-line-num">+</span>
      <code>timeout = 60</code>
    </div>
    <div class="diff-line diff-context">
      <span class="diff-line-num"> </span>
      <code>retries = 3</code>
    </div>
  </div>
</div>
```

**CSS:**
```css
.code-diff {
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  overflow: hidden;
  font-family: var(--font-mono);
  font-size: 0.85em;
  margin: var(--sp-4) 0;
}

.diff-header {
  background: var(--surface);
  padding: var(--sp-2) var(--sp-3);
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.diff-file {
  font-weight: 600;
}

.diff-stats {
  font-size: 0.85em;
}

.diff-stats::before {
  content: "+";
  color: var(--success);
}

.diff-stats::after {
  content: " -";
  color: var(--danger);
}

.diff-content {
  background: var(--bg);
}

.diff-line {
  padding: 2px var(--sp-3);
  display: flex;
  gap: var(--sp-2);
}

.diff-line-num {
  width: 20px;
  text-align: right;
  user-select: none;
  opacity: 0.5;
}

.diff-old {
  background: var(--danger-light);
  color: var(--danger);
}

.diff-new {
  background: var(--success-light);
  color: var(--success);
}

.diff-context {
  color: var(--text-muted);
}
```

## Performance Guidelines

### Image Optimization

```html
<!-- Responsive images -->
<img src="image-800.webp" 
     srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
     sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
     alt="Description"
     loading="lazy"
     decoding="async">
```

### Code Splitting

```html
<!-- Defer non-critical CSS -->
<link rel="preload" href="critical.css" as="style">
<link rel="stylesheet" href="critical.css">
<link rel="stylesheet" href="non-critical.css" media="print" onload="this.media='all'">

<!-- Async JavaScript -->
<script src="analytics.js" async></script>
<script src="interactive.js" defer></script>
```

### Lazy Loading

```html
<!-- Lazy load images -->
<img loading="lazy" src="image.jpg" alt="...">

<!-- Lazy load iframes -->
<iframe loading="lazy" src="video.html"></iframe>

<!-- Lazy load sections -->
<section id="heavy-content" data-lazy="true">
  <!-- Content loaded on scroll -->
</section>
```

## SEO Guidelines

### Meta Tags

```html
<head>
  <title>OceanBase Full Mode Technical Guide</title>
  <meta name="description" content="Complete guide to OceanBase full mode implementation">
  <meta name="keywords" content="OceanBase, full mode, technical guide">
  
  <!-- Open Graph -->
  <meta property="og:title" content="OceanBase Full Mode">
  <meta property="og:description" content="Complete technical guide">
  <meta property="og:image" content="https://example.com/preview.png">
  <meta property="og:url" content="https://example.com/guide">
  <meta property="og:type" content="article">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="OceanBase Full Mode">
  <meta name="twitter:description" content="Complete technical guide">
  <meta name="twitter:image" content="https://example.com/preview.png">
  
  <!-- Canonical -->
  <link rel="canonical" href="https://example.com/guide">
</head>
```

### Structured Data

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "OceanBase Full Mode Technical Guide",
  "description": "Complete guide to implementation",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2026-07-14",
  "dateModified": "2026-07-14"
}
</script>
```

## Simplified Tab System

Use native HTML `<details>` for simple tabs:

```html
<details class="tab-simple" open>
  <summary>English</summary>
  <div class="tab-content-simple">English content</div>
</details>

<details class="tab-simple">
  <summary>中文</summary>
  <div class="tab-content-simple">中文内容</div>
</details>
```

**CSS (only one open at a time):**
```css
.tab-simple {
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  margin: var(--sp-2) 0;
}

.tab-simple summary {
  padding: var(--sp-2) var(--sp-3);
  cursor: pointer;
  font-weight: 600;
  list-style: none;
}

.tab-simple summary::-webkit-details-marker {
  display: none;
}

.tab-content-simple {
  padding: var(--sp-3);
  border-top: 1px solid var(--border);
}

/* Close others when one opens */
.tab-simple[open] ~ .tab-simple {
  /* JavaScript needed for mutual exclusion */
}
```

**JavaScript for mutual exclusion:**
```javascript
document.querySelectorAll('.tab-simple').forEach(details => {
  details.addEventListener('toggle', () => {
    if (details.open) {
      document.querySelectorAll('.tab-simple').forEach(other => {
        if (other !== details) other.open = false;
      });
    }
  });
});
```

## Flexible Layout Options

### Layout 1: Standard (Default)

```
┌─────────────────────────────────┐
│ Header                          │
├─────────────────────────────────┤
│ TOC                             │
├─────────────────────────────────┤
│ Section 1                       │
├─────────────────────────────────┤
│ Section 2                       │
└─────────────────────────────────┘
```

### Layout 2: Minimal (No TOC)

```html
<body>
  <header class="doc-header">...</header>
  <div class="container">
    <section>...</section>
    <section>...</section>
  </div>
</body>
```

### Layout 3: Landing Page

```html
<body>
  <!-- Hero section -->
  <section class="hero">
    <h1>Product Name</h1>
    <p>Tagline</p>
    <a href="#features" class="btn">Learn More</a>
  </section>
  
  <!-- Features -->
  <section id="features">
    <h2>Features</h2>
    <div class="grid-3">
      <div class="card">...</div>
      <div class="card">...</div>
      <div class="card">...</div>
    </div>
  </section>
  
  <!-- CTA -->
  <section class="cta">
    <h2>Get Started</h2>
    <a href="#" class="btn">Sign Up</a>
  </section>
</body>
```

**Hero CSS:**
```css
.hero {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: linear-gradient(135deg, var(--brand-dark), var(--brand));
  color: white;
}

.hero h1 {
  font-size: 4em;
  margin-bottom: var(--sp-4);
}

.btn {
  display: inline-block;
  padding: var(--sp-3) var(--sp-6);
  background: white;
  color: var(--brand);
  border-radius: var(--r-md);
  text-decoration: none;
  font-weight: 600;
  transition: transform var(--transition-fast);
}

.btn:hover {
  transform: translateY(-2px);
}
```

## Content Types

This skill supports two primary content categories:

### 1. Documentation (文档)
- **Technical deep-dives** — 算法/架构/流程详解
- **API documentation** — 接口说明、参数详解、示例代码
- **Architecture explanations** — 系统架构、数据流、模块关系
- **Workflow analysis** — 业务流程、决策树、状态机
- **Performance reports** — 基准测试、性能对比、优化建议

### 2. Proposals (方案)
- **Technical proposals (技术方案)** — 技术选型、实现路径、风险评估
- **Project plans (项目方案)** — 目标、里程碑、资源、时间线
- **Architecture proposals (架构方案)** — 系统设计、组件关系、扩展性
- **Design proposals (设计方案)** — 交互流程、视觉风格、用户体验
- **Implementation plans (实施方案)** — 分阶段部署、依赖关系、验收标准
- **Research reports (研究报告)** — 调研结果、对比分析、结论建议

## Proposal Structure Template

When generating a proposal, use this structural template:

```
┌─────────────────────────────────────────────────────────────────────┐
│  Header: 方案标题 · 日期 · 作者/团队                                 │
│  [eyebrow] PROJECT · TYPE · STATUS                                  │
└─────────────────────────────────────────────────────────────────────┘
┌─ Executive Summary (执行摘要) ─────────────────────────────────────┐
│  背景 · 目标 · 核心结论（3-5 个要点，卡片式布局）                    │
└────────────────────────────────────────────────────────────────────┘
┌─ Background (背景分析) ────────────────────────────────────────────┐
│  现状 · 问题 · 机会 · 数据支撑（SVG 流程图）                         │
└────────────────────────────────────────────────────────────────────┘
┌─ Objectives (目标与指标) ──────────────────────────────────────────┐
│  SMART 目标 · KPIs · 成功标准（表格 + 徽章标记优先级）               │
└────────────────────────────────────────────────────────────────────┘
┌─ Approach (方案概述) ──────────────────────────────────────────────┐
│  总体思路 · 核心策略 · 关键决策（SVG 架构图 + 分栏卡片）             │
└────────────────────────────────────────────────────────────────────┘
┌─ Implementation (实施计划) ────────────────────────────────────────┐
│  分阶段计划 · 里程碑 · 时间线（SVG 甘特图/时间线）                   │
└────────────────────────────────────────────────────────────────────┘
┌─ Resources (资源需求) ─────────────────────────────────────────────┐
│  团队 · 预算 · 工具 · 依赖（表格 + 成本汇总）                        │
└────────────────────────────────────────────────────────────────────┘
┌─ Risks & Mitigation (风险与应对) ──────────────────────────────────┐
│  风险清单 · 概率 · 影响 · 应对策略（callout + 表格）                 │
└────────────────────────────────────────────────────────────────────┘
┌─ Alternatives (备选方案) ──────────────────────────────────────────┐
│  对比分析 · 推荐方案 · 决策依据（对比表格 + SVG 决策树）             │
└────────────────────────────────────────────────────────────────────┘
┌─ Conclusion (结论与下一步) ────────────────────────────────────────┐
│  总结 · 审批请求 · 后续行动 · 联系信息                              │
└────────────────────────────────────────────────────────────────────┘
```

## Proposal-Specific Components

### Executive Summary Card Grid
```html
<div class="grid-4">
  <div class="stat-card">
    <div class="num">3</div>
    <div class="label">核心目标</div>
  </div>
  <div class="stat-card">
    <div class="num">Q3</div>
    <div class="label">启动时间</div>
  </div>
  <div class="stat-card">
    <div class="num">6mo</div>
    <div class="label">实施周期</div>
  </div>
  <div class="stat-card">
    <div class="num">¥2M</div>
    <div class="label">总预算</div>
  </div>
</div>
```

### Phase Timeline (SVG)
```svg
<!-- Timeline arrow with phase markers -->
<line x1="100" y1="500" x2="1100" y2="500"
      stroke="url(#g-arrow)" stroke-width="3"/>
<!-- Phase markers -->
<g>
  <circle cx="200" cy="500" r="8" fill="url(#g-brand)"/>
  <text x="200" y="530" text-anchor="middle" class="mono" font-size="11">
    Phase 1
  </text>
  <text x="200" y="548" text-anchor="middle" class="body" font-size="10" fill="#6b7280">
    调研 · 1mo
  </text>
</g>
```

### Risk Matrix Callouts
```html
<div class="callout danger">
  <div class="callout-title">⚠️ 高风险：数据迁移失败</div>
  概率：中 · 影响：高<br>
  <strong>应对策略：</strong>分批次灰度迁移，保留回滚能力
</div>
```

### Comparison Table (Alternatives)
```html
<table class="fields">
  <thead>
    <tr>
      <th>维度</th>
      <th>方案 A</th>
      <th class="hl">方案 B (推荐)</th>
      <th>方案 C</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>实施成本</td><td>¥1.5M</td><td>¥2M</td><td>¥3M</td></tr>
    <tr><td>实施周期</td><td>9mo</td><td>6mo</td><td>4mo</td></tr>
  </tbody>
</table>
```

### Status Badge System
```html
<span class="badge" style="background:#059669;">已批准</span>
<span class="badge" style="background:#d97706;">待审批</span>
<span class="badge" style="background:#dc2626;">已拒绝</span>
<span class="badge" style="background:#6b7280;">已归档</span>
```

## Documentation vs Proposal Decision Guide

| Signal | Generate |
|--------|----------|
| 用户提到"文档/说明/介绍/流程" | Documentation |
| 用户提到"方案/计划/提案/建议" | Proposal |
| 用户给出完整内容要求呈现 | Documentation |
| 用户描述问题并要求解决思路 | Proposal |
| 用户需要对比多个选项 | Proposal (with alternatives) |
| 用户需要详细解释现有系统 | Documentation |

**Mixed content**: If the request contains both elements, combine them — e.g., a technical proposal with architecture documentation sections.


## Chinese Technical Spec Style (中文技术规格 · Multi-ES 风格)

A second design system distilled from the reference document **《Multi-ES Precise 模式流程详解》** — the house style for Chinese technical deep-dives that walk through a pipeline, an algorithm flow, or a system's internals node by node (流程详解 / 模式详解 / 链路图 / 节点拆解 / 参数说明).

**Choose this style when**: the doc is in Chinese AND explains a process/flow — a retrieval pipeline, an LLM chain, a multi-stage algorithm, a system workflow — with stages, steps, parameters and thresholds to document. Choose the International style (below) for English docs, API references, or content that is mostly prose rather than flow.

Full CSS lives in **`templates/css-system-cn.css`** — copy it into the `<style>` block and customize `--purple`/`--blue` accents if you want a different hue. The core shapes (cover hero, part dividers, vertical flow, funnel) are what give the style its identity; keep them intact.

### Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

| Role | Font | Usage |
|------|------|-------|
| Body / UI | `Noto Sans SC` (300–700) | Paragraphs, lists, tables, callouts — CJK-optimized metrics |
| Headings / Display | `Noto Serif SC` (400/600/700) | Cover H1, part titles, `h2.sec` — serif gives 中文文档 gravitas |
| Code / Technical | `JetBrains Mono` (400/500) | Inline code, pre blocks, KPIs, numbers, badges |

### Palette (semantic families)

Six accent families, each with a base + light tint used for bars, callouts, stage tags and badges:

```css
--blue:#2563eb; --blt2:#dbeafe;      /* 召回/入口 */
--purple:#7c3aed; --plt:#ede9fe;     /* 增强/扩展 + 主强调色 */
--teal:#0891b2; --tlt:#cffafe;       /* 存储/DB */
--green:#059669; --glt:#d1fae5;      /* 输出/成功 */
--amber:#d97706; --alt:#fef3c7;      /* LLM 调用点 / 警告 */
--red:#dc2626; --rlt:#fee2e2;        /* 错误 / 易错点 */
```

Plus 4-level text scale `--text:#1a1a2e → --text2 → --text3 → --text4` and surfaces `--bgsub:#f8f9fc` / `--border:#e2e6ef`. Page background is a light gray-blue gradient (`#eef1f7 → #e8ecf4`) so the white `.doc` card floats on top.

### Layout skeleton

```
┌─ .doc (1200px white card, layered shadow) ─────────────────┐
│ ┌─ .cover ── dark purple gradient hero ─────────────────┐ │
│ │  [.tag pill]  h1(serif)  .sub  .meta  .kpis(4 个数字) │ │
│ └──────────────────────────────────────────────────────┘ │
│ ┌─ .body ──────────────────────────────────────────────┐ │
│ │  .exec 管理摘要 (紫色左边条渐变卡)                      │ │
│ │  .toc 分部分卡片网格 (Part 01 … 06)                    │ │
│ │  .part 分隔条 + h2.sec 小节 + h3.sub + p.lead          │ │
│ │  .flow 纵向流程 / .funnel 数据漏斗 / 表格 / callout     │ │
│ │  .footer                                              │ │
│ └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### Cover hero (with KPIs)

The cover is a **155deg dark-purple gradient** (`#1a0a2e → #2d1440 → #4a0d5e → #5b0e7d`) with two radial glow circles (`::before`/`::after`) — the glow is what keeps it from looking flat. Layout: eyebrow `.tag` pill → serif `h1` → `.sub` one-line subtitle → `.meta` version/module lines with `<b>` labels → `.kpis` row of mono numbers.

```html
<div class="cover">
  <span class="tag">Technical Spec · SAG-Benchmark</span>
  <h1>Multi-ES Precise 模式流程详解</h1>
  <p class="sub">高精度 LLM 精选的多元事项检索链路 — 一句话副标题</p>
  <div class="meta">
    <b>版本：</b>v1.0 — 2026 年 7 月<br>
    <b>模块：</b>pipeline/modules/search/multi_vector.py<br>
    <b>定位：</b>链路设计、阈值与机制说明
  </div>
  <div class="kpis">
    <div class="kpi"><div class="v">1</div><div class="l">LLM 调用次数</div></div>
    <div class="kpi"><div class="v">2</div><div class="l">召回通道</div></div>
    <div class="kpi"><div class="v">8</div><div class="l">链路节点</div></div>
  </div>
</div>
```

### Part dividers & section headings

Long specs are split into **numbered Parts** — a `Part 01`-style divider with a 3px top rule and serif title, then `h2.sec` sub-sections each with a 48px purple underline accent, `h3.sub` for sub-points, and `p.lead` for gray intro paragraphs:

```html
<div class="part" id="p1">
  <span class="num">Part 01</span>
  <div class="title">链路全景图</div>
</div>
<h2 class="sec">数据流量漏斗</h2>
<h3 class="sub">① 召回控制参数</h3>
<p class="lead">Precise 模式的行为由 … 控制。</p>
```

### Executive summary

A purple-left-border gradient box right after the cover, summarizing the whole chain in 2–3 paragraphs with inline `<code>` and `<b>` emphasis:

```html
<div class="exec">
  <h2>管理摘要</h2>
  <p>链路概要：<b>Step1</b> BM25 实体召回 → <b>Step2</b> … → <b>Step8</b> 获取 Chunk。</p>
</div>
```

### Vertical flow (the signature component)

This is the component that makes 流程详解 docs read like a pipeline. A `.flow` is a column of `.fnode`s; each node = a 5px colored `.fbar` + a `.fcard` with four fields — `.fn` (STEP label), `.ft` (bold title, usually the param name), `.fd` (description, may include `<code>`/`<br>`), `.fb` (output pill with `<b>` value). Nodes are joined by `.arrow` rows carrying ▼ and optional `.badge` count pills. Group stages under `.stage-tag` pills (st1 blue / st2 purple / st3 green).

```html
<span class="stage-tag st1">阶段一 · 召回</span>
<div class="flow">
  <div class="fnode"><div class="fbar" style="background:var(--blue)"></div>
    <div class="fcard">
      <div class="fn">STEP 1 · BM25 实体召回</div>
      <div class="ft">entity_top_k = 20</div>
      <div class="fd">ES 全文检索 · 按原始分排序截断，<b>无相似度阈值</b>。</div>
      <div class="fb">输出 ≤ <b>20</b> 实体</div>
    </div>
  </div>
  <div class="arrow">▼ <span class="badge">20 实体</span></div>
  <div class="fnode"><div class="fbar" style="background:var(--green)"></div>
    <div class="fcard">
      <div class="fn">STEP 6 · 向量粗排</div>
      <div class="ft">max_events = 100</div>
      <div class="fd">kNN + <code>event_ids</code> 精确过滤，按相似度降序截断。</div>
      <div class="fb">输出 ≤ <b>100</b> 候选</div>
    </div>
  </div>
</div>
```

**Bar color semantics** (keep consistent across the doc): `--blue` = 召回/入口, `--purple` = 增强/扩展, `--green` = 精选/输出, `--amber` = LLM 调用点, `--teal` = 存储/MySQL. Explain the mapping once in a `.legend` (swatch + label) below the flow:

```html
<div class="legend">
  <span class="lg"><span class="sw" style="background:var(--blue)"></span>召回节点</span>
  <span class="lg"><span class="sw" style="background:var(--amber)"></span>LLM 调用点</span>
</div>
```

### Funnel (data-flow sizing)

When the doc tracks how candidate counts shrink through stages (20 → 40 → ≤100 → ≤10), use a `.funnel`: each row = right-aligned `.fstep` label + a width-encoded `.fbar2` bar (width % ≈ relative volume, color = stage family) + `.fnote` annotation. This makes capacity/throughput readable at a glance.

```html
<div class="funnel">
  <div class="frow"><div class="fstep">BM25 实体</div><div class="fbar2" style="width:18%;background:var(--blue)">20</div><div class="fnote">Step1</div></div>
  <div class="frow"><div class="fstep">LLM 精选</div><div class="fbar2" style="width:14%;background:var(--amber)">≤10</div><div class="fnote">Step7</div></div>
</div>
```

### Callouts, tables, code

- **Callouts** — four tinted semantics, full-border + tinted background (NOT left-bar gradient like the International style): `.callout.info` (teal, 细节), `.callout.warn` (amber, 提示/注意), `.callout.err` (red, 易错点), `.callout.ok` (green, 测试清单/结论). Put 易错点 lists in `.err` with numbered `<br>`-separated lines.
- **Tables** — plain `<table>` (no `class`), `th` on `--bgsub` with `white-space:nowrap`, zebra rows via `tr:nth-child(even)`. First column is often a `<code>` param name.
- **Code** — inline `code` is purple text on `--bgsub`; block `pre` is **dark** `#0f1220` with colored spans `.c` (comment `#5b6080`), `.k` (keyword `#c792ea`), `.s` (string `#a5d6a7`), `.n` (number `#82aaff`). Highlight code comments with `<span class="c">` and keywords with `<span class="k">`.
- **Collapsibles** — use `<details open><summary>…</summary>…</details>` for long prompt texts / full source excerpts; summary is bold `13.5px`.
- **Feature grid** — `.feature-grid` of `.feature` cards (`.ic` emoji + `.t` title + `.d` description) for "特点/能力" sections.

### Footer & doc identity

Close with `.footer` — centered, faint gray, `<b>` for the doc name, a `<br>` for related-doc links.

### Style decision table

| Doc type | Style | Reason |
|----------|-------|--------|
| 中文流程详解 / 模式详解 / 链路图 / 节点拆解 / 参数表 | **Chinese Technical Spec** | Noto SC fonts + flow/funnel components are built for CJK pipeline docs |
| English doc / API reference / prose-heavy | International | Playfair/Inter system |
| 中文方案 / 提案 (proposal without flow) | International (purple) | Proposal structure components live there |
| Chinese research report with data & tables | Either — prefer CN style if it has a pipeline, else International | — |

## Core Design System

### Typography

Always use this three-font system for maximum polish:

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400;1,700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

| Role | Font | Usage |
|------|------|-------|
| Display / Headings | `Playfair Display` (800 weight, -0.02em letter-spacing) | Page titles, section headers, emphasis words |
| Body / UI | `Inter` (400/500/600/700) | Paragraphs, lists, labels, metadata |
| Code / Technical | `JetBrains Mono` (500/600) | Inline code, code blocks, badges, tags, numbers |

Chinese fallback chain: `'PingFang SC', 'Microsoft YaHei', -apple-system, sans-serif`

### Color Palettes

Two brand palettes — pick one based on the topic:

**Indigo (technical, analytical, professional):**
```css
--brand-dark: #1e3a8a;
--brand: #4338ca;
--brand-light: #e0e7ff;
--brand-soft: #eef2ff;
```
Use for: fast mode, performance analysis, data flows, architecture

**Purple (creative, refined, premium):**
```css
--brand-dark: #5b21b6;
--brand: #7c3aed;
--brand-light: #ede9fe;
--brand-soft: #f5f3ff;
```
Use for: precise mode, LLM content, design topics, methodology

**LLM / Emphasis accent (when LLM is involved):**
```css
--accent-llm: #be185d;  /* rose */
--accent-llm-light: #fce7f3;
```

**Semantic colors (always include):**
```css
--success: #059669;     --success-light: #d1fae5;
--warning: #d97706;     --warning-light: #fef3c7;
--danger: #dc2626;      --danger-light: #fee2e2;
--info: #0284c7;        --info-light: #e0f2fe;
```

**Surfaces:**
```css
--bg: #fafaf9;
--surface: #ffffff;
--surface-raised: #fcfcfc;
--border: #e5e7eb;
--border-strong: #d1d5db;
--text: #111827;
--text-secondary: #374151;
--text-muted: #6b7280;
--text-faint: #9ca3af;
```

### Spacing Rhythm

Always use the 8px-based scale:
```css
--sp-1: 4px;   --sp-2: 8px;   --sp-3: 12px;  --sp-4: 16px;
--sp-5: 24px;  --sp-6: 32px;  --sp-7: 48px;  --sp-8: 64px;
```

### Border Radius
```css
--r-sm: 6px;   --r-md: 10px;  --r-lg: 14px;  --r-xl: 20px;
```

### Layered Shadows
```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
--shadow-md: 0 4px 12px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
--shadow-lg: 0 12px 32px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
--shadow-xl: 0 24px 48px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.06);
--shadow-brand: 0 8px 24px rgba(BRAND_RGB, 0.20), 0 2px 8px rgba(BRAND_RGB, 0.10);
```

## Layout Structure

Every page uses three aligned sections at 1280px max-width:

```
┌────────── Header (1280px, rounded 20px, gradient bg) ──────────┐
│  [eyebrow label]                                                │
│  Page Title · <em>Emphasis Word</em>                            │
│  Subtitle text                                                  │
│  📅 Date · 📦 Project · 🔖 Config                               │
└─────────────────────────────────────────────────────────────────┘
┌────────── TOC (1280px, rounded 14px, left brand bar) ──────────┐
│  ● Chapter 1                                                    │
│  ● Chapter 2                                                    │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
┌────────── Section 1 (1280px, rounded 14px) ────────────────────┐
│  ## Title with <em>emphasis</em>                                │
│  Content...                                                     │
└─────────────────────────────────────────────────────────────────┘
```

Key rules:
- **All elements share 1280px max-width** — no wider, no narrower
- **20px gaps** between header → TOC → sections
- **Hover shadow lift** on sections: `--shadow-sm` → `--shadow-md`
- **Header** gets `--shadow-brand` (colored shadow matching brand)
- **Body background** has subtle radial gradients for atmosphere

### Header Template

```html
<header class="doc-header">
  <div class="header-inner">
    <span class="eyebrow">CATEGORY · SERIES</span>
    <h1>Title · <em>emphasis</em> word</h1>
    <div class="subtitle">Descriptive subtitle</div>
    <div class="meta">
      <span>📅 2026-07-14</span>
      <span>•</span>
      <span>📦 Project-Name</span>
      <span>•</span>
      <span>🔖 <code>key = "value"</code></span>
    </div>
  </div>
</header>
```

The `eyebrow` is a frosted pill badge with mono font, uppercase, 0.25em letter-spacing.

### TOC Template

Use `nav.toc` with an `::before` left brand-gradient bar. Two-column `columns: 2` for link list. Each link has a dot (`::before`) that scales on hover. **Must set `list-style: none` on `nav.toc ol`** — since dots come from `a::before`, default `<ol>` numbers would create ugly double markers (e.g. "1. ● Chapter 1").

## Components

### Tab Switching (Parallel Content)

For parallel content that should be shown one at a time (e.g., language versions, multiple examples), use tab-based switching:

```html
<!-- Tab bar -->
<div class="tabs" data-group="unique-group-name">
  <button class="tab active" data-tab="option1">选项 1</button>
  <button class="tab" data-tab="option2">选项 2</button>
</div>

<!-- Tab content panels -->
<div class="tab-content active" data-group="unique-group-name" data-tab="option1">
  选项 1 的内容
</div>
<div class="tab-content" data-group="unique-group-name" data-tab="option2">
  选项 2 的内容
</div>
```

**CSS (include in `<style>`):**
```css
.tabs {
  display: flex;
  gap: var(--sp-1);
  border-bottom: 2px solid var(--border);
  margin-bottom: var(--sp-4);
}
.tab {
  padding: var(--sp-2) var(--sp-4);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  cursor: pointer;
  font-family: var(--font-mono);
  font-size: 0.85em;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.2s var(--ease);
}
.tab:hover { color: var(--brand); }
.tab.active {
  color: var(--brand);
  border-bottom-color: var(--brand);
}
.tab-content { display: none; }
.tab-content.active { display: block; }
```

**JavaScript (include before `</body>`):**
```javascript
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.tabs').forEach(function(tabBar) {
    const tabs = tabBar.querySelectorAll('.tab');
    const tabGroup = tabBar.dataset.group;
    const contents = document.querySelectorAll(`.tab-content[data-group="${tabGroup}"]`);

    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        const target = tab.dataset.tab;
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        contents.forEach(c => c.classList.remove('active'));
        const targetContent = document.querySelector(`.tab-content[data-group="${tabGroup}"][data-tab="${target}"]`);
        if (targetContent) targetContent.classList.add('active');
      });
    });
  });
});
```

**Use cases:**
- **Language switching**: EN / 中文 / 日本語
- **Multiple examples**: 示例 1 / 示例 2 / 示例 3
- **Nested tabs**: Example tabs containing language tabs
- **Version switching**: v1.0 / v2.0 / v3.0

**Nested Tab Isolation (CRITICAL):**

When nesting tabs (e.g., language tabs inside example tabs), follow these rules:

```html
<!-- ✓ CORRECT: Each nesting level has unique data-group -->
<div class="tab-content" data-group="examples" data-tab="ex1">
  <div class="tabs" data-group="example1-lang">  <!-- Unique group name -->
    <button class="tab active" data-tab="en">EN</button>
    <button class="tab" data-tab="zh">中文</button>
  </div>
  <div class="tab-content active" data-group="example1-lang" data-tab="en">
    English content
  </div>
  <div class="tab-content" data-group="example1-lang" data-tab="zh">
    Chinese content
  </div>
</div>

<div class="tab-content" data-group="examples" data-tab="ex2">
  <div class="tabs" data-group="example2-lang">  <!-- Different group name -->
    <button class="tab active" data-tab="en">EN</button>
    <button class="tab" data-tab="zh">中文</button>
  </div>
  <div class="tab-content active" data-group="example2-lang" data-tab="en">
    English content
  </div>
  <div class="tab-content" data-group="example2-lang" data-tab="zh">
    Chinese content
  </div>
</div>
```

**✗ WRONG: Shared data-group across nesting levels:**
```html
<div class="tab-content" data-group="examples" data-tab="ex1">
  <div class="tabs" data-group="lang">  <!-- ❌ Same group name -->
    ...
  </div>
</div>
<div class="tab-content" data-group="examples" data-tab="ex2">
  <div class="tabs" data-group="lang">  <!-- ❌ Conflicts with ex1's lang tabs -->
    ...
  </div>
</div>
```

**No Orphaned Content:**
- ✅ ALL content must be inside `tab-content` divs
- ✅ Close each `tab-content` before starting the next one
- ❌ Never leave standalone elements (h4, pre, etc.) between tab groups
- ❌ Never have content outside tab-content that should be tab-controlled

**JavaScript Scope Isolation:**

The JavaScript MUST use `:scope >` to select only direct children, preventing cross-tab contamination:

```javascript
// ✓ CORRECT: Scoped to parent element
const parentContainer = tabBar.parentElement;
const contents = parentContainer.querySelectorAll(`:scope > .tab-content[data-group="${tabGroup}"]`);

// ✗ WRONG: Selects ALL matching elements in document
const contents = document.querySelectorAll(`.tab-content[data-group="${tabGroup}"]`);
```

**Rules:**
- ✅ Each tab group needs a unique `data-group` name
- ✅ Nested tabs must have DIFFERENT `data-group` names at each level
- ✅ First tab and first content should have `class="active"`
- ✅ Tab buttons use `data-tab` to link to content
- ✅ Content panels use `data-group` + `data-tab` for matching
- ✅ Use `:scope >` in JavaScript to scope selection to parent
- ✅ Close all `tab-content` divs properly before starting next group
- ✅ No orphaned content between tab groups
- ❌ Never reuse `data-group` names across nesting levels
- ❌ Never use `document.querySelectorAll` for tab-content (use scoped selection)
- ❌ Never hardcode visibility — always use JavaScript to toggle `.active`
- ❌ Never leave content outside `tab-content` that should be controlled by tabs

### Code Blocks (with Prism.js)

Include Prism CDN:
```html
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
```

Code blocks must have:
1. **Dark background**: `#0f172a` (slate-900) — not pure black
2. **Traffic-light dots** top-left: `::after { content: '● ● ●'; }` in red/orange/green
3. **Language label** top-right: `::before { content: attr(data-lang); }` uppercase mono
4. **`data-lang` attribute** on the `<code>` element (e.g., `<code class="language-python" data-lang="python">`)
5. **Layered shadow**: `--shadow-lg`

```html
<pre class="code" data-lang="python"><code class="language-python">def hello():
    print("world")
</code></pre>
```

### Cards

```html
<div class="card">
  <h5>Card Title</h5>
  <p>Card description text</p>
</div>
```

Cards have:
- `--r-md` border radius
- `--shadow-sm` default, `--shadow-md` on hover
- `-2px translateY` lift on hover

### Callouts

```html
<div class="callout">          <!-- brand color -->
<div class="callout warning">  <!-- yellow -->
<div class="callout success">  <!-- green -->
<div class="callout danger">   <!-- red -->
<div class="callout llm">      <!-- rose pink, for LLM content -->
```

Left border 4px + gradient background fading to transparent (90deg).

### Badges & Tags

```html
<span class="badge badge-brand">BRAND</span>
<span class="badge badge-llm">LLM</span>
<span class="tag tag-query">query</span>
```

Badges: `--r-20` pill, mono font, 0.7em size, 600 weight
Tags: `--r-sm` rectangle, mono font, 0.72em size

### Tables

```html
<table class="fields">
  <thead><tr><th>Column 1</th><th>Column 2</th></tr></thead>
  <tbody>
    <tr><td><code>key</code></td><td>value</td></tr>
    <tr class="hl"><td>highlighted row</td><td>...</td></tr>
  </tbody>
</table>
```

Tables have:
- Outer border + `--r-md` radius + `overflow: hidden`
- Gradient header background (white → gray)
- Mono font in first column (technical field names)
- Row hover highlight with brand-soft background
- `.hl` class for red-tinted emphasis rows

## SVG Diagrams

For flow diagrams and architecture visuals, create inline SVG with:

### Font Setup
```svg
<defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');
    .title { font-family: 'Playfair Display', Georgia, serif; font-weight: 800; }
    .body { font-family: 'Inter', -apple-system, sans-serif; }
    .mono { font-family: 'JetBrains Mono', monospace; font-weight: 600; }
  </style>
</defs>
```

**Important:** Use raw `&` in CSS URLs inside `<style>` blocks (NOT `&amp;`). The `&amp;` HTML entity encoding is only needed in HTML attributes and text content, not inside `<style>` tags (including those embedded in SVG). This applies to both parent HTML and embedded SVGs.

### Brand Color Gradients
```svg
<linearGradient id="g-brand" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#3730a3"/>
  <stop offset="50%" stop-color="#4338ca"/>
  <stop offset="100%" stop-color="#6366f1"/>
</linearGradient>
```

Use 3-stop gradients for richness. For precise mode, shift to purple (#5b21b6 → #7c3aed → #8b5cf6).

### Layered Shadow Filters
```svg
<filter id="shadow-soft" x="-20%" y="-20%" width="140%" height="160%">
  <feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#1e3a8a" flood-opacity="0.08"/>
  <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#1e3a8a" flood-opacity="0.10"/>
  <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#1e3a8a" flood-opacity="0.06"/>
</filter>
<filter id="shadow-glow" x="-30%" y="-30%" width="160%" height="180%">
  <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#4338ca" flood-opacity="0.35"/>
</filter>
```

Three-layer shadow = realistic depth. Glow filter for important/emphasis nodes.

### Card Template
```svg
<g filter="url(#shadow-soft)">
  <rect x="..." y="..." width="..." height="..." rx="12"
        fill="url(#g-brand-card)" stroke="#c7d2fe" stroke-width="1"/>

  <!-- ⚠️ CRITICAL: Use SINGLE <path> for title bar — NEVER two stacked <rect> -->
  <!-- Two stacked rects create a visible seam line at their boundary -->
  <!-- Path formula for top-rounded rect: -->
  <!--   M x y+h  V y+r  Q x y x+r y  H x+w-r  Q x+w y x+w y+r  V y+h  Z -->
  <path d="M {x} {y+h} V {y+r} Q {x} {y} {x+r} {y} H {x+w-r}
           Q {x+w} {y} {x+w} {y+r} V {y+h} Z" fill="url(#g-brand)"/>

  <!-- Traffic light dots -->
  <circle cx="..." cy="..." r="4" fill="#fbbf24"/>
  <circle cx="..." cy="..." r="4" fill="#fb923c"/>
  <circle cx="..." cy="..." r="4" fill="#34d399"/>
  <text x="..." y="..." class="mono" font-size="11" fill="white"
        letter-spacing="0.5">chapter · subtitle</text>

  <!-- Content text -->
  <text class="body" font-size="11.5" fill="#1f2937">...</text>
</g>
```

**Concrete example** (x=40, y=100, w=320, h=90, title-h=30, r=12):
```svg
<path d="M 40 130 V 112 Q 40 100 52 100 H 348 Q 360 100 360 112 V 130 Z"
      fill="url(#g-brand)"/>
```

### Background Texture
```svg
<!-- Base gradient -->
<linearGradient id="g-bg" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#fafaf9"/>
  <stop offset="100%" stop-color="#ffffff"/>
</linearGradient>
### Background (Clean Approach)
```svg
<!-- ✓ PREFERRED: Clean solid background — NO grid patterns -->
<rect width="1200" height="520" fill="#fafaf9"/>

<!-- Subtle decorative halos (optional, very low opacity) -->
<circle cx="200" cy="200" r="300" fill="#4338ca" opacity="0.03"/>
<circle cx="1000" cy="900" r="400" fill="#6366f1" opacity="0.02"/>
```

**Avoid grid patterns** — they add visual noise and make diagrams look cluttered. Premium SVGs use clean backgrounds with subtle color halos only when needed.

### Premium SVG Layout Principles

1. **Horizontal flow layout** — Clear left-to-right reading direction, the natural reading pattern
2. **Clean visual hierarchy** — Use size and color weight to signal importance (core node largest/boldest)
3. **Consistent node sizing** — All sibling nodes same size (e.g., 220x120); core node can be larger
4. **Color-coded flow paths** — Green arrows for success/hit, red for failure/miss, brand for neutral flow
5. **Professional typography** — Larger, confident text; mono for technical terms; clear size hierarchy
6. **Minimal decoration** — No grid, no ornamental shapes, no traffic-light dots unless showing a window/terminal
7. **Clear legend** — Bottom-left or bottom-center, explaining colors and arrow types
8. **Balanced composition** — Even whitespace distribution, centered main flow

### Emphasis Techniques
- **Red `#dc2626`** for critical values (sizes, thresholds, counts)
- **Brand color** for variable names and output identifiers
- **Mono font** for all technical terms
- **Gradient arrows** for flow direction
- **Glow shadow** on important/final output nodes
- **Rose/pink** for LLM-related steps (differentiates from brand)

### Arrow Labels (CRITICAL)
Text labels placed on or near arrows **must always have a background** — never bare text.

**For diagonal arrows: keep labels horizontal and center them EXACTLY at the arrow's midpoint.**

```svg
<!-- ✓ GOOD: horizontal label, rx=3 (nearly square), centered at arrow midpoint -->
<!-- Calculate midpoint: mx = (x1+x2)/2, my = (y1+y2)/2 -->
<!-- Rect positioned so its center is at (mx, my) -->
<rect x="546" y="175" width="78" height="20" rx="3"
      fill="#d1fae5" stroke="#059669" stroke-width="1"/>
<text x="585" y="189" text-anchor="middle" class="mono" font-size="10"
      fill="#059669">✓ Cache Hit</text>

<!-- ✗ BAD: pill/capsule shape (rx=10+) on diagonal arrow -->
<rect x="555" y="165" width="78" height="20" rx="10" fill="#d1fae5"/>

<!-- ✗ BAD: rotated label group (unnecessary, looks awkward) -->
<g transform="rotate(-32, 585, 185)">
  <rect .../>
  <text .../>
</g>

<!-- ✗ BAD: bare text on arrow -->
<text x="580" y="175" fill="#059669">✓ Cache Hit</text>
```

**Positioning rules:**
1. Calculate arrow midpoint: `mx = (x1+x2)/2`, `my = (y1+y2)/2`
2. Set rect `x = mx - width/2`, `y = my - height/2`
3. Set text `x = mx`, `y = my + 4` (baseline offset)
4. Use `text-anchor="middle"` for centering
5. Use `rx="3"` (nearly square corners) — **NOT `rx="10"`** (capsule shape)
6. Keep labels HORIZONTAL — never rotate

**Background color rules:**
- Success/positive labels: `fill="#d1fae5"` (success-light) with `stroke="#059669"`
- Error/negative labels: `fill="#fee2e2"` (danger-light) with `stroke="#dc2626"`
- Neutral/info labels: `fill="#e0f2fe"` (info-light) with `stroke="#0284c7"`
- Brand labels: `fill="var(--brand-soft)"` with `stroke="var(--brand)"`

### Arrow Routing (CRITICAL)

**The final arrow segment MUST be perpendicular to the edge it connects to.** Diagonal arrows across the diagram are confusing and look unprofessional.

**For connections between nodes at different vertical positions, use L-shaped paths:**

```svg
<!-- ✗ BAD: diagonal line crossing the diagram -->
<line x1="1020" y1="260" x2="600" y2="360" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arr)"/>

<!-- ✓ GOOD: L-shaped path with perpendicular final arrow -->
<path d="M1020 260 L1020 300 L600 300 L600 360" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arr)" fill="none"/>
```

**L-shape path formula:**
1. Start at source edge (e.g., bottom of node A)
2. Go vertically down (or up) to intermediate Y
3. Go horizontally to target X
4. Go vertically down (or up) to target edge
5. Final segment is perpendicular to target edge

**Example routing:**
```
Node A bottom (1020, 260)
    │
    │  (vertical down to y=300)
    ▼
(1020, 300)
    │
    │  (horizontal left to x=600)
    ├──────────────
    │
(600, 300)
    │
    │  (vertical down to Node B top)
    ▼
Node B top (600, 360)  ← arrow perpendicular to horizontal edge
```

**Rules:**
- ✅ Use `<path>` with multiple `L` commands for L-shapes
- ✅ Route paths AROUND cards, not THROUGH them
- ✅ Final arrow segment perpendicular to target edge
- ✅ Keep arrow markers 12x12 with `orient="auto"`
- ❌ Never use diagonal `<line>` elements between distant nodes
- ❌ Never use bezier curves (`C`, `Q`) for simple connections — they're unpredictable

### Timeline SVGs (Project Roadmaps, Implementation Plans)

For phase-based timelines (3+ phases), use this premium layout structure:

```
┌─ 标题区 (Phase 卡片) ─┐  ┌─ ... ─┐  ┌─ ... ─┐
│ Phase N · Week X-Y    │
│ 阶段标题               │
│ 关键任务               │
└──────────┬────────────┘
           │
  ─────────●═════════════════════════●  ✓
       渐变进度条                  完成节点
  ──────────────────────────────────────
┌─ 交付物卡片 ─┐  ┌─ ... ─┐  ┌─ ... ─┐
│ 交付物 1     │
│ 交付物 2     │
└──────────────┘
  图例
```

**Key design rules:**

1. **Phase cards** — Use `rx="10"` rounded rect with brand gradient title bar:
```svg
<g filter="url(#shadow-sm)">
  <rect x="130" y="80" width="180" height="70" rx="10"
        fill="url(#g-muted)" stroke="#c7d2fe" stroke-width="1"/>
  <!-- Title bar using path for top-rounded corners only -->
  <path d="M130 104 V 90 Q 130 80 140 80 H 300 Q 310 80 310 90 V 104 Z"
        fill="url(#g-brand)"/>
  <text x="145" y="97" class="mono" font-size="11" fill="white">Phase 1 · Week 1-2</text>
  <text x="145" y="124" class="title" font-size="15" fill="#1e3a8a">阶段标题</text>
  <text x="145" y="143" class="body" font-size="10.5" fill="#374151">任务描述</text>
</g>
```

2. **Timeline bar** — Use TWO stacked rects: light background + gradient progress:
```svg
<!-- Background (entire timeline, muted) -->
<rect x="100" y="178" width="1000" height="6" rx="3" fill="#e0e7ff"/>
<!-- Progress (completed portion, gradient from brand to success) -->
<rect x="100" y="178" width="850" height="6" rx="3" fill="url(#g-timeline)"/>
```

3. **Phase nodes** — Small circles ON the timeline, white stroke border for emphasis:
```svg
<circle cx="220" cy="181" r="10" fill="url(#g-brand)" stroke="white" stroke-width="3"/>
<text x="220" y="185" text-anchor="middle" class="mono" font-size="10" fill="white">1</text>
```

4. **Completion node** — Larger circle with success color:
```svg
<circle cx="1090" cy="181" r="14" fill="url(#g-success)"
        stroke="white" stroke-width="3" filter="url(#shadow-sm)"/>
<text x="1090" y="186" text-anchor="middle" class="mono" font-size="12" fill="white">✓</text>
```

5. **Deliverable cards** — Below timeline, muted gray rects listing key outputs:
```svg
<rect x="140" y="238" width="160" height="56" rx="6"
      fill="#f1f5f9" stroke="#e2e8f0" stroke-width="1"/>
<text x="150" y="254" class="mono" font-size="10" fill="#4338ca" font-weight="600">交付物</text>
<text x="150" y="270">• 交付物 1</text>
<text x="150" y="286">• 交付物 2</text>
```

6. **Legend** — Bottom row showing color meanings:
```svg
<g transform="translate(100, 325)">
  <rect x="0" y="-10" width="12" height="12" rx="3" fill="url(#g-brand)"/>
  <text x="18" y="0">进行中</text>
  <!-- ... more legend items -->
</g>
```

**Timeline gradient for progress bar:**
```svg
<linearGradient id="g-timeline" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#e0e7ff"/>
  <stop offset="50%" stop-color="#4338ca"/>
  <stop offset="100%" stop-color="#059669"/>
</linearGradient>
```

## Code Highlighting Colors (for SVG text)

When coloring text inside SVG code blocks, use these VS Code-inspired colors:
```
Keywords (.kw):    #c084fc  (purple)
Functions (.fn):   #fde68a  (yellow)
Types (.tp):       #67e8f9  (cyan)
Strings (.st):     #86efac  (green)
Comments (.cm):    #64748b  (slate, italic)
Variables (.var):  #7dd3fc  (light blue)
Numbers (.num):    #fda4af  (pink)
```

## Generation Workflow

### For Documentation:

1. **Analyze content** — Understand the topic, identify sections, note where diagrams/code belong
2. **Choose style + palette** — Chinese flow/process doc → Chinese Technical Spec style (`templates/css-system-cn.css`, cover + part dividers + flow/funnel); otherwise International style (Indigo for technical/analytical, Purple for creative/LLM)
3. **Plan structure** — Map chapters to sections, decide density (high for reading, low for presenting)
4. **Generate HTML skeleton** — Use the layout template above (header + TOC + sections)
5. **Style each component** — Apply cards, tables, code blocks, callouts as appropriate
6. **Design SVG diagrams** — Create flow diagrams using the template components
7. **Test responsive** — Ensure 900px/600px breakpoints work
8. **Verify typography** — Check that all three fonts are loaded and applied correctly

### For Proposals:

1. **Identify proposal type** — Technical / Project / Architecture / Design / Implementation / Research
2. **Clarify scope** — 背景、目标、约束条件、利益相关者
3. **Choose palette** — Indigo for technical proposals, Purple for design/architecture
4. **Build skeleton** — Use the Proposal Structure Template above
5. **Populate Executive Summary** — 3-5 key stats with `stat-card` components
6. **Generate Background section** — 现状 + 问题分析 + SVG 流程图
7. **Design Objectives** — SMART 目标表格 + KPI 徽章
8. **Create Approach section** — 总体策略 + SVG 架构图 + 分栏卡片
9. **Build Implementation timeline** — SVG 甘特图/时间线 + 里程碑
10. **Compose Resources section** — 团队/预算表格 + 依赖关系图
11. **Draft Risks section** — 风险矩阵 + 分级 callout（danger/warning/success）
12. **Create Alternatives section** — 对比表格 + 推荐方案高亮 + SVG 决策树
13. **Write Conclusion** — 审批请求 + 下一步行动
14. **Add meta information** — 作者/日期/版本/状态徽章
15. **Test responsive** — Ensure 900px/600px breakpoints work

## Proposal Palette Guidance

| Proposal Type | Recommended Palette | Reasoning |
|---------------|---------------------|-----------|
| 技术方案 | Indigo | 专业、可信赖、强调数据 |
| 项目方案 | Indigo | 结构化、严肃、重视里程碑 |
| 架构方案 | Purple | 创意、设计感、视觉层次 |
| 设计方案 | Purple | 审美、风格、用户体验导向 |
| 实施方案 | Indigo | 严谨、时间线、可执行性 |
| 研究报告 | Indigo | 数据驱动、客观、分析性 |

## Proposal Header Variants

```html
<!-- Technical proposal -->
<header class="doc-header">
  <div class="header-inner">
    <span class="eyebrow">Technical Proposal · v2.1 · DRAFT</span>
    <h1>系统架构升级方案 · <em>微服务化改造</em></h1>
    <div class="subtitle">将单体架构拆分为领域驱动的微服务架构，提升系统可扩展性</div>
    <div class="meta">
      <span>📅 2026-07-14</span>
      <span>•</span>
      <span>👥 Architecture Team</span>
      <span>•</span>
      <span>🔖 <code>Status: Pending Review</code></span>
    </div>
  </div>
</header>
```

## Quality Checklist

Before delivering:
- [ ] Content type identified (Doc vs Proposal vs Mixed)
- [ ] **Style selected** (Chinese Technical Spec for CJK flow docs vs International for English/prose) and CSS copied from the matching template
- [ ] CN style: cover has `.tag` + serif h1 + `.sub` + `.meta` + `.kpis`
- [ ] CN style: parts numbered `Part 01…` with `.part` dividers; `h2.sec` has 48px purple underline
- [ ] CN style: flow bar colors consistent with legend (blue 召回 / purple 增强 / green 输出 / amber LLM / teal DB)
- [ ] CN style: `.exec` 管理摘要 present for pipeline docs
- [ ] CN style: callouts use tinted full-border variants (info/warn/err/ok)
- [ ] CN style: funnel bars width encodes relative volume
- [ ] Playfair Display used for ALL display headings
- [ ] Inter used for body text
- [ ] JetBrains Mono for ALL technical terms (including inside tables)
- [ ] Brand color consistent throughout (header, TOC bar, section titles, accents)
- [ ] All sections exactly 1280px wide and aligned
- [ ] Code blocks have traffic-light dots AND language labels
- [ ] SVG uses same font stack as page
- [ ] SVG @import URLs use raw `&` (NOT `&amp;`)
- [ ] TOC uses `list-style: none` (no double number+dot markers)
- [ ] SVG arrow labels have pill-shaped backgrounds (never bare text)
- [ ] SVG arrow routing uses L-shaped paths (final segment perpendicular to target edge)
- [ ] SVG title bars use single `<path>` (NOT two stacked `<rect>` — causes seam line)
- [ ] No visible thin accent bars (`<rect height="4">`) on nodes — they create unwanted seam lines
- [ ] **Timelines**: Phase nodes have white stroke border, completion node is success green
- [ ] **Timelines**: Progress bar uses TWO stacked rects (light bg + gradient progress)
- [ ] **Timelines**: Deliverable cards below timeline listing key outputs per phase
- [ ] **Timelines**: Legend at bottom explaining colors/line types
- [ ] Shadows layered (not flat)
- [ ] Callouts have gradient fade (not flat background)
- [ ] **Proposals**: Executive summary with stat cards
- [ ] **Proposals**: Timeline / Gantt / decision tree SVG
- [ ] **Proposals**: Alternatives comparison with recommendation highlighted
- [ ] **Proposals**: Risks with severity-level callouts
- [ ] **Proposals**: Status badge in header
- [ ] Responsive breakpoints work (900px: stack grids, 600px: single column)
- [ ] Emphasis words use `<em>` with brand/rose color

## Anti-Patterns to Avoid

❌ System fonts (Arial, Helvetica) as display type
❌ Pure black (#000) backgrounds for code — use slate-900 (#0f172a)
❌ Flat design with no shadows — always use layered shadows
❌ Generic purple gradients on white — our brand purple is deeper/sophisticated
❌ Inconsistent widths between header, TOC, and content
❌ Missing `data-lang` attribute on code blocks
❌ SVG with different fonts than the page
❌ Flat callout backgrounds (use gradient fade)
❌ Emoji-only icons without context
❌ Generic card layouts without hover effects
❌ `&amp;` in CSS URLs inside `<style>` blocks (use raw `&`)
❌ TOC with both list numbers AND bullet dots (use `list-style: none` on `<ol>`)
❌ Bare text labels on SVG arrows without background boxes
❌ Capsule-shaped labels (`rx="10"+`) on arrows — use `rx="3"` (nearly square) instead
❌ Rotated label groups on diagonal arrows — keep labels horizontal, center at arrow midpoint
❌ Diagonal `<line>` elements between distant nodes — use L-shaped `<path>` instead
❌ Bezier curves (`C`, `Q`) for simple arrow connections — unpredictable rendering
❌ Arrow final segment not perpendicular to target edge
❌ Arrow paths crossing through cards — route around instead
❌ SVG title bars made of two stacked `<rect>` elements (causes visible seam line — use single `<path>` with top-rounded corners only)
❌ Thin decorative accent bars (`<rect height="4" opacity="0.3-0.6">`) on top of nodes — they create visible horizontal seam lines
❌ Grid pattern backgrounds on SVG diagrams (`<pattern>` with lines) — adds visual noise, makes diagrams look cluttered
❌ Timeline with only bare circles on a line — use phase cards + gradient bar + deliverable cards + legend
❌ Timeline with a single solid color progress bar — use TWO stacked rects (light background + gradient progress)

## Reference Files

| File | Purpose |
|------|---------|
| `templates/css-system.css` | International style — complete CSS with all components |
| `templates/css-system-cn.css` | Chinese Technical Spec style (Multi-ES) — cover hero, part dividers, vertical flow, funnel, tinted callouts |
| `templates/svg-components.svg` | Reusable SVG card templates |
