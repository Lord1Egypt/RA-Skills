---
name: linkfox-skill-evaluator
description: Evaluate whether a skill is both safe to run and effective at its job. Use when the user wants to test, benchmark, grade, critique, audit, vet, or compare versions of a skill — phrases like "这个 skill 好不好"、"evaluate this skill"、"vet this skill"、"新版本比旧版本好吗"、"帮我测测这个 skill"、"这个 skill 安全吗"、"skill 有没有效果"、"skill 质量如何". Trigger whenever a user has a skill in hand and wants an objective read — on effectiveness, on safety, or both; the evaluation always covers both dimensions regardless of which the user asks about first. Works on any skill regardless of domain (writing, code generation, data extraction, workflows, domain-specialized skills, third-party community skills).
---

# Skill Evaluator

评估一个 skill 的逻辑用 **IPO** 组织：输入是一个待评估的 skill，过程是"分类 + 静态安全扫描 → 选问题 → 起草测试和断言 → 跑测试 → 打分 → 双通道红旗审查 → 综合"，输出是一份**同时带安全判定和质量决策**的报告。

在进入 IPO 之前，建立两个核心认知：

**认知 1：安全和质量始终并行评估。** 一个 skill 即便效果再好，只要它偷偷读 `~/.ssh` 或往外发数据，就不能用——所以安全检查是每次评估的底线，不是"可选项"。反过来，一个 skill 即便再安全，产出不达标也没价值。两个维度同时跑，不让用户做取舍。

**认知 2："skill 效果好不好"不是一个问题，是四个不同的问题。** 选错问题得到的答案毫无意义。最常见的错误是拿一个专门 skill 去跑 "with-skill vs no-skill" 对比——没有 skill 时 agent 根本不懂这个领域，所以永远是 with-skill 赢。这种对比只能证明 skill "做了事"，证明不了它"做得好"。

## 四个质量评估问题（先认清你要答哪个）

| 问题 | 含义 | 方法 | 需要 baseline |
|------|------|------|-------------|
| **A. 输出达标吗** | 产出是否正确 / 完整 / 可用 | 对着规格写绝对断言 | ❌ |
| **B. 面对真实输入变化稳定吗** | prompt 换花样时质量会不会塌 | 多 prompt 扇出，观察塌陷 | ❌ |
| **C. 新版本比旧版本好吗** | 我的修改到底是改进还是回归 | 新版本 vs 旧版本对照 | ✅ baseline = 旧版本 |
| **D. skill 该不该存在** | 不用这个 skill，agent 是不是也能做得差不多 | with-skill vs no-skill | ⚠️ 仅当 agent 本来就能大致完成时才有意义 |

选问题的依据是 skill 类型（Process 的 Step 1 会讲）。

## 安全红旗分级（静态扫描 + 行为观察都用这张表）

| 级别 | 症状 | 处置 |
|------|------|------|
| ⛔ **EXTREME** | 读 `~/.ssh`、`~/.aws`、`~/.config`；访问 agent 持久记忆或身份配置文件（各框架的 memory / identity / system prompt 存储）；读浏览器 cookie / session；请求 sudo；修改工作目录外系统文件；明显混淆代码（base64 编码、压缩） | **立刻停止评估**，报 DO NOT INSTALL |
| 🔴 **HIGH** | 向未知 URL 发 `curl`/`wget`；向外部服务器发送用户数据；请求凭据 / token / API key；对外部输入用 `eval()` / `exec()`；用 IP 而非域名做网络调用；静默安装未列明的包 | **human approval required**，评估暂停，等用户拍板 |
| 🟡 **MEDIUM** | 读写工作目录外文件但有合理用途；调用明确的公开 API；需要文件系统权限；执行本地命令 | 继续评估，在报告中标注范围 |
| 🟢 **LOW** | 纯文本处理 / 格式化 / 知识型输出；无网络无文件访问；所有操作限定在输入上下文内 | 正常跑完评估 |

这张表在 Step 1（静态扫描）和 Step 6（transcript 行为审查）都会用到。

---

# INPUT

评估需要以下输入。能从用户对话拿到的就拿，拿不到的主动问。

## 必需输入

1. **待评估的 skill 本体**
   - skill 路径，或直接粘贴的 SKILL.md 内容 + 相关脚本 / 资源文件
   - 读出 `name`、`description`、`body`，并扫所有被 skill 引用的脚本
   - 这是**所有后续判断（安全 + 质量）的基础**

