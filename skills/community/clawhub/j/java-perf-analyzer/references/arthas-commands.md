# Arthas 常用命令速查表

## 基础命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `help` | 查看命令帮助 | `help thread` |
| `dashboard` | JVM 仪表盘（实时） | `dashboard -i 5000` |
| `jvm` | JVM 信息 | `jvm` |
| `memory` | 内存详情 | `memory --limit 10` |
| `sysprop` | 系统属性 | `sysprop` |
| `sysenv` | 环境变量 | `sysenv` |
| `version` | Arthas 版本 | `version` |
| `quit/exit` | 退出 Arthas | `quit` |

## 线程命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `thread` | 线程列表 | `thread` |
| `thread -n 5` | 最忙 5 个线程 | `thread -n 5` |
| `thread <id>` | 线程详情 | `thread 123` |
| `thread --state BLOCKED` | 按状态筛选 | `thread --state BLOCKED` |
| `thread --all` | 所有线程 | `thread --all` |

## 类命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `sc -d <class>` | 查看类信息 | `sc -d com.example.*` |
| `sm -d <class>` | 查看方法信息 | `sm -d com.example.UserService` |
| `jad <class>` | 反编译类 | `jad com.example.UserService` |
| `jad <class> <method>` | 反编译方法 | `jad com.example.UserService getUser` |
| `classloader` | 类加载器 | `classloader -t` |
| `mc` | 内存编译器 | `mc /tmp/Test.java` |
| `retransform` | 热更新类 | `retransform /tmp/Test.class` |

## 方法追踪

| 命令 | 说明 | 示例 |
|------|------|------|
| `trace <class>#<method>` | 追踪方法耗时 | `trace com.example.UserService#getUser` |
| `trace -n 5` | 限制次数 | `trace com.example.Service#* -n 5` |
| `trace "#cost > 100"` | 条件过滤 | `trace com.example.Service#method "#cost > 100"` |
| `watch <class>#<method>` | 观察方法 | `watch com.example.Service#method "{params, returnObj}"` |
| `watch -b` | 观察调用前 | `watch com.example.Service#method "{params}" -b` |
| `stack <class>#<method>` | 调用来源 | `stack com.example.Service#method` |
| `monitor <class>#<method>` | 统计监控 | `monitor -c 5 com.example.Service#method` |

## 内存命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `heapdump <path>` | 堆转储 | `heapdump /tmp/dump.hprof` |
| `heapdump --live` | 只存活对象 | `heapdump --live /tmp/dump.hprof` |
| `vmtool --action getInstances` | 获取实例 | `vmtool --action getInstances --className java.util.HashMap --limit 10` |
| `profiler` | 性能采样 | `profiler start --event cpu` |
| `profiler stop` | 停止采样 | `profiler stop --format html` |

## 性能分析命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `profiler start` | 开始采样 | `profiler start --event cpu --duration 30` |
| `profiler stop` | 停止并输出 | `profiler stop --format html` |
| `profiler status` | 查看状态 | `profiler status` |
| `profiler list` | 支持事件 | `profiler list` |

支持的事件：
- `cpu` - CPU 采样（默认）
- `alloc` - 内存分配
- `lock` - 锁竞争
- `wall` - 墙钟时间

## 高级命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `ognl` | OGNL 表达式 | `ognl '@com.example.Constants@MAX_SIZE'` |
| `vmoption` | VM 参数 | `vmoption` |
| `vmoption --set` | 修改参数 | `vmoption --set MaxHeapFreeRatio 70` |
| `logger` | 日志级别 | `logger --name com.example --level debug` |
| `tt` | 时间隧道 | `tt -t com.example.Service#method` |
| `tt -i <index>` | 重放调用 | `tt -i 1000 -p` |

## MCP 快捷调用

```bash
# 基本信息
mcporter call arthas jvm_info

# 线程
mcporter call arthas thread_info --args '{"threadId":"-n 5"}'

# 内存
mcporter call arthas memory_info

# 类搜索
mcporter call arthas class_info --args '{"className":"*Service"}'

# 方法追踪
mcporter call arthas method_trace --args '{"classMethod":"com.example.Service#method"}'

# 反编译
mcporter call arthas decompile_class --args '{"className":"com.example.Service"}'

# 火焰图
mcporter call arthas profiler --args '{"action":"start","duration":30}'
mcporter call arthas profiler --args '{"action":"stop"}'

# 堆转储
mcporter call arthas heapdump --args '{"path":"/tmp/dump.hprof"}'

# 任意命令
mcporter call arthas arthas_command --args '{"command":"thread --state BLOCKED"}'
```

## 常见问题排查流程

### CPU 高

```
1. thread -n 5          # 找最忙线程
2. thread <id>          # 查堆栈
3. profiler start       # 采样 30 秒
4. profiler stop        # 生成火焰图
```

### 内存泄漏

```
1. jvm                  # 查内存趋势
2. memory               # 各区域详情
3. heapdump             # 转储
4. 用 MAT/JProfiler 分析
```

### 接口慢

```
1. trace <class>#<method> "#cost > 100"  # 找慢方法
2. watch <class>#<method> "{params,#cost}"  # 看参数和耗时
3. stack <class>#<method>  # 找调用链
```

### 类加载问题

```
1. sc -d <class>        # 类信息
2. classloader -t       # 加载器树
3. jad <class>          # 反编译看代码
```

## 注意事项

⚠️ 生产环境警告：
- `trace/watch/stack` 有性能开销，高峰期避免长时间开启
- `heapdump` 大堆会暂停应用
- 用 `-n` 限制次数，完成后 `stop` 关闭追踪
- 火焰图采样 30-60 秒足够