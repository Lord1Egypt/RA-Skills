# Pandas常用操作参考

本文档提供pandas常用操作的快速参考和示例代码。

## 1. 数据读取与保存

### 读取数据
```python
# CSV文件
df = pd.read_csv('file.csv')
df = pd.read_csv('file.csv', encoding='utf-8', sep=',')

# Excel文件
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# JSON文件
df = pd.read_json('file.json')

# SQL数据库
df = pd.read_sql('SELECT * FROM table', connection)

# Parquet文件
df = pd.read_parquet('file.parquet')
```

### 保存数据
```python
# CSV
df.to_csv('output.csv', index=False, encoding='utf-8')

# Excel
df.to_excel('output.xlsx', sheet_name='Sheet1', index=False)

# JSON
df.to_json('output.json', orient='records', indent=2)

# Parquet
df.to_parquet('output.parquet', index=False)
```

## 2. 数据探索

### 基础信息
```python
# 查看前几行
df.head(10)
df.tail(5)

# 基础信息
df.info()
df.shape  # (行数, 列数)
df.columns  # 列名
df.dtypes  # 数据类型

# 统计摘要
df.describe()  # 数值列统计
df.describe(include='all')  # 所有列统计

# 缺失值
df.isnull().sum()
df.isna().sum()

# 重复值
df.duplicated().sum()

# 唯一值
df['column'].unique()
df['column'].nunique()
```

## 3. 数据选择与过滤

### 选择列
```python
# 单列
df['column_name']
df.column_name

# 多列
df[['col1', 'col2', 'col3']]
```

### 选择行
```python
# 按位置
df.iloc[0]  # 第一行
df.iloc[0:5]  # 前5行
df.iloc[0:5, 0:3]  # 前5行，前3列

# 按标签
df.loc[0, 'column_name']
df.loc[0:5, ['col1', 'col2']]
```

### 条件过滤
```python
# 单条件
df[df['age'] > 18]
df[df['name'] == 'Alice']

# 多条件 (AND)
df[(df['age'] > 18) & (df['gender'] == 'F')]

# 多条件 (OR)
df[(df['age'] < 18) | (df['age'] > 60)]

# NOT
df[~(df['age'] > 18)]

# isin
df[df['city'].isin(['Beijing', 'Shanghai'])]

# query方法
df.query('age > 18 and gender == "F"')
df.query('city in ["Beijing", "Shanghai"]')
```

## 4. 数据清洗

### 处理缺失值
```python
# 删除缺失值
df.dropna()  # 删除任何含有缺失值的行
df.dropna(axis=1)  # 删除任何含有缺失值的列
df.dropna(subset=['col1', 'col2'])  # 删除特定列有缺失的行
df.dropna(thresh=2)  # 保留至少有2个非空值的行

# 填充缺失值
df.fillna(0)  # 用0填充
df.fillna(method='ffill')  # 前向填充
df.fillna(method='bfill')  # 后向填充
df['column'].fillna(df['column'].mean())  # 用均值填充
df.fillna({'col1': 0, 'col2': 'Unknown'})  # 不同列不同填充值
```

### 删除重复值
```python
df.drop_duplicates()  # 删除所有重复行
df.drop_duplicates(subset=['col1'])  # 基于特定列删除重复
df.drop_duplicates(keep='last')  # 保留最后一个重复项
```

### 数据类型转换
```python
# 转换单列
df['column'] = df['column'].astype(int)
df['column'] = df['column'].astype(float)
df['column'] = df['column'].astype(str)

# 转换多列
df = df.astype({'col1': int, 'col2': float})

# 转换为日期时间
df['date'] = pd.to_datetime(df['date'])
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
```

### 处理异常值
```python
# IQR方法
Q1 = df['column'].quantile(0.25)
Q3 = df['column'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['column'] >= lower_bound) & (df['column'] <= upper_bound)]

# Z-score方法
from scipy import stats
z_scores = np.abs(stats.zscore(df['column']))
df = df[z_scores < 3]
```

## 5. 数据转换

### 列操作
```python
# 添加新列
df['new_col'] = df['col1'] + df['col2']
df['new_col'] = df['col1'].apply(lambda x: x * 2)

# 删除列
df.drop('column', axis=1, inplace=True)
df.drop(['col1', 'col2'], axis=1, inplace=True)

# 重命名列
df.rename(columns={'old_name': 'new_name'}, inplace=True)

# 列名标准化
df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
```

