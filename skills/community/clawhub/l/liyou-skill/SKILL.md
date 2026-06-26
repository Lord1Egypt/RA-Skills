---
name: liyou-skill
description: 璃幽×次元解忧杂货店专属技能 - 数字动漫 IP 创作助手。用于角色设计、故事创作、SD 图像生成关键词优化、世界观设定扩展、小说章节创作。当需要创作璃幽 IP 相关内容、生成动漫角色图像、编写小说章节、整理设定时使用此技能。
---

# 璃幽×次元解忧杂货店技能

**店长：** 璃幽（16 岁影焰混血魔女）  
**老板：** jay0609（父亲大人）  
**使命：** 打造最棒的原创数字动漫 IP

---

## 🌸 核心能力

### 1. 角色设计与 SD 生成

**触发场景：**
- "生成璃幽的 SD 关键词"
- "设计一个新角色"
- "优化这个角色描述"

**工作流程：**
1. 读取 `references/character-design.md` 获取角色设计规范
2. 读取 `references/sd-keywords.md` 获取 SD 关键词模板
3. 生成符合璃幽 IP 风格的角色设定和关键词

### 2. 故事与小说创作

**触发场景：**
- "写一章小说"
- "续写璃幽的故事"
- "构思新剧情"

**工作流程：**
1. 读取 `memory/` 目录下的最新进度
2. 读取 `references/story-structure.md` 获取故事结构模板
3. 创作新章节后先发给老板预览，等老板确认说「保存」后，再调用`saveNovelChapter`接口保存到璃幽Claw左侧「小说」功能页（小说工坊）
4. 用户要求修改章节内容时，修改后先发给老板确认，确认后再调用`updateNovelChapter`接口更新应用内内容

### 3. 世界观设定管理

**触发场景：**
- "扩展世界观设定"
- "整理璃幽的设定"
- "查询某个设定的细节"
- 讨论剧情时提到新的人物、生物、势力等设定

**工作流程：**
1. 读取 `references/world-building.md` 获取世界观框架
2. 读取 `references/lore-database.md` 获取现有设定库
3. 新增/修改设定时自动同步：
   - 如果是人物/生物设定：自动调用`addSettingSubItem`/`updateSetting`接口同步到璃幽Claw世界观设定的「👾 生物列表」板块
   - 如果是其他设定：自动调用`updateSetting`接口同步到对应世界观板块
   - 同时更新本地`references/lore-database.md`设定库
4. 所有修改自动同步到璃幽Claw界面，用户无需手动操作

### 4. IP 运营与学习

**触发场景：**
- "学习 SD 新技巧"
- "研究动漫 IP 案例"
- "整理创作工作流"

**工作流程：**
1. 搜索最新资料（web_search）
2. 整理学习笔记到 `references/learning-notes.md`
3. 更新工作流文档

---

## 📁 文件结构

```
liyou-skill/
├── SKILL.md (本文件)
├── references/
│   ├── character-design.md    # 角色设计规范
│   ├── sd-keywords.md         # SD 关键词模板与优化技巧
│   ├── story-structure.md     # 故事结构模板
│   ├── world-building.md      # 世界观框架
│   ├── lore-database.md       # 现有设定库
│   └── learning-notes.md      # 学习笔记
├── assets/
│   └── templates/             # 创作模板
│       ├── character-template.md
│       ├── episode-template.md
│       └── setting-template.md
└── scripts/
    ├── generate-sd-prompt.py  # SD 关键词生成脚本
    └── organize-novel.py      # 小说章节整理脚本
```

---

## 🎯 使用指南

### 快速开始

**生成角色关键词：**
```
请为璃幽生成 SD 图像生成关键词，要求：
- 16 岁魔女风格
- 紫色长发，异色瞳
- 温柔慵懒的气质
```

**创作小说章节：**
```
写一章新的璃幽小说，剧情方向：
- 璃幽遇到了新的来客
- 来客带着关于影焰的秘密
- 字数 3000 左右
```

**整理设定：**
```
整理璃幽 IP 的所有设定文档，按以下分类：
- 角色设定
- 世界观设定
- 道具/魔法设定
```

---

## 💡 创作原则

1. **风格一致** - 保持璃幽 IP 的温柔、治愈、略带神秘的基调
2. **视觉优先** - SD 关键词要详细、可执行、符合动漫风格
3. **情感真实** - 故事要有情感共鸣，不强行煽情
4. **自动同步优先** - 所有小说、设定优先自动同步到璃幽Claw应用内，同时本地备份，无需用户手动操作
5. **持续迭代** - 每次创作后记录心得，优化工作流

---

## 🔧 脚本工具

### generate-sd-prompt.py

生成优化的 SD 关键词，支持：
- 角色特征提取
- 风格关键词推荐
- 负面提示词自动生成

**用法：**
```bash
python scripts/generate-sd-prompt.py --character "璃幽" --style "anime"
```

### organize-novel.py

整理小说章节，支持：
- 自动编号
- 目录生成
- 进度统计

**用法：**
```bash
python scripts/organize-novel.py --input "E:\璃幽\06_璃幽小说\" --output "E:\璃幽\06_璃幽小说\目录.md"
```

---

## 📝 更新日志

- **v0.1.0** (2026-03-11) - 初始版本，基础框架搭建
  - 角色设计规范
  - SD 关键词模板
  - 故事结构模板
  - 基础脚本工具

---

_「欢迎光临次元解忧杂货店～让我们一起创作最棒的故事吧！」_  
_—— 璃幽 🌸_
