# Pandas数据清洗最佳实践

本文档总结了使用pandas进行数据清洗的最佳实践和常见问题解决方案。

## 1. 数据质量检查清单

在开始清洗之前，先检查数据质量：

```python
def data_quality_check(df):
    """全面的数据质量检查"""
    print("=" * 60)
    print("数据质量报告")
    print("=" * 60)
    
    # 基础信息
    print(f"\n1. 基础信息:")
    print(f"   行数: {len(df):,}")
    print(f"   列数: {len(df.columns)}")
    print(f"   内存使用: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # 数据类型
    print(f"\n2. 数据类型分布:")
    print(df.dtypes.value_counts())
    
    # 缺失值
    print(f"\n3. 缺失值分析:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        '缺失数': missing,
        '缺失率(%)': missing_pct
    })
    missing_df = missing_df[missing_df['缺失数'] > 0].sort_values('缺失数', ascending=False)
    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("   ✓ 无缺失值")
    
    # 重复值
    duplicates = df.duplicated().sum()
    print(f"\n4. 重复行: {duplicates:,} ({duplicates/len(df)*100:.2f}%)")
    
    # 数据分布
    print(f"\n5. 数值列统计:")
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())
    
    print("=" * 60)
```

## 2. 缺失值处理策略

### 策略决策树

```
缺失值 → 缺失率?
├─ < 5%  → 删除行 (dropna)
├─ 5-30% → 填充
│   ├─ 数值型
│   │   ├─ 正态分布 → 均值填充
│   │   ├─ 偏态分布 → 中位数填充
│   │   └─ 有时序关系 → 前向/后向填充
│   └─ 分类型
│       ├─ 有众数 → 众数填充
│       └─ 无明显众数 → 填充"Unknown"
└─ > 30% → 考虑删除该列或标记为单独类别
```

### 实现示例

```python
def handle_missing_intelligently(df):
    """智能处理缺失值"""
    df = df.copy()
    
    for col in df.columns:
        missing_pct = df[col].isnull().sum() / len(df) * 100
        
        if missing_pct == 0:
            continue
        
        print(f"处理 {col}: 缺失率 {missing_pct:.2f}%")
        
        # 缺失率过高，考虑删除
        if missing_pct > 30:
            print(f"  → 建议删除 (缺失率过高)")
            continue
        
        # 数值型列
        if df[col].dtype in ['int64', 'float64']:
            # 检查偏度
            skewness = df[col].skew()
            if abs(skewness) < 0.5:  # 近似正态分布
                df[col].fillna(df[col].mean(), inplace=True)
                print(f"  → 用均值填充")
            else:  # 偏态分布
                df[col].fillna(df[col].median(), inplace=True)
                print(f"  → 用中位数填充")
        
        # 分类型列
        else:
            mode_val = df[col].mode()
            if len(mode_val) > 0:
                df[col].fillna(mode_val[0], inplace=True)
                print(f"  → 用众数填充: {mode_val[0]}")
            else:
                df[col].fillna('Unknown', inplace=True)
                print(f"  → 用'Unknown'填充")
    
    return df
```

## 3. 异常值检测与处理

### 多种检测方法对比

```python
def detect_outliers_multiple_methods(df, column):
    """使用多种方法检测异常值"""
    
    # 方法1: IQR (四分位距)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    iqr_lower = Q1 - 1.5 * IQR
    iqr_upper = Q3 + 1.5 * IQR
    iqr_outliers = df[(df[column] < iqr_lower) | (df[column] > iqr_upper)]
    
    # 方法2: Z-Score
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    zscore_outliers = df[z_scores > 3]
    
    # 方法3: 百分位数
    lower_percentile = df[column].quantile(0.01)
    upper_percentile = df[column].quantile(0.99)
    percentile_outliers = df[(df[column] < lower_percentile) | (df[column] > upper_percentile)]
    
    print(f"异常值检测结果 - {column}:")
    print(f"  IQR方法: {len(iqr_outliers)} 个异常值")
    print(f"  Z-Score方法: {len(zscore_outliers)} 个异常值")
    print(f"  百分位数方法: {len(percentile_outliers)} 个异常值")
    
    return {
        'iqr': iqr_outliers,
        'zscore': zscore_outliers,
        'percentile': percentile_outliers
    }
```

### 异常值处理策略

```python
def handle_outliers(df, column, method='cap', strategy='iqr'):
    """
    处理异常值
    
    method:
    - 'remove': 删除异常值
    - 'cap': 截断(winsorize)
    - 'transform': 对数变换
    - 'mark': 标记但不删除
    """
    df = df.copy()
    
    if strategy == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
    
    if method == 'remove':
        df = df[(df[column] >= lower) & (df[column] <= upper)]
    
    elif method == 'cap':
        df[column] = df[column].clip(lower=lower, upper=upper)
    
    elif method == 'transform':
        df[column] = np.log1p(df[column])  # log(1 + x)
    
    elif method == 'mark':
        df[f'{column}_is_outlier'] = (df[column] < lower) | (df[column] > upper)
    
    return df
```

## 4. 数据类型优化

### 内存优化技巧

