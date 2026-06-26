---
name: pretext
description: "精准文本测量与布局引擎（基于开源 Pretext）。无需触碰 DOM，纯算术计算文本像素高度，支持中文、CJK、emoji 等多语言。多用于前端虚拟滚动、AI 生成 UI 布局预计算、Canvas 渲染等场景。当用户需要计算文字在指定宽度下的高度、判断换行行数、或精确布局文本时调用此 Skill。"
description_zh: "精准文本测量与布局引擎，基于 GitHub 42K Stars 的开源项目 @chenglou/pretext。无需 DOM，快速计算任意文本在指定宽度/字体下的像素高度与行数，支持中文、CJK、emoji 等多语言。"
description_en: "Accurate text measurement and layout engine powered by @chenglou/pretext. Zero DOM, pure arithmetic. Calculate text height and line count for any font/width. Supports Chinese, CJK, emoji."
version: "1.0.0"
homepage: https://github.com/chenglou/pretext
license: MIT
allowed-tools: Bash, Read, Write, Edit
metadata:
  clawdbot:
    emoji: "📐"
    requires:
      bins:
        - node
      pip: []
      note: "需要 Node.js 运行环境（v16+）。@chenglou/pretext 为自动依赖。canvas（node-canvas）为可选依赖，在 Windows/Linux/macOS 上可获得高精度测量；未安装时自动降级为纯 JS Unicode 估算模式，功能完整但精度略低。"
    setup:
      - "cd ${CLAUDE_SKILL_DIR} && npm install"
      - "canvas（可选）：npm install canvas — 在 Windows 上需要系统依赖（Cairo/Pango 等），安装失败不影响基础功能"
      - "高清模式：node scripts/install-deps.js"
  tags:
    - text-measurement
    - layout
    - frontend
    - virtual-scroll
    - canvas
    - chinese-text
    - i18n
---

# 📐 Pretext Text Measurement Skill

基于开源库 **@chenglou/pretext**（MIT License）构建的精准文本测量与布局引擎。

