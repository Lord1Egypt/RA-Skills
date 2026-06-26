---
name: nbs-data-collection
description: 国家统计局数据采集技能。当用户需要采集国家统计局（NBS）的宏观经济数据（如GDP、CPI、PPI、产出缺口等）时触发。适用场景包括：（1）采集GDP、CPI、PPI等指标；（2）从国家统计局官网/统计年鉴获取数据；（3）计算产出缺口（HP滤波）；（4）整理数据到Excel。本skill包含标准工作流程、数据源URL、指标说明和复用脚本。
---

# 国家统计局数据采集 Skill

## 快速开始

当用户要求采集国家统计局数据时，按以下流程执行：

```
用户请求 → 计划阶段 → 数据采集 → 数据处理 → 质量核验 → 输出交付
```

## 工作流程（6阶段）

### 阶段1：计划阶段（吏部）
1. 明确采集指标和数据范围
2. 确认数据频率（季度/月度/年度）
3. 评估数据可获取性（2015年前数据可能有特殊限制）
4. 规划采集顺序

### 阶段2：数据采集（户部）
1. 从国家统计局data.stats.gov.cn或统计公报获取原始数据
2. 保存到checkpoint文件（支持断点续采）
3. 标注数据来源和采集时间

### 阶段3：数据处理（工部）
1. 计算衍生指标：
   - 人均GDP = GDP ÷ 人口
   - GDP平减指数 ≈ CPI链式指数
   - 产出缺口 = HP滤波(λ=1600)
2. 季度均值计算（月度→季度）
3. 同比/环比计算

### 阶段4：质量核验（刑部）
1. **数据抽查**：从统计公报/年鉴核实2-3个关键数据点
2. **计算验证**：确认衍生指标计算正确
3. **差异处理**：如发现差异，记录并说明

### 阶段5：链接与可视化
1. **添加数据来源链接**（见下方"数据源URL"）
2. **绘制折线图**：时间序列数据用折线图展示趋势
3. **验证链接有效性**：批量检查所有链接

### 阶段6：输出交付
1. Excel文件（多Sheet，每个指标一个Sheet）
2. 数据说明Sheet（标注计算方法、数据来源）
3. checkpoint文件备份

## 关键指标说明

| 指标 | 频率 | 来源 | 计算说明 |
|------|------|------|---------|
| 实际GDP | 季度 | 国家统计局API/统计年鉴 | 已有，标注"初步核算"/"最终核实" |
| GDP增速 | 季度 | 计算或年鉴 | 同比增速 |
| 人均GDP | 季度 | 计算 | = GDP ÷ 人口(季度估算) |
| CPI | 月度→季度均值 | 国家统计局API | 上年同月=100 |
| PPI | 月度→季度均值 | 国家统计局API | 上年同月=100 |
| GDP平减指数 | 年度 | 计算 | ≈ CPI季度链式指数（标注⚠️估算） |
| 产出缺口 | 季度 | HP滤波 | λ=1600趋势成分 |

## HP滤波参数

```python
λ = 1600  # 季度标准值
# 年度 λ=100，月度 λ=14400
```

## 数据源URL

### 统计年鉴（重要！URL格式不统一）

| 数据年份 | 年鉴URL格式 | 说明 |
|---------|------------|------|
| 2003年数据 | `.../ndsj/yb2004-c/indexch.htm` | ⚠️ 特殊格式 |
| 其他年份 | `.../ndsj/{yearbook_year}/indexch.htm` | 数据年+1=年鉴年份 |

**规则**：数据年份N → 年鉴年份N+1
- 2003年数据 → 2004年鉴（URL: `.../ndsj/yb2004-c/indexch.htm`）
- 2024年数据 → 2025年鉴（URL: `.../ndsj/2025/indexch.htm`）

### 统计公报（用于2025年等最新数据）

| 季度 | URL |
|------|-----|
| 2025Q1 | `https://www.stats.gov.cn/sj/zxfb/202504/t20250417_1959334.html` |
| 2025Q2 | `https://www.stats.gov.cn/sj/zxfb/202507/t20250716_1960426.html` |
| 2025Q3 | `https://www.stats.gov.cn/sj/zxfb/202510/t20251021_1961646.html` |
| 2025Q4 | `https://www.stats.gov.cn/sj/zxfb/202601/t20260120_1962349.html` |

### data.stats.gov.cn
- 主页: `https://data.stats.gov.cn`
- ⚠️ 旧API `/easyquery.htm` 已返回404，需使用新API

## 输出文件结构

```
output/
├── 国民经济核算与价格指数_YYYY-MM-DD.xlsx
│   ├── 实际GDP (季度)
│   ├── GDP增速
│   ├── 人均GDP
│   ├── 产出缺口
│   ├── CPI (季度均值)
│   ├── PPI (季度均值)
│   ├── GDP平减指数
│   └── 数据说明
├── checkpoint_gdp.csv
├── checkpoint_hp_filter.csv
└── raw_data/
    ├── gdp_quarterly.json
    └── cpi_monthly.json
```

## 复用脚本

- `scripts/nbs_crawler.py` - 数据采集主脚本
- `scripts/verify_links.py` - 批量验证链接有效性
- `scripts/add_charts.py` - 为Excel添加折线图
- `scripts/hp_filter.py` - HP滤波计算

## 注意事项

1. **2015年界限**：2015年前数据可能需从年鉴OCR获取
2. **数据修订**：2025年等最新数据可能与初步核算有差异，应使用最终核实数
3. **SSL问题**：部分年份年鉴访问可能间歇性404
4. **计算项标注**：所有估算/计算项必须标注⚠️和计算方法

## 参考文档

- 工作流程详解: [references/workflow.md](references/workflow.md)
- 指标说明: [references/indicators.md](references/indicators.md)
- 数据源URL: [references/sources.md](references/sources.md)
