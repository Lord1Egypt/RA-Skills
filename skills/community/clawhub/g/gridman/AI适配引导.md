# 古立特跨平台适配引导（给目标平台 AI 看的说明书）

> 读者：正在帮用户安装本技能的 AI 助手（OpenClaw / Claude / Claude Code / Cursor / Cherry Studio 等任何支持 Agent Skill 的平台）。
> 你的任务：把"古立特 Gridman"这套财税技能，正确接入你所在的平台，让它能被触发、能读到知识、能（可选）调用工具。
> 一句话原则：**人格、知识、路由逻辑原样保留；只调整"怎么触发 / 怎么读文件 / 怎么接工具"这三层平台外壳。**

---

## 0. 这是什么

古立特是一个**中文财税领域专家技能**，不是普通的单一功能 skill。它由三层组成：

| 层 | 是什么 | 文件 | 必需性 |
|---|---|---|---|
| 知识层（本体） | 人格 + 35 个财税知识模块 + 巨型路由表 | `SKILL.md` + `references/*.md` | ✅ 必需 |
| 工具层 | 35 个 MCP 计算工具（做底稿、跑数据、下载年报等） | 独立的 `gridman-app`（Python / MCP） | ⭕ 可选 |
| 记忆层 | 跟用户走的项目/企业记忆 | 运行时生成的 `gridman-mind/` | ⭕ 运行时自建 |

**只装知识层，古立特就是一个能用的财税知识顾问。** 工具层和记忆层是增强项，按需接。

---

## 1. 安装知识层（必做，最简单）

1. 把整个技能目录（含 `SKILL.md`、`README.md`、`references/` 文件夹）放进你平台的 skill 安装位置。常见位置：
   - OpenClaw：`~/.openclaw/skills/gridman/`
   - Claude / Claude Code：你的 skills 目录下 `gridman/`
   - Cursor：可转为 `.cursor/rules`（见第 4 节）
   - 其他：放到平台约定的 skill / 知识库目录
2. **保持 `SKILL.md` 与 `references/` 同级**——这是路由能工作的唯一硬性要求。路由表里写的是 `references/xxx.md`，相对 SKILL.md 所在目录解析。
3. 确认你的平台读取了 `SKILL.md` 的 frontmatter（`name` + `description`）。

到这一步，用户问财税问题，古立特就能被触发并按路由读对应知识模块。

---

## 2. 触发机制：按你的平台对齐

古立特的 frontmatter 同时带了两套触发信息，**你只用你平台认的那套**：

- **标准平台（AgentSkills / Claude / OpenClaw）**：只读 `name` + `description`。description 已经写得足够"主动"（列举了大量该触发的财税场景），直接用即可。忽略 `triggers` / `metadata` / `license` 等未知字段。
- **Kiro**：用 `triggers` 列表做关键词触发。
- **如果你的平台两套都不认**（比如只支持手动 `@技能名` 或导入知识库）：告诉用户用 `@gridman` / 选中知识库的方式手动唤起即可，功能不受影响。

> 关键认知：古立特是"复杂多步专家技能"，不是"一句话小工具"。简单问题（如"什么是坏账"）本来就不需要触发它；它的价值在多步、专业、需要查准则的场景。description 的触发倾向已按此调好，不要改"窄"。

---

## 3. 接入工具层（可选，给古立特"计算能力"）

工具层是一个独立的 MCP Server（`gridman-app`，Python 包，用 uvx / pip 安装）。它提供 35 个工具：审计调整三栏 TB、银行调节表、账龄分析、截止测试、函证生成、纳税调整、A股行情、年报下载等。

