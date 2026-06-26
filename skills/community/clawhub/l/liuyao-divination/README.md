# 六爻预测 Skill

## 简介

`liuyao-divination` 是一个专业的六爻预测工具，帮助AI Agent进行中国传统易学占卜。支持完整的六爻排盘流程：起卦、纳甲、寻世应、定六亲、配六神及吉凶判断。

## 安装要求

- Python 3.10+
- 依赖：无（标准库足够）
- 可选：`lunar-python`（用于更精确的农历计算）

## 使用方式

### 方式一：独立版本（推荐）

下载单个文件即可使用，无需依赖项目其他代码：

```bash
# 直接运行
python3 liuyao_standalone.py "今年财运如何" --sex 男
```

作为Python模块导入：

```python
from liuyao_standalone import LiuyaoSkill

skill = LiuyaoSkill()

# 执行占卜
result = skill.divinate("今年财运如何", "男")

# 使用结构化数据
print(result['date'])          # {'year': '甲辰', 'month': '丙寅', ...}
print(result['fortune'])       # {'level': '大吉', 'description': '...'}

# 或获取格式化文本
print(skill.format_text(result))
```

### 方式二：集成到现有项目

如果你已经克隆了整个项目，可以这样使用：

```python
from initialize import initialization
from utils import (
    deriveChange, seekForEgo, matchSkyandEarth,
    seekForReps, seekForDefects, seekForSouls, judgeFortune,
)

# 起卦
xiang = initialization('今年财运如何', '男')

# 完整排盘流程
deriveChange(xiang)
seekForEgo(xiang)
matchSkyandEarth(xiang)
seekForReps(xiang)
seekForDefects(xiang)
seekForSouls(xiang)
judgeFortune(xiang)

# 输出结果
print(f"吉凶结果: {xiang.fortune_result.value}")
print(f"分析: {xiang.fortune_description}")
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `liuyao_standalone.py` | **独立版本** - 包含所有代码，可直接使用（推荐） |
| `liuyao_skill.py` | 项目内使用版本（依赖项目其他文件）|
| `skill.yaml` | Claude Code Skill 配置 |
| `README.md` | 本文档 |

## 数据结构

### XIANG（象）
包含完整卦象信息的类：

- `base`: GUA - 本卦
- `change`: GUA - 变卦（如有）
- `question`: str - 所占事项
- `sex`: str - 卦主性别
- `origin`: int - 卦宫（乾7坎2艮4震1巽6离5坤0兑3）
- `year/month/day/hour`: List - 八字信息
- `lacks`: List - 空亡地支
- `defects`: List[Reps] - 缺失的六亲
- `fortune_result`: FortuneLevel - 吉凶等级
- `fortune_description`: str - 吉凶分析

### YAO（爻）
单个爻信息：

- `essence`: int - 本质（0阴1阳）
- `feature`: int - 特征（0变爻1静爻）
- `ego`: int - 世爻标记
- `other`: int - 应爻标记
- `najia`: List - 纳甲[天干, 地支]
- `representation`: Reps - 六亲
- `soul`: Soul - 六神

### 枚举类型

**天干 (Sky)**: 甲、乙、丙、丁、戊、己、庚、辛、壬、癸

**地支 (Earth)**: 子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥

**六亲 (Reps)**: 父母、官鬼、兄弟、妻财、子孙

**六神 (Soul)**: 青龙、朱雀、勾陈、腾蛇、白虎、玄武

**吉凶等级 (FortuneLevel)**: 大吉、吉、小吉、平、小凶、凶、大凶

## 用神参考

根据所占事项确定用神：

| 用神 | 所主事项 |
|------|----------|
| 妻财 | 求财、婚姻、财物、买卖、投资 |
| 官鬼 | 功名、官职、工作、考试、疾病、诉讼 |
| 父母 | 长辈、房屋、文书、考试、车辆 |
| 子孙 | 晚辈、医药、出行、解忧、孕产 |
| 兄弟 | 朋友、竞争、合作、分家 |

## 输出示例

```
==================================================
【占卜问题】 今年财运如何
【卦主】 男

【日期】丙午年 壬辰月 乙卯日 丙戌时
【旬空】子丑

【本卦六爻】
上爻：⚊ 阳(变) 父母壬戌 玄武 
五爻：⚊ 阳(变) 兄弟壬申 白虎 【应】
四爻：⚊ 阳 官鬼壬午 腾蛇 
三爻：⚊ 阳 兄弟丙申 勾陈 
二爻：⚋ 阴(变) 官鬼丙午 朱雀 【世】
初爻：⚋ 阴 父母丙辰 青龙 

【变卦六爻】
上爻：⚋ 阴 父母庚戌
五爻：⚋ 阴 兄弟庚申
四爻：⚊ 阳 官鬼庚午
三爻：⚊ 阳 兄弟辛酉
二爻：⚊ 阳 子孙辛亥
初爻：⚋ 阴 父母辛丑

【卦宫】乾宫 (7)
【世爻】第2爻
【应爻】第5爻
【缺失六亲】子孙、妻财

【吉凶判断】
结果：大凶
分析：有变爻，事情有变动；世爻临官鬼，多忧愁；
      卦中不见妻财，难求；用神妻财不上卦，大凶；
      世爻临朱雀，需谨慎
==================================================
```

## 文件说明

- `initialize.py` - 起卦与初始化
- `utils.py` - 核心算法（世应、纳甲、六亲、六神、吉凶判断）
- `XIANG.py` - 象（完整卦象）数据类
- `GUA.py` - 卦数据类
- `YAO.py` - 爻数据类
- `enums.py` - 枚举定义
- `skill.yaml` - Skill配置

## 测试

运行测试套件：

```bash
source venv/bin/activate
python3 run_tests.py
```

运行单个测试：

```bash
python3 -m pytest tests/test_core.py -v
python3 -m pytest tests/test_algorithms.py -v
python3 -m pytest tests/test_integration.py -v
```

## 注意事项

1. 日期计算依赖 `lunar-python` 库，确保已安装
2. 起卦使用 SHA256 哈希确保可复现性
3. 需要在虚拟环境中运行以获取正确的依赖

## License

MIT
