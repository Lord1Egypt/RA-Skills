---
name: data-analyst-pro
version: 1.0.0
description: Professional data analysis skill pack - SQL queries, Python analytics, visualization, and automated reports. Perfect for data analysts, developers, and business professionals.
author: 秘书
price: 39
currency: USD
keywords: [data-analysis, SQL, Python, pandas, visualization, reports, analytics]
category: productivity
---

# 📊 Data Analyst Pro - 专业数据分析技能包

**从数据到洞察，让 AI 成为你的数据分析师**

---

## 🎯 这个技能能帮你做什么？

✅ **SQL 查询生成** - 自动生成复杂 SQL 查询
✅ **数据分析** - Python/Pandas 自动化分析
✅ **数据可视化** - 自动生成图表和报告
✅ **数据清洗** - 处理缺失值、异常值
✅ **统计分析** - 描述性统计、相关性分析
✅ **自动化报告** - 生成专业分析报告

---

## 📚 包含内容

### 第一部分：SQL 查询模式（30+ 模板）

#### 基础查询
```sql
-- 数据探索
SELECT COUNT(*) FROM table_name;
SELECT * FROM table_name LIMIT 10;

-- 列统计
SELECT 
    column_name,
    COUNT(*) as count,
    COUNT(DISTINCT column_name) as unique_values,
    MIN(column_name) as min_val,
    MAX(column_name) as max_val
FROM table_name
GROUP BY column_name;
```

#### 时间序列分析
```sql
-- 日聚合
SELECT 
    DATE(created_at) as date,
    COUNT(*) as daily_count,
    SUM(amount) as daily_total
FROM transactions
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- 环比增长
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as count,
    LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)) as prev_month,
    (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at))) / 
        NULLIF(LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)), 0) * 100 as growth_pct
FROM transactions
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;
```

#### 漏斗分析
```sql
-- 转化漏斗
WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as views,
        COUNT(DISTINCT CASE WHEN event = 'signup' THEN user_id END) as signups,
        COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases
    FROM events
    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT 
    views,
    signups,
    ROUND(signups * 100.0 / NULLIF(views, 0), 2) as signup_rate,
    purchases,
    ROUND(purchases * 100.0 / NULLIF(signups, 0), 2) as purchase_rate
FROM funnel;
```

#### 用户分层
```sql
-- RFM 分析
WITH rfm AS (
    SELECT 
        user_id,
        DATEDIFF(CURRENT_DATE, MAX(order_date)) as recency,
        COUNT(*) as frequency,
        SUM(amount) as monetary
    FROM orders
    GROUP BY user_id
)
SELECT 
    CASE 
        WHEN recency <= 30 THEN 'Active'
        WHEN recency <= 90 THEN 'Churning'
        ELSE 'Churned'
    END as segment,
    COUNT(*) as users,
    AVG(frequency) as avg_frequency,
    AVG(monetary) as avg_monetary
FROM rfm
GROUP BY segment;
```

---

### 第二部分：Python 数据分析

#### Pandas 快速操作
```python
import pandas as pd

# 加载数据
df = pd.read_csv('data.csv')

# 基础探索
print(df.shape)  # (rows, columns)
print(df.info())  # 列类型和空值
print(df.describe())  # 统计摘要

# 数据清洗
df = df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'])
df['amount'] = df['amount'].fillna(0)

# 聚合分析
summary = df.groupby('category').agg({
    'amount': ['sum', 'mean', 'count'],
    'quantity': 'sum'
}).round(2)

# 导出
summary.to_csv('analysis_output.csv')
```

#### 常用分析模式
```python
# 过滤
filtered = df[df['status'] == 'active']
filtered = df[df['amount'] > 1000]
filtered = df[df['date'].between('2024-01-01', '2024-12-31')]

# 聚合
by_category = df.groupby('category')['amount'].sum()
pivot = df.pivot_table(values='amount', index='month', columns='category', aggfunc='sum')

# 窗口函数
df['running_total'] = df['amount'].cumsum()
df['pct_change'] = df['amount'].pct_change()
df['rolling_avg'] = df['amount'].rolling(window=7).mean()

# 合并
merged = pd.merge(df1, df2, on='id', how='left')
```

---

### 第三部分：数据可视化

#### 图表选择指南
| 数据类型 | 最佳图表 | 使用场景 |
|---------|---------|---------|
| 时间趋势 | 折线图 | 展示模式/变化 |
| 类别比较 | 柱状图 | 比较离散类别 |
| 占比关系 | 饼图/环形图 | 展示比例（≤5类） |
| 分布 | 直方图 | 理解数据分布 |
| 相关性 | 散点图 | 两个变量关系 |
| 多类别 | 横向柱状图 | 排名或比较 |

