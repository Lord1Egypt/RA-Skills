# 蒲公英 MCP 工具参考

> **关于工具名前缀**：不同 AI 平台会自动给 MCP 工具添加不同的前缀。例如 WorkBuddy 中显示为 `mcp__pgy__get_sdwan_network`，Claude Desktop 中可能显示为 `pgy__get_sdwan_network`，Cursor/VS Code 中可能又是另一种格式。本文档使用去掉平台前缀的通用工具名，调用时请按所在平台的实际名称使用。

---

## 一、SD-WAN 网络管理

### 查询 — `get_sdwan_network`

| action | 用途 | 关键参数 |
|--------|------|---------|
| `list` (默认) | 获取所有 SD-WAN 网络 | 无 |
| `info` | 查询指定网络详情 | `network_id` |
| `members` | 查看网络成员列表 | `network_id` |
| `member_info` | 查询成员详细配置 | `network_id`, `member` |

### 管理 — `manage_sdwan_network`

| action | 用途 | 风险 | 关键参数 |
|--------|------|------|---------|
| `create` | 创建 SD-WAN 网络 | 无 | `name`, `type` |
| `update` | 更新网络名称/类型 | ⚠️ 需二次确认 | `network_id`, `name`/`type`, `operation` |
| `delete` | 删除网络 | ⚠️ 需二次确认 | `network_id`, `operation` |

**网络类型 `type` 取值：**
- `Peer-to-Peer`：对等网络，所有成员平等互访
- `Client-Server`：集散网络，需指定 hub/client 角色
- `Zero-Trust`：自定义网络，自定义访问权限
- `Client-Server-Public`：集散网络-公网版

### 成员管理 — `manage_sdwan_network_member`

| action | 用途 | 风险 | 关键参数 |
|--------|------|------|---------|
| `add` | 将成员加入网络 | 无 | `network_id`, `member` |
| `set_role` | 设置成员角色 | ⚠️ 需二次确认 | `network_id`, `member`, `role`, `operation` |
| `remove` | 将成员移出网络 | ⚠️ 需二次确认 | `network_id`, `member`, `operation` |

**角色 `role` 取值：** `hub`（中心节点）/ `client`（普通节点）/ `admin`（管理员）

**成员 `member` 格式：** VPNID（如 `92889499:001`）或设备 SN 码

---

## 二、软件成员管理

### 查询 — `get_vpnid`

| action | 用途 | 关键参数 |
|--------|------|---------|
| `list` (默认) | 获取软件成员列表 | 可选 `type`（client/server） |
| `count` | 统计成员数量 | 可选 `type` |
| `get` | 查询单个成员详情 | `member` |

### 在线状态 — `get_vpnid_status`

| 参数 | 说明 |
|------|------|
| `members` | 必填，成员 UID 列表，如 `["92889499:001", "92889499:002"]` |

返回每个成员的 `online`（是否在线）和 `status`（状态）。

### 管理 — `manage_vpnid`

| action | 用途 | 风险 | 关键参数 |
|--------|------|------|---------|
| `create` | 批量创建成员 | 无 | `type`, `number`, `memo`(可选), `password`(可选) |
| `set_memo` | 修改备注 | 无 | `member`, `memo` |
| `set_password` | 修改密码 | ⚠️ 高风险，需二次确认 | `member`, `password`, `operation` |
| `reset` | 重置成员（返回新密码） | ⚠️ 高风险，需二次确认 | `member`, `operation` |
| `delete` | 删除成员 | ⚠️ 高风险，需二次确认 | `member`, `operation` |

**成员类型 `type` 取值：** `client`（客户端）/ `server`（服务器端，需付费）

---

## 三、硬件设备管理

### 查询 — `get_device`

| action | 用途 | 关键参数 |
|--------|------|---------|
| `list` (默认) | 获取所有硬件设备 | 无 |
| `info` | 查询指定设备详情 | `sn` |

### 在线状态 — `get_device_status`

| 参数 | 说明 |
|------|------|
| `sns` | 必填，SN 码列表，如 `["726666578469"]` |

### 管理 — `manage_device`

| action | 用途 | 风险 | 关键参数 |
|--------|------|------|---------|
| `bind` | 绑定设备到账号 | 无 | `sn`, `mackey`(部分设备需要) |
| `unbind` | 解绑设备 | ⚠️ 需二次确认 | `sn`, `operation` |

**mackey**：MAC 地址后 6 位，部分设备绑定时必填。若绑定返回错误码 `400130`，说明需要提供 mackey。

---

## 四、路由器管理

### 信息查询 — `get_oraybox_information`

传入 `sn` 参数，查询路由器的系统信息、LAN/DNS/MTU 配置、时间/时区等。

### 管理 — `manage_oraybox`

| action | 用途 | 风险 | 关键参数 |
|--------|------|------|---------|
| `set_lan` | 设置 LAN 口 IP 和子网掩码 | ⚠️ 需二次确认，路由器会重启 | `sn`, `ip`, `mask`, `operation` |

---

## 二次确认机制

高风险操作使用两步确认流程：

1. **首次调用**：传入 `operation: ""`（空字符串），触发确认提示
2. **二次调用**：用户回复确认后，传入 `operation: "confirm"` 执行；传入 `operation: "cancel"` 取消

**AI 禁止自动确认**，必须等待用户明确回复。

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 查询返回空 | 检查 ID/SN 是否正确，确认资源存在 |
| 操作失败 | 检查权限、资源状态、参数合法性 |
| 连接超时 | 检查 MCP 连接状态，确认 API 密钥有效 |
| 绑定返回 400130 | 需补充 `mackey`（MAC 后 6 位）重新绑定 |
| 工具名未找到 | 检查平台前缀，如 WorkBuddy 用 `mcp__pgy__`，Claude Desktop 用 `pgy__` |
