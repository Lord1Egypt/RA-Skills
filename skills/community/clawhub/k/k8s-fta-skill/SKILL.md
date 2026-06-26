---
name: k8s-fta-skill
description: 基于FTA故障树分析法的Kubernetes问题定位和修复工具。当用户遇到k8s集群问题、Pod运行异常、服务访问失败、RBAC权限问题、DNS解析失败、OOMKilled、健康检查失败、网络策略限制、存储挂载问题、HPA扩展问题、API Server连接问题等情况时，使用此技能自动执行kubectl命令进行故障排查和修复。同时支持k3s轻量级Kubernetes发行版的故障排查。Supports both Chinese and English troubleshooting and automated fixing for Kubernetes cluster issues including Pod failures, service access problems, RBAC issues, DNS resolution failures, OOMKilled, health check failures, network policy restrictions, storage mount issues, HPA scaling problems, and API Server connectivity issues. Also supports k3s lightweight Kubernetes distribution.
compatibility:
  tools: ["kubectl", "git", "shell"]
---

# Kubernetes FTA故障树分析技能 / Kubernetes FTA Fault Tree Analysis Skill

## 技能简介 / Skill Introduction

本技能基于FTA（故障树分析）方法，提供系统化的Kubernetes集群故障排查和自动修复功能。通过自动执行kubectl命令，帮助用户快速定位和解决k8s环境中的各种问题，包括Pod运行异常、服务访问失败、网络通信问题、RBAC权限问题、DNS解析失败、OOMKilled、健康检查失败、网络策略限制、存储挂载问题、HPA扩展问题、API Server连接问题等。

This skill provides systematic Kubernetes cluster troubleshooting and automated fixing based on FTA (Fault Tree Analysis) methodology. Through automatic kubectl command execution, it helps users quickly locate and resolve various issues in k8s environments, including Pod failures, service access problems, network communication issues, RBAC permission issues, DNS resolution failures, OOMKilled, health check failures, network policy restrictions, storage mount issues, HPA scaling problems, API Server connectivity issues, and more.

## 工作方式 / Working Method

### 自动化故障排查流程

1. **用户描述问题**：用户描述k8s集群中遇到的问题
2. **自动执行命令**：技能根据FTA流程，自动执行相应的kubectl命令
3. **分析输出结果**：技能分析命令输出，识别问题原因
4. **执行下一步操作**：技能根据分析结果，自动执行下一步排查命令
5. **提供修复方案**：技能提供具体的修复建议，必要时自动执行修复命令
6. **验证修复效果**：技能验证修复是否成功，确保问题得到解决

### 安全性考虑

- **只读操作优先**：优先执行只读命令（如kubectl get、kubectl describe、kubectl logs）
- **修改操作确认**：执行修改操作前，先向用户确认操作内容
- **环境检查**：执行命令前检查k8s/k3s环境是否可用
- **错误处理**：遇到错误时自动重试或提供替代方案
- **回滚机制**：对于修改操作，提供回滚选项

## 故障排查流程

### 1. 开始排查

自动执行以下命令检查集群中所有Pod的状态：

```bash
kubectl get pods --all-namespaces
```

**分析输出**：
- 检查是否有Pod处于非Running状态
- 识别异常状态的Pod（Pending、CrashLoopBackOff、Error等）
- 记录异常Pod的名称和命名空间

### 2. Pod状态检查

#### 2.1 Pod状态分析

根据第一步的结果，对异常状态的Pod执行详细检查：

```bash
kubectl describe pod <pod-name> -n <namespace>
```

**分析输出**：
- 检查Events部分，识别调度失败、镜像拉取失败等问题
- 检查Container State，识别容器启动失败、运行时错误等
- 检查Conditions，识别Pod就绪状态、调度状态等

#### 2.2 根据状态执行相应检查

**Pending状态**：
```bash
kubectl describe node <node-name>
kubectl get resourcequota -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>
```

**CrashLoopBackOff状态**：
```bash
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> --previous -n <namespace>
```

**Error状态**：
```bash
kubectl logs <pod-name> -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
```

### 3. 资源配额检查

如果Pod处于Pending状态且资源不足，检查资源配额：

