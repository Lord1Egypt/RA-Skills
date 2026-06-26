---
name: github-experiment-accuracy
description: GitHub仓库项目准确度验证实验 - 给定GitHub仓库地址和数据文件，运行项目并验证预测准确度，生成详细流程报告和准确度报告。用于：1) 用户给出一个GitHub仓库+数据文件进行实验；2) 验证算法对目标数据的预测准确度；3) 生成包含流程+准确度的完整实验报告。
---

# GitHub仓库项目准确度验证实验

## 快速开始

用户给出一个GitHub仓库URL和一个数据文件，运行项目并验证准确度，生成报告。

```bash
# 输入参数
github_url: https://github.com/username/repo
data_file: D:/path/to/data.xls
```

## 完整流程

### Step 1: 仓库获取

1. **优先尝试 git clone**
   ```bash
   git clone {github_url} {project_dir} --depth 1
   ```
2. **失败则用 Web 下载**
   ```powershell
   Invoke-WebRequest -Uri "{github_url}/archive/refs/heads/main.zip" -OutFile "outputs/repo.zip"
   Expand-Archive -Path "outputs/repo.zip" -DestinationPath "outputs/projects"
   ```

### Step 2: 数据准备

```python
# 1. 复制数据到项目
Copy-Item {data_file} -Destination "{project_dir}/data/"

# 2. 读取数据
df = pd.read_excel(data_file)

# 3. 数据清洗
valid_idx = ~df.iloc[:, 1:].isna().any(axis=1)
df_valid = df[valid_idx]
```

### Step 3: 查找并加载模型

```python
# 查找模型文件
model_file = glob.glob(f"{project_dir}/**/model.pt", recursive=True)[0]

# 加载模型
net = torch.load(model_file, map_location='cpu', weights_only=False)
net.eval()
```

### Step 4: 特征工程

分析项目README或代码，构建特征：

```python
# 典型特征 (需根据项目调整)
- 历史数据特征: 前N天 × 维度 = X维
- 天气特征: N维
- 时间特征: 星期(7) + 节假日(2) = 9维
```

### Step 5: 预测验证

```python
# 测试集: 最后30天
test_days = 30
predictions = []
actuals = []

for i in range(len(df_valid) - test_days, len(df_valid)):
    # 构建特征
    features = build_features(df_valid.iloc[i])
    # 预测
    pred = net(features)
    predictions.append(pred)
    actuals.append(df_valid.iloc[i].values)
```

### Step 6: 计算准确度

```python
mae = mean(|predictions - actuals|)
rmse = sqrt(mean((predictions - actuals)²))
mape = mean(|predictions - actuals| / actuals) * 100
accuracy = 100 - mape
```

### Step 7: 生成报告

```markdown
# 实验报告

## 1. 实验信息
- GitHub仓库: {url}
- 数据文件: {file}
- 测试集: {N}天

## 2. 运作流程 (详细步骤)

### Step 1: 仓库获取
...

### Step 2: 数据准备
...

### Step 3: 模型加载
...

### Step 4: 特征工程
...

### Step 5: 预测验证
...

## 3. 准确度结果

| 指标 | 值 |
|------|-----|
| MAE | {mae:.2f} |
| RMSE | {rmse:.2f} |
| MAPE | {mape:.2f}% |
| 准确度 | {accuracy:.2f}% |
```

## 关键代码片段

### 模型加载
```python
from torch import load, Tensor, no_grad
import torch.nn as nn

# 加载 (新版torch需要weights_only=False)
net = load(model_file, map_location='cpu', weights_only=False)
net.eval()
```

### 数据处理
```python
import pandas as pd
import numpy as np

df = pd.read_excel(data_file, sheet_name=0, header=None)
# 清洗NaN
valid = ~df.isna().any(axis=1)
df = df[valid]
```

### 准确度计算
```python
mae = np.mean(np.abs(pred - actual))
rmse = np.sqrt(np.mean((pred - actual)**2))
mape = np.mean(np.abs((pred - actual) / actual)) * 100
```

## 报告位置

报告保存在:
- `{project_dir}/accuracy_report.md`
- `{project_dir}/experiment_report.md`
- `{project_dir}/outputs/daily_results.json`

## 常见问题

1. **网络超时**: 使用 Web 下载 ZIP 方式
2. **模型加载错误**: 使用 `weights_only=False`
3. **数据找不到**: 复制到项目 data/ 目录
4. **特征构建**: 参考项目 README 或源码