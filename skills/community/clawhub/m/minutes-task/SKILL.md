---
name: minutes-scheduled-task
description: 当用户需要"每 N 分钟"（如每10分钟、每5分钟）定时执行任务时使用。WorkBuddy 内置调度器仅支持 DAILY/HOURLY/WEEKLY/MONTHLY/YEARLY 且忽略 BYMINUTE，必须改用 Windows 任务计划程序 + 独立脚本实现分钟级调度。
version: 1.2.0
agent_created: true
category: productivity
---

# Windows 分钟级定时任务（Agent 执行手册）

## 何时使用
用户提出"每 N 分钟执行一次"的定时需求（如：每 10 分钟推送微博热搜、每 5 分钟检查邮箱、每 30 分钟备份文件）。此时**不要**创建 WorkBuddy 内置自动化（见下方核心事实），改用本方案。

## 核心事实（2026-08 实测，不要重复验证）
1. WorkBuddy 自动化调度器 RRULE 只支持 `DAILY / HOURLY / WEEKLY / MONTHLY / YEARLY`
2. `FREQ=MINUTELY` 创建时直接报错 `Unsupported RRULE frequency`
3. `FREQ=HOURLY;BYMINUTE=0,10,20,30,40,50` 可创建但 **BYMINUTE 被忽略**，next_run_at 全部被解析为"创建时间+1小时" → 每小时只触发 1 次
4. 结论：分钟级调度必须用 **Windows 任务计划程序 + 独立脚本**

## 执行流程（Agent 全自动完成，用户无需动手）

### Step 1：确认需求
向用户确认两件事（若已明确可跳过）：
1. **任务内容**：每分钟要执行什么？（如"抓取微博热搜发飞书"）
2. **间隔分钟数**：N = 几？（如 10、5、30）

### Step 2：生成脚本
在工作目录创建 `<task_name>.py`（任务名用小写英文+下划线，如 `weibo_hot_push.py`），脚本结构如下：

```python
# -*- coding: utf-8 -*-
import json, os, subprocess, sys, urllib.request
from datetime import datetime

TASK_NAME = "<task_name>"  # 任务名，用于日志识别
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), TASK_NAME + ".log")

def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def do_work():
    """写入用户的业务逻辑。返回 True=成功, False=失败。"""
    # 在此实现具体任务（抓数据/发消息/处理文件）
    # 失败时抛异常或返回 False
    return True

def main():
    log("=== 任务开始 ===")
    try:
        ok = do_work()
    except Exception as e:
        log(f"失败: {e}")
        ok = False
    log("=== 任务结束 " + ("成功" if ok else "失败") + " ===")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
```

**要点**：
- 用绝对路径定位 python 解释器（如 `C:/Users/<user>/.workbuddy/binaries/python/versions/3.13.12/python.exe`），避免 PATH 差异
- 日志写入脚本同目录 `.log`，用于事后验证运行次数
- 业务逻辑集中在 `do_work()`，失败要有日志与返回码

### Step 3：测试脚本
前台运行一次脚本，确认 `=== 任务结束 成功 ===` 且无报错：
```
<python绝对路径> <脚本绝对路径>
```

### Step 4：注册 Windows 计划任务
用 PowerShell 执行（`<间隔分钟>` 填 N，`<任务名>` 用 `myapp-10min` 格式）：

```powershell
$python = '<python绝对路径>'
$script = '<脚本绝对路径>'
$workDir = '<脚本所在目录>'

$action = New-ScheduledTaskAction -Execute $python -Argument ('"{0}"' -f $script) -WorkingDirectory $workDir
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes <间隔分钟>) -RepetitionDuration (New-TimeSpan -Days 365)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "<任务名>-<间隔分钟>min" -Action $action -Trigger $trigger -Settings $settings -Description '<任务描述>' -Force
```

**首次运行在 1 分钟后**，之后每 N 分钟一次。

### Step 5：验证
1. `Get-ScheduledTask -TaskName "<任务名>-<间隔分钟>min"` → State 应为 `Ready`
2. `Get-ScheduledTaskInfo -TaskName "<任务名>-<间隔分钟>min"` → 记录 LastRunTime / NextRunTime
3. 等待首次触发后，检查脚本 `.log` 出现新的"任务开始/结束"记录
4. 向用户确认：任务已创建，每 N 分钟运行一次，首次运行时间

### 任务生命周期管理
- **修改间隔**：删除后重建（`Unregister-ScheduledTask -TaskName X -Confirm:$false`，再走 Step 4）
- **暂停**：`Disable-ScheduledTask -TaskName X`（保留定义，可恢复）
- **恢复**：`Enable-ScheduledTask -TaskName X`
- **彻底删除**：`Unregister-ScheduledTask -TaskName X -Confirm:$false`

## 不影响其他定时任务（重要）
- Windows 计划任务与 WorkBuddy 内置自动化是**两套独立系统**，并行互不干扰
- 每个计划任务必须有**唯一任务名**，命名规范 `<业务>-<间隔>min`（如 `weibo-10min`、`backup-30min`），重复命名会覆盖
- 多个分钟级任务并存无冲突
- 不要为分钟级需求创建 WorkBuddy 自动化（会造成每小时冗余触发，如上文核心事实）

## 已知坑（遇到即处理）
- `-RepetitionDuration ([TimeSpan]::MaxValue)` 报错 `任务 XML 包含格式不正确或超出范围的值` → 用有限时长 `(New-TimeSpan -Days 365)`
- PowerShell 输出被吞（某些环境 stdout 不显示）→ 用 `*> $log` 重定向到文件再读取验证
- `schtasks` 等系统工具被安全策略禁用 → 用 `Register-ScheduledTask`（本方案不依赖 schtasks）
- 脚本路径含中文/空格 → PowerShell 参数用双引号包住（模板已处理）
- Git Bash 下运行 `.cmd` shim 路径转换崩溃（`c:\c\...`）→ 直接调用 node.exe 或 exe 完整路径

## 飞书消息发送（如需）
用 lark-cli（飞书连接器安装后可用）：
```
node.exe <lark-cli安装目录>/node_modules/@larksuite/cli/scripts/run.js im +messages-send --user-id <ou_xxx> --text "<消息>" --as bot
```
- 用户身份可能缺 `im:message.send_as_user` 权限 → 用 `--as bot`
- Python 中调用时用 subprocess 传参数列表（不经 shell），避免转义问题
