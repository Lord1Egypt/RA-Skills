---
name: jf-open-pro-ai-elderly-care
description: 杰峰开放平台老人看护技能。适配独居、日间无人看护老人场景，全天候守护居家安全与健康，帮助家属实时掌握老人状态，轻松远程看护，消除照护顾虑。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 老人看护
    - 跌倒检测
    - 异常行为
    - 远程照护
  triggers:
    - 老人看护
    - 跌倒告警
    - 异常行为检测
    - 远程看护
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
    - 需开通老人看护套餐
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-ai-elderly-care - 老人看护技能

## 技能描述

适配独居、日间无人看护老人场景，全天候守护居家安全与健康，帮助家属实时掌握老人状态，轻松远程看护，消除照护顾虑。

**核心功能：**
- **跌倒告警** - 实时检测老人跌倒事件，推送告警通知
- **异常行为检测** - 久坐、久卧、久未出现异常提醒
- **服务状态管理** - 开启/关闭老人看护服务
- **异常提醒配置** - 查询和设置异常提醒阈值
- **今日统计** - 查询今日作息和饮食数据
- **七日统计** - 查询近七日作息和饮食记录

## 触发词

- 老人看护 / 跌倒告警 / 远程看护
- 异常行为检测 / 久坐久卧 / 老人监护

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
3. **套餐开通** - 需开通相应 AI 套餐 - 需开通老人看护 AI 套餐

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
| 查询服务状态 | `POST /elderly/ai/analysis/switch/get` | POST | ✅ | ✅ |
| 开关服务 | `POST /elderly/ai/analysis/switch/change` | POST | ✅ | ✅ |
| 查询异常配置 | `POST /elderly/abnormalBehavior/findConfigList` | POST | ✅ | ✅ |
| 更新异常配置 | `POST /elderly/abnormalBehavior/updateConfig` | POST | ✅ | ✅ |
| 跌倒告警列表 | `POST /elderly/falldown/alarm/page` | POST | ✅ | ✅ |
| 异常行为告警 | `POST /elderly/behavior/alarm/page` | POST | ✅ | ✅ |
| 今日作息统计 | `POST /elderly/static/dailyRoutineRecord/*` | POST | ✅ | ✅ |
| 今日饮食统计 | `POST /elderly/static/dailyDietRecord/*` | POST | ✅ | ✅ |
| 七日作息记录 | `POST /elderly/static/weekRoutineRecord` | POST | ✅ | ✅ |
| 七日饮食记录 | `POST /elderly/static/weekDietRecord` | POST | ✅ | ✅ |

## 核心功能

### 1. 服务状态管理

**查询服务状态：** `POST /elderly/ai/analysis/switch/get`

**开关服务：** `POST /elderly/ai/analysis/switch/change`

### 2. 异常提醒配置

**异常行为类型枚举：**
| 枚举值 | 说明 |
|--------|------|
| `0` | 久未出现 |
| `1` | 久坐 |
| `2` | 久卧 |

### 3. 跌倒告警查询

**跌倒告警列表：** `POST /elderly/falldown/alarm/page`

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| data.total | integer | 告警总数 |
| data.records | array | 告警列表 |
| ├─ alarmId | string | 告警 ID |
| ├─ sn | string | 设备号 |
| ├─ picUrl | string | 告警图片地址 |
| ├─ videoUrl | string | 告警视频地址 |
| └─ alarmTime | string | 告警时间 |

### 4. 异常行为告警查询

**异常行为告警：** `POST /elderly/behavior/alarm/page`

### 5. 今日统计数据

**今日作息统计：**
- `walkCount` - 走路次数
- `sitAndLyingCount` - 坐卧次数
- `playCount` - 娱乐次数
- `walkTime` - 走路时间（秒）
- `sitAndLyingTime` - 坐卧时间（秒）
- `playTime` - 娱乐时间（秒）

