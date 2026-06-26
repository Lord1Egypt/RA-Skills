# Installation & Integration

## 目标

说明安装 `memory-governor` 之后，包外哪些文件可以改，为什么改，不改会少什么能力。

这是一个治理内核，不是自动接管系统的总线。

阅读顺序建议：

1. generic core
2. host profile
3. optional package-external integration

所以安装分两层：

- **安装 skill 本体**
- **选择是否做包外集成**

## Readiness Model

推荐把 `memory-governor` 的状态理解成三层：

### 1. Installed

表示：

- skill 本体已经安装
- 规则、reference、snippet、scripts 可用

这个状态下：

- 可以开始用统一规则思考记忆治理
- 但宿主还不一定已经接上这套规则

### 2. Integrated

表示宿主已经完成包外接入，例如：

- 主入口已承认 `memory-governor`
- 相关 skill 已补 `Memory Contract`
- 宿主已声明 `memory-governor-host.toml`
- 如果希望 machine-checkable，还应在 manifest 里声明 host entry 和 writer contract 路径

这个状态下：

- 宿主行为才开始完整服从 `memory-governor`

### 3. Validated

表示：

- 已运行 `scripts/check-memory-host.py`
- 当前宿主通过检查

这个状态下：

- 不只是“自认为接好了”
- 而是已经被工具确认当前接线是完整的

一句话：

- `Installed` = 内核已带入
- `Integrated` = 宿主已接线
- `Validated` = 接线已确认

## 默认不会自动改包外文件

安装 `memory-governor` 本体时，默认 **不会** 自动修改这些文件：

- 宿主的 `AGENTS.md`
- 其他 skill 的 `SKILL.md`
- 现有 `MEMORY.md`
- 现有 daily note

原因：

- 这些都属于宿主自己的系统边界
- 不同宿主的总入口文件名和目录结构可能不同
- 自动补 `Memory Contract` 容易误判 skill 的真实职责

所以当前默认模型是：

- 安装 skill 本体
- 给出 snippet、manifest、checker 和说明
- 由宿主或安装者显式决定是否做包外集成

如果未来做自动化，也应该是 **显式触发的 guided integration**，而不是安装副作用。

如果宿主想在尚未安装或尚未完整接入时对用户做提醒，建议看：

- `openclaw-adoption-prompts.md`

## 装完后默认获得什么

即使不改任何包外文件，安装后也已经获得：

- 一套统一的记忆治理规则
- target classes 定义
- adapter / fallback 模型
- 路由、升级、排除规则

如果宿主后续启用 Dreaming，还应额外遵守：

- Dreaming 是 optional consolidation engine
- `DREAMS.md` / `memory/.dreams/` 不是新的 target class
- 不应让 Dreaming 和人工 daily promotion 同时成为默认 authority

如果宿主后续启用 Active Memory 或 Memory Wiki，还应额外遵守：

- Active Memory 是 runtime recall 层，不是新的 target class
- Memory Wiki 是 compiled knowledge / wiki surface，不是 canonical durable memory
- 不应把 wiki vault 结构反向提升成治理层 target classes
- 不应因为 runtime recall 变强，就跳过 `learning_candidates` 的显式纠错分层

这意味着：

- 你可以用它来判断“什么该记”
- 你可以用它来设计自己的 memory contract
- 你不必立刻改整个工作区

但这只意味着你达到了 `Installed`，不意味着已经 `Integrated`。

## Python Compatibility

当前脚本默认兼容：

- Python 3.11+：使用标准库 `tomllib`
- Python 3.9 / 3.10：需要额外安装 `tomli`

涉及的脚本主要包括：

- `scripts/check-memory-host.py`
- `scripts/validate-memory-frontmatter.py`

## 包外集成点

以下文件属于“可选集成点”。

### 1. 工作区总入口

这一步是 **host-specific** 的，不是 generic core 的前提。

推荐文件：

- `AGENTS.md`

作用：

