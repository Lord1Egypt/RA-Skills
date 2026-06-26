---
name: java-perf-analyzer
description: Java 应用性能分析与诊断工具。基于 Arthas + MCP 实现远程 JVM 分析。**触发条件**：用户描述 Java 应用性能问题或诊断需求，包括：(1) 直接描述问题现象（CPU飙高、内存泄漏/紧张、接口响应慢、线程阻塞/死锁、类加载异常）(2) 请求 JVM 分析、Arthas 排查、性能诊断 (3) 说"帮我排查 xxx 问题"或"分析下 xxx 性能"。触发后先了解问题现象，再针对性收集信息、执行分析。
license: Apache-2.0
---

# Java 性能分析 Skill

基于 Arthas 的远程 JVM 性能分析工具，支持生产环境无侵入诊断。

## 工作流程（智能对话式）

### Phase 1: 了解问题现象

触发后，**先了解用户遇到的具体问题**，不要急着问参数。

**询问模板**：
```
遇到什么问题？
- CPU 飙高？
- 内存紧张/泄漏？
- 接口响应慢？
- 线程阻塞/死锁？
- 类加载异常？

描述一下现象，我来针对性分析。
```

### Phase 2: 问题类型 → 分析策略

根据用户描述的问题，选择对应的分析方法：

| 问题类型 | 首选分析 | 需要额外信息 |
|----------|----------|--------------|
| CPU 飙高 | `thread -n 5` 找忙线程 | 无 |
| 内存紧张 | `jvm` + `memory` 查使用率 | 无 |
| 内存泄漏 | `heapdump` + 离线分析 | 可能需要转储路径 |
| 接口慢 | `trace` 方法耗时 | **需要源码定位方法** |
| 线程阻塞 | `thread --state BLOCKED` | 无 |
| 类加载问题 | `sc` + `jad` + `classloader` | 类名 |

### Phase 3: 检查已有配置

执行分析前，检查 `MEMORY.md` 是否已有：
- SSH 地址、用户名、密码
- Java 进程名
- Arthas/MCP 配置状态

**有配置** → 直接执行分析
**无配置** → 询问缺少的信息（只问必要的）

### Phase 4: 收集缺少的信息

只收集 **当前分析需要的信息**：

| 信息 |何时需要 | 示例 |
|------|----------|------|
| SSH 地址 | 无配置时 | trythis.cn |
| SSH 用户名 | 无配置时 | root |
| SSH 密码 | 无配置时 | （用户提供） |
| Java 进程名 | 无配置时 | chat-editor |
| 源码地址 | 分析慢接口时 | /root/workspace/project |
| 类名 | 分析类加载问题时 | UserService |

**不要一次性问所有信息，按需询问**。

### Phase 5: 安装/连接 Arthas

**首次使用**：运行安装脚本
```bash
scripts/install-arthas.sh <ssh-host> <ssh-user> <ssh-password> <arthas-dir> <process-name>
```

**已有配置**：确认 SSH 隧道和 MCP 连接
```bash
# 检查隧道
ps aux | grep "ssh.*8563"

# 测试连接
mcporter call arthas jvm_info
```

### Phase 6: 执行针对性分析

根据 Phase 2 确定的策略，执行对应的分析命令。分析完成后：
1. 输出诊断报告
2. 给出优化建议
3. 如果需要深入分析，询问用户是否继续

根据用户描述的问题，选择合适的分析命令。

## 如果源码地址已提供

源码可用于：
1. **定位类和方法**：搜索源码找到可疑的类名和方法名
2. **反编译对比**：反编译运行中的类，对比源码看是否有差异
3. **方法追踪**：精确追踪问题方法

示例：
```bash
# 先在源码中搜索
grep -r "class UserService" <源码路径>

# 找到类名后追踪
mcporter call arthas method_trace --args '{"classMethod":"com.xxx.UserService#getUser"}'
```

## 核心分析命令

