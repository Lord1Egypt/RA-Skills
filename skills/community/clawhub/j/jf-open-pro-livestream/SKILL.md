---
name: jf-open-pro-livestream
description: 杰峰设备直播预览技能（开发版）。支持多端集成实时视频播放，兼容 HLS、RTSP、RTMP、FLV、MP4、WebRTC 等主流协议，适配 H.264/H.265 设备。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 直播预览
    - 实时视频
    - HLS
    - RTSP
    - RTMP
    - FLV
    - WebRTC
  triggers:
    - 获取直播地址
    - 直播预览
    - 实时播放
    - 视频流地址
    - 获取播放 URL
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
    - 低功耗设备需在 3 秒内播放
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-livestream - 杰峰设备直播预览技能（开发版）

## 技能描述

支持杰峰设备实时直播地址获取，适用于多端集成播放：

- **多协议支持** - HLS、RTSP、RTMP、FLV、MP4、WebRTC
- **多端适配** - Web、微信小程序、H5、第三方播放器
- **编码兼容** - H.264、H.265 视频编码
- **低时延** - WebRTC 低时延预览（仅 H.264）

**适用场景：**
- Web 页面嵌入实时监控
- 微信小程序视频播放
- 第三方播放器集成
- 移动端 APP 视频预览

## 触发词

- 获取直播地址 / 直播预览 / 实时播放
- 视频流地址 / 获取播放 URL / 直播流

## 前置条件

### 设备要求

1. **设备在线** - 设备需在线且可访问
2. **低功耗设备** - 获取 URL 后必须在 3 秒内播放
3. **编码配置** - H.265 设备建议使用特定协议

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
| `JF_DEVICE_PASSWORD` | 设备密码 | - | ❌ |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 获取直播地址 | `POST /gwp/v3/rtc/device/livestream/{token}` | POST | ✅ | ✅ |

## 支持的协议

### FLV 协议族

| 协议 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| FLV | `flv` | 标准 FLV 封装 | Web 端（H.264/H.265） |
| FLV 增强 | `flv-enhanced` | FLV-enhanced 封装 | VLC 4.0+、ffmpeg 6.1+ |
| WS-FLV | `ws-flv` | WebSocket FLV | Web 端低时延 |
| WS-FLV 增强 | `ws-flv-enhanced` | WebSocket FLV-enhanced | Web 端低时延 |
| WS 私有 | `ws-pri` | 杰峰私有协议 | 杰峰 WEB 播放器 |

### HLS 协议族

| 协议 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| HLS-TS | `hls-ts` | HLS+TS 切片 | iOS、Safari |
| HLS-FMP4 | `hls-fmp4` | HLS+fMP4 切片 | iOS、Safari |

### RTMP 协议族

| 协议 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| RTMP-FLV | `rtmp-flv` | RTMP+FLV | 微信小程序 |
| RTMP 增强 | `rtmp-enhanced` | RTMP+FLV-enhanced | 微信小程序 |

### RTSP 协议族

| 协议 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| RTSP-SDP | `rtsp-sdp` | RTSP 标准协议 | VLC、FFmpeg |
| RTSP 私有 | `rtsp-pri` | RTSP 私有协议 | 杰峰客户端 |

### MP4 协议

| 协议 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| MP4 | `mp4` | HTTP+MP4 | Chrome 23+ |

### WebRTC 协议

| 协议 | 值 | 说明 | 适用场景 |
|------|-----|------|----------|
| WebRTC | `webrtc` | WebRTC 协议 | **仅 H.264**，低时延 |

## 使用场景推荐

### 微信小程序

| 组件 | 支持协议 |
|------|----------|
| live-player | `http-flv`、`rtmp`、`hls` |

### H5 页面/Web 端