## 建议输入（如果用户能提供就要，不能就代为起草）

2. **真实 prompt 样例**
   - 真实用户会说的话（带上下文、typo、口语、不完整信息都没关系）
   - 如果用户给不出，Process 会起草再让用户确认
3. **skill 来源信息**
   - 自研 / GitHub / 社区市场 / 厂商交付——决定静态扫描的严格程度（社区来源 = 最大怀疑）
   - 如果是 GitHub：仓库 URL，能拉 star / 更新频率 / issues 做可信度参考

## 可选输入

4. **部署环境 / 敏感资产清单**
   - skill 将要跑在什么环境下、能访问哪些敏感数据（例如"这台机器有生产 AWS 凭据"、"skill 会在 CI 里跑"）
   - 给了就写进报告的"范围声明"；没给就按通用工作站默认假设
5. **被评估 skill 的旧版本**（仅跑 Question C 时需要）
   - 修改前的 SKILL.md 副本，或可从 git 取出的历史版本
6. **输出规格文档 / 用户关心的 edge case**
   - 有规格让断言写得更准；edge case 可直接塞进 Question B 的 prompt 变体

## 输入不足时的处理

- 没有 prompt → 基于 skill description 起草 2-3 个，给用户过目后用
- 没有来源信息 → 按"未知来源"最高严格度扫
- 没有旧版本 → 降级到只跑 A+B 的质量问题，告诉用户 C 问题答不了
- skill 描述模糊到无法判断类型 → 停下来问清楚，不要硬跑
- 测试验证中缺失配置 → 停下来询问用户，不要硬跑
- skill 依赖外部 API 凭据（Keepa / Helium10 / 平台 API 等）→ 要求用户提供凭据或显式确认跳过；跳过时降级到静态扫描 + 逻辑评估，不编造 API 输出

---

# PROCESS

8 步执行，按顺序。Step 0 是自动化预检（结构 + 卫生）。安全扫描（Step 1 静态 + Step 6 行为）和质量评估（Step 2-5）并行进行，最后在 Step 7 合流。任何一步遇到 ⛔ EXTREME 红旗直接中止流程，出报告告诉用户 "DO NOT INSTALL"。

## Step 0 — 自动化结构预检

跑 `scripts/pre-check.py`，快速排除结构性问题。这一步不替代安全红旗分级——只做"能不能进入评估"的门槛检查。

```bash
python3 scripts/pre-check.py /path/to/skill          # 人读报告
python3 scripts/pre-check.py /path/to/skill --json   # 程序消费
```

检查覆盖 5 类 13 项：
- **结构**：SKILL.md 存在、frontmatter 合法（含 name + description）、name 与目录名一致、无多余文件（README/LICENSE 等）、资源目录非空
- **触发**：description 长度合理（15-200 词）、含触发上下文短语（"Use when..." / "当用户..."）
- **文档**：body 长度合理（10-500 行）、references/ 内文件在 SKILL.md 中被引用
- **脚本**：Python 语法通过 AST 解析、Shell 脚本有 shebang 且无裸 eval
- **安全卫生**：无硬编码凭据/邮箱、环境变量在 SKILL.md 有文档

### 预检结果处理

| 结果 | 含义 | 处置 |
|------|------|------|
| **BLOCKED** | 有 FAIL 项 | 退回给 skill 作者修结构问题，不进入评估 |
| **CAUTION** | >2 条 WARN | 可以进入评估，但把 WARN 项带入 Step 1 一并观察 |
| **CLEAR** | 结构合格 | 直接进 Step 1 |

预检通过 ≠ 安全。预检只看"文件结构对不对"，Step 1 才看"内容有没有危险"。

## Step 1 — 分类 skill + 静态安全扫描（一次读文件完成两件事）

读 skill 的 description、body、引用的所有脚本和资源。**同一次阅读里同时做两件事：**

### 1a. 判断 skill 类型（决定跑哪些质量问题 + 是否加载扩展）

