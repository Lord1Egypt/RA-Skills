---
name: lerwee-api
description: 乐维监控系统 API 集成工具。提供完整的 API 签名认证、监控对象管理、告警查询、事件平台等 86+ 个接口的调用能力。
---

# Lerwee API Skill - 乐维监控系统 API 集成

> **当前版本**: v6.0 | **最后更新**: 2026-03-11 | **状态**: 与官方文档完全同步

## 配置

设置 API 凭证和服务器信息：

```bash
# 服务器配置
export LERWEE_BASE_URL="http://192.168.1.79:8081/api/v6"
export LERWEE_SECRET=""
```

## API 基础信息

- **Base URL**: `http://192.168.1.79:8081/api/v6`
- **请求方法**: POST
- **Content-Type**: `application/json`
- **字符编码**: UTF-8
- **时间格式**: 北京时间 (UTC+8)
- **认证方式**: 签名验证

## 签名算法

### 普通接口签名

所有接口需要在请求参数中包含：

1. **timestamp** (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
2. **sign** (string, 必填): 请求签名

**签名计算步骤：**

```python
import hashlib

def make_sign(params, secret):
    """
    计算签名

    Args:
        params: 请求参数字典
        secret: 密钥

    Returns:
        签名字符串
    """
    # 1. 过滤空值、数组、sign 字段
    filtered = {k: v for k, v in params.items()
                if k != 'sign' and v != "" and v is not None and not isinstance(v, list)}

    # 2. 按键名字典序排序
    sorted_items = sorted(filtered.items())

    # 3. 拼接字符串（不包含键值分隔符）
    str_to_sign = ''.join([f"{k}{v}" for k, v in sorted_items])

    # 4. 计算签名
    sign = hashlib.sha1((secret + str_to_sign).encode('utf-8')).hexdigest().lower()

    return sign
```

### 特殊接口签名（事件平台等）

部分接口（如 `/aialert/*`）使用 JSON 序列化的 `data` 字段：

```python
import json
import time

def make_data_params(data_dict, appid, token):
    """
    生成 data 参数和签名

    Args:
        data_dict: data 参数内容
        appid: 应用 ID
        token: 应用 token

    Returns:
        (data_json, timestamp, sign)
    """
    # 1. 添加 appid 和 token
    data_dict['appid'] = appid
    data_dict['token'] = token

    # 2. JSON 序列化
    data_json = json.dumps(data_dict, separators=(',', ':'))

    # 3. 生成时间戳
    timestamp = int(time.time())

    # 4. 计算签名
    sign_str = token + data_json + str(timestamp)
    sign = hashlib.sha1(sign_str.encode('utf-8')).hexdigest().lower()

    return data_json, timestamp, sign
```

## API 模块索引

### 1. 监控中心 (Monitor)
- 监控对象管理（列表、创建、更新、删除）
- 监控对象详情、指标、宏
- 监控类型和配置

📄 **详细参数**: `references/api_details_monitor.md`

### 2. 设备探测 (Device Detection)
- Agent 列表、创建、安装、卸载
- Agent 状态检查
- 批量操作

📄 **详细参数**: `references/api_details_device.md`

### 3. 告警管理 (Alert)
- 告警列表、问题列表
- 告警统计、确认
- 告警历史查询

📄 **详细参数**: `references/api_details_alert.md`

### 4. 事件平台 (Event Platform)
- 事件列表、详情、关闭
- 事件数据接收
- 告警处理状态更新
- 第三方告警恢复

📄 **详细参数**: `references/api_details_alert.md`

### 5. 事件平台告警 (AI Alert)
- 告警列表、状态更新
- 告警关闭
- 第三方推送告警恢复（特殊签名）

📄 **详细参数**: `references/api_details_alert.md`

### 6. 业务视图 (Business View)
- 组织树、业务树
- 业务列表、告警、主机
- 业务统计

📄 **详细参数**: `references/api_details_business.md`

### 7. 链路监控 (Link Monitor)
- 链路列表、详情
- 链路添加、更新、删除

📄 **详细参数**: `references/api_details_business.md`

### 8. 网络拓扑 (Network Topology)
- 拓扑图列表、详情
- 拓扑图添加、更新、删除
- 节点和连线管理

📄 **详细参数**: `references/api_details_business.md`

### 9. 用户管理 (User Management)
- 用户列表、创建、更新、删除
- 部门管理
- 角色管理

📄 **详细参数**: `references/api_details_user.md`

### 10. 自动化运维 (Automation)
- 脚本执行
- 执行结果查询

📄 **详细参数**: `references/api_details_user.md`

### 11. 虚拟化管理 (Virtualization)
- 虚拟中心管理
- 虚拟机列表

📄 **详细参数**: `references/api_details_user.md`

### 12. 网络管理 (Network)
- IP 地址段管理
- IP 地址管理

📄 **详细参数**: `references/api_details_user.md`

### 13. 资产管理 (Asset)
- 资产列表、添加、更新、删除

📄 **详细参数**: `references/api_details_user.md`

### 14. 知识库 (Knowledge)
- 知识列表、添加、更新、删除

📄 **详细参数**: `references/api_details_user.md`

## 返回格式

所有接口返回统一的 JSON 格式：

```json
{
    "code": 0,
    "message": "",
    "data": {
        // 具体数据内容
    }
}
```

- **code**: 状态码（0 表示成功，非 0 表示失败）
- **message**: 消息说明
- **data**: 返回数据（成功时存在）

## 错误码

常见错误码：
- `0`: 成功
- `403`: 签名异常或认证失败
- `404`: 接口不存在
- `500`: 服务器内部错误

📄 **详细错误码**: `references/error_codes.md`

## 使用示例

### Python 示例

```python
import requests
import json
import hashlib
import time

base_url = "http://192.168.1.79:8081/api/v6"
secret = ""

def make_sign(params):
    sorted_items = sorted(params.items())
    str_to_sign = ''.join([f"{k}{v}" for k, v in sorted_items
                          if k != 'sign' and v != "" and v is not None
                          and not isinstance(v, list)])
    return hashlib.sha1((secret + str_to_sign).encode('utf-8')).hexdigest().lower()

# 调用监控对象列表
params = {
    "page": 1,
    "pageSize": 20,
    "keyword": "linux"
}
params["timestamp"] = int(time.time())
params["sign"] = make_sign(params)

response = requests.post(f"{base_url}/monitor/host-list", json=params)
print(response.json())
```

### cURL 示例

```bash
# 获取监控对象列表
curl -X POST "http://192.168.1.79:8081/api/v6/monitor/host-list" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "pageSize": 20,
    "keyword": "linux",
    "timestamp": 1678838400,
    "sign": " computed_signature_here "
  }'
```

## 参考文档

### 快速查询
- `references/api_endpoints.md` - 完整 API 端点列表（按模块分类）

### 详细参数
- `references/api_details_monitor.md` - 监控中心详细参数
- `references/api_details_device.md` - 设备探测详细参数
- `references/api_details_alert.md` - 告警与事件详细参数
- `references/api_details_business.md` - 业务视图与拓扑详细参数
- `references/api_details_user.md` - 用户管理与其他模块详细参数

### 参考数据
- `references/monitoring_types.md` - 监控类型对照表
- `references/error_codes.md` - 错误码详解

## 注意事项

1. **时间格式**: 所有时间戳使用 Unix 时间戳（秒），时区为北京时间 (UTC+8)
2. **历史数据时间**: 返回的历史数据中，`graph.data` 为毫秒级时间戳，`text.data.clock` 为秒级时间戳，**显示时需转换为北京时间 (UTC+8)**
3. **请求方法**: 所有接口使用 POST 方法
4. **签名计算**: 必须跳过 `sign` 字段本身、空值和数组类型参数
5. **特殊接口**: 事件平台相关接口使用 JSON 序列化的 `data` 字段
6. **分页参数**: 列表类接口通常使用 `page` 和 `pageSize` 参数

**时间转换示例（北京时间）：**
```python
from datetime import datetime, timezone, timedelta

beijing_tz = timezone(timedelta(hours=8))

# 秒级时间戳
dt = datetime.fromtimestamp(clock, beijing_tz)
print(dt.strftime('%Y-%m-%d %H:%M:%S'))  # 2026-03-11 18:41:32

# 毫秒级时间戳
dt = datetime.fromtimestamp(timestamp_ms / 1000, beijing_tz)
```

## 脚本工具

- `scripts/lerwee_api.py` - Python API 客户端封装
- `scripts/sign_test.py` - 签名算法测试工具

## 版本历史

- **v6.0** (2026-03-11): 与官方文档完全同步，覆盖 86+ 个接口
- **v5.0** (2025-12-01): 初始版本

## 支持与反馈

如有问题，请联系系统管理员。
