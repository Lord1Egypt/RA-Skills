---
name: markdown2html-converter
description: Use when building a Markdown to HTML converter with multiple blog themes, real-time preview, and download functionality
---

# Markdown 转 HTML 转换器

## 概述

创建单文件 Web 应用，将 Markdown 转换为 HTML，提供 20 种博客风格可选，支持实时预览和下载功能。

**核心技术原则：** 单文件架构 + CDN 依赖 + 模块化 JavaScript

## 使用场景

- 需要快速将 Markdown 文档转换为 HTML
- 需要多种博客风格选择
- 需要实时预览转换效果
- 需要离线使用的工具

## 架构设计

### 文件结构
```
index.html (单文件应用)
├── HTML 结构
│   ├── 头部（标题 + 下载按钮）
│   ├── 主容器（三列布局）
│   │   ├── 输入面板（textarea + 上传按钮）
│   │   ├── 样式选择面板（竖列卡片）
│   │   └── 实时预览面板
├── CSS（<style> 标签内）
│   ├── 重置和基础样式
│   ├── 布局样式
│   ├── 组件样式
│   ├── 20 种主题样式
│   └── 响应式媒体查询
└── JavaScript（<script> 标签内）
    ├── AppState（应用状态）
    ├── THEMES（主题配置）
    ├── SAMPLE_MARKDOWN（示例内容）
    ├── markdownParser 模块
    ├── styleManager 模块
    ├── fileHandler 模块
    ├── downloadHandler 模块
    └── uiManager 模块
```

### 三列布局结构
```
桌面端 (>1280px)：
┌─────────────────────────────────────────┐
│        输入(markdown)    实时预览(html)      │
├─────────────────────────────────────────┤
│            样式选择 (240px宽)             │
│            20个主题竖列展示             │
└─────────────────────────────────────────┘

所有面板高度：calc(100vh - 140px)
```

### 核心模块

**AppState（应用状态）**
```javascript
const AppState = {
    currentTheme: 'medium',      // 当前主题ID
    uploadedFileName: 'document'   // 上传的文件名
};
```

**markdownParser（Markdown解析器）**
- `configure()` - 配置 marked.js 选项（GFM、语法高亮）
- `parse(markdown)` - 将 Markdown 转换为 HTML

**styleManager（样式管理器）**
- `getAllThemes()` - 获取所有主题配置
- `setTheme(themeId)` - 切换主题
- `renderStyleCards()` - 渲染样式卡片
- `updateStyleCards()` - 更新选中状态

**fileHandler（文件处理器）**
- `handleFileUpload(file)` - 处理文件上传
- `loadSample()` - 加载示例内容

**downloadHandler（下载处理器）**
- `getThemeCSS(themeId)` - 提取主题CSS
- `generateHTML(markdown)` - 生成完整HTML
- `downloadHTML(markdown)` - 下载HTML文件

**uiManager（UI管理器）**
- `debounce(func, delay)` - 防抖函数
- `updatePreview()` - 更新预览内容
- `bindEvents()` - 绑定事件监听器
- `init()` - 初始化应用

## 快速参考

### HTML 结构模板
```html
<header class="header">
    <div class="header-container">
        <h1 class="header-title">标题</h1>
        <button id="downloadBtn" class="btn btn-primary">按钮</button>
    </div>
</header>

<main class="main-container">
    <div class="layout-grid">
        <!-- 输入面板 -->
        <section class="panel panel-input">
            <h2 class="panel-title">输入(markdown)</h2>
            <textarea id="markdownInput" class="markdown-textarea"></textarea>
            <div class="input-actions">
                <button id="uploadBtn" class="btn btn-secondary">上传</button>
                <button id="sampleBtn" class="btn btn-secondary">示例</button>
            </div>
        </section>

        <!-- 预览面板 -->
        <section class="panel panel-preview">
            <h2 class="panel-title">实时预览(html)</h2>
            <div id="previewContainer" class="preview-container">
                <div id="previewContent" class="preview-content theme-medium"></div>
            </div>
        </section>

        <!-- 样式选择面板 -->
        <section class="panel panel-styles">
            <h2 class="panel-title">选择样式</h2>
            <div id="styleCards" class="style-cards-grid"></div>
        </section>
    </div>
</main>
```

### 响应式断点
```css
/* 桌面端 (>1280px) */
grid-template-columns: 1fr 1fr 240px;
height: calc(100vh - 140px);

/* 平板端 (768-1280px) */
grid-template-columns: 1fr 1fr 220px;
height: calc(100vh - 120px);

/* 移动端 (<768px) */
grid-template-columns: 1fr;
height: auto;
```

