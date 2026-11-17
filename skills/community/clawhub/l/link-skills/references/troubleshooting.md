# Link 故障排查指南

## 常见问题快速索引

| 问题 | 原因 | 解决方案 | 严重程度 |
|------|------|----------|----------|
| curl 返回 475 | link 框架入站签名校验失败 | 通过网关访问或配置签名头 | 高 |
| Maven 编译失败 | link-core 不在本地 .m2 | 配置 settings.xml 指向内部 Nexus | 高 |
| 接口返回 412 | 乐观锁冲突 | 重试或检查并发更新 | 中 |
| MyBatis SQL 注入 | `${}` 拼接排序字段 | 改用白名单校验 | 高 |
| 大文件下载 OOM | Range 解析脆弱 | 使用流式写入 + 分片处理 | 高 |
| Fastjson 漏洞 | 1.2.83 版本历史漏洞 | 评估升级到 Fastjson2 或替换 Jackson | 中 |
| 服务注册失败 | Eureka 连接超时 | 检查网络、Eureka 地址配置 | 高 |
| Apollo 配置不生效 | Namespace 未关联 | 确认 AppID、Cluster、Namespace 配置 | 中 |
| 网关路由 404 | 路由规则未配置 | 检查 gateway application.yml 路由配置 | 中 |

## 环境限制

### 本地开发环境限制

| 限制 | 详细说明 | 影响范围 |
|------|----------|----------|
| Maven 环境异常 | 本地 Maven 无法正常执行 `mvn compile` | 无法本地编译 |
| link-core 缺失 | link-core 1.5.95-RELEASE JAR 不在本地 .m2 仓库 | 编译失败 |
| 签名过滤器 | link-mvc 入站签名过滤器导致直接 curl 返回 475 | 无法直接测试接口 |
| 无测试数据库 | 本地无 linkbase 数据库实例 | 无法执行集成测试 |

### 解决方案

#### Maven 编译问题

1. **配置 settings.xml**：

```xml
<!-- 路径: link-ai/settings.xml -->
<settings>
  <mirrors>
    <mirror>
      <id>aliyun</id>
      <mirrorOf>central</mirrorOf>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
  </mirrors>
  <servers>
    <server>
      <id>link-nexus</id>
      <username>linkcrm</username>
      <password>hand123654</password>
    </server>
  </servers>
  <profiles>
    <profile>
      <id>link-repo</id>
      <repositories>
        <repository>
          <id>link-nexus</id>
          <url>http://nexus.saas.hand-china.com/repository/link-maven-repository-proxy/</url>
          <releases><enabled>true</enabled></releases>
          <snapshots><enabled>true</enabled></snapshots>
        </repository>
      </repositories>
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>link-repo</activeProfile>
  </activeProfiles>
</settings>
```

2. **使用 Docker 构建**：跳过本地 Maven，直接用 Dockerfile 多阶段构建

#### 签名过滤器问题

**方案一**：通过网关访问（网关处理签名）
```bash
curl -X POST http://{gateway}:8888/linkcrm/ai/aiAssistant/kbDocument/queryByExamplePage \
  -H "Content-Type: application/json" \
  -d '{"page":1,"pageSize":10}'
```

**方案二**：本地开发禁用签名校验
```yaml
# application-dev.yml
link:
  mvc:
    security:
      sign-check: false
```

**方案三**：获取 Token 后携带签名头
```bash
# 先登录获取 Token
TOKEN=$(curl -s -X POST http://{gateway}:8888/linkcrm/login/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"xxx"}' | jq -r '.result.token')

# 带 Token 访问
curl -H "Authorization: Bearer $TOKEN" ...
```

## 已知代码问题

### 来源：code-review-report.md

#### 问题 1：SQL 注入风险（严重）

**位置**：MyBatis XML 中排序字段使用 `${}` 拼接

**风险**：恶意排序参数可注入 SQL