```bash
kubectl get resourcequota -n <namespace>
kubectl describe resourcequota <quota-name> -n <namespace>
kubectl describe node <node-name>
```

**分析输出**：
- 检查ResourceQuota是否已满
- 检查节点资源使用情况
- 识别资源瓶颈（CPU、内存、存储等）

**自动修复建议**：
- 建议增加ResourceQuota限制
- 建议调整Pod资源请求和限制
- 建议扩容节点资源

### 4. 存储问题检查

如果存在PersistentVolumeClaim问题，检查存储配置：

```bash
kubectl get pvc -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>
kubectl get pv
kubectl describe pv <pv-name>
```

**分析输出**：
- 检查PVC是否处于Bound状态
- 检查PV是否可用
- 检查存储类（StorageClass）配置
- 识别存储驱动问题

**自动修复建议**：
- 建议检查存储类配置
- 建议修复PV/PVC绑定问题
- 建议检查存储驱动状态

### 5. 镜像问题检查

如果存在镜像拉取失败，检查镜像配置：

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get pods -n <namespace> -o jsonpath='{.items[*].spec.containers[*].image}'
```

**分析输出**：
- 检查镜像名称是否正确
- 检查镜像Tag是否存在
- 检查是否需要从私有仓库拉取镜像
- 识别认证问题

**自动修复建议**：
- 建议修正镜像名称和Tag
- 建议创建或更新imagePullSecret
- 建议检查私有仓库访问权限

### 6. 容器启动问题检查

如果Pod处于CrashLoopBackOff状态，检查容器日志：

```bash
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl logs <pod-name> -n <namespace> --previous --tail=100
```

**分析输出**：
- 检查应用程序错误日志
- 检查配置错误
- 检查依赖服务连接失败
- 识别启动失败原因

**自动修复建议**：
- 建议修复应用程序错误
- 建议修正配置文件
- 建议检查依赖服务状态
- 建议增加健康检查超时时间

### 7. 网络通信检查

执行端口转发测试Pod内部服务是否正常：

```bash
kubectl port-forward <pod-name> 8080:<pod-port> -n <namespace>
```

**分析输出**：
- 检查端口转发是否成功
- 测试本地端口访问
- 验证容器内部服务是否正常

**自动修复建议**：
- 建议检查容器端口配置
- 建议检查应用程序监听地址
- 建议检查网络策略限制

### 8. Service配置检查

如果服务访问失败，检查Service配置：

```bash
kubectl get svc -n <namespace>
kubectl describe svc <service-name> -n <namespace>
kubectl get endpoints <service-name> -n <namespace>
```

**分析输出**：
- 检查Service类型配置
- 检查端口映射是否正确
- 检查Pod选择器是否匹配
- 检查后端Pod是否就绪

**自动修复建议**：
- 建议修正Service端口配置
- 建议确保Pod标签匹配
- 建议检查网络策略
- 建议检查后端Pod状态

### 9. Ingress配置检查

如果通过Ingress访问失败，检查Ingress配置：

```bash
kubectl get ingress -n <namespace>
kubectl describe ingress <ingress-name> -n <namespace>
kubectl get svc -n <namespace>
```

**分析输出**：
- 检查Ingress规则配置
- 检查后端Service配置
- 检查Ingress控制器状态
- 检查TLS证书配置

**自动修复建议**：
- 建议修正Ingress规则
- 建议检查Ingress控制器
- 建议检查后端Service状态
- 建议更新TLS证书

### 10. 节点状态检查

如果多个Pod出现问题，检查节点状态：

```bash
kubectl get nodes
kubectl describe node <node-name>
kubectl top nodes
```

**分析输出**：
- 检查节点是否处于NotReady状态
- 检查节点资源使用情况
- 检查kubelet状态
- 识别节点问题

**自动修复建议**：
- 建议重启kubelet服务
- 建议检查节点资源
- 建议排查节点网络问题
- 建议替换故障节点

### 11. OOMKilled问题检查

如果Pod被OOMKilled，检查内存使用：

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl top pod <pod-name> -n <namespace>
kubectl top nodes
```

**分析输出**：
- 检查Pod内存限制设置
- 检查实际内存使用情况
- 识别内存泄漏
- 检查节点内存压力

