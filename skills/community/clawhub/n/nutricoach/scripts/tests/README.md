# NutriCoach 单元测试

## 测试结构

```
scripts/tests/
├── README.md                 # 本文件
├── run_all_tests.py          # 测试运行器
├── test_nutrition_calc.py    # 营养计算测试
├── test_database.py          # 数据库测试
└── manual/                   # 手动测试脚本
    ├── test_barcode_match.py
    ├── test_ocr_flow.py
    └── test_silent_scan.py
```

## 运行测试

### 运行所有测试
```bash
cd scripts/tests
python3 run_all_tests.py
```

### 运行单个测试文件
```bash
python3 test_nutrition_calc.py
python3 test_database.py
```

## 测试覆盖

### test_nutrition_calc.py
- **TestNutritionCalculation**: 营养计算核心功能
  - 按重量计算营养值
  - 每日营养汇总
  - BMI计算
  - TDEE计算 (Mifflin-St Jeor公式)

- **TestFoodDatabase**: 食物数据库
  - 必需营养字段完整性
  - 新增营养字段验证 (钙、铁、锌、维生素等)

- **TestPantryCalculations**: 食材库存计算
  - 剩余百分比计算
  - 过期天数计算
  - 过期状态分类

- **TestDataValidation**: 数据验证
  - 体重值范围验证
  - 食物数量解析

### test_database.py
- **TestDatabaseSchema**: 数据库结构
  - 用户表字段完整性
  - 餐食表字段完整性
  - 食物表字段完整性
  - 列索引类型验证

- **TestDatabaseOperations**: 数据库操作
  - 用户插入和查询
  - 体重记录插入
  - 餐食记录插入
  - 每日营养汇总查询

- **TestDataIntegrity**: 数据完整性
  - 热量计算一致性验证

## 测试状态

**当前状态**: ✅ 全部通过

```
总测试数: 20
通过: 20
失败: 0
错误: 0
```

## 添加新测试

1. 创建新的测试文件，如 `test_feature.py`
2. 继承 `unittest.TestCase`
3. 添加测试方法（以 `test_` 开头）
4. 在 `run_all_tests.py` 中导入并添加测试类

示例:
```python
import unittest

class TestMyFeature(unittest.TestCase):
    def test_something(self):
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()
```

## 持续集成

建议在以下场景运行测试:
- 修改核心计算逻辑后
- 数据库结构变更后
- 发布新版本前
- 定期回归测试
