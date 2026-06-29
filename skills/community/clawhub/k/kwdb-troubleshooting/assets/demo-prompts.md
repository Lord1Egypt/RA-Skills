# Demo Prompts

- 请根据 `/var/lib/kaiwudb/logs` 下的 `errlog`，给出这次 KWDB 宕机的通用诊断报告。
- 用户说“下午 2 点半 OOM”，但请你先 grep `messages`、`syslog` 或 `dmesg` 里的 `oom` 和 `kwbase`，确认是否是 `kwbase` 被 OOM kill，再输出通用诊断报告。
- 我抓到一段 `W270101` 日志，请结合上下文和源码给出故障定位结果；如果源码证据不足，不要猜 commit。
- 这是一次性能问题，用户已经提供慢 SQL。请直接用 `EXPLAIN ANALYZE` 定位瓶颈，并输出通用诊断报告。
- 这是一次性能问题，但还没有明确慢 SQL。请先调用 `kwdb-mcp-server` 的 `query-metrics-history` 工具判断是 CPU、IO、内存还是慢 SQL，再输出通用诊断报告。
- 我只给你一段 E26 日志，没有源码。请停在证据结论，不要扩展到源码定位。
- 请把这次诊断结果按固定七段测试单格式输出。
