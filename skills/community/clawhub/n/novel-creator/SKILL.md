---
name: novel-creator
description: 为中文长篇小说、连载网文、章节样稿、已有草稿续写提供一套完整且内聚的创作流程：分流新建/续写/救稿任务，维护 plan/ 与 memory/ 记忆系统，在写正文前先学习指定题材的文风笔触，再按节奏持续产出章节，并在同一技能内完成文风校准、题材适配、连载维护与必要的创作研究。适用于用户要求写小说、开书、搭大纲、出样章、分章节连载、继续写下一章、修大纲救稿、想让 AI 先学某个题材的文风再开写时。
metadata:
  author: km1001
  version: "3.0.0"
  language: zh-CN
  category: creative-writing
  license: "MIT"
  tags: "novel, fiction, creative-writing, chinese, 小说生成, 连载, 样章"
---

# novel-creator 3.0

这是一个内聚式小说创作工作台，不是单纯的“写一段正文”工具。

它的职责只有四件事：
1. 判断当前任务属于新建、续写还是救稿
2. 维护 `plan/` 与 `memory/`，保证长篇不穿帮
3. 在开写前完成**文风预热**，先学题材笔触再落笔
4. 在同一套流程里完成规划、写作、风格校准与连载维护

---

## 核心原则

### 1. 先分流，再写
不要一上来就长问卷，也不要一上来就盲写。

先判断当前任务属于哪一类：
- **新建**：用户要开一本新书
- **续写**：已有 `plan/` / `memory/`，继续写下一章
- **救稿**：已有大纲或稿子，但结构、人设、节奏需要重整
- **样章**：用户只想先看一章或一段试笔

### 2. 文风预热是正式阶段，不是可选装饰
开始写正文前，必须先学习指定题材的文风笔触。

优先读取：
- `examples/` 中对应题材文件，如 `examples/青春校园.md`
- 必要时再读取 `references/` 中对应题材赏析文件，如 `references/小说经典片段赏析_青春校园.md`

预热后必须把结论写入：
- `plan/style_guide.md`

后续每次开写章节前，都优先读取：
- `plan/current_unit.md`
- `plan/style_guide.md`
- 当前章节必要的 `memory/` 文件，如 `memory/roles.md`、`memory/plot_points.md`
- 如果本章涉及伏笔推进、回收或悬念兑现，必须额外读取 `memory/foreshadowing.md`
- 如果本章涉及关键物品出现、易手、损坏、消耗、封印解除或线索转移，必须额外读取 `memory/items.md`

### 3. 保真高于炫技
除非用户明确要求改剧情，否则：
- 不乱补设定
- 不擅自改视角
- 不强行扩写成另一段故事
- 不为了“像小说”而牺牲原逻辑

### 4. 功能内聚
- **按题材去 AI / 人味化润色 / 题材表达校准** → 由当前技能直接处理
- **市场/平台趋势研究** → 只有用户明确需要时才在当前技能流程内处理

不要把“规划、生成、风格化、去 AI、市场研究”全部绑成强制前置步骤。

---

## 四种工作模式

## 模式 A：快速开写
适用情况：
- 用户只有一句想法
- 想先看味道对不对
- 不想先填很多设定

处理方式：
1. 用最少问题确认题材、主角、核心冲突
2. 执行文风预热
3. 生成一章样章
4. 顺手创建最小 `plan/` 与 `memory/`

特点：
- 启动快
- 更像“先试吃再建书”

## 模式 B：标准建书
适用情况：
- 用户明确要做长篇
- 需要系统规划、卷纲、记忆库

处理方式：
1. 确认创作方向
2. 执行文风预热
3. 初始化完整工作区
4. 生成大纲、单元计划、角色设定
5. 再开始逐章创作

## 模式 C：继续连载
适用情况：
- 当前目录已有 `plan/` 或 `memory/`
- 用户要继续写下一章

处理方式：
1. 检测已有工作区
2. 读取 `plan/current_unit.md`、`plan/style_guide.md` 与必要记忆文件
3. 确认上章结尾与本章任务
4. 直接续写

## 模式 D：救稿 / 重构
适用情况：
- 用户已有稿子，但大纲、人设、节奏失控
- 想从已有内容反推结构

处理方式：
1. 先识别现有问题类型
2. 重建 `plan/outline.md`、`plan/current_arc.md`、`plan/current_unit.md`
3. 必要时修复 `memory/`
4. 再决定是重写样章还是继续往后写

---

## 总流程

## 阶段 0：工作区检测

开始前先检查当前目录是否已有以下内容：
- `plan/`
- `memory/`
- `output/`
- `manifest.json`

判断逻辑：
- **若存在完整工作区** → 优先视为续写项目
- **若只存在零散稿件** → 视为救稿项目
- **若什么都没有** → 视为新建项目

不要在检测到旧项目时直接清空。
必须先确认用户是：
- 继续当前项目
- 基于当前项目另开分支
- 完整重开

## 阶段 1：最小需求确认

不再默认进入冗长问卷。

