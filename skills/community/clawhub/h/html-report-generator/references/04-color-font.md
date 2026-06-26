# 04 · 配色与字体系统

---

## 语义色（全报告固定，不随页面变化）

```css
/* 功能色 — 表达状态，所有模板通用 */
--danger:  #ef4444;   /* 威胁、失败、高风险、攻击 */
--warning: #f59e0b;   /* 警告、中等风险、注意 */
--success: #10b981;   /* 通过、安全、正常、防御有效 */
--info:    #3b82f6;   /* 信息、中性数据 */
--neutral: #94a3b8;   /* 辅助文字、次级信息 */
```

---

## 7 套主题配色方案

每页从下表选一套，同一份报告中同一套配色不得连续使用超过 3 页。

### 方案 1 · 执行摘要（蓝）

```css
:root {
  --p:    #3b82f6;
  --pm:   rgba(59,130,246,0.13);
  --bg:   #0a0f1e;
  --card: #0f1629;
  --bd:   rgba(59,130,246,0.22);
  --t:    #e2e8f0;
  --mt:   #94a3b8;
  --dt:   #64748b;
}
```

**适用页面：** 执行摘要、概览、结论

---

### 方案 2 · 攻击/风险（红）

```css
:root {
  --p:    #ef4444;
  --pm:   rgba(239,68,68,0.12);
  --bg:   #130505;
  --card: #1f0808;
  --bd:   rgba(239,68,68,0.22);
  --t:    #fef2f2;
  --mt:   #fca5a5;
  --dt:   #ef4444;
}
```

**适用页面：** 攻击原理、风险分析、威胁描述

---

### 方案 3 · 威胁/预警（橙）

```css
:root {
  --p:    #f59e0b;
  --pm:   rgba(245,158,11,0.12);
  --bg:   #130e02;
  --card: #1f1604;
  --bd:   rgba(245,158,11,0.22);
  --t:    #fffbeb;
  --mt:   #fcd34d;
  --dt:   #d97706;
}
```

**适用页面：** 威胁预警、应急响应、事件分析

---

### 方案 4 · 防御/安全（绿）

```css
:root {
  --p:    #10b981;
  --pm:   rgba(16,185,129,0.11);
  --bg:   #03120a;
  --card: #061d10;
  --bd:   rgba(16,185,129,0.22);
  --t:    #f0fdf4;
  --mt:   #6ee7b7;
  --dt:   #059669;
}
```

**适用页面：** 防御方案、安全加固、合规建议

---

### 方案 5 · 技术/原理（紫）

```css
:root {
  --p:    #8b5cf6;
  --pm:   rgba(139,92,246,0.13);
  --bg:   #08041a;
  --card: #110828;
  --bd:   rgba(139,92,246,0.22);
  --t:    #f5f3ff;
  --mt:   #c4b5fd;
  --dt:   #7c3aed;
}
```

**适用页面：** 技术原理、算法实现、数学推导

---

### 方案 6 · 数据/分析（青）

```css
:root {
  --p:    #06b6d4;
  --pm:   rgba(6,182,212,0.11);
  --bg:   #021318;
  --card: #041e24;
  --bd:   rgba(6,182,212,0.22);
  --t:    #ecfeff;
  --mt:   #67e8f9;
  --dt:   #0891b2;
}
```

**适用页面：** 数据分析、统计报表、检测评估

---

### 方案 7 · 趋势/展望（粉）

```css
:root {
  --p:    #f472b6;
  --pm:   rgba(244,114,182,0.12);
  --bg:   #130410;
  --card: #1f081c;
  --bd:   rgba(244,114,182,0.22);
  --t:    #fdf4ff;
  --mt:   #f0abfc;
  --dt:   #c026d3;
}
```

**适用页面：** 趋势展望、未来预测、路线规划

---

## 配色与视觉模板的搭配

| 视觉模板 | 推荐配色方案 | 说明 |
|---------|-----------|------|
| T1 暗色精品 | 任意方案均可 | 模板本身决定暗色背景 |
| T2 编辑分割 | 方案 2/3/4/5 | 强调色用于色彩条和标签 |
| T3 终端代码 | 固定使用 GitHub Dark，强调色叠加 | 不使用上述 `--bg/--card` |
| T4 数据仪表（亮） | 替换为：bg:`#f0f4f8`，card:`#fff` | 主色 `--p` 保留 |
| T5 极简文字 | 替换为：bg:`#fafaf8`，card:`#fff` | 单色原则：只用 `--p` |

