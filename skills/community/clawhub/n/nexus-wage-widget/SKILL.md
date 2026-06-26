---
name: nexus-wage-widget
description: >
  工作日薪看板 Pro — 实时工资计算 + 番茄钟专注的玻璃质感 HTML widget。
  这是用户的个人生产力工具，存在于 references\daily_wage.html。
  当用户提及"工作日薪"、"工资看板"、"daily_wage"、"番茄钟"、"专注时刻"、桌面 widget 或玻璃质感卡片时，必须使用本 skill。
  本 skill 包含该文件的完整架构、视觉规范、交互逻辑和核心代码，任何 bot 都能据此准确还原。
agent_created: true
version: 1.0.0
---

# 工作日薪看板 Pro — 完整还原指南

本文件是 `daily_wage.html` 的权威参考。路径：`references\daily_wage.html`

## 文件概述

一个单文件 HTML+CSS+JS 桌面 widget，含：
- **实时工资计算**：根据时间/月薪/工时实时计算今日已赚
- **番茄钟专注时刻**：25 分钟倒计时，浏览器通知
- **7 种视觉主题**：极客暗夜、爱马仕橙、总裁黑金、烂漫少女、东方木漏、极简白昼、赛博霓虹
- **两种布局**：横向宽版（PC）和方形液态版（手机/小屏）
- **偏好设置**：弹窗模态框，可调整月薪/工时/主题/透明度等，保存到 localStorage

## 核心规格参数

### 字体
- 中文：`Noto Sans SC`（fonts.loli.net CDN，**不是** Google Fonts）
- 等宽：`Source Code Pro`
- 字体 px 值**只能用偶数**（如 12px、14px、24px、32px），不能用单数
- 该规则**仅限 font-size**，padding/margin/border 等不受限

### 视觉主题（7 个 data-theme）
每个主题通过 CSS 变量 `--variant` 覆盖：
1. **dark** — 默认，深紫渐变
2. **hermes** — 爱马仕橙金
3. **girly** — 粉红少女
4. **business** — 黑金奢华
5. **zen** — 蓝绿禅意
6. **light** — 极简白昼
7. **cyber** — 荧光赛博

每个主题覆盖 15 个 CSS 变量：`--bg-grad`, `--glass-bg`, `--glass-border`, `--glass-highlight`, `--text-main`, `--text-sub`, `--accent-money`, `--accent-money-soft`, `--accent-focus`, `--accent-other`, `--panel-bg`, `--panel-hover`, `--ambient-1`, `--ambient-2`, `--ambient-3`, `--progress-shimmer`, `--shadow-soft`, `--shadow-strong`

### Glass Card 样式
- `--glass-opacity`: 0.4（默认），可设置，CSS 变量
- `--glass-blur`: 24px（默认），可设置
- 圆角 28px，多层 box-shadow（环境光 + 高光线）
- `::before` 伪元素顶部边缘高光

### 面板（.w-panel）
- 圆角 20px，内边距 18px，`overflow: hidden`
- 悬停时轻微上移、边框显色、阴影加深

### 布局

#### 宽屏 PC（.widget-wide，默认，>900px）
- `max-width: 740px`
- 3 列 2 行网格：
  - 时间（1/3, 跨 2 行）：等宽大字体 `clamp(36px, 5.5vw, 48px)`，冒号闪烁动画
  - 今日已赚（2/3, 第 1 行）：等宽绿色大字 `clamp(40px, 6.5vw, 52px)`，发光动画
  - 进度条（2/3, 第 2 行）：水平排列，左侧专注时刻面板 + 右侧进度条
  - 天气（3/3, 第 1 行）：竖排图标+温度，建议使用bot定时抓取当天天气 weather.json 给daily_wage.html调用
  - 发薪倒计时（3/3, 第 2 行）：竖排天数

