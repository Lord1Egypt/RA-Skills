---
name: jf-open-pro-device-reboot
description: 杰峰设备重启技能（开发版）。支持远程重启设备，部分设备支持关闭操作。
metadata:
  version: 1.0.0
  author: JFTech
  category: device
  tags:
    - 杰峰
    - 设备重启
    - 远程重启
    - 设备关闭
    - 设备管理
  triggers:
    - 重启设备
    - 设备重启
    - 远程重启
    - 关闭设备
    - 设备关机
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-device-reboot - 杰峰设备重启技能（开发版）

## 技能描述

支持杰峰设备远程重启功能：

- **设备重启** - 远程重启设备
- **设备关闭** - 部分设备支持关闭操作（大部分设备为重启）

**⚠️ 警告：** 重启设备会导致设备暂时离线，请谨慎操作。

## 触发词

- 重启设备 / 设备重启 / 远程重启
- 关闭设备 / 设备关机

## 前置条件

### 必需配置

1. **签名算法** - 使用杰峰官方移位加密算法生成 signature
2. **时间戳算法** - counter(7 位) + timeMillis(13 位)，实时生成
3. **设备绑定** - 设备需先绑定到开放平台账号
4. **设备在线** - 设备需在线才能执行重启

### 环境变量

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| `JF_UUID` | 开放平台用户 uuid | - | ✅ |
| `JF_APP_KEY` | 开放平台应用 appKey | - | ✅ |
| `JF_APP_SECRET` | 开放平台应用密钥 | - | ✅ |
| `JF_MOVE_CARD` | 移动卡标识（用于签名） | `2` | ✅ |
| `JF_DEVICE_SN` | 设备序列号 | - | ✅ |
| `JF_DEVICE_TOKEN` | 设备接口访问令牌 | - | ✅ |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 设备重启/关闭 | `POST /gwp/v3/rtc/device/opdev/{token}` | POST | ✅ | ✅ |

## 核心功能

### 设备重启/关闭（OPMachine）

**API:** `POST /gwp/v3/rtc/device/opdev/{deviceToken}`

**Name:** `OPMachine`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| Name | string | ✅ | 固定为 `OPMachine` |
| OPMachine.Action | string | ✅ | `Reboot`=重启，`Shutdown`=关闭 |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 平台状态码（2000=成功） |
| msg | string | 响应消息 |
| data | object | 响应数据 |
| ├─ Name | string | 方法名称 |
| ├─ Ret | int | 设备状态码（100=成功） |
| └─ SessionID | string | 会话 ID |

## 使用示例

### 环境准备

```bash
# 设置环境变量（使用占位符，请替换为实际值）
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_MOVE_CARD="2"
export JF_DEVICE_SN="devicesnxxxx"
export JF_DEVICE_TOKEN="devicetokenxxxx"
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 重启设备

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-device-reboot/scripts

# 重启设备
python3 device_reboot.py --action reboot
```

### 2. 关闭设备（部分设备支持）

```bash
# 关闭设备
python3 device_reboot.py --action shutdown
```

### 3. 确认操作

```bash
# 带确认提示的重启
python3 device_reboot.py --action reboot --confirm

# 带确认提示的关闭
python3 device_reboot.py --action shutdown --confirm
```

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | deviceToken 过期，重新获取 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 设备状态码（Ret）

| Ret | 说明 |
|-----|------|
| 100 | 成功 |

## 注意事项

1. **⚠️ 谨慎操作** - 重启会导致设备暂时离线
2. **设备在线** - 设备需在线才能执行重启
3. **关闭支持** - 大部分设备只支持重启，不支持关闭
4. **Token 有效期** - deviceToken 有效期 24 小时
5. **重启时间** - 设备重启通常需要 1-3 分钟
6. **业务影响** - 重启期间无法进行任何设备操作

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/device_reboot.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