**修复**：
```xml
<!-- 禁止 -->
ORDER BY ${orderField}

<!-- 改用白名单 -->
ORDER BY
<choose>
    <when test="orderField == 'name'">DOCUMENT_NAME</when>
    <when test="orderField == 'date'">CREATION_DATE</when>
    <otherwise>CREATION_DATE</otherwise>
</choose>
```

#### 问题 2：大文件下载 OOM 风险（严重）

**位置**：文件下载接口 Range 解析脆弱

**风险**：大文件全量加载到内存导致 OOM

**修复**：使用流式写入 + 分片处理：
```java
// 禁止：全量读取
byte[] data = Files.readAllBytes(path);

// 改用：流式写入
try (InputStream is = new FileInputStream(file);
     OutputStream os = response.getOutputStream()) {
    byte[] buffer = new byte[8192];
    int bytesRead;
    while ((bytesRead = is.read(buffer)) != -1) {
        os.write(buffer, 0, bytesRead);
        os.flush();
    }
}
```

#### 问题 3：启动类 Bug（中）

**位置**：`LinkAiApplication.java` 第 19 行

**问题**：调用 `CoreApplication.class`（疑似应为 `LinkAiApplication.class`）

**修复**：
```java
// 禁止
SpringApplication.run(CoreApplication.class, args);

// 修正
SpringApplication.run(LinkAiApplication.class, args);
```

#### 问题 4：异常信息泄露（中）

**位置**：Controller 层通用异常处理

**风险**：`Exception` 详情返回前端，泄露内部信息

**修复**：
```java
catch (Exception var9) {
    log.error("操作失败", var9);  // 日志记录完整异常
    result.put("success", false);
    result.put("code", "500");
    result.put("detailMessage", "系统错误，请联系管理员");  // 前端不显示详情
}
```

#### 问题 5：Fastjson 安全漏洞（中）

**风险**：Fastjson 1.2.83 存在历史反序列化漏洞

**建议**：
- 评估升级到 Fastjson2（`com.alibaba.fastjson2:fastjson2`）
- 或逐步替换为 Jackson（项目已依赖 Jackson 2.10.5）
- 临时措施：禁用 AutoType（`ParserConfig.getGlobalInstance().setAutoTypeSupport(false)`）

## 服务启动问题排查

### 服务无法启动

**排查步骤**：

1. **检查日志**：
```bash
# K8s 环境
kubectl logs -n cdfai <pod-name> --tail=100

# 本地环境
tail -100 logs/link-ai.log
```

2. **常见原因**：

| 原因 | 日志特征 | 解决方案 |
|------|----------|----------|
| 数据库连接失败 | `Communications link failure` | 检查 MySQL 地址、端口、凭据 |
| Eureka 注册失败 | `Retry execute and register` | 检查 Eureka 地址、网络连通性 |
| Apollo 配置加载失败 | `Apollo config load error` | 检查 AppID、Cluster、网络 |
| Redis 连接失败 | `Cannot get Jedis connection` | 检查 Redis 地址、集群状态 |
| 端口占用 | `Port 8888 was already in use` | 更换端口或释放占用 |
| 内存不足 | `OutOfMemoryError` | 增加 Xmx 或容器内存限制 |

### 服务注册不上 Eureka

**排查步骤**：

1. 确认 Eureka 服务正常运行
2. 检查 `bootstrap.yml` 中 Eureka 配置：
```yaml
eureka:
  client:
    serviceUrl:
      defaultZone: http://{eureka-host}:8761/eureka/
```
3. 检查网络连通性：`telnet {eureka-host} 8761`
4. 检查 `spring.application.name` 是否正确

### 网关路由 404

**排查步骤**：

1. 检查 gateway `application.yml` 路由配置
2. 确认目标服务已注册到 Eureka
3. 检查 StripPrefix 配置
4. 确认请求路径格式：`/linkcrm/{module}/{resource}/{action}`

## 性能问题排查

### 接口响应慢

**排查步骤**：

