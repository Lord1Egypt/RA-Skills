# Long Task Runner

本 ClawHub 分发版本采用 MIT-0；GitHub 主仓库仍为 MIT。源提交：3e267399cc5db606556ecbd0ec8b3746429b790b。

[English](README.md) · [MIT-0 开源协议](LICENSE)

让本地 Python 执行耗时任务、排队、等待和常规验证，让模型负责参数、异常决策与最终审核。默认 Windows / PowerShell，Python 3.10+，核心仅使用标准库。

适用于视频生成/渲染，Blender 等 3D 渲染、烘焙、模拟，本地 TTS，ASR/字幕，OCR/文档转换，转码、下载、依赖安装、编译/长测试、训练评测、ETL、向量索引、科学仿真、备份及已提交远程作业。

## 安装与调用

```sh
npx skills add dhzyw/long-task-runner --skill long-task-runner --agent codex
```

或将仓库克隆到 Codex 支持的个人技能目录；已有同名安装时不要再装第二份：

```powershell
git clone https://github.com/dhzyw/long-task-runner.git "$env:USERPROFILE\.agents\skills\long-task-runner"
```

在 Codex 中说：

> 使用 $long-task-runner 执行这批渲染，沿用现有脚本与已确认参数，本地等待、限制日志，完成后验证产物。

仓库内可跑无网络、无模型调用的廉价演示：

```powershell
python scripts/make_demo.py --directory ./work/demo --seconds 3
python scripts/runner.py start --spec ./work/demo/demo.json --job ./work/demo/job
python scripts/runner.py wait --job ./work/demo/job --seconds 25
```

## 新任务提醒与经验接续

完成上一项工作后，如果在同一对话开始独立新任务，技能会提醒一次：是否新开对话以减少旧上下文，以及是否把成功流程制作或更新为可复用技能。返修同一作品、失败重试和未完成批次不会触发；选择继续原对话后不会为同一任务重复提醒。

新对话携带精简交接摘要：已验证做法、脚本位置、用户偏好和验收标准；不复制整个聊天历史。用户确认后才新建对话或制作技能，没有新建工具时提供可复制的开场提示。两项选择互相独立。

这是技能被选用后的助手行为，不是全局对话监听器，不保证所有聊天自动触发，也不承诺具体 token 节省比例。详见[任务切换指引](references/task-handoff.md)与[交接模板](assets/task-handoff-template.md)。

## 有用的接口

每个命令都指定 `--job <独立作业目录>`。

| 接口 | 作用 |
|---|---|
| `start --spec ...` | 冻结配置并启动隐藏 worker；同配置重复启动不重跑 |
| `status [--since revision]` | 一次简短快照；按任务合并变化 |
| `wait --seconds 25` | 本地有界等待，单次上限 55 秒 |
| `cancel` | 请求清理本地子进程树，之后确认终态 |
| `resume --replay-safe` | 只恢复声明可安全重放的任务，已成功项先重验再跳过 |
| `logs --bytes 4096` | 必要时读取有界日志尾部 |

默认不重试。自动重试还需允许的非零退出码、幂等声明、次数与退避条件；超时与验证失败不自动重放。外部提交和付费操作禁止自动恢复。远程 watcher 只查询已知作业 ID，本地取消不会取消远程费用。

## 等待与质量边界

本地 worker 不额外调用决策模型，但**后台运行不等于自动唤醒 Codex**。须检查实际宿主的工具支持。没有真实完成通知时，当前轮持续等待仍会产生模型往返，不能承诺零 token。

成功需同时满足退出状态和适用的产物断言，不能只看文件存在。检查包括 JSON、完整 WAV、SHA-256 和只读验证器；可选媒体助手使用现有 ffprobe/FFmpeg 检查音画轨、尺寸、时长与完整解码。最终画面、声音和业务质量仍需审核。

Windows Job Object 的进程树清理经过测试；macOS/Linux 崩溃恢复仅实验性支持，不保证同等行为。CPU/RAM/GPU 用应用参数限制，runner 没有硬资源配额。配置散列不包含输入和脚本内容，输入变更要用新作业目录。

## 验证

```powershell
python scripts/test_runner.py --root ./work/tests --report ./work/runner-tests.json
python scripts/test_remote.py --root ./work/tests --report ./work/remote-tests.json
python scripts/benchmark.py --directory ./work/benchmarks --report ./work/benchmark.json --seconds 6
```

初次 Windows 验收：36 项进程测试和 8 项本地 HTTP 测试通过。发布版结果以 [GitHub Actions](https://github.com/dhzyw/long-task-runner/actions) 为准。

一次 6 秒模拟任务中，每秒查状态为 8 次 CLI 调用、5,265 字节；有界等待为 2 次、1,434 字节。两种方式均在本地程序内测量，这是接口次数和返回字节，**不是模型 API 请求数或 token 节省率**。

[配置说明](references/job-spec.md) · [场景表](references/scenarios.md) · [宿主限制](references/host-waiting.md) · [按需压缩](references/optional-compression.md)