> GitHub: [chenglou/pretext](https://github.com/chenglou/pretext) · 42.1K Stars
> 版权声明见本文件末尾 `## 开源许可` 章节。

---

## 🎯 核心能力

当用户需要以下任何一种计算时，调用此 Skill：

| 用户意图 | Skill 做什么 |
|:---|:---|
| "这段文字在 300px 宽、16px 字体下有多高？" | 精确计算高度 + 行数 |
| "帮我判断这段文字会不会换行" | 返回行数和每行内容 |
| "这 50 条消息列表，每条在 375px 下多高？" | 批量测量所有条目 |
| "计算这段富文本（带 @提及、标签）的高度" | 富文本内联布局 |
| "找出让文本恰好不换行的最小宽度" | 收缩包裹宽度测量 |
| "这段文字在 Canvas 里怎么分行绘制？" | 返回逐行绘制坐标 |

---

## 🚀 快速开始

### 基础测量（最常用）

```bash
node "${CLAUDE_SKILL_DIR}/scripts/measure.js" \
  --text "你好，世界！这是一段测试文本。" \
  --font "16px Inter, sans-serif" \
  --width 300 \
  --lineHeight 20
```

**返回示例：**
```json
{
  "success": true,
  "text": "你好，世界！这是一段测试文本。",
  "font": "16px Inter, sans-serif",
  "width": 300,
  "lineHeight": 20,
  "height": 44.8,
  "lineCount": 3,
  "unit": "px"
}
```

---

## 📖 场景化使用指南

### 场景 1：虚拟滚动 / 聊天消息列表

```bash
node "${CLAUDE_SKILL_DIR}/scripts/batch.js" \
  --items "第一条消息内容" \
  --items "第二条消息内容" \
  --items "第三条消息内容" \
  --font "14px -apple-system, sans-serif" \
  --width 375 \
  --lineHeight 20
```

### 场景 2：获取逐行详细信息（Canvas 绘制用）

```bash
node "${CLAUDE_SKILL_DIR}/scripts/layout-lines.js" \
  --text "Hello 世界 🚀" \
  --font "18px Inter" \
  --width 320 \
  --lineHeight 26
```

### 场景 3：仅查询行数 / 最宽行（性能最优）

```bash
node "${CLAUDE_SKILL_DIR}/scripts/line-stats.js" \
  --text "多行文本内容，每行长度不一" \
  --font "16px Inter" \
  --width 200
```

### 场景 4：富文本内联（@提及、代码块、标签）

```bash
node "${CLAUDE_SKILL_DIR}/scripts/rich-inline.js" \
  --items '[{"text":"普通文字 ","font":"16px Inter"},{"text":"@用户名","font":"bold 14px Inter","break":"never","extraWidth":10},{"text":".","font":"16px Inter"}]' \
  --width 300
```

### 场景 5：文本绕排浮动元素（变宽布局）

适用于文字围绕图片/侧边栏排版的场景：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/wrap-layout.js" \
  --text "长文本内容，填充整段..." \
  --font "16px Inter" \
  --width 600 \
  --floatWidth 200 \
  --floatHeight 300 \
  --lineHeight 22
```

### 场景 6：清除内部缓存（换字体时调用）

```bash
node "${CLAUDE_SKILL_DIR}/scripts/clear-cache.js"
```

### 场景 7：DOM 渲染（Accordion / Chat Bubbles / Masonry）

**无需触碰 DOM 测量，Pretext 预先算出每条内容的高度，直接渲染。**

```bash
# 生成 HTML 片段
node "${CLAUDE_SKILL_DIR}/scripts/render-dom.js" \
  --text "小兔子豆豆睡不着，看见窗外有一艘发光的月亮船..." \
  --font "17px sans-serif" \
  --width 400 \
  --lineHeight 34 \
  --align left

# 输出逐行 HTML，可直接粘贴到浏览器控制台
node "${CLAUDE_SKILL_DIR}/scripts/render-dom.js" \
  --text "欢迎使用 Pretext！" \
  --width 300 \
  --output snippet
```

也可作为模块导入：

```javascript
const { renderToDOM, renderAccordion, renderChatBubbles } = require('./scripts/render-dom');

// Accordion 示例
const result = renderAccordion([
  { title: "月亮船", text: "小兔子睡不着...", duration: 300 },
  { title: "小海龟", text: "奇奇第一次旅行...", duration: 300 },
], '16px sans-serif', 400, 24);

// 返回 { items, accordionHtml, totalClosedHeight, totalOpenHeight }
console.log(result.accordionHtml);
```

**适用场景：**
- Accordion（展开折叠，内容高度 Pretext 算好，CSS transition 直接用）
- Chat Bubbles（每条消息高度预计算，插入不抖动）
- Masonry（卡片高度预知，零 DOM 回流）

---

### 场景 8：文字粒子自由运动（Canvas 动画）

**每个字符变成物理粒子，在 Canvas 上自由飘动——用 Pretext 精确测量每个字符宽度，保证字符间距自然。**

```bash
# 生成粒子动画 HTML（直接用浏览器打开）
node "${CLAUDE_SKILL_DIR}/scripts/particle-text.js" \
  --text "你好，世界！Hello World! 🎉" \
  --font "32px sans-serif" \
  --width 800 \
  --height 500

# 分析文本粒子数量
node "${CLAUDE_SKILL_DIR}/scripts/particle-text.js" \
  --text "欢迎来到 Pretext 世界！" \
  --output info

# 自定义风格
node "${CLAUDE_SKILL_DIR}/scripts/particle-text.js" \
  --text "Pretext 粒子引擎" \
  --bg "#1a0a2e" \
  --color "#C77DFF" \
  --mouseRadius 150
```

**交互功能：**
- 🖱️ **鼠标推开**：鼠标靠近粒子会被斥力推开
- 🔄 **反弹模式**：粒子碰到边界弹回
- ↩️ **环绕模式**：粒子从另一边重新进入
- 🌀 **重力模式**：开启后粒子会下坠
- 💥 **爆炸按钮**：所有粒子向四面八方爆开
- ⌨️ **打字机模式**：粒子逐字出现
- 🔄 **重置**：恢复初始状态

**动画原理：**
```
每帧 loop:
  1. 读取鼠标位置 → 计算粒子受推力
  2. 更新粒子速度（+阻尼 +微风）
  3. Pretext 宽度估算 → 粒子位置更新
  4. Canvas 渲染（带发光效果）
  5. requestAnimationFrame → 回到 1
```

---

## 🔧 字体参数指南

### 常用字体组合

| 语言 | 推荐字体 | 示例 |
|:---|:---|:---|
| 英文/通用 | Inter | `16px Inter` |
| 中文 | 系统默认 | `16px -apple-system, "PingFang SC", "Microsoft YaHei"` |
| 中文 + 英文混排 | 混合 | `16px "PingFang SC", Inter` |
| 代码 | 等宽字体 | `14px "Fira Code", "Consolas", monospace` |
| 粗体/斜体 | 组合 | `bold 16px Inter` 或 `italic 16px Inter` |

### Canvas 字体简写格式

```
[style] [variant] [weight] [size] [font-family]
```

示例：`bold 14px Inter`、`italic 16px "PingFang SC"`、`500 17px Inter`

---

## 📋 API 参数速查

### measure.js（最常用）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|:---|:---|:---|:---|:---|
| `--text` | string | ✅ | — | 要测量的文本内容 |
| `--font` | string | ✅ | — | Canvas 字体简写，如 `16px Inter` |
| `--width` | number | ✅ | — | 容器最大宽度（像素） |
| `--lineHeight` | number | ❌ | 20 | 行高（像素），需与 CSS `line-height` 同步 |
| `--whiteSpace` | string | ❌ | `normal` | `normal` 或 `pre-wrap`（保留空格/换行） |
| `--wordBreak` | string | ❌ | `normal` | `normal` 或 `keep-all`（CJK 不自动换行） |

### layout-lines.js（进阶）

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `--text` | string | ✅ | 文本内容 |
| `--font` | string | ✅ | 字体 |
| `--width` | number | ✅ | 宽度 |
| `--lineHeight` | number | ❌ | 行高，默认 24 |
| `--whiteSpace` | string | ❌ | `pre-wrap` 保留空格 |

返回每行的 `text`、`width`，以及 `startCursor` 和 `endCursor` 坐标。

### batch.js（批量）

| 参数 | 类型 | 说明 |
|:---|:---|:---|
| `--items` | string[] | 多个文本，可多次指定 |
| `--font` | string | 字体 |
| `--width` | number | 宽度 |
| `--lineHeight` | number | 行高 |

---

## 🌍 浏览器模式（100% 还原）

当在**浏览器环境**中使用时，Pretext 可以调用 `@chenglou/pretext` 原版 Canvas API，精度达到 **100%**，完整支持所有功能。

### 加载方式

在 HTML 中引入 UMD 构建：

```html
<script src="https://unpkg.com/@chenglou/pretext/dist/pretext.umd.min.js"></script>
```

或通过 npm 安装：

```bash
npm install @chenglou/pretext
```

### 核心 API

| API | 说明 | 返回值 |
|:---|:---|:---|
| `pretext.layout(text, fontSize, lineHeightRatio, maxWidth)` | 最常用，快速布局 | `{height, lineCount, estimatedWidth}` |
| `pretext.measureNaturalWidth(text, fontSize)` | 测量字符串宽度 | `number` (像素) |
| `pretext.prepare(text, fontSize, maxWidth)` | 预处理文本 | `{lines, _chars}` |
| `pretext.layoutNextLine(text, fontSize, lineHeightRatio, maxWidth, startAt)` | 逐行增量布局 | 行对象 |
| `pretext.setLocale(locale)` | 设置语言区域 | void |

### 完整示例（浏览器）

```html
<script src="https://unpkg.com/@chenglou/pretext/dist/pretext.umd.min.js"></script>
<script>
  const text = '小兔子豆豆今天又睡不着了。窗外突然亮了起来！';
  const result = pretext.layout(text, 17, 2.1, 560);
  console.log('高度:', result.height);     // 例如: 71.4
  console.log('行数:', result.lineCount);  // 例如: 3
  console.log('最宽行:', result.estimatedWidth); // 例如: 340
</script>
```

### 交互式演示

完整可操作的 API 演示页面：
`pretext/pretext-browser-demo.html`

包含：
- measureNaturalWidth 逐字宽度分析
- prepare() 逐行布局可视化
- layout() 快速测量（含 JS 估算精度对比）
- 中英文 + Emoji 混合排版
- 批量测量（虚拟滚动场景）

### AI Agent 使用建议

当 AI Agent 需要在浏览器中调用 pretext 时，可以：

1. **生成可注入代码**：运行 `measure-browser.js` 输出浏览器端代码片段
2. **创建演示页面**：使用 `pretext-browser-demo.html` 作为参考
3. **直接调用 API**：在有 DOM 环境的脚本中直接引用 `pretext.*`

---

## ⚠️ 已知限制

| 限制 | 说明 | 规避方案 |
|:---|:---|:---|
| macOS `system-ui` | macOS 下精度不稳定 | 使用具名字体如 `Inter`、`-apple-system` |
| 字体未加载 | `prepare()` 时字体必须已加载 | 确保使用系统已安装字体 |
| `white-space` | 仅支持 `normal` 和 `pre-wrap` | 不支持 `pre`、`nowrap` 等 |
| `word-break` | 仅支持 `normal` 和 `keep-all` | — |
| 空字符串 | 返回 `{lineCount: 0, height: 0}` | 浏览器实际保留一行高度，需注意 |

---

## 🧪 精度对比

| 方案 | 测量方式 | 精度 |
|:---|:---|:---|
| **Pretext（本 Skill）** | 纯算术 + Canvas measureText | ✅ 高精度，与浏览器一致 |
| **getBoundingClientRect** | DOM 渲染 + 重排 | ✅ 高精度，但有性能损耗 |
| **浏览器自动布局** | CSS `text-wrap` | ❌ 高度值不可读出 |
| **RTL 语言** | — | ❌ 暂不支持阿拉伯文/希伯来文 |

---

## 📐 技术原理简述

```
输入：文本 + 字体 + 宽度
       ↓
┌─────────────────────────────┐
│  prepare()  [预处理，一次]   │
│  · Unicode 分词（CJK/emoji） │
│  · Canvas measureText 测量  │
│  · 缓存字符宽度数组          │
└─────────────────────────────┘
       ↓ prepared 句柄
┌─────────────────────────────┐
│  layout()   [计算，无数次]   │
│  · 纯算术遍历宽度数组        │
│  · 模拟浏览器换行规则        │
│  · 返回 { height, lineCount }│
└─────────────────────────────┘
       ↓
输出：精确像素高度 + 行数
```

---

## 🤖 AI Agent 使用提示

当 AI Agent 需要计算文本在特定容器中的布局时：

1. **识别用户意图**：用户是否在说"高度"、"会不会换行"、"几行"、"超出来"等
2. **提取参数**：从用户描述中提取 `text`、`font`、`width`、`lineHeight`
3. **调用脚本**：使用 `measure.js` 或 `layout-lines.js`
4. **解读结果**：将 JSON 结果转换为自然语言反馈给用户

**典型用户话术 → Skill 调用映射：**

| 用户说 | 调用的脚本 |
|:---|:---|
| "计算高度" | `measure.js` |
| "会不会换行" | `measure.js`（看 lineCount > 1） |
| "每行分别多长" | `layout-lines.js` |
| "批量算" | `batch.js` |
| "带 @提及的" | `rich-inline.js` |

---

## 🔗 相关 Skill

- **[frontend-dev](frontend-dev)** — 前端开发综合 Skill，可搭配使用
- **[browser-use](browser-use)** — 浏览器自动化，可用于网页文本提取
- **[Canvas Design](canvas-design)** — Canvas 图形设计，搭配文本测量使用

---

## 📄 开源许可

本 Skill 基于 **@chenglou/pretext** 开发，遵循 MIT License。

---

## ⚠️ 免责声明

**本 Skill 以「现状」（AS IS）提供，不附带任何明示或暗示的保证。**

### 测量精度声明
- 文本高度与行数的计算结果为**估算值**，实际渲染结果可能因浏览器字体渲染、内嵌字体、自定义字形等因素而产生偏差。
- 在对布局精度要求极高的场景（如精确像素级 UI 开发）中，建议以浏览器实际渲染结果为准，本 Skill 提供的数值仅供参考。
- 安装 `canvas` 可显著提升测量精度；未安装时使用纯 JS Unicode 估算模式，功能完整但精度略低。

### 版权与许可
- 本 Skill 基于 MIT 协议开源项目 `@chenglou/pretext` 构建，版权归原作者 Cheng Lou（[@chenglou](https://github.com/chenglou)）所有。
- 详细许可信息见 [LICENSES.md](./LICENSES.md)。

### 使用限制
- 本 Skill 不得用于任何非法用途。
- 开发者不对因使用本 Skill 造成的任何直接或间接损失负责，包括但不限于数据丢失、业务中断、布局错误导致的 UI 问题。
- 不同操作系统/浏览器环境下实际宽度可能存在 ±5% 误差，此为正常现象。

### 第三方依赖
- `@chenglou/pretext`：MIT License（见 [LICENSES.md](./LICENSES.md)）
- `canvas`（可选）：[node-canvas](https://github.com/Automattic/node-canvas)，GPL/FreeType License
- 如未安装 `canvas`，本 Skill 将自动降级为纯 JS Unicode 估算模式，功能完整但精度略低。


### @chenglou/pretext — MIT License

```
MIT License

Copyright (c) 2026 Cheng Lou and Pretext contributors
https://github.com/chenglou/pretext

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

本 Skill 封装层（SKILL.md + scripts/*）版权归属 Skill 作者，遵循相同 MIT License。
