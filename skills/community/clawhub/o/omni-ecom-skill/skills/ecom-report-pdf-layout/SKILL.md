---
name: ecom-report-pdf-layout
description: 电商经营诊断报告的 PDF 排版与版式交付。当需要把生意参谋、光合、退款、客服、粉丝、投放等后台导出的 xls/xlsx 数据，产出「标准电商经营诊断报告版式」的单一 PDF 交付物（含 matplotlib 内嵌图表）时使用。覆盖 reportlab 中文排版三条铁律、版式母版继承、发老板前数据核查流程、交付物页数与占用重试规范。严禁编造数据。
---

# 电商经营诊断报告 · PDF 排版与版式交付

本技能固化「标准电商经营诊断报告版式」。**版式已定版，禁止每次重新设计风格**。自 omni-ecom v1.5.12 起，PDF 是周报、月报、季报、年报、店铺诊断、大促复盘和经营复盘的默认主交付物；当前流程先展示经营摘要与行动，完整数据概览、报表归类和章节映射放入证据附录，不需要用户再次提出格式要求。标题与比较窗口读取报告包的 `task_type/task_profile`，数字来源与公式读取 `claim_ledger`。
适用对象：月报 / 季报 / 诊断报告 / 经营复盘 / 周报定版 PDF。

## 前置闸门

- 先使用 `ecom-diagnosis-core` 完成资料体检、口径锁定、确定性复算和数据质量闸门。
- 使用插件根目录 `scripts/build_report_package.py` 一次生成 `report.json`、`report.md`、`report.pdf` 和 `pdf-delivery.json`；PDF 只消费报告包，不直接读取成员自由文本或旧报告。
- `report.pdf` 至少包含 3 张内嵌图表，使用 `scripts/generate_pdf_report.py` 确定性生成。图表不足、渲染失败、空白页、页数超过 scripts/pdf_layout_policy.py 根据任务与完整内容计算的上限 或哈希不一致均须 fail closed。
- PDF 首页或摘要必须显示报告包中的 `team_version` 和 `version_diff`，让读者能区分专家团升级与客户经营数据变化。
- PDF 证据附录必须完整显示 `expert_participation`：全部六个岗位、实际参与状态、贡献摘要和 handoff 证据；不得只署名总监而隐藏成员是否参与。
- PDF 只能使用 `approved_metrics`、证据 ID 和团长裁决结论。
- `BLOCKED` 时只允许生成数据质量报告或明确标注限制的草稿，不得用版式包装成确定性经营结论。

随包资源（可移植，优先复用）：

- `scripts/pdf_layout_kit.py`：已固化字体、样式、表格、图表、占用检测与 PDF 自检。
- `references/style-master.md`：母版函数和排版事故说明。

不要依赖创建者电脑上的绝对路径或外部样例脚本。

---

## 一、reportlab 中文 PDF 三条铁律（违反即返工）

### 铁律 1：正文严禁 TA_JUSTIFY，必须 TA_LEFT + 首行缩进

```python
styles.add(ParagraphStyle(
    name='Body', fontName='YaHei', fontSize=10, leading=16,
    textColor=DARK,
    alignment=TA_LEFT,        # 铁律：禁止 TA_JUSTIFY
    firstLineIndent=20,       # 铁律：约 2 个中文字符
    spaceAfter=6
))
```

**原因**：reportlab 对中文做两端对齐时，会在字与字之间插入空格撑满行宽。中文句子里夹数字、百分比、英文 SKU 名时，会被撑出异常大的间距，整段看起来像排版事故。
**例外**：表格单元格样式（TableCell / TableHeader）、图注（Caption）、callout 色块内文本 **不加** `firstLineIndent`，仍用 `TA_LEFT` / `TA_CENTER`。

### 铁律 2：禁止滥用 PageBreak()

- 全文 `PageBreak()` 总数 **0~1 个**，且只允许出现在「封面页之后、第一章之前」。
- 其余全部依赖 reportlab 自然分页。
- 章节之间要留白就用 `Spacer(1, 10)` / `spaceBefore`，不要用强制分页。

**原因**：大块元素（全宽图表、宽表格、KeepTogether 组）不能跨页拆分。当一个大块把当前页撑溢出、自动挪到下一页时，如果它后面紧跟一个 `PageBreak()`，就会夹出一整页空白。多个 PageBreak 叠加会出现连续空白页。

**自检**：生成后用 PyMuPDF 逐页统计文本长度，任何页正文字符数 < 30 且无图片 → 判定为空白页，必须回头删 PageBreak 或压图表。

