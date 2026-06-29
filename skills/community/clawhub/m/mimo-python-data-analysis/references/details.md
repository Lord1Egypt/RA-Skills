# Python数据分析 详细参考 v1.3.0

## 支持的分析类型

### 1. 描述统计 📈
```
分析方法：
- 集中趋势：均值(mean)、中位数(median)、众数(mode)
- 离散程度：标准差(std)、方差(var)、极差(range)、四分位距(IQR)
- 分布形状：偏度(skewness)、峰度(kurtosis)
- 分位数：Q1/Q2/Q3/Q4、百分位数

输出模板：
- 数值变量：均值±标准差，或中位数(IQR)
- 分类变量：频次表(count) + 占比(%)
- 图表：直方图、箱线图、密度图

Python代码：
```python
import pandas as pd
import numpy as np

def descriptive_stats(df, col):
    stats = {
        'count': df[col].count(),
        'mean': df[col].mean(),
        'std': df[col].std(),
        'min': df[col].min(),
        'Q1': df[col].quantile(0.25),
        'median': df[col].median(),
        'Q3': df[col].quantile(0.75),
        'max': df[col].max(),
        'missing': df[col].isna().sum()
    }
    return pd.Series(stats)
```
```

### 2. 假设检验 🔬
```
t检验：
- 单样本t检验：样本均值 vs 已知值
- 独立样本t检验：两组均值差异
- 配对样本t检验：同一组前后差异

非参数检验：
- Mann-Whitney U：独立样本
- Wilcoxon符号秩：配对样本
- Kruskal-Wallis：多组比较

卡方检验：
- 独立性检验：两个分类变量
- 拟合优度：实际vs期望分布

ANOVA：
- 单因素方差分析
- 多因素方差分析

显著性水平：α=0.05（可调整）

Python代码：
```python
from scipy import stats

# 独立样本t检验
t, p = stats.ttest_ind(group1, group2)

# Mann-Whitney U检验
u, p = stats.mannwhitneyu(group1, group2)

# 卡方检验
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

# ANOVA
f, p = stats.f_oneway(group1, group2, group3)
```
```

### 3. 回归建模 📉
```
线性回归：
- 简单线性回归：y = ax + b
- 多元线性回归：y = β0 + β1*x1 + ... + βn*xn
- 多项式回归：y = β0 + β1*x + β2*x² + ...

逻辑回归：
- 二分类：0/1
- 多分类：OvR或多项式
- 输出概率和类别

正则化：
- Ridge(L2)：惩罚大系数
- Lasso(L1)：特征选择
- ElasticNet：L1+L2混合

评估指标：
- 回归：R²、MAE、MSE、RMSE、MAPE
- 分类：Accuracy、Precision、Recall、F1、AUC

Python代码：
```python
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, classification_report

# 线性回归
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"R²: {r2_score(y_test, y_pred):.4f}")

# 逻辑回归
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```
```

### 4. 聚类分析 🎯
```
算法选择：
- K-Means：球形簇，大数据集
- DBSCAN：任意形状簇，自动K
- 层次聚类：树状图，小数据集

确定K：
- 肘部法则：SSE下降明显处
- 轮廓系数：越接近1越好
- Gap统计量：更鲁棒

特征处理：
- 数值标准化：StandardScaler
- 类别编码：LabelEncoder/OneHot
- 降维：PCA（高维时）

Python代码：
```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# 评估
silhouette = silhouette_score(X_scaled, labels)
print(f"轮廓系数: {silhouette:.4f}")
```
```

### 5. 时间序列 📅
```
分解：
- 趋势(Trend)：长期变化
- 季节性(Seasonal)：周期性波动
- 残差(Residual)：随机波动

方法：
- 移动平均：简单预测
- 指数平滑：SES/Holt/Holt-Winters
- ARIMA：自回归+移动平均+差分

预测评估：
- MAE、MSE、RMSE
- MAPE（百分比误差）

Python代码：
```python
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

# 分解
result = seasonal_decompose(ts, model='additive', period=12)
result.plot()

# ARIMA
model = ARIMA(ts, order=(1,1,1))
fitted = model.fit()
forecast = fitted.forecast(steps=12)
```
```

### 6. 相关性分析 🔗
```
连续变量：
- Pearson：线性相关
- Spearman：单调相关（秩相关）
- Kendall：秩相关，更稳健

可视化：
- 散点图：直观展示关系
- 热力图：多变量相关矩阵
- 回归线：趋势线

注意：
- 相关≠因果
- 异常值影响大
- 非线性关系用Spearman

Python代码：
```python
import seaborn as sns

