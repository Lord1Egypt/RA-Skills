# Pretext Skill 发布信息

---

## 🗂️ ClawHub 填表信息

| 表单字段 | 填写内容 |
|:---|:---|
| **Skill 名称** | pretext |
| **Slug** | pretext-text-measurement |
| **版本号** | 1.0.0 |
| **许可证** | MIT |
| **作者** | QiuZhenPeng |
| **分类** | Developer Tools / Frontend / Text Processing |
| **标签**（Tags） | text-measurement, layout, frontend, virtual-scroll, canvas, chinese-text, i18n, nodejs, ai-ui |
| **Icon / Emoji** | 📐 |
| **GitHub 地址** | https://github.com/chenglou/pretext |
| **价格** | 免费（Free） |
| **是否开源** | ✅ 是（基于 MIT） |
| **是否收费** | ❌ 否 |

### ClawHub 短简介（≤80 字符）

```
无需 DOM，纯算术计算任意文字在指定宽度下的像素高度与行数。
支持中文、CJK、emoji，零依赖极速运行。
```

### ClawHub 完整产品简介

```
## 📐 Pretext — 精准文本测量与布局引擎

> 「不需要 DOM reflow，不需要 setTimeout，不需要把文字渲染出来再量——直接算出来。」

### 这个 Skill 能解决什么问题？

当你开发虚拟滚动列表、聊天应用、AI 生成 UI、Canvas 文本渲染等场景时，必须提前知道每段文字会占据多高。

传统方案要么渲染后量（慢），要么字数估算（不准）。

Pretext 的解法：**提前一次性测量每个字符的宽度，之后纯算术遍历——O(n) 时间，零 DOM 操作，结果与浏览器渲染高度一致。**

### 核心能力

- **计算高度**：输入文本 + 字体 + 宽度 → 输出精确像素高度
- **判断换行**：返回总行数 + 每行具体内容
- **批量测量**：一次测量 1000 条消息（比 DOM 快 300–600 倍）
- **逐行坐标**：输出每行的起止位置（用于 Canvas 绘制）
- **富文本布局**：支持 @提及、代码块、标签等内联样式
- **DOM 渲染片段**：生成可直接粘贴的逐行 HTML，无需触碰真实 DOM

### 支持语言

中文、CJK（中日韩）、emoji、英文等所有 Unicode 文本。

> ⚠️ 暂不支持 RTL 语言（阿拉伯文、希伯来文）。

### 安装要求

- Node.js v16+
- 可选：`npm install canvas` — 安装后精度更高，未安装不影响基础功能

### 性能数据

| 方案 | 500 条批量测量耗时 |
|:---|---:|
| DOM getBoundingClientRect | 250–1500ms |
| **Pretext（本 Skill）** | **0.09ms** |

### 开源协议

MIT License — 基于 `@chenglou/pretext`（GitHub 42K Stars）
```

### ClawHub 免责声明

```
### ⚠️ 免责声明

**本 Skill 以「现状」（AS IS）提供，不附带任何明示或暗示的保证。**

#### 测量精度
- 文本高度与行数的计算结果为估算值，实际渲染可能因字体渲染引擎、内嵌字体等因素产生偏差。
- 在精确像素级 UI 开发场景中，建议以浏览器实际渲染结果为准。
- 安装 `canvas` 可显著提升精度；未安装时使用纯 JS Unicode 估算模式，功能完整但精度略低。
- 不同操作系统/浏览器环境下实际宽度可能存在 ±5% 误差，此为正常现象。

#### 版权与许可
- 本 Skill 基于 MIT 协议开源项目 `@chenglou/pretext` 构建，版权归原作者 Cheng Lou 所有。
- 本 Skill 封装层（SKILL.md + scripts/*）版权归属 Skill 作者，遵循相同 MIT License。

#### 使用限制
- 不得用于任何非法用途。
- 开发者不对因使用本 Skill 造成的任何直接或间接损失负责。
```

---