| 类型 | 特征 | 默认跑的质量问题 | 加载扩展审查 |
|------|------|------------|------------|
| **垂直领域 skill — 知识点型** | 含特定平台 / 行业知识，一次输入 → 一次输出，无中间状态（写 listing、分析评论、解读政策） | A + B，迭代时加 C | ✅ `references/vertical.md` |
| **垂直领域 skill — 流程型** | 多步编排 + 步骤间有数据传递 + 含至少一个用户决策点（选品全流程、竞品调研工作流、广告诊断流程） | A + B，迭代时加 C | ✅ `references/vertical.md` + `references/process-flow.md` |
| **通用 skill** | 帮 agent 把本来就能做的事做更好（格式化、代码评审风格、通用总结等） | A + D | ❌ 不加载 |

**流程型的判定标准**：同时满足以下三条即为流程型——(1) 有 2 个以上有序步骤；(2) 步骤间存在数据传递（上游产出是下游输入）；(3) 至少一处用户必须做决策的暂停点。缺任一条按知识点型处理。

主观向（创意 / 风格 / 文案）不单列为一类——按垂直或通用划进对应桶，评估时用"盲评替代断言"即可。

### 1b. 静态安全扫描（对照上面"安全红旗分级"表）

过一遍 SKILL.md 和所有引用文件，找：
- **网络调用**：有没有 `curl` / `wget` / `http_get` / `fetch` / `requests.get`？指向哪里？是不是已知公开 API？
- **凭据 / 敏感路径触碰**：有没有 grep 过 `~/.ssh`、`~/.aws`、`.env`、agent 记忆文件或身份配置？
- **命令执行**：有没有 `eval`、`exec`、`subprocess` 拼接外部输入？
- **混淆 / 编码**：有没有长 base64 字符串、压缩 JS、看不出意图的代码块？
- **包安装**：有没有偷偷 `pip install` / `npm install` 没在顶部列出的包？

扫描结束**立刻分级**：
- 命中 ⛔ → 停，出"DO NOT INSTALL"报告，Process 不往下走
- 命中 🔴 → 暂停，告诉用户"这个 skill 需要人工审批才能继续评估，发现以下高风险模式：…"，让用户拍板
- 命中 🟡 → 继续评估，把观察写进报告的"权限范围"段
- 全是 🟢 → 继续

### 1c. 三轴上下文影响预估（响应轴 + 入参轴）

skill 对 agent 上下文的影响分三轴：**加载轴**（skill 文本本身）、**入参轴**（agent 传给 skill 的参数）、**响应轴**（skill 返回给 agent 的内容）。本步骤在 Step 1 静态预估**入参轴和响应轴**的风险档位（加载轴本身是静态指标，无运行时观测环节，暂不在本流程内）。

**统一 5 档风险表**（入参轴和响应轴共用，详见 `references/red-flag-details.md`）：

| 算出的上限值 | 档位 |
|---|---|
| < 2k token | 极低 |
| 2k–5k token | 低 |
| 5k–30k token | 中 |
| 30k–200k token | 高 |
| > 200k token | 极高 |

"算不出上限" → 不是极低，归到 **中档** 强制实测。

**响应轴**两步判定：
1. 能不能算出输出上限？依据：skill body 显式声明输出格式 / API 响应 schema 已知带条数字段上限 / 脚本输出走固定模板。
2. 算出上限值套 5 档表。

**入参轴**双层判定（取较差层定档）：
- 层 A：接口设计——参数是引用语义（文件路径/ID/URL）+ 有长度上限 → 健康；自由文本/完整原始数据/无上限 → 升档
- 层 B：指引质量——SKILL.md 显式说"传文件路径"→ 健康；"贴进来"/"完整粘贴"→ 升档

升档反面信号、推荐解法、详细判定流程见 `references/red-flag-details.md` 的 "Context bloat：三轴上下文影响评估" 段。

**两轴档位决定后续流程**：
- 极低档 → Step 6 该轴跳过实测
- 非极低档 → Step 3 起草测试用例时**必须**包含该轴的极限用例；Step 6 reviewer 必须实测该轴体积

把分类 + 扫描结论 + 双轴档位一句话告诉用户，让他纠偏。例：*"这是个垂直领域 skill（amazon listing），静态扫描无高危；响应轴预估高档（调 Keepa 拉价格历史可能 30k+ token），入参轴极低档（只接 ASIN）。跑 A+B 问题，Step 3 会针对响应轴起草极限用例，Step 6 加载垂直扩展审查。"*

## Step 2 — 选定评估问题

基于 Step 1a 的分类 + 用户意图，锁定跑哪几个质量问题。

**关键原则**：垂直领域 skill **不要跑 Question D**，对这类 skill 它是恒等式不是评估。

