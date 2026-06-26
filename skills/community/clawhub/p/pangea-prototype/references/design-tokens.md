---
inclusion: manual
---

# Pangea Design System Token

> 主题包：`@arco-themes/vue-pangea-3-linear` v1.0.11
>
> 用途：为 AI 大模型提供样式参考，用于生成符合 Pangea 3 Linear 主题规范的 UI 代码

---

## 概述 Overview

这是一个以 **清爽青绿（teal）** 为品牌主色的现代化 UI 主题（Pangea 3 Linear）。整体观感偏 **轻量、干净、理性**：

- **信息层级清晰**：正文与标题使用深色文字（`color-text-1`）在白底上形成明确对比。
- **大面积留白 + 中性灰分割**：容器背景与分割线大多来自中性灰阶（`color-fill-*`、`color-border-*`），强调内容而非装饰。
- **交互强调克制**：主色主要用于 CTA、链接与关键交互态；其余区域以中性色承载。
- **轻投影表达层级**：提供三档投影（Shadow1/2/3），用于浮层、卡片、弹窗等层级区分。

---

## 颜色 Colors

### 品牌色 / 主色

Pangea 3 Linear 主题的品牌色为**青绿色（Teal）**系列，与 Arco Design 默认蓝色不同。

**Less 变量**：`@color-primary-6` = `rgb(var(--primary-6))`

**链接色（link）与主色相同**，`--link-1` ~ `--link-10` 值与 `--primary-*` 一致。

每种颜色有 1-10 共 10 个色阶，1 最浅，10 最深（暗色模式反转）。

通过 `body[arco-theme='dark']` 激活暗色模式，所有 CSS 变量自动切换。

| Token          | 亮色值               | 暗色值               | 说明                                       |
| -------------- | -------------------- | -------------------- | ------------------------------------------ |
| `--primary-1`  | `rgb(232, 255, 251)` | `rgb(0, 68, 77)`     | 浅色背景、白底 hover 背景等                |
| `--primary-2`  | `rgb(173, 238, 228)` | `rgb(4, 92, 100)`    | 文字/图标禁用态（偏浅）                    |
| `--primary-3`  | `rgb(121, 221, 209)` | `rgb(10, 117, 123)`  | 一般禁用态（背景/描边/弱强调）             |
| `--primary-4`  | `rgb(74, 204, 193)`  | `rgb(18, 144, 147)`  | 特殊场景的弱强调（如轻量提示、辅助强调块） |
| `--primary-5`  | `rgb(34, 187, 179)`  | `rgb(27, 170, 167)`  | 关键交互悬浮态                             |
| `--primary-6`  | `rgb(0, 170, 166)`   | `rgb(37, 187, 179)`  | **主色、关键交互、选中态、重点强调**       |
| `--primary-7`  | `rgb(0, 144, 147)`   | `rgb(78, 204, 193)`  | 关键交互点击态                             |
| `--primary-8`  | `rgb(0, 117, 123)`   | `rgb(124, 221, 209)` | 深色                                       |
| `--primary-9`  | `rgb(0, 92, 100)`    | `rgb(176, 238, 228)` | 更深                                       |
| `--primary-10` | `rgb(0, 68, 77)`     | `rgb(235, 255, 251)` | 最深                                       |

### 语义色

#### 边框 / 线（Border / Line）

| Token              | 亮色值                      | 暗色值             | 用途                          |
| ------------------ | --------------------------- | ------------------ | ----------------------------- |
| `--color-border-1` | `rgb(242,243,245)` (gray-2) | `rgb(46,46,48)`    | 浅分割线（弱区隔）            |
| `--color-border-2` | `rgb(229,230,235)` (gray-3) | `rgb(72,72,73)`    | 一般分割线（默认边框）        |
| `--color-border-3` | `rgb(201,205,212)` (gray-4) | `rgb(95,95,96)`    | 深/悬浮边框（hover/强调边框） |
| `--color-border-4` | `rgb(134,144,156)` (gray-6) | `rgb(146,146,147)` | 重边框（如按钮描边、强区隔）  |

#### 填充色（Fill）

| Token              | 亮色值                        | 暗色值                   | 用途                                            |
| ------------------ | ----------------------------- | ------------------------ | ----------------------------------------------- |
| `--color-bg-white` | `rgb(255,255,255)` (bg-white) | `rgb(246,246,246)`       | 纯白填充                                        |
| `--color-fill-1`   | `rgb(247,248,250)` (gray-1)   | `rgba(255,255,255,0.04)` | 浅填充/禁用背景                                 |
| `--color-fill-2`   | `rgb(242,243,245)` (gray-2)   | `rgba(255,255,255,0.08)` | 常规填充/白底 hover 背景                        |
| `--color-fill-3`   | `rgb(229,230,235)` (gray-3)   | `rgba(255,255,255,0.12)` | 深填充/灰底 hover 背景                          |
| `--color-fill-4`   | `rgb(201,205,212)` (gray-4)   | `rgba(255,255,255,0.16)` | 重填充/特殊场景背景                             |
| `--color-fill-5`   | `rgb(78,89,105)` (gray-5)     | `rgba(255,255,255,0.7)`  | 强调填充（图标、强调文字/特殊场景；需谨慎使用） |

