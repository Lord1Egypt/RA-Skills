<div align="center">

# 🎭 novel-creator 3.0

### 先学文风，再写长篇

功能内聚、强记忆、可连载的中文小说创作工作台。

</div>

---

## ✨ 3.0 核心升级

- **四种工作模式**
  - **快速开写**：先出样章，再补设定
  - **标准建书**：完整建档、规划卷纲、进入连载
  - **继续连载**：读取现有 `plan/` 与 `memory/` 直接续写
  - **救稿重构**：从已有稿件反推结构，修复大纲与记忆

- **正式加入“文风预热阶段”**
  - 写正文前先读取指定题材样本
  - 自动提炼语感、句式、对白、意象和禁忌写法
  - 生成 `plan/style_guide.md` 作为后续章节的固定文风卡

- **功能内聚**
  - 规划、记忆、节奏控制、文风预热、语感校准、连载维护放在同一技能里完成
  - 只有在用户明确需要时，才额外进入题材研究或平台风向分析

- **更安全的初始化**
  - 支持 `minimal` / `full` 两种初始化模式
  - 清空旧项目时先自动备份
  - 新增 `manifest.json` 记录项目状态

---

## 🚀 适合什么场景

- “帮我开一本悬疑长篇”
- “先写一章样章试试”
- “继续写第 12 章”
- “这本书写崩了，帮我重整大纲”
- “写之前先学一下这个题材的文风”

---

## 🧩 这个技能能干嘛

- 能把一句灵感快速变成可开写的小说项目，而不是只吐一段散乱正文
- 能区分你现在是在开新书、继续连载、救稿重构，还是只想先看样章
- 能在开写前先做文风预热，产出稳定可复用的 `plan/style_guide.md`
- 能初始化 `plan/`、`memory/`、`output/`、`manifest.json`，把长篇创作做成可持续工程
- 能在逐章创作时优先读取最近单元计划和必要记忆，降低人物失真、设定打架、伏笔遗失
- 能在章节完成后推动更新大纲、角色状态、情节记录和伏笔回收状态
- 能跟踪关键物品、线索、法宝、遗物的出现、易手、消耗和状态变化
- 能在同一技能内完成按题材去机械感、人味化润色，以及必要的市场/平台方向研究

## 🎯 适合谁用

- 想从一句题材灵感直接开书的人
- 已经写到一半，需要持续连载但怕前后设定打架的人
- 手里有旧稿、残纲、废稿，想重整结构再救回来的人
- 想先看某个题材笔触和语感对不对，再决定是否长写的人
- 想把小说创作流程做成“可追踪、可回填、可复盘”工作流的人

## 🛠️ 它通常会产出什么

- `plan/outline.md`：全书长线规划
- `plan/current_arc.md`：当前卷或篇章目标
- `plan/current_unit.md`：最近 3-5 章的推进单元
- `plan/style_guide.md`：文风预热卡
- `memory/roles.md`：角色状态与关系
- `memory/plot_points.md`：关键情节记录
- `memory/story_bible.md`：世界观与底层规则
- `memory/foreshadowing.md`：伏笔状态与回收进度
- `memory/items.md`：关键物品与线索流转
- `output/第xx章_章节名.md`：章节正文
- `manifest.json`：项目元信息

---

## 📂 目录结构

```text
novel-creator/
├── SKILL.md
├── README.md
├── assets/
│   ├── init/
│   │   ├── outline.md
│   │   ├── current_unit.md
│   │   ├── style_guide.md
│   │   ├── ...
│   ├── chapter-template.md
│   ├── memory-template.md
│   ├── plan-template.md
│   ├── PROMPT-TEMPLATE.md
│   └── style-guide-template.md
├── examples/
├── references/
├── scripts/
│   ├── init-novel.ps1
│   ├── init-novel.sh
│   └── check_chapter_wordcount.py
```

运行脚本时会在当前工作目录生成：

```text
output/
plan/
memory/
manifest.json
backup/
```

---

## 🧭 3.0 工作流

初始化脚本会优先读取 `assets/init/` 下的模板来生成工作区文件，因此以后调整默认结构时，改模板即可同步影响脚本输出。

`assets/` 下其余模板文件的职责：
- `assets/init/`：初始化脚本直接读取的真实模板源
- `assets/style-guide-template.md`：扩展版文风预热参考卡
- `assets/chapter-template.md`：单章写作参考结构
- `assets/plan-template.md`、`assets/memory-template.md`：字段设计与结构参考稿，不直接被脚本消费
- `assets/PROMPT-TEMPLATE.md`：提示词拼装参考

### 1. 分流任务
- 新建
- 续写
- 救稿
- 样章

