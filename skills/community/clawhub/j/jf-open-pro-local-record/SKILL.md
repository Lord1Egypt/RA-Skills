---
name: jf-open-pro-local-record
description: 杰峰设备本地录像技能（开发版）。支持 TF 卡/硬盘存储设备的录像日历查询、回放列表、录像回放下载、本地报警图片获取、主辅码流切换等功能。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 本地录像
    - TF 卡录像
    - 硬盘录像
    - 录像回放
    - 录像下载
    - 报警图片
  triggers:
    - 查询录像日历
    - 查询录像列表
    - 录像回放
    - 下载录像
    - 获取报警图片
    - 切换码流
    - 本地录像
    - 卡存录像
  prerequisites:
    - 配置必需的环境变量
    - 设备需支持卡存录像（TF 卡或硬盘）
    - 设备需已完成配网和绑定
    - 设备需在线
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-local-record - 杰峰设备本地录像技能（开发版）

## 技能描述

支持杰峰设备本地录像管理功能，适用于搭载 TF 卡或硬盘存储的设备：

- **录像日历查询** - 查询指定月份哪些日期有录像
- **录像回放列表** - 获取指定时间段的录像文件列表
- **录像回放地址** - 获取 FLV/HLS/RTSP/MP4 回放地址
- **录像下载** - 获取 MP4 格式录像下载地址
- **本地报警图片** - 获取设备本地存储的报警图片
- **主辅码流切换** - 切换本地录像的主码流（高清）或辅码流（标清）

**适用场景：**
- 回看历史录像
- 下载重要录像片段
- 查看报警时的抓拍图片
- 调整录像存储质量（高清/标清）

## 触发词

- 查询录像日历 / 查询录像列表 / 录像回放
- 下载录像 / 获取报警图片 / 切换码流
- 本地录像 / 卡存录像 / TF 卡录像 / 硬盘录像

## 前置条件

### 硬件要求

1. **设备支持卡存录像** - 设备需有 TF 卡或硬盘存储
2. **录像已开启** - 设备已配置录像计划并正常录像

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
| `JF_DEVICE_USERNAME` | 设备用户名 | `admin` | ❌ |
| `JF_DEVICE_PASSWORD` | 设备密码 | - | ✅ |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 录像日历 | `POST /gwp/v3/rtc/device/cardPlaybackCalendar/{token}` | POST | ✅ | ✅ |
| 录像列表 | `POST /gwp/v3/rtc/device/opdev/{token}` | POST | ✅ | ✅ |
| 回放地址 | `POST /gwp/v3/rtc/device/playbackUrl/{token}` | POST | ✅ | ✅ |
| 报警图片 | `POST /gwp/v3/rtc/device/getDeviceLocalPic/{token}` | POST | ✅ | ✅ |
| 切换码流 | `POST /gwp/v3/rtc/device/cardVideoSwitchStream/{token}` | POST | ✅ | ✅ |

## 核心功能

### 1. 录像日历查询（CardPlaybackCalendar）

**API:** `POST /gwp/v3/rtc/device/cardPlaybackCalendar/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| Name | string | ✅ | 固定为 `OPSCalendar` |
| OPSCalendar.Event | string | ✅ | 录像类型（`*`=全部，`A`=外部报警，`M`=动检，`H`=手动等） |
| OPSCalendar.FileType | string | ✅ | 文件类型（`h264`=视频，`jpg`=图片） |
| OPSCalendar.Year | int | ✅ | 年份 |
| OPSCalendar.Month | int | ✅ | 月份（1-12） |
| OPSCalendar.Channel | int | ❌ | 通道号（默认 0） |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| CalendarList | object[] | 日历列表 |
| ├─ date | string | 日期（YYYY-MM-DD） |
| ├─ is_exist | int | 是否存在录像（0=不存在，1=存在） |

### 2. 录像回放列表（OPFileQuery）

**API:** `POST /gwp/v3/rtc/device/opdev/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| Name | string | ✅ | 固定为 `OPFileQuery` |
| OPFileQuery.BeginTime | string | ✅ | 开始时间（yyyy-MM-dd HH:mm:ss） |
| OPFileQuery.EndTime | string | ✅ | 结束时间（yyyy-MM-dd HH:mm:ss） |
| OPFileQuery.Channel | int | ✅ | 通道号（0=第一通道） |
| OPFileQuery.Event | string | ✅ | 录像类型（`*`=全部，`R`=常规，`A`=报警，`M`=动检，`H`=手动等） |
| OPFileQuery.StreamType | string | ✅ | 码流类型（`0x00000000`=主码流，`0x00000001`=辅码流） |
| OPFileQuery.Type | string | ✅ | 文件类型（`h264`=视频，`jpg`=图片） |
| OPFileQuery.DriverTypeMask | string | ✅ | 固定为 `0x0000FFFF` |

**录像类型说明：**
| 类型 | 代码 | 说明 |
|------|------|------|
| 全部 | `*` | 所有类型的录像 |
| 常规录像 | `R` | 没有报警时的录像（包含 AOV 录像） |
| 外部报警 | `A` | IO 口报警等非视频类报警 |
| 动态检测 | `M` | 移动侦测、人形检测等视频类报警 |
| 手动录像 | `H` | 手动开启的录像 |
| AOV 录像 | `V` | 低功耗全时录像 |
| 入侵 | `I` | 入侵检测录像 |
| 人脸 | `F` | 人脸识别录像 |
| 车牌 | `N` | 车牌识别录像 |
| 关键录像 | `K` | 关键录像 |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| OPFileQuery | object[] | 录像文件列表 |
| ├─ BeginTime | string | 开始时间 |
| ├─ EndTime | string | 结束时间 |
| ├─ FileName | string | 录像文件名 |
| ├─ FileLength | int | 文件大小（KB） |

