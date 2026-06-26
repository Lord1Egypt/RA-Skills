# 设备探测 API 详细说明

## Agent 管理

### 获取Agent列表
**接口：** `POST /detection/agent-list`

**参数：**
- `page` (int, 必填): 页码
- `pagesize` (int, 必填): 每页数量
- `ip` (string, 可选): IP地址
- `subtype` (int, 可选): 系统类型 (101001-Linux, 101003-AIX)
- `agent_install_status` (string, 可选): 安装状态 (DOING-进行中, SUCCESS-成功)
- `agent_status` (string, 可选): Agent状态 (UP-正常, DOWN-异常)

**返回字段说明：**
- `id`: 记录ID
- `ip`: IP地址
- `subtype`: 系统类型
- `ssh_user`: SSH用户
- `ssh_port`: SSH端口
- `agent_path`: Agent路径
- `agent_port`: Agent端口
- `agent_user`: Agent用户
- `server_ip`: 服务器IP
- `server_port`: 服务器端口
- `agent_name`: Agent名称
- `agent_version`: Agent版本
- `agent_install_status`: 安装状态
- `agent_install_status_msg`: 安装状态消息
- `agent_status`: Agent状态
- `agent_status_msg`: Agent状态消息
- `server_info`: 服务器信息
- `agent_install_type`: 安装类型
- `agent_install_time`: 安装时间（北京时间）
- `agent_status_time`: 状态时间（北京时间）

### Agent安装详情
**接口：** `POST /detection/agent-install`

**参数：**
- `id` (int, 必填): 任务ID

### 批量安装Agent
**接口：** `POST /detection/agent-batchinstall`

**说明：** Agent 批量发送安装任务，异步安装

**参数：**
- `ip_include` (string, 必填): JSON 字符串格式的 IP 数组或范围，如 `["192.168.1.1-192.168.1.10", "192.168.1.20"]`
- `ssh_port` (string, 必填): SSH 端口
- `ssh_user` (string, 必填): SSH 用户名
- `ssh_pass` (string, 必填): SSH 密码
- `subtype` (string, 必填): 系统类型 (linux-101001, aix-101003)
- `agent_path` (string, 可选): Agent 安装路径
- `agent_port` (string, 可选): Agent 安装端口
- `agent_user` (string, 可选): Agent 安装用户
- `server_ip` (string, 可选): 服务端 IP

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": "发送任务成功"
}
```

### 批量删除Agent安装任务
**接口：** `POST /detection/agent-batchdelete`

**参数：**
- `id` (string, 必填): 记录 ID，多个用英文逗号分隔

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": "成功"
}
```

### 发送Agent卸载任务
**接口：** `POST /detection/agent-uninstall`

**参数：**
- `id` (string, 必填): 记录 ID，多个用英文逗号分隔

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": "发送任务成功"
}
```

### 检查全部Agent状态
**接口：** `POST /detection/agent-checkall`

**参数：** 无

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": "发送任务成功"
}
```

### 检查指定Agent状态
**接口：** `POST /detection/agent-check`

**参数：**
- `id` (string, 必填): 记录 ID，多个用英文逗号分隔

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": "发送任务成功"
}
```

### 修改Agent安装任务
**接口：** `POST /detection/agent-update`

**参数：**
- `id` (int, 必填): 记录 ID
- `ssh_user` (string, 必填): SSH 用户名
- `ssh_pass` (string, 必填): SSH 密码

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": "成功"
}
```

### 删除Agent
**接口：** `POST /detection/agent-delete`

**参数：**
- `ids` (int[], 必填): 记录ID数组
