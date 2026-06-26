---
name: jf-open-pro-device-status
description: 杰峰设备在线状态查询技能（开发版）。专注于查询设备是否在线，支持单设备或批量查询，快速返回在线/离线状态。
metadata:
  version: 1.0.0
  author: JFTech
  category: device
  tags:
    - 杰峰
    - 设备在线
    - 状态查询
    - 批量查询
    - 在线检测
  triggers:
    - 设备在线吗
    - 查询设备状态
    - 设备是否在线
    - 批量查询在线
    - 设备离线检测
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-device-status - 杰峰设备在线状态查询技能（开发版）

## 技能描述

**专注于查询设备是否在线**：

- **单设备查询** - 快速查询单个设备在线状态
- **批量查询** - 同时查询多个设备在线状态（最多 500 个）
- **简洁输出** - 只返回在线/离线状态，不做额外判断

**特别说明：** 设备与平台心跳交互，空闲时长超 250 秒即判定为离线。设备断电或断网后，最长 250 秒可查询到离线状态。

## 触发词

- 设备在线吗 / 查询设备状态 / 设备是否在线
- 批量查询在线 / 设备离线检测

## 前置条件

### 必需配置

1. **签名算法** - 使用杰峰官方移位加密算法生成 signature
2. **时间戳算法** - counter(7 位) + timeMillis(13 位)，实时生成
3. **设备绑定** - 设备需先绑定到开放平台账号

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
| 查询设备状态 | `POST /gwp/v3/rtc/device/status` | POST |

## 请求参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| deviceTokenList | string[] | ✅ | 设备 Token 列表（最多 500 个） |
| region | string | ❌ | 查询区域（`Global`=全球，`Local`=当前区域） |

## 响应参数

| 字段 | 类型 | 说明 |
|------|------|------|
| uuid | string | 设备序列号 |
| status | string | 设备状态（`online`=在线，`notfound`=离线） |
| wakeUpStatus | string | 低功耗设备唤醒状态（0=休眠，1=唤醒，2=准备休眠） |
| wakeUpEnable | string | 是否支持远程唤醒（1=支持，0=需设备端唤醒） |
| wanIp | string | 设备外网 IP |

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

### 1. 查询单设备是否在线

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-device-status/scripts

# 查询单设备
python3 device_status.py --action query \
  --device-token "devicetokenxxxx"
```

### 2. 批量查询设备在线状态

```bash
# 从文件读取设备 Token 列表批量查询
python3 device_status.py --action batch-query \
  --tokens-file "tokens.txt"
```

### 3. 表格格式输出（推荐）

```bash
# 表格格式：显示设备状态和唤醒状态
python3 device_status.py --action query \
  --device-token "devicetokenxxxx" \
  --format table
```

### 4. 按区域查询

```bash
# 只查询当前区域设备
python3 device_status.py --action batch-query \
  --tokens-file "tokens.txt" \
  --region Local
```

## 设备 Token 列表文件格式

```
# tokens.txt - 设备 Token 列表文件
# 格式：每行一个设备 Token
NTQ0NzQ3YmE3MXwyYzFk...
NTQ0NzQ3YmE3MXw5NzRj...
NTQ0NzQ3YmE3MXxiMTFm...
```

## 状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | deviceToken 过期，重新获取 |

## 注意事项

1. **心跳判定** - 设备空闲超**250 秒**判定为离线
2. **离线延迟** - 设备断电/断网后最长 250 秒可查询到离线状态
3. **批量限制** - 单次最多查询 500 个设备
4. **Token 有效期** - deviceToken 有效期 24 小时

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/device_status.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