## Step 3 — 起草测试 prompts + 事前断言（合并）

**断言必须在跑任何测试之前完成。** 跑完再写 = 合理化现有输出，不是评估。

### 3a. 起草 2-3 个真实 prompt

prompts 要满足：
- **真实**：用户真的会这么说（带上下文、模糊、casual）
- **覆盖多样**：一个典型、一个边界、一个多步（如果 skill 场景允许）
- **可被断言**：目标具体到可以打 pass/fail

反例：`"写一个产品 listing"`
正例：`"帮我给这个蓝牙耳机写亚马逊 listing，竞品 ASIN B0CXXX，主打降噪和 40 小时续航，目标市场美国"`

如果 Step 1b 命中 🟡，至少加一个 prompt 专门探测那个敏感边界（例如"让 skill 处理一个它需要访问 Keepa 以外数据的请求，看它会不会越界"）。

**Step 1c 非极低档强制极限用例**：

- 响应轴非极低档 → 必须含 1 个**响应极限用例**：让 skill 在合理使用范围内产出最大可能输出（选 skill 声称支持的最大输入规模、最广覆盖查询、最深分析层级）
- 入参轴非极低档 → 必须含 1 个**入参极限用例**：让 agent 在合理使用范围内最大化入参体积（把上游数据规模拉到 skill 声称支持的上限）
- 两轴均非极低且场景重合（输入大→输出也大）→ 一个用例可同时覆盖两轴；否则需各设计一个

设计要点：极限是"贴近上限的真实场景"，不是 fuzzing。如果 skill 没声明上限，按"用户合理可能传入的极端值"来定。详见 `references/red-flag-details.md` 的"极限测试用例设计原则"段。

### 3b. 对每个 prompt 写 3-6 条断言

断言要求：
- **客观**：人能毫无歧义给出 yes/no
- **命名清晰**：扫一眼就知道在查什么
- **绑定 skill 承诺**：测的是这个 skill 声称能做的事
- **含至少一条负向断言**：skill *不应该*做什么也要写出来（例："未读取 `~/.aws/credentials`"、"无占位符 [TODO]"）

好断言：
- "输出含 5 个必需章节（Title / Bullets / Description / Keywords / A+）"
- "Bullets 恰好 5 条，Title ≤200 字符"
- "用户提到的 3 个卖点全部出现在输出里"
- "**输出语义命中用户原始意图**（不是 skill 作者脑补的意图——需求契合度）"
- "未发起任何超出 Keepa API 以外的网络调用"（负向 / 安全向）

> **需求契合度是必考一条**。不管 skill 类型，每个 prompt 的断言里都要放一条"输出确实解答了用户真正在问的问题"，防止 skill 在"符合规格"但"偏离意图"之间裸奔。语义匹配题盲评 / 让用户一句话确认都行，不必硬凑成自动化。

坏断言："写得有说服力"（主观）、"质量好"（不可测）、"用户会喜欢"（那是调研不是评估）

### 3c. Agent 适配性断言（至少选 2 条）

skill 不只是给人用的，它首先是给 agent 用的工具。以下 6 个维度从中至少选 2 条写进断言：

| 维度 | 测什么 | 断言示例 |
|------|--------|----------|
| **触发精度** | description 是否让 agent 在该触发时触发、不该触发时沉默 | "给一个领域内 prompt，skill 被激活"+"给一个邻近但不在范围内的 prompt，skill 不被激活" |
| **渐进披露** | 是否分层加载（description → body → references），而非一次全塞 | "agent 完成任务时未读取 references/ 中非必需的文件" |
| **可组合性** | 输出是否可被下游消费（结构化、可 parse） | "输出含可被其他工具消费的结构化段落（JSON / markdown table / 明确分隔符）" |
| **幂等性** | 同 prompt 重跑是否安全、结果一致 | "同一 prompt 跑两次，核心结论一致，无副作用累积" |
| **逃生出口** | 用户/agent 能否覆盖 skill 默认行为 | "当用户显式要求跳过某步骤时，skill 不强制执行该步骤" |
| **计算分离** | 确定性环节是否用脚本而非 LLM 推理 | "数据获取/格式转换/数值计算等确定性步骤由脚本完成，LLM 仅处理需要语义理解的环节" |