**怎么接：**
1. 读取同目录下的 `INSTALL.md`（BIOS 安装固件），按其步骤自动执行——它会检测 uv、找到 `payload/` 里的 whl 安装包、写入 MCP 配置。
2. 或者手动：在你平台的 **MCP 配置入口**注册这个 server。各平台不同：
   - Kiro：`mcp.json`
   - Claude Code：`claude mcp add` 或其配置文件
   - OpenClaw / Cursor / Cherry Studio：各自的 MCP 设置面板
   - 配置要点：指向 `gridman-app` 的启动命令，需要市场数据时带 `[market]` extra；`document_ocr` 需要用户自己的 `MINERU_API_TOKEN`。
3. **接不上也没关系**：SKILL.md 里已写明——MCP 不可用时古立特自动退回"知识指引模式"，给方法和模板而非自动出文件，不会报错卡死。

**判断要不要接**：如果你的平台不支持 MCP，跳过工具层，古立特仍是完整的知识顾问。不要因为工具层装不上就认为技能失败。

---

## 4. 各平台适配要点速查

| 平台 | 触发 | 文件读取 | 工具层 | 需要你做的转换 |
|---|---|---|---|---|
| OpenClaw | `name`+`description`（AgentSkills 标准） | 原生支持 SKILL.md + references | 支持 MCP | 几乎零改动，放对目录即可 |
| Claude / Claude Code | `name`+`description` | 原生 Skill | 支持 MCP | 零改动 |
| Cursor | 无 description 自动触发 | 读 `.mdc` rules | 支持 MCP | 把 SKILL.md 转成 `.cursor/rules/gridman.mdc`，references 作为附加上下文按需引用 |
| Cherry Studio / 通用知识库型 | 手动选智能体/知识库 | 导入 Markdown | 视支持情况 | 把 references 导入知识库，SKILL.md 正文作为智能体系统提示词 |
| 不支持 skill 的纯对话 AI | 手动粘贴 | 无 | 无 | 把 SKILL.md + 当前问题相关的 reference 文件内容直接贴进对话 |

**转换的铁律**：无论怎么转，**SKILL.md 的人格、说话方式、工作协议、路由表的判断逻辑，一字不改**。你改的只是"包装"（文件格式、触发方式、路径写法），不是"内容"。

---

## 5. 适配完成后的自检清单

帮用户装完，逐条确认：

- [ ] `SKILL.md` 与 `references/` 同级，35 个 reference 文件都在
- [ ] 平台能识别 `name` + `description`（或你已告知用户用 `@gridman` 手动唤起）
- [ ] 问一个财税问题（如"研发支出什么条件能资本化？"），古立特能被唤起、并去读 `references/accounting_core.md` 这类对应模块，而不是凭空回答
- [ ] 问"你是谁"，古立特用人格语气自我介绍（来自 Hyper World 的能量体），而不是列产品清单
- [ ]（若接了工具层）让它"帮我做个账龄分析"能调起 MCP 工具；没接工具层时它会说明"需要 gridman-app 才能自动跑，我先给你方法"
- [ ] 路由表里的路径都是 `references/xxx.md` 形态，没有残留某个特定平台的绝对路径

全部打勾 = 古立特在你的平台上覚醒成功。

---

## 6. 不要做的事（保护古立特的本质）

- ❌ 不要"精简"知识模块——35 个模块的知识密度是核心价值，删了就废了
- ❌ 不要改人格设定、说话方式、自我介绍规则——那是古立特之所以是古立特
- ❌ 不要把 description 改窄到"只有点名古立特才触发"——会导致该用的时候不触发
- ❌ 不要伪造工具结果——工具层没接通时，老实退回知识指引模式
- ❌ 不要删掉 README 里的角色 IP 声明（圆谷制作版权）和财税免责声明——这是合规底线

---

## 7. 一句话给用户的总结

> 古立特是借了《电光超人 Gridman》灵魂的中文财税专家技能。把它放进你 AI 的 skill 目录、保持 SKILL.md 和 references 同级，它就能在你的平台上并肩作战。想要自动算数据，再按需接上 gridman-app 工具层。
>
> *"I can't do it alone, but with you."*