```python
def optimize_dtypes(df):
    """优化数据类型以减少内存使用"""
    
    initial_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"初始内存使用: {initial_memory:.2f} MB")
    
    # 优化整数类型
    for col in df.select_dtypes(include=['int64']).columns:
        col_min = df[col].min()
        col_max = df[col].max()
        
        if col_min >= 0:  # 无符号整数
            if col_max < 255:
                df[col] = df[col].astype('uint8')
            elif col_max < 65535:
                df[col] = df[col].astype('uint16')
            elif col_max < 4294967295:
                df[col] = df[col].astype('uint32')
        else:  # 有符号整数
            if col_min > -128 and col_max < 127:
                df[col] = df[col].astype('int8')
            elif col_min > -32768 and col_max < 32767:
                df[col] = df[col].astype('int16')
            elif col_min > -2147483648 and col_max < 2147483647:
                df[col] = df[col].astype('int32')
    
    # 优化浮点数类型
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].astype('float32')
    
    # 优化对象类型为类别类型
    for col in df.select_dtypes(include=['object']).columns:
        num_unique = df[col].nunique()
        num_total = len(df[col])
        if num_unique / num_total < 0.5:  # 唯一值少于50%
            df[col] = df[col].astype('category')
    
    final_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"优化后内存使用: {final_memory:.2f} MB")
    print(f"节省: {(1 - final_memory/initial_memory)*100:.1f}%")
    
    return df
```

## 5. 字符串清洗

### 常见字符串问题处理

```python
def clean_string_column(df, column):
    """清洗字符串列"""
    df = df.copy()
    
    # 去除首尾空格
    df[column] = df[column].str.strip()
    
    # 统一大小写
    df[column] = df[column].str.lower()
    
    # 去除特殊字符
    df[column] = df[column].str.replace(r'[^\w\s]', '', regex=True)
    
    # 去除多余空格
    df[column] = df[column].str.replace(r'\s+', ' ', regex=True)
    
    # 替换空字符串为NaN
    df[column] = df[column].replace('', np.nan)
    
    return df
```

## 6. 日期时间处理

```python
def standardize_dates(df, date_columns):
    """标准化日期列"""
    df = df.copy()
    
    for col in date_columns:
        # 尝试解析各种日期格式
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # 检查无效日期
        invalid_dates = df[col].isnull().sum()
        if invalid_dates > 0:
            print(f"警告: {col} 有 {invalid_dates} 个无效日期")
        
        # 检查未来日期
        future_dates = (df[col] > pd.Timestamp.now()).sum()
        if future_dates > 0:
            print(f"警告: {col} 有 {future_dates} 个未来日期")
    
    return df
```

## 7. 完整的数据清洗流程

```python
def complete_data_cleaning_pipeline(df):
    """完整的数据清洗流程"""
    
    print("开始数据清洗流程...")
    print("=" * 60)
    
    # 1. 初始检查
    print("\n步骤1: 数据质量检查")
    data_quality_check(df)
    
    # 2. 删除完全重复的行
    print("\n步骤2: 删除重复行")
    before = len(df)
    df = df.drop_duplicates()
    print(f"  删除了 {before - len(df)} 行重复数据")
    
    # 3. 标准化列名
    print("\n步骤3: 标准化列名")
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    print(f"  列名已标准化")
    
    # 4. 处理缺失值
    print("\n步骤4: 处理缺失值")
    df = handle_missing_intelligently(df)
    
    # 5. 处理异常值
    print("\n步骤5: 检测异常值")
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        outliers = detect_outliers_multiple_methods(df, col)
    
    # 6. 优化数据类型
    print("\n步骤6: 优化数据类型")
    df = optimize_dtypes(df)
    
    # 7. 最终检查
    print("\n步骤7: 最终检查")
    data_quality_check(df)
    
    print("\n" + "=" * 60)
    print("数据清洗完成!")
    
    return df
```

## 8. 常见问题与解决方案

### 问题1: SettingWithCopyWarning

```python
# 错误方式
subset = df[df['age'] > 18]
subset['new_col'] = 0  # 可能触发警告

# 正确方式
subset = df[df['age'] > 18].copy()
subset['new_col'] = 0

# 或使用.loc
df.loc[df['age'] > 18, 'new_col'] = 0
```

### 问题2: 混合数据类型

```python
# 检测混合类型
def detect_mixed_types(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            types = df[col].apply(type).unique()
            if len(types) > 1:
                print(f"{col}: 混合类型 {types}")

# 转换为统一类型
df['mixed_col'] = df['mixed_col'].astype(str)
```

### 问题3: 大数据集处理

```python
# 分块处理
def process_large_file(filename, chunksize=10000):
    results = []
    for chunk in pd.read_csv(filename, chunksize=chunksize):
        cleaned_chunk = complete_data_cleaning_pipeline(chunk)
        results.append(cleaned_chunk)
    
    return pd.concat(results, ignore_index=True)
```

## 9. 数据验证

```python
def validate_cleaned_data(df):
    """验证清洗后的数据"""
    
    checks = {
        'no_duplicates': df.duplicated().sum() == 0,
        'no_nulls': df.isnull().sum().sum() == 0,
        'valid_dtypes': all(df.dtypes != 'object'),  # 假设所有object都应被转换
    }
    
    print("数据验证结果:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    return all(checks.values())
```

## 10. 最佳实践总结

1. **始终保留原始数据备份**
2. **记录清洗步骤**：保持可重现性
3. **渐进式清洗**：一次处理一个问题
4. **验证每一步**：确保没有引入新问题
5. **考虑业务逻辑**：技术清洗要符合业务规则
6. **文档化决策**：记录为什么这样处理
7. **性能优化**：对大数据集使用向量化操作
8. **数据类型优化**：减少内存使用
9. **自动化流程**：创建可复用的清洗管道
10. **持续监控**：定期检查数据质量