# Pearson相关
corr = df.corr(method='pearson')

# Spearman相关
corr = df.corr(method='spearman')

# 热力图
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
```
```

---

## 可视化规范 📊

### 图表类型选择
| 目的 | 推荐图表 |
|------|----------|
| 分布 | 直方图、箱线图、密度图 |
| 比较 | 柱状图、雷达图 |
| 趋势 | 折线图、面积图 |
| 关系 | 散点图、热力图 |
| 占比 | 饼图、堆叠柱状图 |
| 地理 | 地图可视化 |

### 样式规范
```python
import matplotlib.pyplot as plt
import seaborn as sns

# 全局设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# 调色板
colors = sns.color_palette("husl", 8)

# 主题
sns.set_style("whitegrid")
```

### 导出规范
```python
import os
from datetime import datetime

output_dir = f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(output_dir, exist_ok=True)

# 保存图表
plt.savefig(f"{output_dir}/chart.png", bbox_inches='tight')
plt.close()
```

---

## 数据清洗规范 🧹

### 缺失值处理
```python
# 检测
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100

# 删除（缺失<5%）
df_clean = df.dropna()

# 填充
# 数值：均值/中位数
df['col'].fillna(df['col'].median(), inplace=True)

# 分类：众数
df['col'].fillna(df['col'].mode()[0], inplace=True)

# 插值（时间序列）
df['col'].interpolate(method='linear', inplace=True)
```

### 异常值处理
```python
# IQR方法
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# 标记
df['is_outlier'] = (df['col'] < lower) | (df['col'] > upper)

# 处理：删除/替换/保留
df_clean = df[(df['col'] >= lower) & (df['col'] <= upper)]
```

### 数据转换
```python
# 标准化（Z-score）
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['col_scaled'] = scaler.fit_transform(df[['col']])

# 归一化（0-1）
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['col_normalized'] = scaler.fit_transform(df[['col']])

# 对数变换（右偏分布）
df['col_log'] = np.log1p(df['col'])

# Box-Cox变换
from scipy import stats
df['col_boxcox'], lambda_ = stats.boxcox(df['col'].dropna() + 1)
```

---

## 完整分析流程模板

```python
#!/usr/bin/env python3
"""
Python数据分析脚本
生成时间：{timestamp}
分析目标：{objective}
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 配置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 输出目录
OUTPUT_DIR = f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def load_data(path):
    """数据加载"""
    if path.endswith('.csv'):
        try:
            return pd.read_csv(path)
        except:
            return pd.read_csv(path, encoding='gbk')
    elif path.endswith('.xlsx'):
        return pd.read_excel(path)
    elif path.endswith('.json'):
        return pd.read_json(path)
    else:
        raise ValueError(f"不支持的文件格式: {path}")

def explore_data(df):
    """数据探索"""
    print("=" * 50)
    print("📊 数据概览")
    print("=" * 50)
    print(f"样本量: {len(df)}")
    print(f"特征数: {len(df.columns)}")
    print("\n数据类型:")
    print(df.dtypes)
    print("\n缺失值:")
    print(df.isnull().sum())
    print("\n基本统计:")
    print(df.describe())

def clean_data(df):
    """数据清洗"""
    df_clean = df.copy()
    # 缺失值处理
    for col in df_clean.columns:
        if df_clean[col].dtype in ['float64', 'int64']:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
        else:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    return df_clean

def analyze(df):
    """分析逻辑（根据需求定制）"""
    pass

def save_chart(fig, name):
    """保存图表"""
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig.savefig(f"{OUTPUT_DIR}/{name}.png", dpi=150, bbox_inches='tight')

if __name__ == "__main__":
    # 主流程
    print("开始分析...")
```

---

## 错误处理清单

| 错误类型 | 原因 | 解决方案 |
|----------|------|----------|
| UnicodeDecodeError | 文件编码错误 | 尝试GBK/ISO-8859-1 |
| EmptyDataError | 空文件 | 拒绝并提示 |
| KeyError | 列名不存在 | 输出可用列名 |
| TypeError | 数据类型不匹配 | 转换或跳过 |
| MemoryError | 数据量过大 | 采样或拒绝 |
| TimeoutError | 执行超时 | 分批处理 |
| ValueError | 统计方法不适用 | 尝试其他方法 |