### 20 种主题配置
```javascript
const THEMES = [
    { id: 'medium', name: '极简博客' },
    { id: 'ghost', name: '现代博客' },
    { id: 'wordpress', name: '经典博客' },
    { id: 'substack', name: '新闻简报' },
    { id: 'jekyll', name: 'GitHub风格' },
    { id: 'hugo', name: '文档博客' },
    { id: 'hashnode', name: '开发者社区' },
    { id: 'devto', name: '编程社区' },
    { id: 'blogger', name: '传统博客' },
    { id: 'tumblr', name: '休闲博客' },
    { id: 'zhihu', name: '知乎风格' },
    { id: 'juejin', name: '掘金风格' },
    { id: 'csdn', name: 'CSDN风格' },
    { id: 'jianshu', name: '清新简约' },
    { id: 'yuque', name: '语雀文档' },
    { id: 'notion', name: 'Notion风格' },
    { id: 'stackoverflow', name: 'StackOverflow' },
    { id: 'mediumcn', name: 'Medium中文' },
    { id: 'gitbook', name: 'GitBook' },
    { id: 'vuepress', name: 'VuePress' }
];
```

### CDN 依赖
```html
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
```

## 实现要点

### 1. 页面高度统一
所有三个面板（输入、预览、样式）使用相同高度：
```css
height: calc(100vh - 140px);
```

### 2. 内部滚动实现
- 输入面板：textarea 使用 `flex: 1` 占满空间
- 预览面板：preview-container 使用 `overflow-y: auto`
- 样式面板：style-cards-grid 使用 `overflow-y: auto`

### 3. 主题切换机制
- 移除所有主题类：`previewContent.classList.remove('theme-{id}')`
- 添加当前主题类：`previewContent.classList.add('theme-{id}')`
- 更新卡片选中状态

### 4. 防抖处理
```javascript
debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}
```

### 5. 文件上传处理
```javascript
async handleFileUpload(file) {
    // 验证文件类型
    if (!file.name.toLowerCase().endsWith('.md')) {
        throw new Error('只支持 .md 文件');
    }
    // 读取文件内容
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = () => reject(new Error('文件读取失败'));
        reader.readAsText(file);
    });
}
```

### 6. HTML 生成
```javascript
generateHTML(markdown) {
    const themeId = AppState.currentTheme;
    const parsedHTML = markdownParser.parse(markdown);
    const baseCSS = `* { box-sizing: border-box; margin: 0; padding: 0; } body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; padding: 2rem; } .content { max-width: 700px; margin: 0 auto; }`;
    const themeCSS = this.getThemeCSS(themeId);
    return `<!DOCTYPE html><html>...</html>`;
}
```

## 常见问题

### 问题：样式卡片不显示
**解决：** 确保 `styleManager.renderStyleCards()` 在 `uiManager.init()` 中调用

### 问题：预览不更新
**解决：** 确保 `markdownParser.configure()` 在初始化时调用

### 问题：下载的HTML没有样式
**解决：** 确保 `getThemeCSS()` 正确提取了样式规则

### 问题：文件上传失败
**解决：** 检查文件类型是否为 `.md`，控制台查看错误信息

### 问题：主题切换不生效
**解决：** 确保主题 CSS 类名正确，检查 `theme-{id}` 样式是否存在

## 扩展主题

### 添加新主题步骤：

1. 在 `THEMES` 数组中添加主题配置：
```javascript
{ id: 'newtheme', name: '新主题名称' }
```

2. 在 CSS 中添加主题样式：
```css
.theme-newtheme {
    font-family: ...;
    line-height: ...;
    color: ...;
    /* ... 其他样式 */
}
```

3. 在复选框样式中添加新主题：
```css
.theme-newtheme input[type="checkbox"] { ... }
```

### 主题设计原则

- **字体选择**：衬线 vs 无衬线 vs 等宽
- **色彩方案**：主色调、链接色、代码背景色
- **间距调整**：行高、段落间距、列表缩进
- **独特元素**：h2 装饰、引用样式、表格边框

## 性能优化

### 防抖输入
```javascript
input.addEventListener('input', debounce(() => {
    this.updatePreview();
}, 300));
```

### 事件委托
```javascript
container.addEventListener('click', (e) => {
    const card = e.target.closest('.style-card');
    if (card) {
        const themeId = card.dataset.theme;
        this.setTheme(themeId);
    }
});
```

### 语法高亮缓存
```javascript
if (lang && hljs.getLanguage(lang)) {
    try {
        return hljs.highlight(code, { language: lang }).value;
    } catch (e) {
        console.error('语法高亮失败:', e);
    }
}
```

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 依赖版本

- marked.js（最新稳定版）
- highlight.js v11.9.0

## 更新日志

- v1.0.0 - 初始版本，20 个主题
- v1.1.0 - 优化布局，统一样式名称
- v1.2.0 - 增加中文社区主题（知乎、掘金、CSDN、简书、语雀）
- v1.3.0 - 添加现代平台主题（Notion、StackOverflow、GitBook、VuePress）
- v1.4.0 - 统一三列面板高度，优化滚动体验
