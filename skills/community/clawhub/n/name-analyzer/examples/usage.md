# Name Analyzer - 使用示例

## 基本使用

### 分析名字

```bash
cd ~/.openclaw/skills/name-analyzer
python3 scripts/name_analyzer.py analyze
```

### 完整分析

```bash
python3 scripts/name_analyzer.py full
```

### 数理分析

```bash
python3 scripts/name_analyzer.py numerology
```

### JSON 输出

```bash
python3 scripts/name_analyzer.py analyze --json
```

## 程序化调用

```python
from name_analyzer import NameAnalyzer

analyzer = NameAnalyzer()
results = analyzer.analyze("张伟", full_mode=True)
print(results['score'])
print(results['meaning'])
```

## 输出示例

```
==================================================
📖 名字分析报告: 张伟
==================================================

🏷️ 类型: chinese
📍 来源: 中华文化姓氏/名字体系

💡 名字含义:
   伟: 伟大、卓越、雄伟

🔢 数理分析:
   生命道路数，代表人生主要课题: 6 (责任、家庭、和谐)
   人格数，代表外在表现: 5 (自由、变化、冒险)
   心灵数，代表内在渴望: 6 (责任、家庭、和谐)

🔍 偏部首:
   亻: 人属性 - 人缘、社交

👥 同名名人:
   • 马云（阿里巴巴创始人）
   • 邓小平和

📊 综合评分: 90/100

💡 建议:
   名字整体评分优秀

==================================================
```