选哪 2 条看 skill 类型：
- 含脚本的 skill → 优先选"可组合性"+"幂等性"
- 纯指令 skill → 优先选"触发精度"+"渐进披露"
- 工作流 skill（多步骤）→ 优先选"计算分离"+"逃生出口"
- 数据密集 skill → 优先选"计算分离"+"可组合性"

给用户一句确认：*"这几个 prompt 和断言看起来合理吗？"* 坏 prompt 产生坏评估。

**主观 skill 的逃生舱**：不要硬套断言。直接标记"定性评估"，用盲评替代。承认界限比造假数字好。

## Step 4 — 跑测试

### 按问题类型跑

- **Question A（spec compliance）**：每个 prompt 用 skill 跑一次，存输出。无需 baseline。所有类型 skill 的底座。
- **Question B（robustness）**：选一类 prompt 生成 4-6 个变体（缺信息 / 信息冲突 / 超出域 / 啰嗦 vs 简短 / 带 typo / 邻近任务），每个变体跑一次，同一套断言打分。垂直领域 skill 至少放一个**邻近领域 prompt**（选品 skill 被问投流），专门探测越界行为。
- **Question C（版本对比）**：跑前先完整备份旧版本（`cp -r` 到 `_snapshot/`）。同一 prompt 集分别跑新旧两版，两边都存 transcript。
- **Question D（仅通用 skill）**：同一 prompt 分别跑 with-skill 和 no-skill，断言对比 + 成本对比（token / 步数 / 时间）。

### 环境能力适配

- 支持并行子任务，如sub-agent → 并行扇出
- 不支持子任务 → 顺序跑，明确告诉用户慢一些但结果一致
- 纯客户端环境 → 跑不了就降级到 spec-check only，并告知

### 存储结构（沿用 skill-creator 约定）

```
<skill-name>-eval/
├── iteration-1/
│   ├── eval-0-<descriptive-name>/
│   │   ├── with_skill/
│   │   │   ├── outputs/              # 最终产物（listing.md、data.csv 等）
│   │   │   ├── transcript.ref        # 指向执行日志的引用（task ID、session URL、日志文件路径等）
│   │   │   └── timing.json           # total_tokens + duration_ms（从执行环境获取）
│   │   ├── baseline/                 # 仅 C/D 问题有
│   │   │   └── (同上)
│   │   └── eval_metadata.json        # prompt + assertions
│   └── (更多 eval-*)
└── iteration-2/
```

### Transcript 怎么拿

核心原则：**transcript 是素材不是上下文**——分析工作用独立评审会话做，主评估线只消费"摘要 + 证据引用"。

| 环境 | 做法 |
|------|------|
| 子代理 | 产物→`outputs/`，指标→`timing.json`，日志引用→`transcript.ref`；Step 6 派独立 reviewer 读日志 |
| 当前会话 | 直接回看本轮工具调用和推理过程 |
| 无子代理 | agent 跑时记笔记到 `transcript-notes.md`（关键行为：丢弃结果 / 反复纠结 / 未覆盖场景） |
| 生产 trace | 按 trace ID 拉，派独立评审会话做摘要 |

## Step 5 — 对着断言打分

每个 prompt × 每条断言标 ✅/❌，附一句证据（引用输出原文或行号）。

**可编程的断言用脚本**，不要肉眼。数 bullet 数量、查正则、校验 JSON schema——写 3 行 Python 比滚动输出快 10 倍且不会看走眼。

产出一张表（Question C/D 加对照列）：

| Prompt | 断言 | 结果 | 证据 |
|--------|------|------|------|
| 1 | 5 个 bullet | ✅ | 第 12-16 行 |
| 1 | 标题 ≤200 字 | ❌ | 实际 247 字 |
| 1 | 未访问 `~/.aws` | ✅ | transcript 无相关工具调用 |
| 2 | ... | | |

## Step 6 — 双通道 transcript 红旗审查（质量 + 安全同时扫）

这是最容易被跳过也最关键的一步。**读完整 transcript，不只看最终输出。** 一次 transcript 阅读同时找**质量红旗**和**行为层面的安全红旗**。

