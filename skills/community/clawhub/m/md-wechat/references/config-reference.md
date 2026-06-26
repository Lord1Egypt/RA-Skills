# 配置项参考

本文档详细说明 `md-config.json` 配置文件中的所有配置项。

## 配置文件结构

```json
{
  "version": "1.0.0",
  "theme": { ... },
  "style": { ... },
  "codeBlock": { ... },
  "image": { ... },
  "link": { ... },
  "content": { ... },
  "headingStyles": { ... },
  "customCSS": ""
}
```

---

## 主题配置 (theme)

### theme.name

预设主题名称。

| 值 | 说明 | 适用场景 |
|---|------|---------|
| `default` | 经典主题 | 技术文章、教程、文档 |
| `grace` | 优雅主题 | 散文、游记、生活方式 |
| `simple` | 简洁主题 | 科技资讯、产品介绍、报告 |

```json
{
  "theme": {
    "name": "default"
  }
}
```

---

## 样式配置 (style)

### style.fontFamily

正文字体。

| 字体类型 | 值 | 特点 |
|---------|-----|------|
| 无衬线（推荐） | `-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif` | 现代简洁，适合屏幕阅读 |
| 衬线 | `Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, 'PingFang SC', Cambria, Cochin, Georgia, Times, 'Times New Roman', serif` | 传统典雅，适合长文阅读 |
| 等宽 | `Menlo, Monaco, 'Courier New', monospace` | 代码风格，适合技术文章 |

```json
{
  "style": {
    "fontFamily": "-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif"
  }
}
```

### style.fontSize

正文字号。

| 值 | 说明 | 适用场景 |
|---|------|---------|
| `14px` | 更小 | 信息密度高的文章 |
| `15px` | 稍小 | 普通文章 |
| `16px` | 推荐（默认） | 大多数场景 |
| `17px` | 稍大 | 适合中老年读者 |
| `18px` | 更大 | 大屏阅读 |

### style.primaryColor

主题色，用于标题、强调、链接等元素。

| 颜色名 | 值 | 气质 |
|-------|-----|------|
| 经典蓝 | `#0F4C81` | 稳重冷静 |
| 翡翠绿 | `#009874` | 自然平衡 |
| 活力橘 | `#FA5151` | 热情活力 |
| 柠檬黄 | `#FECE00` | 明亮温暖 |
| 薰衣紫 | `#92617E` | 优雅神秘 |
| 天空蓝 | `#55C9EA` | 清爽自由 |
| 玫瑰金 | `#B76E79` | 奢华现代 |
| 橄榄绿 | `#556B2F` | 沉稳自然 |
| 石墨黑 | `#333333` | 内敛极简 |
| 雾烟灰 | `#A9A9A9` | 柔和低调 |
| 樱花粉 | `#FFB7C5` | 浪漫甜美 |

```json
{
  "style": {
    "primaryColor": "#0F4C81"
  }
}
```

---

## 代码块配置 (codeBlock)

### codeBlock.themeUrl / codeBlock.themeName

代码高亮主题。

**常用主题**：
- `atom-one-dark` - Atom One Dark（默认）
- `atom-one-light` - Atom One Light
- `github` - GitHub 风格
- `github-dark` - GitHub Dark
- `monokai` - Monokai
- `nord` - Nord
- `vs` - Visual Studio
- `vs2015` - Visual Studio 2015 Dark
- `xcode` - Xcode

完整主题列表：
```
1c-light, a11y-dark, a11y-light, agate, an-old-hope, androidstudio,
arduino-light, arta, ascetic, atom-one-dark-reasonable, atom-one-dark,
atom-one-light, brown-paper, codepen-embed, color-brewer, dark, default,
devibeans, docco, far, felipec, foundation, github-dark-dimmed,
github-dark, github, gml, googlecode, gradient-dark, gradient-light,
grayscale, hybrid, idea, intellij-light, ir-black, isbl-editor-dark,
isbl-editor-light, kimbie-dark, kimbie-light, lightfair, lioshi, magula,
mono-blue, monokai-sublime, monokai, night-owl, nnfx-dark, nnfx-light,
nord, obsidian, panda-syntax-dark, panda-syntax-light, paraiso-dark,
paraiso-light, pojoaque, purebasic, qtcreator-dark, qtcreator-light,
rainbow, routeros, school-book, shades-of-purple, srcery,
stackoverflow-dark, stackoverflow-light, sunburst, tokyo-night-dark,
tokyo-night-light, tomorrow-night-blue, tomorrow-night-bright, vs,
vs2015, xcode, xt256
```

```json
{
  "codeBlock": {
    "themeUrl": "https://cdn-doocs.oss-cn-shenzhen.aliyuncs.com/npm/highlightjs/11.11.1/styles/atom-one-dark.min.css",
    "themeName": "atom-one-dark"
  }
}
```

### codeBlock.isMacStyle

是否使用 Mac 风格代码块（带红黄绿三个圆点）。