### 铁律 3：图表高宽比 0.35~0.40

```python
CHART_W = 15.5 * cm
CHART_RATIO = 0.38            # 铁律：允许区间 0.35~0.40，禁止 0.5 及以上
img = Image(path, width=CHART_W, height=CHART_W * CHART_RATIO)
```

- 宽度 15.5cm 时，高度约 5.4~6.2cm。
- matplotlib 出图时 `figsize` 同步用扁平比例（如 `figsize=(9, 3.4)`, `dpi=160`），避免 PDF 里再压缩造成字变形。
- **11 张图的总高度必须控制在 A4 可打印范围内**：A4 正文区高约 24.7cm（上下边距各 2cm 时）。11 张图按 6.0cm 算 ≈ 66cm ≈ 2.7 页，加图注和正文后应落在 4~5 页内；若超出，先压图表尺寸，再考虑合并同类图。

---

## 二、版式风格继承（标准电商经营诊断报告版式）

以下要素**必须完整继承**，不得自创风格：

| 要素 | 规范 |
|---|---|
| 首页 | 标题块（22pt YaHei-Bold）+ 报告期/生成日期 meta 行 + 一句话结论定调 |
| 章节编号 | 正文用「一、二、三…」中文章节号；子节用「1. 2. 3.」 |
| 表格 | 浅灰表头 `#F5F5F5` + 细边框 `#DDDDDD` 0.5pt；单元格一律 Paragraph 包裹；数值居中、名称列左对齐；`repeatRows=1` |
| 涨跌标注 | 绿涨红跌箭头：↑好=绿 `#52C41A`，↓坏=红 `#FF4D4F`；**退款率、跳失率、退货率等「越低越好」指标反向着色**（`inverse=True`）；百分点用 `pp`，相对变化用 `%` |
| callout 色块 | 仅两种：「经营判断」「关键发现」，底色 `#F2F2F2`，加粗前缀 |
| 行动建议 | 统一结构「目标 / 动作 / 观察指标 / 验收标准 / 停止条件」，不写成散文 |
| 主色 | 正文 `#333333`、次要 `#666666`、标题强调 `#2E5AAC` |

### 字体注册（Windows）

```python
pdfmetrics.registerFont(TTFont('YaHei',      r'C:\Windows\Fonts\msyh.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('YaHei-Bold', r'C:\Windows\Fonts\msyh.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('SimHei',     r'C:\Windows\Fonts\simhei.ttf'))
```

- matplotlib 图表字体：`C:/Windows/Fonts/simhei.ttf`。
- **货币符号禁用「¥」，一律用中文「元」**（黑体缺该字形会渲染成空白）。金额写法：`120.00万元` / `1,200,000.00元`。

---

## 三、数据核查流程（发老板前必做，缺一不可）

1. **检查数据闸门**：确认 `gate_status`、批准指标和禁止结论。未通过闸门时停止正式经营报告。
   报告包 `status=data_blocked` 时，交付物标题和页眉必须明确“数据质量报告”，不能改成经营诊断。
2. **独立重算核心指标**：从原始数据文件重新计算 GMV、净支付、退款率、TOP SKU 排名、客单价、UV 价值，**不沿袭任何底稿/上一版报告里的数字**。底稿只能用来对账，不能用来抄。
3. **描述性区间必须与复算一致**：正文里写的「UV 价值 0.8~1.6 元」「客单价集中在 120~180 元」这类区间，必须来自直接复算结果的真实 min/max 或分位数。**严禁为了好看编造紧凑区间**。区间口径（是极值还是 P10~P90）要在正文或脚注说明。
4. **源文件去重检查**：解析前先列出数据目录下的匹配文件，检查是否存在同一份数据的**日度版 + 周度版 + 月度版**或 `(1)` `副本` 之类的重复导出。glob 全量匹配会把它们一起读入导致重复计数。
   - 处理方式：按「时间口径 + 最新导出时间」只保留一份，其余在资料体检清单里列出并标注「已排除，原因：重复口径」。
5. **交叉校验**：退款各原因金额之和 = 退款总额；各 SKU 销售额之和 ≈ 店铺总 GMV（差额 <1% 可接受，超出必须说明）；流量来源同时检查占比和覆盖率，不默认一定合计为 100%。
6. **对不上就标注，不假设**：多份报表冲突时，按同平台、同期间、同口径下的来源权威性与导出时间裁决，并在报告里写明差异与取舍。数据缺失一律标「数据不足」。