- 让主入口正式承认 `memory-governor`
- 告诉主 agent，记忆先路由到 target classes，再由 adapter 落地

不改会怎样：

- skill 仍可用
- 但工作区主入口不会自动承认这套规则

### 2. 会写记忆的其他 skill

推荐文件：

- 其他相关 `SKILL.md`

作用：

- 为每个 skill 补 `Memory Contract`
- 让它们不再各自发明全局记忆定义

不改会怎样：

- `memory-governor` 仍可单独使用
- 但其他 skill 可能继续沿用自己的旧口径

### 3. fallback 文件

generic package 自带 fallback 模板：

- `assets/fallbacks/proactive-state.md`
- `assets/fallbacks/reusable-lessons.md`
- `assets/fallbacks/working-buffer.md`

如果宿主希望有本地副本，再映射到自己的路径。  
例如 OpenClaw reference profile 常见位置是：

- `workspace/memory/proactive-state.md`
- `workspace/memory/reusable-lessons.md`
- `workspace/memory/working-buffer.md`

作用：

- optional skill 没装时，内核仍有本地落点

不改会怎样：

- 仍可安装 skill
- 但某些 target classes 会缺少默认本地落点

### 4. OpenClaw runtime memory features

如果宿主是 OpenClaw，并且已经启用：

- Dreaming
- Active Memory
- Memory Wiki
- session pruning / automatic memory flush

推荐补一层运行时说明，哪怕只是 host note：

- Dreaming 负责 `daily_memory -> long_term_memory`
- Active Memory 负责 runtime recall
- Memory Wiki 负责编译后的 wiki / provenance / search surface
- `memory-governor` 继续负责 capture rules、candidate staging、manual hardening boundaries

不补会怎样：

- 宿主仍可运行
- 但后续很容易把 runtime surface 当成治理层，把编译层当成 canonical truth

## 哪些不建议直接改

默认不建议因为安装本 skill 而直接改：

- `MEMORY.md`
- 现有 daily note 内容
- 项目正文档内容

原因：

- 这些文件属于数据层，不是安装层
- 安装 skill 不应强迫迁移已有记忆内容

## 最小接入方案

适合先试用的人。

只做这些：

1. 安装 `memory-governor`
2. 阅读 `SKILL.md`
3. 在主工作区 `AGENTS.md` 加一段简短声明

结果：

- 有统一规则
- 不大动现有系统
- 可以逐步接 skill

完成这一步后，通常仍是 `Installed` 向 `Integrated` 过渡中的状态。

## OpenClaw Optimization Notes

对于新版 OpenClaw，建议宿主额外做三件事：

1. 保持 `working_buffer` 和当前任务 `proactive_state` 极短、可恢复、可替换

原因：

- session pruning 和 automatic memory flush 会放大短小高信号状态的价值

2. 在 host note 或 writer-skill contract 里明确：

- one-off explicit corrections -> `learning_candidates`
- proven reusable guidance -> `reusable_lessons`
- wiki compilation inputs should prefer proven layers over candidate layers

原因：

- 避免候选层过早被编译、检索、传播

如果使用 OpenClaw reference profile，`learning_candidates` 应显式落到：

- `~/self-improving/candidates.md`，如果该 adapter 存在
- 否则使用本地 fallback，例如 `memory/learning-candidates.md`

3. 明确 runtime query strategy：

- 普通任务恢复先靠 Active Memory + minimal read order
- 需要实体关系、证据链、共享知识导航时再用 Memory Wiki

原因：

- 避免每次任务都把所有 memory surfaces 当成同级入口

这一步仍然默认是手动或显式触发的，不是安装时自动执行。

如果你想从空白宿主快速起一个最小骨架，可先看：

- `bootstrap.md`

如果你是从已有散乱宿主收敛，而不是从空白宿主开始，可先看：

- `migration-guide.md`

## 完整接入方案

适合准备把它作为正式内核的人。

做这些：

