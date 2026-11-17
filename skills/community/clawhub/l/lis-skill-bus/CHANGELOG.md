# CHANGELOG

## 0.1.12 · 2026-11-10 · 发布链路脱敏修复

- **入口闸门脱敏**：`lib/entry_gate.py` 文档串的本机私有目录前缀改为 `$HOME` 变量写法，报错文案去掉脚本路径字面串，修复发布扫描误报；行为逻辑不变。
- **版本占位**：0.1.11 已在 SkillHub 占用，按“同版本不可覆盖”规则递增到 0.1.12，重新发布三平台。
- 五个算量技能内 vendored `entry_gate.py` 与本版 canonical 同步（SHA-256 `f5c19c3f…1d00`）。

## 0.1.11 · 2026-11-09 · 常驻注入瘦身

- **description 精简**：技能目录注入的 description 压到 ≤45 字，保留原有触发词与「不做什么」边界；SKILL.md 正文与算法口径未变。

## 0.1.10 · 2026-11-08 · 技能层瘦身与发布完整性

- **SKILL.md 瘦身**：4,311 B → 3,825 B（-11.3%）。触发词、硬规则、能力边界保留在前置段；低频细则外移到 `references/`、`docs/`、`packs/`，按需加载，算法与业务口径不变。
- **发布完整性**：被引用文件随包存在、Python/bash/JSON 语法通过、技能自检 PASS；未实现的检查如实记 SKIP。
- **脱敏**：本机路径、真实项目名与公司资料引用替换为通用示例；平台专用入口只改发布副本。


## 0.1.9

- 固化钢结构正式识图口径：`cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`；
  缺 bus 时正式 statesync 以退出码 2 停止。
- 清除“MCP 是增强层不是前置”“未命中降级本机解析”等容易被误解为可绕过正式链路的旧文案。
- 版本号与自测基线统一为 0.1.9。

## 0.1.8

- 发布包统一使用系列蓝图蓝标 `icon.png`，与钢结构算量技能保持同一视觉系列。
- 补齐 SkillHub 专用图标元数据与公开页面展示，不改变本机技能的识图或状态同步逻辑。

## 0.1.7

- 新增钢结构算量 `gangjiegou-suanliang` 的 bus 接线：`integration/gangjiegou_pull_contract.sh/.cmd`
  与 `gangjiegou_publish_contract.sh/.cmd`，等价转发到该技能的 statesync。
- 技能范围扩为 `cad-file-reader + 5 个算量技能`（土建、安装、装饰、园林、钢结构）；
  钢结构核心 section 为 `members`、`sections`，支持 `--require-core`。
- 文档收紧正式识图口径：固定为 `cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> 算量技能`，
  缺 bus 时停止正式识图并提示安装，不提供算量技能自行解图的第二套路径。
- 文档、版本号与 Windows 静态接线同步到 0.1.7。

## 0.1.6

- 目录探测修复：`scripts/` 缺失也能探测（原默认 marker=scripts 的 deps.py 逻辑失败），
  无 scripts 的 lis-skill-bus 用根目录 `SKILL.md`/`manifest.json` 兜底。`list_skills`
  与新增 `detect-skill` 返回 `marker`/`has_scripts`/`scripts`。
- 新增 `find_contract`（CLI + MCP + client）：按 source sha256/文件名判同图，`同图只解析一次`
  有明确判据；push 时把 `source.file`/`source.sha256` 写入 `_provenance` 溯源。
- 自测扩到 14 个用例：同图判重、多算量共享、降级自身 state、无 scripts 目录探测全绿。
- 修 install_skillbus.sh 全角括号紧跟变量导致 bash 把 `（` 首字节并入标识符的问题（--dry-run/--uninstall 输出）。

## 0.1.5

- 前端文档补齐：识图契约红线（禁止各算量技能自行解图）固化到 SKILL.md，README 同步。
- 版本口径统一：SKILL.md / _meta.json / README 统一为 0.1.5。


- 发布兼容：SkillHub 打包不保留执行位，脚本调用统一走 `bash`；`LICENSE` 更名为 `LICENSE.md`（平台文件类型白名单）。

## 0.1.3

- 文档更正：土建技能名由 `shangwu-suanliang` 更正为实际发布的 `tujian-suanliang`（frontmatter 与正文两处）。
- 版本口径统一：SKILL.md / _meta.json 统一为 0.1.3，正文标题同步。
- 补齐 `LICENSE`（MIT，与 frontmatter 声明一致）与本 CHANGELOG。
- 补充说明：安装脚本支持 `CODEX_HOME` 覆盖落点，非 Codex 环境（如 WorkBuddy）可指定到本机对应目录。

## 0.1.2

- 内部版本：状态文件结构兼容性修补。

## 0.1.1

- 首次对外发布：MCP server 安装器 + 五个 CAD 技能共享项目状态与 `cad-contract/v1` 契约。
