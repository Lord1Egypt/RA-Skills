---
name: jf-open-pro-video-record
description: 杰峰设备录像回放技能。支持获取设备云存储录像和设备本地录像回放地址，包括录像列表查询、回放地址获取、录像下载等功能。使用场景：云存回放、本地卡录像回放、录像下载、历史视频查看。

# 必需凭证声明 - 平台元数据
credentials:
  required:
    - name: JF_UUID
      type: string
      description: 杰峰开放平台用户唯一标识
      source: https://open.jftech.com/
    - name: JF_APPKEY
      type: string
      description: 杰峰开放平台应用 Key
      source: https://open.jftech.com/
    - name: JF_APPSECRET
      type: string
      description: 杰峰开放平台应用密钥
      source: https://open.jftech.com/
    - name: JF_MOVECARD
      type: integer
      description: 签名算法偏移量 (0-9)
      source: https://open.jftech.com/
  optional:
    - name: JF_SN
      type: string
      description: 设备序列号
    - name: JF_USERNAME
      type: string
      description: 设备登录用户名
      default: admin
    - name: JF_PASSWORD
      type: string
      description: 设备登录密码
    - name: JF_ENDPOINT
      type: string
      description: API 端点
      default: api.jftechws.com

# 网络端点声明
endpoints:
  - url: https://api.jftechws.com
    description: 杰峰官方 API (国际)
  - url: https://api-cn.jftech.com
    description: 杰峰官方 API (中国大陆)

# 安全声明
security:
  credentials_required: true
  env_vars_only: true
  language: python
  network_access:
    - api.jftechws.com
    - api-cn.jftech.com
  file_access: none
---

# JF Open Pro Video Record - 杰峰设备录像回放技能

> **面向开发者的杰峰设备录像回放工具 (Python)**
> 
> 支持设备云存储录像和设备本地录像回放地址获取，包括录像列表查询、回放地址获取、录像下载等功能。

---

## 🔒 安全说明

**凭据存储：仅支持环境变量**

| 方式 | 支持 | 说明 |
|------|------|------|
| **环境变量** | ✅ 支持 | 推荐方式，避免凭据出现在进程列表或日志中 |
| **命令行参数** | ❌ 不支持 | 避免凭据泄露风险 |
| **配置文件** | ❌ 不支持 | 避免明文存储凭据 |

**网络访问：**
- ✅ 仅访问杰峰官方 API 端点 (`api.jftechws.com` / `api-cn.jftech.com`)
- ❌ 不访问第三方服务
- ❌ 不读取敏感系统文件

---

## 🚀 快速开始

### 设置环境变量

```bash
# 开放平台凭证（必需）
export JF_UUID="your-uuid"              # 开放平台用户唯一标识
export JF_APPKEY="your-appkey"          # 开放平台应用 Key
export JF_APPSECRET="your-appsecret"    # 开放平台应用密钥
export JF_MOVECARD=5                    # 签名算法偏移量 (0-9)

# 设备信息
export JF_SN="your-device-sn"           # 设备序列号
export JF_USERNAME="admin"              # 设备登录用户名（可选，默认：admin）
export JF_PASSWORD="your-password"      # 设备登录密码（本地录像必需）
export JF_ENDPOINT="api.jftechws.com"   # API 端点（可选）
```

### 使用技能

```bash
# ========== 云存录像 ==========

# 获取云存视频列表（按时间范围查询）
python scripts/cloud_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00"

# 获取云存视频列表（带报警类型过滤）
python scripts/cloud_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00" --events "HumanDetect"

# 获取云存回放地址（按时间范围）
python scripts/cloud_playback_url.py --start-time "2026-04-07 15:23:26" --stop-time "2026-04-07 15:23:36"

# 获取云存回放地址（按视频 ID 精准查询）
python scripts/cloud_playback_url.py --video-id "xxxxxxxxxx"

# 获取云存回放地址（下载 MP4 格式）
python scripts/cloud_playback_url.py --start-time "2026-04-07 15:23:26" --stop-time "2026-04-07 15:23:36" --format MP4

# ========== 本地录像 ==========

# 获取本地录像回放列表
python scripts/local_video_list.py --start-time "2026-04-07 10:00:00" --stop-time "2026-04-07 18:00:00"

# 获取本地录像回放地址
python scripts/local_playback_url.py --file-name "/idea0/2026-04-07/001/15.23.26-15.23.36[R][@39733][2].h264" --start-time "2026-04-07 15:23:26" --stop-time "2026-04-07 15:23:36"

# 本地录像下载（MP4 格式）
python scripts/local_playback_url.py --file-name "xxx.h264" --start-time "2026-04-07 15:23:26" --stop-time "2026-04-07 15:23:36" --download
```

---

## 📋 环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `JF_UUID` | 开放平台用户唯一标识 | 是 | - |
| `JF_APPKEY` | 开放平台应用 Key | 是 | - |
| `JF_APPSECRET` | 开放平台应用密钥 | 是 | - |
| `JF_MOVECARD` | 签名算法偏移量 (0-9) | 是 | - |
| `JF_SN` | 设备序列号 | 云存必需 | - |
| `JF_USERNAME` | 设备登录用户名 | 本地录像必需 | `admin` |
| `JF_PASSWORD` | 设备登录密码 | 本地录像必需 | - |
| `JF_ENDPOINT` | API 端点 | 否 | `api.jftechws.com` |

