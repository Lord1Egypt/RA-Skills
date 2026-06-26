---
name: nexus-642things
description: 生成「642件可写的小事」H5 创意写作应用。当用户说「642」「创意写作」「写作灵感」「642件事」「写作应用」「生成写作H5」时触发。Bot 直接生成完整单文件 H5 应用，无需用户提供额外信息。
agent_created: true
---

# nexus-642things — 642件可写的小事 H5 应用生成器

根据标准设计 prompt，由 bot 直接生成完整单文件 H5 创意写作应用（`642-things-to-write.html`），零外部依赖，可直接在浏览器运行。

---

## 触发词

用户说以下任意关键词时触发本 skill：

- 642件事 / 642件可写的小事
- 创意写作应用 / 写作灵感 / 写作H5
- 生成642 / nexus-642things

---

## 工作流程（Bot 直接执行）

### Step 1：确认输出路径

默认输出到当前工作区的 `data/642-things-to-write.html`。若用户指定路径则使用用户路径。

### Step 2：按规范生成完整 HTML 文件

按照以下完整产品规范直接生成单文件 H5 应用，写入输出路径。

---

## 完整产品规范

### 产品定位

- **目标用户**：文艺青年、写作爱好者、创意写作者
- **品牌调性**：温暖文艺 × 咖啡馆氛围 × 灵感激发
- **核心体验**：低压力创作——无字数要求、无体裁限制、无时间限制
- **平台**：移动端 H5（max-width: 440px 居中），兼容 iOS/Android 浏览器

---

### 设计系统

#### 配色 — Coffee Roast 暖琥珀系

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#F7F1E8` | 页面底色，暖米白 |
| `--bg-warm` | `#F0E6D4` | 次级背景，提示区/标签底色 |
| `--card` | `rgba(255,255,255,0.72)` | 毛玻璃卡片背景 |
| `--card-solid` | `#FFFFFF` | 实色卡片（写作面板） |
| `--accent` | `#B8703F` | 主强调色，琥珀 |
| `--accent-deep` | `#8B4C1A` | 深琥珀，渐变终点 |
| `--accent-glow` | `rgba(184,112,63,0.18)` | 强调色光晕 |
| `--sage` | `#7B8B6F` | 鼠尾草绿，成功/保存/次要强调 |
| `--sage-light` | `#A8B89C` | 浅鼠尾草 |
| `--text` | `#3D2B1F` | 主文字，深暖棕 |
| `--text-mid` | `#6B5744` | 次级文字 |
| `--text-light` | `#9C8B7A` | 辅助文字 |
| `--text-faint` | `#C4B8A8` | 极淡文字/占位符 |
| `--border` | `rgba(61,43,31,0.08)` | 卡片边框 |
| `--border-strong` | `rgba(61,43,31,0.15)` | 按钮边框 |

#### 阴影

| Token | 值 | 用途 |
|-------|-----|------|
| `--shadow-sm` | `0 2px 8px rgba(61,43,31,0.06)` | 小卡片 |
| `--shadow-md` | `0 8px 32px rgba(61,43,31,0.08)` | 主卡片 |
| `--shadow-lg` | `0 16px 48px rgba(61,43,31,0.10)` | 写作面板 |
| `--shadow-glow` | `0 0 40px rgba(184,112,63,0.12)` | 题目卡片光晕 |

#### 圆角

| Token | 值 | 用途 |
|-------|-----|------|
| `--radius-sm` | `10px` | 按钮/小卡片 |
| `--radius` | `18px` | 主卡片 |
| `--radius-lg` | `28px` | 大面板 |

#### 排版 — Editorial 混排

| Token | 值 | 用途 |
|-------|-----|------|
| `--font-display` | `'Noto Serif SC', 'Source Han Serif SC', 'STSong', 'SimSun', Georgia, serif` | 标题/题目文字 |
| `--font-body` | `-apple-system, 'PingFang SC', 'Noto Sans SC', 'Helvetica Neue', sans-serif` | 正文/按钮 |
| `--font-mono` | `'SF Mono', 'Fira Code', 'Consolas', monospace` | 数字/代码 |

排版层级：
- 页面标题：32px / 700 / serif / 渐变色
- 题目文字：20px / 600 / serif / line-height 1.8
- 按钮文字：15px / 600 / sans-serif
- 正文：14-15px / 400 / sans-serif / line-height 1.8-2
- 辅助文字：11-12px / 500 / 浅色