1. **数据库慢查询**：
```sql
-- 查看慢查询日志
SHOW VARIABLES LIKE 'slow_query_log%';
-- 分析执行计划
EXPLAIN SELECT * FROM LNK_KB_DOCUMENT WHERE DOCUMENT_NAME LIKE '%test%';
```

2. **MyBatis 插件性能**：检查 `MybatisSqlInterceptor` 字段审计是否影响性能

3. **JVM GC**：
```bash
# 查看 GC 日志
tail -100 logs/gc.log
# 关注 Full GC 频率和 STW 时间
```

4. **Redis 缓存**：确认热点数据是否命中缓存

5. **Feign 调用**：检查跨服务调用是否有超时、重试

### 内存泄漏

**排查步骤**：

1. **监控容器内存**：
```bash
kubectl top pod -n cdfai -l app=link-ai
```

2. **Heap Dump**：
```bash
# 触发 heap dump
kubectl exec -n cdfai <pod-name> -- jmap -dump:format=b,file=/app/heap.hprof 1
```

3. **分析 Dump**：使用 MAT (Memory Analyzer Tool) 分析

### CPU 飙高

**排查步骤**：

1. **查找高 CPU 线程**：
```bash
kubectl exec -n cdfai <pod-name> -- top -H -p 1
```

2. **线程 Dump**：
```bash
kubectl exec -n cdfai <pod-name> -- jstack 1 > thread_dump.txt
```

3. **分析热点**：查找 RUNNABLE 状态线程，对应代码位置

## 日志排查

### 日志级别

| 级别 | 使用场景 |
|------|----------|
| ERROR | 系统错误、异常、需要立即处理 |
| WARN | 潜在问题、降级、重试 |
| INFO | 关键业务操作、状态变更 |
| DEBUG | 调试信息（生产环境关闭） |

### 关键日志关键词

| 关键词 | 含义 | 排查方向 |
|--------|------|----------|
| `BasicServiceException` | 业务异常 | 查看异常 code 和 detailMessage |
| `Communications link failure` | 数据库连接失败 | 检查网络、数据库状态 |
| `Cannot get Jedis connection` | Redis 连接失败 | 检查 Redis 集群状态 |
| `Hystrix timeout` | 服务调用超时 | 检查下游服务、调整超时配置 |
| `OutOfMemoryError` | 内存溢出 | 增加内存、排查泄漏 |
| `475` | 签名校验失败 | 检查签名头、Token 有效性 |
| `OptimisticLockException` | 乐观锁冲突 | 重试或检查并发更新 |

## 运维操作清单

### 日常巡检

| 项目 | 频率 | 命令/操作 |
|------|------|-----------|
| Pod 状态 | 每日 | `kubectl get pods -n cdfai` |
| 服务注册 | 每日 | Eureka 控制台检查 |
| 错误日志 | 每日 | 检查 ERROR 级别日志 |
| 数据库慢查询 | 每周 | 慢查询日志分析 |
| Redis 内存 | 每周 | `redis-cli info memory` |
| 磁盘空间 | 每周 | `df -h` |
| JVM GC | 每周 | GC 日志分析 |
| Apollo 配置变更 | 每次变更 | 记录变更内容和原因 |

### 应急响应

1. **服务宕机**：
   - 检查 Pod 状态：`kubectl get pods -n cdfai`
   - 查看 Pod 事件：`kubectl describe pod <pod-name> -n cdfai`
   - 查看日志：`kubectl logs <pod-name> -n cdfai --tail=200`
   - 重启服务：`kubectl rollout restart deployment/<service> -n cdfai`

2. **数据库故障**：
   - 检查 MySQL 状态：`SHOW STATUS LIKE 'Threads_connected'`
   - 检查主从同步：`SHOW SLAVE STATUS\G`
   - 切换从库：修改数据源配置（Apollo 热更新）

3. **配置回滚**：
   - Apollo 控制台回滚配置
   - K8s 回滚：`kubectl rollout undo deployment/<service> -n cdfai`
