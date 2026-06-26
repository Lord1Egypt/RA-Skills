# Before / After

## Why This Page Exists

这一页不是宣传稿。

它用来回答一个很实际的问题：

安装 `memory-governor` 之前和之后，系统到底发生了什么变化？

## Before

在没有治理内核时，常见状态通常是：

- 不同 skill 各自定义“什么值得记”
- 路径直接等于记忆模型
- optional skill 实际上变成 hidden dependency
- 同一种信息在不同地方重复出现
- 升级规则靠临场判断，没有统一口径
- fallback 只是口头存在，没有可复制模板

典型表现：

- 今天把经验写进 daily note
- 明天把类似经验写进某个 skill 自己的文件
- 后天又想把它搬进长期记忆
- 但没人能说清这三次为什么不一样

## After

安装 `memory-governor` 之后，变化不在“多了一个存储位置”，而在“多了一层统一解释”。

系统会先做这三步：

1. 判断 memory type
2. 路由到 target class
3. 由 adapter 决定具体路径，缺失时走 fallback

于是变化变成：

- skill 不再直接发明自己的全局记忆定义
- 路径从“内核本体”降级为“宿主适配结果”
- optional skill 变成 adapter，不再是前提
- fallback 成为显式、可打包、可复制的默认行为
- 升级规则可以跨 skill 复用
- host 可以保留自己的目录结构，而不必假装自己是 OpenClaw

## Side-by-Side

| 维度 | Before | After |
|---|---|---|
| 记忆定义 | 各 skill 各写各的 | 统一 memory contract |
| 路由逻辑 | 直接写死到路径 | 先 target class，再 adapter |
| optional skill | 隐性依赖 | 可选 adapter |
| fallback | 口头约定 | 包内模板 + 显式规则 |
| host 假设 | 默认照搬 OpenClaw | generic core + host profile |
| 升级规则 | 临场判断 | promotion rules |
| 分发性 | 只在作者机器上顺手 | 可以指导第三方接入 |

## Concrete Example

同样是一条信息：

`This retry pattern is reusable in future API tools.`

### Before

不同 skill 可能会有不同做法：

- 写进当天 daily note
- 写进某个项目文档
- 写进 `self-improving`
- 或者根本不写

### After

先判断：

- memory type: reusable lesson
- target class: `reusable_lessons`

再决定 adapter：

- 如果宿主装了对应改进型 skill，就映射到那个 skill 的路径
- 如果没装，就使用 packaged fallback template

所以“记不记、记到哪、为什么记到那”会有同一套解释。

## What Does Not Change

`memory-governor` 不会强迫这些事情一起变化：

- 你的目录结构
- 你的工具栈
- 你的外脑产品
- 每个 skill 的内部执行逻辑

它统一的是 contract，不是把一切改造成同一个框架。

## Practical Outcome

接入前，系统更像一组习惯。

接入后，系统更像一套制度：

- 有统一分类
- 有统一路由
- 有升级规则
- 有排除规则
- 有宿主适配
- 有缺省降级

这就是它的价值。
