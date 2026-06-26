---
name: jf-open-pro-device-human-detection
description: 杰峰设备人形检测技能（开发版）。支持人形检测开关设置、人形检测灵敏度设置、云台设备人形追踪开关设置等功能。
metadata:
  version: 1.0.0
  author: JFTech
  category: ai
  tags:
    - 杰峰
    - 人形检测
    - 人体追踪
    - 云台控制
    - AI 检测
    - 灵敏度设置
  triggers:
    - 查询人形检测配置
    - 设置人形检测开关
    - 开启人形检测
    - 关闭人形检测
    - 设置人形灵敏度
    - 查询人形追踪配置
    - 设置人形追踪开关
    - 开启人形追踪
    - 关闭人形追踪
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
    - 云台设备支持人形追踪功能
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-device-human-detection - 杰峰设备人形检测技能（开发版）

## 技能描述

支持杰峰设备的人形检测和追踪功能，基于杰峰开放平台 OpenAPI 实现：

- **人形检测开关设置** - 开启/关闭人形检测报警
- **人形检测灵敏度设置** - 调节检测灵敏度（低/中/高）
- **人形追踪开关设置** - 开启/关闭云台自动追踪人形
- **人形追踪灵敏度设置** - 调节追踪灵敏度
- **追踪返回时间设置** - 设置无人时返回守望位的时间

## 触发词

- 查询人形检测配置 / 设置人形检测开关 / 开启人形检测 / 关闭人形检测
- 设置人形灵敏度 / 查询人形追踪配置 / 设置人形追踪开关
- 开启人形追踪 / 关闭人形追踪 / 人形跟踪设置

## 前置条件

### 必需配置

1. **签名算法** - 使用杰峰官方移位加密算法生成 signature
2. **时间戳算法** - counter(7 位) + timeMillis(13 位)，实时生成
3. **设备绑定** - 设备需先绑定到开放平台账号
4. **云台设备** - 人形追踪功能需要云台设备支持

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
| 获取人形检测配置 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST | ✅ | ✅ |
| 设置人形检测配置 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST | ✅ | ✅ |
| 获取人形追踪配置 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST | ✅ | ✅ |
| 设置人形追踪配置 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST | ✅ | ✅ |

## 核心功能

### 1. 人形检测配置（Detect.HumanDetection）

**配置项说明：**

| 字段 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `Enable` | boolean | 人形检测开关 | `true`=开启，`false`=关闭 |
| `Sensitivity` | int | 检测灵敏度 | `0`=低，`1`=中，`2`=高，`3`=灵敏度数量 |
| `PedFdrAlg` | int | 人形人脸算法类型 | `0`=单人形，`1`=人形 + 人脸，`2`=人形 + 人脸识别，`3`=人形 + 车形，`4`=人形 + 车形 + 人脸，`5`=宠物 |
| `ObjectType` | int | 检测目标类型 | `0`=检测人，`1`=检测物体 |
| `ShowRule` | boolean | 是否叠加人形规则框 | `true`=是，`false`=否 |
| `ShowTrack` | boolean | 是否叠加移动人形框 | `true`=是，`false`=否 |
| `PushInterval` | int | 单人脸推图间隔（毫秒） | `-1`=不推图，其他=间隔时间 |

**警戒规则（PedRule）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `Enable` | boolean | 规则是否使能 |
| `RuleType` | int | 规则类型（0=警戒线，1=警戒区域） |
| `RuleRegion` | object | 警戒区域参数 |
| `RuleLine` | object | 警戒线参数 |

**警戒区域参数：**
- `PtsNum`: 区域点数（3-8）
- `AlarmDirect`: 检测方向（0=进入，1=离开，2=双向）
- `Pts`: 坐标点数组（0-8192）
- `Sensitivity`: 该区域灵敏度

### 2. 人形追踪配置（Detect.DetectTrack）

**配置项说明：**

| 字段 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `Enable` | int | 人形追踪开关 | `0`=关闭，`1`=开启 |
| `Sensitivity` | int | 追踪灵敏度 | `0`=低，`1`=中，`2`=高 |
| `ReturnTime` | int | 返回默认位置时间（秒） | `0`=不返回，`1-600`=指定时间 |

