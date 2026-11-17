# 宿主等待边界

此包在 2026-09-08 的 Windows 10.0.26200 / Codex Desktop CLI 0.153.4、Python 3.14.3 上验收。日期/工具版本会变化；每次优先服从当前工具定义，不把此处参数当成权限扩展。

事实层次须分清：

1. **本地等待**：worker 内的 subprocess 等待、资源锁、退避和 HTTP GET 轮询不调用模型。后台线程、Python sleep、JS setTimeout 都只影响本地执行，不注册 Codex 唤醒。
2. **单次工具挂起**：一个 await 在返回前无需模型再读进度；超过 yield 窗口，外层工具可能返回 session/cell ID。接着调用 wait 是一次新的模型发起工具往返。不能仅凭 await 很长就说整个长任务没有模型重入。
3. **完成事件**：必须是当前工具公开提供并验证可达当前任务的完成通知；某个 API 的输出流/OS 提示音/状态文件更新不等于助手自动继续。不得暗中调用 Codex/其他模型 API、创建定时器任务或 heartbeat 来冒充宿主原生通知。

本次可调用接口及实测：

| 接口 | 证据与用法 |
|---|---|
| exec_command | Windows 实际最早约 10 秒返回；有效 yield_time_ms 10000–30000。12 秒静默命令先返回 session ID，之后用 write_stdin 才读到完成；无已验证的任意本地 worker 自动唤醒本任务能力 |
| write_stdin | 仅用于 exec 返回的实际 session_id；空输入可阻塞等输出/退出。按本轮沟通要求选择 ≤55 秒，不用默认/最大 300 秒超过允许等待边界 |
| functions.exec / functions.wait | exec 可保持 awaited promise，或先返回 `Script running with cell ID`；只有后者才能调用 functions.wait。wait 只接其 cell ID，不能混用进程 session_id；未 await 的 promise 会随 isolate 结束被丢弃 |
| wait_threads | 等待已有 Codex 任务终态，不接本地 PID/runner 作业 ID。不能为本地任务等待而擅自创建一个新 Codex 任务 |
| app-server | 官方协议有 command/exec 输出事件；这不证明当前助手拥有连接任意 worker 完成事件并唤醒的工具。此包只用 initialize/skills/list 做只读安装验证，没有新增宿主桥接服务 |

可执行退路：

- 预计当前窗口内完成：start 后用一次 `runner.py wait --seconds 25`，调用 exec_command 时可用 yield_time_ms=30000，通常仅返回终态。普通多分钟以上任务保持 worker 独立运行，在有用的准备/检查工作结束后再等。
- 工具给出 session ID：用一次适当窗口的 write_stdin 等待该 waiter 退出。如果结果是 runner wait 的“仍运行”（退出码 3），worker 仍继续；需要下一窗口时再启动有界 wait，不以读取大日志代替等待。
- 用户要求本轮完成：遵守当前持续工作及沟通要求，使用允许的窗口继续等到终态再审核。坦白仍有模型往返；不能用一个包住无限循环的 functions.exec 绕过 60 秒沟通/等待约束，也不能保证零 token。
- 用户已接受后台交付：可在交代作业目录、状态命令和当前限制后结束本轮；没有真实唤醒时，完成后由用户“继续/查进度”触发一次读取和审核。不得把“任务还在后台”报告成制作完成。
- 若未来宿主工具确有 completion callback/event：先用 2–15 秒廉价任务验证事件到达与后台生存，再利用它；记录工具名称、调用/事件数量、返回字节与异常通知，不套用本次不支持的结论。

测量时分开记录模型工具往返、工具内部本地循环次数、输出字节、墙钟时间。有 usage 日志才报告 token；不以字符数乘常数伪造 token。函数调用次数不等于计费模型请求数。性能测量应区分必要修复与等待，缓存不能算全价输入；不要许诺未经对照测试的节省比例。

安装发现：[官方技能文档](https://learn.chatgpt.com/docs/build-skills)描述自动发现与 `$HOME/.agents/skills`；本机 [app-server skills/list](https://learn.chatgpt.com/docs/app-server) 实际也返回 `$HOME/.codex/skills` 的 user 技能，因此使用已核实的 `$CODEX_HOME/skills`（CODEX_HOME 未设时回退用户主目录下的 .codex/skills）。只装一份，保留自动选择默认值。当前任务技能目录可能是旧快照；其他任务扫描即可发现，UI 未刷新时按官方说明重启应用，不修改全局配置。