> 交付前口头自查一句：**"这份 PDF 里每一个数字，我是不是都能从原始文件里重新算出来？"** 答不上来就不发。

---

## 四、交付物标准

| 项 | 标准 |
|---|---|
| 文件形态 | **PDF 为默认主交付物**，A4 纵向；图表以 matplotlib 生成 PNG 后 **内嵌**，禁止外链；Markdown 仅作可编辑底稿 |
| 页数 | 生成与复核统一读取 scripts/pdf_layout_policy.py；正文精简，附录保留完整发现与证据。超出时优先级：① 压图表尺寸（比例降到 0.35）② 合并同类章节 ③ 删重复表格。**不允许靠删数据结论来凑页数** |
| 文件名 | `{品牌}{店铺}{期间}经营分析报告.pdf`，中文，不带空格 |
| 路径占用 | 生成前检测目标路径是否被 PDF 阅读器占用（Windows 下文件被锁会写入失败）。占用时**自动追加版本号后缀** `_v2.4`、`_v2.5`…，并在终端打印实际写入路径 |
| 生成后验证 | ① 抽取文字确认中文正常；② PyMuPDF 渲染每页并实际检查空白页、图表溢出、表格断行；③ 打印总页数并核对本次统一页数上限。若无法渲染，必须标“视觉 QA 未完成” |

### 占用检测与版本号追加（标准写法）

```python
import os, re

def resolve_out_path(path):
    """目标被占用时自动追加 _vX.Y 后缀，返回可写路径。"""
    def writable(p):
        if not os.path.exists(p):
            return True
        try:
            with open(p, 'a+b'):
                return True
        except (PermissionError, OSError):
            return False

    if writable(path):
        return path
    root, ext = os.path.splitext(path)
    m = re.search(r'_v(\d+)\.(\d+)$', root)
    if m:
        base, major, minor = root[:m.start()], int(m.group(1)), int(m.group(2))
    else:
        base, major, minor = root, 2, 3
    while True:
        minor += 1
        cand = f"{base}_v{major}.{minor}{ext}"
        if writable(cand):
            print(f"[INFO] 原路径被占用，改写入：{cand}")
            return cand
```

---

## 五、标准执行流程

```
1. 数据闸门   → 使用 ecom-diagnosis-core，确认状态与批准指标
2. 资料体检   → 列文件清单、去重检查、标缺失，严禁编造
3. 解析提取   → pandas 读各 sheet；交叉校验
4. 独立复算   → 核心指标从原始数据重算，不抄底稿
5. 报告包     → 运行 build_report_package.py，固定事实、判断、行动和来源索引
6. 生成图表   → build_report_package 自动调用 generate_pdf_report.py；至少 3 张，中文字体，货币用「元」
7. 组装 PDF   → 自动复用 scripts/pdf_layout_kit.py，套三条铁律
8. 占用检测   → resolve_out_path()
9. 生成后验证 → 抽文字 + PyMuPDF 渲染逐页检查 + 本次页数不超过统一页数上限
10. 交付      → PDF 主文件 + release-receipt.json + completion-receipt.json；回复首屏标注专家团版本、报告修订号和六岗位完成状态
```

## 六、技术栈与环境（已验证）

- Python：使用当前 WorkBuddy 会话可用的 Python 环境，不写死创建者电脑路径。
- 依赖：`pandas`、`xlrd`（.xls OLE）、`openpyxl`（.xlsx）、`matplotlib`、`reportlab`、`pypdf`、`pymupdf`；缺失时如实标注未完成项。
- 文件格式嗅探：`PK\x03\x04` → xlsx/zip；`\xd0\xcf\x11\xe0` → xls OLE

## 七、已踩过的坑

- 正文 TA_JUSTIFY → 中文数字间距炸开（铁律 1）
- 多个 PageBreak + 大图溢出 → 整页空白（铁律 2）
- 图表比例 0.5+ → 11 张图撑到 20+ 页（铁律 3）
- 黑体无「¥」字形 → 一律用「元」
- reportlab 中文不注册字体 → 全是方块
- 表格塞长文本不用 Paragraph → 不换行、撑破列宽
- 涨跌着色不分正反向 → 退款率上升被标成绿色
- glob 全量匹配把日度+周度导出一起读 → GMV 翻倍
- GMV 与净支付混用 → 退款率极端时（如 80%+）严重高估真实规模

## References

- `references/style-master.md` — 母版样式函数逐个说明（section_title / judge / finding / change_html / make_table / chart）
- `scripts/pdf_layout_kit.py` — 开箱即用的样式工具模块，import 后直接调用
