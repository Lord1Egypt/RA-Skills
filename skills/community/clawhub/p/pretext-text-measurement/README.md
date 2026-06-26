# 📐 Pretext Text Measurement Skill

> 精准文本测量与布局引擎 — 基于 GitHub 42.1K Stars 开源项目 `@chenglou/pretext`

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/chenglou/pretext/blob/main/LICENSE)
[![Node.js >=16](https://img.shields.io/badge/Node.js->=16-green.svg)](https://nodejs.org/)

---

## 🎯 这个 Skill 能做什么？

当你在开发中遇到这些问题时，Pretext Skill 可以帮你解决：

| 场景 | 问题 | Pretext 能做什么 |
|:---|:---|:---|
| 虚拟滚动列表 | 渲染前不知道每条消息多高 | 预计算所有消息高度，零 DOM |
| 聊天应用 | 新消息插入导致滚动位置漂移 | 提前锁定每条消息高度 |
| Canvas 渲染 | Canvas 里无法使用 `getBoundingClientRect` | 直接计算文本宽度和高度 |
| AI 生成 UI | AI 生成代码后文本溢出容器 | 预计算验证布局是否正确 |
| SSR | 服务端无法测量文本高度 | 在 Node.js 中直接计算 |
| 响应式布局 | 窗口缩放需要重新测量 | `layout()` 可无限次调用，极快 |
| **DOM 渲染** | Accordion/Chat Bubbles/Masonry 需要 DOM 回流 | Pretext 预计算高度，直接渲染零抖动 |
| **粒子动画** | 字符需要作为粒子自由运动 | Pretext 精确宽度 + Canvas 动画引擎 |

---

## ⚡ 性能对比

| 方案 | 单次测量耗时 | 500 条批量耗时 |
|:---|:---:|:---:|
| DOM `getBoundingClientRect` | 0.5–3ms + 重排 | 250–1500ms |
| **Pretext（本 Skill）** | **0.0002ms** | **0.09ms** |
| 加速比 | **快了 300–600 倍** | — |

---

## 🚀 快速开始

### 第一步：安装依赖

```bash
cd ~/.workbuddy/skills/pretext
npm install
```

> 如果 `canvas` 安装失败，Skill 会自动降级到 fallback 模式（仍可正常工作，仅换行精度略低）。

### 第二步：运行测试

```bash
# 基础测量
node scripts/measure.js --text "你好，世界！" --font "16px Inter" --width 300

# 批量测量（虚拟滚动）
node scripts/batch.js \
  --items "第一条消息内容" \
  --items "第二条消息内容" \
  --font "14px -apple-system" \
  --width 375

# 逐行布局
node scripts/layout-lines.js --text "Hello 世界 🚀" --font "18px Inter" --width 320
```

---

## 📁 Skill 结构

```
pretext/
├── SKILL.md              ← WorkBuddy/ClawHub 入口文件（Agent 指令）
├── package.json          ← 依赖声明
├── README.md             ← 你正在看的文档
├── LICENSES.md           ← 开源协议声明
├── particle-text-demo.html ← 自动生成：粒子动画演示页
└── scripts/
    ├── measure.js        ← 核心：基础文本测量（最常用）
    ├── layout-lines.js    ← 进阶：逐行详细信息
    ├── batch.js          ← 高效：批量测量（虚拟滚动）
    ├── line-stats.js      ← 极速：仅行统计（性能最优）
    ├── rich-inline.js     ← 富文本：@提及/标签布局
    ├── wrap-layout.js     ← 进阶：文本绕排浮动元素
    ├── render-dom.js     ← 🆕 DOM 渲染（Accordion/Chat/Masonry）
    ├── particle-text.js   ← 🆕 粒子自由运动（Canvas 动画）
    ├── clear-cache.js     ← 工具：清除内部缓存
    └── install-deps.js    ← 工具：自动安装依赖
```

---

## 📖 场景示例

### 示例 1：虚拟滚动初始化

```javascript
// 用户：有 1000 条消息，每条宽 375px，帮我算总高度
// AI 调用：
node scripts/batch.js \
  --items "消息1内容..." \
  --items "消息2内容..." \
  --font "14px -apple-system" \
  --width 375

// 返回：{ totalHeight: 28400, averageHeight: 28.4, itemCount: 1000 }
```

### 示例 2：判断文本会不会溢出

```javascript
// 用户："这段文字在 300px 宽下会换行吗？"
// AI 调用：
node scripts/line-stats.js \
  --text "这是一段可能比较长的文本内容" \
  --font "16px Inter" \
  --width 300

// 返回：{ lineCount: 2, analysis: { verdict: "会换行 2 行" } }
```

### 示例 3：Canvas 绘制代码生成

```javascript
// 用户：这段文字想在 Canvas 里居中绘制，帮我算坐标
// AI 调用：
node scripts/layout-lines.js \
  --text "Hello World！" \
  --font "20px Inter" \
  --width 600 \
  --lineHeight 28

// 返回逐行坐标信息 + Canvas 绘制代码模板
```

### 示例 4：DOM 渲染（Accordion / Chat Bubbles）

生成可直接粘贴到浏览器的 HTML 片段，无需触碰真实 DOM 测量：

```bash
# 生成 HTML 片段
node scripts/render-dom.js \
  --text "小兔子睡不着，看见窗外有一艘发光的月亮船..." \
  --font "17px sans-serif" \
  --width 400 \
  --lineHeight 34

# 生成带动画效果的代码（逐字高亮）
node scripts/render-dom.js \
  --text "欢迎使用 Pretext！" \
  --width 300 \
  --output snippet

# 分析文本行数（JSON 输出）
node scripts/render-dom.js \
  --text "多行文本内容" \
  --width 400 \
  --output json
```

作为模块使用：

```javascript
const { renderToDOM, renderAccordion, renderChatBubbles } = require('./scripts/render-dom');

// Accordion 示例
const result = renderAccordion([
  { title: "月亮船", text: "小兔子睡不着...", duration: 300 },
  { title: "小海龟", text: "奇奇第一次旅行...", duration: 300 },
], '16px sans-serif', 400, 24);

// result.accordionHtml → 直接渲染到页面即可
// result.totalClosedHeight / totalOpenHeight → 精确高度预知
```

### 示例 5：文字粒子自由运动

每个字符变成物理粒子，在 Canvas 上自由飘动，用鼠标推开：

```bash
# 生成粒子动画 HTML（直接用浏览器打开）
node scripts/particle-text.js \
  --text "你好，世界！Hello World! 🎉" \
  --font "32px sans-serif" \
  --width 800 \
  --height 500

# 分析粒子数量
node scripts/particle-text.js \
  --text "欢迎来到 Pretext 世界！" \
  --output info

# 自定义风格
node scripts/particle-text.js \
  --text "Pretext 粒子引擎" \
  --bg "#1a0a2e" \
  --color "#C77DFF" \
  --mouseRadius 150
```

---

## 🌍 多语言支持

| 语言类型 | 支持情况 | 示例 |
|:---|:---|:---|
| 中文（CJK） | ✅ | `你好，世界！` — 按字换行 |
| 日文 | ✅ | `こんにちは、世界！` |
| 韩文 | ✅ | `안녕하세요, 세상아!` |
| 英文 | ✅ | `Hello, World!` |
| Emoji | ✅ | `🚀 🌟 💯` — 完整组合序列 |
| 混合语言 | ✅ | `Hello 世界 123 🎉` |

> ⚠️ 暂不支持 RTL 语言（阿拉伯文、希伯来文）。

---

## ⚠️ 已知限制

1. **macOS `system-ui` 字体**：精度不稳定，建议使用具名字体
2. **字体必须预加载**：`prepare()` 时字体需已安装
3. **CSS 支持有限**：仅 `white-space: normal/pre-wrap`、`word-break: normal/keep-all`
4. **不支持**：混合字号、内联图片、伪元素

---

## 📄 开源协议

本 Skill 基于 MIT 协议开源项目构建。

- **@chenglou/pretext**：MIT License — [GitHub](https://github.com/chenglou/pretext)
- **node-canvas**：MIT License — [GitHub](https://github.com/Automattic/node-canvas)
- **Skill 封装层**：MIT License

详见 `LICENSES.md`。

---

## 🤝 贡献 & 反馈

遇到问题或有功能建议？欢迎提交 Issue！

本 Skill 会跟随上游 `@chenglou/pretext` 更新，请定期 `npm update`。

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
- 开发者不对因使用本 Skill 造成的任何直接或间接损失负责。
- 不同操作系统/浏览器环境下实际宽度可能存在 ±5% 误差，此为正常现象。