**自动修复建议**：
- 建议增加Pod内存限制
- 建议优化应用程序内存使用
- 建议排查内存泄漏
- 建议增加节点内存

### 12. 健康检查失败检查

如果Pod因健康检查失败而重启，检查健康检查配置：

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

**分析输出**：
- 检查livenessProbe配置
- 检查readinessProbe配置
- 检查健康检查端点状态
- 识别健康检查失败原因

**自动修复建议**：
- 建议调整健康检查参数
- 建议增加初始延迟时间
- 建议修复健康检查端点
- 建议优化应用程序启动时间

### 13. RBAC权限问题检查

如果遇到权限拒绝错误，检查RBAC配置：

```bash
kubectl auth can-i <verb> <resource> --as=<user> -n <namespace>
kubectl get role -n <namespace>
kubectl get clusterrole
kubectl get rolebinding -n <namespace>
kubectl get clusterrolebinding
```

**分析输出**：
- 检查ServiceAccount权限
- 检查Role/ClusterRole配置
- 检查RoleBinding/ClusterRoleBinding绑定
- 识别权限不足问题

**自动修复建议**：
- 建议创建或更新Role/ClusterRole
- 建议创建或更新RoleBinding/ClusterRoleBinding
- 建议为ServiceAccount分配足够权限
- 建议检查权限策略

### 14. DNS解析问题检查

如果Pod无法解析域名，检查DNS配置：

```bash
kubectl exec -it <pod-name> -n <namespace> -- nslookup <domain>
kubectl exec -it <pod-name> -n <namespace> -- cat /etc/resolv.conf
kubectl get svc -n kube-system kube-dns
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

**分析输出**：
- 检查CoreDNS/Kube-DNS状态
- 检查DNS配置文件
- 检查网络策略是否阻止DNS
- 识别DNS解析失败原因

**自动修复建议**：
- 建议重启CoreDNS Pod
- 建议检查DNS配置
- 建议检查网络策略
- 建议检查Service DNS名称

### 15. 网络策略限制检查

如果Pod无法访问其他服务，检查网络策略：

```bash
kubectl get networkpolicies --all-namespaces
kubectl describe networkpolicy <policy-name> -n <namespace>
kubectl get pods -n <namespace> -o wide
```

**分析输出**：
- 检查网络策略规则
- 检查Pod标签是否匹配
- 检查流量是否被阻止
- 识别网络策略限制

**自动修复建议**：
- 建议调整网络策略规则
- 建议确保Pod标签匹配
- 建议允许必要的网络流量
- 建议删除限制性网络策略

### 16. 持久化存储挂载问题检查

如果Pod无法挂载存储卷，检查存储配置：

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get pvc -n <namespace>
kubectl get pv
kubectl get storageclass
```

**分析输出**：
- 检查PVC绑定状态
- 检查PV可用性
- 检查存储类配置
- 识别挂载失败原因

**自动修复建议**：
- 建议修复PVC/PV绑定
- 建议检查存储类配置
- 建议检查存储驱动
- 建议调整存储权限

### 17. 容器启动超时检查

如果Pod因启动超时而失败，检查启动配置：

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

**分析输出**：
- 检查应用程序启动时间
- 检查健康检查配置
- 检查terminationGracePeriodSeconds
- 识别启动超时原因

**自动修复建议**：
- 建议优化应用程序启动
- 建议增加健康检查初始延迟
- 建议增加terminationGracePeriodSeconds
- 建议检查依赖服务启动时间

### 18. 节点污点和容忍度检查

如果Pod无法调度到特定节点，检查污点配置：

```bash
kubectl describe node <node-name>
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
```

**分析输出**：
- 检查节点污点配置
- 检查Pod容忍度配置
- 检查节点选择器
- 识别调度失败原因

**自动修复建议**：
- 建议为Pod添加容忍度
- 建议调整节点污点
- 建议修改节点选择器
- 建议检查节点标签

### 19. Pod优先级和抢占检查

