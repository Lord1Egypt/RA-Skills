---
name: lol-analyst
description: "英雄联盟数据分析助手。查询召唤师信息、排位数据、对局历史、英雄熟练度，AI智能分析上分策略。需要Riot Games API Key。触发词：查战绩、LOL数据、英雄联盟、排位分析、对局分析、查段位、英雄熟练度、上分建议、lol analyst。"
env:
  RIOT_API_KEY: "Riot Games Developer API Key (必需)。获取方式: developer.riotgames.com 登录后自动生成"
always: false
---

# lol-analyst — 英雄联盟数据分析助手

基于 Riot Games Official API 的 LOL 数据分析 Skill，支持中文自然语言查询。

## 功能

| 功能 | 说明 | 触发词 |
|-----|------|--------|
| 🔍 召唤师查询 | 查询玩家基本信息 | 查查 {name#tag} 的信息 |
| 🏆 排位分析 | 排位段位、胜率、趋势 | 看看我的排位 / {name}的段位 |
| 📜 对局历史 | 最近N场对局详情 | 最近{20}把战绩 |
| ⭐ 英雄熟练度 | 英雄池分析 | 最擅长的英雄 |
| 🎯 AI智能解读 | LLM解读数据 | 分析我需要怎么改进 |
| 🆚 英雄对比 | 多英雄表现对比 | 对比我的 Jinx vs Caitlyn |

## 前置条件

### 1. 获取 Riot Games API Key

1. 访问 [Riot Developer Portal](https://developer.riotgames.com/)
2. 用你的 Riot Games 账号登录（就是玩LOL的账号）
3. 登录后自动生成 **Development API Key**（24小时过期）
4. 如需永久 Key：注册产品 → 申请 Personal API Key

### 2. 配置 API Key

在 Skill 首次运行时输入，或设置环境变量：

```bash
export RIOT_API_KEY="RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

## 使用示例

```
# 查询玩家
查查 虎牙丶Uzi#TW2 的信息

# 排位分析
看看 Faker#KR1 的排位

# 对局历史
我最近20把排位战绩

# 英雄分析
对比我的金克丝和凯特琳数据

# AI分析
分析我最近的对局，给上分建议
```

## 支持区域

| 代码 | 区域 |
|-----|------|
| KR | 韩国 |
| NA1 | 北美 |
| EUW1 | 西欧 |
| EUN1 | 北欧/东欧 |
| TW2 | 中国台湾 |
| JP1 | 日本 |
| BR1 | 巴西 |
| ... | 全部13个区域 |

## WorkBuddy 集成

### 前置条件

```bash
# 安装依赖（一次性）
C:/Users/PC/.workbuddy/binaries/python/envs/default/Scripts/pip install riotwatcher
```

### 调用方式

WorkBuddy 应通过 CLI 调用此 Skill：

```bash
PYTHON_PATH = "C:/Users/PC/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
SKILL_SCRIPT = "C:/Users/PC/.workbuddy/skills/lol-analyst/scripts/lol_analyst.py"

# 配置 API Key
{ PYTHON_PATH } { SKILL_SCRIPT } --setup --api-key "RGAPI-xxx"

# 查询召唤师档案 → 输出 HTML
{ PYTHON_PATH } { SKILL_SCRIPT } --profile --name "name#tag" --region kr --output result.html

# 查询对局历史
{ PYTHON_PATH } { SKILL_SCRIPT } --matches --name "name#tag" --region kr --count 20 --output matches.html

# 综合分析报告
{ PYTHON_PATH } { SKILL_SCRIPT } --analysis --name "name#tag" --region kr --count 20 --output analysis.html
```

### 结果呈现

脚本执行后输出 HTML 文件路径（格式：`__OUTPUT_FILE__:C:\path\to\file.html`），WorkBuddy 需：
1. 读取输出的 HTML 文件路径
2. 使用 `preview_url` 打开该 HTML
3. 用中文给用户解读关键数据

### 无 API Key 时的处理

如果用户没有 API Key，引导用户：
1. 访问 https://developer.riotgames.com/
2. 用 Riot 账号登录（就是玩LOL的账号）
3. 复制自动生成的 Development API Key（RGAPI-xxx 格式）
4. 在 WorkBuddy 中执行 `lol-analyst --setup --api-key "RGAPI-xxx"`

## 文件结构

```
lol-analyst/
├── SKILL.md
├── scripts/
│   ├── lol_analyst.py      # 主入口
│   ├── riot_client.py       # Riot API 封装
│   ├── config_manager.py    # 配置管理
│   └── report_generator.py  # HTML 报告生成
└── requirements.txt
```

## 技术栈

- Python 3.10+
- RiotWatcher (Riot API Python 封装)
- 纯 Python 标准库 HTML 报告（无外部前端依赖）
