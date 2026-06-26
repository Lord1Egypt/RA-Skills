---
name: jf-open-pro-ai-child-care
description: 杰峰开放平台儿童看护技能。实时监控客厅、书房等场景，提供人身、生活安全守护，及时掌握孩子在家状态，保障安全的同时，关注其生活起居、学习娱乐情况。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 儿童看护
    - 安全守护
    - 行为统计
    - 居家安全
  triggers:
    - 儿童看护
    - 孩子看护
    - 异常告警
    - 行为统计
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
    - 需开通儿童看护套餐
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-ai-child-care - 儿童看护技能

## 技能描述

实时监控客厅、书房等场景，提供人身、生活安全守护，及时掌握孩子在家状态，保障安全的同时，关注其生活起居、学习娱乐情况。

**核心功能：**
- **服务状态管理** - 开启/关闭儿童看护服务
- **异常提醒配置** - 查询和设置异常提醒（可疑人员/危险区域/久未出现/进入离开）
- **异常告警查询** - 查询可疑车辆/可疑人员/非机动车/明火等告警
- **陌生人管理** - 添加/移除陌生人到人形库
- **行为统计** - 查询学习/娱乐/吃喝/走动/坐卧的次数和时间
- **七日图表** - 查询近七日行为时间图表

## 触发词

- 儿童看护 / 孩子看护 / 居家安全
- 异常告警 / 行为统计 / 学习娱乐

## ⚠️ 环境变量检查（使用前必读）

**使用本技能前，必须先检查以下 7 个必需环境变量是否已配置！**

### 检查清单

| 序号 | 环境变量 | 配置项 | 是否必需 | 检查状态 |
|------|----------|--------|----------|----------|
| 1 | `JF_UUID` | `jf_uuid` | ✅ 必需 | □ 已配置 |
| 2 | `JF_APP_KEY` | `jf_appKey` | ✅ 必需 | □ 已配置 |
| 3 | `JF_APP_SECRET` | `jf_secret` | ✅ 必需 | □ 已配置 |
| 4 | `JF_MOVE_CARD` | `jf_moveCard` | ✅ 必需 | □ 已配置 |
| 5 | `JF_DEVICE_SN` | `jf_device_sn` | ✅ 必需 | □ 已配置 |
| 6 | `JF_AUTHORIZATION` | `jf_authorization` | ✅ 必需 | □ 已配置 |
| 7 | `JF_USER` | `jf_user` | ✅ 必需 | □ 已配置 |

## 前置条件

### 前置条件

1. **设备在线** - 设备需在线且可访问
2. **设备绑定** - 设备需先绑定到开放平台账号
3. **套餐开通** - 需开通相应 AI 套餐 - 需开通儿童看护 AI 套餐

签名算法** - 使用杰峰官方 `SignatureUtil.getEncryptStr()` 方法生成 signature
2. **时间戳算法** - 使用杰峰官方 `TimeMillisUtil.getTimMillis()` 方法生成 timeMillis
3. **设备绑定** - 设备需先绑定到开放平台账号

## 环境变量

