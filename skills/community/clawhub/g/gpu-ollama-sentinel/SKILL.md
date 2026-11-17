---
name: "gpu-ollama-sentinel"
description: "Watches NVIDIA GPU and local Ollama health for always-on boxes and GPU earning workers — checks Ollama API, GPU util and VRAM via nvidia-smi, auto-restarts Ollama on failure, appends JSON status logs. Built from real Windows 24-7 operations experience"
---

# GPU / Ollama Sentinel

一句话：给"挂着挣钱/常驻跑服务"的 Windows 机器装一个心脏监护仪——Ollama 挂了自动救活，GPU 异常留痕报警。

## 为什么需要它

常驻 GPU 推理（本地 Agent、GPU 挂机、自动化工作流）最常见的三种静默死亡：

1. **Ollama 进程消失**——Agent 还在跑，每次推理都超时，浪费时长且任务失败
2. **显存被占满僵死**——进程活着但永远 OOM，表现为"显存不动了"
3. **驱动/温度异常**——长跑几天后性能骤降，没人发现

本技能的 watchdog 脚本每 N 分钟跑一次，发现前两种直接自动处置并写 JSON 日志。

## 安装

1. 把本 skill 目录复制到 Agent 可访问的路径（示例用 `C:\Tools\gpu-ollama-sentinel`）
2. （可选）建 Windows 计划任务每 5 分钟跑一次：

```powershell
schtasks /Create /TN "GpuOllamaSentinel" /SC MINUTE /MO 5 /TR ^
 "powershell -NoProfile -ExecutionPolicy Bypass -File C:\Tools\gpu-ollama-sentinel\scripts\watchdog.ps1" /F
```

> 计划任务方式不受"父进程退出回收"影响，是 Windows 上最可靠的常驻姿势。

## 用法

```powershell
# 单次体检（人也能跑，直接看结论）
powershell -File scripts\watchdog.ps1

# 修改判定阈值
powershell -File scripts\watchdog.ps1 -MinFreeVramMB 2000 -OllamaUrl http://127.0.0.1:11434

# 只体检不自动修复（观察模式）
powershell -File scripts\watchdog.ps1 -NoHeal
```

## watchdog.ps1 做什么

| 检查项 | 判定 | 自动处置 |
|---|---|---|
| Ollama `/api/tags` 响应 | >5s 无响应=死亡 | 按 `-HealCommand` 配置的命令重启（默认 `ollama serve`） |
| Ollama 模型列表 | 空=异常 | 只记录，不乱动 |
| GPU 显存/利用率（nvidia-smi） | 空闲显存 < 阈值且利用率≈0 = 疑似僵死 | 记录 top 占用进程名单，供人工决策（不擅自杀进程） |
| 上述全部结果 | — | 追加写入 `sentinel-log.jsonl`（一行一条 JSON，好分析） |

## 日志示例

```json
{"ts":"2026-10-29T16:40:00","ollama":"up","models":7,"gpu_free_mb":10123,"gpu_util_pct":3,"action":"none"}
{"ts":"2026-10-29T16:45:00","ollama":"down","action":"restart_ollama","result":"ok"}
```

## 设计原则（来自实战）

- **能自愈的自动自愈，不能自愈的绝不擅自杀进程**——宁可留下证据让人确认，也不误杀生产任务
- 全部输出 JSONL，方便 Agent 或人 grep/分析
- 单文件、零第三方依赖（PowerShell 原生 + nvidia-smi），拷过去就能跑

## 适用人群

- 用本机 Ollama 挂 GPU 挣钱/跑任务的（掉线=白烧电）
- 常驻跑本地 Agent 的（飞书/TG 机器人背后的推理不能死）
- 任何"装完三天崩"的 Windows AI 环境受害者
