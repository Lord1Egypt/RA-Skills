---
name: lottery-analyzer
description: 彩票智能分析助手，支持双色球（SSQ）和大乐透（DLT）的深度数据分析、趋势预测和智能推荐。适用于：历史开奖数据统计分析、热号冷号追踪、奇偶和值走势、连号模式识别、智能号码推荐（单注/复式）、7+2/6+2复式方案生成。当用户需要分析彩票数据、生成推荐号码或查看号码热度排名时激活。
version: 1.1.0
author: 海东青智能体系统
last_updated: 2026-04-16
data_included: true
---

# 彩票分析助手

智能分析双色球和大乐透彩票数据，提供基于统计学的号码推荐和趋势分析。

## 🎁 本技能包含数据文件

本技能已包含完整的双色球历史开奖数据，无需额外准备数据文件即可直接使用。

**包含的数据文件：**
- `data/ssq_base_english.csv` - 原始双色球数据（3438期，2003-2026年）
- `data/ssq_standard.csv` - 标准格式数据（彩票分析助手专用格式）
- `data/5_recommendations.json` - 示例推荐结果

**数据范围：**
- 期数：2003001 至 2026041（共3438期）
- 时间：2003年至2026年4月
- 最新开奖：2026041期（2026年第41期）

## 支持彩票类型

- **双色球 (SSQ)**：6个红球(1-33) + 1个蓝球(1-16)
- **大乐透 (DLT)**：5个前区(1-35) + 2个后区(1-12)

## 快速开始

### 1. 使用内置数据直接分析（推荐）

本技能已包含完整历史数据，可直接分析：

```bash
# 使用内置数据文件分析双色球
python skills/lottery-analyzer/scripts/analyze_lottery.py ssq skills/lottery-analyzer/data/ssq_standard.csv 7+2

# 或使用简化脚本
python skills/lottery-analyzer/scripts/analyze_ssq_simple.py
```

### 2. 查看示例推荐结果

```bash
# 查看已生成的5注推荐
cat skills/lottery-analyzer/data/5_recommendations.json
```

### 3. 分析自定义数据文件

如果你有自己的开奖数据文件，也可以使用：

```bash
# 分析自定义数据文件
python skills/lottery-analyzer/scripts/analyze_lottery.py ssq /path/to/your_data.csv 7+2
```

格式说明：
- **ssq** / **dlt**：彩票类型
- **数据路径**：Excel或CSV文件路径
- **格式**：`simple`（单注）或 `7+2`（复式）

### 4. 对话式分析（推荐）

直接使用内置数据进行实时分析：

```python
import sys
sys.path.insert(0, 'skills/lottery-analyzer/scripts')
from analyze_lottery import LotteryAnalyzer

# 创建分析器
analyzer = LotteryAnalyzer('ssq')

# 加载内置数据（标准格式，无表头）
analyzer.load_data('skills/lottery-analyzer/data/ssq_standard.csv', has_header=False)

# 分析最近100期数据
analyzer.extract_numbers(100)

# 查看热号
print("热红球:", analyzer.red_freq.most_common(10))
print("热蓝球:", analyzer.blue_freq.most_common(5))

# 生成推荐
recommendations = analyzer.generate_multiple_recommendations(5, '7+2')

# 输出结果
for rec in recommendations:
    print(f"策略: {rec['strategy']}")
    print(f"红球: {' '.join(f'{n:02d}' for n in rec['red_balls'])}")
    print(f"蓝球: {' '.join(f'{n:02d}' for n in rec['blue_balls'])}")
```

## 数据文件格式

### 内置数据格式（已包含）

本技能包含的标准格式数据：
```csv
期号,红1,红2,红3,红4,红5,红6,蓝
2003001,10,11,12,13,26,28,11
2003002,4,9,19,20,21,26,12
...
2026041,2,8,10,17,19,24,13
```

### 自定义数据格式

如果你有自己的数据文件，支持以下格式：

**Excel格式：**
```csv
期号  红球号码        (表头行，可选)
26018   11  15  17  22  25  30  7
26017   1   3   5   18  29  32  4
...
```

**CSV格式：**
```csv
期号,红1,红2,红3,红4,红5,红6,蓝
26018,11,15,17,22,25,30,7
26017,1,3,5,18,29,32,4
```

## 核心分析功能

### 1. 统计分析

获取详细统计数据：