| 值 | 说明 |
|---|------|
| `true` | 显示 Mac 风格装饰（默认） |
| `false` | 不显示装饰 |

### codeBlock.showLineNumber

是否显示代码行号。

| 值 | 说明 |
|---|------|
| `true` | 显示行号 |
| `false` | 不显示行号（默认） |

---

## 图片配置 (image)

### image.legend

图片图注显示格式。

| 值 | 说明 | 示例 |
|---|------|------|
| `title-alt` | title 优先 | 先显示 title，没有则显示 alt |
| `alt-title` | alt 优先（默认） | 先显示 alt，没有则显示 title |
| `title` | 只显示 title | 仅显示 title 属性 |
| `alt` | 只显示 alt | 仅显示 alt 属性 |
| `none` | 不显示 | 不显示图注 |

```json
{
  "image": {
    "legend": "alt-title"
  }
}
```

---

## 链接配置 (link)

### link.citeStatus

是否在文末添加引用链接列表。

微信公众号不支持外链，开启此选项后，外链会在文末统一列出。

| 值 | 说明 |
|---|------|
| `true` | 添加引用链接 |
| `false` | 不添加（默认） |

```json
{
  "link": {
    "citeStatus": false
  }
}
```

---

## 内容配置 (content)

### content.countStatus

是否显示字数统计和预估阅读时间。

| 值 | 说明 |
|---|------|
| `true` | 在文章开头显示统计信息 |
| `false` | 不显示（默认） |

### content.useIndent

是否开启段落首行缩进（2em）。

| 值 | 说明 |
|---|------|
| `true` | 首行缩进 |
| `false` | 不缩进（默认） |

### content.useJustify

是否开启两端对齐。

| 值 | 说明 |
|---|------|
| `true` | 两端对齐 |
| `false` | 左对齐（默认） |

```json
{
  "content": {
    "countStatus": false,
    "useIndent": false,
    "useJustify": false
  }
}
```

---

## 标题样式配置 (headingStyles)

为每个级别的标题设置独立样式。

### 可选样式

| 值 | 说明 | 效果 |
|---|------|------|
| `default` | 使用主题默认样式 | - |
| `color-only` | 主题色文字 | 标题使用主题色 |
| `border-bottom` | 下边框 | 底部显示主题色边框 |
| `border-left` | 左边框 | 左侧显示主题色边框 |
| `custom` | 自定义 | 使用 customCSS 定义 |

### 配置示例

```json
{
  "headingStyles": {
    "h1": "border-bottom",
    "h2": "color-only",
    "h3": "border-left",
    "h4": "default",
    "h5": "default",
    "h6": "default"
  }
}
```

---

## 自定义 CSS (customCSS)

添加自定义 CSS 样式，可覆盖预设样式。

```json
{
  "customCSS": "h1 { font-size: 2em; }\nblockquote { background: #fffbe6; }"
}
```

### 常用自定义样式示例

**修改引用块背景色**：
```css
blockquote {
  background: #fffbe6;
  border-left-color: #ffc53d;
}
```

**添加图片阴影**：
```css
img {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

**修改链接颜色**：
```css
a {
  color: var(--md-primary-color);
  border-bottom: 1px dashed var(--md-primary-color);
}
```

**代码块圆角**：
```css
pre {
  border-radius: 12px;
}
```

---

## 完整配置示例

```json
{
  "version": "1.0.0",
  
  "theme": {
    "name": "default"
  },

  "style": {
    "fontFamily": "-apple-system-font,BlinkMacSystemFont, Helvetica Neue, PingFang SC, Hiragino Sans GB , Microsoft YaHei UI , Microsoft YaHei ,Arial,sans-serif",
    "fontSize": "16px",
    "primaryColor": "#0F4C81"
  },

  "codeBlock": {
    "themeUrl": "https://cdn-doocs.oss-cn-shenzhen.aliyuncs.com/npm/highlightjs/11.11.1/styles/atom-one-dark.min.css",
    "themeName": "atom-one-dark",
    "isMacStyle": true,
    "showLineNumber": false
  },

  "image": {
    "legend": "alt-title"
  },

  "link": {
    "citeStatus": false
  },

  "content": {
    "countStatus": false,
    "useIndent": false,
    "useJustify": false
  },

  "headingStyles": {
    "h1": "default",
    "h2": "default",
    "h3": "default",
    "h4": "default",
    "h5": "default",
    "h6": "default"
  },

  "customCSS": ""
}
```

---

## CSS 变量参考

在自定义 CSS 中可使用以下变量：

| 变量名 | 说明 | 默认值 |
|-------|------|-------|
| `--md-primary-color` | 主题色 | `#0F4C81` |
| `--md-font-family` | 字体 | 无衬线字体栈 |
| `--md-font-size` | 字号 | `16px` |

**使用示例**：
```css
.my-custom-class {
  color: var(--md-primary-color);
  font-size: calc(var(--md-font-size) * 1.2);
}
```