### 2. 最小确认
优先只确认：
- 题材
- 模式（网文 / 文学）
- 当前任务
- 生成节奏
- 是否需要市场调研

### 3. 文风预热
写之前先读：
- `examples/[题材].md`
- 必要时 `references/小说经典片段赏析_[题材].md`

然后生成：
- `plan/style_guide.md`

### 4. 初始化
- `minimal`：适合样章、快速试写
- `full`：适合正式建书、长期连载

### 5. 逐章创作
每次优先读取：
- `plan/current_unit.md`
- `plan/style_guide.md`
- 必要的 `memory/*.md`

### 6. 章节完成后
- 保存正文
- 更新 `plan/`
- 更新 `memory/`
- 回填伏笔推进/回收状态
- 回填关键物品与线索流转记录
- 跑字数检查脚本

---

## 💡 技能使用例子

### 快速开写

```text
帮我开一本青春校园小说，先不要问太多，先给我一章样章看看感觉。
```

```text
我只有一句话灵感：高三转学生回到老家重点中学，发现自己能听见别人撒谎时的杂音。先试写第一章。
```

### 标准建书

```text
我们正式开一本长篇悬疑，题材偏现实刑侦，先建完整工作区，再做卷纲、当前单元和角色表。
```

```text
帮我做一个都市职场长篇，模式偏网文，目标 150 万字，先完成初始化和大纲，再进入样章。
```

### 继续连载

```text
继续写下一章。先读取当前目录里的 plan 和 memory，不要重开项目。
```

```text
接着写第 13 章，重点承接上一章结尾的反转，把女主怀疑和男主隐瞒同时推进。
```

```text
继续写第 21 章。先检查哪些伏笔快到回收点了，再确认那枚铜戒现在在谁手里。
```

### 救稿重构

```text
这本书写崩了，帮我按救稿模式处理。先抽取现有剧情事实，重建 current_unit，再决定后面怎么写。
```

```text
我这边有旧稿和残纲，但人物关系已经乱了。不要直接续写，先回填 memory，再修结构。
```

```text
先别写正文，先帮我把旧稿里的伏笔、已回收伏笔和关键物品流转全部整理进 memory。
```

### 文风预热

```text
正式写之前，先学一下青春校园题材的文风，给我生成 style_guide。
```

```text
这本书想走悬疑推理里偏冷感、克制、细节型叙述，先做文风预热，不急着出正文。
```

### 配套能力调用场景

```text
这一章先写完，然后帮我把语感修得更像真人写的青春校园文。
```

```text
我想走平台爆款路线，先研究一下这个题材最近常见套路，再决定大纲。
```

---

## 🗺️ 推荐使用方式

### 路线 A：一句灵感直接起步

1. 让技能判断是“快速开写”
2. 先做文风预热
3. 生成样章
4. 感觉对了再补全 `plan/` 和 `memory/`

### 路线 B：正式做长篇

1. 使用 `full` 初始化工作区
2. 明确题材、模式、节奏和是否需要市场调研
3. 生成 `style_guide.md`
4. 搭建 `outline.md`、`current_arc.md`、`current_unit.md`
5. 进入逐章创作与持续更新

### 路线 C：已有项目继续连载

1. 保留当前目录里的 `plan/`、`memory/`、`output/`
2. 让技能先检测现有工作区
3. 优先读取 `current_unit`、`style_guide` 和必要记忆
4. 直接续写并回填最新变化

### 路线 D：旧稿救回来

1. 不直接盲写
2. 先抽取已有剧情事实
3. 重建最近单元和关键记忆
4. 再决定重写样章还是继续往后推进

---

## 🛠️ 初始化脚本

### PowerShell

```powershell
./scripts/init-novel.ps1 "夜航档案" -Mode minimal
./scripts/init-novel.ps1 "夜航档案" -Mode full
./scripts/init-novel.ps1 "夜航档案" -Mode full -Clean
./scripts/init-novel.ps1 "夜航档案" -Mode full -TargetDir "D:\\novels\\夜航档案"
```

### Bash

```bash
./scripts/init-novel.sh "夜航档案" --mode minimal
./scripts/init-novel.sh "夜航档案" --mode full
./scripts/init-novel.sh "夜航档案" --mode full --clean
./scripts/init-novel.sh "夜航档案" --mode full --target-dir ~/novels/夜航档案
```

---

## 🤝 鸣谢与许可

本项目是对以下两个优秀的开源 Agent Skill 的合并与深度定制升级版本：
- **[chinese-novelist](https://github.com/penglonghuang/chinese-novelist-skill)** (MIT License)
- **[novel-generator](https://clawhub.ai/ITYHG/novel-generator)** (MIT License)

感谢原作者们的卓越贡献！


## ⚖️ 许可证

本项目遵循 **MIT License**。
