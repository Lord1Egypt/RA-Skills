# 彩票分析助手 - 快速开始指南

## 🚀 一分钟上手

### 方法1：使用简化脚本（推荐）
```bash
# 进入技能目录
cd skills/lottery-analyzer

# 运行简化分析脚本
python scripts/analyze_ssq_simple.py
```

### 方法2：直接分析
```bash
# 使用内置数据生成推荐
python scripts/analyze_lottery.py ssq data/ssq_standard.csv 7+2
```

### 方法3：查看已有推荐
```bash
# 查看已生成的5注推荐
cat data/5_recommendations.json

# 或使用Python查看
python -c "import json; data=json.load(open('data/5_recommendations.json')); [print(f'第{r[\"序号\"]}注: {r[\"红球\"]} + {r[\"蓝球\"]}') for r in data['推荐号码']]"
```

## 📊 内置数据说明

### 数据文件
- `data/ssq_base_english.csv` - 原始数据（3438期）
- `data/ssq_standard.csv` - 标准格式（分析脚本专用）
- `data/5_recommendations.json` - 示例推荐结果

### 数据范围
- **期数**：2003001 至 2026041（共3438期）
- **时间**：2003年至2026年4月
- **最新**：2026041期（2026年第41期）

## 🎯 常用命令

### 1. 热号分析
```python
import sys
sys.path.insert(0, 'scripts')
from analyze_lottery import LotteryAnalyzer

analyzer = LotteryAnalyzer('ssq')
analyzer.load_data('data/ssq_standard.csv', has_header=False)
analyzer.extract_numbers(50)

print("热红球:", analyzer.red_freq.most_common(10))
print("热蓝球:", analyzer.blue_freq.most_common(5))
```

### 2. 生成推荐
```python
# 生成5组7+2复式推荐
recommendations = analyzer.generate_multiple_recommendations(5, '7+2')
for rec in recommendations:
    print(f"{rec['strategy']}: {rec['red_balls']} + {rec['blue_balls']}")
```

### 3. 自定义分析
```python
# 分析最近30期奇偶比例
analyzer.extract_numbers(30)
patterns = analyzer.analyze_patterns(30)
for p in patterns:
    print(f"奇偶: {p['odd_even']}, 大小: {p['big_small']}, 和值: {p['sum']}")
```

## 🔧 故障排除

### Windows编码问题
如果遇到编码错误，使用简化脚本：
```bash
python scripts/analyze_ssq_simple.py
```

### 数据加载失败
检查数据文件路径：
```bash
# 验证数据文件
python -c "import pandas as pd; df=pd.read_csv('data/ssq_standard.csv', header=None); print(f'行数: {len(df)}')"
```

### 依赖问题
确保已安装必要依赖：
```bash
pip install pandas numpy
```

## 📁 文件结构
```
lottery-analyzer/
├── SKILL.md              # 技能说明（已更新）
├── QUICK_START.md        # 本快速指南
├── scripts/              # 分析脚本
│   ├── analyze_lottery.py    # 核心分析
│   └── analyze_ssq_simple.py # 简化版（推荐）
├── data/                 # 数据目录
│   ├── ssq_base_english.csv    # 原始数据
│   ├── ssq_standard.csv        # 标准格式
│   ├── 5_recommendations.json  # 示例推荐
│   └── simple_analysis.json    # 简化分析结果
└── .clawhub/             # 安装信息
```

## 💡 使用技巧

### 1. 快速查看热号
```bash
python -c "
import sys
sys.path.insert(0, 'scripts')
from analyze_lottery import LotteryAnalyzer
a = LotteryAnalyzer('ssq')
a.load_data('data/ssq_standard.csv', False)
a.extract_numbers(30)
print('热号:', dict(a.red_freq.most_common(5)))
"
```

### 2. 生成单注推荐
```bash
python -c "
import sys
sys.path.insert(0, 'scripts')
from analyze_lottery import LotteryAnalyzer
import random
a = LotteryAnalyzer('ssq')
a.load_data('data/ssq_standard.csv', False)
a.extract_numbers(50)
hot = [n for n,_ in a.red_freq.most_common(10)]
print('推荐:', sorted(random.sample(hot, 6)))
"
```

### 3. 保存分析结果
```python
import json
results = {
    "热号": dict(analyzer.red_freq.most_common(10)),
    "冷号": dict(analyzer.red_freq.most_common()[-10:]),
    "推荐": recommendations
}
with open('my_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## ⚠️ 重要提醒

1. **数据更新**：内置数据更新到2026年4月，如需最新数据请自行更新
2. **编码问题**：Windows用户建议使用简化脚本
3. **理性购彩**：分析结果仅供参考，不保证中奖
4. **文件权限**：确保有读写data目录的权限

## 🔄 更新数据

如需更新到最新开奖数据：

1. 获取最新开奖数据（Excel/CSV格式）
2. 转换为标准格式：期号,红1,红2,红3,红4,红5,红6,蓝
3. 替换 `data/ssq_standard.csv` 文件
4. 重新运行分析

---

**版本**: 1.1.0  
**最后更新**: 2026-04-16  
**数据包含**: ✅ 是  
**开箱即用**: ✅ 是