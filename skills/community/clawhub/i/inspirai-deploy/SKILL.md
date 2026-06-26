---
name: inspirai-deploy
description: "智能部署工具 - 自动检测部署策略，预检查、发布、监控一体化。支持 K8s/Helm、Docker Compose、Vercel、Fly.io。Triggers: '部署', 'deploy', '发布', '上线', '预检查', '部署监控', 'helm upgrade', 'docker compose up'."
version: 1.0.0
license: MIT
---

# inspirai-deploy - 智能部署工具

自动检测部署策略，执行预检查、发布、监控的一体化部署工具。支持 K8s/Helm、Docker Compose、Vercel、Fly.io。

## Init

### 初始化部署配置

自动检测项目结构，生成 `.deploy.yaml` 配置文件。

### 使用方式

```
/deploy init                     # 自动检测并生成配置
/deploy init --strategy k8s      # 指定策略
```

### 执行步骤

#### Step 1: 检测项目结构

```bash
echo "[INFO] 检测项目结构..."

# 检测部署策略
DETECTED_STRATEGIES=""

[ -d "helm" ] && DETECTED_STRATEGIES="$DETECTED_STRATEGIES k8s"
[ -f "docker-compose.yml" ] && DETECTED_STRATEGIES="$DETECTED_STRATEGIES compose"
[ -f "docker-compose.prod.yml" ] && DETECTED_STRATEGIES="$DETECTED_STRATEGIES compose"
[ -f "vercel.json" ] && DETECTED_STRATEGIES="$DETECTED_STRATEGIES vercel"
[ -f "fly.toml" ] && DETECTED_STRATEGIES="$DETECTED_STRATEGIES fly"
[ -f "Dockerfile" ] && DETECTED_STRATEGIES="$DETECTED_STRATEGIES docker-ssh"

echo "[INFO] 检测到策略: $DETECTED_STRATEGIES"
```

#### Step 2: 收集信息

使用 AskUserQuestion 确认或补充信息：

1. **策略选择** — 如果检测到多个，让用户选择
2. **项目名称** — 从 package.json / go.mod / 目录名推断
3. **环境列表** — 从 helm/environments 或询问用户

#### Step 3: 策略专属信息收集

**K8s：**
- 从 justfile/Makefile 提取 registry 信息
- 从 helm/ 目录发现 chart 和 values
- 从 .service-tags.json 或 services/ 发现组件
- 从 helm/environments/ 发现环境配置

**Compose：**
- 解析 docker-compose.yml 中的 services
- 检测远程部署目标（如有）

**Vercel/Fly：**
- 从 vercel.json / fly.toml 读取项目配置

#### Step 4: 生成 .deploy.yaml

**K8s 模板：**
```yaml
strategy: k8s

project:
  name: {project_name}
  description: {description}

registry:
  domain: {registry_domain}
  namespace: {registry_namespace}
  overrides:
    prd: {vpc_registry}

components:
  - name: {component}
    path: services/{component}
    image: {project}-{component}

environments:
  dev:
    cluster: {cluster}
    namespace: {namespace}
    context: {context}
  prd:
    cluster: {cluster}
    namespace: {namespace}
    context: {context}

commands:
  build: "{build_cmd}"
  push: "{push_cmd}"
  deploy: "{deploy_cmd}"
  config: "{config_cmd}"

helm:
  chart_path: helm/{chart}
  release_name: {release}

monitor:
  interval: 5
  timeout: 600
  failure_threshold: 3
```

**Compose 模板：**
```yaml
strategy: compose

project:
  name: {project_name}

compose:
  file: docker-compose.prod.yml
  # 远程部署（可选）
  host: {user}@{server}
  path: /opt/{project_name}

environments:
  dev:
    file: docker-compose.yml
  prd:
    file: docker-compose.prod.yml

commands:
  deploy: "docker compose -f {file} up -d"
  logs: "docker compose -f {file} logs -f"

monitor:
  interval: 5
  timeout: 120
```

**Vercel 模板：**
```yaml
strategy: vercel

project:
  name: {project_name}

environments:
  preview:
    auto: true
  prd:
    branch: main
    prod: true

commands:
  deploy: "vercel --prod"
  preview: "vercel"
```

#### Step 5: 确认配置

显示生成的配置文件，询问用户确认或修改。

### 输出

- 在项目根目录生成 `.deploy.yaml`
- 建议将 `.deploy.yaml` 加入版本控制（不含敏感信息时）

### 注意事项

- 如果 `.deploy.yaml` 已存在，询问是否覆盖
- 敏感信息（credentials、tokens）不写入配置文件
- 配置文件中使用占位符的命令模板，实际值从环境变量读取