只优先确认这 5 项：
1. **当前任务**：新建 / 续写 / 救稿 / 样章
2. **题材**：悬疑 / 校园 / 仙侠 / 爽文 / 科幻等
3. **模式**：网文 / 文学 / 未定
4. **生成节奏**：先一章 / 连写几章 / 长线连载
5. **是否需要市场调研**：只有用户明确想要爆款路线、平台套路、受众偏好时才做

如果用户没有完整想法，再补以下轻量问题：
- 主角是谁
- 当前最想看的冲突是什么
- 这一章或这一卷最想给读者什么感觉

## 阶段 1.5：文风预热（强制）

这是 3.0 最重要的新阶段。

### 目标
在写正文前先学会指定类型小说的笔触，而不是边写边猜。

### 操作
1. 读取 `examples/` 中对应题材文件，如 `examples/青春校园.md`
2. 如果题材复杂或用户要求更强风格，再读取 `references/` 中对应题材赏析文件，如 `references/小说经典片段赏析_青春校园.md`
3. 提炼并写入 `plan/style_guide.md`

### `plan/style_guide.md` 必须包含
- 题材
- 叙事温度
- 推荐视角
- 句式节奏
- 对白习惯
- 常用意象 / 词汇场
- 禁忌写法
- 去 AI 注意点
- 本书专属偏好

### 何时刷新
- 开新书时必须生成
- 用户切换题材或明显改文风时必须更新
- 连载中如果文风跑偏，也应回写修正

## 阶段 2：初始化

初始化不再只有一种重模式。
以下条目均为**初始化后生成的工作区文件**，首次运行前可能不存在。

### 最小初始化
适用于快速开写：
- `plan/outline.md`
- `plan/current_unit.md`
- `plan/style_guide.md`
- `memory/roles.md`
- `memory/plot_points.md`
- `memory/story_bible.md`
- `manifest.json`

### 完整初始化
适用于标准建书：
- `plan/outline.md`
- `plan/current_arc.md`
- `plan/current_unit.md`
- `plan/style_guide.md`
- `memory/roles.md`
- `memory/locations.md`
- `memory/plot_points.md`
- `memory/story_bible.md`
- `memory/errors.md`
- `memory/foreshadowing.md`
- `memory/items.md`
- `manifest.json`

初始化脚本优先使用：
- Windows：`scripts/init-novel.ps1`
- Unix：`scripts/init-novel.sh`

脚本默认在**当前工作目录**初始化工作区；
如果要把工作区建到别处，可显式传目标目录参数。
初始化内容优先来自 `assets/init/` 模板，避免脚本与模板双份维护。
`assets/` 下其余模板默认视为参考资料，而不是初始化脚本输入源。

如用户选择重开且需要清空旧内容：
- 必须先备份旧工作区
- 再执行清理

## 阶段 3：结构构建

### 新建项目
根据需求生成工作区文件：
- `plan/outline.md`
- `plan/current_arc.md`（若是长篇或全量模式）
- `plan/current_unit.md`
- 基础 `memory/` 文件，如 `memory/roles.md`、`memory/plot_points.md`

要求：
- 在 `plan/current_arc.md` 中明确写出“**这个篇章存在的意义**”
- 在 `plan/current_unit.md` 中明确写出“**这个单元存在的意义**”
- 在单元内每一章的规划里补出“**这一章存在的意义**”

### 续写项目
不要重建全书。
只更新：
- 本卷目标
- 当前单元任务
- 必要的角色/伏笔/物品状态

### 救稿项目
优先做三件事：
1. 抽取已有剧情事实
2. 回填 `memory/plot_points.md` 与 `memory/roles.md`
3. 重写 `plan/current_unit.md`，恢复最近几章的推进秩序

救稿时尤其要补足：
- 这个篇章为什么必须存在
- 这个单元为什么不能删
- 每一章如果删掉，会损失什么

## 阶段 4：逐章创作

每章创作前按以下顺序读取：
1. `plan/current_unit.md`
2. `plan/style_guide.md`
3. `plan/current_arc.md`（如存在）
4. 必要的 `memory/` 文件，如 `memory/roles.md`、`memory/plot_points.md`
5. 涉及伏笔推进或回收时，读取 `memory/foreshadowing.md`
6. 涉及关键物品或线索流转时，读取 `memory/items.md`
7. 上一章结尾

### 章节写作规则
- **网文模式**：节奏快，反馈直接，优先推进冲突与回报
- **文学模式**：节奏允许更缓，但必须保证情绪或悬念递进
- **默认不要超长铺垫**：先让章节成立，再谈雕花

### 字数建议
- 网文模式：`2500-4000`
- 文学模式：`3500-5000`

### 输出前的处理
- 默认做一轮轻量按题材语感校准与去机械化润色
- 如果用户要求更自然、更像真人写的、或更像某类小说，则在当前技能内进一步加强题材笔触与表达校准

## 阶段 5：保存与更新

