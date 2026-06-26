# GitHub实验准确度验证 - 参考文档

## 完整运作流程

### 阶段1: 仓库获取

```
尝试顺序:
1. git clone --depth 1 <url> <dir>
2. 失败 → Web下载: <url>/archive/refs/heads/main.zip
3. 解压到 projects/
```

### 阶段2: 数据处理

```
1. 复制数据文件到项目 data/ 目录
2. pandas.read_excel() 读取
3. 清洗NaN行
4. 分离训练/测试集
```

### 阶段3: 模型加载

```
1. 查找模型文件 (model.pt, *.pth)
2. torch.load(weights_only=False)
3. net.eval()
```

### 阶段4: 特征构建

```
根据项目调整:
- 历史特征: 前N天×M点
- 外部特征: 天气/时间/节假日
- 归一化: ÷最大值
```

### 阶段5: 预测验证

```
测试集: 最后N天
逐日预测→对比→计算误差
```

### 阶段6: 结果统计

```
MAE = mean(|pred - actual|)
RMSE = sqrt(mean((pred - actual)²))
MAPE = mean(|pred - actual|/actual) × 100%
Accuracy = 100% - MAPE
```

## 准确度评估标准

| 准确度 | 评估 |
|--------|------|
| ≥95% | 优秀 |
| 90-95% | 良好 |
| 80-90% | 一般 |
| <80% | 需改进 |

## 报告模板

```markdown
# {项目名} 准确度验证报告

## 1. 实验信息
- GitHub仓库: {url}
- 数据文件: {file}
- 实验日期: {date}
- 测试集大小: {N}天

## 2. 运作流程

### Step 1: 仓库获取
... (详细步骤)

### Step 2: 数据准备
... 

### Step 3: 模型加载
...

### Step 4: 特征构建
...

### Step 5: 预测验证
...

## 3. 准确度结果

| 指标 | 值 |
|------|-----|
| MAE | {value} |
| RMSE | {value} |
| MAPE | {value}% |
| 准确度 | {value}% |

## 4. 结论
...
```

## 典型项目结构

```
项目/
├── data/
│   └── data.xls
├── src/
│   ├── model.pt
│   ├── train.py
│   └── predict.py
├── README.md
└── outputs/
```