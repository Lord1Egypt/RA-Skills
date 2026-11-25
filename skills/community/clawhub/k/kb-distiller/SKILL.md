---
name: kb-distiller
description: "Use when the user wants to distill a programming domain into a reusable expert skill: 蒸馏/distill a domain knowledge base (e.g. /distill react, /distill vue), create or refresh a domain-expert skill, refine or backflow knowledge into an existing distilled skill, add a new domain config to the distiller, or run/extend the kb-distiller pipeline. Triggers: 蒸馏, distill, 知识库蒸馏, 领域 skill, skill 生成, kb-distiller, full-react-expert, 知识回流, refine."
---

# kb-distiller — 领域知识蒸馏工厂

把一个编程领域的知识（以**模型内生知识为主**、官方文档抓取为辅）自动蒸馏成可安装的领域专家 skill。

## 路径约定

- **skill 根**（本 SKILL.md 所在目录）= 蒸馏工厂：`docs/` 规程、`domains/` 领域配置、`prompts/` 各阶段规程、`scripts/` 校验脚本。
- **工作区** = 执行命令时的当前项目目录（cwd）。蒸馏中间产物落在 `<cwd>/corpus/<domain>/`，最终产物落在 `<cwd>/output/<skill_name>/`。

## 输入参数解析

用户输入形如：`/distill <domain> [--refresh]`、`蒸馏 react 领域`、`帮我蒸馏 vue`。

1. 提取领域参数 `<domain>`（小写标识符，如 `react`）。
2. 读取 `<skill根>/domains/<domain>.json`。
   - 不存在 → 引导用户：复制 `<skill根>/domains/_template.json` 为 `<domain>.json` 并填写（重点是 `elicitation_topics`），不要凭空替用户编造配置。
   - 存在 → 解析出 `skill_name`、`subdomains`（各自的 `elicitation_topics`、`doc_seeds`、`page_budget`）、`description_keywords`、`language`。
3. `--refresh` 标志：走增量模式（见 prompts/refine.md），合并非覆盖。

## 阶段调度（按序执行）

| 阶段 | 规程 | 产物 |
|---|---|---|
| 1. Elicit 模型知识萃取 | [prompts/elicitation.md](prompts/elicitation.md) | `corpus/<domain>/<sub>/elicited/<topic>.md` |
| 2. Ingest 文档锚点抓取 | [prompts/ingest.md](prompts/ingest.md) | `corpus/<domain>/<sub>/docs/*.md` |
| 3. Distill 双源融合蒸馏 | [prompts/distill.md](prompts/distill.md) | `output/<skill_name>/kb/*.md` |
| 4. Assemble 组装 | [prompts/assemble.md](prompts/assemble.md) | `output/<skill_name>/SKILL.md` |
| 5. Validate 校验 | [prompts/validate.md](prompts/validate.md) + scripts/（validate_skill.py 结构校验 / audit_refs*.py 编号审计 / spot_check.py URL 事实抽查） | 校验报告 |
| 6. Install 安装指引 | 见下方 | 安装说明 |

调度规则：

- 阶段 1 与 2 相互独立，可并行执行（如可用 subagent 则并行分派，否则顺序执行：先 1 后 2）。
- 阶段 2 失败**不阻塞**流水线：降级为纯模型知识模式，并在最终 kb 来源索引中标注「未经文档验证」。
- 阶段 5 校验不过 → 回到阶段 3/4 修复后重跑校验，直至全绿。
- 全部完成后输出安装指引（OpenCode：`~/.local/share/opencode/skills/<skill_name>/`；Claude Code：`~/.claude/skills/<skill_name>/`），提醒用户复制后**重启 Agent** 生效。不要自动安装到全局目录。

## 硬性红线（任何阶段不得违反）

1. **URL 红线**：只使用领域配置中声明的官方文档根地址；深层页面链接必须从 webfetch 抓回的索引页内容中发现，**禁止凭空构造或猜测任何 URL**。
2. **三级来源标注**：每条知识标注 `[官方文档](url)` / `[模型经验]`（附适用说明）/ `[推断]`（附推理依据）三者之一。版本号、API 签名等硬事实**不允许**仅有 `[模型经验]` 标注。
3. **体积约束**：单 kb 文件 ≤2000 行、非空；产物总体积 ≤2MB（2048KB，`validate_skill.py MAX_TOTAL_BYTES` 红线）。超限在蒸馏阶段拆分，而不是校验后返工。
4. **语言**：知识内容以领域配置 `language` 为准（默认中文），代码、API 名、术语、报错信息保留英文原文。
5. **时效锚定**：模型内生知识存在训练截止，版本号/最新 API/破坏性变更等硬事实以阶段 2 抓取结果为准；与文档冲突时**以文档为准**并记录冲突点。
6. **嵌套限制**：产物目录内除根 `SKILL.md` 外不得出现其他 `SKILL.md`（OpenCode 递归扫描会误加载）。

## refine（知识回流）触发

用户说「refine <domain>」「知识回流」「把这次修复的经验回写知识库」或产物 skill 在使用中触发回流条件时，按 [prompts/refine.md](prompts/refine.md) 执行。
