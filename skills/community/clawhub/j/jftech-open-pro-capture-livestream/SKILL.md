---
name: jf-open-pro-capture-livestream
description: 面向开发者杰峰设备 API 工具，支持批量获取杰峰设备实时画面，可多设备多通道抓图和直播地址获取。触发词：检查设备状态、查询设备、设备登录、设备抓图、直播地址、获取播放地址、批量抓图。

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
    - name: JF_USERNAME
      type: string
      description: 设备用户名
      default: admin
    - name: JF_PASSWORD
      type: string
      description: 设备密码
    - name: JF_SN
      type: string
      description: 设备序列号
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
  env_vars_only: true  # 仅支持环境变量
  language: python  # 仅支持 Python
---

# JF Open Pro Capture Livestream

> **面向开发者杰峰设备 API 工具 (Python)**
> 
> 支持批量获取杰峰设备实时画面，可多设备多通道抓图和直播地址获取。

---

## 🔒 安全说明

**仅支持环境变量存储凭据**

| 方式 | 支持 | 说明 |
|------|------|------|
| **环境变量** | ✅ 支持 | 不会在进程列表中暴露，不会执行本地代码 |
| **命令行参数** | ❌ 不支持 | 避免凭据泄露风险 |
| **配置文件** | ❌ 不支持 | 避免代码执行风险 |

---

## 🚀 快速开始

### 设置环境变量

```bash
export JF_UUID="your-uuid"              # 开放平台用户唯一标识
export JF_APPKEY="your-appkey"          # 开放平台应用 Key
export JF_APPSECRET="your-appsecret"    # 开放平台应用密钥
export JF_MOVECARD=5                    # 签名算法偏移量 (0-9)
export JF_SN="your-device-sn"           # 设备序列号
```

### 使用技能

```bash
# 查询设备状态
python scripts/jf_open_pro_capture_livestream.py status

# 设备登录
python scripts/jf_open_pro_capture_livestream.py login

# 云抓图
python scripts/jf_open_pro_capture_livestream.py capture

# 获取直播地址
python scripts/jf_open_pro_capture_livestream.py livestream

# 获取 Token
python scripts/jf_open_pro_capture_livestream.py token
```

---

## 📋 环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `JF_UUID` | 开放平台用户唯一标识 | 是 | - |
| `JF_APPKEY` | 开放平台应用 Key | 是 | - |
| `JF_APPSECRET` | 开放平台应用密钥 | 是 | - |
| `JF_MOVECARD` | 签名算法偏移量 (0-9) | 是 | - |
| `JF_SN` | 设备序列号 | 是 | - |
| `JF_USERNAME` | 设备用户名 | 否 | `admin` |
| `JF_PASSWORD` | 设备密码 | 否 | - |
| `JF_ENDPOINT` | API 端点 | 否 | `api.jftechws.com` |
| `JF_KEEPALIVE` | 保活时长（秒） | 否 | `300` |

---

## 🛠️ 功能

1. **获取设备 Token** - 通过设备序列号获取 24 小时有效的访问令牌
2. **设备登录认证** - 使用设备用户名/密码完成登录，获取 SessionID
3. **查询设备状态** - 获取设备在线状态、休眠状态、认证状态、IP 信息等
4. **设备云抓图** - 抓取设备实时图片（辅码流），图片地址有效期 24 小时
5. **获取直播地址** - 获取设备直播流地址（HLS/RTMP/FLV/WebRTC 等），默认有效期 10 小时

---

## 📖 详细文档

### 1. 获取设备 Token

**接口**: `POST /gwp/v3/rtc/device/token`

**响应**:
```json
{
  "code": 2000,
  "data": [{
    "sn": "YOUR_DEVICE_SN",
    "token": "ZTA3NTRiODMzNHw0OGRlOGMxYzFjMjBhNGEzfHwx..."
  }]
}
```

**注意**: Token 有效期 24 小时，可缓存复用。

---

### 2. 查询设备状态

**接口**: `POST /gwp/v3/rtc/device/status`

**状态判定表**:

| status | wakeUpStatus | wakeUpEnable | 设备状态 |
|--------|--------------|--------------|----------|
| online | 空 | 空 | 常电设备，在线 |
| online | 0 | 1 | 低功耗设备，已休眠 |
| online | 1 | 1 | 低功耗设备，已唤醒 |
| online | 2 | 1 | 低功耗设备，准备休眠中 |
| notfound | 空 | 空 | 设备不在线 |

---

### 3. 设备云抓图

**接口**: `POST /gwp/v3/rtc/device/capture/{deviceToken}`

**注意**:
- ⚠️ **按调用次数计费** - 详见官网定价
- ⚠️ **图片有效期 24 小时** - 过期自动清除，需及时下载

---

### 4. 获取直播地址

**接口**: `POST /gwp/v3/rtc/device/livestream/{deviceToken}`

**支持协议**:
| 协议 | 参数 | 适用场景 |
|------|------|----------|
| HLS | `hls-ts` | Web 浏览器、移动端（推荐） |
| FLV | `flv` | Web 播放器 |
| WebRTC | `webrtc` | 超低延迟（仅 H.264） |
| RTMP | `rtmp-flv` | 微信小程序 |

**注意**:
- ⚠️ **直播地址默认有效期 10 小时**
- ⚠️ **低功耗设备** - 获取后 3 秒内必须播放

---

## ⚠️ 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `2000` | 成功 | - |
| `4118` | 连接超时 | 设备离线/休眠，稍后重试 |
| `10001` | Token 无效 | 重新获取 Token |
| `10002` | 设备未登录 | 调用 login 接口登录 |

---

## 📚 官方参考资料

- **杰峰开放平台**: https://open.jftech.com/
- **API 文档**: https://docs.jftech.com/
- **API 端点**: `api.jftechws.com` (国际) / `api-cn.jftech.com` (中国大陆)