**注意：** 人形追踪不是报警，只是云台自动跟随人形移动。画面需要正放，识别出人形才能生效。

## 使用示例

### 环境准备

```bash
# 设置环境变量
export JF_UUID="uuidxxxx"
export JF_APP_KEY="appkeyxxxx"
export JF_APP_SECRET="appsecretxxxx"
export JF_MOVE_CARD=0
export JF_DEVICE_SN="snxxx1"
export JF_DEVICE_TOKEN="NTQ0NzQ3YmE3MXwyYzFk..."
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 查询人形检测配置

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-device-human-detection/scripts

python3 human_detection.py --action get-human-detect-config
```

### 2. 开启/关闭人形检测

```bash
# 开启人形检测
python3 human_detection.py --action set-human-detect-switch --enable true

# 关闭人形检测
python3 human_detection.py --action set-human-detect-switch --enable false
```

### 3. 设置人形检测灵敏度

```bash
# 设置低灵敏度
python3 human_detection.py --action set-human-detect-sensitivity --level 0

# 设置中灵敏度
python3 human_detection.py --action set-human-detect-sensitivity --level 1

# 设置高灵敏度
python3 human_detection.py --action set-human-detect-sensitivity --level 2
```

### 4. 查询人形追踪配置

```bash
python3 human_detection.py --action get-human-track-config
```

### 5. 开启/关闭人形追踪

```bash
# 开启人形追踪
python3 human_detection.py --action set-human-track-switch --enable true

# 关闭人形追踪
python3 human_detection.py --action set-human-track-switch --enable false
```

### 6. 设置人形追踪灵敏度

```bash
# 设置低灵敏度
python3 human_detection.py --action set-human-track-sensitivity --level 0

# 设置中灵敏度
python3 human_detection.py --action set-human-track-sensitivity --level 1

# 设置高灵敏度
python3 human_detection.py --action set-human-track-sensitivity --level 2
```

### 7. 设置追踪返回时间

```bash
# 设置 10 秒后返回
python3 human_detection.py --action set-track-return-time --seconds 10

# 设置不返回
python3 human_detection.py --action set-track-return-time --seconds 0

# 设置 5 分钟后返回（300 秒）
python3 human_detection.py --action set-track-return-time --seconds 300
```

## 灵敏度说明

### 人形检测灵敏度

| 级别 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| 低灵敏度 | 0 | 检测较宽松，误报少 | 人员流动频繁区域 |
| 中灵敏度 | 1 | 平衡检测和误报 | 一般区域（默认） |
| 高灵敏度 | 2 | 检测更敏感，易触发 | 重要安防区域 |

### 人形追踪灵敏度

| 级别 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| 低灵敏度 | 0 | 追踪较平缓 | 目标移动缓慢 |
| 中灵敏度 | 1 | 追踪速度适中 | 一般场景（默认） |
| 高灵敏度 | 2 | 追踪响应快 | 目标移动快速 |

## 人形人脸算法类型

| 类型 | 值 | 说明 |
|------|-----|------|
| 单人形检测 | 0 | 仅检测人形（默认） |
| 人形加人脸检测 | 1 | 检测人形并检测人脸 |
| 人形加人脸识别 | 2 | 检测人形并识别人脸身份 |
| 人形加车形检测 | 3 | 检测人形和车辆 |
| 人形加车形加人脸 | 4 | 检测人形、车形和人脸 |
| 宠物检测 | 5 | 检测宠物 |

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
| 106 | 用户名或密码错误 |

## 注意事项

1. **deviceToken 有效期** - 24 小时，过期需重新获取
2. **设备在线要求** - 配置类操作需要设备在线
3. **云台设备** - 人形追踪功能仅云台设备支持
4. **画面正放** - 人形追踪需要画面正放才能生效
5. **识别生效** - 需先识别出人形，追踪功能才能生效
6. **坐标范围** - 警戒区域坐标需缩放到 0-8192 范围
7. **北京时间** - 建议使用北京时间（UTC+8）进行时间查询
8. **算法创建** - 多通道设备可能部分通道不创建算法（AlgoCreate 字段）

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/human_detection.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