如果Pod被抢占或无法调度，检查优先级配置：

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get priorityclass
kubectl get pods -n <namespace> --sort-by=.spec.priorityClassName
```

**分析输出**：
- 检查Pod优先级类
- 检查集群资源使用
- 检查高优先级Pod状态
- 识别抢占问题

**自动修复建议**：
- 建议调整Pod优先级
- 建议增加集群资源
- 建议检查资源请求设置
- 建议优化Pod调度

### 20. HPA/VPA自动扩展问题检查

如果自动扩展不工作，检查扩展配置：

```bash
kubectl get hpa -n <namespace>
kubectl describe hpa <hpa-name> -n <namespace>
kubectl get vpa -n <namespace>
kubectl describe vpa <vpa-name> -n <namespace>
kubectl get pods -n kube-system -l k8s-app=metrics-server
```

**分析输出**：
- 检查HPA/VPA配置
- 检查metrics-server状态
- 检查Pod资源使用
- 检查扩展指标

**自动修复建议**：
- 建议修复HPA/VPA配置
- 建议检查metrics-server
- 建议调整扩展参数
- 建议检查资源使用率

### 21. Pod中断预算问题检查

如果Pod在更新时被意外终止，检查PDB配置：

```bash
kubectl get pdb -n <namespace>
kubectl describe pdb <pdb-name> -n <namespace>
kubectl get deployment -n <namespace>
kubectl describe deployment <deployment-name> -n <namespace>
```

**分析输出**：
- 检查PDB配置
- 检查最小可用Pod数量
- 检查更新策略
- 识别中断问题

**自动修复建议**：
- 建议调整PDB参数
- 建议修改更新策略
- 建议检查Pod状态
- 建议优化滚动更新

### 22. 容器运行时问题检查

如果容器无法启动或运行异常，检查运行时状态：

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
systemctl status docker  # 或 containerd
docker ps  # 或 crictl ps
```

**分析输出**：
- 检查容器运行时状态
- 检查容器运行时日志
- 检查镜像兼容性
- 识别运行时问题

**自动修复建议**：
- 建议重启容器运行时服务
- 建议检查镜像兼容性
- 建议检查运行时配置
- 建议更新容器运行时版本

### 23. 集群证书过期检查

如果遇到证书相关错误，检查证书状态：

```bash
kubeadm certs check-expiration
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates
kubectl get pods -n kube-system | grep -E 'apiserver|controller-manager|scheduler'
```

**分析输出**：
- 检查证书过期时间
- 检查证书有效性
- 检查组件证书状态
- 识别过期证书

**自动修复建议**：
- 建议更新过期证书
- 建议重启相关组件
- 建议检查证书配置
- 建议设置证书监控

### 24. API Server连接问题检查

如果无法连接到API Server，检查API Server状态：

```bash
kubectl cluster-info
kubectl get componentstatuses
kubectl get pods -n kube-system | grep apiserver
kubectl logs -n kube-system kube-apiserver-<node-name>
```

**分析输出**：
- 检查API Server状态
- 检查kubeconfig配置
- 检查网络连接
- 检查API Server日志

**自动修复建议**：
- 建议重启API Server
- 建议检查kubeconfig配置
- 建议检查网络连接
- 建议检查防火墙规则

### 25. etcd集群问题检查

如果etcd集群出现问题，检查etcd状态：

```bash
kubectl get pods -n kube-system | grep etcd
kubectl logs -n kube-system etcd-<node-name>
ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key endpoint health
etcdctl --endpoints=https://[127.0.0.1]:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key endpoint status --write-out=table
```

**分析输出**：
- 检查etcd Pod状态
- 检查etcd集群健康
- 检查etcd数据备份
- 检查etcd存储空间

**自动修复建议**：
- 建议重启etcd Pod
- 建议清理etcd存储空间
- 检查etcd集群配置
- 建议恢复etcd备份

## 错误处理和重试机制

### 错误处理策略

1. **命令执行失败**：
   - 记录错误信息
   - 分析失败原因
   - 提供替代命令
   - 自动重试（最多3次）

2. **权限不足**：
   - 检查kubectl配置
   - 建议检查kubeconfig
   - 建议检查RBAC权限
   - 提供权限修复建议

3. **网络连接问题**：
   - 检查API Server连接
   - 建议检查网络配置
   - 建议检查防火墙规则
   - 提供网络诊断命令

4. **资源不足**：
   - 检查集群资源使用
   - 建议增加资源配额
   - 建议优化资源使用
   - 提供资源扩容建议

### 重试机制