### JVM 信息

```bash
mcporter call arthas jvm_info
```

输出关键指标：
- 内存使用（HEAP/METASPACE）
- GC 统计（次数、时间）
- 线程状态（活跃、峰值、死锁）
- 类加载统计

### 线程分析

```bash
# 最忙的 N 个线程
mcporter call arthas thread_info --args '{"threadId":"-n 10"}'

# 按状态筛选
mcporter call arthas arthas_command command='thread --state BLOCKED'

# 线程详情
mcporter call arthas arthas_command command='thread <thread-id>'
```

### 内存分析

```bash
# 内存概览
mcporter call arthas arthas_command command='memory'

# 堆转储（用于离线分析）
mcporter call arthas arthas_command command='heapdump /path/to/dump.hprof'

# 查看大对象
mcporter call arthas arthas_command command='vmtool --action getInstances --className java.lang.Object --limit 10'
```

### 方法追踪

```bash
# 追踪方法调用耗时
mcporter call arthas method_trace --args '{"classMethod":"com.example.UserService#getUser"}'

# 监控方法参数和返回值
mcporter call arthas watch_method --args '{"classMethod":"com.example.UserService#getUser"}'

# 高级追踪（带条件）
mcporter call arthas arthas_command command='trace com.example.Service#method "#cost > 100"'
```

### 类分析

```bash
# 搜索类
mcporter call arthas class_info --args '{"className":"*Service"}'

# 反编译类
mcporter call arthas decompile_class --args '{"className":"com.example.UserService"}'

# 查看类加载器
mcporter call arthas arthas_command command='classloader -t'
```

### CPU 火焰图

```bash
# 启动 30 秒采样
mcporter call arthas arthas_command command='profiler start --event cpu --duration 30'

# 停止并生成火焰图
mcporter call arthas arthas_command command='profiler stop --format html'

# 下载火焰图（SSH）
scp <ssh-user>@<ssh-host>:/path/to/arthas-output/*.html ./flamegraph.html
```

## 性能诊断流程

### 场景 1：CPU 飙高

```
1. thread -n 5           → 找最忙线程
2. thread <id>           → 查线程堆栈
3. trace <method>        → 追踪热点方法
4. profiler start/stop   → 生成火焰图
```

### 场景 2：内存紧张

```
1. jvm                   → 查内存使用率
2. memory                → 查各区域详情
3. heapdump              → 堆转储离线分析
4. vmtool getInstances   → 查大对象
```

### 场景 3：响应慢

```
1. trace <class>#<method> "#cost > 100"  → 找慢方法
2. watch <class>#<method> "{params,returnObj,#cost}"  → 看参数耗时
3. stack <class>#<method>  → 查调用来源
```

### 场景 4：类加载问题

```
1. sc -d <class>         → 查类信息
2. jad <class>           → 反编译看实际代码
3. classloader -t        → 查加载器树
```

## MCP 配置模板

`~/.openclaw/workspace/config/mcporter.json`：

```json
{
  "mcpServers": {
    "arthas": {
      "command": "node",
      "args": ["/root/.openclaw/workspace/arthas-mcp-stdio.js"]
    }
  }
}
```

MCP 脚本见 `scripts/arthas-mcp-stdio.js`。

## Arthas 常用命令速查

见 `references/arthas-commands.md`。

## 注意事项

⚠️ **生产环境慎用**：
- `trace/watch` 有性能开销，高峰期避免长时间追踪
- `heapdump` 会暂停应用，大堆可能卡住
- 完成后记得 `stop` 停止追踪

✅ **最佳实践**：
- 优先用 `-n` 限制结果数量
- 使用条件过滤 `#cost > 100`
- 火焰图采样时间 30-60 秒足够
- 堆转储后用 MAT/JProfiler 离线分析

## 依赖

- 目标服务器有 Java 环境（JDK 8+）
- SSH 访问权限
- 本地 Node.js（MCP 需要）