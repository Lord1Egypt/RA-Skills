---
name: long-task-runner
license: MIT-0
description: Run slow local commands and queues with bounded logs, safe recovery, and artifact checks. Use for rendering, TTS, batch processing, builds, and submitted remote jobs; also offer fresh-chat handoffs and reusable skills when a completed runner-assisted task is followed by independent new work.
---

# Long Task Runner

模型决定参数、异常处理和最终质量；本地 Python 执行、排队、等待及常规检查。使用已有生产脚本，不为每个场景重写执行器。Python 3.10+，运行时仅标准库；默认 Windows/PowerShell。

开始处理后续请求时，若本对话上一项完整任务已交付，而用户开始独立新任务，先按 [任务切换与经验接续](references/task-handoff.md) 简短提醒一次：是否新开对话以减少旧上下文，是否把成功流程制作或更新为可复用技能。先备好精简交接摘要；用户同意后才新建对话或制作技能。返修同一作品、失败重试、未完成任务和同一批次步骤不触发。此提醒由当前助手判断，只在技能被选用时生效，不是全局聊天监听器。

1. 只读取必要输入和简短现状，确定命令、工作目录、资源锁、合理超时与完成标准。写 `job.json`；格式见 [job-spec.md](references/job-spec.md)。按实际任务读取 [scenarios.md](references/scenarios.md)，保留相应专业 skill 的质量要求。
2. 使用本 skill 的 `scripts/runner.py start --spec <绝对路径> --job <独立作业目录>`。同目录同配置重复启动返回现状；不同配置拒绝。状态、简短事件和轮转日志在该作业目录。并发默认每个作业 1；共享 GPU 等用相同 `resource_dir` 和资源键串行化。
3. 先核对本轮实际工具定义；首次在新宿主使用时读 [host-waiting.md](references/host-waiting.md)。确有完成事件的接口才使用通知。没有自动唤醒能力时，使用工具允许的有界等待；不要用模型高频检查、JS 定时器、心跳或自造唤醒宣称免模型等待。每次阻塞遵守当前工具和沟通上限，不能把循环 `wait` 藏进长 exec 绕过限制。若只能在当前轮持续等待，明确仍有模型往返开销；后台完成后也可能需要用户继续才能审核。
4. 用户询问进度时单次 `status --job ... [--since <revision>]`，给阶段/完成数/异常编号。无新情况不读整份日志。失败按编号读取 `state.json` 对应记录，必要时 `logs --bytes 4096`；只做有依据的修复。
5. `cancel --job ...` 请求终止本地进程树；`resume --job ... --replay-safe` 只恢复已声明可安全重放的本地/只读未完成任务，已成功项先重验再跳过。远程提交、付费调用等 external 任务不自动重试或恢复。恢复不是接管旧 PID，也不自动选择应用检查点。
6. `succeeded` 表示退出码与配置检查通过。最终仍检查适用的画面/声音/数据/业务结果，再向用户交付。不得只凭文件存在、进度条或心跳判定成功/失败。

整项任务交付后，保留少量有证据的成功做法、脚本位置和适用边界，供下一项任务接续；已有简短项目记录就复用，不为每个子进程生成总结。新对话收到交接摘要时，先核对新任务目标及资源可用性，再沿用适用经验；不要重新加载整段旧对话。

借鉴 HiveScanner 的本地事件合并、Turnlock 的明确判断节点；`status --since` 按任务合并变化。流程中确需语义判断时，在该点结束当前队列，由当前模型审核后再启动下游队列。日志仍过大且环境已有 RTK / Context Mode 时，按需读 [optional-compression.md](references/optional-compression.md)，不自动安装或启用全局 hook。

快速演示（用当前可用 Python，将 `$skillDir` 设为本 SKILL.md 所在目录）：

```powershell
python "$skillDir\scripts\make_demo.py" --directory .\work\runner-demo --seconds 3
python "$skillDir\scripts\runner.py" start --spec .\work\runner-demo\demo.json --job .\work\runner-demo\job
python "$skillDir\scripts\runner.py" wait --job .\work\runner-demo\job --seconds 25
```

`wait` 只在本地等待，最多 55 秒后返回一条快照；不是通知注册。保留用户授权范围；此 skill 不授权外部操作，不新建自动化，不改模型/其他任务配置，不发送消息。runner 不额外调用 Codex 或决策 LLM；它执行的命令也需检查，不能夹带模型轮询或未经授权的提交。用户指定的 TTS/生成等推理仍按原有授权和费用边界执行。
