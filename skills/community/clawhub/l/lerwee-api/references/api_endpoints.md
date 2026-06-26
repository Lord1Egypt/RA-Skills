# Lerwee API Endpoints

乐维监控平台完整 API 端点列表。

## Base URL

```
http://192.168.1.79:8081/api/v6
```

## 接口列表

### 监控中心 (Monitor Center)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 监控对象列表 | POST | `/monitor/host-list` | 获取监控对象列表 |
| 创建监控对象 | POST | `/monitor/host-create` | 创建新的监控对象 |
| 更新监控对象 | POST | `/monitor/host-update` | 更新监控对象信息 |
| 删除监控对象 | POST | `/monitor/host-delete` | 删除监控对象（参数: hostids[]） |
| 监控对象指标 | POST | `/monitor/host-metric` | 获取监控对象指标列表 |
| 指标历史数据 | POST | `/monitor/metric-history` | 获取指标历史数据 |
| 监控对象宏 | POST | `/monitor/host-macro` | 获取监控对象宏变量 |
| 监控对象表单 | POST | `/monitor/host-form` | 获取创建/编辑表单数据 |
| 监控对象视图 | POST | `/monitor/host-view` | 获取监控对象视图数据 |
| 监控对象报表 | POST | `/monitor/host-report` | 获取监控对象报表 |
| 监控类型列表 | POST | `/monitor/classification` | 获取监控类型列表 |
| 配置文件 | POST | `/monitor/profile` | 获取配置文件 |

### 设备探测 (Device Detection)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| Agent 列表 | POST | `/detection/agent-list` | 获取 Agent 列表 |
| Agent 安装详情 | POST | `/detection/agent-install` | 获取 Agent 安装任务详情 |
| 批量安装 Agent | POST | `/detection/agent-batchinstall` | 批量发送 Agent 安装任务（异步） |
| 批量删除任务 | POST | `/detection/agent-batchdelete` | 批量删除 Agent 安装任务（参数: id 逗号分隔） |
| 卸载 Agent | POST | `/detection/agent-uninstall` | 发送 Agent 卸载任务（参数: id 逗号分隔） |
| 检查全部状态 | POST | `/detection/agent-checkall` | 发送检查全部 Agent 状态任务 |
| 检查指定状态 | POST | `/detection/agent-check` | 发送检查指定 Agent 状态任务（参数: id 逗号分隔） |
| 修改任务 | POST | `/detection/agent-update` | 修改 Agent 安装任务（参数: id, ssh_user, ssh_pass） |

### 告警管理 (Alert Management)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 告警列表 | POST | `/alert/problem-list` | 获取问题列表（详细参数: searchtype, page, pageSize, clock_begin, clock_end, ip, is_ip, keyword, isMaintenanced, isAcked, status, classification, subtype, groupid, priority, sortOrder, sortName） |
| 确认问题 | POST | `/alert/problem-ack` | 确认问题（参数: eventid, message） |
| 告警数量统计 | POST | `/alert/problem-report` | 获取告警数量统计 |

### 事件平台 (Event Platform / AI Alert)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| AI 事件列表 | POST | `/aialert/list` | 获取事件平台事件列表 |
| AI 告警详情 | POST | `/aialert/info` | 获取事件平台告警详情（参数: eventid） |
| 接收事件 | POST | `/aialert/receive` | 接收外部事件数据 |
| 更新处理状态 | POST | `/aialert/update-status` | 更新告警处理状态（参数: id, status） |
| 第三方告警恢复 | POST | `/aialert/recovery` | 第三方推送告警恢复（JSON 序列化 data） |
| AI 告警关闭 | POST | `/aialert/close` | 关闭事件平台告警（参数: id） |

### 业务视图 (Business View)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 组织树 | POST | `/business/organization-tree` | 获取组织树结构（无参数） |
| 业务树 | POST | `/business/business-tree` | 获取业务树结构（无参数） |
| 业务列表 | POST | `/business/business-list` | 获取业务列表 |
| 业务告警列表 | POST | `/business/business-alarms` | 获取业务告警列表 |
| 业务主机列表 | POST | `/business/business-hosts` | 获取业务主机列表 |
| 业务统计 | POST | `/business/business-statistic` | 获取业务统计数据 |
| 监控统计 | POST | `/business/monitor-statistic` | 获取监控统计数据 |
| 根据IP获取拓扑图 | POST | `/business/get-topographies-by-ip` | 根据IP获取关联的拓扑图（参数: ip） |

### 链路监控 (Link Monitoring)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 链路列表 | POST | `/links/list` | 获取链路监控列表（支持关键字、状态筛选） |

### 网络拓扑图 (Network Topology)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 拓扑图列表 | POST | `/topography/list` | 获取拓扑图列表 |
| 拓扑图树 | POST | `/topography/tree` | 获取拓扑图树结构 |
| 拓扑图消息 | POST | `/topography/message` | 获取拓扑图消息 |
| 拓扑图告警列表 | POST | `/topography/topography-alarms` | 获取某拓扑图的告警列表（支持级别筛选） |
| 拓扑图主机列表 | POST | `/topography/topography-hosts` | 获取某拓扑图的监控主机列表 |

