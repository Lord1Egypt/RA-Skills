# Changelog — nodecoda-workflow skill

## [Unreleased]

### Added
- **REST 直连回退指南**（SKILL.md「公共部署」）：MCP 工具返回 `401 NO_KEY`（stdio server 未继承 `NODECODA_KEY`）
  时直接打公网网关的完整 curl 流程（提交/轮询/artifact 拉取），凭据只从环境读取。
- **gotchas G13**：`else if` 链合法——`grammar.ebnf` 只显示 `else_clause_opt` 易误判，实证可链式。
- **gotchas G14**：REST 直连缺 `Idempotency-Key` 请求头 → `400 WORKFLOW_BUILD_REQUEST_INVALID`
  （幂等 key 必须 body + header 双份；MCP server 自动转发，直连不会）。
- **failure-modes.md**：新增「客户端/环境层 HTTP 错误（不是 Source 诊断）」——`401 NO_KEY` / `400`
  不改 Source、不伪造 build_id。

### Changed
- **SkillHub 详情页展示化**（build-skillhub.mjs）：发布包 SKILL.md frontmatter `description` 改为用户向
  中文简介（平台将其放入"中文简介"槽），正文顶部新增「这是什么 / 快速上手 / 环境要求」用户向介绍；
  源 SKILL.md 与 npm 安装路径不变，agent 触发词保留。
- **营销文案加「为什么值得信」**（build-skillhub.mjs）：发布包用户向介绍新增痛点故事（手工搭
  Dify 的坑）、构建校验背书（过不了不交付）与边界声明（运行时行为由用户在 Dify 配置确认）。
- **精简展示文案**（build-skillhub.mjs）：删除「开箱即用」段（Node.js 版本、Dify 1.16、免费体验与注册引导）。
- **展示文案营销化**（build-skillhub.mjs）：发布包用户向介绍改为营销向文案——收益导向（不用自己写
  YAML、几分钟拿成品）、「开箱即用」替代「环境要求」、去掉配额宣传（设备日限 50 次）、新增 GitHub 链接；
  H1 引导段与 frontmatter description 同步改为用户向表述。
- **改名与品牌**（SKILL.md + build-skillhub.mjs）：展示名 `NodeCoda Workflow` → `NodeCoda Dify Workflow`；
  发布包用户向介绍新增口号「让 AI Agent 构建你信得过的 Dify 工作流」、官网 https://www.nodecoda.com，
  快速上手改为「直接导入、无需检测」。
- `references/mcp-contract.md`：Build 段补 `Idempotency-Key` header 双份要求；Poll 段补 REST 直连
  artifact 需单独 `GET /v1/workflow-builds/{build_id}/artifact`。
- `references/project-workflow.md`：补同 Source 重建完整状态链
  `SUCCEEDED -> SOURCE_READY(--rev+1) -> BUILDING(--build-id) -> SUCCEEDED`（直接跳 SUCCEEDED 会非法）。
- SKILL.md：`save-build` / `live-mcp` 补充 npx 等价调用形式（脚本在包内，非仓库根）。

## [0.2.15] — 2026-08-13

### Added
- **机器可读语言包** `language-pack/`（研究文档 `docs/research/teaching-ai-a-new-c-style-dsl.md`
  Phase 0/1 skill 侧落地）：
  - `grammar.ebnf` — 带 `[feature]` 标签的 EBNF（源自 grammar-reference.md）
  - `builtins.json` — 内置函数签名/效应/输出字段/retry 支持
  - `diagnostics.json` — 诊断分类（L1-L4）+ 实证 code→修复映射
  - `targets/dify-1.16-graphon-0.6.json` — 能力矩阵 + capability gate
  - `antipatterns.json` — G1–G8 反模式结构化（id/codes/symptom/cause/correct）
  - `version.json` — 文件 hash + source_docs 原文 hash（版本漂移检测）
- `scripts/validate-language-pack.mjs` — 语言包校验（JSON schema、hash 一致性、
  源文档漂移检测）；已纳入 `npm run validate` / `npm run test:all`
- `scripts/test-language-pack.mjs` — 语言包回归测试（含漂移检测用例）
- manifest.json 新增 `language_pack` 字段；references 规范新增 §4 语言包章节

### Changed
- `SKILL.md` 新增语言包检索指引：按 feature 取最小规则集，不整卷塞 prompt

## [0.1.0] — 2026-08-11

### Added
- Initial split-out from the main NodeCoda repository
- Full content from the original skill:
  - `SKILL.md` — workflow contract, 6-step process, final report template
  - `references/mcp-contract.md` — 3 MCP tools + invariants
  - `references/source-generation.md` — minimal Source and 5 core operations
  - `references/language-reference.md` — full DSL reference
  - `references/public-service.md` — client config, admission, polling, readiness
- New references added during split-out:
  - `references/diagnostics.md` — Diagnostic shape, code taxonomy, severity, repair priority
  - `references/target-capabilities.md` — Dify 1.16 capability matrix (supported / partial / unsupported)
  - `references/iteration-loop.md` — bounded repair loop (5 iterations max) and stop signals
  - `references/failure-modes.md` — `failure_kind` handling table
- 4 runnable examples in `examples/`
- `manifest.json` with cross-platform metadata
