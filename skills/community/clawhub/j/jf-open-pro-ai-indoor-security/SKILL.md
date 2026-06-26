---
name: jf-open-pro-ai-indoor-security
description: 杰峰开放平台室内安防技能。实时监测客厅等居家场景，全方位守护人身与居家安全，实时掌握家人动态。筑牢安全防线，同步感知居家日常，安心守护居家点滴时光。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 室内安防
    - 家人看护
    - 异常检测
    - 居家安全
  triggers:
    - 室内安防
    - 家人看护
    - 异常告警
    - 居家安全
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
    - 需开通室内安防套餐
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-ai-indoor-security - 室内安防技能

## 技能描述

实时监测客厅等居家场景，全方位守护人身与居家安全，实时掌握家人动态。筑牢安全防线，同步感知居家日常，安心守护居家点滴时光。

**核心功能：**
- **服务状态管理** - 开启/关闭室内安防服务
- **异常提醒配置** - 查询和设置异常提醒（疑似陌生人/明火/危险行为）
- **异常告警查询** - 查询疑似陌生人、明火、危险行为、有人进入/离开告警
- **成员管理** - 新增、删除、修改、查询家庭成员
- **统计数据** - 查询进入/离开次数、最大人数、存在时长、日/周图表

## 触发词

- 室内安防 / 家人看护 / 居家安全
- 异常告警 / 成员管理 / 家人动态

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
3. **套餐开通** - 需开通相应 AI 套餐 - 需开通室内安防 AI 套餐

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
| 查询服务状态 | `POST /indoor/ai/analysis/switch/get` | POST | ✅ | ✅ |
| 开关服务 | `POST /indoor/ai/analysis/switch/change` | POST | ✅ | ✅ |
| 查询异常配置 | `POST /indoor/abnormalAlarmConfig/list` | POST | ✅ | ✅ |
| 更新异常配置 | `POST /indoor/abnormalAlarmConfig/save` | POST | ✅ | ✅ |
| 异常告警列表 | `POST /indoor/alarm/page` | POST | ✅ | ✅ |
| 新增成员 | `POST /indoor/face/sample/add` | POST | ✅ | ✅ |
| 删除成员 | `POST /indoor/face/sample/delete` | POST | ✅ | ✅ |
| 修改成员 | `POST /indoor/face/sample/update` | POST | ✅ | ✅ |
| 成员列表 | `POST /indoor/face/sample/list` | POST | ✅ | ✅ |
| 统计查询 | `POST /indoor/static/behavior/*` | POST | ✅ | ✅ |
| 统计图表 | `POST /indoor/static/exist/*` | POST | ✅ | ✅ |

## 核心功能

### 1. 服务状态管理

**查询服务状态：** `POST /indoor/ai/analysis/switch/get`

**开关服务：** `POST /indoor/ai/analysis/switch/change`

### 2. 异常提醒配置

**异常类型枚举：**
| 枚举值 | 说明 |
|--------|------|
| `SuspectedStranger` | 疑似陌生人 |
| `FireDetection` | 明火 |
| `DangerousBehavior` | 危险行为 |

**灵敏度枚举：**
| 枚举值 | 说明 |
|--------|------|
| `low` | 低 |
| `middle` | 中 |
| `high` | 高 |

### 3. 异常告警查询

**异常告警类型：**
| 枚举值 | 说明 |
|--------|------|
| `SuspectedStranger` | 疑似陌生人 |
| `FireDetection` | 明火 |
| `DangerousBehavior` | 危险行为 |
| `SomeoneEntered` | 有人进入 |
| `SomeoneLeft` | 有人离开 |

### 4. 成员管理

**新增成员：** `POST /indoor/face/sample/add`

**删除成员：** `POST /indoor/face/sample/delete`

**修改成员：** `POST /indoor/face/sample/update`

**成员列表：** `POST /indoor/face/sample/list`

### 5. 统计数据

**行为统计：**
- `queryCount` - 查询标签总次数（进入/离开）
- `dayDataChart` - 当日数据图（进入/离开）
- `weekDataChart` - 周数据图（进入/离开）

