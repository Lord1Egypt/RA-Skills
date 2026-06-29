# lol-analyst — 英雄联盟数据分析助手 🎮

基于 **Riot Games Official API** 的 LOL 数据分析 WorkBuddy Skill，支持中文自然语言查询，生成暗色主题 HTML 可视化报告。

## ✨ 功能

| 功能 | 说明 |
|-----|------|
| 🔍 召唤师查询 | 通过 Riot ID（name#tag）查询玩家基本信息 |
| 🏆 排位分析 | 段位、胜率、胜点、队列分布 |
| 📜 对局历史 | 最近 N 场对局，KDA / 补刀 / 经济 / 参团 |
| ⭐ 英雄熟练度 | Top 10 英雄熟练度 + 点数 |
| 📊 综合分析 | 多维度数据汇总 + AI 洞察占位 |
| 📄 多格式输出 | HTML 暗色主题报告 / JSON 原始数据 |

## 🚀 快速开始

### 1. 获取 Riot API Key

访问 [Riot Developer Portal](https://developer.riotgames.com/)，用你的 LOL 账号登录，自动生成 **Development API Key**（RGAPI-xxx 格式）。

> ⚠️ 开发 Key 每 24 小时过期，长期使用建议申请 Personal Key。

### 2. 安装依赖

```bash
pip install riotwatcher
```

### 3. 配置并查询

```bash
# 配置 API Key
python scripts/lol_analyst.py --setup --api-key "RGAPI-xxxxxxxx"

# 查询召唤师
python scripts/lol_analyst.py --profile --name "Faker#KR1" --region kr --output faker.html

# 对局历史（最近20场）
python scripts/lol_analyst.py --matches --name "Faker#KR1" --region kr --count 20

# 综合分析报告
python scripts/lol_analyst.py --analysis --name "Faker#KR1" --region kr --output report.html
```

## 🌍 支持区域

| 代码 | 区域 | 代码 | 区域 |
|-----|------|-----|------|
| KR | 韩国 | NA1 | 北美 |
| EUW1 | 西欧 | EUN1 | 北欧/东欧 |
| JP1 | 日本 | TW2 | 中国台湾 |
| BR1 | 巴西 | OC1 | 大洋洲 |

> ⚠️ 中国区（CN服）由腾讯独立运营，Riot API 不覆盖。

## 📁 项目结构

```
lol-analyst/
├── SKILL.md              # WorkBuddy Skill 定义
├── README.md
├── requirements.txt
├── .gitignore
└── scripts/
    ├── lol_analyst.py    # 主入口 CLI
    ├── riot_client.py    # Riot API 封装（RiotWatcher）
    ├── config_manager.py # 配置 + 区域映射 + 中文翻译
    └── report_generator.py # HTML 暗色主题报告生成
```

## 🎨 报告预览

生成的 HTML 报告采用 LOL 主题暗色风格：
- 🟡 金色（#c9a84c）强调色
- 🌑 深蓝黑色背景渐变
- 📊 胜率 / KDA 颜色区分（绿/黄/红）
- 📱 响应式布局

## 🔧 技术栈

- **Python 3.10+**
- **RiotWatcher** 3.x — Riot API Python 封装
- **Riot Games Official API** v5
- 纯标准库 HTML 生成（无前端框架依赖）

## 📄 License

MIT