```python
stats = analyzer.generate_statistics()

# 输出内容：
{
    'red': {
        'hot_numbers': [13, 9, 3, 5, 2, ...],   # 热号（前15）
        'cold_numbers': [21, 11, 16, ...],      # 冷号（前10）
        'avg_number': 16.0,                      # 平均数
        'median': 15.0,                          # 中位数
        'stdev': 9.8                            # 标准差
    },
    'blue': {
        'hot_numbers': [10, 4, 13, ...],
        'cold_numbers': [9, 11, 14, ...]
    },
    'sum': {
        'avg': 95.9,      # 平均和值
        'min': 46,        # 最小和值
        'max': 133        # 最大和值
    }
}
```

### 2. 模式识别

分析近期走势：

```python
patterns = analyzer.analyze_patterns(10)  # 近10期

# 输出内容：
[
    {
        'consecutive': 1,      # 连号对数
        'odd_even': '3:3',     # 奇偶比例
        'big_small': '4:2',    # 大小比例
        'sum': 120,            # 和值
        'sum_range': '101-120' # 和值区间
    },
    ...
]
```

### 3. 智能推荐

多种推荐策略：

```python
# 策略1：均衡推荐（热冷混合）
rec = analyzer.recommend_numbers(strategy='balanced', format_type='7+2')

# 策略2：热号策略（推荐高频号码）
rec = analyzer.recommend_numbers(strategy='hot', format_type='7+2')

# 策略3：冷号策略（博冷门回归）
rec = analyzer.recommend_numbers(strategy='cold', format_type='7+2')

# 策略4：连号策略（包含连号组合）
rec = analyzer.recommend_numbers(strategy='consecutive', format_type='7+2')

# 策略5：区间策略（覆盖多个数字区间）
rec = analyzer.recommend_numbers(strategy='segment', format_type='7+2')
```

## 复式方案说明

### 7+2复式（双色球）

- 组合数：C(7,6) × C(2,1) = 7 × 2 = **14注**
- 费用：14注 × 2元 = **28元**
- 覆盖范围：7个红球中任选6个，2个蓝球中任选1个

### 7+2复式（大乐透）

- 组合数：C(7,5) × C(2,2) = 21 × 1 = **21注**
- 费用：21注 × 2元 = **42元**
- 覆盖范围：7个前区中任选5个，2个后区全选

### 6+2复式（双色球）

- 组合数：C(6,6) × C(2,1) = 1 × 2 = **2注**
- 费用：2注 × 2元 = **4元**
- 覆盖范围：6个红球全选，2个蓝球中任选1个

## 完整工作流示例

### 示例1：使用内置数据快速分析

```bash
# 进入技能目录
cd skills/lottery-analyzer

# 使用内置数据生成5组7+2推荐
python scripts/analyze_lottery.py ssq data/ssq_standard.csv 7+2

# 查看热号分析
python -c "
import sys
sys.path.insert(0, 'scripts')
from analyze_lottery import LotteryAnalyzer
analyzer = LotteryAnalyzer('ssq')
analyzer.load_data('data/ssq_standard.csv', has_header=False)
analyzer.extract_numbers(50)
print('热红球:', analyzer.red_freq.most_common(10))
"
```

### 示例2：生成5注不同策略的推荐

```python
# 生成5注不同策略的推荐
import sys
sys.path.insert(0, 'skills/lottery-analyzer/scripts')
from analyze_lottery import LotteryAnalyzer
import random

analyzer = LotteryAnalyzer('ssq')
analyzer.load_data('skills/lottery-analyzer/data/ssq_standard.csv', has_header=False)
analyzer.extract_numbers(100)

# 获取热号和冷号
hot_reds = [num for num, _ in analyzer.red_freq.most_common(15)]
cold_reds = [num for num, _ in analyzer.red_freq.most_common()[-15:]]
hot_blues = [num for num, _ in analyzer.blue_freq.most_common(8)]

# 生成5注不同策略的推荐
strategies = ['热号', '均衡', '冷号', '奇偶均衡', '大小均衡']
for i, strategy in enumerate(strategies, 1):
    if strategy == '热号':
        reds = random.sample(hot_reds, 6)
    elif strategy == '均衡':
        reds = random.sample(hot_reds, 4) + random.sample(cold_reds, 2)
    elif strategy == '冷号':
        reds = random.sample(cold_reds, 6)
    else:
        reds = random.sample(hot_reds, 6)
    
    blues = random.sample(hot_blues, 1)
    print(f"第{i}注 ({strategy}): 红球{sorted(reds)} 蓝球{blues}")
```

## 输出文件位置

分析结果默认保存在技能目录的data文件夹中：

```
skills/lottery-analyzer/data/
├── ssq_base_english.csv      # 原始数据
├── ssq_standard.csv          # 标准格式数据
├── 5_recommendations.json    # 示例推荐结果
└── lottery_analysis_results.json  # 分析结果（运行后生成）
```