**存在统计：**
- `queryCount` - 查询最大人数/存在时长
- `dayDataChart` - 当日数据图（最大人数/存在时长）
- `weekDataChart` - 周数据图（最大人数/存在时长）

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
cd ~/.openclaw/workspace/jf-open-pro-ai-indoor-security/scripts

# 查询室内安防服务状态
python3 indoor_security.py --action status \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 2. 成员管理

```bash
# 新增成员
python3 member_manager.py --action add \
  --name "爸爸" --avatar "base64_image" --notice 1 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 查询成员列表
python3 member_manager.py --action list \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 删除成员
python3 member_manager.py --action delete --id 10 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 3. 查询异常告警

```bash
# 查询疑似陌生人告警
python3 alarm_query.py --action list \
  --msg-type "SuspectedStranger" \
  --start-time 1733241600 --end-time 1733846399 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"
```

### 4. 查询统计数据

```bash
# 查询进入次数
python3 stats_query.py --action behavior-count \
  --type "SomeoneEntered" \
  --start-time 1733241600 --end-time 1733327999 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 查询当日进入图表
python3 stats_query.py --action day-chart \
  --chart-type behavior \
  --type "SomeoneEntered" \
  --start-time 1733241600 --end-time 1733327999 \
  --sn "<your-device-sn>" \
  --user "<your-uuid>"

# 查询最大人数
python3 stats_query.py --action exist-count \
  --type "MaxPersonCount" \
  --start-time 1733241600 --end-time 1733327999 \
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
| 12504 | 授权失败 - 设备未开通套餐 | 登录开放平台为设备绑定室内安防套餐卡 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 错误码 12504 详细处理步骤

**错误信息：** `authorize failed,Please check it in the open platform`

**原因：** 设备未开通室内安防服务，或未绑定套餐卡

**解决步骤：**

1. 登录杰峰开放平台：https://developer.jftech.com
2. 进入 **套餐管理** / **服务管理**
3. 找到 **室内安防** 套餐
4. 为设备购买并绑定套餐卡
5. 等待配置生效（通常 1-5 分钟）
6. 重新调用 API 测试

## 注意事项

1. **时间戳** - 统计查询使用秒级时间戳
2. **套餐开通** - 使用前需确保设备已开通室内安防套餐
3. **Token 有效期** - authorization 需在有效期内
4. **签名算法** - 使用杰峰官方移位加密算法
5. **成员图片** - 新增成员时需要提供 base64 格式的图片

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/indoor_security.py` | 服务状态管理脚本 |
| `scripts/member_manager.py` | 成员管理脚本 |
| `scripts/alarm_query.py` | 告警查询脚本 |
| `scripts/stats_query.py` | 统计数据查询脚本 |
| `references/indoor-security-api.md` | API 参考文档 |

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
登录杰峰开放平台 → 个人中心/开发者信息 → 复制用户 UUID

### 2. JF_APP_KEY（jf_appKey）
登录杰峰开放平台 → 应用管理 → 我的应用 → 复制 appKey

### 3. JF_APP_SECRET（jf_secret）
登录杰峰开放平台 → 应用管理 → 应用详情 → 复制 secret 密钥

### 4. JF_MOVE_CARD（jf_moveCard）
通过 appKey 查询接口获取，或在开放平台应用详情页查看

### 5. JF_DEVICE_SN（jf_device_sn）
查看设备底部标签，或在开放平台设备管理中查看

### 6. JF_AUTHORIZATION（jf_authorization）⭐
- **使用杰峰用户系统**：参考用户登录接口获取 Authorization 值（JWT Token）
- **使用开发者自己的用户系统**：传值参考套餐卡使用中的 userId

### 7. JF_USER（jf_user）
与 JF_UUID 通常相同，或在开放平台个人中心查看

---

## 配置示例

```bash
export JF_UUID="your-uuid-here"
export JF_APP_KEY="your-appkey-here"
export JF_APP_SECRET="your-secret-here"
export JF_MOVE_CARD="your-movecard-here"
export JF_DEVICE_SN="your-device-sn-here"
export JF_AUTHORIZATION="your-authorization-token-here"
export JF_USER="your-user-id-here"
```

---

## 重要提醒

> **使用原则：** 后续所有 API 调用，必须严格使用用户环境变量中配置的参数值，**不允许**技能自己发散去获取或推算参数！