### 用户管理 (User Management)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 用户列表 | POST | `/auth/user-list` | 获取用户列表 |
| 创建用户 | POST | `/auth/user-create` | 创建用户 |
| 更新用户 | POST | `/auth/user-update` | 更新用户信息 |
| 删除用户 | POST | `/auth/user-delete` | 删除用户 |
| 创建部门 | POST | `/auth/dept-create` | 创建部门（参数: name, parent_id） |
| 更新部门 | POST | `/auth/dept-update` | 更新部门（参数: id, name, parent_id） |
| 删除部门 | POST | `/auth/dept-delete` | 删除部门（参数: id[]） |
| 部门节点树 | POST | `/auth/dept-node` | 获取部门节点树（包含部门组） |
| 创建角色 | POST | `/auth/role-create` | 创建角色（参数: name, group_id） |
| 更新角色 | POST | `/auth/role-update` | 更新角色（参数: id, name, group_id） |
| 删除角色 | POST | `/auth/role-delete` | 删除角色（参数: id[]） |
| 角色节点树 | POST | `/auth/role-node` | 获取角色节点树（包含角色组） |


### 系统管理 (System Management)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 标签列表 | POST | `/profile/tag-list` | 获取标签列表（参数: pageSize, page, keyword） |
| 创建标签 | POST | `/profile/tag-create` | 创建标签（参数: name） |
| 更新标签 | POST | `/profile/tag-update` | 更新标签（参数: id, name） |
| 删除标签 | POST | `/profile/tag-delete` | 删除标签（参数: id 或 id[]） |


### 自动化运维 (Automation Operations)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 主机列表 | POST | `/devops/host-list` | 获取自动化主机列表（参数: pageSize, page, keyword, ansible_host, true_ip, os） |
| 网络设备列表 | POST | `/devops/network-list` | 获取网络设备列表（参数: pageSize, page, keyword, ansible_host, true_ip, firm, ansible_ssh_connection, model） |
| 执行脚本 | POST | `/devops/run-script` | 执行脚本（参数: hostid, script_id, timeout） |
| 获取文件目录 | POST | `/devops/file-dir` | 获取文件目录（参数: hostid, path） |
| 分发文件 | POST | `/devops/dispenses-file` | 分发文件到目标主机 |
| 上传文件 | POST | `/devops/upload-file` | 上传文件 |
| 执行历史 | POST | `/devops/execution-history` | 获取脚本执行历史 |
| 备份历史 | POST | `/devops/backup-history` | 获取备份历史 |

### 虚拟化管理 (Virtualization Management)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 存储列表 | POST | `/virtualization/storage-list` | 获取存储列表 |
| ESXi 层级结构 | POST | `/virtualization/esxi-hierarchy` | 获取 ESXi 层级结构 |
| 主机列表 | POST | `/virtualization/host-list` | 获取虚拟化主机列表 |

### 网络管理 (Network Management)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| IP 地址列表 | POST | `/network/ip-list` | 获取 IP 地址列表 |
| 子网掩码列表 | POST | `/network/ip-mask-list` | 获取子网掩码列表 |
| IP 地址段 | POST | `/network/ip-column` | 获取 IP 地址段 |
| 远程 IP 列表 | POST | `/network/ip-remote-list` | 获取远程 IP 列表 |

### 资产管理 (CMDB)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 同步库存 | POST | `/cmdb/sync-stock` | 同步资产库存 |
| 业务列表 | POST | `/cmdb/businesses` | 获取资产业务列表 |
| 资产对象列表 | POST | `/cmdb/objects` | 获取资产对象列表 |
| 实例列表 | POST | `/cmdb/instances` | 获取资产实例列表 |
| 创建实例 | POST | `/cmdb/create-instance` | 创建资产实例 |
| 更新实例 | POST | `/cmdb/update-instance` | 更新资产实例 |
| 删除实例 | POST | `/cmdb/delete-instance` | 删除资产实例（参数: ids[]） |
| 关系查询 | POST | `/cmdb/relation-query` | 查询资产实例关系 |
| 业务资产树 | POST | `/cmdb/business-tree` | 获取业务资产树 |

### 知识库 (Knowledge Base)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 知识列表 | POST | `/zikoo/knowledge-list` | 获取知识列表 |
| 知识详情 | POST | `/zikoo/knowledge-detail` | 获取知识详情（参数: id） |
| 知识分类 | POST | `/zikoo/knowledge-category` | 获取知识分类 |
| 知识附件下载 | GET | `/zikoo/knowldege/download` | 下载知识附件（参数: hash）【官方拼写 knowldege】 |
| 知识分享 | POST | `/zikoo/knowledge-share` | 生成知识分享链接 |

### 资源配置 (Resource Configuration)

| 接口 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 创建分组 | POST | `/magpie/group-create` | 创建资源分组（参数: name） |
| 更新分组 | POST | `/magpie/group-update` | 更新资源分组（参数: groupid, name） |
| 删除分组 | POST | `/magpie/group-delete` | 删除资源分组（参数: groupid） |

## 响应格式

所有接口返回统一的 JSON 格式：

```json
{
    "code": 0,
    "message": "",
    "data": {}
}
```

- `code`: 状态码，0 表示成功
- `message`: 消息说明
- `data`: 返回数据

## 错误码

常见错误码：

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 签名验证失败 |
| 1003 | 时间戳过期 |
| 2001 | 资源不存在 |
| 2002 | 权限不足 |
| 3001 | 操作失败 |

## 注意事项

1. 所有接口使用 POST 方法
2. 请求头必须设置 `Content-Type: application/json`
3. 所有请求必须包含 `timestamp` 和 `sign` 参数
4. 时间戳使用 Unix 时间戳（秒）
5. 签名计算时跳过 `sign` 字段本身、空值和数组类型参数
6. 数组参数使用数组格式传递（如 `hostids: [1, 2, 3]`）