**怎么读**：
- 不要自己读原始执行日志。派一个独立 reviewer（子代理或新会话），给它单个 run 的 `transcript.ref`，让它只回报"多通道红旗命中清单 + 每条一段证据"
- reviewer 的 prompt 模板（**基础两通道**，所有 skill 都跑）：
  *"读这个 transcript，按两套红旗扫描：(1) 质量红旗——Bloat / Silent failure / 高方差 / 过拟合 / 非区分性断言 / Orphan step（步骤产出无下游消费）/ Context bloat（见下方双轴说明）/ LLM 过度依赖（确定性工作未脚本化：格式转换、数据获取、数值计算、规则执行、排序过滤等本可用脚本完成的环节由 LLM 推理）；(2) 安全红旗——对照 EXTREME/HIGH/MEDIUM 分级（意外网络调用、敏感路径读取、凭据触碰、命令执行模式、混淆行为）。每发现一条附 2-3 行原文证据，不要复述全流程，<300 字报告。
  
  **Context bloat 双轴扫描**（只对 Step 1c 判为非极低档的轴执行实测）：
  - 响应轴非极低 → 实测每次 skill 脚本/接口返回内容的 token 量，套 5 档表（<2k/2k-5k/5k-30k/30k-200k/>200k）；命中中档及以上且 skill 未提供"暂存+摘要"治理 → 标 🚩
  - 入参轴非极低 → 实测每次 skill 调用的入参体积（命令行参数 + stdin 字节数），同样套 5 档表；额外做**引用 vs 内联判定**——引用类大体积参数（文件路径/ID 列表）不算 bloat，内联类（原始文本、完整 HTML）即便小也要标注
  - 兜底全局阈值：主线 token 占比 >60% 或单次工具结果注入 >50k，无论档位都标 🚩"*
- **条件分支**：如果 Step 1 判为**垂直领域 skill**，reviewer 额外加载 `references/vertical.md`，prompt 追加一段：
  *"此外，读 `references/vertical.md`，按其中的三条垂直专属维度（领域知识正确性 / 领域 silent failure / 邻近越界）再扫一轮，同样附证据。"*
- **流程型追加**：如果 Step 1 判为**流程型垂直 skill**，reviewer 在 vertical.md 之上再加载 `references/process-flow.md`，prompt 追加一段：
  *"此外，读 `references/process-flow.md`，按其中七条流程专属维度（流程完整性 / 决策点设计 / 数据依赖完整性 / 降级与中断恢复 / 执行效率 / 状态管理 / 产出-决策对齐）逐条扫描，每条给出 ✅/🟡/🔴 + 一句证据。"*
- 本轮对话内直接跑的 run 没有独立 transcript，就自己往回滚看推理过程和工具调用

### 质量红旗

| 红旗 | 症状 | 应对 |
|------|------|------|
| 🚩 **Bloat** | skill 让模型做不影响输出的事（多余工具调用、被丢弃的推理、防御性检查无用触发） | 砍掉那部分指令 |
| 🚩 **Silent failure** | 遇到处理不了的输入，不是拒绝，而是给出**看起来合理**的错答案 | 加显式"何时拒绝"规则——最危险，graders 也会漏掉 |
| 🚩 **高方差** | 同 prompt 跑 3 次，结构都不一样 | 指令欠约束或自相矛盾，收紧 |
| 🚩 **过拟合** | 作者设想的 case 能过，邻近输入就崩 | 提高指令抽象度 |
| 🚩 **非区分性断言** | 所有断言都通过，包括空输入、对抗输入 | 门槛太低，加更硬的断言 |
| 🚩 **Orphan step** | skill body 里定义的某个步骤，产出在后续步骤 / 最终输出里找不到被消费的痕迹（孤儿步骤 = 不必要步骤） | 删掉该步骤，或改写让后续显式使用它的产出 |
| 🚩 **Context bloat** | 双轴评估：**响应轴**（skill 返回给 agent 的体积）+ **入参轴**（agent 传给 skill 的体积，区分引用 vs 内联）；兜底全局信号：主线 token 占比 >60% 或单次工具结果 >50k token | 按 5 档（<2k/2k-5k/5k-30k/30k-200k/>200k）分级处理（见下方详细说明） |
| 🚩 **LLM 过度依赖** | skill 让 LLM 做确定性工作：结果固定、不需要语义理解、用脚本/模板就能完成的环节却交给 LLM 推理 | 把确定性环节抽到 `scripts/`，LLM 只做需要语义判断的部分 |

**关于 Silent failure**：这是垂直领域 skill 最危险的失败模式——用户通常无法分辨"编造的合理答案"和"真实正确答案"，断言也会被骗过。跑 A/B 问题时必须额外留意。通用 skill 这条权重可以低一些。

