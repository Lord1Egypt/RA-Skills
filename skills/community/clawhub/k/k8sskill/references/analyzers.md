# K8sSkill 分析器详细说明

## 分析器架构

K8sSkill的分析器基于SRE最佳实践设计，采用模块化架构，每个分析器专注于特定Kubernetes资源的故障检测。

```
┌─────────────────────────────────────────────────────────────┐
│                      BaseAnalyzer                            │
│                    （分析器基类）                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ PodAnalyzer │  │ Deployment  │  │  Service    │         │
│  │             │  │  Analyzer   │  │  Analyzer   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  PVCAnalyzer│  │  NodeAnalyzer│  │ EventAnalyzer│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## PodAnalyzer

### 检测逻辑（基于Kubernetes官方文档）

#### 1. Pending状态检测
```python
# 检查Pod是否处于Pending状态
if pod.status.phase == "Pending":
    # 检查调度失败原因
    for condition in pod.status.conditions:
        if condition.type == "PodScheduled" and condition.reason == "Unschedulable":
            # 记录故障：无法调度
```

**常见原因：**
- 节点资源不足（CPU/内存）
- 亲和性规则无法满足
- 污点（Taint）阻止调度
- PVC未绑定

#### 2. Container状态检测

**CrashLoopBackOff检测：**
```python
if container.state.waiting.reason == "CrashLoopBackOff":
    # 获取上次终止原因
    last_reason = container.last_state.terminated.reason
    # 常见原因：OOMKilled、Error、Completed
```

**ImagePullBackOff检测：**
```python
if container.state.waiting.reason == "ImagePullBackOff":
    # 镜像拉取失败
    # 可能原因：镜像不存在、仓库认证失败、网络问题
```

**错误状态列表（基于Kubernetes规范）：**
```python
ERROR_REASONS = [
    "CrashLoopBackOff",      # 容器反复崩溃
    "ImagePullBackOff",      # 镜像拉取失败
    "CreateContainerConfigError",  # 容器配置错误
    "PreCreateHookError",    # 创建前钩子错误
    "CreateContainerError",  # 创建容器错误
    "PreStartHookError",     # 启动前钩子错误
    "RunContainerError",     # 运行容器错误
    "ImageInspectError",     # 镜像检查错误
    "ErrImagePull",          # 镜像拉取错误
    "ErrImageNeverPull",     # 镜像永不拉取
    "InvalidImageName"       # 无效镜像名
]
```

#### 3. 健康检查失败
```python
# Pod运行中但容器未就绪
if not container.ready and pod.status.phase == "Running":
    # 检查Events获取健康检查失败详情
    # 常见原因：readinessProbe配置错误、依赖服务不可用
```

### 故障模式与解决方案

| 故障现象 | 检测方法 | 修复建议 |
|---------|---------|---------|
| CrashLoopBackOff | container.state.waiting.reason | 1. 查看日志<br>2. 检查资源限制<br>3. 验证配置 |
| OOMKilled | last_state.terminated.reason | 1. 增加内存限制<br>2. 检查内存泄漏 |
| ImagePullBackOff | container.state.waiting.reason | 1. 检查镜像标签<br>2. 验证仓库权限 |
| Pending/Unschedulable | pod.condition.reason | 1. 检查节点资源<br>2. 检查亲和性规则 |
| NotReady | container.ready == False | 1. 检查健康检查配置<br>2. 查看应用日志 |

## DeploymentAnalyzer

### 检测逻辑（基于Kubernetes官方文档）

#### 1. 副本可用性检测
```python
desired = spec.replicas or 0
available = status.available_replicas or 0

if available < desired:
    # 记录故障：可用副本不足
```

#### 2. 滚动更新状态检测
```python
if updated < desired:
    # 滚动更新进行中或停滞
    # 检查Progressing条件
    for condition in status.conditions:
        if condition.type == "Progressing" and condition.status == "False":
            # 更新进度停滞
