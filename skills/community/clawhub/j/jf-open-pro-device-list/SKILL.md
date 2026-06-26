---
name: jf-open-pro-device-list
description: 杰峰设备列表查询技能（开发版）。查询开发者账号下绑定的设备列表，支持分页查询和按设备序列号条件查询。
metadata:
  version: 1.0.0
  author: JFTech
  category: device
  tags:
    - 杰峰
    - 设备列表
    - 设备查询
    - 分页查询
    - 设备管理
  triggers:
    - 查询设备列表
    - 设备列表
    - 我的设备
    - 绑定设备
    - 设备分页
  prerequisites:
    - 配置必需的环境变量
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-device-list - 杰峰设备列表查询技能（开发版）

## 技能描述

支持查询开发者账号下绑定的设备信息列表：

- **分页查询** - 获取账号下所有绑定的设备
- **条件查询** - 按设备序列号列表查询（最多 100 个）
- **设备信息** - 返回设备序列号、用户名、昵称、Token 等

## 触发词

- 查询设备列表 / 设备列表 / 我的设备
- 绑定设备 / 设备分页 / 查询绑定设备

## 前置条件

### 必需配置

1. **签名算法** - 使用杰峰官方移位加密算法生成 signature
2. **时间戳算法** - counter(7 位) + timeMillis(13 位)，实时生成
3. **开放平台账号** - 需要有绑定的设备

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `JF_UUID` | 开放平台用户 uuid | - | ✅ |
| `JF_APP_KEY` | 开放平台应用 appKey | - | ✅ |
| `JF_APP_SECRET` | 开放平台应用密钥 | - | ✅ |
| `JF_MOVE_CARD` | 移动卡标识（用于签名） | `2` | ✅ |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 |
|------|------|------|
| 查询设备列表 | `POST /gwp/v3/rtc/device/list` | POST |

## 核心功能

### 设备列表查询（Device List）

**API:** `POST /gwp/v3/rtc/device/list`

**请求参数：**
| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | ❌ | `1` | 页码（分页查询） |
| limit | int | ❌ | `100` | 每页数量（最大 100） |
| sns | string[] | ❌ | - | 设备序列号列表（最多 100 个） |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 平台状态码（2000=成功） |
| msg | string | 响应消息 |
| data | object | 响应数据 |
| └─ deviceList | object[] | 设备列表 |
| &nbsp;&nbsp;&nbsp;&nbsp;├─ sn | string | 设备序列号 |
| &nbsp;&nbsp;&nbsp;&nbsp;├─ username | string | 设备登录用户名 |
| &nbsp;&nbsp;&nbsp;&nbsp;├─ password | string | 设备登录密码 |
| &nbsp;&nbsp;&nbsp;&nbsp;├─ nickname | string | 设备昵称 |
| &nbsp;&nbsp;&nbsp;&nbsp;└─ loginToken | string | 设备登录 Token |

## 查询场景

### 场景 1：分页查询

获取开发者账号下的所有绑定设备信息列表。

**请求示例：**
```json
{
  "page": 1,
  "limit": 100
}
```

### 场景 2：条件查询（按设备序列号列表）

指定设备序列号查询设备信息列表（最多 100 个）。

**请求示例：**
```json
{
  "sns": ["5e26d516f54f500dxxxx", "115477b8705dxxxx"]
}
```

## 使用示例

### 环境准备

```bash
# 设置环境变量（使用占位符，请替换为实际值）
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_MOVE_CARD="2"
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 查询设备列表（分页）

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-device-list/scripts

# 查询第 1 页，每页 100 个
python3 device_list.py --action list

# 查询第 2 页
python3 device_list.py --action list --page 2

# 每页 50 个
python3 device_list.py --action list --limit 50
```

### 2. 按设备序列号查询

```bash
# 查询指定设备
python3 device_list.py --action query-by-sns \
  --sns "devicesnxxxx"

# 查询多个设备（最多 100 个）
python3 device_list.py --action query-by-sns \
  --sns "devicesnxxxx,devicesnyyyy"
```

### 3. 从文件读取设备序列号

```bash
# 从文件读取设备序列号列表
python3 device_list.py --action query-by-sns \
  --sns-file "devices.txt"
```

### 4. 格式化输出

```bash
# 表格格式输出（推荐）
python3 device_list.py --action list --format table

# JSON 格式输出
python3 device_list.py --action list --format json
```

## 设备序列号文件格式

```
# devices.txt - 设备序列号列表文件
# 格式：每行一个设备序列号
devicesnxxxx
devicesnyyyy
devicesnzzzz
```

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | 检查 uuid 和 appKey |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

## 注意事项

1. **分页限制** - 每页最大 100 个设备
2. **条件查询** - 最多查询 100 个设备序列号
3. **设备信息** - 部分设备可能没有 nickname 或 loginToken
4. **密码安全** - 设备密码可能为空或加密显示

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/device_list.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
