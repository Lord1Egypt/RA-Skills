# 性能问题诊断

## 监控数据采集

| 监控类别 | 指标 | 频率 | 保留时间 | 工具 |
|---------|------|------|---------|------|
| 操作系统 | CPU、内存、网络、IO、磁盘 | 每 1 分钟 | 至少一周 | nmon |
| 数据库 | KWR、KSH 性能数据 | 每小时快照 | 至少一周 | KWR/KSH |

## 风险/问题识别

### 阈值告警

| 分类 | 子类 | 告警条件 |
|------|------|---------|
| OS-CPU | 利用率超过 70%、快速上涨、% System 过高 | |
| OS-IO | 利用率超过 50% | |
| OS-网络 | 利用率超过 50%、丢包和报错 | |
| OS-内存 | 空闲少于 10% 或存在 swap | |
| DB-等待事件 | 等待时间超过 5% | |
| DB-事务 | 回滚比例超过 20% | |
| DB-事务 | 执行时间过长 | |
| DB-SQL | 执行时间过长 | |

### 报告分析

- 操作系统资源：nmon analyzer 生成趋势报告
- 数据库资源：KWR、KSH 报告

## 风险/问题溯因

| 分类 | 子类 | 识别条件 | 溯因方法 |
|------|------|---------|---------|
| OS-CPU | >70% | 火焰图 + KWR 报告中 TOP SQL | |
| OS-IO | >50% | pidstat/iotop 查看 IO 分布；KWR IO Profile | |
| OS-网络 | >50% | nethogs/iftop 查看网络分布；KWR 按返回行数的 TOP SQL | |
| OS-内存 | <10% 空闲 | top 查看内存使用 + 数据库内存配置 | |
| DB-等待事件 | >5% | KWR/KDDM 报告等待事件部分 | |
| DB-事务回滚 | >20% | 分析运行日志与应用 | |
| DB-长事务 | 执行时间长 | 日志确认长 SQL，参考 SQL 调优指南 | |
| DB-慢 SQL | 执行时间长 | 日志确认 SQL，参考 SQL 调优指南 | |

## 风险/问题处理

### 处理方法

1. 参考《KingbaseES 数据库性能调优指南》"第三部分 性能优化"
2. 参考《KingbaseES 数据库 SQL 调优指南》"第 5 章 SQL 优化手段"
3. 纵向扩展：扩容存储、增加内存、增加处理器核数
4. 横向扩展：增加只读副本并均衡负载

### 常见场景

**慢 SQL 优化**：执行计划分析 + 火焰图

**并发场景吞吐量低**：收集问题时间段的 nmon、KWR 报告、火焰图

**响应时间持续上升**：在响应时间对比明显的两个时刻分别收集 nmon、KWR 报告、火焰图，分析关键指标差异（尤其是时间模型数据差异）

## 常用性能诊断工具

### nmon

广泛使用的操作系统监控与分析工具，实时捕捉 CPU、IO、内存、网络等资源使用情况。

**工具获取**：

- nmon：http://nmon.sourceforge.net/pmwiki.php?n=Site.Download
- nmon analyzer：http://nmon.sourceforge.net/pmwiki.php?n=Site.Nmon-Analyser

**交互模式**：

```bash
./nmon
```

通过快捷键选择需实时显示的信息。

**后台收集模式**：

```bash
./nmon -f -t -s 10 -c 100 -m /home/kingbase/nmon/
```

参数说明：

| 参数 | 含义 |
|------|------|
| -f | 带时间戳的文件输出 |
| -t | 显示顶级进程 |
| -s 10 | 每 10 秒采样一次 |
| -c 100 | 采样 100 次 |
| -m | 输出目录 |

可视化：通过 nmon analyzer 导入 nmon 文件生成 Excel 报告。

### KWR、KSH 报告

- **KWR（sys_kwr）**：自动负载信息库，参考《KingbaseES 数据库性能调优指南》KWR 报告章节
- **KSH（sys_ksh）**：活跃会话历史报告，参考 KSH 报告章节

### sys_stat_activity 视图

查看当前数据库活动连接信息，参考系统视图文档。

### sys_stat_statements 插件

记录历史 SQL 执行统计信息，参考 sys_stat_statements 插件手册。

### 火焰图

使用 perf 采集数据库进程的热点函数信息。

**使用步骤**：

```bash
# 1）下载工具
git clone https://github.com/brendangregg/FlameGraph.git

# 2）进入工具目录（root 用户）
cd FlameGraph

# 3）启动 perf 记录数据
perf record -F 99 -a -g

# 4）采集足够数据后（如 1 分钟），Ctrl+C 结束

# 5）生成火焰图
perf script | ./stackcollapse-perf.pl > out.perf-folded
./flamegraph.pl out.perf-folded > perf-kernel.svg
```

将生成的 SVG 文件导出或截图用于分析。分析方法请咨询 KingbaseES 支持人员。
