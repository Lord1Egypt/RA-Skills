# Skill Marketplace - 技能市场


## 🎯 推荐安装场景

✅ **你应该安装这个技能，如果：**
- [ ] 你想发现更多技能
- [ ] 你需要智能推荐
- [ ] 你想浏览 ClawHub 技能
- [ ] 你需要一键安装

❌ **不需要安装，如果：**
- [ ] 你手动搜索技能
- [ ] 你使用 CLI 安装

---

## ⭐ 觉得好用？

如果喜欢这个技能，请：
1. 在 ClawHub 给个 **⭐⭐⭐⭐⭐ 5 星好评**
2. 分享给其他 OpenClaw 用户
3. 提交 Issue 或 PR 改进

**你的评分对我们很重要！** 帮助更多人发现这个技能。

---

## 🔗 相关技能推荐

安装了这个技能的用户也安装了：

| 技能 | 作用 | 推荐度 |
|------|------|--------|
| [auto-backup](../auto-backup) | 自动备份 | ⭐⭐⭐⭐⭐ |
| [model-switch](../model-switch) | 模型切换 | ⭐⭐⭐⭐⭐ |
| [memory-enhancer](../memory-enhancer) | 增强记忆 | ⭐⭐⭐⭐⭐ |

**推荐组合安装：**
```bash
npx clawhub install openclaw-auto-backup
npx clawhub install openclaw-model-switch
npx clawhub install openclaw-memory-enhancer
```

---


发现和安装优质 OpenClaw 技能。

---

## ✨ 功能

### 🎯 智能推荐（v1.1.0 新增）
- **场景推荐** - 根据使用场景推荐技能组合（开发编程、内容创作等）
- **行业推荐** - 根据行业领域推荐（互联网、金融、教育等）
- **身份推荐** - 根据职业身份推荐（开发者、设计师、学生等）
- **基础必装** - 所有用户都应该安装的基础技能
- **排行榜** - Top 100 热门技能排行

### 🔍 技能发现（v1.3.0 增强）
- 🛒 **浏览技能** - 查看所有可用技能
- 🔎 **精确搜索** - 完全匹配名称、标签（`--exact`）
- 🔍 **模糊搜索** - 相似度匹配、中文关键词（`--fuzzy`）
- 🧠 **智能搜索** - 自动选择精确/模糊（默认）
- ⭐ **评分评论** - 用户评分和评论
- 📊 **排行榜** - 下载量/评分排行
- 🔔 **更新提醒** - 技能更新通知
- 📦 **一键安装** - 自动下载安装

**中文关键词映射：**
- "备份" → "backup"
- "模型" → "model"
- "记忆" → "memory"
- "搜索" → "search"
- "设计" → "design"
- [查看更多](#中文关键词映射)

---

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/skill-marketplace
```

---

## 📖 使用

### 🎯 智能推荐（v1.1.0 新增）

```bash
# 根据场景推荐
python3 skill-marketplace/scripts/recommend.py --scenario "开发编程"
# 输出：推荐技能组合 + 安装命令

# 根据行业推荐
python3 skill-marketplace/scripts/recommend.py --industry "互联网"

# 根据身份推荐
python3 skill-marketplace/scripts/recommend.py --role "开发者"

# 查看基础必装技能
python3 skill-marketplace/scripts/recommend.py --basic
# 输出：5 个基础必装技能（auto-backup, model-switch, memory-enhancer 等）

# 查看排行榜 Top 10
python3 skill-marketplace/scripts/recommend.py --top 10
# 输出：评分最高的 10 个技能

# 列出所有可用选项
python3 skill-marketplace/scripts/recommend.py --list-scenarios
python3 skill-marketplace/scripts/recommend.py --list-industries
python3 skill-marketplace/scripts/recommend.py --list-roles
```

### 🔍 增强搜索（v1.3.0 新增）

```bash
# 智能搜索（自动选择精确/模糊）
python3 skill-marketplace/scripts/search-enhanced.py "backup"

# 精确搜索（完全匹配名称、标签）
python3 skill-marketplace/scripts/search-enhanced.py "openclaw-auto-backup" --exact

# 模糊搜索（相似度匹配、中文关键词）
python3 skill-marketplace/scripts/search-enhanced.py "备份" --fuzzy
python3 skill-marketplace/scripts/search-enhanced.py "ai" --fuzzy

# 在 ClawHub 同步的技能中搜索
python3 skill-marketplace/scripts/search-enhanced.py "backup" --from-clawhub

# 列出所有关键词映射
python3 skill-marketplace/scripts/search-enhanced.py --list-keywords
```

**搜索示例：**
```bash
# 中文搜索
python3 search-enhanced.py "备份" --fuzzy
# 结果：openclaw-auto-backup

python3 search-enhanced.py "模型切换" --fuzzy
# 结果：openclaw-model-switch

python3 search-enhanced.py "记忆" --fuzzy
# 结果：openclaw-memory-enhancer

# 英文搜索
python3 search-enhanced.py "backup" --exact
# 结果：精确匹配名称包含"backup"的技能

python3 search-enhanced.py "design" --fuzzy
# 结果：openclaw-ui-designer
```

### 🔍 传统搜索

```bash
# 浏览技能
python3 skill-marketplace/scripts/browse.py

# 搜索技能
python3 skill-marketplace/scripts/search.py "backup"

# 安装技能
python3 skill-marketplace/scripts/install.py model-switch

# 查看排行榜
python3 skill-marketplace/scripts/rankings.py
```

---

## 📁 目录结构

```
skill-marketplace/
├── SKILL.md
├── README.md
├── config/
│   └── marketplace.json
└── scripts/
    ├── browse.py
    ├── search.py
    ├── install.py
    └── rankings.py
```

---

## 🈶 中文关键词映射

**支持中文搜索，自动映射到英文技能名：**

| 中文关键词 | 映射英文 | 对应技能 |
|-----------|---------|---------|
| 备份 | backup | openclaw-auto-backup |
| 模型 | model | openclaw-model-switch |
| 记忆 | memory | openclaw-memory-enhancer |
| 搜索 | search | openclaw-search-pro |
| 市场 | marketplace | openclaw-skill-marketplace |
| 发布 | publish | openclaw-clawhub-publish |
| 设计 | design | openclaw-ui-designer |
| 小说/写作 | novel/writing | openclaw-webnovel-writer |
| 多 Agent | multi-agent | openclaw-multi-agent-orchestrator |
| 脚手架/模板 | scaffold/template | openclaw-skill-scaffold |

**使用示例：**
```bash
# 中文搜索
python3 search-enhanced.py "备份" --fuzzy
python3 search-enhanced.py "模型切换" --fuzzy
python3 search-enhanced.py "记忆增强" --fuzzy
```

---

**作者：** @williamwg2025  
**版本：** 1.3.0（新增增强搜索）  
**许可证：** MIT-0

---

## 🔒 安全说明

### 代码来源 ✅
**所有脚本已包含：** browse.py, search.py, install.py, rankings.py
- ❌ 不克隆外部仓库
- ❌ 不下载外部代码

### 网络访问
- **脚本本身不联网**
- **install.py 调用 ClawHub** - 下载技能时联网（预期行为）

### 文件访问
- **读取：** 本地技能列表（可选）
- **写入：** install.py 安装技能到 skills/ 目录

### 系统操作
- **install.py：** 调用 `npx clawhub install <skill>`

### 使用建议
1. 检查 scripts/ 目录脚本
2. 先测试 browse.py 或 search.py
3. 安装技能时确保信任来源

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