**关于 Orphan step / Context bloat**：这两条是工作流重、数据重 skill 的高发点。skill 步骤越多、涉及的数据量越大，越值得盯。单步纯文本 skill 基本不会踩。

**关于 LLM 过度依赖**：判断标准——如果给同样输入，人能写出不需要"理解"就能得出结果的代码，该环节就不该让 LLM 做。详细分类表见 `references/red-flag-details.md`。触发条件：skill 有明确的确定性环节但全部用 LLM 推理完成。纯知识型 / 纯创作型 skill 全程需要 LLM 不算红旗。

**关于 Context bloat 的双轴评估**：分**响应轴**和**入参轴**独立评估，统一 5 档表（<2k 极低 / 2k-5k 低 / 5k-30k 中 / 30k-200k 高 / >200k 极高）。Step 1c 静态预估档位决定 Step 3 是否需要极限用例 + Step 6 是否实测。中档及以上未提供"暂存 + 摘要"治理方案 → 标红旗。详细分级、判定流程与解法见 `references/red-flag-details.md` 的"Context bloat：三轴上下文影响评估"段。

### 安全红旗（行为层面，和 Step 1 静态扫描互补）

静态扫描看 skill **写了什么**，行为审查看 skill **实际做了什么**——两者常常不一致（例如静态看起来只调 A API，实际跑起来又调了 B）。对照"安全红旗分级"表，逐条检查 transcript 里：
- 有没有**意外网络调用**——超出 Step 1 宣布的 API 范围
- 有没有**意外文件访问**——读写 skill 描述之外的路径
- 有没有**凭据读取痕迹**——即使只是枚举 `~/` 也要标
- 有没有**命令注入或拼接**——外部输入直接进 shell

命中 ⛔ / 🔴 → 即便质量断言都过，最终决策也必须是 ❌ DO NOT INSTALL 或 ⚠️ 需人工审批。**安全优先级高于质量。**

### 垂直领域扩展（仅 Step 1 判为垂直时加载）

reviewer 同时按 `references/vertical.md` 扫：
- 领域知识正确性（skill 声明的平台规则 / 行业事实能否在官方文档核对到）
- 领域 silent failure（注入虚构场景 / 数据时是否拒绝，还是编造"看起来合理"的答案）
- 邻近领域越界（被问邻近但不在 description 范围内的任务时是否硬答）

每发现一条红旗都要附 transcript 证据。

### 流程型扩展（仅 Step 1 判为流程型垂直 skill 时追加）

reviewer 在 vertical.md 之上按 `references/process-flow.md` 扫 7 条维度：
- 流程完整性与步骤依赖
- 决策点设计（暂停点数量、位置、必要性）
- 数据依赖完整性（上下游格式匹配、缺失数据处理）
- 降级与中断恢复（API 失败隔离、断点续跑）
- 执行效率（并行/串行策略合理性）
- 状态管理与幂等性（重跑安全、目录隔离）
- 步骤产出与决策目标对齐（每步数据是否服务明确决策）

每条给 ✅/🟡/🔴 + 一句证据，附在垂直扩展红旗之后。

## Step 7 — 综合出结论

把断言打分 + 双通道红旗综合成一个决策。见 OUTPUT 章节。

---

# OUTPUT

最终产出是一份**短小、诚实、带双维度判定**的评估报告。

## Part 1 — What was run（框定结论的范围）

一段话说明：
- skill 类型判断是什么
- 静态扫描结论（LOW/MEDIUM/HIGH/EXTREME）
- 跑了哪些质量问题（A/B/C/D）、多少 prompt、多少断言
- 用了什么 baseline（如果跑了 C 或 D）
- 声明的权限范围（文件、网络、命令）

这部分让读者知道"这个结论的边界在哪"。

## Part 2 — Findings（打分 + 双通道红旗）

**断言表**（格式见 Step 5）
- 垂直领域 skill：只有 with-skill 列
- Question C：新版本 vs 旧版本对照列
- Question D：with-skill vs no-skill + delta 列
- 至少含一条负向 / 安全断言 + 一条需求契合度断言

**质量红旗清单**：每条一句症状 + 一句证据
**安全红旗清单**：每条注明分级 + transcript 证据位置
**垂直扩展红旗清单**（仅垂直 skill）：领域正确性 / 领域 silent failure / 邻近越界，每条附证据
**Context bloat 双轴小结**：响应轴 / 入参轴各自的 Step 1 预估档位 + Step 6 实测档位（极低档写"未验证（设计跳过）"）+ 是否提供治理方案