- **自动重试**：对于临时性错误，自动重试命令
- **指数退避**：重试间隔采用指数退避策略
- **最大重试次数**：默认3次，可配置
- **重试超时**：每次重试超时时间递增

## 输出格式

### 问题诊断报告

```
### 问题诊断报告 / Issue Diagnosis Report

**问题描述 / Issue Description**: [用户描述的问题]

**诊断结果 / Diagnosis Result**:
- 问题类型 / Issue Type: [识别的问题类型]
- 严重程度 / Severity: [Critical/High/Medium/Low]
- 影响范围 / Impact: [受影响的Pod、Service、Node等]

**根本原因 / Root Cause**:
- 主要原因 / Primary Cause: [主要问题原因]
- 次要原因 / Secondary Cause: [次要问题原因]
- 相关组件 / Affected Components: [受影响的k8s组件]

**执行的检查 / Performed Checks**:
1. [检查1] - 结果: [结果]
2. [检查2] - 结果: [结果]
3. [检查3] - 结果: [结果]

**修复建议 / Fix Recommendations**:
- 立即行动 / Immediate Action: [建议的立即操作]
- 短期方案 / Short-term Solution: [短期解决方案]
- 长期方案 / Long-term Solution: [长期解决方案]

**预防措施 / Prevention Measures**:
- [预防措施1]
- [预防措施2]
- [预防措施3]
```

### 自动修复执行

对于可以自动修复的问题，技能会执行以下操作：

```bash
# 示例：自动修复Pod资源限制
kubectl patch pod <pod-name> -n <namespace> --type='json' -p='[{"op": "replace", "path": "/spec/containers/0/resources/limits/memory", "value": "2Gi"}]'

# 示例：自动重启失败的Pod
kubectl delete pod <pod-name> -n <namespace>

# 示例：自动更新Service端口
kubectl patch svc <service-name> -n <namespace> --type='json' -p='[{"op": "replace", "path": "/spec/ports/0/targetPort", "value": 8080}]'
```

## 使用示例

### 示例1：Pod处于CrashLoopBackOff状态

**用户输入**：我的Pod一直处于CrashLoopBackOff状态，如何排查？

**技能自动执行**：
1. `kubectl get pods -n <namespace>` - 识别异常Pod
2. `kubectl describe pod <pod-name> -n <namespace>` - 获取详细信息
3. `kubectl logs <pod-name> -n <namespace>` - 查看当前日志
4. `kubectl logs <pod-name> --previous -n <namespace>` - 查看之前日志

**分析结果**：
- 问题类型：容器启动失败
- 严重程度：High
- 根本原因：应用程序启动错误

**自动修复建议**：
- 立即行动：检查应用程序日志，修复启动错误
- 短期方案：增加健康检查超时时间
- 长期方案：优化应用程序启动流程

### 示例2：Service无法访问

**用户输入**：我的Service创建成功但无法访问，如何排查？

**技能自动执行**：
1. `kubectl get svc -n <namespace>` - 检查Service状态
2. `kubectl describe svc <service-name> -n <namespace>` - 获取详细信息
3. `kubectl get endpoints <service-name> -n <namespace>` - 检查后端Pod
4. `kubectl port-forward svc/<service-name> 8080:<service-port> -n <namespace>` - 测试访问

**分析结果**：
- 问题类型：Service访问失败
- 严重程度：Medium
- 根本原因：后端Pod未就绪

**自动修复建议**：
- 立即行动：检查后端Pod状态，确保Pod就绪
- 短期方案：调整Service选择器，确保Pod标签匹配
- 长期方案：实施健康检查，确保Pod质量

## 总结

本技能通过FTA故障树分析方法，提供系统化的Kubernetes故障排查和自动修复功能。技能能够自动执行kubectl命令，分析输出结果，识别问题原因，并提供具体的修复建议。技能包含完善的错误处理和重试机制，确保排查过程的稳定性和可靠性。

使用此技能时，用户只需描述遇到的问题，技能会自动执行相应的排查命令，分析结果，并提供修复方案。对于可以自动修复的问题，技能会直接执行修复操作；对于需要人工干预的问题，技能会提供详细的修复指导。

技能支持k8s和k3s环境，适用于各种规模的Kubernetes集群，是k8s运维人员的得力助手。