章节完成后按顺序执行：
1. 保存正文到 `output/`，文件名格式为 `第xx章_章节名.md`
2. 更新 `plan/outline.md`
3. 更新 `plan/current_unit.md`
4. 必要时更新 `plan/current_arc.md`
5. 更新 `memory/roles.md`
6. 更新 `memory/plot_points.md`
7. 如本章埋下新伏笔、推进旧伏笔、部分兑现或正式回收，更新 `memory/foreshadowing.md`
8. 如本章出现关键物品、线索、凭证、法宝、遗物，或发生易手、损坏、消耗、封印变化，更新 `memory/items.md`
9. 如有新增，再更新地点、错误记录等其他记忆文件
10. 运行 `scripts/check_chapter_wordcount.py`
11. 当一个 unit 或关键事件完成后，必须做一次“合理性复盘”

### 更新原则
- 只更新被本章真正改变的内容
- 不要把所有记忆文件每次都重写一遍
- 已失效条目用状态列标记，不删除历史
- 伏笔条目优先更新“状态”和“计划回收节点”；已兑现的伏笔不要直接删掉，应标记为已回收
- 物品条目优先更新“当前持有者”“状态”“流转与消耗记录”；已经消耗或损毁的物品不要直接删掉

### 合理性复盘规则
当一个单元、篇章或关键事件完成后，必须回头检查：
- 这个段落 / 单元 / 章节存在的意义是否真的完成
- 人物行为是否符合此前人设
- 事件推进是否过于巧合
- 因果链是否完整
- 如果删掉这一段，故事会不会反而更紧

按题材执行不同严格度：
- **纪实类文学 / 现实题材**：严格检查，不允许明显便利性推进、悬浮行为或偷懒跳步
- **网络爽文 / 高速类型**：允许少量小 bug 或轻微便利性推进，但不得伤及主线逻辑、核心人设和关键因果

---

## `plan/` 设计

`plan/` 用来控制宏观到微观的写作路线。
以下条目均为初始化后生成的工作区文件。

| 文件 | 作用 | 读取优先级 |
|---|---|---|
| `plan/current_unit.md` | 最近 3-5 章的具体推进，并说明每章/每单元存在的意义 | 最高 |
| `plan/style_guide.md` | 当前作品的文风笔触卡 | 最高 |
| `plan/current_arc.md` | 当前卷 / 当前阶段目标，并说明该篇章存在的意义 | 高 |
| `plan/outline.md` | 全书长线规划 | 中 |

### 读取原则
- 写章节时，优先读 `plan/current_unit.md` + `plan/style_guide.md`
- 卡文、换卷、修大纲时，再重读 `plan/outline.md`

---

## `memory/` 设计

`memory/` 用来记录已经发生的客观事实。
以下条目均为初始化后生成的工作区文件。

所有表格型记忆都应带状态列，便于按需检索和过滤。

| 文件 | 作用 |
|---|---|
| `memory/roles.md` | 角色状态与关系；至少记录性别，非现实题材额外记录种族/物种 |
| `memory/locations.md` | 地点与场景 |
| `memory/plot_points.md` | 已发生关键事件 |
| `memory/story_bible.md` | 世界观、规则、等级体系 |
| `memory/errors.md` | 穿帮与修正记录 |
| `memory/foreshadowing.md` | 伏笔与回收状态 |
| `memory/items.md` | 关键物品和线索流转 |

### 检索原则
- 只读取与当前章节相关、且状态有效的条目
- 不要把整本书所有历史一次性塞回上下文
- 对 `memory/foreshadowing.md`，优先检索“未回收 / 部分暗示 / 即将回收”的条目
- 对 `memory/items.md`，优先检索“仍在场 / 仍有效 / 正在流转”的条目

---

## 何时启用增强处理

### 启用题材语感强化
在以下情况应主动加强：
- 章节已经写完，但机器味重
- 用户说“更自然一点”“更像真人写的”
- 用户明确指定题材笔触
- 用户说“更像悬疑文 / 校园文 / 仙侠文”
- 需要按题材压掉机械感，同时把语感校准到对应类型

### 启用创作研究
仅在以下情况启用：
- 用户明确要“对标平台爆款”
- 用户想研究当前流行套路
- 需要题材市场趋势，而不是单纯写作

不要把创作研究作为默认步骤。

---

## 失败与回退策略

### 如果信息不够
- 优先进入快速开写模式
- 先给样章，再补设定

### 如果文风不稳
- 回到 `plan/style_guide.md`
- 重新做一次文风预热

### 如果剧情跑偏
- 先修 `plan/current_unit.md`
- 再修相关 `memory/` 文件
- 不要直接硬写下一章

### 如果项目太旧太乱
- 先按“救稿模式”回填结构
- 再决定是否继续写

---

## 附录：推荐资源

需要时按需读取：
- `references/prompt-guide.md`
- `references/plot-structures.md`
- `references/chapter-guide.md`
- `references/dialogue-writing.md`
- `references/hook-techniques.md`
- `references/character-building.md`
- `references/content-expansion.md`
- `references/consistency.md`
- `references/quality-checklist.md`

文风预热优先读取：
- `examples/` 中对应题材文件，如 `examples/青春校园.md`
- `references/` 中对应题材赏析文件，如 `references/小说经典片段赏析_青春校园.md`

脚本：
- `scripts/init-novel.ps1`
- `scripts/init-novel.sh`
- `scripts/check_chapter_wordcount.py`
