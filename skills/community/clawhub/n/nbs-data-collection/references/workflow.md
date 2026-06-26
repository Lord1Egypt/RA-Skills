# 国家统计局数据采集 - 详细工作流程

## 6阶段流程详解

### 阶段1：计划阶段（吏部）

#### 1.1 明确需求
- 与用户确认需要采集的指标清单
- 确定数据时间范围（起始年份~结束年份）
- 确定数据频率（年度/季度/月度）

#### 1.2 评估可获取性
| 数据范围 | 可获取性 | 说明 |
|---------|---------|------|
| 1951-2015年 | 部分受限 | 2015前年鉴数据可能为图片格式 |
| 2015-2024年 | 较好 | 年鉴HTML/图片格式 |
| 2025年 | 统计公报 | 最新数据需从公报获取 |

#### 1.3 规划采集顺序
推荐顺序：
1. GDP（核心指标，其他指标依赖）
2. CPI/PPI（相对独立）
3. 人口（计算人均GDP）
4. 产出缺口（最后计算，依赖GDP）

---

### 阶段2：数据采集（户部）

#### 2.1 确定数据源
| 数据类型 | 优先数据源 | 备选数据源 |
|---------|-----------|-----------|
| 季度GDP | data.stats.gov.cn新API | 统计公报 |
| 年度GDP | 统计年鉴 | 统计公报 |
| CPI/PPI月度 | data.stats.gov.cn | 中国人民银行 |
| 历史数据(2015前) | 统计年鉴PDF | OCR识别 |

#### 2.2 采集执行
```bash
# 使用checkpoint机制，支持断点续采
python3.10 scripts/nbs_crawler.py --indicator gdp_quarterly --start 2003 --end 2025
```

#### 2.3 保存原始数据
```bash
output/raw_data/
├── gdp_quarterly.json  # {"period": "2003Q1", "gdp": 29698.8, "source": "nbs_api"}
├── cpi_monthly.json    # {"period": "2025-01", "cpi": 100.5, "source": "nbs_api"}
└── ppi_monthly.json
```

---

### 阶段3：数据处理（工部）

#### 3.1 计算衍生指标

**人均GDP计算**：
```
人均GDP(元/季度) = GDP(亿元) × 亿 / 季度人口(万人)
                ≈ GDP(亿元) × 2000 / 季度人口(万)
```

**GDP平减指数估算**：
```
GDP平减指数 ≈ CPI季度链式指数（基于上年同月=100）
⚠️ 注意：这是估算方法，标注说明
```

**产出缺口计算**（HP滤波）：
```python
import numpy as np
from scipy.ndimage import uniform_filter1d

def hp_filter(y, lamb=1600):
    """
    Hodrick-Prescott滤波
    lamb: 平滑参数（季度=1600, 年度=100, 月度=14400）
    """
    n = len(y)
    # 构建二阶差分矩阵
    I = np.eye(n)
    D = np.diff(I, n=2)
    # 趋势成分
    tau = np.linalg.solve(I + lamb * D.T @ D, y)
    # 周期成分 = 实际 - 趋势
    cycle = y - tau
    return tau, cycle

# 使用
gdp_series = df['gdp'].values
trend, cycle = hp_filter(gdp_series, lamb=1600)
gap = cycle / trend * 100  # 产出缺口率(%)
```

#### 3.2 季度均值计算
```python
# 月度→季度均值
quarterly_cpi = df.resample('QE').mean()

# 同比计算
df['cpi_yoy'] = df['cpi'] / df['cpi'].shift(12) * 100 - 100
```

---

### 阶段4：质量核验（刑部）

#### 4.1 数据抽查
从统计公报/年鉴抽查2-3个数据点：
```python
# 例：抽查2025Q1 GDP
official_value = 318758  # 从公报获取
our_value = df.loc['2025Q1', 'gdp']
if abs(official_value - our_value) > 1:
    print(f"⚠️ 差异: {our_value} vs {official_value}")
```

