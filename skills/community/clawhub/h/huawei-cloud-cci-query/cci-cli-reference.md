# CCI hcloud 命令参考

> 基于 KooCLI Version 7.2.12 实测。CCI 服务采用 Kubernetes 风格 API，操作名为 `list*` / `read*` / `get*`。

## ⚠️ 命令名澄清

Issue/Spec 中提到的 `ListInstances` / `ShowInstance` **在 `hcloud CCI` 中不存在**。实测 `hcloud CCI ListInstances --help` 返回：

```
[USE_ERROR]Operation ListInstances is not supported.
```

CCI 的"实例"在 Kubernetes 语义下是 **Pod**。查询 Pod 列表 → `listCoreV1NamespacedPod`；查询 Pod 详情 → `readCoreV1NamespacedPod`。

## 命令格式

```
hcloud CCI <Operation> --cli-region=<region> --cli-profile=<profile> [--path-params] [--query-params]
```

- Service：`CCI`（固定）
- Operation：见下表（只列出只读 list/read/get 操作）
- 必填路径参数：`--namespace`、`--name`（视操作而定）
- 可选查询参数：`--label-selector`、`--field-selector`、`--limit`、`--continue`、`--watch`、`--pretty`

## 只读查询命令清单

### 命名空间（Namespace）

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listNamespaces` | GET | `--cli-region` | 列出用户所有命名空间 |
| `listCoreV1Namespace` | GET | `--cli-region` | 列出命名空间（CoreV1） |
| `readCoreV1Namespace` | GET | `--cli-region --name` | 查询指定命名空间详情 |
| `readNamespace` | GET | `--cli-region --name` | 查询命名空间详情 |

**示例**：

```bash
hcloud CCI listNamespaces --cli-region=cn-north-4 --cli-profile=default
```

返回：

```json
{
  "kind": "NamespaceList",
  "apiVersion": "cci/v2",
  "metadata": {},
  "items": []
}
```

### Pod（容器实例）

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listCoreV1NamespacedPod` | GET | `--cli-region --namespace` | 列出命名空间下 Pod |
| `listCoreV1PodForAllNamespaces` | GET | `--cli-region` | 跨命名空间列出所有 Pod |
| `readCoreV1NamespacedPod` | GET | `--cli-region --namespace --name` | 查询指定 Pod 详情 |
| `readCoreV1NamespacedPodStatus` | GET | `--cli-region --namespace --name` | 查询 Pod 状态 |
| `readCoreV1NamespacedPodLog` | GET | `--cli-region --namespace --name` | 查询 Pod 日志 |

**list 可选查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `--label-selector` | string | 标签选择器，如 `app=nginx` |
| `--field-selector` | string | 字段选择器，如 `status.phase=Running` |
| `--limit` | integer | 返回数量上限 |
| `--continue` | string | 分页续传 token |
| `--watch` | boolean | 是否监听变更 |
| `--timeout-seconds` | integer | 超时秒数 |

**示例**：

```bash
hcloud CCI listCoreV1NamespacedPod --cli-region=cn-north-4 --cli-profile=default --namespace=default --label-selector=app=nginx --limit=50
hcloud CCI readCoreV1NamespacedPod --cli-region=cn-north-4 --cli-profile=default --namespace=default --name=my-pod-xxx
```

### Deployment

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listAppsV1NamespacedDeployment` | GET | `--cli-region --namespace` | 列出 Deployment |
| `listAppsV1DeploymentForAllNamespaces` | GET | `--cli-region` | 跨命名空间列出 |
| `listNamespacedDeployments` | GET | `--cli-region --namespace` | 列出（旧 API） |
| `readAppsV1NamespacedDeployment` | GET | `--cli-region --namespace --name` | 查询详情 |
| `readAppsV1NamespacedDeploymentStatus` | GET | `--cli-region --namespace --name` | 查询状态 |
| `readAppsV1NamespacedDeploymentScale` | GET | `--cli-region --namespace --name` | 查询副本数 |
| `readNamespacedDeployment` | GET | `--cli-region --namespace --name` | 查询详情（旧 API） |

### StatefulSet

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listAppsV1NamespacedStatefulSet` | GET | `--cli-region --namespace` | 列出 StatefulSet |
| `listAppsV1StatefulSetForAllNamespaces` | GET | `--cli-region` | 跨命名空间列出 |
| `readAppsV1NamespacedStatefulSet` | GET | `--cli-region --namespace --name` | 查询详情 |
| `readAppsV1NamespacedStatefulSetStatus` | GET | `--cli-region --namespace --name` | 查询状态 |

