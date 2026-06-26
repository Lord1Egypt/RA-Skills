---
name: k8sskill
description: 诊断Kubernetes集群问题。用户问Pod崩溃、部署失败、服务不可访问等K8s问题时使用。
---

# K8sSkill - Kubernetes智能诊断助手

## AI执行指南（必读）

**执行诊断时遵守以下规则：**

**正确做法：**
```powershell
cd scripts
python -c "from orchestrator import analyze_cluster; print(analyze_cluster('集群有什么问题'))"
```

指定命名空间：
```powershell
cd scripts
python -c "from orchestrator import analyze_cluster; print(analyze_cluster('检查Pod问题', namespace='kubesphere-logging-system'))"
```

**禁止做法：**
1. 禁止创建任何额外的Python脚本文件
2. 禁止创建报告输出文件
3. 禁止封装orchestrator.py的功能

---

## 使用方式

用户用自然语言描述问题，AI自动调用k8sskill执行诊断。

**触发示例：**
- "检查Pod为什么崩溃"
- "部署失败了怎么回事"
- "为什么服务无法访问"
- "节点有问题"
- "存储绑定失败"
- "查看最近事件"
- "集群有什么问题"

---

## 支持的查询类型

| 查询类型 | 示例问法 |
|---------|---------|
| **Pod问题** | "检查Pod为什么崩溃" / "为什么有Pod一直在重启" |
| **Deployment问题** | "部署失败了怎么回事" / "deployment rollout卡住了" |
| **Service问题** | "为什么服务无法访问" / "访问不了我的服务" |
| **节点问题** | "节点有问题" / "检查节点健康状态" |
| **存储问题** | "存储绑定失败" / "PVC无法挂载" |
| **事件日志** | "查看最近事件" / "集群有什么警告" |
| **全量检查** | "集群有什么问题" / "检查所有资源" |

---

## 核心能力

### 智能资源诊断（21种分析器）

**工作负载分析器：**
- **PodAnalyzer** - 检测CrashLoopBackOff、OOMKilled、ImagePullBackOff等状态
- **DeploymentAnalyzer** - 检查滚动更新失败、副本不足等问题
- **ServiceAnalyzer** - 诊断端点缺失、负载均衡异常
- **StatefulSetAnalyzer** - 检查Headless Service、StorageClass、Pod就绪状态
- **JobAnalyzer** - 检测Job挂起、执行失败、超时问题
- **CronJobAnalyzer** - 检查Cron表达式格式、调度配置
- **ReplicaSetAnalyzer** - 检查副本创建失败、ReplicaFailure条件
- **HPAAnalyzer** - 检查自动伸缩配置、目标资源存在性、扩容限制

**存储和网络分析器：**
- **PVCAnalyzer** - 检测存储绑定失败、ProvisioningFailed错误
- **IngressAnalyzer** - 检查IngressClass配置、后端Service存在性、TLS证书
- **GatewayAnalyzer** - 检查Gateway API配置、GatewayClass存在性、接受状态
- **HTTPRouteAnalyzer** - 检查HTTPRoute引用的Gateway、后端Service存在性
- **NetworkPolicyAnalyzer** - 检查网络策略范围、未应用的策略

**集群分析器：**
- **NodeAnalyzer** - 监控节点就绪状态、内存/磁盘/PID压力
- **EventAnalyzer** - 分析最近警告事件、异常事件模式
- **StorageAnalyzer** - 检查StorageClass配置、PV状态、PVC绑定
- **SecurityAnalyzer** - 检查ServiceAccount使用、容器安全上下文、特权模式
- **WebhookAnalyzer** - 检查Validating/Mutating Webhook的后端Service和Pod

**配置分析器：**
- **ConfigMapAnalyzer** - 检测未使用的ConfigMap、空配置
- **SecretAnalyzer** - 检查未使用的Secret、TLS证书格式、Docker Registry配置
- **PDBAnalyzer** - 检查PodDisruptionBudget中断限制、选择器匹配

### 自然语言交互

| 用户输入示例 | 执行的分析 |
|-------------|-----------|
| "检查我的Pod为什么崩溃" | PodAnalyzer - 检查容器状态和事件 |
| "为什么服务无法访问" | ServiceAnalyzer + IngressAnalyzer |
| "部署失败了怎么回事" | DeploymentAnalyzer + Event分析 |
| "存储绑定失败" | PVCAnalyzer - 检查PVC状态 |
| "节点有问题" | NodeAnalyzer - 检查节点健康 |
| "查看最近事件" | EventAnalyzer - 分析警告事件 |
| "集群有什么问题" | 全量分析所有资源 |

### 分析结果展示
- **结构化输出**：清晰的表格和列表展示问题
- **严重程度分级**：Critical/Warning/Info 三级分类
- **修复建议**：基于SRE经验的逐步解决方案
- **相关资源关联**：展示问题资源的上下游依赖

---

## 使用示例

```python
# 在 scripts/ 目录下执行
from orchestrator import AnalyzerOrchestrator, analyze_cluster

# 方式1: 使用编排器
orchestrator = AnalyzerOrchestrator()
results = orchestrator.analyze("检查Pod问题", namespace="default")
report = orchestrator.format_report(results)
print(report)

# 方式2: 使用便捷函数
report = analyze_cluster("检查集群问题", namespace="production")
print(report)
```

---

## 配置

### kubeconfig支持
支持3种配置方式：
1. 项目自带：`config/k8s-Test-admin.conf`
2. 默认位置：`~/.kube/config`
3. 环境变量：`KUBECONFIG=/path/to/config`

### 快速验证配置
```python
# 在 scripts/ 目录下执行
from core import verify_k8s_connection
success, message = verify_k8s_connection()
print(message)
```

---

## 参考文档

- [分析器详细说明](references/analyzers.md) - 各分析器的检测逻辑和故障模式
- [故障排查手册](references/troubleshooting.md) - 常见问题的排查步骤

---

## 依赖要求

- Python 3.8+
- kubernetes-python 客户端
- 有效的kubeconfig文件

---

## 使用限制

- 本skill为**诊断工具**，不会修改集群资源
- 需要集群的**只读权限**即可运行
- 大型集群（>1000 Pod）分析可能需要等待数秒
- 首次使用前请确保kubeconfig配置正确

---

**版本**: 1.0.0  
**最后更新**: 2026-04-03