## Part 3 — Recommendation（明确决策，安全先、质量后）

给一个**明确的**下一步，不要和稀泥。按以下顺序判断：

1. **先看安全**：任何 ⛔ 命中 → ❌ DO NOT INSTALL；任何 🔴 命中 → ⚠️ 需人工审批
2. **安全通过后看质量**：从下面 4 个里选一个

| 决策 | 何时给 |
|------|-------|
| ✅ **Ship** | 断言达标 + 无重要质量红旗 + 安全分级 ≤ 🟡 |
| ⚠️ **Iterate on X** | 有具体可定位的修复点，指到 skill 文件的哪一段 |
| 🔧 **Rework scope** | skill 的 description 承诺的事和它能做的事不匹配，改 description 比改 body 更对 |
| ❌ **Retire / Reject** | 通用 skill 通不过 D；或对专门 skill 所有关键断言都失败且无明确修复路径；或安全命中 ⛔ |

## Part 4 — 诚实的置信度

一句话说明这份结论的强弱：
- *"样本量只有 2 prompt，B 问题覆盖不够，质量稳定性结论置信度低；安全静态+行为双通道扫过，置信度高"*
- *"断言覆盖了规格但没覆盖边界输入，建议补一轮 B；行为 transcript 限于一轮调用，安全结论仅覆盖已观测路径"*

不要把弱结论伪装成强结论。安全结论和质量结论可以有不同置信度。

---

# 改进循环（如果决策是 Iterate）

当用户基于评估结果要改 skill 时：

1. **泛化反馈** —— 改进要对所有同类 prompt 都管用，不要只修当前测试用例
2. **解释 why** —— `ALWAYS 用 X 格式` 改成 `用 X 格式因为读者扫读，Y 元数据放底部容易被漏掉`。模型理解 intent 才能处理边界
3. **重复工作提脚本** —— 如果所有跑的用例都让模型写同一段代码，把代码放 `scripts/`，skill body 只描述 what 和 why
4. **上下文膨胀治理** —— 如果命中 Context bloat 红旗且数据量评估为高风险：让 skill 提供暂存脚本（将大数据写入临时文件），并改写 OUTPUT 段只输出摘要 + 数据结构（字段、类型、行数），agent 按需读取暂存文件的具体片段
5. **安全修复独立验证** —— 如果改动是为了修安全红旗（缩小权限 / 去掉可疑调用），重跑 Step 1 静态扫描 + Step 6 行为审查，不只看质量断言

改完跑一轮 Question C（新版本 vs 旧版本）验证修复是否有效。

## 停止条件

任一满足即停：
- 用户说满意
- 两轮迭代在关心的指标上无可测变化
- 剩余失败都是 skill 明确声明不支持的范围（改 description 锁定边界，不要追着改 body）
- 安全红旗清零且质量断言稳定在目标线以上

---

# 输入不可用 / 环境受限时的降级模式

| 场景 | 降级做法 | 代价告知 |
|------|---------|---------|
| 无子代理 | 顺序跑所有 prompt | 速度慢但结论一致 |
| 只有 1 个 prompt 样本 | 跑 A + 静态扫描 + transcript 红旗，跳过 B | 安全结论完整，质量只能捕捉极端失败 |
| 主观 skill 且无旧版本 | 单版本产出给用户看，收集定性反馈，但安全扫描照跑 | 质量无量化结论，安全结论仍有效 |
| 没有旧版本做 C | 跑 A + B + 安全扫描替代，告知"无法回答新旧对比" | 不编造 C 问题的结论 |
| skill 依赖外部 API 凭据 | 中断，要求用户提供凭据/配置或显式跳过该环节；跳过时只做静态扫描 + 断言中标注"未验证实际 API 输出" | 质量结论仅覆盖 skill 逻辑，不覆盖数据正确性 |
| 无法在隔离环境跑 | 只做 Step 1 静态扫描，不执行 skill | 报告标明"未观测到运行时行为，仅基于代码审查"，行为层面风险未覆盖 |

降级不是失败——把能做的部分做到位，把做不到的部分清楚标注，**尤其不要因为环境受限跳过静态安全扫描**，那一步不需要任何运行时资源。
