---
name: huawei-cloud-cce-cluster-management
description: |
  华为云 CCE 集群生命周期管理技能，支持集群创建、删除、休眠/唤醒、节点池扩缩容、节点生命周期管理（cordon/uncordon/drain/delete）等操作。
  触发场景：(1) 创建或删除 CCE 集群；(2) 集群休眠/唤醒操作；(3) 节点池扩缩容；(4) 节点调度管理（标记不可调度、驱逐Pod、删除节点）；(5) 绑定/解绑集群 EIP；(6) 查询集群和节点信息；(7) 管理集群插件。
  关键词：CCE 集群管理、创建集群、删除集群、节点池、节点管理、集群休眠、集群唤醒、cordon、uncordon、drain、kubeconfig
tags: [cce, kubernetes, 集群管理, 节点池, 插件]
version: 1.0.0
---

# 华为云 CCE 集群管理

## 概述

华为云 CCE (Cloud Container Engine) 集群生命周期管理，包括集群创建/删除、休眠/唤醒、节点池管理、节点调度控制等操作。

## ⛔ 安全约束

### 危险操作二次确认机制

> **本技能严格执行变动类操作二次确认机制，防止误操作导致业务中断或数据丢失。**

所有危险操作必须携带 `confirm=true` 参数才会真正执行，否则仅返回操作预览和确认提示。

#### 需二次确认的操作列表

| 工具 | 操作类型 | 风险等级 | 说明 |
|------|---------|---------|------|
| `huawei_delete_cce_cluster` | 删除 | 🔴 极高 | 删除整个 CCE 集群，不可恢复 |
| `huawei_hibernate_cce_cluster` | 休眠 | 🟠 高 | 休眠集群，停止所有工作负载，暂停控制面计费 |
| `huawei_awake_cce_cluster` | 唤醒 | 🟠 高 | 唤醒休眠集群，恢复工作负载和控制面计费 |
| `huawei_resize_cce_nodepool` | 扩缩容 | 🟡 中 | 调整节点池节点数量，影响业务容量 |
| `huawei_delete_cce_nodepool` | 删除 | 🟠 高 | 删除节点池，影响业务容量 |
| `huawei_delete_cce_node` | 删除 | 🟠 高 | 从集群删除节点，影响业务调度 |
| `huawei_uninstall_cce_addon` | 卸载 | 🟠 高 | 卸载集群插件，可能影响集群功能 |
| `huawei_cce_node_cordon` | 标记不可调度 | 🟡 中 | 节点标记为不可调度，新 Pod 不会分配 |
| `huawei_cce_node_uncordon` | 恢复调度 | 🟡 中 | 节点恢复可调度，新 Pod 可能立即分配 |
| `huawei_cce_node_drain` | 驱逐 | 🟠 高 | 驱逐节点所有 Pod，影响业务运行 |

#### 工作流程

**第一步：预览操作** - 不带 `confirm` 参数调用

```bash
# 示例：预览删除集群
python3 huawei-cloud.py huawei_delete_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx
```

返回：操作预览、风险警告、确认示例

**第二步：确认执行** - 携带 `confirm=true` 参数再次调用

```bash
# 示例：确认并执行删除
python3 huawei-cloud.py huawei_delete_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx \
  confirm=true
```

#### 安全特性

- ❌ **未带 confirm 参数时**：操作不执行，仅返回预览和警告
- ✅ **携带 confirm=true 时**：操作才真正执行
- 📝 **返回清晰的提示**：包含警告信息、操作影响和确认示例
- ⏱️ **代码级验证**：函数内部强制校验 confirm 参数

### 认证信息安全

✅ **本技能严格遵守以下安全规则：**

1. **禁止持久化存储认证信息** - 从不将 AK/SK、Token、证书等敏感认证信息保存到磁盘文件
2. **禁止长期内存缓存** - AK/SK 仅在当前 API 请求调用过程中存在于内存，调用结束后自动释放
3. **仅项目 ID 内存缓存** - 仅将非敏感的项目 ID 缓存在进程内存中（不写入磁盘）
4. **禁止日志泄露** - 不在任何日志、响应输出或错误信息中包含 AK/SK 等敏感信息
5. **临时文件安全清理** - 如果因 API 需求创建临时证书文件，使用后立即删除

AK/SK 仅支持以下两种方式使用：

- 通过环境变量 `HW_ACCESS_KEY` / `HW_SECRET_KEY` / `HW_REGION_NAME` 传入（进程级，不保存）
- 通过每次调用参数传入（仅本次调用有效）

---

## 前置条件

### 环境变量配置

#### 方式一：环境变量（推荐）