---

## T3 终端配色（固定值，不使用主题变量）

```css
/* GitHub Dark 调色板 */
--term-bg:      #0d1117;
--term-surface: #161b22;
--term-header:  #21262d;
--term-border:  #30363d;
--term-text:    #c9d1d9;
--term-dim:     #8b949e;
--term-muted:   #484f58;

/* 语法高亮 */
--syn-keyword:  #ff7b72;
--syn-function: #d2a8ff;
--syn-string:   #a5d6ff;
--syn-number:   #79c0ff;
--syn-comment:  #8b949e;
--syn-variable: #ffa657;

/* 状态色 */
--term-ok:   #3fb950;
--term-warn: #d29922;
--term-err:  #f85149;
--term-info: #58a6ff;
```

---

## T2 编辑分割配色（双区）

| 报告主题 | 左栏背景 | 右栏背景 | 强调色条 |
|---------|---------|---------|---------|
| 攻击/风险 | `#111827` | `#f8f7f3` | `#dc2626` → `#ef4444` |
| 防御/安全 | `#0a1a12` | `#f7faf8` | `#059669` → `#10b981` |
| 技术/原理 | `#0e0a1e` | `#f9f8ff` | `#7c3aed` → `#8b5cf6` |
| 数据/分析 | `#021318` | `#f0fcff` | `#0891b2` → `#06b6d4` |
| 趋势/展望 | `#130410` | `#fdf4ff` | `#c026d3` → `#f472b6` |

---

## 字体规则

### 系统字体栈（主力，覆盖中文）

```css
/* 中英文混排通用 */
font-family: 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', 'Hiragino Sans GB', sans-serif;

/* 数字/代码 */
font-family: 'SF Mono', 'Fira Code', Consolas, monospace;
```

### Google Fonts（T1 专用）

```html
<!-- 仅在 T1 模板的 <head> 中引入 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
```

```css
/* T1 字体变量 */
--font-display: 'Syne', 'PingFang SC', sans-serif;   /* 大标题 */
--font-body:    'DM Sans', 'PingFang SC', sans-serif; /* 正文 */
```

### 字重用途规范

| 字重 | 用途 |
|------|------|
| 900 | T2/T5 超大标题（页面唯一） |
| 800 | T1 Syne 大标题 |
| 700 | 卡片标题、徽章 |
| 600 | 次级标题、强调标签 |
| 500 | 中等强调 |
| 400 | 正文 |
| 300 | 辅助文字（T1/T5） |

---

## 渐变文字配方（T1 专用）

```css
/* 主色渐变文字 */
.gradient-text {
  background: linear-gradient(135deg, #e2e8f0 30%, VAR_ACCENT);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 危险红渐变 */
.gradient-red    { background: linear-gradient(135deg, #fca5a5, #ef4444); }
/* 蓝紫渐变 */
.gradient-indigo { background: linear-gradient(135deg, #a5b4fc, #6366f1); }
/* 金黄渐变 */
.gradient-amber  { background: linear-gradient(135deg, #fde68a, #f59e0b); }
/* 绿色渐变 */
.gradient-green  { background: linear-gradient(135deg, #6ee7b7, #10b981); }
/* 粉色渐变 */
.gradient-pink   { background: linear-gradient(135deg, #f9a8d4, #f472b6); }
```

---

## 配色配置页面规划参考

```
P01 执行摘要   → 方案1 蓝    T1 暗色精品
P02 核心概念   → 方案5 紫    T2 编辑分割
P03 分类对比   → 方案6 青    T4 数据仪表
P04 技术实现   → 方案5 紫    T3 终端代码
P05 案例分析   → 方案3 橙    T2 编辑分割
P06 风险评估   → 方案2 红    T1 暗色精品
P07 检测评估   → 方案6 青    T4 数据仪表
P08 防御方案   → 方案4 绿    T1 暗色精品
P09 工具框架   → 方案5 紫    T3 终端代码
P10 趋势展望   → 方案7 粉    T5 极简文字
```
