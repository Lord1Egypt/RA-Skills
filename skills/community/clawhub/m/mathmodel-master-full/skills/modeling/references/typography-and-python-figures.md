# 深层参考：字体规范与 Python 图表生成

## 读取时机

当最终交付为 Word/PDF、用户要求字体统一、图表美观、图表由 Python 生成，或需要避免 AI 风格图表时，读取本文件。

## 字体硬规则

竞赛论文默认字体体系：

- 中文：宋体。
- 英文、数字和公式编号周边文本：Times New Roman。
- 图中文字：中文宋体，英文和数字 Times New Roman。
- 表格、图注、页眉页脚、题目、一级标题、二级标题、三级标题、摘要和正文都要遵守同一字体体系。
- 题目和所有层级标题必须为黑色，不使用蓝色、灰色、主题色或装饰色。

不要保留 Word 默认 Calibri、Arial、微软雅黑或等线。若使用 `python-docx`，设置 run 字体时至少同时写入：

```python
run.font.name = "Times New Roman"
run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Times New Roman")
run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Times New Roman")
run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "SimSun")
```

对 Word 样式也要设置 `Normal`、`Title`、`Heading 1`、`Heading 2`、`Heading 3`、表格和图注相关样式，避免局部 run 正确但样式仍继承默认字体。题目和标题样式的 `font.color.rgb` 必须设置为黑色或保持自动黑色，不要使用蓝色标题。

示例：

```python
from docx.shared import RGBColor

for name in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
    style = doc.styles[name]
    style.font.name = "Times New Roman"
    style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Times New Roman")
    style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Times New Roman")
    style._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "SimSun")
    style.font.color.rgb = RGBColor(0, 0, 0)
```

## Python 图表硬规则

论文图表必须由 Python 绘图库生成。优先使用：

- matplotlib / seaborn：统计图、分布图、误差图、校准图、森林图、热力图。
- plotly：交互原型或复杂图的静态导出。
- networkx：网络图、流程/关系图。
- scipy / statsmodels：拟合曲线、置信区间、统计检验可视化。
- pandas + matplotlib：结果表驱动的可复现绘图。

不得用 AI 生成图、网页截图、Excel 默认图、PPT 手工形状图、低分辨率截图或 PIL 纯手工拼贴图作为论文主体图表。PIL 只能用于合页预览、裁剪、拼接或辅助标注，不能作为主要数据图绘制工具。

## matplotlib/seaborn 字体模板

生成图前显式配置字体和输出质量：

```python
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

font_manager.fontManager.addfont("C:/Windows/Fonts/simsun.ttc")
font_manager.fontManager.addfont("C:/Windows/Fonts/times.ttf")
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams["font.family"] = ["Times New Roman", "SimSun"]
plt.rcParams["font.serif"] = ["Times New Roman"]
plt.rcParams["font.sans-serif"] = ["SimSun"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 300
```

若系统字体文件名不同，应查找 Windows 字体目录中的宋体和 Times New Roman，并把实际路径加入 font manager。

## 美观标准

图表应像严肃竞赛论文中的统计图，而不是 AI 海报或默认截图：

- 白底或极浅灰底，细网格，轻边框。
- 深蓝、青绿、珊瑚、金色、紫灰等低饱和配色，整篇统一。
- 只突出关键阈值、峰值、分组差异或异常点。
- 坐标轴标签包含变量名和单位。
- 图例放在不遮挡数据的位置，必要时使用外置图例。
- 不使用发光、玻璃拟态、大面积渐变、装饰卡片、3D 柱状图、彩虹色或视觉噪声。
- 图中字号插入 Word 后仍可读，线宽和标记大小不过度夸张。

## 创新表达

“创新图表”应服务模型解释，而不是为了好看。优先考虑：

- 总览+细节复合图：一图中同时展示总体结构和关键分布。
- 事件时间图：展示发生时间、阈值和病例排序。
- 校准曲线+ROC/PR 曲线：同时说明分类区分度和概率可靠性。
- 系数森林图或 SHAP 汇总图：解释特征贡献和方向。
- 分组轨迹图：展示时间序列或亚组演化差异。
- 聚类热力图：展示变量关系或样本分型。
- 敏感性响应面：展示参数扰动对结果的影响。

每个创新图必须有明确论文角色：回答哪个问题、支持哪个结论、暴露哪个不确定性。

## 交付前检查

交付 `.docx` 前：

```bash
python scripts/verify_docx_typography.py paper.docx
python scripts/verify_docx_figures.py paper.docx --min-figures 12 --min-explained 12
```

脚本检查不能替代视觉审查。仍需打开最终 Word/PDF 或渲染页图，逐页检查字体、题目和各级标题是否为黑色、公式、图表清晰度、图例位置和图文衔接。若检查脚本报告标题样式或标题段落存在非黑色颜色值，必须回到文档生成脚本中修改样式，而不是在 Word 中手动临时改色。