**今日饮食统计：**
- `eatCount` - 吃饭次数
- `drinkCount` - 喝水次数
- `eatTime` - 吃饭时间（秒）
- `drinkTime` - 喝水时间（秒）

### 6. 近七日统计数据

**七日作息记录：** `POST /elderly/static/weekRoutineRecord`

**响应：**
```json
{
  "data": [
    {
      "walkTime": 3600,
      "sitAndLieTime": 3600,
      "playTime": 3600,
      "day": "2024-05-21"
    }
  ]
}
```

**七日饮食记录：** `POST /elderly/static/weekDietRecord`

**响应：**
```json
{
  "data": [
    {
      "eatCount": 3,
      "drinkCount": 8,
      "day": "2024-05-21"
    }
  ]
}
```

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
cd ~/.openclaw/workspace/jf-open-pro-ai-elderly-care/scripts

# 查询老人看护服务状态
python3 elderly_care.py --action status \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 2. 开关服务

```bash
# 开启老人看护服务
python3 elderly_care.py --action switch --enable true \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 3. 查询异常提醒配置

```bash
# 查询异常提醒设置
python3 config_manager.py --action list \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 更新异常提醒（开启久坐提醒，阈值 3600 秒）
python3 config_manager.py --action update \
  --behavior-type 1 --enable 1 --threshold 3600 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 4. 查询跌倒告警

```bash
# 查询跌倒告警列表（最近 7 天）
python3 alarm_query.py --action falldown \
  --start-time 1733241600 --end-time 1733846399 \
  --page 1 --rows 10 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 5. 查询今日统计

```bash
# 查询今日作息统计
python3 stats_query.py --action daily-routine \
  --start-time 1733241600 --end-time 1733327999 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 查询今日饮食统计
python3 stats_query.py --action daily-diet \
  --start-time 1733241600 --end-time 1733327999 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 6. 查询七日统计

```bash
# 查询近七日作息记录
python3 stats_query.py --action week-routine \
  --start-time 1732982400 --end-time 1733587199 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 查询近七日饮食记录
python3 stats_query.py --action week-diet \
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
| 12504 | 授权失败 - 设备未开通套餐 | 登录开放平台为设备绑定老人看护套餐卡 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 错误码 12504 详细处理步骤

**错误信息：** `authorize failed,Please check it in the open platform`

**原因：** 设备未开通老人看护服务，或未绑定套餐卡

**解决步骤：**

1. 登录杰峰开放平台：https://developer.jftech.com
2. 进入 **套餐管理** / **服务管理**
3. 找到 **老人看护** 套餐
4. 为设备购买并绑定套餐卡
5. 等待配置生效（通常 1-5 分钟）
6. 重新调用 API 测试

## 注意事项

1. **时间戳** - 统计查询使用秒级时间戳
2. **套餐开通** - 使用前需确保设备已开通老人看护套餐
3. **Token 有效期** - authorization 需在有效期内
4. **签名算法** - 使用杰峰官方移位加密算法
5. **异常行为类型** - 0=久未出现，1=久坐，2=久卧

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/elderly_care.py` | 服务状态管理脚本 |
| `scripts/config_manager.py` | 异常配置管理脚本 |
| `scripts/alarm_query.py` | 告警查询脚本 |
| `scripts/stats_query.py` | 统计数据查询脚本 |
| `references/elderly-care-api.md` | API 参考文档 |

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
export JF_ENDPOINT="api-cn.jftechws.com"  # 可选，默认值
```

---

## 验证配置

配置完成后，可以先调用一个简单的接口验证配置是否正确：

```bash
# 查询服务状态（验证配置）
python3 elderly_care.py --action status \
  --sn "$JF_DEVICE_SN" \
  --user "$JF_USER" \
  --uuid "$JF_UUID" \
  --appkey "$JF_APP_KEY" \
  --secret "$JF_APP_SECRET" \
  --auth "$JF_AUTHORIZATION" \
  --movecard "$JF_MOVE_CARD"
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