#### 文字颜色（Text）

| Token            | 亮色值                        | 暗色值                  | 用途                                  |
| ---------------- | ----------------------------- | ----------------------- | ------------------------------------- |
| `--color-text-1` | `rgb(29, 33, 41)` (gray-10)   | `rgba(255,255,255,0.9)` | 强调/正文标题（默认正文与标题）       |
| `--color-text-2` | `rgb(78, 89, 105)` (gray-8)   | `rgba(255,255,255,0.7)` | 次强调/正文标题（次级标题、次级正文） |
| `--color-text-3` | `rgb(134, 144, 156)` (gray-6) | `rgba(255,255,255,0.5)` | 次要信息（描述、提示、弱信息）        |
| `--color-text-4` | `rgb(201, 205, 212)` (gray-4) | `rgba(255,255,255,0.3)` | 置灰信息（禁用文案）                  |
| `--color-white`  | `rgb(255,255,255)` (white)    | `rgba(255,255,255,0.9)` | 白色文字（深色背景上的文本）          |

#### 层级背景（Background）

> 注意：亮色模式下所有 bg 层级均为白色，通过 fill 层级区分层次。

| Token              | 亮色值    | 暗色值    | 用途                      |
| ------------------ | --------- | --------- | ------------------------- |
| `--color-bg-1`     | `#ffffff` | `#17171a` | 整体背景                  |
| `--color-bg-2`     | `#ffffff` | `#232324` | 一级容器背景              |
| `--color-bg-3`     | `#ffffff` | `#2a2a2b` | 二级容器背景              |
| `--color-bg-4`     | `#ffffff` | `#313132` | 三级容器背景              |
| `--color-bg-5`     | `#ffffff` | `#373739` | 浮层/下拉弹出框等容器背景 |
| `--color-bg-white` | `#ffffff` | `#f6f6f6` | 纯白背景                  |

#### 功能色（Functional）

