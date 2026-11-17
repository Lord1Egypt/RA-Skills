# 配置与接口（需要创建/修复作业时读取）

一个核心 `scripts/runner.py`，所有普通工作用 argv 适配。路径例子需换成本机真实绝对路径；先用 `make_demo.py` 可生成可运行配置。JSON 使用 UTF-8，可带 BOM；未知字段拒绝。

```json
{
  "version": 1,
  "name": "render-and-check",
  "total_timeout_s": 7200,
  "log_bytes": 262144,
  "min_free_bytes": 1073741824,
  "resources": ["gpu0"],
  "tasks": [{
    "id": "render",
    "argv": ["C:\\Python\\python.exe", "D:\\project\\scripts\\render.py"],
    "cwd": "D:\\project",
    "timeout_s": 7000,
    "effect": "local",
    "replay_safe": true,
    "launch_limit": 3,
    "retry": {"max_attempts": 1, "exit_codes": [], "delay_s": 5},
    "env": {"OMP_NUM_THREADS": "4"},
    "artifacts": [{"kind": "json", "path": "render-report.json", "equals": {"ok": true}}]
  }]
}
```

`argv` 不经 shell 拼接，无字符串插值。使用实际 exe 路径；`.cmd/.bat` 需另经已审核的 PowerShell `-File` 脚本调用，不能把参数随意拼成 shell 命令。命令必须前台运行到工作完成，不得启动服务/守护进程后提前退出。stdin 关闭；预先提供非交互参数，安装器不能等 GUI 确认。

字段与限制：

| 字段 | 行为 |
|---|---|
| tasks | 顺序队列 1–1000 项；任一失败即停止；跨作业可并发 |
| cwd / timeout_s | 每任务必填；绝对存在目录 / 单次主命令墙钟超时 0.1 秒–30 天；静默不触发失败 |
| total_timeout_s | 每次启动/恢复的总预算，含资源等待、重试和验证，默认 24 小时，上限 30 天；不是跨恢复累计 SLA |
| resources / resource_dir | 最多 16 个排他锁键；默认同用户系统临时目录 `long-task-runner-resources`，跨任务共享。可指定同一个绝对本地路径；不是分布式锁。锁不会限制不使用 runner 的进程 |
| min_free_bytes | 每个未完成主任务开始前检查 cwd 所在盘；默认 0；不等于持续磁盘配额，其他产物盘另验 |
| effect | 必填 `local`、`read_only`、`external`。本地写文件也须自行判断能否重复；HTTP POST、收费、提交发布通常 external |
| replay_safe | 默认 false。true 是对命令的实际幂等承诺；程序不会证明幂等。external 禁止设 true |
| retry | 默认一次。仅声明安全且退出码命中非零允许表才自动重试；最多 5 次、指数退避，延迟最高 3600 秒；超时、验证失败、未知退出码不自动重试 |
| launch_limit | 同一任务累计主命令启动次数，默认 3，最大 20；包括恢复。每个作业最多 6 代，拒绝无限重试 |
| env | 最多 64 个字符串覆盖；默认继承启动时环境。不要写令牌、密码或带令牌 URL：冻结配置会落盘；凭证通过既有环境/工具凭证机制 |
| log_bytes | 每段合并 stdout/stderr 日志大小，默认 256 KiB，范围 1 KiB–16 MiB，当前段+2 个备份；事件另限 64 KiB×2。预算不包含应用自行写出的日志与产物 |

CPU/RAM/GPU 用应用自身参数（线程数、batch size、设备、分辨率等）限制；runner 只提供顺序队列、排他锁、时限和磁盘预检，没有硬内存/显存配额。Windows worker 崩溃由 Job Object 关闭清理子树；正常结束也清理遗留子进程。不支持用它托管常驻服务。锁文件与状态目录保留，不按 PID 文件判断占用，不主动删除旧作业。

产物检查是组合的：先要求退出码 0，再要求全部 checks 通过。每任务最多 100 项。没有产物的编译/测试命令需写 `success_basis`，解释其退出码为何足以作为程序完成信号；不要用“exit 0”包装吞掉真实失败。

