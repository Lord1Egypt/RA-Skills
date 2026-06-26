---
name: jf-open-pro-ai-pet-care
description: 杰峰开放平台宠物看护技能。化身全天候"宠物保姆"，提供异常情况通知、详尽的宠物行为报告和云端视频存档，给宠物最安心的守护。
---

# JF Tech Pro AI 宠物看护技能

**目标用户：** 开发者 / 集成工程师

化身全天候的"宠物保姆"，提供异常情况通知、详尽的宠物行为报告和云端视频存档，给宠物最安心的守护。

本技能提供 JF Tech 宠物看护功能的完整开发支持，包括脚本工具、API 参考和集成示例。

## 功能列表

| 功能模块 | 说明 |
|----------|------|
| 设备支持查询 | 查询设备是否支持宠物看护功能 |
| 套餐开通查询 | 查询套餐是否开通，未开通时引导绑定套餐卡 |
| 服务状态管理 | 开启/关闭宠物看护服务 |
| 宠物管理 | 新增、删除、修改、查询宠物列表 |
| 异常告警查询 | 查询异常告警列表（卡粮、食量异常、等待投喂、宠物久未出现） |
| 统计数据查询 | 查询宠物行为次数、时间、当日/一周数据图表 |

## 目标用户

**本技能面向开发者使用**，适用于以下场景：

- **应用集成** - 在你的应用中集成 JF Tech 宠物看护功能
- **自动化脚本** - 编写宠物监控、告警通知的自动化流程
- **二次开发** - 基于 JF Tech API 构建定制化宠物看护功能
- **调试测试** - 快速测试 API 功能和验证集成

> ⚠️ **非开发者用户**：如果你只是想使用宠物看护功能，建议使用现成的客户端应用或联系系统管理员。

## 触发场景

开发者使用此技能当需要：
- **集成宠物看护功能** - 在应用中添加宠物监控和告警
- **管理宠物信息** - 添加、编辑、删除宠物档案
- **查询异常告警** - 获取卡粮、食量异常等告警记录
- **生成行为报告** - 统计宠物吃喝、走动、躺着等行为数据
- **调试 API 问题** - 测试认证、签名、请求格式

## 支持平台

| 平台 | 状态 | 说明 |
|------|------|------|
| JF Tech (杰峰) | ✅ 已实现 | 完整支持宠物看护 API |

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

### 开发环境要求

- Python 3.6+
- 网络连接（访问 JF Tech API）
- JF Tech 开放平台账号

### 获取 API 凭证

1. **注册开放平台**：https://developer.jftech.com
2. **创建应用**：获取 `appKey` 和 `secret`
3. **获取用户 Token**：调用登录 API 或使用管理后台
4. **绑定设备**：确保设备已开通宠物看护套餐

### JF Tech 凭证清单

| 凭证 | 配置项 | 说明 | 获取方式 |
|------|--------|------|----------|
| `uuid` | `jf_uuid` | 开放平台用户 uuid（必填） | 用户中心查看 |
| `appKey` | `jf_appKey` | 应用 appKey | 应用管理后台 |
| `secret` | `jf_secret` | 应用密钥 | 应用管理后台 |
| `moveCard` | `jf_moveCard` | 移动卡标识 | 应用管理后台 |
| `authorization` | `jf_authorization` | 用户登录 token (JWT) | 登录 API 获取 |
| `user` | `jf_user` | 用户 ID | 自定义或管理后台 |
| `sn` | `jf_device_sn` | 设备序列号 | 设备标签或管理后台 |

### 凭证管理建议

**开发环境：** 使用环境变量
```bash
export JFTECH_UUID="your-uuid"
export JFTECH_APPKEY="your-appkey"
export JFTECH_SECRET="your-secret"
export JFTECH_AUTH="your-token"
export JFTECH_USER="your-user-id"
export JFTECH_SN="your-device-sn"
```

**生产环境：** 使用配置中心或密钥管理服务

**本地测试：** 存入 `TOOLS.md`（仅限开发机）

```markdown
### 杰峰开放平台配置（个人版）

| 参数 | 配置项 | 说明 |
|------|------|------|
| `jf_uuid` | `<your-uuid>` | 开放平台用户 uuid（必填） |
| `jf_appKey` | `<your-appkey>` | 应用 appKey |
| `jf_secret` | `<your-secret>` | 应用密钥 |
| `jf_moveCard` | `7` | 移动卡标识 |
| `jf_authorization` | *(空)* | 用户 token (JWT) |
| `jf_user` | `<your-uuid>` | 用户 ID |
| `jf_device_sn` | `<your-device-sn>` | 设备序列号 |
```

## 使用方式

### 方式一：使用 Python 脚本（推荐）

```bash
# 查询宠物看护服务状态
python ~/.openclaw/workspace/skills/jf-open-pro-ai-pet-care/scripts/pet_care.py \
  --action status \
  --uuid <uuid> \
  --appkey <appKey> \
  --secret <secret> \
  --auth <authorization> \
  --user <user> \
  --sn <设备序列号>

# 开启/关闭宠物看护
python ~/.openclaw/workspace/skills/jf-open-pro-ai-pet-care/scripts/pet_care.py \
  --action switch \
  --enable true \
  --uuid <uuid> \
  --appkey <appKey> \
  --secret <secret> \
  --auth <authorization> \
  --user <user> \
  --sn <设备序列号>

# 宠物管理 - 新增宠物
python ~/.openclaw/workspace/skills/jf-open-pro-ai-pet-care/scripts/pet_manage.py \
  --action add \
  --name "咪咪" \
  --type "银渐层" \
  --image <base64 图片> \
  --uuid <uuid> \
  --appkey <appKey> \
  --secret <secret> \
  --auth <authorization> \
  --user <user> \
  --sn <设备序列号>

# 查询异常告警列表
python ~/.openclaw/workspace/skills/jf-open-pro-ai-pet-care/scripts/alarm_query.py \
  --start-time 1726033162 \
  --end-time 1726070399 \
  --uuid <uuid> \
  --appkey <appKey> \
  --secret <secret> \
  --auth <authorization> \
  --user <user> \
  --sn <设备序列号>

# 查询统计数据
python ~/.openclaw/workspace/skills/jf-open-pro-ai-pet-care/scripts/stats_query.py \
  --action count \
  --type eating \
  --start-time 1726033162 \
  --end-time 1726070399 \
  --uuid <uuid> \
  --appkey <appKey> \
  --secret <secret> \
  --auth <authorization> \
  --user <user> \
  --sn <设备序列号>
```

