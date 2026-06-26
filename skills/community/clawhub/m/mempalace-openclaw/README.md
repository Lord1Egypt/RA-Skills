# MemPalace Skill

> 让 AI 记住所有对话，随时搜索，像人一样积累经验。

---

## 一、这是什么？

MemPalace 是给 AI 用的长期记忆系统。

普通 AI 的记忆只在"当前对话"里，关掉就没了。MemPalace 把对话永久存档，还能语义搜索。

---

## 二、优势对比

| | 普通 memory/ | MemPalace |
|---|---|---|
| 存储位置 | workspace 内，仅当前项目 | 本地，跨项目 |
| 搜索方式 | 关键词匹配 | 语义向量搜索（懂意思）|
| 数据结构 | 扁平文件 | Wing > Room > Drawer 层级 |
| 长期积累 | 越积越多 AI 越慢 | 定时压缩，按需查询 |
| 本地存储 | ✅ | ✅ 全部在你电脑 |
| 自动归档 | ❌ | ✅ 每天自动 |

---

## 三、是否本地存储？

全部本地，没有任何数据上云。

所有文件存在 skill 同目录下的 palace_data/ 文件夹里：
- 对话归档：palace_data/convos/
- 向量索引：palace_data/.mempalace/
- 配置文件：palace_data/mempalace.yaml

---

## 四、目录结构

mempalace/                    Skill 根目录
├── mempalace/                内置 MemPalace 源码
│   ├── cli.py, miner.py     等所有源码文件
│   └── pyproject.toml       pip install -e 所需
├── scripts/
│   └── archive.ps1          归档和搜索脚本
├── palace_data/              首次运行后自动创建
│   ├── convos/              归档的对话文件
│   └── .mempalace/          ChromaDB 向量索引
├── mempalace.yaml            Wing/Room 配置
└── SKILL.md

---

## 五、如何安装

第一步：安装 skill
通过 ClawHub 安装：
clawhub install mempalace-openclaw

或手动：把 mempalace 文件夹放到你的 OpenClaw skills 目录

第二步：安装依赖（自动）
第一次运行 /mem-arc 时会自动：
1. 从 skill 源码目录安装 mempalace Python 包
2. 安装 chromadb 和 pyyaml 依赖
3. 创建 palace_data/ 目录
4. 完成初始化

无需手动敲命令，AI 会自动处理。

---

## 六、三个命令

| 命令 | 效果 |
|------|------|
| /mem-arc | 手动归档当前对话 |
| /mem-sea <关键词> | 搜索历史记忆 |
| /mem-asave | 立即保存今天记忆 |

---

## 七、自动归档

设置好后，每天 23:00 AI 会自动把当天对话归档，不需要手动操作。

---

## 八、兼容哪些 AI？

✅ OpenClaw  ✅ XClaw  ✅ WorkBuddy  ✅ Claude Code  ✅ 所有支持 Python + Skill 的 AI

---

## 九、常见问题

Q: 会泄露隐私吗？
A: 不会。所有数据存在你本地，不上传任何服务器。

Q: 存档的内容是什么？
A: AI 自动压缩，只保留精华（决策、配置、待办），删除废话。

Q: 记忆太多会变慢吗？
A: 不会。搜索是向量匹配，只返回最相关的几条。

---

*Skill: mempalace-openclaw | Version 1.4.0 | ClawHub: mempalace-openclaw | 基于 milla-jovovich/mempalace*