#### 4.2 HP滤波结果验证
经济危机时期的产出缺口应该显著为负：
| 时期 | 预期产出缺口 | 验证 |
|------|-------------|------|
| 2009Q1 | -10% ~ -15% | 验证是否合理 |
| 2020Q1 | -15% ~ -20% | 验证是否合理 |

#### 4.3 差异处理
- 如果差异>1%，需要查明原因
- 如果是数据修订，更新为最新数据
- 如果是计算错误，重新计算

---

### 阶段5：链接与可视化

#### 5.1 添加数据来源链接

**链接规则**：
| 数据年份 | 链接目标 | 显示文本 |
|---------|---------|---------|
| 2003年 | `.../ndsj/yb2004-c/indexch.htm` | "2004年鉴" |
| 2004-2024年 | `.../ndsj/{year+1}/indexch.htm` | "{year+1}年鉴" |
| 2025年 | 统计公报URL | "统计公报" |

**注意**：2004年鉴URL格式特殊，使用`yb2004-c`而非`2004`

#### 5.2 绘制折线图
```python
from openpyxl.chart import LineChart, Reference

def add_trend_chart(ws, data_col, title, y_axis):
    chart = LineChart()
    chart.title = title
    chart.height = 10
    chart.width = 20
    chart.y_axis.title = y_axis
    chart.x_axis.title = "期间(季度)"
    
    data = Reference(ws, min_col=data_col, min_row=1, max_row=ws.max_row-1)
    periods = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row-1)
    
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(periods)
    ws.add_chart(chart, "H2")
```

#### 5.3 验证链接有效性
```bash
#!/bin/bash
for year in {2003..2024}; do
    yb=$((year+1))
    if [ $yb -eq 2004 ]; then
        url="https://www.stats.gov.cn/sj/ndsj/yb2004-c/indexch.htm"
    else
        url="https://www.stats.gov.cn/sj/ndsj/${yb}/indexch.htm"
    fi
    code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    echo "$year -> ${yb}年鉴: HTTP $code"
done
```

---

### 阶段6：输出交付

#### 6.1 Excel结构
```
国民经济核算与价格指数_YYYY-MM-DD.xlsx
├── 实际GDP (季度)     # A:期间, B:年份, C:季度, D:GDP, E:GDP增速, F:数据来源
├── GDP增速           # A:期间, B:年份, C:季度, D:同比增速, E:数据来源
├── 人均GDP           # A:期间, B:年份, C:季度, D:人口, E:人均GDP, F:数据来源
├── 产出缺口           # A:期间, B:潜在GDP, C:实际GDP, D:缺口, E:缺口率, F:数据来源
├── CPI (季度均值)    # A:期间, B:年份, C:季度, D:CPI均值, E:数据来源
├── PPI (季度均值)    # A:期间, B:年份, C:季度, D:PPI均值, E:数据来源
├── GDP平减指数       # A:期间, B:平减指数, C:同比, D:数据来源
└── 数据说明          # 数据来源、计算方法、修订记录
```

#### 6.2 checkpoint文件
```bash
output/
├── checkpoint_gdp.csv       # 最后采集位置
├── checkpoint_cpi.csv       # 用于断点续采
└── raw_data/
    └── gdp_quarterly.json   # 原始数据备份
```

---

## 常见问题处理

### Q1: 某年年鉴404怎么办？
检查是否使用了错误的URL格式（如2004年鉴应用`yb2004-c`）

### Q2: 2025年数据与公报不符？
可能是初步核算与最终核实数的差异，使用公报中的最终核实数

### Q3: HP滤波结果不合理？
检查λ参数是否正确（季度=1600），检查输入数据是否有缺失值

### Q4: 数据来源链接太多，维护困难？
使用统一的"年鉴目录页"链接，不逐个指标设置直接链接
