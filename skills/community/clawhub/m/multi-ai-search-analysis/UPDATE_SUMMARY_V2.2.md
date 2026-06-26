# v2.2 更新总结 - 可视化图表生成

**更新日期**：2026-03-19 21:20  
**版本**：v2.2（图表生成版）

---

## 🎉 新增功能

### 1. 图表生成模块（charts.py）

新增独立的图表生成模块，支持 4 种图表类型：

#### 📊 数据对比柱状图
- **用途**：对比多家 AI 的关键数据预测
- **示例**：油价预测、通胀率、GDP 影响等
- **特点**：自动标注数值、多 AI 并列对比

#### 🎯 质量评分雷达图
- **用途**：可视化展示各家 AI 的 5 维度质量评分
- **维度**：字数、数据点、结构、引用、具体性
- **特点**：多维度对比、一目了然

#### 📈 趋势分析折线图
- **用途**：展示时间序列数据的变化趋势
- **示例**：油价走势、支持率变化等
- **特点**：多 AI 趋势线对比

#### 📑 综合图表报告
- **用途**：一键生成包含多种图表的综合报告
- **特点**：自动命名、统一风格、批量生成

---

## 📁 新增文件

```
skills/multi-ai-search-analysis/
├── scripts/
│   └── charts.py              # 图表生成模块（新增）
├── reports/
│   └── charts/                # 图表输出目录（自动创建）
└── UPDATE_SUMMARY_V2.2.md     # 本文件（新增）
```

---

## 🔧 使用方法

### 方式 1：独立使用图表模块

```python
from scripts.charts import ChartGenerator

# 初始化
generator = ChartGenerator(output_dir="reports/charts")

# 生成对比柱状图
comparison_data = {
    "油价预测": {"DeepSeek": 103, "Qwen": 105, "豆包": 104, "Kimi": 102},
    "通胀率": {"DeepSeek": 3.8, "Qwen": 4.1, "豆包": 3.9, "Kimi": 4.0}
}
generator.generate_comparison_bar_chart(comparison_data, "关键数据对比")

# 生成质量评分雷达图
quality_scores = {
    "DeepSeek": {"字数": 85, "数据点": 90, "结构": 80, "引用": 75, "具体性": 85},
    "Qwen": {"字数": 80, "数据点": 85, "结构": 90, "引用": 70, "具体性": 80}
}
generator.generate_quality_radar_chart(quality_scores, "质量评分对比")
```

### 方式 2：集成到 run.py

在 `run.py` 中导入并使用：

```python
from scripts.charts import ChartGenerator

# 在生成报告后
if args.charts:  # 新增 --charts 参数
    generator = ChartGenerator()
    
    # 从提取的数据生成图表
    generator.generate_multi_chart_report(
        comparison_data=extracted_data,
        quality_scores=quality_scores,
        report_title="多 AI 分析报告"
    )
```

---

## 📦 依赖安装

```bash
# 进入技能目录
cd skills/multi-ai-search-analysis

# 安装新依赖
pip install -r requirements.txt

# 或单独安装
pip install matplotlib numpy
```

---

## 🎨 中文字体支持

图表模块会自动检测系统中可用的中文字体：

**Windows 推荐字体**：
- SimHei（黑体）
- Microsoft YaHei（微软雅黑）

**macOS 推荐字体**：
- Arial Unicode MS
- Heiti TC

**Linux 推荐字体**：
- WenQuanYi Micro Hei

如果未检测到中文字体，中文可能显示为方框。建议安装上述字体之一。

### 手动指定字体路径

```python
generator = ChartGenerator(font_path="C:/Windows/Fonts/simhei.ttf")
```

---

## 📊 输出示例

生成的图表保存在 `reports/charts/` 目录：

```
reports/charts/
├── comparison_20260319_212000.png    # 数据对比柱状图
├── quality_radar_20260319_212001.png # 质量评分雷达图
├── trend_20260319_212002.png         # 趋势分析折线图
└── report_comparison_20260319_212000.png  # 综合报告图表
```

---

## 🔮 后续计划

- [ ] 集成到 run.py 主流程（--charts 参数）
- [ ] 支持图表样式自定义（颜色、主题）
- [ ] 添加饼图支持（占比分析）
- [ ] 支持导出交互式图表（plotly）
- [ ] 图表自动嵌入 Markdown 报告

---

## 🐛 已知问题

1. **中文字体**：部分系统可能未安装中文字体，需要手动安装
2. **图表尺寸**：大数据量时图表可能拥挤，需要动态调整
3. **颜色区分**：AI 平台超过 8 个时颜色可能重复

---

## 📝 技术细节

### ChartGenerator 类

**主要方法**：
- `__init__(output_dir, font_path)`: 初始化
- `generate_comparison_bar_chart()`: 柱状图
- `generate_quality_radar_chart()`: 雷达图
- `generate_trend_line_chart()`: 折线图
- `generate_multi_chart_report()`: 综合报告

**配置项**：
- 输出目录：默认 `reports/charts/`
- 中文字体：自动检测或手动指定
- 图表样式：seaborn 风格
- 分辨率：150 DPI

---

*更新者：小呱 🐸*  
*更新时间：2026-03-19 21:20*
