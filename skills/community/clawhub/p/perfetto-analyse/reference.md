# Perfetto 配置参考

## 常用 Android 数据源名称（config.name）

| name | 用途 | 子配置 |
|------|------|--------|
| linux.ftrace | 内核/调度/atrace | ftrace_config（ftrace_events, atrace_categories, atrace_apps） |
| linux.process_stats | 进程/线程与内存采样 | process_stats_config（proc_stats_poll_ms 等） |
| linux.sys_stats | /proc 系统计数（meminfo、cpufreq 等） | sys_stats_config |
| android.power | 功耗 | android_power_config |
| android.heapprofd | Native 堆分析 | heapprofd_config（Android 10+） |
| android.java_hprof | Java 堆 dump | java_hprof_config（Android 11+） |
| gpu.counters | GPU 计数器 | gpu_counter_config |
| gpu.renderstages | GPU 渲染阶段 | gpu_renderstages_config |
| android.surfaceflinger.layers | SurfaceFlinger 图层 | surfaceflinger_layers_config |
| android.surfaceflinger.transactions | SF 事务 | surfaceflinger_transactions_config |
| android.windowmanager | 窗口管理 | windowmanager_config |
| android.kernel_wakelocks | 内核 wakelock | kernel_wakelocks_config |
| android.app_wakelocks | 应用 wakelock | app_wakelocks_config |
| android.log | Logcat | android_log_config |
| track_event | 应用/Perfetto SDK 打点 | track_event_config |

## TraceConfig 顶层字段（常用）

- **duration_ms**：采集时长（ms）。
- **buffers**：至少一个；size_kb、fill_policy（RING_BUFFER / DISCARD）。
- **data_sources**：DataSource 数组，每项含 config（name、target_buffer、数据源专属 config）。
- **write_into_file**：true 时周期写文件，长 trace 用；配合 file_write_period_ms、max_file_size_bytes。
- **trigger_config**：START_TRACING / STOP_TRACING 触发；trigger_timeout_ms。

## FtraceConfig 常用

- **ftrace_events**：如 "sched/sched_switch", "sched/sched_wakeup", "power/gpu_frequency"。
- **atrace_categories**：如 "gfx", "view", "am", "wm"。
- **atrace_apps**：包名，只抓指定应用 atrace。
- **buffer_size_kb**：每 CPU 内核 ring buffer（可选）。

## Android 采集命令速查

```bash
# 文本 config 从 stdin（Android 10+）
cat config.pbtx | adb shell perfetto --txt -c - -o /data/misc/perfetto-traces/out.pftrace

# 拉取
adb pull /data/misc/perfetto-traces/out.pftrace .
```

详细 proto 定义见 [TraceConfig Reference](https://perfetto.dev/docs/reference/trace-config-proto)。

## Trace 文件命令行查询（trace_processor）

对已抓取的 .pftrace 做 SQL 分析可用 **trace_processor**（与 UI 共用同一套 PerfettoSQL）。

### 方式一：本 skill 脚本（推荐，可被 Agent 直接调用）

```bash
pip install -r perfetto-analyse/scripts/requirements.txt   # 或 pip install perfetto
python perfetto-analyse/scripts/query_trace.py trace.pftrace -q "SELECT name, dur/1e6 AS dur_ms FROM slice LIMIT 10"
python perfetto-analyse/scripts/query_trace.py trace.pftrace -f my_query.sql
python perfetto-analyse/scripts/query_trace.py trace.pftrace -q "SELECT * FROM slice LIMIT 5" --csv
```

- **-q / --query**：内联 SQL 字符串。
- **-f / --file**：从文件读取 SQL。
- **--csv**：输出 CSV，默认制表符分隔。

### 方式二：交互式 trace_processor 二进制

```bash
curl -LO https://get.perfetto.dev/trace_processor && chmod +x ./trace_processor
./trace_processor trace.pftrace
# 进入交互式 SQL，输入 SELECT ... 等
```

- 文档：[Trace Processor](https://perfetto.dev/docs/analysis/trace-processor)
- Python API：[Trace Processor Python](https://perfetto.dev/docs/analysis/trace-processor-python)