你也可以指定其他保存位置：

```python
analyzer.save_results('./my_analysis.json')  # 保存到当前目录
```

## 技术依赖

- pandas（数据处理）
- numpy（数值计算）
- openpyxl（Excel支持，可选）

**Windows用户注意：** 如果遇到编码问题，可以使用提供的简化脚本或确保控制台使用UTF-8编码。

## 数据更新

### 1. 自动数据更新系统

本技能提供自动数据更新功能，支持通过消息自动添加新开奖数据。

**支持的输入格式：**
```
2026041 020810171924+13
双色球 2026041 020810171924+13
2026041 02 08 10 17 19 24 + 13
```

**自动更新脚本：**
```bash
# 启动自动更新系统
python scripts/openclaw_integration.py

# 测试数据更新
python scripts/openclaw_integration.py test
```

**功能特点：**
- ✅ 自动检测双色球数据格式
- ✅ 检查期号重复（重复则不添加）
- ✅ 验证号码有效性（范围1-33/1-16）
- ✅ 自动保存到 `data/ssq_standard.csv`
- ✅ 实时反馈添加结果
- ✅ 更新日志记录
- ✅ 可选自动分析

### 2. 手动更新内置数据

如果你想批量更新数据到最新开奖：

1. 获取最新的开奖数据（Excel或CSV格式）
2. 转换为标准格式：期号,红1,红2,红3,红4,红5,红6,蓝
3. 替换 `data/ssq_standard.csv` 文件
4. 重新运行分析

### 3. 数据验证

内置数据已验证：
- 总期数：3438期
- 数据范围：2003001 至 2026041
- 格式正确性：已通过脚本验证

## 免责声明

本工具仅基于历史数据进行统计分析，**不保证中奖**。彩票本质是随机事件，请理性购彩，量力而行。

分析结果仅供娱乐和参考，切勿过度投入。

**内置数据来源：** 公开的双色球历史开奖数据，经过格式标准化处理。

## 扩展功能

### 1. 自动数据更新系统

**核心脚本：**
- `update_data.py` - 数据更新核心逻辑
- `auto_update_handler.py` - 消息处理处理器
- `openclaw_integration.py` - OpenClaw集成脚本

**使用方式：**
```python
# 集成到OpenClaw消息处理
from scripts.openclaw_integration import OpenClawLotteryUpdater

updater = OpenClawLotteryUpdater()

# 处理收到的消息
message = "2026042 010305071113+09"
processed, reply = updater.process_incoming_message(message, "用户")

if processed and reply:
    print(f"需要回复: {reply}")
```

### 2. 自定义分析脚本

本技能提供以下实用脚本：

1. **快速分析脚本** - `analyze_ssq_simple.py`（避免编码问题）
2. **5注推荐生成** - `generate_5_recommendations.py`
3. **数据转换脚本** - 将原始数据转换为标准格式
4. **自动更新脚本** - 支持消息自动更新数据

### 3. 添加自定义分析

```python
# 自定义分析示例
import sys
sys.path.insert(0, 'skills/lottery-analyzer/scripts')
from analyze_lottery import LotteryAnalyzer

analyzer = LotteryAnalyzer('ssq')
analyzer.load_data('skills/lottery-analyzer/data/ssq_standard.csv', has_header=False)
analyzer.extract_numbers(100)

# 自定义统计：计算特定数字出现间隔
for num in range(1, 34):
    occurrences = [i for i, n in enumerate(analyzer.all_red_numbers) if n == num]
    if len(occurrences) > 1:
        intervals = [occurrences[i+1] - occurrences[i] for i in range(len(occurrences)-1)]
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        print(f"{num:02d}号: 出现{len(occurrences)}次, 平均间隔{avg_interval:.1f}期")
```

### 4. 与OpenClaw集成

**配置OpenClaw自动监听：**

1. 创建OpenClaw钩子脚本
2. 设置消息过滤器，识别双色球数据格式
3. 自动调用 `openclaw_integration.py` 处理消息
4. 返回处理结果给用户

**示例钩子配置：**
```python
# 在OpenClaw配置中添加消息处理器
{
  "hooks": {
    "message_received": {
      "script": "skills/lottery-analyzer/scripts/openclaw_integration.py",
      "patterns": [
        "^\\d{7}\\s+\\d{12}\\+\\d{2}$",
        "^双色球\\s+\\d{7}\\s+\\d{12}\\+\\d{2}$"
      ]
    }
  }
}
```

脚本完全
