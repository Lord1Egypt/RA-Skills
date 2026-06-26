---
name: jf-open-pro-video-masking
description: 杰峰设备视频遮挡技能（开发版）。支持一键遮蔽功能，开启后摄像头转至遮蔽位置并关闭视频预览和录像，保护隐私。
metadata:
  version: 1.0.0
  author: JFTech
  category: privacy
  tags:
    - 杰峰
    - 视频遮挡
    - 一键遮蔽
    - 隐私保护
    - 云台遮蔽
  triggers:
    - 开启遮蔽
    - 关闭遮蔽
    - 一键遮蔽
    - 视频遮挡
    - 隐私模式
  prerequisites:
    - 配置必需的环境变量
    - 设备需支持一键遮蔽功能
    - 设备需已完成配网和绑定
    - 设备需在线
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-video-masking - 杰峰设备视频遮挡技能（开发版）

## 技能描述

支持杰峰云台设备的一键遮蔽功能：

- **开启遮蔽** - 摄像头转至最下方然后转至最右侧，关闭视频预览和录像
- **关闭遮蔽** - 摄像头恢复到原监控位置，恢复正常预览和录像
- **状态查询** - 查询当前遮蔽状态

**适用场景：**
- 家庭隐私保护
- 会议室隐私模式
- 定时遮蔽计划

## 触发词

- 开启遮蔽 / 关闭遮蔽 / 一键遮蔽
- 视频遮挡 / 隐私模式 / 遮蔽模式

## 前置条件

### 硬件要求

1. **云台设备** - 设备需支持 PTZ 功能
2. **能力集验证** - `SystemFunction.SupportOneKeyMaskVideo` 为 `true`

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
| `JF_DEVICE_SN` | 设备序列号 | - | ✅ |
| `JF_DEVICE_TOKEN` | 设备接口访问令牌 | - | ✅ |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 设置视频遮挡 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST | ✅ | ✅ |

## 核心功能

### 一键遮蔽（OneKeyMaskVideo）

**API:** `POST /gwp/v3/rtc/device/setconfig/{deviceToken}`

**Name:** `OPPTZControl`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| Name | string | ✅ | 固定为 `OPPTZControl` |
| General.OneKeyMaskVideo | object[] | ✅ | 遮蔽配置数组 |
| └─ Enable | boolean | ✅ | `true`=开启遮蔽，`false`=关闭遮蔽 |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 平台状态码（2000=成功） |
| msg | string | 响应消息 |
| data | object | 响应数据 |
| ├─ Name | string | 方法名称 |
| ├─ Ret | int | 设备状态码（100=成功） |
| └─ SessionID | string | 会话 ID |

## 功能说明

### 开启遮蔽

当开启"一键遮蔽"后：

1. **摄像头动作** - 往下转至最下方，然后转至最右侧
2. **视频状态** - 关闭视频预览（无法查看实时画面）
3. **录像状态** - 停止录像（不录制任何内容）

**适用场景：**
- 家庭成员在家时保护隐私
- 会议室敏感会议期间
- 夜间不需要监控时

### 关闭遮蔽

当关闭"一键遮蔽"后：

1. **摄像头动作** - 自动恢复到原来的监控位置
2. **视频状态** - 恢复正常视频预览
3. **录像状态** - 恢复正常录像

**适用场景：**
- 家庭成员外出后恢复监控
- 会议结束后恢复监控
- 定时恢复监控计划

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

### 1. 开启遮蔽

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-video-masking/scripts

# 开启一键遮蔽
python3 video_masking.py --action enable
```

### 2. 关闭遮蔽

```bash
# 关闭一键遮蔽
python3 video_masking.py --action disable
```

### 3. 查询遮蔽状态

```bash
# 查询当前遮蔽状态
python3 video_masking.py --action status
```

### 4. 切换遮蔽状态

```bash
# 切换遮蔽状态（开→关 或 关→开）
python3 video_masking.py --action toggle
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

1. **设备要求** - 设备需支持一键遮蔽功能（检查能力集）
2. **deviceToken 有效期** - 24 小时，过期需重新获取
3. **设备在线要求** - 操作需要设备在线
4. **遮蔽位置** - 遮蔽时摄像头转到最下方和最右侧
5. **恢复位置** - 关闭遮蔽后自动恢复到原监控位置
6. **视频录像** - 遮蔽期间无法预览也不录像
7. **隐私保护** - 适用于家庭、会议室等隐私场景

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/video_masking.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