1. 安装 `memory-governor`
2. 在 `AGENTS.md` 加 `Memory Governance` 段落
3. 为会写记忆的 skill 补 `Memory Contract`
4. 准备 fallback 文件
5. 在宿主根目录加 `memory-governor-host.toml`
6. 检查 optional skill 是否需要 adapter 说明
7. 选择并记录当前 host profile
8. 如果想让 checker 也验证接线面，在 manifest 里补 `[integration]`

如果你想先看一个不依赖 OpenClaw 的完整样例，可直接参考：

- `../examples/generic-host/README.md`

完成这一步后，才更适合称为 `Integrated`。

## OpenClaw 安装说明

如果宿主本身是 OpenClaw：

- 安装后，agent **会知道** 应该如何按 `memory-governor` 的规则来理解记忆治理
- 但这不等于安装过程会自动去改 `AGENTS.md` 或批量改别的 skill

当前更合理的做法是：

- OpenClaw 读取 `memory-governor` 的规则
- 需要时由人或显式任务触发包外集成
- 用 snippet、manifest、checker 来完成接线

也就是说：

- **安装** 负责把规则带进来
- **集成** 负责把宿主接上去
- **校验** 负责确认当前接线状态

这两步默认不应混成一个隐式副作用。

## 降级运行

如果你什么包外文件都不想改：

- 仍然可以把 `memory-governor` 当成规则参考来使用
- 只是不会自动影响你现有系统的默认行为

这属于合法用法，不是安装失败。

## 推荐复制模板

可直接复制这些片段：

- [AGENTS-memory-governance.md](../assets/snippets/AGENTS-memory-governance.md)
- [SKILL-memory-contract.md](../assets/snippets/SKILL-memory-contract.md)
- [ADAPTERS-fallback-note.md](../assets/snippets/ADAPTERS-fallback-note.md)

如果你想要更强的结构化约束，再看：

- `adapter-manifest.md`
- `schema-conventions.md`
- `../scripts/validate-memory-frontmatter.py`
- `host-checker.md`
- `../scripts/check-memory-host.py`

## Host Profile Reminder

如果你在 OpenClaw 环境中使用，按 OpenClaw reference profile 集成。

如果你不在 OpenClaw 环境中，不要机械复制 `AGENTS.md` 或 `workspace/memory/` 这类路径。  
先看 [host-profiles.md](host-profiles.md) 再决定怎么接。

## 安装者应回答的三个问题

安装后，至少想清楚这三件事：

1. 你要不要让主入口承认这套治理规则？
2. 你有哪些 skill 会“写点东西”，需要补 `Memory Contract`？
3. 如果 optional skill 没装，你准备接受默认 fallback，还是自己定义 adapter？

## 推荐的声明式接入

如果你不是直接照着 reference profile 落地，推荐在宿主根目录再加一份：

- `memory-governor-host.toml`

它的作用是：

- 给 checker 一个 machine-readable adapter map
- 显式声明 custom host 的 target class 落点
- 避免长期依赖“目录猜测”

格式说明见：

- `adapter-manifest.md`

## 如何确认“已经接好”

推荐把下面这份最小检查表当成 readiness checklist：

- skill 已安装
- 宿主已声明或确认 target class adapter map
- 主入口已承认 `memory-governor`
- 相关 skill 已补 `Memory Contract`
- `scripts/check-memory-host.py` 返回 `PASS` 或可接受的 `WARN`

只有满足前几项时，才应称为 `Integrated`。  
只有 checker 跑过时，才应称为 `Validated`。

## 如果以后要做自动化

推荐只做两种模式：

1. `manual integration`
   只提供说明、snippet、manifest、checker
2. `guided integration`
   由用户显式触发，再去补 `AGENTS.md` 或建议哪些 skill 应该加 `Memory Contract`

不推荐：

- 安装时静默修改包外文件
- 安装时批量改所有 skill
- 安装时假设宿主一定存在 `AGENTS.md`

如果要做安装前或接入前提示，也应遵循：

- 条件触发
- 低频
- 可拒绝
- 按当前会话语言本地化