```bash
export HW_ACCESS_KEY="your-access-key-id"
export HW_SECRET_KEY="your-secret-access-key"
export HW_REGION_NAME="cn-north-4"
```

**方式二：每次调用参数传入**
在每次 API 调用时传入 `ak` 和 `sk` 参数（不推荐用于生产环境）。

### 节点登录密码

创建节点/节点池时，如未提供 `ssh_key`，密码通过 `CCE_NODE_PASSWORD` 环境变量传入（不从 CLI 参数传入）。脚本自动验证密码复杂度（8-26 位，至少含大写、小写、数字、特殊字符中的三种），并自动进行 SHA-512 加盐加密 + base64 编码。

```bash
export CCE_NODE_PASSWORD="你的密码"
```

### Python 依赖

```bash
pip install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkiam
```

### IAM 权限策略

确保 IAM 用户具有以下最小权限：

| 权限 | 说明 |
|------|------|
| `cce:cluster:list` | 查询集群列表 |
| `cce:cluster:get` | 查询集群详情 |
| `cce:cluster:create` | 创建集群 |
| `cce:cluster:delete` | 删除集群 |
| `cce:cluster:update` | 更新集群（休眠/唤醒/EIP 绑定） |
| `cce:node:list` | 查询节点列表 |
| `cce:node:get` | 查询节点详情 |
| `cce:node:delete` | 删除节点 |
| `cce:node:update` | 更新节点（cordon/uncordon/drain） |
| `cce:nodepool:list` | 查询节点池列表 |
| `cce:nodepool:update` | 更新节点池（扩缩容） |
| `cce:addon:list` | 查询插件列表 |
| `cce:addon:get` | 查询插件详情 |

---

## 核心命令

### 集群查询

| 工具 | 功能 | 参数 |
|------|------|------|
| `huawei_list_cce_clusters` | 查询区域内所有 CCE 集群列表 | `region` |
| `huawei_get_cce_nodes` | 获取指定节点详细信息 | `region`, `cluster_id`, `node_id` |
| `huawei_get_cce_kubeconfig` | 获取集群 kubeconfig 配置 | `region`, `cluster_id` |

**参数说明：**

- `region` (required): 华为云区域 (e.g., cn-north-4, cn-east-3)
- `cluster_id` (required): CCE 集群 ID
- `node_id` (required): 节点 ID

---

### 集群管理

| 工具 | 功能 | 风险等级 | 需确认 |
|------|------|---------|-------|
| `huawei_create_cce_cluster` | 创建 CCE 集群 | 🟢 低 | 否 |
| `huawei_delete_cce_cluster` | 删除 CCE 集群 | 🔴 极高 | **是** |
| `huawei_hibernate_cce_cluster` | 休眠集群 | 🟠 高 | **是** |
| `huawei_awake_cce_cluster` | 唤醒集群 | 🟠 高 | **是** |
| `huawei_bind_cce_cluster_eip` | 绑定集群 EIP | 🟢 低 | 否 |
| `huawei_unbind_cce_cluster_eip` | 解绑集群 EIP | 🟡 中 | 否 |

**参数说明：**

- `region` (required): 华为云区域
- `cluster_id` (required): CCE 集群 ID
- `confirm` (optional): 设为 `true` 确认执行危险操作

**使用示例：**

```bash
# 查询集群列表
python3 huawei-cloud.py huawei_list_cce_clusters region=cn-north-4

# 创建集群（基础示例）
python3 huawei-cloud.py huawei_create_cce_cluster \
  region=cn-north-4 \
  name=my-cluster \
  version=v1.28 \
  flavor=cce.s1.small \
  vpc_id=xxx \
  subnet_id=xxx

# 删除集群（需二次确认）
python3 huawei-cloud.py huawei_delete_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx
# 返回预览和警告，不执行

# 确认删除集群
python3 huawei-cloud.py huawei_delete_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx \
  confirm=true

# 休眠集群（需二次确认）
python3 huawei-cloud.py huawei_hibernate_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx

# 确认休眠集群
python3 huawei-cloud.py huawei_hibernate_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx \
  confirm=true

# 唤醒集群（需二次确认）
python3 huawei-cloud.py huawei_awake_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx

# 确认唤醒集群
python3 huawei-cloud.py huawei_awake_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx \
  confirm=true

# 获取 kubeconfig
python3 huawei-cloud.py huawei_get_cce_kubeconfig \
  region=cn-north-4 \
  cluster_id=xxx
```

---

### 节点池管理

