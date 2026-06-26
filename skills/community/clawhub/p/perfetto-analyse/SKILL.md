---
name: perfetto-analyse
description: >-
  Captures and analyzes Android Perfetto traces via CLI and config files. Covers
  trace collection (CPU, GPU, memory, rendering, power), editing TraceConfig
  (.pbtx), and analyzing jank, latency, overdraw, and power. Trace query can be
  done in Perfetto UI or via trace_processor command-line tool (PerfettoSQL).
  Use when working with Perfetto, systrace, Android performance, trace configs,
  or analyzing .perfetto-trace files.
---

# Perfetto 分析与采集

## 何时使用本 Skill

- 需要命令行采集 Android Perfetto trace（adb + perfetto）
- 需要编写或修改 trace 配置文件（.pbtx / TraceConfig）
- 需要根据诉求分析 trace：卡顿(jank)、耗时、过度绘制、功耗等

## 一、Trace 采集

### 1.1 基本命令

**本地设备（adb）：**

```bash
# 使用文本格式配置（Android 10+ 推荐）
adb shell perfetto --txt -c - -o /data/misc/perfetto-traces/trace.pftrace < config.pbtx

# 或先把 config 推到设备再执行（Android 12+ 可写 /data/misc/perfetto-configs）
adb push config.pbtx /data/misc/perfetto-configs/
adb shell perfetto --txt -c /data/misc/perfetto-configs/config.pbtx -o /data/misc/perfetto-traces/trace.pftrace
```

**拉取 trace 到本机：**

```bash
adb pull /data/misc/perfetto-traces/trace.pftrace .
```

**长时采集（benchmark/CI）：** 用 `perfetto --background` 拿到 PID，结束时 `kill $PID`；或用 `write_into_file: true` + 较大 `duration_ms` 做流式写入。

### 1.2 配置结构要点

- **buffers**：至少一个；`size_kb` 建议 20480+（约 20MB）避免高事件率时丢数据；高吞吐与低频率数据源可分开 buffer（`target_buffer: 0/1`），避免 ring buffer 冲掉慢数据。
- **duration_ms**：采集时长（毫秒），不包含 suspend 时间。
- **data_sources**：每个 source 用 `config { name: "..." target_buffer: 0 ... }`，name 必须与数据源注册名一致。

常用 Android 数据源名称见 [reference.md](reference.md)。

### 1.3 按诉求选数据源

