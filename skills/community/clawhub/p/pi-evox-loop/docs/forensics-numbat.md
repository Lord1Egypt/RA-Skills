# 独立取证 PoC：numbat × PiEvoX（2026-10-13）

> **EN**: Read-only forensic PoC with [numbat](https://github.com/perplexityai/numbat) (Perplexity, Apache-2.0, methodology credit). `agents` discovers Claude Code/OpenClaw/Pi/Hermes; `scan` reads artifacts with 0 findings baseline; `timeline --agent openclaw` reconstructs historical sessions with file:line evidence per event. Coverage limit: live sessions live in SQLite/WAL (deferred upstream). Next step: cross-check injected genes against the reconstructed timeline as an independent evidence source.


> 目标（见 [`docs/advanced.md`](docs/advanced.md)「独立取证」节）：用第三方审计器对 agent 会话做**只读取证重建**，
> 为「注入的基因是否真的体现在 agent 后续命令里」提供 register-hit（self-report）之外的**独立证据源**。
> 方法论致谢：[numbat](https://github.com/perplexityai/numbat)（Perplexity AI，Apache-2.0）。

## 1. 环境
- 自有 Linux 节点装 numbat **v0.2.0**（Go 单二进制，`~/numbat/numbat`，release 直下 linux_amd64 tar.gz 6.7MB）。
- 免安装免配置——与 SKILL.md「30 秒上手」同级的零门槛。

## 2. `numbat agents`（发现）
| AGENT | CONFIG | ARTIFACTS | LIVE | WIRED | 备注 |
|---|---|---|---|---|---|
| Claude Code | yes | none found | hooks | no | 未装 |
| **OpenClaw** | yes | **found transcripts** | plugin | no | **可解析**；SQLite/WAL sessions 在 2026.7.2 beta 线延后 |
| Pi | yes | none found | plugin | no | 未装 |
| Hermes | yes | n/a（hook-only；state.db SQLite/WAL 延后） | hooks | no | 未装 |

## 3. `numbat scan`（只读扫描）
```
scan complete: 2 discovered, 2 parsed, 0 findings   （run-20261013T130427…）
```
- 基线健康：现有可解析产物 **0 findings**（51 条规则全空）。
- ⚠️ 覆盖限制：仅 2 个 artifacts 可扫——**活跃会话在 SQLite/WAL 里，当前版本延后解析**（OpenClaw 2026.7.2 beta 线）。取证重建对活跃期会话暂不可用，对 reset/归档的 jsonl 会话可用。

## 4. `numbat timeline --agent openclaw`（取证重建）
- 成功重建一个 OpenClaw agent 的历史会话（2026-08-21，99 events）：
  `prompt.user` / `tool.call` / `command.exec` / `command.result` 全时间线，**每条挂 原始文件:行号** 可回查。
- 实测样例：一次「token 消耗统计」任务里 agent 连续 `ls/logs`、`find *.db`、三条 `sqlite3 …` 探测命令全部按序重建——**这就是对账素材**。

## 5. 集成路线（0.20+）
1. **对靶核对**：`evolver-recall --query` 注入基因 G 后，用 `numbat timeline` 抓取该时间窗的 `command.exec` 序列，grep G.strategy 中的关键命令/参数——命中即**独立证据 hit**（不依赖 `--register-hit` 自报）。
2. **前置条件**：活跃会话（SQLite/WAL）解析需等 numbat 上游支持（关注 releases）；或改用 OpenClaw hook 通道（`numbat hook install --agent openclaw`，但那是写路径，需另行评估）。
3. **隐私边界**：numbat 自带 redact 默认脱敏（密钥掩码）；但 timeline 本身含任务内容——仅限自有设备本地使用，不外发。

## 6. 结论
- PoC **成功**：发现/扫描/timeline 三命令全部跑通，OpenClaw jsonl 会话可取证重建。
- 现阶段价值：**历史会话审计** + 「agent 到底干了什么」的独立视角。
- 下一步（0.20）：等 SQLite/WAL 支持或接 hook 通道，然后做基因有效性的 timeline 对靶核对。
