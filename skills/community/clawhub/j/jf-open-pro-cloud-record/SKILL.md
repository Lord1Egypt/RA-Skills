---
name: jf-open-pro-cloud-record
description: 杰峰设备云存储技能（开发版）。支持云存视频列表查询、云存视频回放/下载、云存报警消息查询等功能。设备需开通云存储套餐。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 云存储
    - 云录像
    - 视频回放
    - 报警消息
  triggers:
    - 查询云存视频
    - 云存回放
    - 云录像下载
    - 云存报警
    - 云存消息列表
  prerequisites:
    - 配置必需的环境变量
    - 设备需开通云存储套餐
    - 设备需已完成配网和绑定
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-cloud-record - 杰峰设备云存储技能（开发版）

## 技能描述

支持杰峰设备云存储视频管理功能：

- **云存视频列表** - 查询指定时间段的云存视频列表
- **云存视频回放** - 获取云存视频回放地址（HLS 在线播放）
- **云存视频下载** - 获取云存视频下载地址（MP4 文件）
- **云存报警消息** - 查询云存报警消息列表

**⚠️ 前提条件：** 设备需开通云存储套餐

## 触发词

- 查询云存视频 / 云存回放 / 云录像下载
- 云存报警 / 云存消息列表 / 云存视频列表

## 前置条件

### 必需配置

1. **签名算法** - 使用杰峰官方移位加密算法生成 signature
2. **时间戳算法** - counter(7 位) + timeMillis(13 位)，实时生成
3. **云存储套餐** - 设备需开通云存储服务

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

| 功能 | 地址 | 方法 |
|------|------|------|
| 获取云存视频列表 | `POST /gwp/v3/rtc/device/getVideoList/{token}` | POST |
| 获取云存回放地址 | `POST /gwp/v3/rtc/device/getVideoUrl/{token}` | POST |
| 获取云存报警消息 | `POST /gwp/v3/rtc/device/getDeviceAlarmList/{token}` | POST |

## 核心功能

### 1. 云存视频列表（Video List）

**API:** `POST /gwp/v3/rtc/device/getVideoList/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| startTime | string | ✅ | 开始时间（yyyy-MM-dd HH:mm:ss） |
| stopTime | string | ✅ | 结束时间（yyyy-MM-dd HH:mm:ss） |
| sn | string | ✅ | 设备序列号 |
| channel | int | ❌ | 通道号（默认 0） |
| pageStart | int | ❌ | 起始页（默认 1） |
| pageSize | int | ❌ | 每页数量（1-200，默认 200） |
| events | string[] | ❌ | 报警类型过滤 |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| VideoArray | object[] | 视频列表 |
| ├─ StartTime | string | 录像开始时间 |
| ├─ StopTime | string | 录像结束时间 |
| ├─ IndexFile | string | 录像文件名（.m3u8） |
| ├─ PicFlag | int | 是否有缩略图（1=有，0=无） |
| ├─ VideoSize | int | 视频大小（字节） |
| ├─ thumbURL | string | 缩略图 URL |
| ├─ events | string[] | 报警类型 |
| └─ videoId | string | 视频 ID |

### 2. 云存视频回放/下载（Video URL）

**API:** `POST /gwp/v3/rtc/device/getVideoUrl/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| videoId | string | ❌ | 视频 ID（精准查询） |
| startTime | string | ❌ | 开始时间（条件查询） |
| stopTime | string | ❌ | 结束时间（条件查询） |
| channel | int | ❌ | 通道号（默认 0） |
| fileFormat | string | ❌ | 格式（`m3u8`=在线播放，`MP4`=下载） |
| multiVideo | string | ❌ | 多目设备标识（`1`=多目） |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| url | string | 视频地址（**有效期 24 小时**） |

### 3. 云存报警消息（Alarm List）

**API:** `POST /gwp/v3/rtc/device/getDeviceAlarmList/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| startTime | string | ✅ | 开始时间（yyyy-MM-dd HH:mm:ss） |
| endTime | string | ✅ | 结束时间（yyyy-MM-dd HH:mm:ss） |
| pageNum | int | ❌ | 页数（默认 1） |
| pageSize | int | ❌ | 每页数量（1-100，默认 10） |
| alarmEvent | string | ❌ | 报警类型 |

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

### 1. 查询云存视频列表

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-cloud-record/scripts

# 查询今天云存视频
python3 cloud_record.py --action get-video-list \
  --start "2026-05-07 00:00:00" \
  --stop "2026-05-07 23:59:59"

# 查询报警视频（人体检测）
python3 cloud_record.py --action get-video-list \
  --start "2026-05-07 00:00:00" \
  --stop "2026-05-07 23:59:59" \
  --event "HumanDetect"
```

### 2. 获取云存回放地址

```bash
# 获取回放地址（在线播放）
python3 cloud_record.py --action get-video-url \
  --video-id "videoIdxxxx" \
  --format m3u8

# 获取下载地址（MP4）
python3 cloud_record.py --action get-video-url \
  --video-id "videoIdxxxx" \
  --format MP4
```

### 3. 查询云存报警消息

```bash
# 查询今天报警消息
python3 cloud_record.py --action get-alarm-list \
  --start "2026-05-07 00:00:00" \
  --end "2026-05-07 23:59:59"

# 查询人体检测报警
python3 cloud_record.py --action get-alarm-list \
  --start "2026-05-07 00:00:00" \
  --end "2026-05-07 23:59:59" \
  --event "appEventHumanDetectAlarm"
```

## 报警类型参考

| 报警类型 | 说明 |
|----------|------|
| `HumanDetect` | 人形检测 |
| `VehicleDetect` | 车辆检测 |
| `PetDetect` | 宠物检测 |
| `MotionDetect` | 移动侦测 |
| `appEventHumanDetectAlarm` | 人体检测报警 |

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | deviceToken 过期，重新获取 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

## 注意事项

1. **云存储套餐** - 设备需开通云存储服务才能使用
2. **URL 有效期** - 回放/下载地址有效期**24 小时**
3. **流量计费** - MP4 下载按文件大小消耗流量计费
4. **分页限制** - 视频列表每页最大 200 条
5. **时间格式** - 所有时间参数使用 `yyyy-MM-dd HH:mm:ss` 格式

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/cloud_record.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