| 诉求         | 建议启用的数据源 / 配置 |
|--------------|--------------------------|
| CPU 调度     | `linux.ftrace` + ftrace_events（sched_switch, sched_wakeup 等） |
| GPU / 渲染   | `linux.ftrace`（含 atrace_categories: "gfx"）、`gpu.renderstages`、`gpu.counters` |
| 内存         | `linux.process_stats`、可选 `android.heapprofd` / `android.java_hprof` |
| 渲染/合成    | atrace "gfx"、"view"；`android.surfaceflinger.layers` 等 |
| 功耗         | `android.power`、ftrace 中 power/*（如 power/gpu_frequency） |
| 卡顿/帧率   | 必须：ftrace + atrace "gfx"；建议：surfaceflinger、gpu 相关 |

编辑 config 时按上表勾选对应 `data_sources` 块，并保证 buffers 足够大。

## 二、编辑 Trace 配置文件

### 2.1 最小可运行示例（仅 CPU 调度）

```text
duration_ms: 10000
buffers {
  size_kb: 20480
  fill_policy: RING_BUFFER
}
data_sources {
  config {
    name: "linux.ftrace"
    target_buffer: 0
    ftrace_config {
      ftrace_events: "sched/sched_switch"
      ftrace_events: "sched/sched_wakeup"
    }
  }
}
```

### 2.2 通用 UI/卡顿分析配置要点

- **buffers**：至少 20MB（如 20480），必要时多块 buffer 分离 ftrace 与 sys_stats/heapprofd。
- **linux.ftrace**：启用 `sched/sched_switch`、`sched/sched_wakeup`；加 `atrace_categories: "gfx"`、`atrace_categories: "view"` 做渲染与 View 层级；需看指定应用时用 `atrace_apps: "com.example.app"`。
- **android.surfaceflinger.layers** / **gpu.renderstages**：按需开启，用于帧时间线与 GPU 阶段。
- **android.power**：功耗分析时加上对应 `android_power_config`。

具体字段与更多数据源见 [reference.md](reference.md)。修改后用 `adb shell perfetto --txt -c - -o /data/misc/perfetto-traces/out.pftrace < config.pbtx` 验证能否正常采集。

### 2.3 Android 注意点

- Android 10 以下不支持 `--txt`，需用二进制 config。
- 长 trace 可用 `write_into_file: true`、较大 `duration_ms`，并设 `file_write_period_ms`（最小约 100ms）；buffer 建议 32MB+。
- 非 root 且 Android 12 以下：config 用 stdin 传入，`adb shell perfetto -c - -o ...` 且 `cat config.pbtx | adb shell perfetto --txt -c - -o ...`。

## 三、Trace 分析

### 3.1 分析入口

- **Perfetto UI**：在 [ui.perfetto.dev](https://ui.perfetto.dev) 打开 .pftrace / .perfetto-trace，看时间线（Scheduling、Frame Timeline、GPU、Binder、内存等）和 Query 面板。
- **命令行查询**：使用 Perfetto 自带的 **trace_processor** 对 trace 文件做 SQL 查询，适合脚本和 CI。见 3.6。

### 3.2 卡顿（Jank）与帧率

- **Frame Timeline**：看 Present Type（早/准时/迟到）、Jank Type、On time finish、GPU Composition。
- **常见 Jank 类型**：AppDeadlineMissed（应用未按时完成）、BufferStuffing（队列堆积）、SurfaceFlinger GpuDeadlineMissed（GPU 合成超时）等。
- **排查顺序**：主线程是否被长任务/锁阻塞 → GPU 阶段是否过长 → Binder/GC 是否密集。

### 3.3 耗时与热点

- 在时间线上选中区间，看该区间内各 track 的时长分布。
- 用 **Query (SQL)**：查 slice/event 的 duration 排序，定位耗时点。示例见下节。

### 3.4 过度绘制

- 结合 atrace 的 "view" 与 "gfx"：看 measure/layout/draw 的频次与时长；单帧内过多 draw 或重复的 layout 可作为过度绘制线索。
- 若 trace 中有渲染层级或 SurfaceFlinger 数据，可结合 Frame Timeline 与 layer 信息看合成与绘制成本。

### 3.5 功耗

- 看 **android.power** 与 ftrace 中 power 相关事件（如 `power/gpu_frequency`、wakelock）。
- 结合 CPU 调度与 wakeup：高唤醒、高 CPU 占用时段对应功耗热点。

### 3.6 SQL 查询（UI 或命令行 trace_processor）

Trace 的 SQL 可在 **Perfetto UI** 的 Query 面板执行，也可用 **trace_processor** 命令行工具在本地执行（同一套 PerfettoSQL）。

**命令行用法：**

```bash
# 下载（Linux/macOS）
curl -LO https://get.perfetto.dev/trace_processor
chmod +x ./trace_processor

# 打开 trace 进入交互式 SQL shell
./trace_processor trace.pftrace
# 进入后直接输入 SQL，例如：
# SELECT name, dur/1e6 AS dur_ms FROM slice WHERE dur > 1000 ORDER BY dur DESC LIMIT 20;
```

**通过本 skill 提供的脚本调用 trace_processor（推荐在需要执行单条/文件内 SQL 时使用）：**

```bash
# 依赖: pip install perfetto（或 pip install -r perfetto-analyse/scripts/requirements.txt）
python perfetto-analyse/scripts/query_trace.py <trace.pftrace> -q "SELECT name, dur/1e6 AS dur_ms FROM slice WHERE dur > 1000 ORDER BY dur DESC LIMIT 20"
python perfetto-analyse/scripts/query_trace.py <trace.pftrace> -f query.sql
python perfetto-analyse/scripts/query_trace.py <trace.pftrace> -q "SELECT ..." --csv
```

脚本内部通过 Perfetto 的 Trace Processor（Python API）加载 trace 并执行 SQL，输出制表符分隔或 CSV。分析 trace 时优先考虑直接运行该脚本并传入用户给出的 SQL 或查询诉求。

**示例查询 1：slice 按耗时降序**

```sql
SELECT slice.name, slice.dur/1e6 AS dur_ms
FROM slice
WHERE slice.dur > 1000
ORDER BY slice.dur DESC
LIMIT 50;
```

**示例查询 2：带进程名（thread track）**

```sql
SELECT slice.name, slice.dur/1e6 AS dur_ms, process.name AS process_name
FROM slice
JOIN track ON slice.track_id = track.id
JOIN thread ON track.utid = thread.utid
JOIN process ON thread.upid = process.id
WHERE slice.dur > 1000
ORDER BY slice.dur DESC
LIMIT 30;
```

（时间单位：ts/dur 为纳秒，除以 1e6 得毫秒。以上 SQL 在 UI 与 trace_processor 中均可运行。）

**Frame 相关：** 若有 `ExpectedFrameTimeline` 等表，可查 present/jank 类型与 ts 范围，再与 slice 做时间关联。

根据用户具体诉求（只要卡顿 / 只要耗时 / 只要功耗等），从本节选对应子节并给出更具体的操作步骤与可选的 SQL 变体。

## 四、资源与模板

- 配置字段与数据源速查：[reference.md](reference.md)
- 按场景的配置示例：[configs/](configs/) 目录下的 TraceConfig 模板（通用 UI、CPU、功耗等）：`configs/cpu_only.pbtx.txt`、`configs/ui_jank.pbtx.txt`、`configs/power.pbtx.txt`。**文件以 .pbtx.txt 存储以便上传；内容为标准 .pbtx（TraceConfig）格式。** 使用方式：
  - **stdin 传入**：直接 `adb shell perfetto --txt -c - -o ... < configs/xxx.pbtx.txt`，无需改后缀。
  - **推到设备再执行**：先 `cp configs/xxx.pbtx.txt config.pbtx`（或写入到带 .pbtx 的文件），再 `adb push config.pbtx ...` 与 `adb shell perfetto -c /path/config.pbtx ...`。perfetto 只认内容，不认本地文件名，但设备上路径建议用 .pbtx 便于识别。
- **调用 trace_processor 做 SQL 查询**：[scripts/query_trace.py](scripts/query_trace.py)，用法见上文 3.6。对 trace 文件做查询时，可执行该脚本并传入 `-q "SQL"` 或 `-f query.sql`，必要时加 `--csv`。

分析时优先确认 trace 是否包含对应数据源（如没开 gfx 则看不到详细帧合成），再在 UI 中切到对应 track 与 SQL 做定量分析；需在命令行得到查询结果时，使用 `scripts/query_trace.py`。
