# LoongFlow 监控 Cron 配置

所有 LoongFlow 任务（native 和 engine 模式）共用**同一个**监控 cron，在首次启动任务时创建，后续任务直接复用。

## 检查是否已存在

```bash
openclaw cron list --json | python3 -c "
import json, sys
jobs = json.load(sys.stdin).get('jobs', [])
found = [j for j in jobs if 'loongflow' in j.get('name','').lower()]
print('FOUND' if found else 'MISSING')
"
```

- **FOUND**：不重复创建，直接跳过。
- **MISSING**：执行下方命令创建。

## 创建监控 Cron

```bash
openclaw cron add \
  --name "loongflow任务监控" \
  --every "10m" \
  --session isolated \
  --announce \
  --channel infoflow \
  --timeout-seconds 120 \
  --message '你是 LoongFlow 任务监控 agent。每次触发时，扫描所有活跃任务并向用户发送有价值的进度摘要。

## 数据收集

1. 读取 /root/.openclaw/openclaw.json，遍历 agents.list[].workspace（fallback: agents.defaults.workspace），收集所有 workspace 路径
2. 对每个 workspace，读取 <workspace>/.loongflow/tasks.json（不存在则跳过）
3. 合并所有 status=running 的任务

## 每个 running 任务的数据提取

**native 模式：**
- 读取 taskDir/index.md，提取：
  - 所有已完成迭代的分数列表（从 "Score: 0.XX" 行提取）
  - 最新迭代的 Insight 内容（关键发现）
  - 最新迭代的 Plan 摘要（本轮策略）
  - 当前 bestScore 和 currentIteration（从 tasks.json）
- 分析趋势：计算最近 2 轮分数差，判断是否在改进

**engine 模式：**
- 读取 logFile 最后 100 行，提取：
  - 最新 best_score 和当前 iteration 数
  - 最近一轮的 plan/execute 摘要（如有）
  - 是否有 ERROR 或异常
- 用 kill -0 检查进程是否还活着（pidFile 中的 PID）

**时间计算：**
- `import time; now = int(time.time())`，与 updatedAtEpoch 相减得秒数，除以 3600 得小时数
- 严禁用本地时间字符串比较

## 生成摘要消息

对每个 running 任务，发送一条有实质内容的摘要，格式如下：

```
📊 **<task-name>** [native/engine] · 第 X/N 轮 · 最佳分 0.XX

**进度趋势：** 分数 0.XX → 0.XX → 0.XX（↑上升 / →持平 / ↓下降）
**本轮策略：** <从 plan.md 或 log 提取的一句话，说明这轮在做什么>
**关键发现：** <从 summary.md 的 Insight 或 log 提取，说明学到了什么>
**预计剩余：** 还有 N 轮 / 已达上限 / 距上次更新 Xh
```

**规则：**
- "本轮策略" 和 "关键发现" 必须来自实际内容，不能是占位符
- 如果没有足够信息（第一轮刚开始），只发前两行，注明 "首轮运行中"
- 如果 engine 进程已退出（kill -0 失败）：标记 status=done，发最终结果摘要（best_score、总迭代数、solution 路径）
- 如果任务连续 3 轮分数无提升（delta < 0.05），在摘要中加 ⚠️ 提示用户考虑切换 Engine 模式

## 通知分发

- 从每个任务的 notifyUser 字段读取收件人（fallback: os.environ.get("BAIDU_CC_USERNAME") or whoami）
- 用 infoflow_send 分别发给对应的 notifyUser
- 每个任务发一条消息（不要把多个任务拼在一条里）

## Cron 生命周期管理

- 本轮结束后若仍有 running 任务：保留 cron
- 若无 running 任务：等下一轮再确认，连续两轮无 running 任务才执行 `openclaw cron rm <cron-id>` 删除本 cron
- 用 tasks.json 中的一个字段记录"上轮无任务"状态，避免依赖外部状态'
```

> **注意**：`--message` 使用单引号包裹，内部无需对 `$` 转义，避免 shell 提前展开变量。

## 重要约束

- ⚠️ **不要用 `infoflow_cron`**（systemEvent 模式）——它只触发 heartbeat，不执行实际逻辑。
- ⚠️ **不要依赖 HEARTBEAT.md**——cron 触发的 isolated session 不读 HEARTBEAT.md。
- 必须用 `--session isolated --announce` 才能真正执行检查并推送结果。
- 所有任务共用同一个监控 cron，不要为每个任务单独创建。
- `--timeout-seconds 120`：摘要生成需要读取文件和分析内容，给足时间。
