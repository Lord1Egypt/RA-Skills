# 多阶段审稿流水线

一次加载所有审查规则能扩大覆盖面，但不保证每一项都检查得更深。规则过多时，模型可能漏项、混用标准，或者把大量上下文花在重复说明上。

本项目同时保留三种方式：

| 方式 | 用途 |
| --- | --- |
| `build --review` | 正文生成时的精简编辑与 AI 痕迹提醒 |
| `build --deep-review` | 扩展版传统自审；新增高成本叙事模块仍需按需选择 |
| `pipeline` | 把同一稿件拆成多个互不干扰的独立审稿阶段 |

## 完整流水线

```powershell
human-writing-skills pipeline `
  --draft my-chapter.md `
  --context my-novel-ledger.md `
  --output-dir chapter-audit
```

默认生成：

1. `logic`：逻辑、时间线、知识来源、动机、规则、资源和后果
2. `character`：人物目标、声音、能力、边界、知识和变化桥梁
3. `relationship`：谁在谁面前提谁、阵营、等级、秘密和信息权限
4. `physical`：位置、容量、触达、服装、道具和伤势
5. `ai-trace`：套话、公式结构、段落无推进和其他 AI 痕迹
6. `numbers`：动作与情绪中的假精确数字
7. `proofread`：错别字、标点、称谓、排版和机械错误

为节约上下文，`voice`、`register`、`capability`、`serial`、`world`、`process`、`momentum`、`salience`、
`recurrence`、`texture`、`fidelity` 和 `sources` 不属于默认完整流水线。只有显式选择或使用
`--auto` 命中条件时才会生成。`preservation` 属于高成本原文对照，始终只接受显式选择。

输出目录里的每个 Markdown 都是一份完整但单一职责的提示词。应在新的 Chatbox 会话、独立 API 请求或没有上一阶段聊天记忆的模型会话中分别运行。

目录还会生成确定性预检 `00-pattern-lint.md` 和 JSON，包含命中位置和透明分数，
但不据此判断作者身份。

只有传入 `--with-stats` 才会额外生成 `00-style-stats.md` 和 JSON。统计默认关闭，
只作编辑诊断，不作作者身份判断。

## 动态按需加载

```powershell
human-writing-skills pipeline `
  --draft my-chapter.md `
  --context my-novel-ledger.md `
  --auto `
  --output-dir chapter-audit
```

自动模式始终保留：

- `logic`
- `ai-trace`
- `proofread`

然后根据本章内容决定是否追加：

- 有人物行为或声音线索：`character`
- 有对话、等级、阵营、亲密或秘密线索：`relationship`
- 有持续多轮对白和说话归属线索：`voice`；提供人物账本时，较短的归属明确对白也可触发
- 对白与明确语言、方言、敬语或语域证据同时存在：`register`
- 提供账本且出现战力、技能、权限、装备、伤势或资源约束：`capability`
- 已提供前章/账本且正文具有连载叙事线索：`serial`
- 有明确时代、世界规则、技术体系或架空设定：`world`
- 同时出现关键过程和结果线索，或多次出现过程线索：`process`
- 正文含两个以上章节标题或重复续篇标记：`momentum`
- 至少 4000 字符、12 个段落且属于叙事长稿：`salience`
- 至少三个章节标题：`recurrence`
- 有位置、移动、服装、道具或空间线索：`physical`
- 有电影式开场堆料、公式化内心解释、密集比喻、资料倾倒、连续短段或展示后再解释：`texture`
- 有带单位的精确数字：`numbers`
- 明确传入 `--reference` 或 `--reference-style`：`style-match`
- 明确传入改写前原文 `--original`：`fidelity`
- 显式选择并传入改写前原文：`preservation`；自动模式不会加入
- 严肃文体，或明确选择的事实类 self-media / argumentative，与一个以上 `--source` 同时存在：`sources`

`voice` 会对照人物稳定语言基线、当场目的、知识与角色约束、听众、回应衔接和
变调依据，并检查关键台词或动作是否得到语言、动作、可读沉默、明确打断或延迟
回应，不会把职业直接等同于口吻。`README.md` 清单会记录每个阶段为什么被
选择或跳过。自动判断是保守的文本启发式，不理解完整剧情；重要章节应显式指定阶段。

`register` 不根据国籍或地域凭空生成口音，只审查已经提供证据的共同语言、方言经历、
敬语称谓、语气词和变调依据。`capability` 区分永久基线与临时伤势、装备、资源、
冷却、克制和权限，并要求变化存在过程门与代价。

## 显式选择

```powershell
human-writing-skills pipeline `
  --draft my-chapter.md `
  --stage logic `
  --stage character `
  --stage relationship `
  --output-dir chapter-audit
```

`--auto` 和 `--stage` 不能同时使用。

显式选择 `--stage style-match` 时必须同时提供参考资料或明确文风方向。只有这个
阶段会收到参考原文，其他专项审查不会被范文内容干扰。

显式选择 `--stage serial` 时必须同时提供 `--context`，否则命令会拒绝运行，防止
模型凭空补造前情。

显式选择 `--stage capability` 同样必须提供 `--context`，否则没有可靠的既有战力、
技能、权限、伤势或资源状态可供前后比较。

显式选择 `--stage fidelity` 时必须同时提供 `--original`。只有这个阶段会收到改写
前原文，它检查语义是否保留，不把原文自动当作文风范本。

显式选择 `--stage preservation` 同样必须提供 `--original`。它对照有意义的含混、
重复、母题、迟疑、潜台词、人物口吻和未结压力，避免把所有毛边都误判成错误。

显式选择 `--stage sources` 时必须同时提供 `--source`，并将 `--document-type`
设为论文、新闻、法律或技术文档，或者让自动识别获得足够的严肃文体证据。来源
文件只进入 `sources` 阶段，不进入小说审稿和文风对齐阶段。

## 推荐执行顺序

先改结构，后改文字：

```text
确定性扫描 -> 可选统计 -> 逻辑 -> 人物/关系/声音/语域/能力/前情/世界/过程/推进 -> 注意力/跨章结构 -> 物理 -> AI 痕迹/文字质地 -> 文风对齐/语义保真 -> 数字 -> 来源 -> 校对
```

逻辑或剧情结构发生重写后，应重新运行受影响的后续阶段。不要先校对一段随后会被整体删除的文字。

## 边界

`pipeline` 负责生成分阶段提示词文件，不会主动调用 Chatbox 或任何模型，也不会自动合并模型输出。这样可以兼容 Chatbox、Codex、ChatGPT、Claude、本地模型和 API 工作流。
