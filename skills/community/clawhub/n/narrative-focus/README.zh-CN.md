# Narrative Focus

[English](README.md) | **[中文](README.zh-CN.md)**

> 叙述重心错位是技术文章中最隐蔽的结构性问题。它不是"写得不好"，而是"写得重心不对"——响亮但表层的实现细节抢了真正决定行为的架构性机制的风头。读者的心智模型被锚定在错误的位置，后续学习不断回流重构。

一个用于检测和修正技术教程、面试准备文章中**叙述重心错位**的 AgentSkill。兼容 OpenClaw、CodeBuddy 及其他 AI coding agent。

## 这个 Skill 在解决什么问题

技术教程有一个普遍但几乎无人系统性解决的问题：**概念的叙述权重与实际重要性不匹配。**

一篇讲 React 事件系统的文章，把"事件委托"作为"三大核心机制"之一给了整整一章——但事件委托只是信号传递的管道，真正决定行为的是 Fiber 树遍历，后者被压缩成了流程图里的几行字。读者读完后记住了"事件委托"，然后在生产环境调试 `stopPropagation()` 时一头雾水。

这不是个例。我们用 8 篇跨领域文章（Kubernetes、PostgreSQL、Transformer、Rust、TLS、MySQL、Linux CFS、Git）做了实验，**篇篇存在叙述重心错位**，错位率 75.8%。问题的普遍性毋庸置疑。

## 核心理念：叙事重心是前置条件

大多数技术文章的问题不是内容不够，而是重心混乱。

一篇重心混乱的文章，读者看完后能复述概念，但无法建立因果理解。他们的时间花在了理解"为什么这个概念被单独成节"这种结构性困惑上，而不是去追问真正有意义的深度问题。

反过来，**在叙事重心正确的情况下，才能更高效地引发读者正向的疑问链和学习链。** 读者会沿着正确的因果链自然产生下一个问题——这些问题可以由其他文章、文档、实践来填补，也可以由用户向 agent 提出具体要求补充，而不是要求一篇文章穷尽所有内容。

**更快地将读者引导到知识的主战场，而不是被设计不够好的门槛绊倒，这是技术写作中比内容完备性更优先的设计目标。**

叙事重心是内容质量的前置条件。先校准重心，再谈深度。

## 怎么判断：替换实验

对任何技术细节提问：**如果这个细节传达的命题被替换为另一种实现，用户的可观测行为会改变吗？**

- **会变** → 架构性（Architectural）→ 决定系统行为的机制 → 值得高叙述权重
- **不会变，只是传递方式变了** → 传输性（Transport）→ 信号传递管道 → 低叙述权重
- **行为不变，只是配置不同** → 可配置性（Configurable）→ 现有机制上的开关/选项 → 中等叙述权重

**关键细节：先识别命题，再做替换。** 同一个技术细节在不同上下文中传达的命题不同。你必须先搞清楚这个细节在文章中实际在说什么，然后替换那个命题——不是替换字面的术语或实现。

例如"JSX 是 `React.createElement()` 的语法糖"——如果文章实际在断言"JSX 没有独立的运行时语义"，替换它会根本改变读者对 React 的理解 → Architectural。但如果文章只是在说"JSX 编译成 `createElement` 这个具体函数"，换成 `jsx()` 不影响读者行为 → Transport。正确判断取决于文章实际在主张什么。

**命题粒度。** 同一个细节可以在不同粒度上解读——例如"位置编码提供位置信息"（概念层面）vs "正弦/余弦公式实现位置编码"（数学层面）。正确的粒度取决于文章实际展开到什么程度。详见 `references/proposition-granularity-guide.md` 的判定流程图和示例。

## 适用范围

| 适用 | 不适用 |
|------|--------|
| 技术教程、深度解析 | API 参考文档 |
| 面试准备文章 | 观点文、新闻/changelog |
| 框架对比文章 | 非技术内容 |

这个 Skill 回答一个问题：**"每个概念的叙述权重是否与其实际角色匹配？"** 它不检查内容缺失、主题边界或体裁一致性。

### 两种工作模式

| 模式 | 场景 | 目的 |
|------|------|------|
| **前处理** | 研究/收集阶段 | 给收集到的技术细节打角色标签，防止后续写作时重心错位 |
| **后处理** | 文章初稿完成后 | 检测已有文章的重心错位并精准修正 |

### 后处理安全步骤

后处理在修正之后包含两个安全步骤：

