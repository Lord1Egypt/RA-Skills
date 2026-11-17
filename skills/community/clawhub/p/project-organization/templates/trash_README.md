# .trash — 软删除暂存

本项目根内**"删除"文件一律先移入此处，不得直接硬删**（遵守 AGENTS.md「文件删除铁律」）。

由 `scripts/trash.py` 管理：

| 动作 | 命令 | 说明 |
|------|------|------|
| 移入 | `python <skills>/project-organization/scripts/trash.py put <路径> --reason "..."` | 默认只预演，加 `--apply` 执行 |
| 查看 | `python .../trash.py list` | 列出暂存条目 |
| 恢复 | `python .../trash.py restore --id <条目> --apply` | 还原到原路径 |
| 清空 | `python .../trash.py purge --id <条目> --confirm` | 彻底删除（需用户确认） |

条目结构：`.trash/<时间戳>__<原名>/`，内含被移入的文件/目录 + `_manifest.json`（记录原路径、原因、时间）。
