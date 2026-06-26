# 微信公众号平台规范

## 目录
- [支持的HTML标签和样式](#支持的html标签和样式)
- [不支持的特性](#不支持的特性)
- [编辑器兼容性](#编辑器兼容性)
- [最佳实践](#最佳实践)

## 概览
本文档详细说明微信公众号平台支持的HTML标签、CSS样式，以及主流编辑器的兼容性，帮助生成符合规范的排版模板。

---

## 支持的HTML标签和样式

### 基本文本标签
```html
<h1> - 一级标题（不常用，建议使用<h2>-<h4>）
<h2> - 二级标题（推荐）
<h3> - 三级标题
<h4> - 四级标题
<p> - 段落
<span> - 行内文本
<br> - 换行
<strong> - 加粗
<b> - 加粗（推荐使用<strong>）
<em> - 斜体
<i> - 斜体（推荐使用<em>）
```

### 列表标签
```html
<ul> - 无序列表
<ol> - 有序列表
<li> - 列表项
```

### 引用标签
```html
<blockquote> - 引用块
```

### 分隔标签
```html
<hr> - 水平分隔线
```

### 图片标签
```html
<img> - 图片（需使用外部链接或上传到微信图库）
```

### 支持的内联样式

#### 字体相关
```css
font-family: "微软雅黑", "Microsoft YaHei", sans-serif;
font-size: 14px; /* 推荐：12-20px */
font-weight: normal | bold;
font-style: normal | italic;
line-height: 1.75; /* 推荐：1.5-2.0 */
letter-spacing: 1px; /* 推荐：0-3px */
color: #333333; /* 推荐：使用十六进制颜色 */
```

#### 文本对齐
```css
text-align: left | center | right;
text-indent: 2em; /* 首行缩进 */
```

#### 背景和边框
```css
background-color: #F5F5F5;
background-image: url('图片URL'); /* 可能被过滤 */
border: 1px solid #E0E0E0;
border-left: 3px solid #1976D2; /* 左侧边框常用 */
border-radius: 4px; /* 圆角，支持但有限制 */
```

#### 间距和填充
```css
margin: 10px 0;
padding: 15px;
```

#### 其他
```css
text-decoration: none | underline;
opacity: 0.8; /* 透明度 */
```

### 推荐的样式组合

#### 标题样式
```html
<h2 style="color: #1976D2; font-size: 18px; font-weight: bold; margin: 20px 0 10px 0; padding-bottom: 10px; border-bottom: 2px solid #1976D2;">
  标题文本
</h2>
```

#### 正文样式
```html
<p style="color: #333333; font-size: 14px; line-height: 1.75; margin: 15px 0;">
  正文文本
</p>
```

#### 引用样式
```html
<blockquote style="background-color: #F1F8E9; padding: 15px; margin: 20px 0; border-left: 3px solid #2E7D32; color: #555555; font-style: italic;">
  引用内容
</blockquote>
```

#### 重点标注样式
```html
<span style="color: #D32F2F; font-weight: bold; font-size: 16px;">
  重点内容
</span>

<span style="background-color: #FFF3E0; color: #FF5722; padding: 2px 5px; border-radius: 2px;">
  重点内容
</span>
```

#### 列表样式
```html
<ul style="margin: 15px 0; padding-left: 20px; color: #333333; font-size: 14px; line-height: 1.75;">
  <li style="margin: 5px 0;">列表项1</li>
  <li style="margin: 5px 0;">列表项2</li>
  <li style="margin: 5px 0;">列表项3</li>
</ul>
```

#### 分隔线样式
```html
<hr style="border: none; border-top: 1px solid #E0E0E0; margin: 30px 0;">
```

---

## 不支持的特性

### 不支持的标签
```html
<div> - 部分编辑器支持，但不推荐
<table> - 表格标签不支持
<form> - 表单标签不支持
<input> - 输入控件不支持
<button> - 按钮不支持
<script> - 脚本不支持
<style> - 样式标签不支持
<iframe> - 内联框架不支持
<object> - 嵌入对象不支持
<embed> - 嵌入内容不支持
<video> - 视频标签不支持
<audio> - 音频标签不支持
```

### 不支持的CSS属性
```css
position - 定位属性不支持
float - 浮动不支持
display: flex - Flexbox不支持
display: grid - Grid不支持
transform - 变换不支持
transition - 过渡不支持
animation - 动画不支持
box-shadow - 盒阴影不支持（部分编辑器支持）
background-size - 背景尺寸不支持
background-repeat - 背景重复不支持
```

### 不支持的伪元素和伪类
```css
:before - 不支持
:after - 不支持
:first-child - 不支持
:last-child - 不支持
:nth-child - 不支持
:hover - 不支持
```

### 其他限制
- 不支持外部CSS文件引用
- 不支持JavaScript
- 不支持自定义字体（需使用系统字体）
- 不支持SVG（部分编辑器支持但不推荐）
- 背景图片可能被过滤
- 部分样式可能被编辑器自动清理

---

## 编辑器兼容性

### 主流编辑器对比

| 特性 | 135编辑器 | 秀米 | i排版 | 微信自带 |
|------|----------|------|-------|---------|
| 基本文本样式 | ✅ | ✅ | ✅ | ✅ |
| 背景色 | ✅ | ✅ | ✅ | ✅ |
| 边框 | ✅ | ✅ | ✅ | ✅ |
| 圆角 | ✅ | ✅ | ⚠️ | ❌ |
| 阴影 | ⚠️ | ⚠️ | ❌ | ❌ |
| 图标 | ✅ | ✅ | ✅ | ✅ |
| 模板丰富度 | 高 | 中 | 中 | 低 |

### 编辑器使用建议

#### 135编辑器
- 支持的样式最多，兼容性最好
- 提供丰富的模板库
- 支持自定义CSS
- 建议用于复杂排版需求

#### 秀米
- 界面简洁，易于使用
- 模板质量高
- 支持简单的自定义样式
- 建议用于快速排版

#### i排版
- 功能适中
- 模板实用
- 支持基础自定义样式
- 建议用于常规排版

#### 微信自带编辑器
- 功能最基础
- 不支持复杂样式
- 建议仅用于简单文本编辑

### 兼容性最佳实践
- 使用内联样式，不依赖外部CSS
- 避免使用复杂的CSS属性
- 测试时使用多个编辑器验证
- 优先使用平台原生支持的标签和样式
- 备份原始文本，避免样式丢失

---

## 最佳实践

### 1. 使用内联样式
```html
<!-- 推荐 -->
<p style="color: #333333; font-size: 14px;">文本</p>

<!-- 不推荐 -->
<p class="text">文本</p>
```

### 2. 使用系统字体
```css
/* 推荐 */
font-family: "微软雅黑", "Microsoft YaHei", sans-serif;

/* 不推荐 */
font-family: "自定义字体";
```

### 3. 控制字体大小
```html
<!-- 推荐 -->
<h2 style="font-size: 18px;">标题</h2>
<p style="font-size: 14px;">正文</p>

<!-- 不推荐 -->
<h2 style="font-size: 24px;">标题</h2>
<p style="font-size: 12px;">正文</p>
```

### 4. 使用十六进制颜色
```css
/* 推荐 */
color: #333333;
background-color: #F5F5F5;

/* 不推荐 */
color: rgb(51, 51, 51);
color: red;
```

### 5. 合理设置间距
```html
<!-- 推荐 -->
<p style="margin: 15px 0; padding: 10px;">文本</p>

<!-- 不推荐 -->
<p style="margin: 0; padding: 0;">文本</p>
```

### 6. 避免嵌套过深
```html
<!-- 推荐 -->
<p style="color: #333333;"><span style="font-weight: bold;">重点</span>文本</p>

<!-- 不推荐 -->
<div><p><span><em>文本</em></span></p></div>
```

### 7. 图片处理
```html
<!-- 推荐：使用外部链接 -->
<img src="https://example.com/image.jpg" alt="图片描述" style="width: 100%; display: block; margin: 20px 0;">

<!-- 推荐：使用微信图库上传后的链接 -->
<img src="微信图库URL" alt="图片描述" style="width: 100%; display: block; margin: 20px 0;">

<!-- 不推荐：使用本地路径 -->
<img src="./image.jpg" alt="图片描述">
```

### 8. 表情符号使用
```html
<!-- 推荐：使用Emoji -->
<p>🔥 限时特惠！</p>

<!-- 推荐：使用图片图标 -->
<img src="图标URL" style="width: 16px; height: 16px;">

<!-- 不推荐：使用特殊字符 -->
<p>♔ 限时特惠！</p>
```

### 9. 分隔线使用
```html
<!-- 推荐：简单的水平线 -->
<hr style="border: none; border-top: 1px solid #E0E0E0; margin: 30px 0;">

<!-- 推荐：带样式的分隔线 -->
<div style="text-align: center; color: #CCCCCC; margin: 30px 0;">✦ ✦ ✦</div>
```

### 10. 链接处理
```html
<!-- 推荐：使用微信内部链接 -->
<a href="https://mp.weixin.qq.com/s/xxx" style="color: #1976D2; text-decoration: none;">点击查看</a>

<!-- 不推荐：使用外部链接（可能被过滤） -->
<a href="https://www.baidu.com" style="color: #1976D2;">点击查看</a>
```

---

## 常见问题

### Q: 为什么有些样式在微信中不显示？
A: 微信会过滤不支持的样式和标签，确保只使用平台支持的HTML和CSS。

### Q: 如何确保排版在不同手机上显示一致？
A: 使用响应式设计，避免固定宽度，使用百分比和相对单位。

### Q: 可以使用自定义字体吗？
A: 不可以，只能使用系统默认字体（微软雅黑、思源黑体、苹方等）。

### Q: 如何处理图片？
A: 建议上传到微信图库或使用稳定的外部图床，避免图片加载失败。

### Q: 为什么复制粘贴后样式丢失？
A: 部分编辑器会自动清理样式，建议使用支持富文本的编辑器或直接复制HTML代码。

### Q: 可以使用视频吗？
A: 微信不支持直接嵌入视频，需要使用视频号或腾讯视频链接。

---

## 示例模板

### 基础文章模板
```html
<div style="font-family: '微软雅黑', 'Microsoft YaHei', sans-serif; color: #333333;">
  <!-- 标题 -->
  <h2 style="font-size: 18px; font-weight: bold; color: #1976D2; text-align: center; margin: 30px 0;">
    文章标题
  </h2>

  <!-- 正文段落1 -->
  <p style="font-size: 14px; line-height: 1.75; margin: 15px 0;">
    正文内容第一段...
  </p>

  <!-- 重点内容 -->
  <p style="font-size: 14px; line-height: 1.75; margin: 15px 0;">
    普通内容，<span style="color: #D32F2F; font-weight: bold;">重点内容</span>，普通内容。
  </p>

  <!-- 引用 -->
  <blockquote style="background-color: #F1F8E9; padding: 15px; margin: 20px 0; border-left: 3px solid #2E7D32; color: #555555; font-style: italic;">
    "引用内容..."
  </blockquote>

  <!-- 列表 -->
  <ul style="margin: 15px 0; padding-left: 20px; font-size: 14px; line-height: 1.75;">
    <li style="margin: 5px 0;">列表项1</li>
    <li style="margin: 5px 0;">列表项2</li>
    <li style="margin: 5px 0;">列表项3</li>
  </ul>

  <!-- 分隔线 -->
  <hr style="border: none; border-top: 1px solid #E0E0E0; margin: 30px 0;">

  <!-- 结尾 -->
  <p style="font-size: 14px; line-height: 1.75; margin: 15px 0; text-align: center; color: #999999;">
    感谢阅读，欢迎分享！
  </p>
</div>
```
