# 在 Chatbox 中使用 Advanced Human Writing & AI Humanizer

这份说明用于解决两个问题：

- 这个项目能不能在 Chatbox 里用
- 长篇写作时怎样尽量不丢上下文

结论：可以用。这个项目输出的是纯文本指令包，不依赖插件。你用 CLI 生成指令包后，把它粘贴到 Chatbox 的 system prompt，或者作为新会话的第一条消息即可。

## 为什么还是可能丢上下文

Chatbox 的上下文通常包含：

- System Prompt
- 聊天历史
- 当前问题

但是模型本身有上下文窗口限制，Chatbox 也有最大上下文消息数设置。长对话写久以后，早期内容可能不再进入模型本次请求。因此，长文本不要只依赖聊天记录，要维护一份独立的 continuity ledger，也就是“连续性账本”。

## 推荐设置

1. 选择上下文窗口更大的模型。
2. 在 Chatbox 设置里提高 maximum context messages / 最大上下文消息数。
3. 每个小说、文章系列、章节或项目单独开一个会话。
4. 能设置 system prompt 的话，把本项目生成的指令包放进去。
5. 如果当前 Chatbox 界面没有 system prompt，就把指令包作为新会话第一条消息，并声明“以下是本会话长期规则”。
6. 每隔几轮更新一次连续性账本，必要时用账本开启新会话。

## 生成 Chatbox 指令包

小说写作示例：

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --module controlled-drift `
  --module narrative-bridges `
  --module relationship-state `
  --module natural-measurement `
  --module embodied-emotion `
  --module vocal-rhythm `
  --module cultural-anchors `
  --review `
  --context examples/story-ledger.md `
  --task "把这些作为 Chatbox 写作会话的长期规则。现在不要开始正文，等待我的场景任务。"
```

自媒体写作示例：

```powershell
python -m humanwriting.cli build `
  --style self-media `
  --module imperfect-prose `
  --module cultural-anchors `
  --module vocal-rhythm `
  --review `
  --context examples/article-brief.md `
  --task "把这些作为 Chatbox 写作会话的长期规则。现在不要开始正文，等待我的文章任务。"
```

## 不丢上下文的使用流程

每 3 到 5 次长输出，或者你感觉对话变长时，做一次账本更新。

### 1. 让 Chatbox 更新账本

复制这段给 Chatbox：

```text
只更新连续性账本，不要继续正文。

保留：
- 固定事实
- 活跃线索
- 关系状态
- 当前在场者、可能偷听者、公开或私下场合
- 关系公开立场、私下立场和信息权限
- 谁能在谁面前提谁、允许语气、禁泄秘密和例外动机
- 声音锚点
- 人物稳定说话基线、知识/角色约束、披露习惯和面对不同听众的变化
- 当前对话契约：谈话目的、各方所求、不可透露内容、回应策略和预期状态变化
- 未关闭的互动欠账：待回应、拒绝、打断、产生后果或延迟回收的关键台词与动作
- 空间位置和座位/站位
- 物理资源的形态、容量和占用者
- 服装、鞋子、伤口和道具状态
- 已写出的移动过渡
- 已写出的形态转换，例如座椅放倒、桌面清空、床铺展开
- 当前场景或章节状态
- 节拍桥：上一拍残留、进入压力、下一步微转折、结尾压力
- 最近输出后新增为真的事实
- 新暴露的秘密、新产生的怀疑、阵营变化和提及策略变化
- 未解决问题和悬而未决的压力

删除：
- 重复措辞
- 已放弃的方案
- 泛泛总结
- 后续连续性不需要的信息
```

### 2. 保存账本

把 Chatbox 输出的账本复制到本地 Markdown 文件，例如：

```text
my-novel-ledger.md
```

### 3. 用最新账本重新生成指令包

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --module controlled-drift `
  --module narrative-bridges `
  --module relationship-state `
  --module natural-measurement `
  --module embodied-emotion `
  --module vocal-rhythm `
  --review `
  --context my-novel-ledger.md `
  --task "从当前场景状态继续。严格保留固定事实、活跃线索和未解决压力。"
```

### 4. 必要时开启新会话

出现下面情况时，建议新开 Chatbox 会话：

- 当前会话超过 20 到 30 轮
- 模型开始重复
- 人物、设定、时间线开始漂移
- 要进入新章节、新文章或新方向

新会话第一条消息粘贴最新指令包即可。

## 在 Chatbox 中审查已有稿件

如果不是续写，而是检查已经写好的章节，先用本项目生成审稿指令：

```powershell
python -m humanwriting.cli audit `
  --draft my-chapter.md `
  --context my-novel-ledger.md
```

把输出粘贴到 Chatbox。它会要求模型先抽取证据表，再检查座位、隔板、触达、服装、鞋子、道具和伤口是否矛盾。

如果要审查假精确数字：

```powershell
python -m humanwriting.cli audit `
  --draft my-chapter.md `
  --profile numbers
```

它会要求模型列出每个精确数字，判断是必须保留、可保留、应弱化还是应删除。

### 在 Chatbox 中运行多阶段审稿

```powershell
human-writing-skills pipeline `
  --draft my-chapter.md `
  --context my-novel-ledger.md `
  --auto `
  --output-dir chapter-audit
```

为输出目录中的每个阶段分别新建 Chatbox 会话，再粘贴对应 Markdown。不要在同一个会话里连续运行全部阶段，否则上一阶段的判断会影响下一阶段。全部完成后，再根据清单合并重复问题和修复顺序。

## 可直接复制的 Chatbox 开场消息

```text
请把下面内容作为本次写作会话的长期规则。

规则：
- 始终维护连续性账本。
- 每次写正文前，先检查固定事实、活跃线索、声音锚点和当前状态。
- 对话前检查“说话人 -> 听话人/在场观众 -> 被提及第三方”，并核对人物基线、
  当场目的、知识/角色约束、回应关系、提及策略和信息权限；职业不能直接替代人物性格。
- 关键台词或动作之后，转场前必须出现语言、动作、可读沉默、明确打断或延迟回应；
  不要让互动刺激无痕消失，也不要把每句话机械写成一问一答。
- 涉及车内、房间、电梯、餐桌、床、板凳、飞机、摩托等空间时，先检查位置、物理资源容量、形态转换、可触达范围、服装道具和移动过渡。
- 不要为了方便改写已确定设定。
- 如果上下文缺失，只做最小假设，并标注为假设。
- 长输出后，只有当我要求“更新账本”时，才输出 Ledger Update。
- 如果我输入“更新账本”，你只更新账本，不要继续正文。

接下来我会粘贴 Advanced Human Writing & AI Humanizer 生成的指令包。
```

## 现实边界

这个流程能显著减少上下文丢失，但不能让模型无限记忆。长篇小说、系列文章、科研报告、世界观设定集，都应该把 continuity ledger 当成唯一可信的连续性来源。

模型一旦忘了，不要和聊天记录纠缠。用最新账本重新生成指令包，然后继续。