### 排序
```python
# 按单列排序
df.sort_values('column', ascending=True)

# 按多列排序
df.sort_values(['col1', 'col2'], ascending=[True, False])

# 按索引排序
df.sort_index()
```

### apply函数
```python
# 对列应用函数
df['column'].apply(lambda x: x * 2)
df['column'].apply(custom_function)

# 对多列应用函数
df.apply(lambda row: row['col1'] + row['col2'], axis=1)

# map函数
df['category'].map({'A': 1, 'B': 2, 'C': 3})
```

## 6. 分组与聚合

### groupby操作
```python
# 单列分组
df.groupby('category').mean()
df.groupby('category').sum()
df.groupby('category').count()

# 多列分组
df.groupby(['category', 'subcategory']).mean()

# 聚合多个函数
df.groupby('category').agg(['mean', 'sum', 'count'])

# 不同列不同聚合
df.groupby('category').agg({
    'sales': 'sum',
    'quantity': 'mean',
    'price': ['min', 'max']
})

# 自定义聚合函数
df.groupby('category').agg(custom_function)
```

### 透视表
```python
# 创建透视表
pd.pivot_table(df, 
               values='sales',
               index='category',
               columns='month',
               aggfunc='sum',
               fill_value=0)

# 多个聚合值
pd.pivot_table(df,
               values=['sales', 'quantity'],
               index='category',
               columns='month',
               aggfunc='sum')
```

## 7. 合并与连接

### concat拼接
```python
# 垂直拼接(按行)
pd.concat([df1, df2], ignore_index=True)

# 水平拼接(按列)
pd.concat([df1, df2], axis=1)
```

### merge合并
```python
# 内连接
pd.merge(df1, df2, on='key', how='inner')

# 左连接
pd.merge(df1, df2, on='key', how='left')

# 右连接
pd.merge(df1, df2, on='key', how='right')

# 外连接
pd.merge(df1, df2, on='key', how='outer')

# 多个键
pd.merge(df1, df2, on=['key1', 'key2'])

# 不同列名的键
pd.merge(df1, df2, left_on='key1', right_on='key2')
```

### join连接
```python
df1.join(df2, on='key', how='left')
```

## 8. 时间序列

### 日期时间操作
```python
# 解析日期
df['date'] = pd.to_datetime(df['date'])

# 提取日期组件
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['weekday'] = df['date'].dt.weekday
df['quarter'] = df['date'].dt.quarter

# 日期计算
df['date'] + pd.Timedelta(days=7)
df['date'] - pd.Timedelta(weeks=1)

# 设置日期为索引
df.set_index('date', inplace=True)

# 重采样
df.resample('D').mean()  # 按天
df.resample('M').sum()   # 按月
df.resample('Q').mean()  # 按季度
```

## 9. 字符串操作

```python
# 小写/大写
df['column'].str.lower()
df['column'].str.upper()

# 去除空格
df['column'].str.strip()
df['column'].str.lstrip()
df['column'].str.rstrip()

# 替换
df['column'].str.replace('old', 'new')

# 包含
df[df['column'].str.contains('pattern')]

# 分割
df['column'].str.split(',')
df[['col1', 'col2']] = df['column'].str.split(',', expand=True)

# 提取
df['column'].str.extract(r'(\d+)')  # 提取数字
```

## 10. 性能优化技巧

### 内存优化
```python
# 查看内存使用
df.memory_usage(deep=True)

# 优化数据类型
df['int_col'] = df['int_col'].astype('int32')  # 而非int64
df['cat_col'] = df['cat_col'].astype('category')  # 分类型

# 分块读取大文件
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process(chunk)
```

### 向量化操作
```python
# 使用向量化而非循环
df['result'] = df['col1'] * df['col2']  # 快
# 避免: for i in range(len(df)): ...  # 慢
```

### 使用query
```python
# query比布尔索引更快
df.query('age > 18 and city == "Beijing"')
```

## 11. 常见模式与最佳实践

### 链式操作
```python
result = (df
    .query('age > 18')
    .groupby('city')
    .agg({'sales': 'sum'})
    .sort_values('sales', ascending=False)
    .head(10)
)
```

### 避免SettingWithCopyWarning
```python
# 使用.loc
df.loc[df['age'] > 18, 'category'] = 'adult'

# 或使用copy()
df_filtered = df[df['age'] > 18].copy()
```

### 处理大数据集
```python
# 使用更高效的格式
df.to_parquet('file.parquet')  # 比CSV快很多

# 使用Dask处理超大数据集
import dask.dataframe as dd
ddf = dd.read_csv('large_file.csv')
```
