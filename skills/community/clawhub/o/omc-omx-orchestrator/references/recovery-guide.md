# 重启恢复指南

## 恢复脚本

Agent 重启后，运行恢复脚本扫描所有 `task.json`：

```bash
python3 ~/.openclaw/workspace/skills/omc-omx-orchestrator/scripts/task-recovery.py recover
```

## 恢复逻辑

### Step 1: 扫描任务目录
```python
import os, json
task_dir = os.path.expanduser("~/.openclaw/workspace/tasks")
for task_id in os.listdir(task_dir):
    if not os.path.isdir(os.path.join(task_dir, task_id)):
        continue
    task_json = os.path.join(task_dir, task_id, "task.json")
    if not os.path.exists(task_json):
        continue
    # 处理每个任务
```

### Step 2: 状态检查矩阵

| task.json status | exit_code 文件 | PID 存活 | 新状态 | 说明 |
|-----------------|---------------|---------|--------|------|
| `running` | 存在 | - | `completed/failed` | 任务已完成，更新状态 |
| `running` | 不存在 | 存活 | `running` + `detached=true` | 进程仍在跑，标记分离 |
| `running` | 不存在 | 已死 | `failed` | 进程异常退出 |
| `completed/failed` | 存在 | - | 保持不变 | 状态正确 |

### Step 3: 详细恢复算法

```python
def recover_task(task_dir, task):
    exit_code_file = os.path.join(task_dir, "exit_code")
    
    # 检查 1：exit_code 文件是否存在
    if os.path.exists(exit_code_file):
        with open(exit_code_file) as f:
            exit_code = f.read().strip()
        
        # 任务已完成，更新状态
        task["exit_code"] = int(exit_code) if exit_code else -1
        task["completed_at"] = datetime.now(TZ).isoformat()
        task["status"] = "completed" if task["exit_code"] == 0 else "failed"
        task["detached"] = False
        return task
    
    # 检查 2：进程是否存活
    pid = task.get("pid")
    if pid:
        try:
            os.kill(pid, 0)  # 检查进程存在
            # 进程仍在运行，标记为分离
            task["detached"] = True
            task["status"] = "running"
            return task
        except OSError:
            # 进程已死
            pass
    
    # 检查 3：都不满足，标记失败
    task["status"] = "failed"
    task["failure_reason"] = "进程已退出但 exit_code 未写入（可能被 SIGKILL）"
    task["completed_at"] = datetime.now(TZ).isoformat()
    task["detached"] = False
    return task
```

## 手动操作

### 查询命令

```bash
# 列出所有任务
python3 task-recovery.py list

# 只看运行中的任务
python3 task-recovery.py list running

# 查看任务详情
python3 task-recovery.py show 2026-04-27-120000-fix-auth

# 查看最近 10 个任务
python3 task-recovery.py list --limit 10
```

### 清理操作

```bash
# 清理 >7 天的已完成任务
python3 task-recovery.py cleanup --days 7

# 清理 >30 天的所有任务（包含失败的）
python3 task-recovery.py cleanup --days 30 --include-failed

# 强制清理指定任务
python3 task-recovery.py remove 2026-04-27-120000-fix-auth
```

### 修复操作

```bash
# 手动标记任务为失败
python3 task-recovery.py mark-failed 2026-04-27-120000-fix-auth "手动终止"

# 重置任务状态（重新派发）
python3 task-recovery.py reset 2026-04-27-120000-fix-auth

# 修复 PID 不一致
python3 task-recovery.py fix-pid 2026-04-27-120000-fix-auth
```

## 自动化部署

### Cron 任务配置

```bash
# 每 5 分钟恢复状态（修复 notify 丢失问题）
*/5 * * * * cd ~/.openclaw/workspace && python3 ~/.openclaw/workspace/skills/omc-omx-orchestrator/scripts/task-recovery.py recover

# 每小时清理 OMX 残留进程
0 * * * * tmux ls 2>/dev/null | grep 'omx-.*-detached-' | cut -d: -f1 | xargs -r tmux kill-session -t 2>/dev/null

# 每周清理过期任务
0 2 * * 0 cd ~/.openclaw/workspace && python3 ~/.openclaw/workspace/skills/omc-omx-orchestrator/scripts/task-recovery.py cleanup --days 7
```

### 启动 Hook

在 `~/.openclaw/workspace/hooks/startup.sh` 中添加：

```bash
#!/bin/bash
# 启动时自动恢复任务状态
python3 ~/.openclaw/workspace/skills/omc-omx-orchestrator/scripts/task-recovery.py recover
```

## 故障排查

### 常见问题

1. **task.json 损坏**
   ```bash
   # 检查 JSON 格式
   python3 -m json.tool ~/.openclaw/workspace/tasks/TASK_ID/task.json
   
   # 备份并修复
   cp task.json task.json.bak
   # 手动编辑修复
   ```

2. **PID 冲突**
   ```bash
   # 检查 PID 是否属于其他进程
   ps -p PID -o pid,ppid,comm
   
   # 修复方法：清空 PID 字段
   python3 task-recovery.py fix-pid TASK_ID
   ```

3. **exit_code 文件格式错误**
   ```bash
   # 检查文件内容
   cat ~/.openclaw/workspace/tasks/TASK_ID/exit_code
   
   # 应该只有一个数字，如果有其他内容需要清理
   echo "1" > ~/.openclaw/workspace/tasks/TASK_ID/exit_code  # 标记为失败
   ```

4. **任务目录权限问题**
   ```bash
   # 修复权限
   chmod 755 ~/.openclaw/workspace/tasks/
   chmod 644 ~/.openclaw/workspace/tasks/*/task.json
   ```

### 数据一致性检查

```bash
# 检查所有任务的数据一致性
python3 task-recovery.py validate

# 报告内容：
# - task.json 格式正确性
# - 必需文件存在性
# - 时间戳合理性
# - PID 有效性
# - 状态转换合法性
```

## 迁移和备份

### 任务数据备份

```bash
# 导出所有任务元数据
python3 task-recovery.py export --format json > tasks-backup.json

# 导出指定日期范围
python3 task-recovery.py export --from "2026-04-01" --to "2026-04-30" > april-tasks.json
```

### 任务数据导入

```bash
# 从备份恢复
python3 task-recovery.py import tasks-backup.json

# 验证导入结果
python3 task-recovery.py validate
```