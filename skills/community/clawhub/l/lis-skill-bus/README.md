# lis-skill-bus v0.1.12

本地 Skill 联动总线：**Skill 管专业算法，bus 管项目状态与契约**。
纯 Python stdlib、不联网、跨平台；CLI 与 MCP 双模式，是正式识图链路的必需契约桥。

## 装上有什么好处（给用户看）
- **同一张图只解析一次**：cad-file-reader 解析完写契约，土建/安装/装饰/园林/钢结构直接复用候选，不重复解图；
- **6 技能共享**：同一把项目 key，状态与契约通用，断点接续；
- **完全本地**：纯 stdlib、不联网，公司数据只落本机；
- **正式识图必须安装**：链路固定为 `cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> 算量技能`；bus 缺失时停止正式识图并提示安装，不允许算量技能自行解图；
- **一行安装**：`bash install_skillbus.sh --apply`（Windows GitHub 完整包：`install_skillbus.cmd --apply`，SkillHub 版用 `python install_py.py --apply`；只注册复制不留注册：`SKIP_MCP_REG=1 bash install_skillbus.sh --apply`）。
详细话术见 `BENEFITS.md`。

## 目录
- `skillbus.py`             MCP stdio server + CLI 入口（含 detect-skill / find-contract）
- `schemas/cad-contract-v1.schema.json`  统一联动契约（复用 cad-file-reader/v0 + qto-project/v1）
- `install_skillbus.sh`     安装/回滚脚本（--dry-run / --apply / --uninstall，macOS/Linux）
- `install_skillbus.cmd`    Windows 安装壳（调 install_py.py，纯静态校验通过）
- `install_py.py`           .cmd 的跨平台 config 助手（纯 stdlib）
- `skillbus_client.py`      各 SKILL 的 CLI 接线客户端（push/pull/list/resolve）
- `skillbus_client.cmd`     Windows CLI 薄壳
- `SKILL.md`                平台发布用最小安装器说明（非业务技能）
- `BENEFITS.md`             引导好处文案
- `mcp-config.example.json` Claude Desktop / Cursor / 其他 stdio 客户端注册样例
- `integration/`            cad-file-reader 发布契约 / 土建、安装、装饰、园林、钢结构算量拉取契约的接线脚本与验收
- `example_pilot/`          cad-file-reader → 土建算量链路示例（示例项目，非真实工程）

## 4 个能力
| 工具 | MCP | CLI |
|---|---|---|
| 枚举 skill | `list_skills` | `list-skills` |
| 读项目状态 | `get_project_state` | `get-project-state` |
| 写项目状态（原子写） | `push_project_state` | `push-project-state` |
| 解析契约 schema | `resolve_contract` | `resolve-contract` |

## 状态过滤红线
- 状态默认存 `$HOME/.codex/skills/.skillbus/state.json`（`SKILLBUS_STATE_DIR` 可改）
- 数据库仅本机、不入 iCloud/网盘/Git 远端；公司数据不经过任何网络
- state.json 损坏时降级为空库并返回 `_corrupted`，不覆盖原文件

## SKILLBUS_HOME 与 bus 命中优先级（2026-10-22）
- 客户端（各 SKILL 的 `*_statesync.py`）定位 `skillbus_client.py` 的顺序：
  ① `SKILLBUS_HOME`（bus 目录）或 `SKILLBUS_CLIENT`（直接指向 client 文件）显式环境变量
  ② `$HOME/.codex/mcp_servers/lis-skill-bus/skillbus_client.py`（**正式安装落点**，即 `install_skillbus.sh --apply` 的目标目录）
  ③ `$HOME/.codex/skills/lis-skill-bus/skillbus_client.py` 与 `$HOME/.codex/skills/.skillbus/skillbus_client.py`
  ④ 常见本机开发/临时副本目录（临时工作区/开发副本）——先正式，仅正式缺失才回退
- 命中 dev/临时副本时，statesync 在 stderr 输出告警行：`bus 命中来源：<路径>（临时副本/dev，非正式安装）`；正式命中输出 `（正式安装）`。
- `SKILLBUS_DISABLE=1` 只用于隔离测试。正式识图链路不得用 `SKILLBUS_DISABLE=1` 绕过 bus；算量技能缺少 bus 时应停止正式识图并提示安装，或者只消费已经由正式链路生成并留存的契约。

## 当前边界（骨架版）
- MCP 用行分隔 JSON-RPC，满足 initialize / tools/list / tools/call；未实现 resources/notifications 全集
- 契约 catalog 只收录 `cad-file-reader/v0` 与 `qto-project/v1` 元数据；详细 schema 以完整包为准
- 接线规范见 example_pilot/pilot.md；接线脚本见 integration/
- 已完成 cad-file-reader、土建、安装、装饰、园林、钢结构 6 个 skill 的 bus 接线段；钢结构的正式链路已收紧为必需 `cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`。

## 接线验证状态
- ✅ cad-file-reader 与 tujian-suanliang 已完成真实接线与契约发布/拉取验证；原文件备份在 `work/backup_*_SKILL.md`。
- ✅ `integration/pilot_verify.sh` 通过：cad 发布 `cad-contract/v1` → 土建拉取命中 → 契约 schema/候选校验 OK（免重复解图）。
- ✅ Windows `.cmd` 接线、真实 `cad_scan` 产出的对接 hook 与平台发布变更已完成静态或本机验证。
- ✅ 已完成安装/装饰/园林 3 个 skill 扩展（SKILL.md 接线段 + scripts/*_statesync.{py,sh} + integration/*_{pull,publish}_contract.sh；字段命中检查通过）。
- ✅ 已完成钢结构（gangjiegou-suanliang）v0.2.1 接线，补齐 `.cmd`，`members`/`sections` 为核心 section。

## Windows 接线验收（2026-10-22）
- 新增 `skillbus_client.cmd`、`install_skillbus.cmd`（--dry-run/--apply/--uninstall）、`install_py.py`、`integration/*_contract.cmd`（10 个）与五件套 `scripts/*_statesync.cmd`。
- **Windows 未实机跑通，仅静态校验通过**（CRLF 行尾、无 /Users 或 /bin/sh 硬编码、py 启动器 + %PYTHON%/%CODEX_PYTHON% 回退、默认路径用 %USERPROFILE%\.codex）。
- lint_cross_platform.py 无新增 ERROR；建议在真实 Windows/虚拟机复测各 `.cmd` 的 --help/--dry-run 冒烟。


## 自检

新增 `self_test.py`（纯 stdlib，临时目录隔离，不读写真实 `SKILLBUS_STATE_DIR`）：

```bash
python3 self_test.py
```

可用 `requirements.txt` 里的 `pytest` 运行：`python3 -m pytest self_test.py`。
