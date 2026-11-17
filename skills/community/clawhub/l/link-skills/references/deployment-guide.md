# Link 部署指南

## 部署架构概览

```
                    ┌──────────────────┐
                    │   Kubernetes     │
                    │   Cluster        │
                    └───────┬──────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
    ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐
    │  link-ai    │  │  link-base  │  │ link-gateway│
    │  Pod        │  │  Pod        │  │  Pod        │
    └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
           │                │                │
    ┌──────┴────────────────┴────────────────┴──────┐
    │              Apollo 配置中心                    │
    │         (AppID: cdfai-link-ai)                 │
    └────────────────────────────────────────────────┘
           │                │                │
    ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐
    │   MySQL     │  │   Redis     │  │   Kafka     │
    │  Cluster    │  │  Cluster    │  │             │
    └─────────────┘  └─────────────┘  └─────────────┘
```

## Docker 构建

### Dockerfile（多阶段构建）

路径：`link-ai/Dockerfile`（其他模块类似）

```dockerfile
# Stage 1: 构建
FROM registry.cn-shanghai.aliyuncs.com/cdfsunrise-ci/maven:3.5.4-jdk-8-slim AS maven_build
WORKDIR /app
COPY pom.xml .
COPY src ./src
COPY settings.xml /root/.m2/settings.xml
RUN mvn clean package -DskipTests

# Stage 2: 运行时
FROM registry.cn-hangzhou.aliyuncs.com/choerodon-tools/javabase:0.8.0
ENV TZ=Asia/Shanghai
# 安装字体（CJK 支持，用于导出 PDF 等场景）
RUN apk add --no-cache fontconfig ttf-dejavu font-noto-cjk
WORKDIR /app
COPY --from=maven_build /app/target/*.jar ./app.jar
EXPOSE 9235
ENTRYPOINT exec java -XX:+UseCGroupMemoryLimitForHeap $APP_PARAMS -jar ./app.jar
```

### 构建命令

```bash
# 进入对应模块目录
cd D:\develop\code\cdfai\link-ai

# 构建镜像
docker build -f Dockerfile -t cdfai/link-ai:latest .

# 带版本标签
docker build -f Dockerfile -t cdfai/link-ai:v1.0.0 .
```

### 构建注意事项

1. **Maven settings.xml**：需配置阿里云镜像 + 内部 Nexus 仓库认证
2. **私有依赖**：link-core 等从内部 Nexus 拉取
3. **JDK 版本**：Java 8（镜像内 JDK 8）
4. **时区**：Asia/Shanghai
5. **字体**：安装 CJK 字体包（中文支持）
6. **JVM 参数**：通过 `$APP_PARAMS` 环境变量传入

## Kubernetes 部署

### Deployment.yaml

路径：`link-ai/Deployment.yaml`

关键配置项：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: link-ai
  namespace: cdfai
spec:
  replicas: 1
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
        - name: link-ai
          image: cdfai/link-ai:latest
          ports:
            - containerPort: 9235
          env:
            - name: APP_PARAMS
              value: >-
                -XX:+UseG1GC
                -XX:MaxGCPauseMillis=200
                -Xms1024m
                -Xmx1024m
                -Dspring.profiles.active=eurekamulti
          resources:
            requests:
              memory: "1024Mi"
              cpu: "500m"
            limits:
              memory: "2048Mi"
              cpu: "1000m"
          startupProbe:      # 启动探针
            tcpSocket:
              port: 9235
            initialDelaySeconds: 60
            periodSeconds: 10
            failureThreshold: 30
          readinessProbe:    # 就绪探针
            tcpSocket:
              port: 9235
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:     # 存活探针
            tcpSocket:
              port: 9235
            periodSeconds: 20
            failureThreshold: 3
      affinity:
        nodeAffinity:        # 节点亲和性
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node-role
                    operator: In
                    values:
                      - worker
        podAntiAffinity:     # Pod 反亲和性（分散部署）
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: link-ai
                topologyKey: kubernetes.io/hostname
```

### Helm Charts

路径：`link-ai/charts/link-ai/`

```
charts/link-ai/
├── Chart.yaml          # Chart 元信息
├── values.yaml         # 默认配置值
└── templates/
    ├── deployment.tpl  # Deployment 模板
    ├── service.tpl     # Service 模板
    └── _helpers.tpl    # 辅助模板函数
```

### values.yaml 关键配置

```yaml
replicaCount: 1

image:
  repository: cdfai/link-ai
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8888        # 服务端口
  containerPort: 9235  # 容器端口

resources:
  requests:
    memory: 1024Mi
    cpu: 500m
  limits:
    memory: 2048Mi
    cpu: 1000m

env:
  APP_PARAMS: >-
    -XX:+UseG1GC
    -XX:MaxGCPauseMillis=200
    -Xms1024m
    -Xmx1024m
    -Dspring.profiles.active=eurekamulti

# 数据库
database:
  host: mysql.base
  port: 3306
  name: linkbase