#### 手机/方形（.widget-square, ≤900px）
- `max-width: 340px`，竖排 flex
- 今日已赚大字 `clamp(46px, 9vw, 60px)`
- 2×2 网格按钮（发薪 + 专注时刻）
- 底部进度条，水平显示起止时间

**响应式断点**：单断点 900px。>900px = PC 版，≤900px = 手机版

### 专注时刻面板（Pomodoro）

**宽屏版**（`id="focus-wide"`）：
- 宽度：**112px**，内边距：**12px**
- 标题「专注时刻」：14px → 激活后 12px（**仅 PC 模式缩小，手机模式标题不变**）
- 倒计时数字：激活后 24px 等宽紫字 `--accent-focus`
- 子文本：未激活时「点击开始」12px

**方形版**（`id="focus-sq"`）：
- 倒计时数字：激活后 **32px**
- 未激活时图标 +「专注」文字

**激活状态**：`.pom-active` 类 → 边框 `--accent-focus` + 紫色光晕 box-shadow

**交互逻辑**（IIFE 闭包 `var Pom`）：
- `toggle()` → 启动/停止 25 分钟倒计时
- 激活时图标 ▶ → ⏸（svg 多边形 ↔ 矩形对），两端同时切换
- 每 200ms 刷新显示
- 到点时：浏览器 Notification + 标题栏闪烁 5 秒（🔔专注时间到！↔ 工作日薪看板）

### 设置弹窗（Modal）
- 点击右下角齿轮按钮打开
- 参数：展示组件（宽版/方形）、视觉主题、月薪、发薪日、上下班时间、透明度、模糊度
- 实时预览：切换主题即时生效
- 保存到 localStorage，键名前缀 `widget_`（如 `widget_theme`, `widget_salary`）

### 配置数据（`Config` 对象）
```js
{
  theme, widgetType, salary, startTime, endTime, payday, glassOpacity, glassBlur,
  getDailyData() { /* 计算 dailySalary, startSec, endSec, totalWorkSec, salaryPerSec */ }
}
```
- 月工作日数：21.75 天
- 已赚金额 = (当前秒数 - 上班秒数) × (日薪 / 总工作秒数)

### 实时更新循环
```js
function loop() {
  updateWidget();
  requestAnimationFrame(loop);
}
```

### 动画清单
- `breathe` / `breathe2` — 环境光呼吸
- `shimmer` — 进度条流光
- `pulse-dot` — 工作状态指示灯脉冲
- `colon-blink` — 时间冒号闪烁
- `money-glow` — 金额发光
- `float-btn` — 设置按钮呼吸
- `subtle-float` — 微浮动
- `gradient-shift` — 渐变位移
- 尊重 `prefers-reduced-motion: reduce`

### 进度条
- 高度 6px，圆角 3px
- 填充渐变 `--accent-other → --accent-money` + 阴影
- 流光伪元素 `::after`

### 代码风格约定
- JS 使用 IIFE 闭包模式，**不使用 class / this**
- 所有 CSS font-size px 值必须为**偶数**
- 文件位置：`references\daily_wage.html`
- CDN：fonts.loli.net（Google Fonts 国内镜像），不能用 fonts.googleapis.com

## 新建指南（从零还原）

如果需要在另一台机器重新创建：

1. 创建单文件 HTML，CDN 用 `fonts.loli.net`
2. 7 个主题完整覆盖 18 个 CSS 变量
3. 玻璃质感卡片结构：`.glass-card` + `.w-panel` + 环境光 `.ambient-light` × 3
4. 网格布局 strict 3×2（PC）/ 1 列（手机）
5. 进度条水平排列，专注时刻面板在左侧
6. Pomodoro IIFE 闭包实现，共享状态机
7. 设置弹窗 + localStorage 持久化
8. `requestAnimationFrame` 实时更新循环
9. 所有 font-size 用偶数

**引用源文件**：若用户询问细节，直接读取 `references\daily_wage.html` 获取精确代码。