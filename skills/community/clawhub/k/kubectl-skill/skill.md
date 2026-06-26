# kubectl

Kubernetes 命令行工具 (kubectl)，用于与 Kubernetes 集群进行交互和管理资源。

## 何时使用

- 管理 Kubernetes 资源（Pod、Deployment、Service 等）
- 查看集群状态和日志
- 调试应用程序和容器
- 部署应用到集群
- 配置集群访问和上下文切换
- 执行容器内的命令
- 端口转发到 Pod

## 基本语法

```shell
kubectl [command] [TYPE] [NAME] [flags]
```

- **command**: 操作，如 `create`、`get`、`describe`、`delete`、`apply`
- **TYPE**: 资源类型，支持单数/复数/缩写（如 `pod`/`pods`/`po`）
- **NAME**: 资源名称，省略则显示所有资源
- **flags**: 可选参数

## 常用命令

### 资源查询

```bash
# 查看所有 Pod
kubectl get pods

# 查看所有 Pod（含节点信息）
kubectl get pods -o wide

# 查看特定 Pod 详情
kubectl describe pod <pod-name>

# 查看所有 Deployment
kubectl get deployments

# 查看所有 Service
kubectl get services

# 查看节点状态
kubectl get nodes

# 查看所有资源
kubectl get all

# 按标签筛选
kubectl get pods -l app=myapp

# 持续监视资源变化
kubectl get pods --watch
```

### 创建与更新资源

```bash
# 从文件创建资源
kubectl apply -f manifest.yaml

# 从目录创建资源
kubectl apply -f ./manifests/

# 从标准输入创建
kubectl apply -f -

# 创建 Deployment
kubectl create deployment <name> --image=<image>

# 暴露 Service
kubectl expose deployment <name> --port=80 --type=LoadBalancer

# 滚动更新镜像
kubectl set image deployment/<name> <container>=<new-image>

# 水平扩展
kubectl scale deployment/<name> --replicas=5
```

### 删除资源

```bash
# 从文件删除
kubectl delete -f manifest.yaml

# 按名称删除 Pod
kubectl delete pod <pod-name>

# 按标签删除
kubectl delete pods -l app=myapp

# 删除所有 Pod
kubectl delete pods --all
```

### 日志与调试

```bash
# 查看 Pod 日志
kubectl logs <pod-name>

# 实时跟踪日志（类似 tail -f）
kubectl logs -f <pod-name>

# 查看指定容器日志
kubectl logs <pod-name> -c <container-name>

# 查看之前容器的日志
kubectl logs <pod-name> --previous

# 在 Pod 中执行命令
kubectl exec <pod-name> -- <command>

# 进入 Pod 交互式 Shell
kubectl exec -it <pod-name> -- /bin/sh

# 进入指定容器的交互式 Shell
kubectl exec -it <pod-name> -c <container> -- /bin/bash

# 端口转发
kubectl port-forward <pod-name> 8080:80

# 复制文件到/从容器
kubectl cp <pod-name>:/path/to/file ./local-file
kubectl cp ./local-file <pod-name>:/path/to/file
```

### 集群管理

```bash
# 查看当前上下文
kubectl config current-context

# 查看所有上下文
kubectl config get-contexts

# 切换上下文
kubectl config use-context <context-name>

# 设置当前上下文的默认命名空间
kubectl config set-context --current --namespace=<namespace>

# 查看集群信息
kubectl cluster-info

# 查看 API 资源列表
kubectl api-resources

# 查看 API 版本
kubectl api-versions
```

### 高级操作

```bash
# 编辑资源（交互式）
kubectl edit deployment/<name>

# 打标签
kubectl label pods <pod-name> env=production

# 添加注解
kubectl annotate pods <pod-name> description="test"

# 查看资源差异
kubectl diff -f manifest.yaml

# 滚动更新管理
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>

# 排空节点（维护前）
kubectl drain <node-name> --ignore-daemonsets

# 标记节点不可调度
kubectl cordon <node-name>

# 标记节点可调度
kubectl uncordon <node-name>

# 查看资源使用情况
kubectl top pods
kubectl top nodes
```

## 资源类型缩写

| 完整名称 | 缩写 |
|---------|------|
| pods | po |
| services | svc |
| deployments | deploy |
| replicasets | rs |
| statefulsets | sts |
| daemonsets | ds |
| configmaps | cm |
| secrets | |
| nodes | no |
| namespaces | ns |
| persistentvolumeclaims | pvc |
| persistentvolumes | pv |
| ingresses | ing |
| jobs | |
| cronjobs | cj |
| serviceaccounts | sa |
| roles | |
| rolebindings | |
| clusterroles | |
| clusterrolebindings | |
| horizontalpodautoscalers | hpa |

## 输出格式

```bash
# JSON 格式
kubectl get pod <name> -o json

# YAML 格式
kubectl get pod <name> -o yaml

# 仅输出资源名称
kubectl get pods -o name

# 自定义列
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase

# JSONPath 输出
kubectl get pods -o jsonpath='{.items[*].metadata.name}'

# 宽格式（含额外信息）
kubectl get pods -o wide
```

## 命名空间操作