## 🗂️ WorkBuddy 技能市场填表信息

| 表单字段 | 填写内容 |
|:---|:---|
| **名称** | pretext |
| **版本** | 1.0.0 |
| **图标** | 📐 |
| **许可证** | MIT |
| **作者** | QiuZhenPeng |
| **分类** | 前端开发 / 文本处理 |
| **标签** | text-measurement, layout, frontend, virtual-scroll, canvas, chinese-text, i18n |
| **价格** | 免费 |
| **是否开源** | ✅ |

### WorkBuddy 简介（description_zh，≤100 字）

```
精准文本测量与布局引擎，基于 GitHub 42K Stars 的开源项目 @chenglou/pretext。
无需 DOM，快速计算任意文本在指定宽度/字体下的像素高度与行数，支持中文、CJK、emoji 等多语言。
```

### WorkBuddy 英文简介（description_en，≤100 字）

```
Accurate text measurement and layout engine powered by @chenglou/pretext.
Zero DOM, pure arithmetic. Calculate text height and line count for any font/width.
Supports Chinese, CJK, emoji.
```

---

## 🗂️ 通用产品简介（官网/文档用）

**Pretext — 精准文本测量与布局引擎**

你是否遇到过这些场景？

- **虚拟滚动**：列表渲染前不知道每条消息多高，插入新消息后滚动位置突然跳走
- **AI 生成 UI**：LLM 生成的代码文本溢出容器，布局全乱
- **Canvas 绘制**：Canvas 里没有 `getBoundingClientRect`，不知道文字该从哪里画到哪里
- **SSR 服务端**：Node.js 里无法测量文本高度

传统解法要么 DOM 渲染后量（慢、有副作用），要么字数估算（不准）。

**Pretext 的解法：**

1. `prepare()` — 一次性测量每个字符的宽度，存进内存
2. `layout()` — 输入宽度，纯算术遍历宽度数组，O(n) 返回总高度和行数
3. 结果与浏览器渲染高度一致，零 DOM 操作

**速度对比：**

| 方案 | 500 条批量耗时 |
|:---|---:|
| DOM getBoundingClientRect | 250–1500ms |
| **Pretext** | **0.09ms** |

**为什么选择 Pretext Skill？**

- 基于 `@chenglou/pretext`（42K Stars）官方库，逻辑零修改
- 内置 8 个场景化脚本，从「基础测量」到「粒子动画」开箱即用
- 支持浏览器 100% 精度模式（Canvas API）和 Node.js 快速模式
- 完整中文文档 + 交互式演示页面
- MIT 协议，完全免费

---

## ⚠️ 完整免责声明

---

## 📦 基本信息

| 字段 | 内容 |
|:---|:---|
| **名称** | pretext |
| **版本** | 1.0.0 |
| **图标** | 📐 |
| **许可证** | MIT |
| **作者** | QiuZhenPeng |
| **主页** | https://github.com/chenglou/pretext |
| **标签** | text-measurement, layout, frontend, virtual-scroll, canvas, chinese-text, i18n |

---

## 📝 市场简介（WorkBuddy / ClawHub 通用）

### 短简介（≤50 字）

> 精准文本测量引擎，无需 DOM 即可计算任意文字在指定宽度下的像素高度与行数。支持中文、CJK、emoji 等多语言。

### 标准简介（≤200 字）

**Pretext — 精准文本测量与布局引擎**

基于 GitHub 42K Stars 的开源项目 `@chenglou/pretext` 构建，无需触碰 DOM，纯算术计算文本像素高度与行数。

**能做什么：**
- 计算一段文字在指定宽度和字体下的精确高度
- 判断文字是否会换行，输出每行的具体内容
- 批量测量列表中每一条消息的高度（虚拟滚动必备）
- 支持富文本内联布局（@提及、代码块、标签等）
- 文本绕排浮动元素的变宽布局
- 生成可直接粘贴到浏览器的逐行 HTML 片段

**支持语言：** 中文、CJK（中日韩）、emoji、英文等所有 Unicode 文本。

