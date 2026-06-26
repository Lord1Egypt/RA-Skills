---
name: quant_report
description: |
  量化策略评估报告生成器。读取 Excel 净值数据（策略净值 + 可选品种净值），
  自动计算 20+ 量化指标、生成 12+ 张专业图表，AI 撰写深度分析文字，
  最终输出机构级 PDF（16+ 页）和 Word 策略评估报告。
  触发：用户上传 Excel 净值数据并要求生成策略评估报告、分析报告。
---

# 量化策略评估报告生成器

角色：资深量化分析师。将净值数据转化为机构级策略评估报告。

**架构：Python 计算指标和图表 → AI 撰写深度分析 → Python 排版输出**

## 前置说明

- 所有命令均在 `quant_report` 的**父目录**下执行（即包含 `quant_report/` 文件夹的目录）。
- 用户上传的 Excel 文件放入 `data/` 目录后再运行分析。
- 输出目录默认为 `output/`，PDF 和 Word 报告均生成在此目录下。
- Excel 格式要求：策略净值文件第1列为日期，第2列为净值；品种净值文件第1列为日期，第2列为品种名，第3列为净值。

## 工作流

### Step 1: 运行分析引擎

```bash
python quant_report/run_analysis.py --data data/ --output output/
```

输出 `output/analysis.json` + `output/charts/*.png`。读取 `output/analysis.json` 后进入 Step 2。

> 如直接指定文件路径：
> ```bash
> python quant_report/run_analysis.py --nav data/策略净值.xlsx --variety data/品种净值.xlsx --output output/
> ```

### Step 2: 撰写深度分析

基于 `output/analysis.json` 数据，用 Python 写入 `output/content.json`（避免 JSON 转义问题）：

```python
import json
content = { ... }  # 见下方字段定义
with open(\"output/content.json\", \"w\", encoding=\"utf-8\") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)
```

**重要**：
- 所有文本字段必须是**字符串**类型，不要用列表。
- `suggestions` 必须是 `list[str]`，共 6 条，每条 200-300 字。
- `indicator_evaluations` 必须是 `dict[str, str]`，键为指标名，值为评价文字。
- 每条建议格式：`\"标题——正文内容\"` 或 `\"标题：正文内容\"`。

#### content.json 字段（按报告章节顺序）

| 字段 | 对应章节 | 类型 | 要求 |
|:---|:---|:---|:---|
| `executive_summary` | 一、执行摘要 | str | 3段：策略概况→核心指标→阶段特征+评价 |
| `nav_daily_analysis` | 二、日净值 | str | 识别3-4个运行阶段（时间+收益+波动+回撤） |
| `nav_weekly_analysis` | 二、周净值 | str | 趋势特征、大涨大跌周背景 |
| `nav_monthly_analysis` | 二、月净值 | str | 月度胜率、右偏特征、极端月归因 |
| `nav_yearly_analysis` | 二、年度 | str | 逐年点评+市场环境归因 |
| `indicator_evaluations` | 三、指标表 | dict[str,str] | 10个指标各2-3句评价（见下） |
| `variety_analysis` | 四、品种 | str | 盈利/亏损品种特征+优化建议 |
| `sector_analysis` | 四、板块 | str | 优势/劣势板块+配置建议 |
| `drawdown_analysis` | 五、回撤 | str | 当前状态→历次事件→天数分布→风控建议 |
| `per_10k_analysis` | 六、万元收益 | str | 盈利能力→波动→阶段效率→配置建议 |
| `heatmap_analysis` | 七、热力图 | str | 季节性、连续盈亏区域、近期走势 |
| `rolling_sharpe_analysis` | 八、滚动夏普 | str | 高效期/低迷期特征→操作建议 |
| `cta_comparison` | 九、CTA对比 | str | 与市场均值+头部横向对比+定位 |
| `conclusion` | 十、综合评价 | str | 分维度星级+结论+投资者配置建议 |
| `suggestions` | 十一、改进建议 | list[str] | 6条，每条200-300字 |