| 工具 | 功能 | 风险等级 | 需确认 |
|------|------|---------|-------|
| `huawei_list_cce_nodepools` | 查询节点池列表 | 🟢 低 | 否 |
| `huawei_create_cce_nodepool` | 创建节点池 | 🟢 低 | 否 |
| `huawei_resize_cce_nodepool` | 调整节点池节点数量 | 🟡 中 | **是** |
| `huawei_delete_cce_nodepool` | 删除节点池 | 🟠 高 | **是** |

**参数说明：**

- `region` (required): 华为云区域
- `cluster_id` (required): CCE 集群 ID
- `nodepool_id` (required): 节点池 ID
- `node_count` (required): 目标节点数量
- `confirm` (optional): 设为 `true` 确认执行

**使用示例：**

```bash
# 查询节点池列表
python3 huawei-cloud.py huawei_list_cce_nodepools \
  region=cn-north-4 \
  cluster_id=xxx

# 扩容节点池（预览）
python3 huawei-cloud.py huawei_resize_cce_nodepool \
  region=cn-north-4 \
  cluster_id=xxx \
  nodepool_id=xxx \
  node_count=5

# 确认扩容节点池
python3 huawei-cloud.py huawei_resize_cce_nodepool \
  region=cn-north-4 \
  cluster_id=xxx \
  nodepool_id=xxx \
  node_count=5 \
  confirm=true
```

---

### 节点管理

| 工具 | 功能 | 风险等级 | 需确认 |
|------|------|---------|-------|
| `huawei_list_cce_nodes` | 查询集群内所有节点 | 🟢 低 | 否 |
| `huawei_delete_cce_node` | 删除节点 | 🟠 高 | **是** |
| `huawei_cce_node_cordon` | 标记节点不可调度 | 🟡 中 | **是** |
| `huawei_cce_node_uncordon` | 恢复节点可调度 | 🟡 中 | **是** |
| `huawei_cce_node_drain` | 驱逐节点所有 Pod | 🟠 高 | **是** |
| `huawei_cce_node_status` | 查询节点调度状态 | 🟢 低 | 否 |
| `huawei_create_cce_node` | 创建节点 | 🟢 低 | 否 |

**参数说明：**

- `region` (required): 华为云区域
- `cluster_id` (required): CCE 集群 ID
- `node_id` (required): 节点 ID（删除、cordon、uncordon、drain、status）
- `confirm` (optional): 设为 `true` 确认执行危险操作

**节点调度状态说明：**

- **Schedulable（可调度）**: 新 Pod 可以调度到该节点
- **Unschedulable（不可调度）**: 新 Pod 不会调度到该节点，现有 Pod 不受影响

**使用示例：**

```bash
# 查询节点列表
python3 huawei-cloud.py huawei_list_cce_nodes \
  region=cn-north-4 \
  cluster_id=xxx

# 查询节点调度状态
python3 huawei-cloud.py huawei_cce_node_status \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx

# 标记节点不可调度（预览）
python3 huawei-cloud.py huawei_cce_node_cordon \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx

# 确认标记节点不可调度
python3 huawei-cloud.py huawei_cce_node_cordon \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx \
  confirm=true

# 恢复节点可调度（预览）
python3 huawei-cloud.py huawei_cce_node_uncordon \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx

# 确认恢复节点可调度
python3 huawei-cloud.py huawei_cce_node_uncordon \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx \
  confirm=true

# 驱逐节点所有 Pod（预览）
python3 huawei-cloud.py huawei_cce_node_drain \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx

# 确认驱逐节点所有 Pod
python3 huawei-cloud.py huawei_cce_node_drain \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx \
  confirm=true

# 删除节点（预览）
python3 huawei-cloud.py huawei_delete_cce_node \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx

# 确认删除节点
python3 huawei-cloud.py huawei_delete_cce_node \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx \
  confirm=true
```

---

### 插件管理

| 工具 | 功能 | 风险等级 | 需确认 |
|------|------|---------|-------|
| `huawei_list_cce_addons` | 查询集群插件列表 | 🟢 低 | 否 |
| `huawei_get_cce_addon_detail` | 查询插件详情 | 🟢 低 | 否 |
| `huawei_install_cce_addon` | 安装插件 | 🟢 低 | 否 |
| `huawei_uninstall_cce_addon` | 卸载插件 | 🟠 高 | **是** |
| `huawei_update_cce_addon` | 更新插件 | 🟡 中 | 否 |

**参数说明：**

- `region` (required): 华为云区域
- `cluster_id` (required): CCE 集群 ID
- `addon_id` (required): 插件 ID 或名称

**使用示例：**