#### Python 可视化代码
```python
import matplotlib.pyplot as plt
import seaborn as sns

# 设置样式
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# 折线图（趋势）
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'], marker='o')
plt.title('Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('trend.png', dpi=150)

# 柱状图（比较）
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='category', y='amount')
plt.title('Amount by Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('comparison.png', dpi=150)

# 热力图（相关性）
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation.png', dpi=150)
```

---

### 第四部分：统计检验速查

| 检验 | 使用场景 | Python |
|------|---------|--------|
| T检验 | 比较两个均值 | `scipy.stats.ttest_ind(a, b)` |
| 卡方检验 | 分类变量独立性 | `scipy.stats.chi2_contingency(table)` |
| ANOVA | 比较3+个均值 | `scipy.stats.f_oneway(a, b, c)` |
| Pearson | 线性相关 | `scipy.stats.pearsonr(x, y)` |

---

### 第五部分：自动化报告生成

#### 报告模板
```markdown
# [报告名称]
**周期:** [日期范围]
**生成时间:** [日期]

## 执行摘要
[2-3句话总结关键发现]

## 关键指标

| 指标 | 当前值 | 上期值 | 变化 |
|------|--------|--------|------|
| [指标] | [值] | [值] | [+/-X%] |

## 详细分析

### [部分1]
[分析和支持数据]

### [部分2]
[分析和支持数据]

## 可视化
[插入图表]

## 洞察
1. **[洞察]**: [支持证据]
2. **[洞察]**: [支持证据]

## 建议
1. [可执行建议]
2. [可执行建议]

## 方法论
- 数据源: [源]
- 日期范围: [范围]
- 过滤器: [过滤器]
- 已知限制: [限制]
```

---

## 🚀 快速开始

### 场景1：生成 SQL 查询
```
用户：帮我写一个查询，找出过去30天每天的新用户数

AI：
SELECT 
    DATE(created_at) as date,
    COUNT(DISTINCT user_id) as new_users
FROM users
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### 场景2：数据分析
```
用户：分析这个 CSV 文件的销售趋势

AI：
[自动加载 CSV]
[生成统计摘要]
[创建趋势图]
[生成报告]

关键发现：
- 月均增长：+15%
- 最佳品类：电子产品（+42%）
- 销售高峰：周末
```

### 场景3：自动化报告
```
用户：生成本周销售报告

AI：
# 销售周报（2026-04-01 至 2026-04-07）

## 执行摘要
本周销售额 $45,000，环比增长 12%。新客户增长 23%。

## 关键指标
| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| 销售额 | $45,000 | $40,200 | +12% |
| 订单数 | 230 | 210 | +9.5% |
| 平均订单价值 | $196 | $191 | +2.6% |

[继续...]
```

---

## 💡 特色功能

### 1. 智能数据类型识别
```
自动识别：
- 日期字段
- 数值字段
- 分类字段
- 文本字段

根据数据类型推荐分析类型
```

### 2. 异常检测
```
自动检测：
- 缺失值
- 重复值
- 异常值
- 数据类型错误

提供清洗建议
```

### 3. 可视化推荐
```
根据数据自动推荐：
- 最佳图表类型
- 颜色方案
- 布局建议
```

---

## 🎁 购买即得

1. **30+ SQL 查询模板**
2. **完整 Python 分析代码库**
3. **20+ 可视化模板**
4. **自动化报告生成器**
5. **统计检验速查表**
6. **终身更新**
7. **技术支持**

---

## 📊 适用场景

| 场景 | 推荐度 | 说明 |
|------|--------|------|
| **数据分析师** | ⭐⭐⭐⭐⭐ | 日常工作必备 |
| **产品经理** | ⭐⭐⭐⭐ | 数据驱动决策 |
| **市场营销** | ⭐⭐⭐⭐ | ROI 分析 |
| **创业者** | ⭐⭐⭐⭐ | 业务数据分析 |
| **学生** | ⭐⭐⭐⭐⭐ | 学习数据分析 |

---

## ⚠️ 数据安全

- ✅ 所有分析在本地执行
- ✅ 不上传数据到外部服务器
- ✅ 完全隐私保护

---

## 🔧 版本历史

- v1.0.0 (2026-04-05): 首次发布

---

**立即购买，让 AI 成为你的数据分析师！** 🚀
