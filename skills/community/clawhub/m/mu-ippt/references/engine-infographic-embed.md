# engine-infographic-embed.md — Infographic 截图嵌入 PPT 引擎

> 当 PPT 页面需要**漏斗图/时间线/SWOT/KPI卡片**等信息图时，使用本引擎。
> 适用场景：静态 SVG 模板无法满足（如复杂分层漏斗、多节点时间线），或用户明确要求"信息图风格"。

---

## 何时用本引擎 vs 直接 SVG

| 场景 | 推荐方案 |
|------|---------|
| 纯结构示意（流程箭头/关系图） | 直接手绘 SVG（executor-base.md） |
| 需要复杂漏斗/时间线/SWOT/KPI仪表盘 | **本引擎**（infographic → PNG → 嵌入） |
| 数据驱动图表（柱/折线/散点） | engine-vega.md |

---

## 执行流程

### Step 1：选模板

查询绘图虾的模板列表获取模板名（无需本地文件，直接用模板名）：

常用模板速查：
- 漏斗：`funnel` / `funnel-4step` / `funnel-wide`
- 时间线：`timeline` / `timeline-vertical` / `roadmap`
- SWOT：`swot` / `swot-grid`
- KPI卡片：`kpi-card` / `kpi-3col` / `metric-dashboard`
- 对比：`pros-cons` / `compare-3col`
- 层级：`org-tree` / `pyramid-5`

完整列表见绘图虾 `references/infographic-templates.md`（按需 read）。

### Step 2：准备数据

按模板的 items 结构填写数据，例如 funnel：
```json
{
  "template": "funnel",
  "title": "转化漏斗",
  "items": [
    {"label": "曝光", "value": "100万"},
    {"label": "点击", "value": "10万"},
    {"label": "注册", "value": "1万"},
    {"label": "付费", "value": "1千"}
  ]
}
```

### Step 3：渲染截图

使用 browser automation tool 访问 Markdown Viewer 渲染并截图：

```bash
# 构造渲染 URL（infographic 模板通过 ?template= 参数指定）
RENDER_URL="https://your-infographic-renderer.example.com/infographic?template=funnel&data=<urlencode(json)>"

# 截图保存
browser automation tool screenshot "$RENDER_URL" --output /tmp/infographic-<page>.png --width 1200 --height 800
```

### Step 4：嵌入 SVG 页面

将截图作为图片素材，通过 PPT大师的图片嵌入管线（image-layout-spec.md）放入页面：

```xml
<!-- 在 SVG 中嵌入截图 -->
<image href="data:image/png;base64,<base64>" x="80" y="100" width="1120" height="520" />
```

- 截图占比建议：页面高度的 60-75%，留空间给标题和说明
- 位置：居中放置，上方留 120px 给标题

### Step 5：后处理

正常走 finalize_svg.py 流程（图标嵌入等）；infographic 截图已是 PNG，无需额外处理。

---

## 注意事项

- infographic 渲染需要 browser automation tool（有网络依赖），超时重试最多 2 次
- 截图分辨率 ≥ 1200px 宽，否则文字模糊
- 每页只嵌入一张 infographic，不要多图堆砌
- 嵌入后该页不再手绘其他 SVG 元素（防止风格冲突）
