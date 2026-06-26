# 行业分析 HTML 渲染 · 图表建议

> 这是 HTML 渲染官 调 visual-page skill 时的"图表映射"参考。每个维度对应最适合的可视化形式。

---

## 1. 头部企业 → 排序表 + 重点卡片

### 形式

- **顶部**：完整 Top 10 排序表（横向滚动）
- **中部**：Top 3 重点公司卡片（公司名 + 营收 + 主营 + 1 个亮点）

### 数据结构

```javascript
{
  type: "table",
  data: [
    { rank: 1, name: "公司A", revenue: "5525 亿", main: "医药商业", share: "15%", source: "年报" },
    // ... 10 家
  ]
}

{
  type: "cards",
  highlight: [1, 2, 3],  // 高亮前 3 名
  fields: ["name", "revenue", "main", "highlight"]
}
```

### 视觉建议

- Top 1-3 配色突出（金/银/铜 或 1-2-3 高亮色）
- 其余 4-10 灰色淡化
- 鼠标悬停显示完整备注

---

## 2. 生态图谱 → SVG 关系图

### 形式

- 1 个 SVG 流程图，覆盖 4 生态位 + 关键公司
- 实线 = 上下游关系
- 虚线 = 横向支持关系

### 数据结构

```javascript
{
  type: "svg-flowchart",
  direction: "TB",  // TB=自上而下 LR=左右
  groups: [
    { name: "上游", items: [{id: "A1", label: "原料A"}, {id: "A2", label: "组件B"}] },
    { name: "中游", items: [{id: "B1", label: "制造C"}] },
    { name: "下游", items: [{id: "C1", label: "应用D"}] },
    { name: "横向支持", items: [{id: "D1", label: "IT"}], dashed: true }
  ],
  links: [
    { from: "A1", to: "B1", type: "solid" },
    { from: "D1", to: "B1", type: "dashed" }
  ]
}
```

### 视觉建议

- 4 生态位用 4 种背景色区分
- 关键公司用大节点（圆角矩形）
- 实线 = 主供应链关系
- 虚线 = 横向支持关系
- 鼠标悬停显示公司全名

---

## 3. 数字化方案 → 对比表 + 卡片墙

### 形式

- **4 大厂**：横向对比表（厂商为行，要素为列）
- **垂直厂商**：卡片墙（每厂商 1 张卡）

### 数据结构

```javascript
{
  type: "comparison-table",
  vendors: [
    {
      name: "华为",
      logo: "huawei.svg",
      products: [
        { name: "方案 X", target: "三甲医院上云", differentiator: "端边云协同", case: "北京协和" }
      ],
      positioning: "医疗云领先"
    },
    // ... 4 大厂
  ]
}

{
  type: "vendor-cards",
  verticals: [
    { name: "卫宁健康", products: "...", differentiator: "...", case: "..." }
  ]
}
```

### 视觉建议

- 4 大厂用品牌色（华为红/阿里橙/百度蓝/腾讯青）
- 卡片墙 3-4 列网格
- 每张卡片含：logo / 方案名 / 1 句话差异化 / 1 个客户案例

---

## 4. 行业机会 → 政策 Timeline + 趋势 Cards

### 形式

- **政策 timeline**：横向时间轴，按发布时间排序
- **需求场景 / 痛点**：列表 + 标签
- **未来趋势**：3-5 个 trend cards

### 数据结构

```javascript
{
  type: "timeline",
  events: [
    { date: "2024-01", title: "政策A", department: "国务院", impact: "重大" },
    { date: "2024-08", title: "政策B", department: "卫健委", impact: "中等" }
    // ...
  ]
}

{
  type: "trend-cards",
  trends: [
    { name: "AI 医疗影像", window: "中期 1-3 年", drivers: ["技术成熟", "政策支持"], winners: ["联影", "推想"] }
    // ...
  ]
}
```

### 视觉建议

- Timeline 用横向滚动条
- 政策按时间从左到右
- 重要政策用大节点（标红/标金）
- 趋势 cards 用图标 + 文字

---

## 5. 整体页面建议

### 配色

- 主色：#1E3A8A（深蓝，专业感）
- 辅色：#F59E0B（橙金，强调）
- 背景：#FFFFFF / #F9FAFB（淡灰）
- 文字：#1F2937（深灰）

### 字体

- 中文：PingFang SC / 思源黑体
- 英文：Inter / SF Pro
- 数字：Roboto Mono

### 布局

- 单列流式布局（max-width: 1200px）
- 顶部 Hero 区域（行业名 + 时间窗 + 摘要）
- 每节用 80-100px padding
- 节标题用 H2，44px，深蓝色
- 子标题 H3，28px
- 段落行高 1.7

### 交互

- 顶部固定导航条（节锚点跳转）
- 数据表格可滚动
- 图表鼠标悬停显示详情
- 移动端响应式（< 768px 切换单列）

### 底部

- 源文件清单（5 个 md + session.json）
- 数据缺口汇总
- 生成时间 + session_id
