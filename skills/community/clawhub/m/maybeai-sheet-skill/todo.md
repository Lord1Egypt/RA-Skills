# maybeai-sheet-skill TODO

评分：`7/10`

结论：这个 skill 的可用性明显强于 `finclaw-report-analysis`。它有 `agents/openai.yaml`、脚本样例、较完整的 API 覆盖和比较清楚的触发描述。但它最大的问题也很明显：`SKILL.md` 已经膨胀成 1200+ 行的 API 手册，不再像一个 skill，而像整份产品文档。

## P0

- [ ] 把 `SKILL.md` 从完整 API reference 缩成 skill 入口，目标是保留：何时使用、常见任务路由、worksheet targeting rule、关键注意事项、脚本导航。
- [ ] 将大段 endpoint 文档拆到 `references/`，按主题分文件，例如 `references/file-management.md`、`references/read-write.md`、`references/formulas-sql.md`、`references/charts-formatting.md`。
- [ ] 将当前 1200+ 行主文档控制到更接近最佳实践建议的规模，避免 skill 一触发就吞掉大量上下文。

## P1

- [ ] 给拆分后的长 reference 增加目录。
- [ ] 把“选择哪个 API”的决策逻辑保留在主 `SKILL.md`，把具体请求体和大样例移到 `references/`。
- [ ] 把最常用的 5-10 个任务抽成更短的“agent-safe playbook”，例如上传、读表、按 key 更新、保留表头覆盖、追加行、SQL 结果表、导出。
- [ ] 检查并删除重复说明，比如同一 endpoint 的用途、认证、参数在不同段落多次解释。

## P2

- [ ] 删除 `README.md`，或至少确认该仓库是否真的需要它；按 skill best practice，额外说明文档通常应避免。
- [ ] 清理无关文件，例如 `.DS_Store`。
- [ ] 复核 frontmatter 中扩展字段是否都必要；如果运行时不会消费，尽量减少噪音。
- [ ] 增加一页“错误与恢复” reference，集中说明常见失败模式、鉴权问题、sheet targeting 错误、格式化与数据写入分离等边界。

## 可保留的优点

- [ ] 保留 `agents/openai.yaml`，这是当前目录里做得对的一项。
- [ ] 保留 `scripts/` 的 curl 示例，它们是很好的低自由度执行资产。
- [ ] 保留 `SKILL.md` 中对 `sheet-dashboard` 的边界说明，这有助于避免职责混叠。
- [ ] 保留“Choosing the right write API”这类高价值决策层内容，但应压缩并前置。
