# Changelog

## 1.0.1 · 2026-10-15 · ClawHub 安全审查

- SKILL.md 新增「信任边界」：本 Skill 执行目标仓库自带的 `.harness/` 脚本，`working-tree`/`local` 模式会读本机 Skill 与 Memory；只在自有或明确信任的仓库运行本地模式，来源不明的仓库先征得同意、通读 `verify.sh` 并默认改跑 `--ci-hermetic`。
- README 同步该信任边界说明。
- frontmatter 补 `metadata.openclaw.requires.bins`（bash / python3）；缩短 description 触发边界。

## 未发布 · 2026-10-12 · Skill Doctor 自检误报修复

- 保留机器专属路径扫描能力，同时拆分检查器与 CI 中的检测字面量，避免 Doctor 把检测规则本身误判为硬编码路径。
- 新增正反例回归，证明可移植文档放行、真实机器路径仍会命中。
- 将跨宿主发布信息收进标准 `metadata`，保留信息的同时通过 Codex Skill 基础契约校验。

本文件记录独立 `hekouwang-harness-check-skill` Skill 的发布变化。

## Unreleased

- 增加版本化的 pre-push Hook 与安装脚本，对实际推送的 Skill 快照运行单测和 Skill Doctor，失败时阻止推送。
- 为产品页和 Guide 补充品牌 favicon，避免 GitHub Pages 浏览器标签显示默认图标。
- 新增标准库实现的 `Harness Scorecard` CLI，提供 12 维加权分、硬上限、置信度、成熟度、宿主矩阵、退出码和 JSON/Markdown 输出；
- 新增评分规则与 JSON Schema，输出可直接供后续网页/GIF 消费；
- 新增强/弱仓库 fixture 回归，验证 README 关键词不能绕过缺失门禁；
- 新增可插拔领域 Profile 机制与首个 `content-agent` Profile，把发布状态、来源、渠道、生成物、视觉和外部副作用从通用分中分离；
- 增加 DeepSeek Harness 对标定位，明确运行时与独立验收层的产品边界；
- 新增 GIF/网页演示分镜与离线 JSON 数据消费说明；
- 修正执行日志的检查数量解析、超时/启动失败结构化和失败标签误报。
- 新增自包含 GitHub Pages 产品页：用 Terminal Kit 风格的双语长页展示独立验收定位、四个差异化轴、交互式 Scorecard、证据闭环、`content-agent` Profile 和真实宿主 `unknown` 边界；
- 新增 `website/data/demo-scorecard.json` 演示数据与 Pages 发布工作流，JSON 可下载并可继续驱动网页、GIF 和 CI Artifact。
- 产品页展示名调整为 `hekouwang Harness Doctor`，简称 `Harness Doctor`：用品牌化的“体检/诊断/复查”叙事突出与运行时、普通审计工具的边界；仓库名与 Skill 名保持不变。
- 优化产品页首屏：中文标题按语义固定为三行，`Harness` 使用明确的 Google Sans 粗体字重，并加入绿色—紫色的浅层渐变背景。
- 新增 `harness_score.py --format terminal --live --color`：真实执行验证器时显示动态进度，完成后用颜色区分 `PASS`、`PARTIAL`、`BLOCKED`、分数、置信度和宿主 `unknown`；JSON/Markdown 输出保持无 ANSI 污染。
- 将基于 36 页 Harness 入门教程整理的中文学习路线迁移至独立 `website/guide/index.html` Guide 文档站，覆盖从 `Agent = Model + Harness`、Guides/Sensors、`CLAUDE.md`、Hook、Subagent、Evaluator、Context Reset、Sprint Contract 到失败台账，并补充独立验收层的证据、状态、宿主和硬门槛。
- 产品页新增“从 0 到可验收”学习路线和真实 `Ghostty.gif` 运行录屏；GIF 只作为动态入口，完整结果仍由 JSON Scorecard、真实退出码和人工/宿主边界共同决定。
- 新增 `website/guide/index.html` 独立 Guide 文档站：采用 Terminal Kit 同类的粘性报头、左侧章节导航、阅读进度、代码块、表格、成熟度路线和真实运行证据；产品首页与完整教程分层呈现。
- 精简产品首页：移除占据首屏下方空间的“文档地图”卡片区，并在顶部导航新增 `Guide / 文档` 入口，直接进入独立教程页。
- 修复产品页视觉回归：纠正 Guide 标题的静态字体字重声明，统一英文标题使用真实可变 `Google Sans`；隔离首页摘要的 `.partial` 样式，修复 Scorecard 部分维度按钮塌缩后造成的文字、分数与进度条重叠，并加入 CI 防回归检查。
- 进一步移除 Scorecard 维度按钮对通用 `partial` class 的依赖，改用 `dimension-state-*` 和 `dimension-status-*` 专用状态名，避免跨组件样式碰撞。

## 0.1.0 — 2026-08-17

- 首次独立发布证据驱动 Harness 检查器 Skill；
- 提供 `working-tree`、`staged`、`ci` 三种验证模式的编排与报告协议；
- 覆盖 Hook、Safety Gate、Task Contract、Episode、可观测性、失败台账和真实宿主边界；
- 发布中文 README、英文 README、检查矩阵和 SVG 流程图；
- 采用 MIT License。