```bash
# 指定命名空间
kubectl get pods -n <namespace>

# 查看所有命名空间的资源
kubectl get pods --all-namespaces
kubectl get pods -A

# 创建命名空间
kubectl create namespace <name>
```

## 常用快捷命令

```bash
# 快速查看 Pod 状态
kubectl get pods --all-namespaces

# 快速查看所有事件
kubectl get events --sort-by='.lastTimestamp'

# 删除所有 Evicted Pod
kubectl get pods --all-namespaces --field-selector=status.phase=Failed | grep Evicted | awk '{print $2 " --namespace=" $1}' | xargs -L1 kubectl delete pod

# 强制删除 Terminating 的 Pod
kubectl delete pod <pod-name> --force --grace-period=0
```

## 配置说明

- 默认配置文件位于 `$HOME/.kube/config`
- 可通过 `KUBECONFIG` 环境变量指定其他配置文件
- 可通过 `--kubeconfig` 参数指定配置文件

## 注意事项

- 命令行参数会覆盖默认值和环境变量
- 资源类型不区分大小写
- 名称区分大小写
- 在 Pod 内运行时，kubectl 会自动检测并使用 ServiceAccount 认证
- 使用 `--dry-run=client` 或 `--dry-run=server` 可以预览操作效果而不实际执行

## 参考文档目录

本技能目录下的完整参考文档结构如下，可根据具体问题读取对应文件获取详细参数说明和示例：

### 概述与指南
- `_index.md` - kubectl 命令行工具总览（语法、操作表、资源类型表、输出选项、常用示例、插件）
- `conventions.md` - kubectl 使用约定
- `docker-cli-to-kubectl.md` - Docker 用户迁移到 kubectl 的对照指南
- `introduction.md` - kubectl 简介
- `jsonpath.md` - JSONPath 语法支持
- `quick-reference.md` - 快速参考备忘单
- `kubectl-cmds.md` - kubectl 命令汇总
- `kubectl.md` - kubectl 概述
- `kuberc.md` - kuberc 偏好配置

### 主命令参考（generated）
- `generated/kubectl.md` - kubectl 根命令参数说明
- `generated/kubectl_alpha/` - Alpha 阶段特性命令
- `generated/kubectl_annotate/` - 更新资源注解
- `generated/kubectl_api-resources/` - 列出 API 资源
- `generated/kubectl_api-versions/` - 列出 API 版本
- `generated/kubectl_apply/` - 应用配置（含 edit-last-applied、set-last-applied、view-last-applied）
- `generated/kubectl_attach/` - 挂接到运行中的容器
- `generated/kubectl_auth/` - 授权检查（含 can-i、reconcile、whoami）
- `generated/kubectl_autoscale/` - 自动扩缩
- `generated/kubectl_certificate/` - 证书管理（含 approve、deny）
- `generated/kubectl_cluster-info/` - 集群信息（含 dump）
- `generated/kubectl_completion/` - Shell 补全
- `generated/kubectl_config/` - kubeconfig 管理（含 current-context、delete-cluster、delete-context、delete-user、get-clusters、get-contexts、get-users、rename-context、set、set-cluster、set-context、set-credentials、unset、use-context、view）
- `generated/kubectl_cordon/` - 标记节点不可调度
- `generated/kubectl_cp/` - 文件复制
- `generated/kubectl_create/` - 创建资源（含 clusterrole、clusterrolebinding、configmap、cronjob、deployment、ingress、job、namespace、poddisruptionbudget、priorityclass、quota、role、rolebinding、secret、service、serviceaccount、token）
- `generated/kubectl_debug/` - 调试会话
- `generated/kubectl_delete/` - 删除资源
- `generated/kubectl_describe/` - 资源详情
- `generated/kubectl_diff/` - 配置差异对比
- `generated/kubectl_drain/` - 腾空节点
- `generated/kubectl_edit/` - 交互式编辑
- `generated/kubectl_events/` - 事件列表
- `generated/kubectl_exec/` - 容器内执行命令
- `generated/kubectl_explain/` - 资源文档说明
- `generated/kubectl_expose/` - 暴露服务
- `generated/kubectl_get/` - 查询资源
- `generated/kubectl_kustomize/` - Kustomize 构建
- `generated/kubectl_label/` - 更新标签
- `generated/kubectl_logs/` - 查看日志
- `generated/kubectl_options/` - 全局参数
- `generated/kubectl_patch/` - 更新资源字段
- `generated/kubectl_plugin/` - 插件管理（含 list）
- `generated/kubectl_port-forward/` - 端口转发
- `generated/kubectl_proxy/` - API 代理
- `generated/kubectl_replace/` - 替换资源
- `generated/kubectl_rollout/` - 发布管理（含 history、pause、restart、resume、status、undo）
- `generated/kubectl_run/` - 运行容器
- `generated/kubectl_scale/` - 手动扩缩
- `generated/kubectl_set/` - 设置对象属性（含 env、image、resources、selector、serviceaccount、subject）
- `generated/kubectl_taint/` - 节点污点管理
- `generated/kubectl_top/` - 资源使用监控（含 node、pod）
- `generated/kubectl_uncordon/` - 标记节点可调度
- `generated/kubectl_version/` - 版本信息
- `generated/kubectl_wait/` - 等待资源就绪