---

## 🛠️ 功能

### 1. 云存录像

#### 1.1 获取云存视频列表

查询设备在指定时间段内的云存视频列表。

**支持场景：**
- 条件查询（时间范围）
- 组合条件查询（分页 + 报警类型过滤）

**支持的报警类型：**
- `HumanDetect` - 人形检测
- `MotionDetect` - 移动侦测
- `appEventHumanDetectAlarm` - 人形报警
- 更多类型参考 [报警消息类型](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=ba50abdc08e84216bf8e3d3742df8922&lang=zh)

**使用示例：**

```bash
# 按时间范围查询
python scripts/cloud_video_list.py \
  --start-time "2026-04-07 10:00:00" \
  --stop-time "2026-04-07 18:00:00"

# 带报警类型过滤
python scripts/cloud_video_list.py \
  --start-time "2026-04-07 10:00:00" \
  --stop-time "2026-04-07 18:00:00" \
  --events "HumanDetect"

# 分页查询
python scripts/cloud_video_list.py \
  --start-time "2026-04-07 10:00:00" \
  --stop-time "2026-04-07 18:00:00" \
  --page-start 1 \
  --page-size 50
```

**返回字段：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `StartTime` | 录像开始时间 | `2026-04-07 13:12:34` |
| `StopTime` | 录像结束时间 | `2026-04-07 13:12:51` |
| `IndexFile` | 录像文件名 | `xxx.m3u8` |
| `PicFlag` | 是否有缩略图 (1=有，0=无) | `1` |
| `VideoSize` | 视频大小（字节） | `339014` |
| `thumbURL` | 缩略图 URL | `http://...` |
| `events` | 报警类型列表 | `["HumanDetect"]` |
| `videoId` | 视频 ID（精准查询用） | `0...9a...z` |

#### 1.2 获取云存回放地址

获取云存视频回放或下载地址，支持 HLS 在线播放和 MP4 下载。

**支持模式：**
- 精准查询：根据视频 ID 查询
- 条件查询：根据时间范围查询

**使用示例：**

```bash
# 按时间范围获取回放地址（HLS 在线播放）
python scripts/cloud_playback_url.py \
  --start-time "2026-04-07 15:23:26" \
  --stop-time "2026-04-07 15:23:36"

# 按视频 ID 精准查询
python scripts/cloud_playback_url.py \
  --video-id "xxxxxxxxxx"

# 获取下载链接（MP4 格式）
python scripts/cloud_playback_url.py \
  --start-time "2026-04-07 15:23:26" \
  --stop-time "2026-04-07 15:23:36" \
  --format MP4

# 多目设备（多镜头摄像头）
python scripts/cloud_playback_url.py \
  --start-time "2026-04-07 15:23:26" \
  --stop-time "2026-04-07 15:23:36" \
  --multi-video
```

**播放方式：**

```bash
# VLC 播放
vlc "https://xxx.com/xxx.m3u8?Expires=..."

# 网页播放（HLS.js）
<video src="https://xxx.com/xxx.m3u8?Expires=..." controls></video>

# 下载 MP4
curl -o video.mp4 "https://xxx.com/xxx.mp4?Expires=..."
# 或
ffmpeg -i "https://xxx.com/xxx.mp4?Expires=..." -c copy video.mp4
```

**注意事项：**
- 回放地址有效期：**24 小时**
- MP4 下载按**文件大小流量计费**
- 多目设备返回多个地址，以分号 `;` 分隔

---

### 2. 本地录像（TF 卡/硬盘）

#### 2.1 获取本地录像回放列表

查询设备本地存储（TF 卡或硬盘）中的录像文件列表。

**前置条件：**
- 设备支持卡存录像（有 TF 卡或硬盘）
- 需配置设备登录凭据（`JF_USERNAME`、`JF_PASSWORD`）

**录像类型说明：**

| 类型 | 说明 |
|------|------|
| `*` | 所有类型的录像 |
| `R` | 常规录像（无报警时的连续录像，含 AOV 录像） |
| `A` | 非视频类报警（如 IO 口报警） |
| `M` | 视频类报警（移动侦测、人形检测等） |
| `H` | 手动录像 |
| `C` | 卡号录像 |
| `V` | AOV 录像（低功耗全时录像） |
| `I` | 入侵报警 |
| `S` | 盗移/滞留报警 |
| `F` | 人脸识别录像 |
| `N` | 车牌识别录像 |
| `K` | 关键录像 |

**使用示例：**

```bash
# 查询所有类型录像
python scripts/local_video_list.py \
  --start-time "2026-04-07 10:00:00" \
  --stop-time "2026-04-07 18:00:00"

# 只查询报警录像（移动侦测 + 人形检测 + 常规）
python scripts/local_video_list.py \
  --start-time "2026-04-07 10:00:00" \
  --stop-time "2026-04-07 18:00:00" \
  --event "AMRH"

# 只查询常规录像
python scripts/local_video_list.py \
  --start-time "2026-04-07 10:00:00" \
  --stop-time "2026-04-07 18:00:00" \
  --event "R"
```