```bash
# 查询插件列表
python3 huawei-cloud.py huawei_list_cce_addons \
  region=cn-north-4 \
  cluster_id=xxx

# 查询插件详情
python3 huawei-cloud.py huawei_get_cce_addon_detail \
  region=cn-north-4 \
  cluster_id=xxx \
  addon_id=coredns
```

---

## 支持区域

| 区域代码 | 区域名称 |
|----------|----------|
| cn-north-4 | 华北-北京四 |
| cn-north-1 | 华北-北京一 |
| cn-north-2 | 华北-北京二 |
| cn-east-3 | 华东-上海一 |
| cn-south-1 | 华南-广州 |
| cn-south-2 | 华南-广州友好 |
| cn-east-4 | 华东-华东二 |
| cn-southwest-2 | 贵阳一 |
| ap-southeast-1 | 亚太-香港 |
| ap-southeast-2 | 亚太-曼谷 |
| ap-southeast-3 | 亚太-新加坡 |

---

## 常见场景

### 场景一：集群维护模式（排空节点）

当需要对节点进行维护时，使用 cordon + drain 组合：

```bash
# 步骤 1: 标记节点不可调度
python3 huawei-cloud.py huawei_cce_node_cordon \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx \
  confirm=true

# 步骤 2: 驱逐节点上的所有 Pod
python3 huawei-cloud.py huawei_cce_node_drain \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx \
  confirm=true

# 维护完成后，恢复节点可调度
python3 huawei-cloud.py huawei_cce_node_uncordon \
  region=cn-north-4 \
  cluster_id=xxx \
  node_id=xxx \
  confirm=true
```

### 场景二：集群休眠唤醒（成本优化）

对于非生产环境或开发环境，可以在非工作时间休眠集群以节省成本：

```bash
# 休眠集群
python3 huawei-cloud.py huawei_hibernate_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx \
  confirm=true

# 唤醒集群
python3 huawei-cloud.py huawei_awake_cce_cluster \
  region=cn-north-4 \
  cluster_id=xxx \
  confirm=true
```

**注意：** 休眠集群会停止所有工作负载，暂停控制面计费，但节点计费仍在继续。

### 场景三：节点池扩缩容

根据业务负载动态调整节点数量：

```bash
# 扩容节点池
python3 huawei-cloud.py huawei_resize_cce_nodepool \
  region=cn-north-4 \
  cluster_id=xxx \
  nodepool_id=xxx \
  node_count=10 \
  confirm=true

# 缩容节点池
python3 huawei-cloud.py huawei_resize_cce_nodepool \
  region=cn-north-4 \
  cluster_id=xxx \
  nodepool_id=xxx \
  node_count=3 \
  confirm=true
```

---

## Notes

- 确保 AK/SK 具有正确的 IAM 权限
- 不同区域可能有不同的资源可用性
- 所有危险操作都需要二次确认
- 删除操作不可恢复，请谨慎操作
- 休眠集群会停止所有工作负载，请在非业务时间操作
- 节点 drain 操作会驱逐所有 Pod，请确保应用有足够的副本数

---

## 输出格式

所有工具返回 JSON 格式结果，包含：

- `status`: 操作结果 (`success` / `error`)
- `data`: 操作响应数据（集群信息、节点列表、插件详情等）
- `message`: 人类可读的结果描述
- `warning`: 危险操作的风险警告（预览模式）

## 验证方法

详见 [verification-method.md](references/verification-method.md)。快速验证清单：

1. 确认 AK/SK 凭证已通过环境变量配置
2. 运行 `huawei_list_cce_clusters` 确认 API 连通性
3. 测试危险操作预览（不带 `confirm=true`）
4. 验证 Turbo 集群 ENI 网络配置

## 最佳实践

- 使用环境变量（`HW_ACCESS_KEY` / `HW_SECRET_KEY`）配置凭证，避免硬编码
- 危险操作先预览，再使用 `confirm=true` 确认执行
- 高性能业务场景推荐 Turbo 雑群（`container_network_type=eni`）
- 低流量时段执行节点池扩缩容，减少业务影响
- 生产节点池保持 ≥2 个节点，确保冗余
- 定期通过 `huawei_list_cce_clusters` 和 `huawei_show_cce_cluster` 检查集群健康状态

---

## 参考文档

- [集群生命周期操作](references/task-cluster-management.md)
- [节点池操作](references/task-nodepool-management.md)
- [节点调度操作](references/task-node-management.md)
- [IAM 权限策略](references/iam-policies.md)
- [验证步骤](references/verification-method.md)
- [故障排查](references/troubleshooting.md)
- [CCE Python SDK API 参考](references/cce-api-guide.md)
- [集群/节点池创建参数](references/cce-cluster-parameters.md)