### 方式二：直接调用 API

参考 `references/pet-care-api.md` 获取完整 API 文档。

## 工作流程

```
1. 获取凭证 → 2. 生成签名 → 3. 调用宠物看护 API
                                  ↓
4. 返回结果 ← 3. 解析响应 ← 2. 发送请求
   ↓
5. 格式化输出（状态/告警/统计数据）
```

### 详细步骤

1. **获取凭证** - 从用户或 TOOLS.md 获取 API 凭证
2. **生成签名** - 使用 JF Tech 签名算法生成请求签名
3. **调用 API** - 根据功能调用对应的宠物看护 API
4. **解析结果** - 返回服务状态、宠物列表、告警记录或统计数据
5. **返回结果** - 格式化输出结果信息

## 异常类型说明

| 异常类型 | 枚举值 | 说明 |
|----------|--------|------|
| 卡粮 | `GrainBloack` | 粮仓堵塞，宠物无法进食 |
| 食量异常 | `PetAppetiteAbnormal` | 宠物食量突然增加或减少 |
| 等待投喂 | `WaitFeeding` | 宠物等待投喂提醒 |
| 宠物久未出现 | `PetAbsent` | 宠物长时间未出现在摄像头前 |

## 宠物行为类型

| 行为类型 | 枚举值 | 说明 |
|----------|--------|------|
| 吃喝 | `eating` | 宠物进食或饮水行为 |
| 走动 | `walking` | 宠物活动走动行为 |
| 躺着 | `lying` | 宠物休息躺着行为 |

## 错误处理

### JF Tech 常见错误码

| 状态码 | 说明 | 解决方案 |
|--------|------|----------|
| 2000 | 成功 | ✅ |
| 12504 | 授权失败 - 设备未开通宠物看护套餐 | 登录开放平台为设备绑定宠物看护套餐卡 |
| 10001 | 参数错误 | 检查请求参数格式 |
| 10002 | 签名失败 | 检查 appKey/secret 和时间戳 |

### 错误码 12504 详细处理步骤

**错误信息：** `authorize failed,Please check it in the open platform`

**原因：** 设备未开通宠物看护服务，或未绑定套餐卡

**解决步骤：**

1. 登录杰峰开放平台：https://developer.jftech.com
2. 进入 **套餐管理** / **服务管理**
3. 找到 **宠物看护** 套餐
4. 为设备购买并绑定套餐卡
5. 等待配置生效（通常 1-5 分钟）
6. 重新调用 API 测试

## 配置存储

将常用设备信息存入 `TOOLS.md`：

```markdown
### 宠物看护设备

- camera-pet-feeder: sn=xxx, user=xxx, pet_name=咪咪
```

---

## 开发者集成指南

### 脚本复用

本技能提供的 Python 脚本可直接集成到你的项目中：

```python
# 导入脚本中的函数
import sys
sys.path.insert(0, "/root/.openclaw/workspace/skills/jf-open-pro-ai-pet-care/scripts")
from pet_care import get_switch_status, set_switch
from pet_manage import add_pet, delete_pet, update_pet, list_pets
from alarm_query import query_alarms
from stats_query import query_count, query_time, query_day_chart, query_week_chart

# 查询服务状态
status = get_switch_status(
    sn="48de8c1c1c20a4a3",
    user="admin",
    uuid="your-uuid",
    appkey="your-appkey",
    secret="your-secret",
    authorization="your-token"
)
print(f"宠物看护服务：{'已开启' if status else '已关闭'}")

# 新增宠物
result = add_pet(
    sn="48de8c1c1c20a4a3",
    user="admin",
    name="咪咪",
    pet_type="银渐层",
    images=["base64_image_1", "base64_image_2"],
    uuid="your-uuid",
    appkey="your-appkey",
    secret="your-secret",
    authorization="your-token"
)

# 查询异常告警
alarms = query_alarms(
    sn="48de8c1c1c20a4a3",
    user="admin",
    start_time=1726033162,
    end_time=1726070399,
    uuid="your-uuid",
    appkey="your-appkey",
    secret="your-secret",
    authorization="your-token"
)
```

### API 直接调用

参考 `references/pet-care-api.md` 中的签名算法和请求格式，使用你熟悉的 HTTP 客户端库直接调用 API。

### 在 OpenClaw 中扩展

如果你使用 OpenClaw，可以将此技能作为模板，创建自定义的宠物看护技能。

## 相关技能

- `jf-open-pro-ai-smart-search` - JF Tech AI 智搜技能
- `jf-open-capture-livestream` - JF 设备状态查询、云抓图、直播地址
- `jf-open-ptz-control` - JF 云台控制

## 参考资料

- `references/pet-care-api.md` - JF Tech 宠物看护 API 完整文档

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