## Check

### 部署预检查

执行部署前的预检查，确保所有条件就绪。

### 安全原则

**只检查、只报告，不修改任何文件。** 发现问题后提供修复建议，由用户决定是否执行。

### 使用方式

```
/deploy check <env> [components...] [options]

选项:
  --image-only         仅检查镜像
  --config-only        仅检查配置
  --connectivity-only  仅检查连通性
  --strategy <type>    指定策略
```

### 执行步骤

#### Step 1: 检测策略并加载配置

同 Run 部分的 Step 1。

#### Step 2: 通用检查

所有策略都执行的检查：

```bash
echo "[INFO] ========== 通用预检查 =========="

# 1. 环境变量检查
echo "[CHECK] 环境变量..."
# 检查 .env / .env.{env} 是否存在必需变量

# 2. Git 状态检查
echo "[CHECK] Git 状态..."
UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "[WARN] 有 $UNCOMMITTED 个未提交的变更"
fi

# 3. 分支检查（生产环境）
if [ "$ENV" = "prd" ]; then
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
        echo "[WARN] 当前分支 $BRANCH 不是主分支"
    fi
fi
```

#### Step 3: 策略专属检查

**K8s 策略：**

```bash
echo "[INFO] ========== K8s 预检查 =========="

# 1. 镜像推送检查
echo "[CHECK] 镜像推送状态..."
for comp in $COMPONENTS; do
    tag=$(get_version_tag "$comp" "$ENV")
    image="$REGISTRY/$NAMESPACE/${comp}:${tag}"
    if docker manifest inspect "$image" &>/dev/null; then
        echo "  ✓ $comp: $tag"
    else
        echo "  ✗ $comp: $tag (未推送)"
        FAILED=true
    fi
done

# 2. 配置同步检查
echo "[CHECK] 配置同步..."
# 渲染本地 Helm values vs 集群 ConfigMap/Secret
# 对比 data 字段差异

# 3. 集群连通性
echo "[CHECK] 集群连通性..."
kubectl cluster-info $KUBECTL_ARGS &>/dev/null || echo "[ERROR] 无法连接集群"

# 4. Namespace 存在性
kubectl get namespace "$NAMESPACE" $KUBECTL_ARGS &>/dev/null || echo "[ERROR] Namespace $NAMESPACE 不存在"
```

**Compose 策略：**

```bash
echo "[INFO] ========== Compose 预检查 =========="

# 1. 镜像构建检查
echo "[CHECK] 镜像构建..."
docker compose config --quiet || echo "[ERROR] compose 配置无效"

# 2. 目标主机连通性（远程部署时）
if [ -n "$DEPLOY_HOST" ]; then
    echo "[CHECK] 远程主机连通性..."
    ssh -o ConnectTimeout=5 "$DEPLOY_HOST" "echo ok" || echo "[ERROR] 无法连接 $DEPLOY_HOST"
fi

# 3. 磁盘空间
echo "[CHECK] 磁盘空间..."
docker system df
```

**Vercel/Fly 策略：**

```bash
echo "[INFO] ========== 平台预检查 =========="

# 1. CLI 登录状态
echo "[CHECK] 登录状态..."
vercel whoami || fly auth whoami || echo "[ERROR] 未登录"

# 2. 项目链接
echo "[CHECK] 项目链接..."
# 检查是否已 link 到远程项目
```

#### Step 4: 输出报告

```
========== 预检查报告 ==========

环境: uat
策略: k8s
组件: core, ops, admin

通用检查:
  ✓ 环境变量完整
  ✓ Git 状态干净
  ✓ 分支: main

策略检查:
  ✓ 镜像: core (v1.2.3)
  ✗ 镜像: ops (v1.2.3) - 未推送
  ✓ 配置同步
  ✓ 集群连通

结果: 1 项失败
建议: 执行 `just push uat COMPONENTS="ops"` 推送镜像后重试
```

### 注意事项

- 检查过程完全只读，不修改任何文件或集群状态
- 失败项提供具体的修复命令建议
- 可单独运行用于 CI/CD pipeline 的 gate check

## Run

### 执行部署

自动检测部署策略，执行完整的 check → deploy → monitor 流程。

### 安全原则

**严禁修改应用逻辑代码。** 本 skill 只操作部署相关文件（配置、Dockerfile、Helm、compose 等）。

如果部署过程中发现问题源于应用逻辑：
1. **立即停止部署**
2. **报告问题详情**（错误日志、堆栈信息）
3. **建议转交专业技能处理**（如 `/wxm:dev`、代码修复等）
4. **设置检查点**，修复后可从当前步骤恢复部署

