# 室内设计工程预算自动生成技能

## 功能
- 基于隐室空间设计标准模板（爱琴海岸版）自动生成新预算表
- 按空间自动拆分分项工程清单
- 保留项目特征、品牌备注列格式
- 支持不同面积、类型项目（家装/办公/餐饮）

## 使用方法
```bash
# 交互式生成
python3 generate_budget.py --output ~/Desktop/new_budget.xlsx

# 命令行参数
python3 generate_budget.py \
  --name "瑞安叠墅项目" \
  --client "陈总" \
  --address "瑞安市XX楼盘" \
  --area 210 \
  --type "home" \
  --output /path/to/output.xlsx
```

## 模板来源
标准模板：`/Users/laobaobei/Downloads/同步空间/财务文件/爱琴海岸1-2001/杨总爱琴海岸预算.xlsx`

## 格式规范（保持工作室标准）
1. 表头：工程名称、客户姓名、地址、面积、联系方式
2. 分空间列项：客餐厅、主卧、次卧、书房、厨房、卫生间、阳台等
3. 每一项包含：序号、项目名称、项目特征、计量单位、工程量、单价、合价、备注（品牌）
4. 最后汇总：总价、税金
