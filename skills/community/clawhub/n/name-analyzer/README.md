# Name Analyzer

名字分析工具，提供名字含义、来源、性格分析、数理分析等功能。

## 功能特点

- 📖 **名字含义** - 解析名字的语义和典故
- 🌍 **来源分析** - 追溯名字的文化渊源
- 🔢 **数理分析** - 基于姓名的生命灵数、人格数、心灵数
- 👥 **重名查询** - 查询同名名人
- 📊 **综合评分** - 名字的整体评分和建议

## 快速开始

```bash
# 分析名字
python3 scripts/name_analyzer.py analyze --name "张伟"

# 完整分析
python3 scripts/name_analyzer.py full --name "李明"

# 数理分析
python3 scripts/name_analyzer.py numerology --name "Michael"

# JSON 输出
python3 scripts/name_analyzer.py analyze --name "张伟" --json
```

如果不传 `--name`，脚本会默认分析 `张伟`。

## 目录结构

```
name-analyzer/
├── SKILL.md
├── README.md
├── scripts/
│   └── name_analyzer.py
├── tests/
│   └── test_basic.md
└── examples/
    └── usage.md
```

## 依赖

- Python 3.8+
- 无外部依赖