- **Success** (`success-6`, #00B42A)：成功状态、正向反馈
  - Hover `success-5` #23C343；Active `success-7` #009A29
  - Light surface `success-1` #E8FFEA
- **Warning** (`warning-6`, #FF7D00)：警示状态
  - Hover `warning-5` #FF9A2E；Active `warning-7` #D25F00
  - Light surface `warning-1` #FFF7E8
- **Danger** (`danger-6`, #F53F3F)：错误、破坏性操作
  - Hover `danger-5` #F76560；Active `danger-7` #CB272D
  - Light surface `danger-1` #FFECE8

### 其他调色板（主色 6 级参考值）

| Token       | 亮色值               |
| ----------- | -------------------- |
| `--gray-1`  | `rgb(247, 248, 250)` |
| `--gray-2`  | `rgb(242, 243, 245)` |
| `--gray-3`  | `rgb(229, 230, 235)` |
| `--gray-4`  | `rgb(201, 205, 212)` |
| `--gray-5`  | `rgb(169, 174, 184)` |
| `--gray-6`  | `rgb(134, 144, 156)` |
| `--gray-7`  | `rgb(107, 119, 133)` |
| `--gray-8`  | `rgb(78, 89, 105)`   |
| `--gray-9`  | `rgb(39, 46, 59)`    |
| `--gray-10` | `rgb(29, 33, 41)`    |

| 色系       | `*-6` 亮色值        | 用途                 |
| ---------- | ------------------- | -------------------- |
| red        | `#f53f3f`           | 错误/危险            |
| orangered  | `#f77234`           | 橙红                 |
| orange     | `#ff7d00`           | 警告                 |
| gold       | `#f7ba1e`           | 金色                 |
| yellow     | `#fadc19`           | 黄色                 |
| lime       | `#9fdb1d`           | 黄绿                 |
| green      | `#00b42a`           | 成功                 |
| cyan       | `#14c9c9`           | 青色                 |
| blue       | `#3491fa`           | 蓝色                 |
| arcoblue   | `#165dff`           | Arco 蓝              |
| purple     | `#722ed1`           | 紫色                 |
| pinkpurple | `#d91ad9`           | 粉紫                 |
| magenta    | `#f5319d`           | 品红                 |
| bluepurple | `rgb(129, 78, 255)` | 蓝紫（智能产品专用） |
| info       | `rgb(22, 93, 255)`  | 信息蓝               |

---

## 字体 Typography

### Font families

- **Headline / Body（拉丁字符）**：Inter
- **CJK 与系统回退**：`apple-system, BlinkMacSystemFont, PingFang SC, Hiragino Sans GB, noto sans, Microsoft YaHei, Helvetica Neue, Helvetica, Arial, sans-serif`

### Font size scale

- Display（运营标题）：56px / 48px / 36px
- Headlines（页面/区块标题）：24px（页面主标题）/ 20px（区块标题/弹窗标题）/ 16px（列表标题/卡片标题）
- Body（正文）：14px（默认正文）/ 13px（表格密集信息、次级正文）
- Labels / Helper（辅助文本）：12px

### Font weight

- 标题：SemiBold(600) 或 Medium(500)
- 正文：Regular(400)
- 标签/控件文案：Medium(500)（少量使用）

### Line height

- Regular：`line-height = font-size * 1.5715`

---

## 阴影 Shadow

| 级别             | 值                              | 用途                              |
| ---------------- | ------------------------------- | --------------------------------- |
| No elevation     | `none`                          | 基础容器、默认卡片                |
| Special shadow   | `0 0 1px rgba(0,0,0,0.3)`       | 极细微描边式投影                  |
| Shadow1（轻）    | `0 0 5px rgba(0,0,0,0.1)`       | Popover/Dropdown/Tooltip、轻卡片  |
| Shadow2（中）    | `0 0 10px rgba(0,0,0,0.1)`      | Modal/Drawer、重要浮层            |
| Shadow3（强）    | `0 0 20px rgba(0,0,0,0.1)`      | 强层级弹窗                        |

每级阴影支持 9 个方向：`center`、`up`、`down`、`left`、`right`、`left-up`、`left-down`、`right-up`、`right-down`

---

## 间距 Token（Spacing）

基于 2px 基准，常用值为 4px 的倍数：

| Token           | 值     | 常用场景   |
| --------------- | ------ | ---------- |
| `@spacing-none` | `0`    | 无间距     |
| `@spacing-1`    | `2px`  | 极小间距   |
| `@spacing-2`    | `4px`  | 最小间距   |
| `@spacing-3`    | `6px`  | 小间距     |
| `@spacing-4`    | `8px`  | 常用小间距 |
| `@spacing-5`    | `10px` |            |
| `@spacing-6`    | `12px` | 常用中间距 |
| `@spacing-7`    | `16px` | 常用大间距 |
| `@spacing-8`    | `20px` |            |
| `@spacing-9`    | `24px` | 区块间距   |
| `@spacing-10`   | `32px` | 大区块间距 |
| `@spacing-11`   | `36px` |            |
| `@spacing-12`   | `40px` |            |
| `@spacing-13`   | `48px` |            |
| `@spacing-14`   | `56px` |            |

---

## 圆角 Token（Border Radius）

| Token                   | CSS 变量                 | 值    | 用途                   |
| ----------------------- | ------------------------ | ----- | ---------------------- |
| `@border-radius-none`   | `--border-radius-none`   | `0`   | 无圆角                 |
| `@border-radius-small`  | `--border-radius-small`  | `2px` | 小圆角（标签等）       |
| `@border-radius-medium` | `--border-radius-medium` | `4px` | 中圆角（按钮、输入框） |
| `@border-radius-large`  | `--border-radius-large`  | `8px` | 大圆角（卡片、弹窗）   |
| `@border-radius-circle` | `--border-radius-circle` | `50%` | 圆形                   |

---

## 过渡动画 Token（Transition）

### 时长

| Token                          | 值     | 用途         |
| ------------------------------ | ------ | ------------ |
| `@transition-duration-1`       | `0.1s` | 极快         |
| `@transition-duration-2`       | `0.2s` | 快速（常用） |
| `@transition-duration-3`       | `0.3s` | 标准（常用） |
| `@transition-duration-4`       | `0.4s` | 慢速         |
| `@transition-duration-5`       | `0.5s` | 极慢         |
| `@transition-duration-loading` | `1s`   | 加载动画     |

### 缓动函数

| Token                                    | 值                              | 用途         |
| ---------------------------------------- | ------------------------------- | ------------ |
| `@transition-timing-function-linear`     | `cubic-bezier(0,0,1,1)`         | 线性         |
| `@transition-timing-function-standard`   | `cubic-bezier(0.34,0.69,0.1,1)` | 标准（默认） |
| `@transition-timing-function-overshoot`  | `cubic-bezier(0.3,1.3,0.3,1)`   | 弹性超出     |
| `@transition-timing-function-decelerate` | `cubic-bezier(0.4,0.8,0.74,1)`  | 减速进入     |
| `@transition-timing-function-accelerate` | `cubic-bezier(0.26,0,0.6,0.2)`  | 加速离开     |

---

## 层级 Token（Z-Index）

| Token                   | 值     | 用途                    |
| ----------------------- | ------ | ----------------------- |
| `@z-index-affix`        | `999`  | 固钉                    |
| `@z-index-popup`        | `1000` | 弹出层（下拉、tooltip） |
| `@z-index-drawer`       | `1001` | 抽屉                    |
| `@z-index-modal`        | `1001` | 模态框                  |
| `@z-index-message`      | `1003` | 消息提示                |
| `@z-index-notification` | `1003` | 通知                    |

---

## 设计规范建议

1. **禁止硬编码颜色**，始终使用 CSS 变量或 Less token
2. **间距使用 4px 倍数**：4、8、12、16、20、24、32px
3. **主色使用**：交互元素用 `primary-6`，hover 用 `primary-5`，active 用 `primary-7`
4. **暗色适配**：使用语义 token（`--color-text-*`、`--color-bg-*`）而非调色板直接值，可自动适配暗色模式