# Redis
redis:
  host: hone-redis-cluster.base
  port: 6379

# Kafka
kafka:
  bootstrapServers: 172.23.16.83:9092

# XXL-JOB
xxlJob:
  port: 8025

# Apollo
apollo:
  appId: cdfai-link-ai
  cluster: LOCAL
  namespaces: ops,biz,stability
```

### 部署命令

```bash
# 首次部署
helm install link-ai ./charts/link-ai -n cdfai

# 更新部署
helm upgrade link-ai ./charts/link-ai -n cdfai

# 查看部署状态
kubectl get pods -n cdfai -l app=link-ai

# 查看 Pod 日志
kubectl logs -n cdfai -l app=link-ai --tail=200

# 进入 Pod
kubectl exec -it -n cdfai <pod-name> -- /bin/sh

# 滚动重启
kubectl rollout restart deployment/link-ai -n cdfai

# 回滚
kubectl rollout undo deployment/link-ai -n cdfai
```

### PVC 持久化

```yaml
# 持久化挂载（如需要文件存储）
volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: link-ai-pvc
volumeMounts:
  - name: data-volume
    mountPath: /app/data
```

## Apollo 配置中心

### 配置信息

| 配置项 | 值 |
|--------|-----|
| AppID | `cdfai-link-ai` |
| Cluster | `LOCAL` |
| Namespaces | `ops` / `biz` / `stability` |

### Namespace 用途

| Namespace | 用途 | 示例配置 |
|-----------|------|----------|
| `ops` | 基础设施配置 | 数据源、Redis、Kafka 连接 |
| `biz` | 业务配置 | 业务参数、功能开关 |
| `stability` | 稳定性配置 | 限流、熔断、降级策略 |

### 配置文件

路径：`link-ai/etc/link-ai-service.yaml`

## 日志配置

### Log4j2

路径：`link-ai/src/main/resources/log4j2.xml`

- 日志框架：Log4j2 2.17.0
- 远程日志：Graylog GELF 1.3.1
- 日志目录：`logs/`

### 日志级别建议

| 环境 | 级别 |
|------|------|
| 开发 | DEBUG |
| 测试 | INFO |
| 生产 | INFO（关键模块 DEBUG） |

## JVM 调优

### 推荐参数

```bash
-XX:+UseG1GC                          # 使用 G1 垃圾回收器
-XX:MaxGCPauseMillis=200              # 最大 GC 停顿 200ms
-Xms1024m                             # 初始堆内存
-Xmx1024m                             # 最大堆内存
-XX:+UseCGroupMemoryLimitForHeap      # 根据容器限制自动设置堆内存
-XX:+PrintGCDetails                   # 打印 GC 详情
-XX:+PrintGCDateStamps                # 打印 GC 时间戳
-Xloggc:/app/logs/gc.log              # GC 日志路径
```

### 容器内存规划

| 容器内存 | 堆内存 | 说明 |
|----------|--------|------|
| 1024Mi | 512m-768m | 最小配置 |
| 2048Mi | 1024m-1536m | 推荐配置 |
| 4096Mi | 2048m-3072m | 高负载配置 |

## 服务端口规划

| 服务 | 容器端口 | 服务端口 | 说明 |
|------|----------|----------|------|
| link-ai | 9235 | 8888 | AI 助手服务 |
| link-gateway | 8888 | 8888 | API 网关 |
| link-ai (XXL-JOB) | 8025 | - | 定时任务执行器 |

## 上线检查清单

### 部署前

- [ ] Maven 打包成功（`mvn clean package -DskipTests`）
- [ ] Docker 镜像构建成功
- [ ] Helm Chart values 配置正确（副本数、资源限制、数据库连接）
- [ ] Apollo 配置已更新（新配置项已添加）
- [ ] 数据库 DDL 已执行
- [ ] 网关路由已配置（如需新增路由）

### 部署中

- [ ] Helm 部署成功
- [ ] Pod 启动成功（startupProbe 通过）
- [ ] Pod 就绪（readinessProbe 通过）
- [ ] 无 CrashLoopBackOff

### 部署后

- [ ] Eureka 注册成功
- [ ] 网关路由可达
- [ ] 接口冒烟测试通过
- [ ] 日志无 ERROR
- [ ] Swagger 文档可访问（`/swagger-ui.html`）
- [ ] 监控告警配置已确认
- [ ] XXL-JOB 任务注册成功（如涉及）

## 回滚方案

### K8s 回滚

```bash
# 查看发布历史
kubectl rollout history deployment/link-ai -n cdfai

# 回滚到上一版本
kubectl rollout undo deployment/link-ai -n cdfai

# 回滚到指定版本
kubectl rollout undo deployment/link-ai -n cdfai --to-revision=2
```

### 数据库回滚

- 保留 DDL 回滚脚本（DROP TABLE / ALTER TABLE REVERT）
- 数据变更需备份原数据

### 配置回滚

- Apollo 配置中心支持版本回滚
- 回滚前确认配置依赖关系
