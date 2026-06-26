# 用户与权限管理 API 详细说明

## 用户管理

### 获取用户列表
**接口：** `POST /user/list`

**参数：**
- `page` (int, 必填): 页码
- `pageSize` (int, 必填): 每页数量
- `keyword` (string, 可选): 关键词搜索
- `status` (int, 可选): 用户状态

### 创建用户
**接口：** `POST /user/create`

**参数：**
- `username` (string, 必填): 用户名
- `realname` (string, 必填): 真实姓名
- `password` (string, 必填): 密码
- `email` (string, 可选): 邮箱
- `phone` (string, 可选): 手机号
- `role_id` (int, 可选): 角色ID
- `group_ids` (int[], 可选): 分组ID数组
- `status` (int, 可选): 状态 (1-启用, 0-禁用)

### 更新用户
**接口：** `POST /user/update`

**参数：**
- `userid` (int, 必填): 用户ID
- `username` (string, 可选): 用户名
- `realname` (string, 可选): 真实姓名
- `password` (string, 可选): 密码
- `email` (string, 可选): 邮箱
- `phone` (string, 可选): 手机号
- `role_id` (int, 可选): 角色ID
- `group_ids` (int[], 可选): 分组ID数组
- `status` (int, 可选): 状态

### 删除用户
**接口：** `POST /user/delete`

**参数：**
- `userids` (int[], 必填): 用户ID数组

## 部门管理

### 获取部门列表
**接口：** `POST /department/list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词搜索

### 创建部门
**接口：** `POST /department/create`

**参数：**
- `name` (string, 必填): 部门名称
- `parent_id` (int, 可选): 上级部门ID
- `description` (string, 可选): 描述

### 更新部门
**接口：** `POST /department/update`

**参数：**
- `departmentid` (int, 必填): 部门ID
- `name` (string, 可选): 部门名称
- `parent_id` (int, 可选): 上级部门ID
- `description` (string, 可选): 描述

### 删除部门
**接口：** `POST /department/delete`

**参数：**
- `departmentids` (int[], 必填): 部门ID数组

## 角色管理

### 获取角色列表
**接口：** `POST /role/list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词搜索

### 创建角色
**接口：** `POST /role/create`

**参数：**
- `name` (string, 必填): 角色名称
- `description` (string, 可选): 描述

### 更新角色
**接口：** `POST /role/update`

**参数：**
- `roleid` (int, 必填): 角色ID
- `name` (string, 可选): 角色名称
- `description` (string, 可选): 描述

### 删除角色
**接口：** `POST /role/delete`

**参数：**
- `roleids` (int[], 必填): 角色ID数组

## 自动化运维

### 执行脚本
**接口：** `POST /automation/script-exec`

**参数：**
- `host_ids` (array, 必填): 主机ID数组
- `script` (string, 必填): 脚本内容
- `timeout` (int, 可选): 超时时间（秒）

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "task_id": "task_123456",
        "status": "running"
    }
}
```

### 获取执行结果
**接口：** `POST /automation/script-result`

**参数：**
- `task_id` (string, 必填): 任务ID

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "task_id": "task_123456",
        "status": "success",
        "results": [
            {
                "host_id": 10521,
                "host": "test-host",
                "exit_code": 0,
                "output": "script output here"
            }
        ]
    }
}
```

## 虚拟化管理

### 获取虚拟中心列表
**接口：** `POST /virtualization/vcenter-list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词搜索

### 添加虚拟中心
**接口：** `POST /virtualization/vcenter-add`

**参数：**
- `name` (string, 必填): 虚拟中心名称
- `type` (string, 必填): 类型 (VMware)
- `host` (string, 必填): 主机地址
- `port` (int, 可选): 端口（默认 443）
- `username` (string, 必填): 用户名
- `password` (string, 必填): 密码

### 更新虚拟中心
**接口：** `POST /virtualization/vcenter-update`

**参数：**
- `id` (int, 必填): 虚拟中心ID
- `name` (string, 可选): 虚拟中心名称
- `type` (string, 可选): 类型
- `host` (string, 可选): 主机地址
- `port` (int, 可选): 端口
- `username` (string, 可选): 用户名
- `password` (string, 可选): 密码

### 删除虚拟中心
**接口：** `POST /virtualization/vcenter-delete`

**参数：**
- `ids` (array, 必填): 虚拟中心ID数组

### 获取虚拟机列表
**接口：** `POST /virtualization/vm-list`

**参数：**
- `vcenter_id` (int, 必填): 虚拟中心ID
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词搜索

## 网络管理

### 获取 IP 地址段列表
**接口：** `POST /network/subnet-list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词搜索