---

### 图标系统 — Lucide Inline SVG

**禁止使用 emoji 作为图标**。所有图标使用 Lucide 风格的 inline SVG，定义在 JS 对象 `L` 中，通过 `data-icon` 属性 + DOM 注入脚本渲染。

图标清单：

| 名称 | Lucide 对应 | 尺寸 | 使用位置 |
|------|------------|------|----------|
| `sparkle` | sparkles (单星) | 14×14 | 题目徽章、发现页亮点 |
| `btnShuffle` | shuffle | 18×18 | 换一题按钮 |
| `btnPen` | pen-line | 18×18 | 开始写按钮 |
| `navShuffle` | shuffle | 22×22 | 底部导航·灵感 |
| `navBook` | book-open | 22×22 | 底部导航·作品 |
| `navLightbulb` | lightbulb | 22×22 | 底部导航·发现 |
| `titleBook` | book-open | 20×20 | 发现页标题 |
| `titleTarget` | target | 20×20 | 贴士标题 |
| `titleCollection` | book-open | 20×20 | 作品集标题 |
| `writePen` | pen-line | 17×17 | 写作面板标题 |
| `x` | x | 16×16 | 关闭按钮 |
| `fileEdit` | file-edit | 48×48 | 空状态插画 |
| `trash2` | trash-2 | 14×14 | 删除按钮 |
| `actionPen` | pen-line | 16×16 | 空状态CTA |

渲染机制：
```html
<!-- HTML 中使用 data-icon 属性 -->
<span class="icon" data-icon="btnShuffle"></span>

<!-- JS 中定义 SVG -->
const L = { btnShuffle: `<svg ...>...</svg>`, ... };

<!-- 页面加载时注入 -->
document.querySelectorAll('[data-icon]').forEach(el => {
  const name = el.getAttribute('data-icon');
  if (L[name]) { el.innerHTML = L[name]; el.removeAttribute('data-icon'); }
});
```

---

### 页面结构

#### 三个 Tab 页

| Tab | 图标 | 标签 | 内容 |
|-----|------|------|------|
| 灵感 | shuffle | 首页 | 统计 + 进度 + 题目卡片 + 操作按钮 + 写作面板 |
| 作品 | book-open | 作品集 | 作品列表 / 空状态 |
| 发现 | lightbulb | 发现 | 关于这本书 + 写作贴士 |

#### 底部导航栏

- 毛玻璃效果：`backdrop-filter: blur(20px)` + 半透明背景
- 活跃项：图标弹性放大 `scale(1.15) translateY(-2px)` + 顶部渐变指示条
- 适配 safe-area-inset-bottom

---

### 组件规范

**1. 氛围层（Atmosphere）**
- 浮动光斑：两个 `radial-gradient` 椭圆，amber + sage 色，20s/25s 缓慢漂移动画
- 纸张纹理：SVG `feTurbulence` fractalNoise，2.5% 透明度叠层
- 均为 `position: fixed; pointer-events: none`

**2. 页头（Header）— Editorial 风格**
- Eyebrow 文字：11px / 500 / uppercase / letter-spacing 4px / sage 色
- 主标题：serif 32px / "642" 渐变色（accent → accent-deep）
- 副标题：serif 14px / italic / text-light
- 装饰线：40px 宽渐变条（accent → sage）
- 全部带错落渐入动画（0.1s-0.4s delay）

**3. 统计卡片（Stats Row）**
- 3 列 grid，Glassmorphism 卡片（blur 16px + 半透明 + border）
- 数值：serif 28px / 700 / 渐变色；标签：11px / 500 / text-light
- 点击缩放反馈

**4. 进度条（Progress）**
- 标签 + 分数（mono 字体）
- 5px 高轨道，渐变填充（accent → sage）
- 弹簧过渡 `cubic-bezier(0.34,1.56,0.64,1)`

**5. 题目卡片（Prompt Card）— 核心组件**
- Glassmorphism：blur 20px + 半透明 + border + shadow-md + shadow-glow
- 顶部 3px 渐变光带（shimmer 动画，3s 循环）
- 右上角 sparkle 装饰（12% 透明度，hover 25% + 旋转）
- 题号徽章：渐变背景 + 白色文字 + 圆角 20px
- 题目文字：serif 20px / 600 / line-height 1.8
- 标签：bg-warm 底色 + border + 圆角 14px
- 换题时 shake 动画 + 文字淡入淡出