### 详细简介（展示页用）

**Pretext — 精准文本测量与布局引擎**

> 「不需要 DOM reflow，不需要 setTimeout，不需要把文字渲染出来再量——直接算出来。」

`@chenglou/pretext` 是由 React Native 核心贡献者 Cheng Lou 开发的高性能文本测量库，在 GitHub 上拥有超过 42,000 颗星，被广泛应用于 React Native、Figma、VR 界面等高性能 UI 场景。

**为什么需要 Pretext？**

在构建聊天列表、虚拟滚动、AI 生成 UI、Canvas 动画等场景时，你必须提前知道每段文字会占据多高。传统方案要么用 DOM 渲染后量（慢、有副作用），要么用粗糙的字数估算（不准）。

Pretext 的解法是：**提前一次性测量每个字符的宽度存在内存里，之后纯算术遍历——O(n) 时间复杂度，零 DOM 操作，结果与浏览器渲染高度一致。**

**核心 API：**
- `prepare()` — 预处理文本，建立字符宽度映射（一次）
- `layout()` — 输入宽度，计算总高度和行数（无数次，极快）
- `measureNaturalWidth()` — 测量任意字符串的自然宽度

**适用场景：**
- 虚拟滚动 / 聊天消息列表（必须预先知道每条高度）
- AI 生成 UI 布局预计算（LLM 输出 JSON UI 之前先量好）
- Canvas 文本绘制（逐字定位、光标渲染）
- Accordion / Chat Bubbles / Masonry 布局（内容高度预知，零回流）
- 任意需要精确文本高度的前端或后端场景

> **注意：** 本 Skill 暂不支持 RTL（从右到左）语言（如阿拉伯文、希伯来文）。如需相关支持，请参考 [@chenglou/pretext](https://github.com/chenglou/pretext) 原版文档。

**安装可选 `canvas` 依赖以获得高精度，未安装时自动降级为纯 JS Unicode 估算模式，功能完整但精度略低。**

---

## 🔧 安装要求

- **Node.js**：v16+
- **可选依赖**：`canvas`（node-canvas）— 安装后精度更高；Windows/Linux/macOS 均可安装，安装失败不影响基础功能

---

## ⚠️ 免责声明

**本 Skill 以「现状」（AS IS）提供，不附带任何明示或暗示的保证。**

### 测量精度

- 文本高度与行数的计算结果为**估算值**，实际渲染结果可能因浏览器字体渲染、内嵌字体、自定义字形、操作系统字体引擎等因素而产生偏差。
- 在对布局精度要求极高的场景（如精确像素级 UI 开发）中，建议以浏览器实际渲染结果为准，本 Skill 提供的数值仅供参考。
- 安装 `canvas` 可显著提升测量精度；未安装时使用纯 JS Unicode 估算模式，功能完整但精度略低。
- 不同操作系统/浏览器环境下实际宽度可能存在 **±5%** 误差，此为正常现象。

### 版权与许可

- 本 Skill 基于 MIT 协议开源项目 `@chenglou/pretext` 构建，版权归原作者 Cheng Lou（[@chenglou](https://github.com/chenglou)）所有。
- 详细许可信息见 [LICENSES.md](./LICENSES.md)。
- 本 Skill 封装层（SKILL.md + scripts/*）版权归属 Skill 作者，遵循相同 MIT License。

### 使用限制

- 本 Skill 不得用于任何非法用途。
- 开发者不对因使用本 Skill 造成的任何直接或间接损失负责，包括但不限于：数据丢失、业务中断、布局错误导致的 UI 问题、测量误差造成的显示异常。
- 本 Skill 的测量结果不构成任何设计或法律建议。

### 第三方依赖

- `@chenglou/pretext`：MIT License（见 [LICENSES.md](./LICENSES.md)）
- `canvas`（可选）：[node-canvas](https://github.com/Automattic/node-canvas)，GPL/FreeType License

---

## 📄 开源许可原文

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