| kind | 参数与验证 |
|---|---|
| file | `path`, `min_bytes` 默认 1；仅弱检查，正式媒体不要单独用它 |
| json | 解析至多 8 MiB 对象；`required` 顶层键数组；`equals` 顶层键值精确匹配 |
| wav | PCM/WAVE 可读、数据未截断，`min_duration_s` / `max_duration_s`；不证明发音、响度或语义质量 |
| sha256 | `sha256` 完整预期散列，流式计算；适合下载/备份固定文件 |
| command | 已审核的只读 `argv`、`timeout_s`（≤300）、`read_only: true`，验证器必须用退出码表达断言失败。长验证应列作单独队列任务 |

除 command 外 `path` 相对 cwd 或绝对；默认 `fresh: true` 要求此次执行前后的大小/mtime_ns 不同，防止旧产物冒充成功；这不是内容溯源或防篡改保证。确实复用已有缓存时可设 false，并配散列/业务校验。成功任务在部分作业恢复时重新检查格式/语义（不重新要求 freshness），再跳过；失效报 `E_COMPLETED_INVALID`，不会静默重做。

接口均需 `--job <独立绝对目录>`：

| 命令 | 语义 |
|---|---|
| start --spec … | 冻结配置、启动隐藏 worker，立即返回。相同 JSON 配置幂等；不同配置拒绝。散列只涵盖配置，不包含脚本/输入内容；输入更新应建新作业，不能复用旧成功状态 |
| status [--since revision] | 一次紧凑快照，无日志全文；revision 只随事件变化；指定 since 后按任务合并最新变化，最多 4 组。内部只保留 16 条变化，有截断标志；终态、失败总数/最近失败与产物另存，不靠增量历史证明成功；不是百分比；starting 无 worker 超过 10 秒显示 interrupted |
| wait --seconds 25 | 本地等待终态，或窗口到期；0–55 秒，默认 25；返回一条快照；退出码 0 成功、2 失败/中断、3 仍运行。其他有效查询/控制命令退出 0，不表示作业成功 |
| cancel | 写取消请求，由 worker 清理整个本地子树；返回 `cancel_requested` 不是“已取消”，等待终态确认。远程计算不受此命令影响 |
| resume --replay-safe | 取得控制锁，确认旧 worker 锁释放；保留成功项。已启动未成功项需 replay_safe 且非 external；仍活跃/已全部成功则返回现状。应用检查点路径需原命令显式处理 |
| logs --bytes 4096 | 只读当前日志尾部，最大 16384 字节；可能包含子命令打印的敏感数据，按需读取和引用 |

文件：`spec.json` 冻结配置，`state.json` 当前完整状态/失败编号/各项尝试记录及最近 32 次失败历史，`events.jsonl[.1]` 变化，`process.log[.1/.2]` 有界日志，内核锁和 `cancel.json`。结果列表默认截至 8 项，更多看 state 对应字段。CLI 状态强制 UTF-8；原始子命令日志按字节保存，`logs` 以 UTF-8 容错预览。状态文件原子替换；断电/磁盘损坏不保证持久化，检查异常后再恢复。不要手改运行中的 spec/state。POSIX 只提供正常运行时的进程组清理，worker 崩溃后不保证子树退出，拒绝直接恢复活跃遗留状态；需人工确认清理后新建作业。本机完整验收针对 Windows。

远程作业：先在已获授权的提交步骤拿到可靠 job ID 并持久化，再将查询阶段交给 `remote_watch.py --url <状态接口> --job-id <已知ID> --output <结果JSON>`，作为 effect=read_only 的普通队列命令。默认 GET 每 15 秒、允许 3 次连续临时读取错误，状态/ID 不符则失败；可设置状态组和顶层键名。令牌用 `--token-env VARIABLE_NAME`；拒绝重定向、明文非本地 HTTP。无提交、自动重新提交或远程取消功能。未知提交结果先与供应商核对，不因本地无文件就再付费。监听器终态 JSON 还需业务/下载产物验证；只读轮询频率也应符合服务限流约定。