| 变量名 | 配置项 | 说明 | 默认值 | 必需 |
|--------|------|------|--------|------|
| `JF_UUID` | `jf_uuid` | 开放平台用户 uuid | - | ✅ |
| `JF_APP_KEY` | `jf_appKey` | 开放平台应用 appKey | - | ✅ |
| `JF_APP_SECRET` | `jf_secret` | 开放平台应用密钥 | - | ✅ |
| `JF_MOVE_CARD` | `jf_moveCard` | 移动卡标识（用于签名） | `2` | ✅ |
| `JF_DEVICE_SN` | `jf_device_sn` | 设备序列号 | - | ✅ |
| `JF_AUTHORIZATION` | `jf_authorization` | 用户 token (JWT) | - | ✅ |
| `JF_USER` | `jf_user` | 用户 ID | - | ✅ |
| `JF_ENDPOINT` | - | API 接入地址 | `api.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 查询服务状态 | `POST /child/ai/analysis/switch/get` | POST | ✅ | ✅ |
| 开关服务 | `POST /child/ai/analysis/switch/change` | POST | ✅ | ✅ |
| 查询异常配置 | `POST /child/abnormalAlarmConfig/list` | POST | ✅ | ✅ |
| 更新异常配置 | `POST /child/abnormalAlarmConfig/save` | POST | ✅ | ✅ |
| 批量更新配置 | `POST /child/abnormalAlarmConfig/batchSave` | POST | ✅ | ✅ |
| 异常告警列表 | `POST /child/alarm/page` | POST | ✅ | ✅ |
| 添加陌生人 | `POST /child/stranger/add` | POST | ✅ | ✅ |
| 移除陌生人 | `POST /child/stranger/remove` | POST | ✅ | ✅ |
| 行为次数 | `POST /child/static/queryCount` | POST | ✅ | ✅ |
| 行为时间 | `POST /child/static/queryTime` | POST | ✅ | ✅ |
| 七日图表 | `POST /child/static/queryTimeForChart` | POST | ✅ | ✅ |

## 核心功能

### 1. 服务状态管理

**查询服务状态：** `POST /child/ai/analysis/switch/get`

**开关服务：** `POST /child/ai/analysis/switch/change`

### 2. 异常提醒配置

**异常类型枚举：**
| 枚举值 | 说明 |
|--------|------|
| `SuspectedStranger` | 可疑人员停留 |
| `DangerousArea` | 危险区域 |
| `LongTimeDisappear` | 久未出现 |
| `EnterAndLeft` | 出现离开 |

**告警类型枚举：**
| 枚举值 | 说明 |
|--------|------|
| `VehicleParking` | 可疑车辆停留 |
| `PIRAlarm` | 可疑人员徘徊 |
| `NonMotorVehicleParking` | 非机动车停留 |
| `FireDetection` | 明火检测 |

### 3. 陌生人管理

**添加到人形库：** `POST /child/stranger/add`

**移除人形库：** `POST /child/stranger/remove`

### 4. 行为统计

**行为类型枚举：**
| 枚举值 | 说明 |
|--------|------|
| `studying` | 学习 |
| `playing` | 娱乐 |
| `eating` | 吃喝 |
| `walking` | 走动 |
| `sitting` | 坐卧 |

## 使用示例

### 环境准备

```bash
# 设置环境变量
export JF_UUID="<your-uuid>"
export JF_APP_KEY="<your-appkey>"
export JF_APP_SECRET="<your-secret>"
export JF_MOVE_CARD="7"
export JF_DEVICE_SN="<your-device-sn>"
export JF_AUTHORIZATION="eyJhbGciOiJIUzI1NiIs..."
export JF_USER="<your-uuid>"
export JF_ENDPOINT="api.jftechws.com"
```

### 1. 查询服务状态

```bash
cd ~/.openclaw/workspace/jf-open-pro-ai-child-care/scripts

# 查询儿童看护服务状态
python3 child_care.py --action status \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 2. 查询异常告警

```bash
# 查询可疑人员告警
python3 alarm_query.py --action list \
  --msg-type "PIRAlarm" \
  --start-time 1733241600 --end-time 1733846399 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 3. 陌生人管理

```bash
# 添加陌生人到人形库
python3 stranger_manager.py --action add \
  --alarm-id "240911184509171" \
  --image "https://..." \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 从人形库移除
python3 stranger_manager.py --action remove \
  --alarm-id "240911184509171" \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 4. 查询行为统计

```bash
# 查询今日学习次数
python3 stats_query.py --action count \
  --type "studying" \
  --start-time 1733241600 --end-time 1733327999 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 查询近七日学习时间图表
python3 stats_query.py --action week-chart \
  --type "studying" \
  --start-time 1732982400 --end-time 1733587199 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | authorization 过期，重新获取 |
| 12504 | 授权失败 - 设备未开通套餐 | 登录开放平台为设备绑定儿童看护套餐卡 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 错误码 12504 详细处理步骤

**错误信息：** `authorize failed,Please check it in the open platform`

**原因：** 设备未开通儿童看护服务，或未绑定套餐卡

**解决步骤：**

1. 登录杰峰开放平台：https://developer.jftech.com
2. 进入 **套餐管理** / **服务管理**
3. 找到 **儿童看护** 套餐
4. 为设备购买并绑定套餐卡
5. 等待配置生效（通常 1-5 分钟）
6. 重新调用 API 测试

## 注意事项

1. **时间戳** - 统计查询使用秒级时间戳
2. **套餐开通** - 使用前需确保设备已开通儿童看护套餐
3. **Token 有效期** - authorization 需在有效期内
4. **签名算法** - 使用杰峰官方移位加密算法

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/child_care.py` | 服务状态管理脚本 |
| `scripts/alarm_query.py` | 告警查询脚本 |
| `scripts/stranger_manager.py` | 陌生人管理脚本 |
| `scripts/stats_query.py` | 统计数据查询脚本 |
| `references/child-care-api.md` | API 参考文档 |

## 参考文档

