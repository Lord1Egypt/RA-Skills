# 标准电商经营诊断报告版式 · 母版样式函数说明

母版实现：`../scripts/pdf_layout_kit.py`。它随专家包分发，不依赖创建者电脑的绝对路径。

---

## 一、调色板（固定，勿改）

```python
DARK       = colors.HexColor('#333333')   # 正文
GRAY       = colors.HexColor('#666666')   # 次要文字、图注
LIGHT_GRAY = colors.HexColor('#F5F5F5')   # 表头底色
MID_GRAY   = colors.HexColor('#DDDDDD')   # 表格边框
ACCENT     = colors.HexColor('#2E5AAC')   # 强调（深蓝）
UP_GOOD    = colors.HexColor('#52C41A')   # 涨=好 → 绿
DOWN_BAD   = colors.HexColor('#FF4D4F')   # 跌=坏 → 红
BG_JUDGE   = colors.HexColor('#F2F2F2')   # callout 底色
```

> 注意：这是**报告版式配色**，不是股票行情配色。经营指标一律「好=绿 / 坏=红」，与股市红涨绿跌无关。

---

## 二、样式表（ParagraphStyle）

| 样式名 | 字体 | 字号/行高 | 对齐 | 用途 |
|---|---|---|---|---|
| `DocTitle` | YaHei-Bold | 22 / 28 | LEFT | 首页大标题 |
| `DocMeta` | YaHei | 10 / 14 | LEFT | 报告期、生成日期、数据来源 |
| `Section` | YaHei-Bold | 15 / 22 | LEFT | 「一、二、三…」章节标题，spaceBefore=18 |
| `SubSection` | YaHei-Bold | 11.5 / 17 | LEFT | 「1. 2. 3.」子节标题 |
| `Body` | YaHei | 10 / 16 | **LEFT + firstLineIndent=20** | 正文段落（铁律 1） |
| `BodyLeft` | YaHei | 10 / 16 | LEFT，无缩进 | callout、列表项、不缩进的说明 |
| `Small` | YaHei | 9 / 13 | LEFT | 脚注、口径说明 |
| `Caption` | YaHei | 9 / 13 | CENTER | 图注 |
| `Judge` | YaHei-Bold | 10 / 16 | LEFT | callout 标题行 |
| `TableHeader` | YaHei-Bold | 9.5 / 14 | CENTER | 表头单元格 |
| `TableCell` | YaHei | 9.5 / 14 | CENTER | 数值单元格 |
| `TableCellLeft` | YaHei | 9.5 / 14 | LEFT | 名称/文本单元格 |

**只有 `Body` 带 `firstLineIndent=20`。** 表格、图注、callout 一律不缩进，否则单元格里会出现莫名其妙的左空白。

---

## 三、核心函数

### `section_title(num, title)` / `subsection_title(num, title)`
输出「一、经营总览」「1. 流量结构」。章节号传中文数字，子节传阿拉伯数字。

### `judge(text)` — 经营判断 callout
加粗前缀「经营判断：」+ 结论。用于**给老板的定性判断**，每章最多 1 条。

### `finding(text)` — 关键发现 callout
加粗前缀「关键发现：」+ 事实。用于**数据层面的异常/亮点**，可多条。

> 两种 callout 是版式的一部分，不允许自创第三种标签（如「风险提示：」写成 callout）。风险走正文或独立章节。

### `change_html(current, previous, inverse=False, unit='pct')`
返回带色箭头的 Paragraph。
- `unit='pct'` → 输出百分点差 `↑2.3pp`（用于率类指标：转化率、退款率）
- `unit='num'` → 输出相对变化 `↓18.5%`（用于量类指标：GMV、访客、订单）
- `inverse=True` → **越低越好**的指标反向着色（退款率、跳失率、退货率、客诉率、获客成本）
- `previous == 0` 返回 `-`；变化 <0.001 返回灰色 `—`

### `make_table(data, col_widths, header=True, align='center', first_col_left=False)`
- 所有单元格自动 Paragraph 包裹（支持中文换行）
- 表头浅灰底 + YaHei-Bold，`repeatRows=1`（跨页重复表头）
- 全表 0.5pt `MID_GRAY` 细网格
- `first_col_left=True` → 首列（通常是指标名/SKU 名）左对齐，其余居中
- **列宽合计必须 = 正文宽度**（A4 减左右边距 = 15.5cm 时，col_widths 合计 15.5*cm）

### `chart(path, width=15.5*cm, caption=None)`
- 高度 = `width * 0.38`（铁律 3，允许 0.35~0.40）
- 图不存在时输出 `[图表缺失: xxx.png]` 占位，**不静默跳过**
- caption 用 `Caption` 样式居中

---

## 四、页面设置

```python
doc = SimpleDocTemplate(
    out_path, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title=..., author=''   # 默认留空；需署名时由调用方传入自己的机构名
)
# 正文宽度 = 21 - 2.5*2 = 16cm；图表用 15.5cm 留一点余量
```

A4 正文区高度 ≈ 29.7 - 2 - 2 = 25.7cm。估页公式：
`总页数 ≈ (Σ图表高 + Σ表格高 + Σ正文高) / 25.7 + 1(封面)`

---

## 五、行动建议三段式（固定格式）

```
建议1：验证高退款商品的承诺与实物差异
  目标：T+14 内将测试商品金额退款率从基线下降 5pp
  动作：① 选 2 个高退款规格做详情页信息补强 ② 保留同类规格作对照
       ③ 客服记录退款原因并按周复盘
  观察指标：金额退款率、退款原因、有效订单数
  停止条件：有效订单不足或退款率连续两周未改善，暂停扩量并复核假设
```

- 目标必须可量化（带基线、指标口径和时间）
- 动作必须具体到「谁做什么」，禁止「加强XX」「优化XX」这类空话
- 观察指标必须是能在后台查到的现成指标
- 必须补充停止 / 回滚条件和审批依赖

---

## 六、常见排版事故对照表

| 症状 | 根因 | 修法 |
|---|---|---|
| 中文里数字前后空一大截 | Body 用了 TA_JUSTIFY | 改 TA_LEFT + firstLineIndent=20 |
| 中间夹整页空白 | 大图溢出后紧跟 PageBreak | 删 PageBreak，靠自然分页 |
| 报告 20+ 页 | 图表高宽比 0.5+ | 改 0.35~0.40 |
| 表格右侧被切 | col_widths 合计 > 正文宽 | 按 15.5cm 重新分配 |
| 单元格文字不换行 | 直接传 str 没包 Paragraph | 用 make_table |
| 金额位置空白 | 用了「¥」而字体缺字形 | 改「元」 |
| 退款率上升显示绿色 | 没传 inverse=True | 反向指标加 inverse=True |
| 中文全是方块 | 没注册 TTF 字体 | registerFont YaHei / SimHei |
