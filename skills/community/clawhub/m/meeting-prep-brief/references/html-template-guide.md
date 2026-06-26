# 会前材料 HTML 模板设计规范

本文档提供会前材料 HTML 的完整设计规范和代码参考，确保每次生成的材料风格统一、专业美观。

## 1. 页面基础结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{会议主题}} — 会前材料 | {{会议时间}}</title>
<style>
  /* 完整 CSS 见下方 */
</style>
</head>
<body>
<div class="container">
  <!-- Header -->
  <!-- Section 1..N -->
  <!-- Footer -->
</div>
</body>
</html>
```

## 2. 完整 CSS 样式表

```css
/* ===== 重置 & 基础 ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: #f5f5f7;
  color: #1d1d1f;
  line-height: 1.7;
  padding: 40px 20px;
}
.container { max-width: 900px; margin: 0 auto; }

/* ===== Header 标题区 ===== */
.header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #fff;
  padding: 48px 40px;
  border-radius: 16px;
  margin-bottom: 32px;
}
.header h1 { font-size: 28px; font-weight: 700; margin-bottom: 8px; }
.header .subtitle { font-size: 15px; color: rgba(255,255,255,0.7); }
.header .meta {
  margin-top: 20px;
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}
.header .meta-item {
  background: rgba(255,255,255,0.12);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
}
.header .meta-item strong { color: #64b5f6; }

/* ===== Section 白色卡片 ===== */
.section {
  background: #fff;
  border-radius: 14px;
  padding: 36px 40px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.section h2 {
  font-size: 20px;
  font-weight: 700;
  color: #0f3460;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e8ecf1;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section h2 .icon {
  width: 28px; height: 28px;
  background: #0f3460;
  color: #fff;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700;
  flex-shrink: 0;
}
.section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 20px 0 10px;
}

p, li { font-size: 14.5px; color: #333; }
p { margin-bottom: 12px; }
ul, ol { padding-left: 20px; margin-bottom: 14px; }
li { margin-bottom: 6px; }

/* ===== Highlight Box (Callout) ===== */
/* 默认蓝色 */
.highlight-box {
  background: #f0f4ff;
  border-left: 4px solid #3b6fd4;
  padding: 16px 20px;
  border-radius: 0 10px 10px 0;
  margin: 16px 0;
}
/* 绿色变体 - 正面/利好信息 */
.highlight-box.green {
  background: #f0faf4;
  border-left-color: #2e9e5e;
}
/* 橙色变体 - 注意/警告 */
.highlight-box.amber {
  background: #fffbf0;
  border-left-color: #d4920b;
}
/* 红色变体 - 紧急/风险 */
.highlight-box.red {
  background: #fff5f5;
  border-left-color: #d44b4b;
}
.highlight-box p:last-child { margin-bottom: 0; }
.highlight-box .label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 6px;
  letter-spacing: 0.5px;
}
.highlight-box.green .label { color: #2e9e5e; }
.highlight-box.amber .label { color: #d4920b; }
.highlight-box.red .label { color: #d44b4b; }

/* ===== Table 表格 ===== */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 14px;
}
th, td {
  padding: 10px 14px;
  text-align: left;
  border-bottom: 1px solid #eee;
}
th {
  background: #f7f8fa;
  font-weight: 600;
  color: #555;
  font-size: 13px;
}

/* ===== Checklist 待确认事项 ===== */
.checklist { list-style: none; padding-left: 0; }
.checklist li {
  padding: 10px 16px;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 8px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 14.5px;
}
.checklist li .checkbox {
  width: 20px; height: 20px;
  border: 2px solid #c0c5ce;
  border-radius: 4px;
  flex-shrink: 0;
  margin-top: 2px;
}
.checklist li strong { color: #0f3460; }

/* ===== Tag 彩色标签 ===== */
.tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  margin-right: 6px;
}
.tag.blue   { background: #e8f0fe; color: #1a5dab; }
.tag.green  { background: #e6f7ed; color: #1a7a42; }
.tag.orange { background: #fff3e0; color: #b86e00; }
.tag.purple { background: #f3e8ff; color: #6b21a8; }
.tag.red    { background: #fee2e2; color: #b91c1c; }

/* ===== Two Column Layout ===== */
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin: 16px 0;
}
.col-card {
  background: #f9fafb;
  border-radius: 10px;
  padding: 18px 20px;
}
.col-card h4 {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #0f3460;
}

/* ===== Divider 分割线 ===== */
.divider { height: 1px; background: #e8ecf1; margin: 24px 0; }

/* ===== Footer 页脚 ===== */
.footer {
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-top: 32px;
}

/* ===== Responsive 响应式 ===== */
@media (max-width: 640px) {
  .two-col { grid-template-columns: 1fr; }
  .header .meta { flex-direction: column; gap: 8px; }
  .section { padding: 24px 20px; }
}

/* ===== Print 打印优化 ===== */
@media print {
  body { background: #fff; padding: 20px; }
  .section { box-shadow: none; border: 1px solid #eee; }
}
```

## 3. 组件使用示例

### 3.1 Header 标题区

展示会议核心信息：主题、副标题、时间/对方/我方等元数据。

```html
<div class="header">
  <h1>{{会议主题}} — 会前材料</h1>
  <div class="subtitle">{{副标题/补充说明}}</div>
  <div class="meta">
    <div class="meta-item"><strong>会议时间</strong>&nbsp;&nbsp;{{时间}}</div>
    <div class="meta-item"><strong>对方</strong>&nbsp;&nbsp;{{对方机构}}</div>
    <div class="meta-item"><strong>我方</strong>&nbsp;&nbsp;{{我方机构/团队}}</div>
  </div>
</div>
```

### 3.2 Section 内容卡片

每个独立模块用一个 `.section` 卡片包裹，`h2` 带编号图标。

```html
<div class="section">
  <h2><span class="icon">1</span>{{模块标题}}</h2>
  <!-- 内容：表格、段落、列表、highlight-box 等 -->
</div>
```

### 3.3 基本面信息表格

适用于展示机构/赛事/会议的基本面信息（key-value 格式）。

```html
<h3>赛事基本面</h3>
<table>
  <tr><th style="width:160px">全称</th><td>{{全称}}</td></tr>
  <tr><th>主办方</th><td>{{主办方}}</td></tr>
  <tr><th>面向对象</th><td>{{描述}}</td></tr>
  <tr><th>规模</th><td>{{数据}}</td></tr>
</table>
```

### 3.4 对比表格

适用于选题方向对比、合作方式对比等。

```html
<table>
  <tr><th style="width:60px">方向</th><th>选题参考</th><th>切入点</th></tr>
  <tr>
    <td><span class="tag purple">A</span></td>
    <td><strong>{{选题名}}</strong></td>
    <td>{{描述}}</td>
  </tr>
  <!-- 更多行... -->
</table>
```

### 3.5 Highlight Box (Callout)

四种颜色分别对应不同语义：

```html
<!-- 蓝色（默认）：一般备注/说明 -->
<div class="highlight-box">
  <p><strong>备注：</strong>{{内容}}</p>
</div>

<!-- 绿色：正面信息/利好 -->
<div class="highlight-box green">
  <div class="label">与我方直接相关</div>
  <p>{{内容}}</p>
</div>

<!-- 橙色：注意事项/警告 -->
<div class="highlight-box amber">
  <div class="label">需要注意</div>
  <p>{{内容}}</p>
</div>

<!-- 红色：紧急/风险 -->
<div class="highlight-box red">
  <div class="label">风险提醒</div>
  <p>{{内容}}</p>
</div>
```

### 3.6 Tag 标签

用于标注人员/分类/优先级等。

```html
<span class="tag blue">腾讯 — 张三</span>
<span class="tag green">已确认</span>
<span class="tag orange">待定</span>
<span class="tag purple">方向A</span>
<span class="tag red">紧急</span>
```

### 3.7 Checklist 待确认事项

核心模块——会上需要确认的问题清单，用 checkbox 样式呈现。

```html
<h3 style="color: #d44b4b;">一、{{分类名}}（紧急确认）</h3>
<ul class="checklist">
  <li>
    <span class="checkbox"></span>
    <div><strong>{{问题标题}}：</strong>{{具体需要确认的内容和追问方向}}</div>
  </li>
  <!-- 更多条目... -->
</ul>
```

**Checklist 分级建议：**
- 🔴 紧急确认项（h3 颜色 `#d44b4b`）— 今天必须得到答案
- 🟢 探讨了解项（h3 颜色 `#2e9e5e`）— 了解情况，不一定要定论
- 🔵 后续跟进项（h3 颜色 `#1a5dab`）— 建立联系，后续推进

### 3.8 Two-Column 双列卡片

适合并排对比两个机会/方案。

```html
<div class="two-col">
  <div class="col-card">
    <h4><span class="tag green">机会 A</span> {{标题}}</h4>
    <p style="font-size:13px; color:#555;">{{时间地点}}</p>
    <ul style="font-size:13.5px;">
      <li><strong>形式：</strong>{{描述}}</li>
      <li><strong>价值：</strong>{{描述}}</li>
    </ul>
  </div>
  <div class="col-card">
    <h4><span class="tag orange">机会 B</span> {{标题}}</h4>
    <!-- 同上结构 -->
  </div>
</div>
```

### 3.9 Footer 页脚

```html
<div class="footer">
  整理于 {{日期}} · 会议前准备材料 · 内部使用
</div>
```

## 4. 设计原则清单

| 原则 | 说明 |
|------|------|
| **信息层级清晰** | Header → Section 卡片 → h3 子标题 → 内容，层次分明 |
| **颜色语义一致** | 蓝=一般, 绿=正面, 橙=注意, 红=紧急, 紫=分类/方向 |
| **数据用表格** | 基本面信息、对比分析一律用表格，不写长段落 |
| **重点用 Callout** | 关键发现、风险提示用 highlight-box 突出 |
| **行动项用 Checklist** | 待确认事项全部 checklist 化，方便会后逐项打勾 |
| **留白适当** | 卡片间 24px 间距，内容不要太密 |
| **移动端兼容** | max-width 900px + 响应式媒体查询 |
| **打印友好** | @media print 去掉阴影、换白底 |

## 5. 内容模块选用指南

根据会议类型，选择需要的模块组合：

| 模块 | 合作洽谈 | 项目评审 | 产学研对接 | 商务拜访 |
|------|:--------:|:--------:|:----------:|:--------:|
| 对方背景速览 | ✅ | ⬜ | ✅ | ✅ |
| 核心议题/关键信息 | ✅ | ✅ | ✅ | ⬜ |
| 合作机会分析 | ✅ | ⬜ | ✅ | ✅ |
| 选题/方案建议 | ✅ | ✅ | ✅ | ⬜ |
| 合作切入思路 | ✅ | ⬜ | ✅ | ✅ |
| 待确认事项清单 | ✅ | ✅ | ✅ | ✅ |
| 沟通策略备忘 | ✅ | ⬜ | ✅ | ✅ |
