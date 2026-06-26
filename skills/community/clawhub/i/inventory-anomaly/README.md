# 库存异常检测和需求预测系统

这是一个完整的库存异常检测和需求预测系统，使用ARIMA模型进行需求预测，并生成TXT格式的库存预警报告。

## 快速开始

### 1. 创建项目结构

```bash
python scripts/create_structure.py your-project-name
```

### 2. 复制模板文件

将templates/目录下的模板文件复制到src/目录：

```bash
cp templates/data_manager_template.py src/data_manager.py
cp templates/inventory_template.py src/inventory.py
cp templates/demand_calculator_template.py src/demand_calculator.py
cp templates/anomaly_detector_template.py src/anomaly_detector.py
cp templates/predictor_template.py src/predictor.py
cp templates/generate_fake_data_template.py src/generate_fake_data.py
cp templates/main_template.py src/main.py
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 生成测试数据

```bash
python src/generate_fake_data.py
```

### 5. 运行系统

```bash
python src/main.py
```

## 系统功能

- **数据管理**：读取和写入Excel数据
- **库存查询**：查询库存状态和预警信息
- **需求计算**：计算日均、周均、月均需求
- **异常检测**：检测库存异常和需求异常
- **需求预测**：使用ARIMA模型预测未来需求
- **报告生成**：生成TXT格式的综合报告

## 自定义配置

### 修改配件信息

编辑`src/generate_fake_data.py`，修改配件信息：

```python
parts_info = pd.DataFrame({
    '配件ID': [f'P{i:03d}' for i in range(1, 21)],
    '配件名称': ['你的配件名称1', '你的配件名称2', ...],
    '规格': ['规格1', '规格2', ...],
    '单价': np.random.randint(50, 500, 20)
})
```

### 调整异常检测阈值

编辑`src/anomaly_detector.py`，修改标准差倍数：

```python
threshold = 3 * std_demand  # 改为其他值
```

### 修改预测周期

编辑`src/main.py`，修改预测周数：

```python
predictions = system.predict_demand(weeks_ahead=8)  # 预测8周
```

## 使用真实数据

将你的Excel文件放到data/目录，命名为`spare_parts.xlsx`，包含三个工作表：

1. **配件信息**：配件ID、名称、规格、单价
2. **库存**：配件ID、当前库存、安全库存、最大库存
3. **订单历史**：订单ID、配件ID、数量、日期

## 报告说明

系统生成的报告包含以下部分：

1. **库存概览**：总配件数、异常库存数
2. **异常检测**：库存异常列表，显示现有库存、需求数量、缺货数量
3. **需求预测**：未来4周预测，异常提醒和Z分数
4. **紧急补货建议**：需要紧急补货的配件列表

## 技术支持

- ARIMA时间序列预测
- 3倍标准差异常检测
- 每日自动数据更新机制
- TXT格式报告生成

## 扩展建议

1. **数据库集成**：将data_manager改为使用数据库
2. **API封装**：将系统功能封装为REST API
3. **可视化界面**：添加Web界面或GUI界面
4. **消息通知**：添加邮件、短信、钉钉等通知功能
5. **多模型支持**：支持Prophet、LSTM、XGBoost等预测模型