### 添加 IP 地址段
**接口：** `POST /network/subnet-add`

**参数：**
- `name` (string, 必填): 名称
- `subnet` (string, 必填): 子网（如：192.168.1.0/24）
- `gateway` (string, 可选): 网关
- `dns` (string, 可选): DNS

### 更新 IP 地址段
**接口：** `POST /network/subnet-update`

**参数：**
- `id` (int, 必填): ID
- `name` (string, 可选): 名称
- `subnet` (string, 可选): 子网
- `gateway` (string, 可选): 网关
- `dns` (string, 可选): DNS

### 删除 IP 地址段
**接口：** `POST /network/subnet-delete`

**参数：**
- `ids` (array, 必填): ID数组

### 获取 IP 地址列表
**接口：** `POST /network/ip-list`

**参数：**
- `subnet_id` (int, 必填): 子网ID
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词搜索

### 添加 IP 地址
**接口：** `POST /network/ip-add`

**参数：**
- `subnet_id` (int, 必填): 子网ID
- `ip` (string, 必填): IP地址
- `mac` (string, 可选): MAC地址
- `host_id` (int, 可选): 关联主机ID
- `description` (string, 可选): 描述

### 更新 IP 地址
**接口：** `POST /network/ip-update`

**参数：**
- `id` (int, 必填): ID
- `ip` (string, 可选): IP地址
- `mac` (string, 可选): MAC地址
- `host_id` (int, 可选): 关联主机ID
- `description` (string, 可选): 描述

### 删除 IP 地址
**接口：** `POST /network/ip-delete`

**参数：**
- `ids` (array, 必填): ID数组

## CMDB 资产管理

### 同步库存
**接口：** `POST /cmdb/sync-stock`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 获取业务列表
**接口：** `POST /cmdb/businesses`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 获取模型对象列表
**接口：** `POST /cmdb/objects`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 获取资产列表
**接口：** `POST /cmdb/instances`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 创建资产实例
**接口：** `POST /cmdb/create-instance`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 更新资产实例
**接口：** `POST /cmdb/update-instance`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 删除资产实例
**接口：** `POST /cmdb/delete-instance`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 关联查询
**接口：** `POST /cmdb/relation-query`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

### 业务树
**接口：** `POST /cmdb/business-tree`

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

## 知识库

### 获取知识库列表
**接口：** `POST /knowledge/list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词搜索
- `category` (string, 可选): 分类

### 添加知识
**接口：** `POST /knowledge/add`

**参数：**
- `title` (string, 必填): 标题
- `content` (string, 必填): 内容
- `category` (string, 可选): 分类
- `tags` (string, 可选): 标签

### 更新知识
**接口：** `POST /knowledge/update`

**参数：**
- `id` (int, 必填): 知识ID
- `title` (string, 可选): 标题
- `content` (string, 可选): 内容
- `category` (string, 可选): 分类
- `tags` (string, 可选): 标签

### 删除知识
**接口：** `POST /knowledge/delete`

**参数：**
- `ids` (array, 必填): 知识ID数组

## 资源配置

### 获取配置列表
**接口：** `POST /config/list`

**参数：**
- `type` (string, 可选): 配置类型

### 更新配置
**接口：** `POST /config/update`

**参数：**
- `key` (string, 必填): 配置键
- `value` (string, 必填): 配置值

## 系统管理

### 获取系统信息
**接口：** `POST /system/info`

**参数：** 无

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "version": "6.0.0",
        "build": "20231201",
        "license": {
            "type": "enterprise",
            "expiry": "2025-12-31"
        }
    }
}
```

### 获取系统状态
**接口：** `POST /system/status`

**参数：** 无

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "cpu_usage": 45.2,
        "memory_usage": 62.8,
        "disk_usage": 38.5,
        "service_status": "running"
    }
}
```
