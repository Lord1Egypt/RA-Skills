---
name: pgyvpn-skill
description: 贝锐蒲公英异地组网全流程技能。覆盖从注册账号、配置 MCP、下载安装客户端、创建网络、添加成员、登录客户端到验证连通的完整流程。当用户需要蒲公英异地组网、SD-WAN 组网、远程访问内网、虚拟局域网等相关操作时使用此技能。触发词：蒲公英、异地组网、SD-WAN、pgyvpn、pgy、组网、虚拟局域网、蒲公英路由器、蒲公英成员、蒲公英设备、远程办公、内网穿透。
---

# 蒲公英异地组网 — 全流程技能

通过蒲公英实现异地组网，让分布在不同地点的设备如同在同一个局域网内互相访问。本技能覆盖从零开始的完整流程，适用于任何支持 MCP（Model Context Protocol）的 AI 平台。

## 流程总览

```
注册贝锐账号 → 配置 MCP 连接 → 创建组网 → 添加成员 → 下载客户端 → 登录客户端 → 验证连通
     ①              ②             ③          ④           ⑤           ⑥           ⑦
```

---

## ① 注册贝锐账号

如已有账号可跳过此步。

1. 访问 [贝锐注册页面](https://passport.oray.com/register?brand=pgy)
2. 填写手机号/邮箱，设置密码，完成验证
3. 前往邮箱/手机查收激活信息，完成账号激活
4. 注册完成后，即可使用该账号登录蒲公英管理平台

> **提示**：贝锐账号通用于向日葵、蒲公英、花生壳等贝锐旗下产品。

---

## ② 配置蒲公英 MCP 连接

MCP 连接用于让 AI 直接管理你的蒲公英网络和设备。蒲公英提供云端 MCP Server，任何支持 MCP 协议的 AI 平台均可接入。

### 获取 MCP 密钥

1. 登录 [蒲公英管理平台](https://console.sdwan.oray.com/)
2. 点击左侧菜单 **【MCP】** → **【立即生成新密钥】**
3. 点击 **【复制含密钥的 MCP 配置 JSON】**

### 写入配置

将复制的 JSON 粘贴到对应 AI 平台的 MCP 配置文件中。配置格式示例：

```json
{
  "mcpServers": {
    "pgy": {
      "url": "https://mcp.pgyapi.com",
      "headers": {
        "X-API-Key": "sk-xxxxxxxxxxxx"
      }
    }
  }
}
```

> **注意**：实际 JSON 以管理平台生成的为准，直接复制粘贴即可，不要手动修改密钥。

### 各平台配置路径

| AI 平台 | 配置文件路径 | 配置方式 |
|---------|-------------|---------|
| **WorkBuddy** | `~/.workbuddy/mcp.json` | 将 JSON 粘贴到该文件，再到连接器管理页面信任该 MCP |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) 或 `%APPDATA%\Claude\claude_desktop_config.json` (Windows) | 将 `mcpServers` 部分合并到已有配置中，重启 Claude Desktop |
| **Cursor** | 项目根目录 `.cursor/mcp.json` 或全局 `~/.cursor/mcp.json` | 同上格式，将 `pgy` server 加入 `mcpServers` |
| **VS Code (Copilot)** | 项目 `.vscode/mcp.json` | 同上格式 |
| **Cline / Roo Code** | VS Code 扩展设置中的 MCP Servers 配置 | 同上格式 |
| **其他 MCP 客户端** | 参考对应平台的 MCP 配置文档 | 将蒲公英 MCP Server URL 和 API Key 按平台要求填入 |

> **通用原则**：无论哪个平台，核心都是将蒲公英的 MCP Server 地址 (`https://mcp.pgyapi.com`) 和 API Key (`X-API-Key` header) 配置到 MCP 客户端中。

### 验证连接

配置完成后，让 AI 尝试查询网络列表（调用 `get_sdwan_network`），确认 MCP 连接正常。

---

## ③ 创建 SD-WAN 组网

可通过 MCP 工具或管理平台创建网络。

### 网络类型选择

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| **Peer-to-Peer（对等网络）** | 所有成员平等互访 | 小型团队、家庭组网 |
| **Client-Server（集散网络）** | 中心节点(hub)与普通节点(client)，普通节点间不可互访 | 总部-分支架构 |
| **Zero-Trust（自定义网络）** | 自定义成员间访问权限 | 需要精细权限控制 |
| **Client-Server-Public（集散网络-公网版）** | 集散网络+公网访问 | 需公网端访问内网 |

> 体验版用户仅支持对等网络和集散网络。

### 通过 MCP 创建

调用 MCP 工具 `manage_sdwan_network`，`action: "create"`，提供：
- `name`：网络名称
- `type`：网络类型（从 Peer-to-Peer / Client-Server / Zero-Trust / Client-Server-Public 中选择）

> **注意**：MCP 工具名称在不同 AI 平台中可能有不同前缀（如 WorkBuddy 中为 `mcp__pgy__manage_sdwan_network`，Claude Desktop 中可能为 `pgy__manage_sdwan_network`），但工具功能和参数相同。下文统一使用去掉平台前缀的工具简称，详见 [tools_reference.md](references/tools_reference.md)。

### 通过管理平台创建

1. 登录 [蒲公英管理平台](https://console.sdwan.oray.com/)
2. **异地组网** → **网络成员** → **+创建网络**
3. 填写网络名称，选择网络类型，确认创建

---

## ④ 添加组网成员

组网成员分两类：软件成员（客户端）和硬件成员（路由器）。

### 软件成员

通过 MCP 工具 `manage_vpnid` 创建：

- `action: "create"`
- `type`：成员类型
  - `client`：客户端成员（适用于 Windows/macOS/Linux/iOS/Android）
  - `server`：服务器端成员（适用于 Windows/Linux，需付费）
- `number`：批量创建数量
- `memo`：备注（可选）
- `password`：登录密码

> 创建成功后会返回 **UID**（格式如 `92889499:001`）和虚拟 IP，**务必记录**，客户端登录时需要。

创建后，使用 `manage_sdwan_network_member` 将成员添加到网络：
- `action: "add"`
- `network_id`：目标网络 ID
- `member`：成员 UID

### 硬件成员

如拥有蒲公英路由器（X1/X3/X4/X5 等）：

1. 路由器通电并连接网络
2. 通过 MCP `manage_device` 绑定设备（`action: "bind"`, `sn`: 设备 SN 码）
3. 部分设备需提供 MAC 地址后 6 位 (`mackey`)
4. 绑定后路由器自动出现在硬件成员列表

**SN 码位置**：路由器底部标签上的序列号

---

## ⑤ 下载安装客户端

各平台客户端下载地址：**https://pgy.oray.com/download/**

| 平台 | 类型 | 下载方式 |
|------|------|---------|
| **Windows** | 客户端 / 服务器端 | 官网下载安装包 |
| **macOS** | 客户端 | 官网下载 .dmg / App Store |
| **Linux** | 客户端 / 服务器端 | 官网下载 .deb / .rpm |
| **iOS** | 客户端 | App Store 搜索「蒲公英」 |
| **Android** | 客户端 | 应用商店搜索「蒲公英」 |

### 安装步骤（以 Windows 为例）

1. 下载客户端安装包
2. 双击运行安装程序，按提示完成安装
3. 安装完成后启动客户端

### Linux 命令行安装

```bash
# Debian/Ubuntu
sudo dpkg -i pgyvisitor_xxx_amd64.deb
sudo apt-get install -f

# CentOS/RHEL
sudo rpm -ivh pgyvisitor_xxx_x86_64.rpm
```

---

## ⑥ 登录客户端

### 客户端登录方式

蒲公英客户端支持多种登录方式：

| 登录方式 | 说明 |
|---------|------|
| **贝锐账号登录** | 使用注册的贝锐账号密码登录 |
| **UID 登录** | 使用创建软件成员时生成的 UID + 密码 |
| **手机号登录** | 绑定手机号后使用手机号 + 验证码 |
| **微信登录** | 扫码登录 |
| **免密登录** | 已登录贝锐账号时自动识别 |

> **推荐**：个人用户使用贝锐账号登录；为他人分配的成员使用 UID + 密码登录。

### 登录后

1. 客户端登录成功后，会显示分配的 **虚拟 IP**（如 `172.16.x.x`）
2. 点击「网络」图标，可以看到同网络下的其他成员
3. 登录成功即自动加入组网，无需额外操作

---

## ⑦ 验证连通性

### Ping 测试

1. 在客户端点击 **「网络」** 图标
2. 选中要测试的目标成员
3. 点击 **「PING」** 按钮
4. 若收到回复，说明组网通道已建立

### 命令行测试

```bash
# ping 对端虚拟 IP
ping 172.16.x.x

# 访问对端服务（如 Web）
curl http://172.16.x.x:8080

# 访问共享文件夹（Windows）
# 资源管理器地址栏输入：\\172.16.x.x
```

### 通过 MCP 验证

调用 `get_vpnid_status` 查询成员在线状态：
- 传入成员 UID 列表
- 查看返回的 `online` 和 `status` 字段

---

## 安全操作原则

### 二次确认规则（MCP 操作）

以下操作涉及不可逆变更，MCP 工具内置了二次确认机制。**AI 必须等待用户明确确认**后才可执行：

| 风险等级 | 操作 | MCP 行为 |
|---------|------|---------|
| ⚠️ 高风险 | 修改/重置成员密码、删除成员 | 首次调用触发确认提示，二次调用需带 `operation: "confirm"` |
| ⚠️ 需确认 | 删除网络、更新网络、移出成员、设置角色 | 同上 |
| ⚠️ 需确认 | 解绑设备、设置路由器 LAN 口 | 同上 |

**AI 禁止自动确认高风险操作**，必须等待用户回复。

### 操作后验证

执行变更操作后，建议立即用查询接口验证结果是否正确。

---

## MCP 工具速查

蒲公英 MCP 提供以下工具，详见 [tools_reference.md](references/tools_reference.md)：

| 工具名 | 功能 | action 值 |
|--------|------|-----------|
| `get_sdwan_network` | 网络查询 | list / info / members / member_info |
| `manage_sdwan_network` | 网络管理 | create / update / delete |
| `manage_sdwan_network_member` | 成员管理 | add / set_role / remove |
| `get_vpnid` | 软件成员查询 | list / count / get |
| `manage_vpnid` | 软件成员管理 | create / set_memo / set_password / reset / delete |
| `get_vpnid_status` | 成员在线状态 | 传 members 数组 |
| `get_device` | 硬件设备查询 | list / info |
| `manage_device` | 设备管理 | bind / unbind |
| `get_device_status` | 设备在线状态 | 传 sns 数组 |
| `get_oraybox_information` | 路由器信息查询 | 传 SN |
| `manage_oraybox` | 路由器管理 | set_lan |

> **关于工具名前缀**：不同 AI 平台会自动给 MCP 工具添加前缀。例如 WorkBuddy 中显示为 `mcp__pgy__get_sdwan_network`，Claude Desktop 中可能显示为 `pgy__get_sdwan_network`，其他平台可能不同。上表使用去掉前缀的通用名称，调用时请按所在平台的实际名称使用。

---

## 常见工作流

### 场景一：纯软件组网（最常见）

```
1. 注册贝锐账号 → 配置 MCP
2. 创建 SD-WAN 网络（对等网络即可）
3. 批量创建软件成员（client 类型）
4. 将成员添加到网络
5. 在各设备上下载安装客户端
6. 使用 UID + 密码登录客户端
7. Ping 测试验证连通
```

### 场景二：硬件 + 软件混合组网

```
1. 注册贝锐账号 → 配置 MCP
2. 路由器通电联网 → 绑定设备到账号
3. 创建 SD-WAN 网络
4. 添加路由器到网络（硬件成员）
5. 创建软件成员并添加到网络
6. 软件端下载客户端并登录
7. 通过虚拟 IP 访问路由器下联设备
```

### 场景三：排查连接问题

```
1. MCP 查询网络成员列表，找到问题成员
2. 查询成员在线状态 (get_vpnid_status)
3. 如离线：检查客户端是否已登录、密码是否正确
4. 如涉及硬件：查询设备在线状态 (get_device_status)
5. 如涉及路由器：检查 LAN/DNS 配置
6. 连接但无法访问：检查网络类型和成员角色配置
```

### 场景四：扩容组网

```
1. 查询当前成员数量 (get_vpnid, action: count)
2. 批量创建新软件成员
3. 将新成员添加到目标网络
4. 将 UID 和密码分发给新成员
5. 查询成员列表确认添加成功
```

---

## 常见问题

### Q: 体验版有什么限制？
- 网络类型仅支持对等网络和集散网络
- 不支持服务器端成员
- 成员数量和网络带宽有上限
- 如需更多功能需升级付费版

### Q: 客户端登录后看不到其他成员？
- 检查是否加入了正确的网络
- 检查网络类型：集散网络中普通节点间不可互访
- 尝试重新登录客户端

### Q: Ping 不通但显示在线？
- 检查本地防火墙是否阻止了 ICMP
- 检查对端防火墙设置
- 尝试使用 TCP 端口访问而非 Ping

### Q: 路由器绑定需要 mackey 怎么办？
- mackey 是设备 MAC 地址后 6 位
- 在路由器底部标签或管理界面中查看

### Q: 如何在 Claude Desktop 中使用？
- 按第②步将配置写入 `claude_desktop_config.json`
- 重启 Claude Desktop 即可在对话中使用蒲公英 MCP 工具

### Q: 如何在 Cursor 中使用？
- 按第②步将配置写入 `.cursor/mcp.json` 或全局配置
- 重新打开 Cursor 即可

---

## 重要链接

| 用途 | 地址 |
|------|------|
| 注册账号 | https://passport.oray.com/register?brand=pgy |
| 管理平台 | https://console.sdwan.oray.com/ |
| 客户端下载 | https://pgy.oray.com/download/ |
| 帮助文档 | https://service.oray.com/ |
| MCP 配置 | 管理平台 → MCP → 生成新密钥 |
| MCP 协议规范 | https://modelcontextprotocol.io/ |

---

## 注意事项

- 集散网络中需明确指定中心节点 (hub) 和普通节点 (client)
- 路由器设置 LAN 口会导致网络重启，期间会短暂断网
- 部分设备绑定时需提供 MAC 地址后 6 位 (mackey)
- 服务器端成员需付费，体验版不支持
- 删除操作不可逆，执行前务必确认
- 操作完成后可在 [管理平台](https://console.sdwan.oray.com/) 复核结果
- 本技能基于蒲公英 MCP 协议，兼容所有支持 MCP 的 AI 平台
