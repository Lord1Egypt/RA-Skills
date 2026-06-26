# PRD 设计系统参考

编写HTML片段时需遵循的设计规范。

## 片段结构规范

### 正文片段

```html
<div class="content">
  <h2 class="section-title page-break" id="partN">
    <span class="num">§0N</span> 标题
  </h2>
  <p class="section-en">English Title</p>
  <p class="section-intro">概述</p>
  <!-- 正文 -->
</div>
```

**三条铁律：**
1. 必须用 `<div class="content">` 包裹
2. 第一个 `<h2>` 必须带 `id="partN"` 属性
3. 第一个 `<h2>` 必须带 `page-break` class

### 特殊片段

- 封面：`<div class="cover">...</div>`
- 目录：`<div class="toc">...</div>`
- 尾页：`<div class="back-page">...</div>`

## 流程图格式

使用Mermaid语法，简单格式：

```html
<div class="diagram">
  <div class="label">流程名称</div>
  <pre class="mermaid">
flowchart TD
    A[开始] --> B[步骤1]
    B --> C{判断}
    C -->|条件1| D[结果1]
    C -->|条件2| E[结果2]
  </pre>
</div>
```

## 常用组件

### 提示框
```html
<div class="tip">提示内容</div>
<div class="warning">警告内容</div>
```

### 表格
```html
<table>
  <tr><th>标题1</th><th>标题2</th></tr>
  <tr><td>内容1</td><td>内容2</td></tr>
</table>
```

### 用户故事
```html
<div class="story">
  <h4>US-001：标题</h4>
  <p>作为一个<strong>角色</strong>，<br>
  我想要<strong>功能</strong>，<br>
  以便于<strong>价值</strong>。</p>
</div>
```

## CSS变量

```css
--bg: #FFFFFF;
--text: #1A1A1A;
--text-secondary: #6B6B6B;
--accent: #2563EB;
--accent-light: #EFF6FF;
--border: #E5E5E5;
```

## 视觉规范

- 主色调：蓝色 `#2563EB`
- 背景：白色/浅灰渐变
- 字体：Noto Sans SC + Inter
- 代码字体：JetBrains Mono
- A4纸张，默认边距