**6. 操作按钮（Actions）**
- 双按钮横排：secondary（白底+边框）+ primary（渐变+光晕阴影）
- 涟漪点击效果（radial-gradient 跟随点击位置）
- 弹簧缩放 `scale(0.96)`

**7. 写作面板（Write Panel）**
- 弹入动画：`translateY(30px) scale(0.97)` → 原位
- 题目提示条：bg-warm 底色 + 左侧 3px accent 竖线
- 文本区：bg 底色 + 聚焦时 accent 光晕边框
- 保存按钮：sage 渐变 + 阴影

**8. 作品卡片（Work Item）**
- Glassmorphism 卡片
- 题目：serif 13px / accent 色 + 左侧 2px 竖线
- 内容：4 行截断，点击展开
- 删除按钮：trash-2 图标 + hover 红色

**9. 空状态（Empty State）**
- 大图标（48px）+ gentleFloat 浮动动画
- 引导文案 + CTA 按钮（accent 渐变）

**10. 发现页（Discover）**
- 关于这本书：book-open 图标 + serif 标题
- 亮点区：sage 左竖线 + 三个 sparkle 标签**横排**（flex + gap 16px + wrap）
- 写作贴士：target 图标 + 箭头列表（`→` accent 色）

---

### 动效体系

| 动效 | 实现 | 用途 |
|------|------|------|
| 错落渐入 | `fadeSlideUp/Down` + 递增 delay | 页头、统计、卡片、按钮 |
| 弹簧缩放 | `cubic-bezier(0.34,1.56,0.64,1)` | 按钮点击、统计更新、面板弹入 |
| Shake | 多段位移+旋转 | 换题卡片抖动 |
| Shimmer | `background-position` 动画 | 题目卡片顶部光带 |
| GentleFloat | `translateY` 往复 | 空状态图标浮动 |
| StaggerIn | 递增 delay 的 fadeSlideUp | 作品列表逐项渐入 |
| 涟漪 | radial-gradient 跟随点击 | 按钮点击反馈 |
| 浮动光斑 | translate + scale 往复 | 背景氛围 |
| 页面切换 | opacity + translateY 过渡 | Tab 切换 |

---

### 功能逻辑

**数据存储**
- 使用 `localStorage`，key：`642_works`（作品数组）、`642_used`（已写题目索引数组）
- 作品结构：`{ id, promptIndex, promptText, content, wordCount, time, date }`

**题目系统**
- 内置 120+ 道精选创意写作题，覆盖书中多种风格
- 每题含 `text`（题目文字）和 `tags`（标签数组，如 `["拟人", "日常"]`）
- 随机选题优先选**未写过的题**
- 换题时关闭写作面板

**统计系统**
- 已写篇数、总字数、连续天数（streak）
- 创作进度：已写不同题数 / 642
- 数值更新时弹跳动画

**写作功能**
- 点击"开始写"展开写作面板，显示当前题目提示
- 实时字数统计
- 保存后记录到 localStorage，更新统计和进度

**作品集**
- 按时间倒序展示
- 内容默认 4 行截断，点击展开
- 支持删除（confirm 确认）
- 空状态显示引导 CTA

---

### 技术约束

1. **单文件**：所有 HTML + CSS + JS 内联，零外部依赖（无 CDN、无框架）
2. **图标**：Lucide 风格 inline SVG，通过 `data-icon` + JS 注入，**禁止 emoji**
3. **移动优先**：max-width 440px 居中，适配 safe-area-inset
4. **无障碍**：语义化 HTML，按钮可聚焦，文字对比度达标
5. **性能**：CSS 动画优先，避免 JS 连续操作 DOM 布局
6. **兼容**：`-webkit-` 前缀（backdrop-filter、text-fill-color、line-clamp 等）

---

## Step 3：预览

生成完成后，调用 `preview_url` 工具打开 HTML 文件展示给用户。

---

## 注意事项

- **本 skill 由 bot 全程自动完成**，无需调用任何外部脚本，直接生成 HTML 文件
- 题目内容（120+题）需 bot 自行创作，覆盖日常/感官/回忆/想象/拟人/对话等多风格
- 每次生成可适当丰富或调整题目内容，保持多样性
- 已有参考实现：`data/642-things-to-write.html`（2026-05-07 首次生成）