**返回字段：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `BeginTime` | 录像开始时间 | `2026-04-07 20:00:00` |
| `EndTime` | 录像结束时间 | `2026-04-07 21:00:00` |
| `FileName` | 录像文件路径 | `/idea0/2026-04-07/002/20.00.00-21.00.00[R][@2dcc5][0].h264` |
| `FileLength` | 文件大小（KB） | `123456` |

#### 2.2 获取本地录像回放地址

获取本地录像文件的回放或下载地址。

**支持的协议格式：**

| 协议 | 格式 | 说明 |
|------|------|------|
| `flv` | FLV | 标准 FLV 封装（H.265 采用国内行业 FLV 标准） |
| `flv-enhanced` | FLV-Enhanced | H.265 标准 FLV-Enhanced 封装 |
| `hls-ts` | HLS-TS | HLS 协议，TS 格式切片 |
| `hls-fmp4` | HLS-fMP4 | HLS 协议，fMP4 格式切片 |
| `mp4` | MP4 | HTTP 协议，MP4 格式（用于下载） |
| `rtsp-sdp` | RTSP-SDP | RTSP 标准协议（默认） |
| `rtsp-pri` | RTSP-PRI | RTSP 私有协议 |

**使用示例：**

```bash
# 在线播放（FLV 格式）
python scripts/local_playback_url.py \
  --file-name "/idea0/2026-04-07/001/15.23.26-15.23.36[R][@39733][2].h264" \
  --start-time "2026-04-07 15:23:26" \
  --stop-time "2026-04-07 15:23:36" \
  --protocol flv

# HLS 播放
python scripts/local_playback_url.py \
  --file-name "xxx.h264" \
  --start-time "2026-04-07 15:23:26" \
  --stop-time "2026-04-07 15:23:36" \
  --protocol hls-ts

# 录像下载（MP4 格式）
python scripts/local_playback_url.py \
  --file-name "xxx.h264" \
  --start-time "2026-04-07 15:23:26" \
  --stop-time "2026-04-07 15:23:36" \
  --protocol mp4 \
  --download

# 指定码流类型（0=主码流/高清，1=辅码流/标清）
python scripts/local_playback_url.py \
  --file-name "xxx.h264" \
  --start-time "2026-04-07 15:23:26" \
  --stop-time "2026-04-07 15:23:36" \
  --stream-type 0
```

**注意事项：**
- 回放地址有效期：**10 小时**
- 同时只支持**一路回放或下载**
- 本地录像回放和下载**按流量计费**
- 必须先获取录像文件列表，使用返回的 `FileName` 字段

---

## ⚠️ 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `2000` | 成功 | - |
| `12504` | 授权失败 - 设备未开通服务 | 登录开放平台为设备绑定对应套餐 |
| `10001` | 参数错误 | 检查请求参数格式 |
| `10002` | 签名失败 | 检查 appKey/appSecret 和时间戳 |
| `200` | 设备响应成功 | - |
| `401` | 设备认证失败 | 检查设备用户名/密码 |

### 常见错误

**1. 云存服务未开通**
```
code: 12504
msg: authorize failed, Please check it in the open platform
```
→ 登录杰峰开放平台，为设备购买并绑定云存套餐卡

**2. 本地录像文件不存在**
```
Ret: 404
msg: File not found
```
→ 检查文件名是否正确，确认设备 TF 卡/硬盘中有录像

**3. 设备登录失败**
```
Ret: 401
msg: Authentication failed
```
→ 检查 `JF_USERNAME` 和 `JF_PASSWORD` 是否正确

---

## 📚 官方参考资料

- **杰峰开放平台**: https://open.jftech.com/
- **API 文档**: https://docs.jftech.com/
- **云存视频列表**: https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=66142b2ca13c418d84085772a627d650
- **云存回放地址**: https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672
- **本地录像列表**: https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=4b1516da5763439a9bc7175d7ac7d246
- **本地录像回放**: https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=4b1516da5763439a9bc7175d7ac7d246
- **API 端点**: `api.jftechws.com` (国际) / `api-cn.jftech.com` (中国大陆)

---

## 📁 脚本工具

**云存录像脚本：**

| 脚本 | 功能 |
|------|------|
| `cloud_video_list.py` | 获取云存视频列表 |
| `cloud_playback_url.py` | 获取云存回放地址 |

**本地录像脚本：**

| 脚本 | 功能 |
|------|------|
| `local_video_list.py` | 获取本地录像回放列表 |
| `local_playback_url.py` | 获取本地录像回放地址 |

```bash
# 获取帮助
python scripts/cloud_video_list.py --help
python scripts/cloud_playback_url.py --help
python scripts/local_video_list.py --help
python scripts/local_playback_url.py --help
```

---

**技能版本：** v1.0.1  
**语言：** Python  
**最后更新：** 2026-04-08