1. **二次检测** — 修正后重新执行检测流程，确认所有错位已解决
2. **权威性校验** — 对照权威来源（官方文档、团队博客、MDN）检查修正后的段落，确保重心迁移没有引入技术语义错误。只对**技术事实**做权威校验；**叙事框架**不做校验（官方文档服务于不同目的，不能作为心智模型导向文章的叙事标准）

## 安装

### OpenClaw / CodeBuddy（原生 AgentSkill）

本 Skill 使用 AgentSkill 兼容的 `SKILL.md` 格式，原生支持 OpenClaw 和 CodeBuddy：

**OpenClaw** — 通过 ClawHub 安装或手动复制到 skills 目录：
```bash
# 通过 ClawHub（推荐）
openclaw skill install narrative-focus

# 或手动复制
cp -r narrative-focus/ ~/.openclaw/skills/
```

**CodeBuddy** — 复制到 skills 目录：
```bash
cp -r narrative-focus/ ~/.codebuddy/skills/
```

### 其他 AI Coding Agent（Claude Code、Cursor、Windsurf 等）

加载 `SKILL.md` 作为上下文，然后根据需要加载对应的参考文件（`references/pre-processing.md` 或 `references/post-processing.md`）。替换实验和角色标签定义在 SKILL.md 中；详细 SOP 在参考文件中。

以 Claude Code 为例：
```
# 添加到 CLAUDE.md 或直接指令：
Read narrative-focus/SKILL.md and follow its workflow for post-processing detection on this article.
```

## 使用方式

### 前处理（收集阶段）

告诉你的 agent：
- "按叙述重心规范收集"
- "角色标注"
- "Label these technical details by role using the substitution test"

Agent 会识别每个细节传达的命题，执行替换实验，并标记为架构性 / 传输性 / 可配置性。

### 后处理（审稿阶段）

告诉你的 agent：
- "检测叙述重心错位"
- "审稿重心"
- "Check this article for narrative weight misalignment"

Agent 会扫描文章，识别错位，执行修正——提升架构性概念的权重，降低传输性/可配置性概念的权重——然后对照权威来源验证修正后的段落，确保没有引入技术事实错误。

## 示例

| 示例 | 展示内容 |
|------|----------|
| [`react-event-system/`](examples/react-event-system/) | 经典错位：事件委托过度突出，Fiber 遍历被压缩。完整 Step 1–5 检测 + 修正 + 二次检测。含**命题粒度分析**。 |
| [`docker-orchestration/`](examples/docker-orchestration/) | 标题-内容不匹配：构建细节挤占了编排内容。多项传输性/可配置性条目被过度突出。 |
| [`v8-gc/`](examples/v8-gc/) | **边界案例**：大部分权重正确，2 项处于灰色地带。展示 Skill 如何处理"差不多对"的文章及其自身范围边界。 |

## 文件结构

```
narrative-focus/
├── SKILL.md                              # 核心概念 + 模式路由
├── README.md                             # English
├── README.zh-CN.md                       # 中文版
├── LICENSE
├── references/
│   ├── pre-processing.md                 # 前处理 SOP：收集与标注阶段
│   ├── post-processing.md                # 后处理 SOP：检测、修正与校验
│   └── proposition-granularity-guide.md  # 如何以正确深度解读命题
├── examples/
│   ├── react-event-system/               # 经典错位 + 粒度分析
│   │   ├── before.md
│   │   └── after.md
│   ├── docker-orchestration/             # 标题-内容不匹配
│   │   ├── before.md
│   │   └── after.md
│   └── v8-gc/                            # 边界案例 + 范围边界
│       └── before.md
└── experiments/                           # 三轮验证实验
    ├── README.md                          #   实验概览
    ├── final-evaluation.md                #   最终综合评价
    ├── round1-cross-domain/               #   R1：5 篇合成文章，跨领域鲁棒性
    │   ├── articles/                      #     K8s、PostgreSQL、Transformer、Rust、TLS
    │   ├── detection-results/             #     Skill 检测报告（5 份）
    │   └── summary.md
    ├── round2-controlled/                 #   R2：3 篇真实文章，Skill vs 无 Skill 对照组
    │   ├── articles/                      #     MySQL、Linux CFS、Git
    │   ├── no-skill-control-results/      #     无 Skill 对照组（同一模型，不加载 Skill）（3 份）
    │   ├── skill-detection-results/       #     Skill 组（同一模型 + Skill 输入）（3 份）
    │   └── summary.md
    └── round3-correction/                 #   R3：修正流程效果验证
        ├── corrected-articles/            #     修正后文章（2 份）
        ├── correction-reports/            #     修正 + 校验报告（2 份）
        ├── re-evaluation/                 #     无 Skill 对照组重评估（2 份）
        └── summary.md
```

## License

MIT