### 使用方式

```
/deploy run <env> [components...] [options]

参数:
  env          目标环境 (dev/test/uat/prd)
  components   要部署的组件列表（默认: 全部）

选项:
  --skip-check         跳过所有预检查
  --skip-image-check   跳过镜像推送检查
  --skip-config-check  跳过配置同步检查
  --force              强制部署
  --strategy <type>    指定策略（跳过自动检测）
```

### 执行步骤

#### Step 1: 检测部署策略

按优先级自动检测：

```bash
# 1. 显式配置
if [ -f ".deploy.yaml" ]; then
    STRATEGY=$(grep "^strategy:" .deploy.yaml | awk '{print $2}')
fi

# 2. 自动检测
if [ -z "$STRATEGY" ]; then
    if [ -d "helm" ] && command -v kubectl &>/dev/null; then
        STRATEGY="k8s"
    elif [ -f "docker-compose.yml" ] || [ -f "docker-compose.prod.yml" ]; then
        STRATEGY="compose"
    elif [ -f "vercel.json" ]; then
        STRATEGY="vercel"
    elif [ -f "fly.toml" ]; then
        STRATEGY="fly"
    elif [ -f "Dockerfile" ]; then
        STRATEGY="docker-ssh"
    elif [ -f "package.json" ]; then
        STRATEGY="script"
    else
        echo "[ERROR] 无法检测部署策略，请创建 .deploy.yaml"
        exit 1
    fi
fi

echo "[INFO] 部署策略: $STRATEGY"
```

#### Step 2: 预检查（调用 Check）

执行策略对应的预检查，参见 Check 部分。

如果检查失败：
- 展示失败原因
- 提供选项：修复后重试 / 跳过检查 / 中止

#### Step 3: 执行部署

根据策略执行部署命令：

**K8s 策略：**
```bash
# 从 .deploy.yaml 或自动发现获取命令
DEPLOY_CMD=$(get_command "deploy" "$ENV")
# 通常是: just deploy $ENV 或 helm upgrade ...

echo "[INFO] 执行部署: $DEPLOY_CMD"
eval "$DEPLOY_CMD"
```

**Compose 策略：**
```bash
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
if [ "$ENV" = "prd" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
fi

docker compose -f "$COMPOSE_FILE" up -d $COMPONENTS
```

**Vercel 策略：**
```bash
if [ "$ENV" = "prd" ]; then
    vercel --prod
else
    vercel
fi
```

**Fly 策略：**
```bash
fly deploy --app "$APP_NAME"
```

**Script 策略：**
```bash
# 从 package.json scripts 中查找
npm run deploy:$ENV
```

#### Step 4: 监控（调用 Monitor）

部署命令执行后，自动进入监控模式，参见 Monitor 部分。

#### Step 5: 问题处理

**部署失败时的处理流程：**

```
检测到错误类型：
├── 配置错误（env vars、secrets）
│   → 提示修改部署配置，不触碰应用代码
├── 镜像拉取失败
│   → 检查 registry 连通性和镜像 tag
├── 健康检查失败（应用启动异常）
│   → ⚠️ 可能是逻辑问题
│   → 停止部署，输出日志
│   → 建议: "应用启动失败，建议检查应用代码后重新部署"
├── 资源不足（OOM、CPU limit）
│   → 提示调整资源配额
└── 未知错误
    → 输出完整日志，等待用户指示
```

**严格规则：任何涉及修改 .go / .ts / .js / .py 等业务代码的操作，必须停止并转交。**

### 检查点机制

每个步骤完成后设置检查点：
```
checkpoint: strategy_detected → checks_passed → deploy_submitted → monitoring
```

失败后恢复：
```
/deploy run <env> --resume    # 从上次检查点恢复
```

### 示例

```
/deploy run uat                    # 完整流程部署到 uat
/deploy run prd core ops           # 只部署 core 和 ops 到生产
/deploy run dev --skip-check       # 开发环境跳过检查
/deploy run uat --strategy compose # 强制使用 compose 策略
```

## Monitor

### 部署状态监控

监控进行中的部署状态，检测异常并提供诊断信息。

### 安全原则

**只监控、只报告。** 发现应用层错误时停止监控，报告问题并建议转交处理。严禁自动修改应用代码来"修复"问题。

### 使用方式

```
/deploy monitor <env> [options]

选项:
  --timeout <seconds>   超时时间（默认 600）
  --interval <seconds>  轮询间隔（默认 5）
  --logs                同时显示 Pod 日志
  --strategy <type>     指定策略
```

### 执行步骤

#### Step 1: 确定监控目标