```

### 故障模式

| 故障现象 | 检测方法 | 修复建议 |
|---------|---------|---------|
| 可用副本不足 | available < desired | 检查Pod状态、资源配额 |
| 滚动更新停滞 | Progressing=False | 检查新ReplicaSet |
| 进度超时 | ProgressDeadlineExceeded | 增加进度超时时间 |

## ServiceAnalyzer

### 检测逻辑（基于Kubernetes官方文档）

#### 端点检测
```python
# 获取Service对应的Endpoints
endpoints = v1.read_namespaced_endpoints(name, namespace)

# 检查是否有可用端点
has_endpoints = False
for subset in endpoints.subsets:
    if subset.addresses:
        has_endpoints = True
        break

if not has_endpoints:
    # 记录故障：无可用端点
```

### 故障模式

| 故障现象 | 检测方法 | 修复建议 |
|---------|---------|---------|
| 端点为空 | endpoints.subsets为空 | 1. 检查Pod标签<br>2. 检查Pod状态 |
| Endpoints不存在 | ApiException 404 | 检查Service配置 |
| 选择器不匹配 | Pod标签与selector不符 | 修正标签或选择器 |

## 通用故障严重级别定义

```python
class Severity(Enum):
    CRITICAL = "critical"    # 服务中断、数据丢失风险
    WARNING = "warning"      # 性能下降、潜在问题  
    INFO = "info"           # 提示信息、优化建议
```

### 分级标准

**CRITICAL：**
- Pod处于CrashLoopBackOff
- 可用副本为0
- ImagePullBackOff持续
- 数据丢失风险

**WARNING：**
- 可用副本不足（但>0）
- 健康检查失败
- 资源压力高
- 配置潜在问题

**INFO：**
- 滚动更新进行中
- 非关键配置建议
- 优化提示

## 分析器列表

| 分析器 | 功能描述 |
|-------|---------|
| PodAnalyzer | Pod状态、容器崩溃、健康检查 |
| DeploymentAnalyzer | 副本数、滚动更新状态 |
| ServiceAnalyzer | Endpoint、选择器匹配 |
| PVCAnalyzer | 存储绑定、供应状态 |
| NodeAnalyzer | 节点状态、资源压力 |
| IngressAnalyzer | Ingress配置、TLS证书 |
| EventAnalyzer | 警告事件分析 |
| StatefulSetAnalyzer | 有状态应用检查 |
| JobAnalyzer | 批处理任务状态 |
| CronJobAnalyzer | 定时任务调度 |
| HPAAnalyzer | 自动伸缩配置 |
| ConfigMapAnalyzer | 配置使用情况 |
| ReplicaSetAnalyzer | 副本创建状态 |
| NetworkPolicyAnalyzer | 网络策略检查 |
| PDBAnalyzer | 中断预算配置 |
| StorageAnalyzer | 存储类和PV状态 |
| SecurityAnalyzer | 安全上下文检查 |
| SecretAnalyzer | 密钥使用情况 |
| GatewayAnalyzer | Gateway API配置 |
| HTTPRouteAnalyzer | HTTP路由配置 |
| WebhookAnalyzer | 准入控制器配置 |

## 扩展新分析器

### 步骤：

1. **创建分析器类**
```python
class CustomAnalyzer(BaseAnalyzer):
    def analyze(self, namespace: str = "", label_selector: str = "") -> List[AnalysisResult]:
        results = []
        # 实现分析逻辑
        return results
```

2. **注册到K8sAnalyzer**
```python
self.analyzers = {
    "pod": PodAnalyzer(),
    "custom": CustomAnalyzer(),  # 添加新分析器
}
```

3. **添加意图关键词**
```python
INTENT_MAP = {
    "custom": ["custom", "自定义", "特定关键词"],
}
```

## 参考

- Kubernetes API: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/
- kubernetes-python: https://github.com/kubernetes-client/python
- Kubernetes Troubleshooting: https://kubernetes.io/docs/tasks/debug/