| 播放方式 | 支持协议 | 说明 |
|----------|----------|------|
| `<video>` 标签 | `hls`、`mp4` | 仅 H.264 |
| flv.js | `http-flv` | 需要 H.264 |
| WebRTC API | `webrtc` | **仅 H.264**，低时延 |
| 杰峰 WEB 播放器 | 全部 | 支持 H.264/H.265 |

### 第三方播放器

| 播放器 | 推荐协议 |
|--------|----------|
| VLC 4.0+ | `flv-enhanced`、`rtsp` |
| FFmpeg 6.1+ | `flv-enhanced`、`rtsp` |
| PotPlayer | `rtsp`、`rtmp` |

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

### 1. 获取 FLV 直播地址（Web 端推荐）

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-livestream/scripts

# 获取 FLV 地址（标清辅码流）
python3 livestream.py --action get-url --protocol flv

# 获取 FLV 地址（高清主码流）
python3 livestream.py --action get-url --protocol flv --stream 0
```

### 2. 获取 HLS 地址（iOS/小程序推荐）

```bash
# 获取 HLS-TS 地址
python3 livestream.py --action get-url --protocol hls-ts

# 获取 HLS-FMP4 地址
python3 livestream.py --action get-url --protocol hls-fmp4
```

### 3. 获取 RTMP 地址（微信小程序）

```bash
# 获取 RTMP-FLV 地址
python3 livestream.py --action get-url --protocol rtmp-flv
```

### 4. 获取 WebRTC 地址（低时延，仅 H.264）

```bash
# 获取 WebRTC 地址（仅支持 H.264 设备）
python3 livestream.py --action get-url --protocol webrtc
```

### 5. 获取 RTSP 地址（VLC/FFmpeg）

```bash
# 获取 RTSP 地址
python3 livestream.py --action get-url --protocol rtsp-sdp
```

### 6. 设置 URL 有效期

```bash
# 设置 24 小时有效期
python3 livestream.py --action get-url --protocol flv --expire-hours 24

# 设置 7 天有效期
python3 livestream.py --action get-url --protocol flv --expire-days 7
```

## 请求参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| channel | string | ✅ | `0` | 通道号（0=第一通道） |
| stream | string | ✅ | `1` | 码流（0=高清主码流，1=标清辅码流） |
| protocol | string | ✅ | - | 播放协议 |
| username | string | ✅ | `admin` | 设备登录用户名 |
| password | string | ❌ | `` | 设备登录密码 |
| expireTime | string | ❌ | 10 小时 | URL 有效期（毫秒时间戳） |

## 响应参数

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 平台状态码（2000=成功） |
| msg | string | 响应消息 |
| data | object | 响应数据 |
| ├─ Ret | int | 设备状态码（100=成功） |
| ├─ url | string | 播放地址 URL |
| └─ retMsg | string | 设备错误信息（失败时） |

## 状态码

### 平台状态码

| code | 说明 | 处理建议 |
|------|------|----------|
| 2000 | 成功 | - |
| 28007 | Header 参数错误 | 检查 uuid、appKey、timeMillis、signature |
| 40103 | 无效 Token | deviceToken 过期，重新获取 |
| 50000 | 服务器内部错误 | 联系杰峰技术支持 |

### 设备状态码（Ret）

| Ret | 说明 | 处理建议 |
|-----|------|----------|
| 100 | 成功 | - |
| 101 | 登录连接超时 | 检查设备是否在线 |
| 106 | 用户名或密码错误 | 检查设备凭证 |

## 注意事项

1. **URL 有效期** - 默认 10 小时，可自定义 30 秒 -720 天
2. **低功耗设备** - 获取 URL 后必须在 3 秒内播放
3. **设备休眠** - 低功耗设备需先唤醒再获取 URL
4. **编码格式** - WebRTC 仅支持 H.264 设备
5. **H.265 设备** - 建议使用 flv-enhanced 或 ws-flv-enhanced
6. **重复使用** - 有效期内 URL 可重复使用，减少起播时长
7. **单路限制** - 部分设备同时只支持一路直播流

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/livestream.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