### 3. 录像回放/下载地址（PlaybackUrl）

**API:** `POST /gwp/v3/rtc/device/playbackUrl/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| channel | int | ✅ | 通道号（0=第一通道） |
| streamType | int | ✅ | 码流类型（0=高清主码流，1=标清辅码流） |
| protocol | string | ✅ | 播放协议（`flv`/`hls-ts`/`hls-fmp4`/`mp4`/`rtsp-sdp`） |
| startTime | string | ✅ | 回放开始时间 |
| endTime | string | ✅ | 回放结束时间 |
| fileName | string | ✅ | 录像文件名（从回放列表获取） |
| username | string | ✅ | 设备登录用户名 |
| password | string | ✅ | 设备登录密码 |
| download | int | ❌ | 0=在线回放，1=录像下载（仅 protocol=mp4 时有效） |
| playPrioritize | int | ❌ | 回放优先级（0-2=普通，8=优先播放，9=持续播放） |

**协议说明：**
| 协议 | 值 | 说明 |
|------|-----|------|
| FLV | `flv` | 标准 FLV 封装（推荐用于 Web 播放） |
| FLV 增强 | `flv-enhanced` | FLV 增强封装（H.265 编码推荐） |
| HLS-TS | `hls-ts` | HLS 协议，TS 格式切片 |
| HLS-FMP4 | `hls-fmp4` | HLS 协议，FMP4 格式切片 |
| MP4 | `mp4` | HTTP 协议，MP4 格式（用于下载） |
| RTSP | `rtsp-sdp` | RTSP 标准协议 |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| url | string | 播放/下载地址（**有效期 10 小时**） |
| Ret | int | 设备响应状态码 |

**⚠️ 注意：**
- URL 有效期为 **10 小时**
- 同时只支持 **一路回放或下载**
- **本地录像回放和下载按照流量计费**

### 4. 本地报警图片（GetDeviceLocalPic）

**API:** `POST /gwp/v3/rtc/device/getDeviceLocalPic/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| startTime | string | ✅ | 开始时间 |
| endTime | string | ✅ | 结束时间 |
| fileName | string | ✅ | 图片文件名（从录像列表获取） |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| image | string | 图片地址 URL |

### 5. 切换主辅码流（CardVideoSwitchStream）

**API:** `POST /gwp/v3/rtc/device/cardVideoSwitchStream/{deviceToken}`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| stream | int | ✅ | 码流类型（0=高清主码流，1=标清辅码流） |

**说明：**
- 切换后新录制的视频将使用新码流
- 不影响已存储的录像文件

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
export JF_DEVICE_USERNAME="admin"
export JF_DEVICE_PASSWORD="xxxx"
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 查询录像日历

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-local-record/scripts

# 查询本月录像日历
python3 local_record.py --action get-calendar --year 2026 --month 5

# 查询指定月份
python3 local_record.py --action get-calendar --year 2026 --month 4
```

### 2. 查询录像列表

```bash
# 查询今天录像列表
python3 local_record.py --action get-record-list \
  --start "2026-05-07 00:00:00" \
  --end "2026-05-07 23:59:59"

# 查询报警录像
python3 local_record.py --action get-record-list \
  --start "2026-05-07 00:00:00" \
  --end "2026-05-07 23:59:59" \
  --event "AMRH"
```

### 3. 获取录像回放地址

```bash
# 获取 FLV 回放地址（Web 播放）
python3 local_record.py --action get-playback-url \
  --file-name "/idea0/2026-05-07/001/10.00.00-11.00.00[R][@12345][0].h264" \
  --start "2026-05-07 10:00:00" \
  --end "2026-05-07 11:00:00" \
  --protocol flv

# 获取 HLS 回放地址（移动端播放）
python3 local_record.py --action get-playback-url \
  --file-name "/idea0/2026-05-07/001/10.00.00-11.00.00[R][@12345][0].h264" \
  --start "2026-05-07 10:00:00" \
  --end "2026-05-07 11:00:00" \
  --protocol hls-ts
```

### 4. 下载录像

```bash
# 获取 MP4 下载地址
python3 local_record.py --action download-record \
  --file-name "/idea0/2026-05-07/001/10.00.00-11.00.00[R][@12345][0].h264" \
  --start "2026-05-07 10:00:00" \
  --end "2026-05-07 11:00:00"
```

### 5. 获取本地报警图片

```bash
# 获取报警图片地址
python3 local_record.py --action get-alarm-pic \
  --file-name "/idea1/2026-05-07/001/10.24.01-10.24.02[M][@48][0].jpg" \
  --start "2026-05-07 10:24:01" \
  --end "2026-05-07 10:24:02"
```

### 6. 切换主辅码流

```bash
# 切换到标清辅码流（节省存储空间）
python3 local_record.py --action switch-stream --stream 1

# 切换到高清主码流（更高画质）
python3 local_record.py --action switch-stream --stream 0

# 查询当前码流状态
python3 local_record.py --action get-stream-status
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
| 200 | 成功（图片接口） |

## 注意事项

1. **设备要求** - 设备需支持卡存录像（TF 卡或硬盘）
2. **deviceToken 有效期** - 24 小时，过期需重新获取
3. **设备在线要求** - 所有操作需要设备在线
4. **回放 URL 有效期** - 10 小时，请及时使用
5. **单路限制** - 同时只支持一路回放或下载
6. **流量计费** - 本地录像回放和下载按照流量计费
7. **时间格式** - 所有时间参数使用 `yyyy-MM-dd HH:mm:ss` 格式
8. **文件名获取** - 录像文件名需从回放列表接口获取

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/local_record.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