根据策略确定要监控的资源：

**K8s：** Deployment replicas、Pod status、Events
**Compose：** Container status、health checks
**Vercel/Fly：** Deployment status API

#### Step 2: 轮询监控

**K8s 监控：**

```bash
TIMEOUT=${TIMEOUT:-600}
INTERVAL=${INTERVAL:-5}
START_TIME=$(date +%s)

while true; do
    ELAPSED=$(( $(date +%s) - START_TIME ))
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "[TIMEOUT] 超过 ${TIMEOUT}s 未完成"
        break
    fi

    echo "[INFO] ===== $(date +%H:%M:%S) (${ELAPSED}s) ====="

    # Deployment 状态
    kubectl get deployment -n $NAMESPACE -l "$INSTANCE_LABEL" $KUBECTL_ARGS \
        -o custom-columns="NAME:.metadata.name,READY:.status.readyReplicas,DESIRED:.spec.replicas,UP-TO-DATE:.status.updatedReplicas"

    # Pod 状态
    kubectl get pods -n $NAMESPACE -l "$INSTANCE_LABEL" $KUBECTL_ARGS \
        -o custom-columns="NAME:.metadata.name,STATUS:.status.phase,RESTARTS:.status.containerStatuses[0].restartCount,AGE:.metadata.creationTimestamp"

    # 异常事件
    WARNINGS=$(kubectl get events -n $NAMESPACE $KUBECTL_ARGS \
        --field-selector type=Warning --sort-by='.lastTimestamp' 2>/dev/null | tail -5)
    if [ -n "$WARNINGS" ]; then
        echo ""
        echo "[WARN] 异常事件:"
        echo "$WARNINGS"
    fi

    # 检查是否全部就绪
    NOT_READY=$(kubectl get deployment -n $NAMESPACE -l "$INSTANCE_LABEL" $KUBECTL_ARGS \
        -o jsonpath='{range .items[*]}{.metadata.name}:{.status.readyReplicas}/{.spec.replicas}{"\n"}{end}' \
        | grep -v -E "^[^:]+:([0-9]+)/\1$" | wc -l | tr -d ' ')

    if [ "$NOT_READY" -eq 0 ]; then
        echo ""
        echo "[SUCCESS] ✓ 所有 Deployment 已就绪"
        break
    fi

    sleep $INTERVAL
done
```

**Compose 监控：**

```bash
while true; do
    docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Health}}"

    # 检查是否全部 healthy
    UNHEALTHY=$(docker compose ps --format json | jq -r 'select(.Health != "healthy") | .Name')
    if [ -z "$UNHEALTHY" ]; then
        echo "[SUCCESS] ✓ 所有容器 healthy"
        break
    fi

    sleep $INTERVAL
done
```

#### Step 3: 异常处理

**检测到的异常类型及处理：**

| 异常 | 处理方式 |
|------|---------|
| ImagePullBackOff | 报告镜像拉取失败，检查 tag 和 registry 权限 |
| CrashLoopBackOff | ⚠️ **停止监控**，输出 Pod 日志，建议检查应用代码 |
| OOMKilled | 报告内存不足，建议调整 resource limits |
| Pending (长时间) | 检查节点资源和调度约束 |
| CreateContainerConfigError | 报告配置错误，检查 ConfigMap/Secret |

**CrashLoopBackOff 特殊处理（应用逻辑问题）：**

```
[ERROR] 检测到 Pod 持续崩溃 (CrashLoopBackOff)

容器: myapp-core-5f8b9c7d4-x2j9k
重启次数: 5
最近日志:
  panic: runtime error: index out of range [3]
  goroutine 1 [running]:
  main.handleRequest(...)
      /app/handlers/user.go:42

⚠️ 这是应用逻辑错误，部署监控已停止。
建议:
  1. 检查 handlers/user.go:42 的数组越界问题
  2. 修复后重新构建镜像
  3. 使用 /deploy run uat core 重新部署

如需回滚到上一版本:
  kubectl rollout undo deployment/myapp-core -n $NAMESPACE
```

#### Step 4: 监控结束

**成功：**
```
[SUCCESS] 部署完成
  耗时: 45s
  组件: core (1/1), ops (1/1), admin (1/1)
  环境: uat
```

**失败（非逻辑问题）：**
提供具体修复建议（配置、资源、网络）。

**失败（逻辑问题）：**
停止监控，输出诊断信息，明确建议转交处理。

### 注意事项

- 监控期间不执行任何修改操作
- CrashLoopBackOff 等应用错误立即停止并报告
- 提供回滚命令供用户选择
- 超时后不自动重试，等待用户指示