- [杰峰开放平台](https://developer.jftech.com)
- [签名算法](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh)
- [时间戳算法](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh)
- [套餐卡使用说明](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh)

---

# 📋 前置配置文档（环境变量缺失时参考）

> **⚠️ 重要提示：** 如果在使用本技能时发现缺少必需的环境变量，请先完成以下配置步骤，然后再继续操作。

## 必需环境变量清单

以下 **7 个环境变量** 必须全部配置，缺一不可：

| # | 变量名 | 配置项 | 说明 |
|---|--------|--------|------|
| 1 | `JF_UUID` | `jf_uuid` | 开放平台用户 uuid |
| 2 | `JF_APP_KEY` | `jf_appKey` | 开放平台应用 appKey |
| 3 | `JF_APP_SECRET` | `jf_secret` | 开放平台应用密钥 |
| 4 | `JF_MOVE_CARD` | `jf_moveCard` | 移动卡标识（用于签名） |
| 5 | `JF_DEVICE_SN` | `jf_device_sn` | 设备序列号 |
| 6 | `JF_AUTHORIZATION` | `jf_authorization` | 用户 token (JWT) |
| 7 | `JF_USER` | `jf_user` | 用户 ID |

---

## 参数获取指南

### 1. JF_UUID（jf_uuid）

**获取方式：**
- 登录杰峰开放平台：https://developer.jftech.com
- 进入 **个人中心** 或 **开发者信息**
- 复制您的用户 UUID

**说明：** 这是您在杰峰开放平台的唯一用户标识

---

### 2. JF_APP_KEY（jf_appKey）

**获取方式：**
- 登录杰峰开放平台：https://developer.jftech.com
- 进入 **应用管理** → **我的应用**
- 选择或创建一个应用
- 复制应用的 `appKey`

**说明：** 这是您创建的应用的唯一标识

---

### 3. JF_APP_SECRET（jf_secret）

**获取方式：**
- 登录杰峰开放平台：https://developer.jftech.com
- 进入 **应用管理** → **我的应用**
- 选择对应的应用
- 查看应用详情，复制 `secret` 密钥

**说明：** 这是应用的密钥，用于 API 签名，请妥善保管

---

### 4. JF_MOVE_CARD（jf_moveCard）

**获取方式：**
- **方式一：** 通过 appKey 查询接口获取并缓存（24 小时有效）
- **方式二：** 登录杰峰开放平台，进入应用详情页查看

**说明：** 移动卡标识，用于签名算法生成

---

### 5. JF_DEVICE_SN（jf_device_sn）

**获取方式：**
- 查看设备底部标签或包装盒上的序列号
- 或在杰峰开放平台 **设备管理** 中查看已绑定的设备

**说明：** 设备的唯一序列号，格式通常为 16 位十六进制字符串

---

### 6. JF_AUTHORIZATION（jf_authorization）⭐

**获取方式（二选一）：**

#### 方式 A：使用杰峰用户系统
> 请参考 **用户登录接口** 获取 Authorization 值
> 
> 调用登录接口后，从响应中提取 `authorization` 字段（JWT Token）

#### 方式 B：使用开发者自己的用户系统
> 传值参考 **套餐卡使用说明** 中的 `userId`
> 
> 将您的用户系统生成的 userId 作为 authorization 值传入

**说明：** 用户鉴权 Token，用于 API 请求的身份验证

---

### 7. JF_USER（jf_user）

**获取方式：**
- 与 `JF_UUID` 通常相同
- 或在杰峰开放平台 **个人中心** 查看用户 ID

**说明：** 用户 ID，用于 API 请求中标识当前用户

---

## 配置示例

完成上述参数获取后，在您的环境中设置：

```bash
# 设置环境变量（请替换为您的实际值）
export JF_UUID="your-uuid-here"
export JF_APP_KEY="your-appkey-here"
export JF_APP_SECRET="your-secret-here"
export JF_MOVE_CARD="your-movecard-here"
export JF_DEVICE_SN="your-device-sn-here"
export JF_AUTHORIZATION="your-authorization-token-here"
export JF_USER="your-user-id-here"
export JF_ENDPOINT="api.jftechws.com"  # 可选，默认值
```

---

## 验证配置

配置完成后，可以先调用一个简单的接口验证配置是否正确：

```bash
# 查询服务状态（验证配置）
python3 child_care.py --action status \
  --sn "$JF_DEVICE_SN" \
  --user "$JF_USER"
```

如果返回 `code: 2000`，说明配置成功！

---

## 重要提醒

> **使用原则：** 后续所有 API 调用，必须严格使用用户环境变量中配置的参数值，**不允许**技能自己发散去获取或推算参数！
> 
> 这样可以确保：
> - 参数来源可控、可追溯
> - 避免使用错误的或过期的凭证
> - 符合安全和审计要求