### Job

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listBatchV1NamespacedJob` | GET | `--cli-region --namespace` | 列出 Job |
| `listBatchV1JobForAllNamespaces` | GET | `--cli-region` | 跨命名空间列出 |
| `readBatchV1NamespacedJob` | GET | `--cli-region --namespace --name` | 查询详情 |
| `readBatchV1NamespacedJobStatus` | GET | `--cli-region --namespace --name` | 查询状态 |

### Service

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listCoreV1NamespacedService` | GET | `--cli-region --namespace` | 列出 Service |
| `listNamespacedServices` | GET | `--cli-region --namespace` | 列出（旧 API） |
| `readCoreV1NamespacedService` | GET | `--cli-region --namespace --name` | 查询详情 |
| `readCoreV1NamespacedServiceStatus` | GET | `--cli-region --namespace --name` | 查询状态 |

### Network（CCI 专属网络）

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listNetworkingCciIoV1beta1NamespacedNetwork` | GET | `--cli-region --namespace` | 列出 Network |
| `listNamespacedNetworks` | GET | `--cli-region --namespace` | 列出（旧 API） |
| `readNetworkingCciIoV1beta1NamespacedNetwork` | GET | `--cli-region --namespace --name` | 查询详情 |
| `readNetworkingCciIoV1beta1NamespacedNetworkStatus` | GET | `--cli-region --namespace --name` | 查询状态 |

### 其他资源

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `listCoreV1NamespacedConfigMap` / `listNamespacedConfigMaps` | GET | `--cli-region --namespace` | 列出 ConfigMap |
| `readCoreV1NamespacedConfigMap` | GET | `--cli-region --namespace --name` | 查询 ConfigMap |
| `listCoreV1NamespacedSecret` / `listNamespacedSecrets` | GET | `--cli-region --namespace` | 列出 Secret |
| `readCoreV1NamespacedSecret` | GET | `--cli-region --namespace --name` | 查询 Secret |
| `listCoreV1NamespacedPersistentVolumeClaim` | GET | `--cli-region --namespace` | 列出 PVC |
| `readCoreV1NamespacedPersistentVolumeClaim` | GET | `--cli-region --namespace --name` | 查询 PVC |
| `listCoreV1NamespacedEvent` | GET | `--cli-region --namespace` | 列出 Event |
| `readCoreV1NamespacedEvent` | GET | `--cli-region --namespace --name` | 查询 Event |
| `listCoreV1NamespacedResourceQuota` | GET | `--cli-region --namespace` | 列出 ResourceQuota |
| `listExtensionsV1beta1NamespacedIngress` | GET | `--cli-region --namespace` | 列出 Ingress |

### 元数据与特性

| Operation | 方法 | 必填参数 | 说明 |
|-----------|------|----------|------|
| `getAPIVersions` | GET | `--cli-region` | 获取 API 版本 |
| `readCciFeatureGates` | GET | `--cli-region` | 查询 CCI 特性开关 |
| `GetOpenAPIv2` | GET | `--cli-region` | 获取 OpenAPI schema |
| `listStorageV1StorageClass` | GET | `--cli-region` | 列出 StorageClass |
| `listRbacAuthorizationV1ClusterRole` | GET | `--cli-region` | 列出 ClusterRole |

## 验证命令

```bash
# 列出 CCI 全部可用操作
hcloud CCI --help

# 查看某操作的参数
hcloud CCI <Operation> --help
```

## 实测验证记录

| 命令 | 区域 | 结果 |
|------|------|------|
| `listNamespaces` | cn-north-4 | ✅ 返回 `NamespaceList`（items 空） |
| `listCoreV1PodForAllNamespaces` | cn-north-4 | ✅ 返回 `items: null`（无资源） |
| `listNamespaces` | cn-east-3 | ❌ 403 需 CCI 服务授权委托 |

> 实测时间：2026-09-15 | KooCLI 7.2.12 | AK/SK 已配置
