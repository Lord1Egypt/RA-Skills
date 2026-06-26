# 设计系统规范

所有颜色、字体、间距必须严格使用下列定义，不要自创。

## 1. 基础色板

### 背景色
```css
body:              #0a0e1a                          /* 最外层底色 */
slide background:  linear-gradient(135deg, #0f1629 0%, #1a1f3a 50%, #0f1629 100%)
slide border:      1px solid rgba(100, 140, 255, 0.15)
slide shadow:      0 20px 80px rgba(0, 0, 0, 0.5), 0 0 60px rgba(80, 120, 255, 0.08)
slide glow (::before): radial-gradient(circle, rgba(80, 120, 255, 0.06) 0%, transparent 70%)
```

### 文字色
```css
主文本:        #e0e6f0
次要文本:      #8899bb / #7788aa
辅助文字:      #5a6a8a / #3a4a6a
白高光:        #ffffff
```

### 主题色（必须成对使用）

| 主题 | 主色 | 次色 | 文字色 | 背景 rgba |
|---|---|---|---|---|
| 蓝（Blue / Reach 层） | `#5070ff` | `#7cacff` | `#a0b4ff` | `rgba(80,112,255,0.12)` |
| 紫（Purple / Agent 层） | `#7c3aed` | `#a78bfa` | `#c4b5fd` | `rgba(124,58,237,0.12)` |
| 绿（Green / User 层、Now） | `#10b981` | `#34d399` | `#6ee7b7` / `#95d5b2` | `rgba(16,185,129,0.12)` |
| 橙（Orange / Support、Next） | `#ea580c` / `#f59e0b` | `#fbbf24` | `#fed7aa` / `#fcd34d` | `rgba(234,88,12,0.12)` |
| 灰（Gray / Cloud 层 / Baseline） | `#475569` / `#64748b` | `#94a3b8` | `#cbd5e1` | `rgba(100,116,139,0.15)` |
| 红（Red / 警示 / 成本增加） | `#ef4444` | `#fb923c` | `#fca5a5` / `#fecaca` | `rgba(239,68,68,0.08)` |

### 渐变（Gradient）
```css
标题渐变（白紫蓝）:    linear-gradient(135deg, #ffffff 0%, #7cacff 50%, #a78bfa 100%)
小标题强调（蓝紫）:    linear-gradient(135deg, #5070ff, #a78bfa)
用户层标签:           linear-gradient(135deg, #2d6a4f, #40916c)
触达层标签:           linear-gradient(135deg, #5070ff, #3a5ce0)
Agent 层标签:        linear-gradient(135deg, #7c3aed, #6d28d9)
支撑层标签:           linear-gradient(135deg, #c2410c, #ea580c)
云产品层标签:         linear-gradient(135deg, #475569, #64748b)
红色数值:            linear-gradient(135deg, #fca5a5, #ef4444)
橙红百分比:          linear-gradient(135deg, #fb923c, #ef4444)
```

## 2. 字体

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

从 Google Fonts 引入 Inter：
```html
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
```

## 3. 字号层级

| 用途 | 字号 | font-weight |
|---|---|---|
| 封面大标题 | 52px | 800 |
| 封面副标题 | 20~22px | 400 |
| slide 编号 | 12px | 600 |
| slide 主标题 | 34~36px | 700 |
| slide 副标题 | 15px | 400 |
| 区块标题（H3）| 17~20px | 700 |
| 卡片标题 | 15~17px | 700 |
| 数值大字 | 26~52px | 800 |
| 正文 | 13~14px | 400~500 |
| 标签/tag | 11~12px | 600~700 |
| footer | 11px | 400 |

## 4. 间距 & 容器

```css
slide 宽度:        1280px（固定）
slide 最小高度:    720px
slide padding:     60px 70px（封面） / 40px 50px（内容页）
slide 上下边距:    margin: 40px auto
slide 圆角:        border-radius: 20px

卡片圆角:          14~16px
小组件圆角:        8~10px
按钮/标签圆角:     4~8px

gap 规范:
  slide 内部区块间:  20~32px
  卡片网格 gap:      16~24px
  图标与文字:         6~10px
```

## 5. 组件通用样式

### 卡片基础
```css
background: rgba(255,255,255,0.03);
border-radius: 14~16px;
border: 1px solid rgba(255,255,255,0.06~0.08);
padding: 20~28px;
```

### 卡片 hover 效果（可选）
```css
transition: transform 0.2s;
&:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
```

### 左侧彩色条（storyline 专用）
```css
.storyline::before {
  content: '';
  position: absolute; left: 0; top: 0; bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, <主色>, <次色>);
}
```

## 6. Footer（每个 slide 必加）

```html
<div class="slide-footer">
  <span>品牌名 / 主题名</span>
  <span>N / Total</span>
</div>
```

```css
position: absolute;
bottom: 20px;
left: 70px; right: 70px;
display: flex; justify-content: space-between; align-items: center;
color: #3a4a6a;
font-size: 11px;
```

## 7. 打印优化（必加）

```css
@media print {
  body { background: #fff; }
  .slide { box-shadow: none; border: 1px solid #ddd; }
}
```

## 8. 图标用法

- **首选** Unicode 几何符号：`&#9733;` ★  `&#9881;` ⚙ `&#9889;` ⚡ `&#10140;` ➜ `&#10145;` ➡ `&#8644;` ⇄ `&#128221;` 📝
- **禁用**彩色 emoji 表情（😀🎉💡 这类）
- 文字汇报中图标用 24~40px，放在卡片左上作为视觉引导

## 9. CSS 变量系统（v2.0+）

从 v2.0 起，所有颜色/间距/字号统一用 CSS custom properties 管理。

### 使用方式
```css
/* 引用变量 */
color: var(--color-blue);
background: var(--bg-card);
border-radius: var(--card-radius);
```

### 亮色主题切换
```html
<!-- 暗色（默认） -->
<body>

<!-- 亮色（投影仪友好） -->
<body class="light">
```

### 完整变量清单
见 `components/base-template.html` 的 `:root` 块。改色只需改这一个地方。

## 10. 交互能力（v2.0+）

- **键盘翻页**：↑↓←→ 和空格键切换 slide
- **导航圆点**：右侧 fixed 定位，JS 自动根据 .slide 数量生成
- **进度条**：顶部 3px 渐变条，滚动时自动更新
- **入场动画**：IntersectionObserver threshold=0.3 触发 fadeInUp
- **PDF 导出**：右上角按钮调 window.print()
- **主题切换**：右上角按钮 toggle body.light class