#### indicator_evaluations 格式

`dict[str, str]`，10个核心指标的评价说明（每条2-3句）：

```json
{
  \"年化收益率\": \"超越行业平均水平约15个百分点，处于优秀区间。\",
  \"年化波动率\": \"25.37%高于行业建议上限20%，策略以较高波动换取超额收益。\",
  \"最大回撤\": \"当前-19.47%逼近20%机构风控红线，安全边际不足，需加强风控。\",
  \"夏普比率\": \"1.08处于行业良好区间，风险调整后收益具竞争力。\",
  \"卡玛比率\": \"1.41高于行业均值，体现出较强的回撤控制能力。\",
  \"索提诺比率\": \"下行波动控制良好，负收益日的冲击相对可控。\",
  \"日胜率\": \"46.3%低于50%，符合趋势跟踪策略截断亏损让利润奔跑的典型特征。\",
  \"日盈亏比\": \"1.38的盈亏比保障了负胜率下的正期望值。\",
  \"最大连续亏损天数\": \"连续亏损最长X天，需关注持仓周期与止损设置是否匹配。\",
  \"VaR(95%)\": \"单日95%置信区间最大损失为X%，尾部风险在可控范围内。\"
}
```

#### suggestions 示例格式

```json
{
  \"suggestions\": [
    \"提升回撤控制能力——优化动态止损机制：当前最大回撤-19.47%逼近20%的机构风控红线，安全边际严重不足。建议从三个层面优化：(1) 引入基于ATR的自适应止损机制，替代固定百分比止损；(2) 建立账户级别的回撤熔断机制，当净值从近期高点回撤超过12%时强制减仓50%，超过15%时全部清仓；(3) 使用凯利公式动态调整仓位。预期效果：将最大回撤控制在15%以内，卡玛比率提升至1.8以上。\",
    \"增强抗震荡能力——引入市场状态识别模块：...\"
  ]
}
```

### Step 3: 生成报告

```bash
python quant_report/build_report.py \\
  --analysis output/analysis.json \\
  --content output/content.json \\
  --format all
```

- `--format` 可选 `pdf` / `docx` / `all`（默认 all，同时生成 PDF 和 Word）。
- `--output` 可指定输出目录，默认使用 `analysis.json` 中记录的路径。
- 输出：`output/{策略名}_策略评估报告.pdf` 和 `output/{策略名}_策略分析报告.docx`。

也可使用 `main.py` 一键完成 Step 1-3：

```bash
python -m quant_report --data data/ --format all --output output/
```

### Step 4: 验证

读取生成的 PDF 确认排版正常，告知用户输出路径。

## 写作规范

- **引数字**：不说"表现良好"，说"年化27.5%，处于行业前15%"
- **分阶段**：启动期/横盘期/加速期/回调期，含时间和特征
- **做归因**：年度好/差要结合市场环境（商品牛市/震荡市/政策事件）
- **用术语**：截断亏损让利润奔跑、风险调整后收益、趋势跟踪特征
- **有逻辑**：章节间递进，不是孤立数据堆砌

## 行业基准

| 指标 | 行业均值 | 优秀 | 顶尖 |
|:---|:---|:---|:---|
| 年化收益率 | 8-12% | 15-20% | >25% |
| 最大回撤 | -15%~-20% | <-15% | <-10% |
| 夏普比率 | 0.5-0.8 | 1.0-1.5 | >1.5 |
| 卡玛比率 | 0.5-1.0 | 1.5+ | >2.0 |

## CTA 特征识别

- 日胜率<50% + 盈亏比>1 → 趋势跟踪
- 年度收益差异大 → 强趋势依赖
- 连续大涨年 → 商品趋势行情驱动

## 依赖

```bash
pip install pandas numpy matplotlib seaborn reportlab python-docx openpyxl scipy
```

> 中文 PDF 字体说明：`reportlab` 使用内置 `STSong-Light` CID 字体，无需额外安装字体文件，但需确保 `reportlab` 版本 >= 3.6。
