---
name: jf-open-pro-capture
description: 杰峰设备批量抓图技能（开发版）。支持多设备同时抓图，自动管理 Token，可选下载图片到本地。按调用次数计费。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - 云抓图
    - 批量抓图
    - 设备抓图
    - 实时图片
    - 缩略图
  triggers:
    - 设备抓图
    - 批量抓图
    - 云抓图
    - 获取设备图片
    - 抓图下载
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
    - 按调用次数计费
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-capture - 杰峰设备批量抓图技能（开发版）

## 技能描述

支持杰峰设备云抓图功能，适用于单设备或多设备批量抓图：

- **批量抓图** - 支持多设备同时抓图
- **自动 Token 管理** - 自动获取和管理 deviceToken
- **本地下载** - 可选下载图片到本地存储
- **多通道支持** - 支持多通道设备抓图
- **图片类型** - 实时图/缩略图

**计费说明：** 按调用次数计费，详见 [杰峰官网 - 云抓拍定价](https://aops.jftech.com/#/pricing?lang=zh&tab=MEDIA_PROCESSING)

## 触发词

- 设备抓图 / 批量抓图 / 云抓图
- 获取设备图片 / 抓图下载 / 实时抓图

## 前置条件

### 设备要求

1. **设备在线** - 设备需在线且可访问
2. **设备绑定** - 设备需先绑定到开放平台账号
3. **辅码流** - 默认抓取辅码流（标清）
4. **主码流** - 需联系销售定制固件

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
| `JF_DEVICE_SN` | 设备序列号（单设备） | - | ❌ |
| `JF_DEVICE_TOKEN` | 设备接口访问令牌 | - | ❌ |
| `JF_DEVICE_USERNAME` | 设备用户名 | `admin` | ❌ |
| `JF_DEVICE_PASSWORD` | 设备密码 | - | ❌ |
| `JF_ENDPOINT` | API 接入地址 | `api-cn.jftechws.com` | ❌ |

## API 接口

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 设备抓图 | `POST /gwp/v3/rtc/device/capture/{token}` | POST | ✅ | ✅ |
| 获取设备 Token | `POST /gwp/v3/rtc/device/token` | POST | ✅ | ❌ |

## 核心功能

### 1. 设备抓图（Capture）

**API:** `POST /gwp/v3/rtc/device/capture/{deviceToken}`

**Name:** `OPSNAP`

**请求参数：**
| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| Name | string | ✅ | `OPSNAP` | 固定值 |
| OPSNAP.Channel | int | ❌ | `0` | 通道号（0=第一通道） |
| OPSNAP.PicType | int | ❌ | `0` | 图片类型（0=实时图，1=缩略图） |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 平台状态码（2000=成功） |
| msg | string | 响应消息 |
| data | object | 响应数据 |
| ├─ Ret | int | 设备状态码（100=成功） |
| └─ image | string | 图片地址 URL（**有效期 24 小时**） |

### 2. 获取设备 Token（批量抓图必需）

**API:** `POST /gwp/v3/rtc/device/token`

**请求参数：**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| sns | string[] | ✅ | 设备序列号列表（最多 500 个） |
| accessToken | string | ❌ | 用户 accessToken（可选） |

**响应参数：**
| 字段 | 类型 | 说明 |
|------|------|------|
| data | object[] | 设备 Token 列表 |
| ├─ sn | string | 设备序列号 |
| └─ token | string | 设备接口访问令牌（**有效期 24 小时**） |

## 使用示例

### 环境准备

```bash
# 设置环境变量（请替换为您的实际配置）
export JF_UUID="your-uuid"
export JF_APP_KEY="your-app-key"
export JF_APP_SECRET="your-app-secret"
export JF_MOVE_CARD="2"
export JF_DEVICE_SN="your-device-sn"
export JF_DEVICE_TOKEN="your-device-token"
export JF_DEVICE_USERNAME="admin"
export JF_DEVICE_PASSWORD="your-device-password"
export JF_ENDPOINT="api-cn.jftechws.com"
```

### 1. 单设备抓图（已有 Token）

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-capture/scripts

# 抓取实时图（辅码流）
python3 capture.py --action capture \
  --device-sn "your-device-sn" \
  --device-token "your-device-token"

# 抓取缩略图
python3 capture.py --action capture --pic-type 1 \
  --device-sn "your-device-sn" \
  --device-token "your-device-token"

# 抓取第二通道
python3 capture.py --action capture --channel 1 \
  --device-sn "your-device-sn" \
  --device-token "your-device-token"
```

### 2. 单设备抓图（自动获取 Token）

```bash
# 自动获取 Token 并抓图
python3 capture.py --action capture-auto \
  --device-sn "your-device-sn" \
  --password "your-device-password"
```

### 3. 批量设备抓图

```bash
# 批量抓图（从文件读取设备列表）
python3 capture.py --action batch-capture \
  --devices-file "devices.txt" \
  --password "your-device-password"

# 批量抓图并下载
python3 capture.py --action batch-capture \
  --devices-file "devices.txt" \
  --password "your-device-password" \
  --download --output-dir "./captures"
```

### 4. 抓图并下载

```bash
# 抓图并下载到当前目录
python3 capture.py --action capture \
  --device-sn "your-device-sn" \
  --device-token "your-device-token" \
  --download

# 抓图并下载到指定目录
python3 capture.py --action capture \
  --device-sn "your-device-sn" \
  --device-token "your-device-token" \
  --download --output-dir "./captures"
```

### 5. 多通道设备抓图

```bash
# 抓取第一通道
python3 capture.py --action capture --channel 0 \
  --device-sn "your-device-sn" \
  --device-token "your-device-token"

# 抓取第二通道
python3 capture.py --action capture --channel 1 \
  --device-sn "your-device-sn" \
  --device-token "your-device-token"
```

### 6. JSON 格式输出（适合程序调用）

```bash
# 单设备抓图 - JSON 格式
python3 capture.py --action capture-auto \
  --device-sn "your-device-sn" \
  --password "your-device-password" \
  --json

# 输出：{"url": "https://..."}

# 批量抓图 - JSON 格式
python3 capture.py --action batch-capture \
  --devices-file "devices.txt" \
  --password "your-device-password" \
  --json

# 输出：{"total":3,"success":3,"failed":0,"results":[...]}
```

## 设备列表文件格式

```
# devices.txt - 设备列表文件
# 格式：设备序列号，设备名称（可选）
your-device-sn-01，大门摄像头
your-device-sn-02，后院摄像头
your-device-sn-03，客厅摄像头
```

## 请求参数说明

### 图片类型（PicType）

| 值 | 类型 | 说明 |
|-----|------|------|
| `0` | 实时图 | 当前播放画面的截图（默认，辅码流） |
| `1` | 缩略图 | 缩略图（较小尺寸） |

### 通道号（Channel）

| 值 | 说明 |
|-----|------|
| `0` | 第一通道（默认） |
| `1` | 第二通道 |
| `2+` | 更多通道（NVR 设备） |

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
| 106 | 用户名或密码错误 | 检查设备凭证 |
| 503 | 设备离线 | 检查设备在线状态 |

## 注意事项

1. **图片有效期** - 抓图 URL 有效期**24 小时**，过期自动清除
2. **及时下载** - 建议及时下载到本地存储
3. **计费说明** - 按调用次数计费，详见官网定价
4. **默认辅码流** - 默认抓取辅码流（标清）
5. **主码流** - 需联系销售定制固件
6. **Token 有效期** - deviceToken 有效期 24 小时
7. **批量限制** - 单次最多 500 个设备
8. **设备在线** - 设备需在线才能抓图成功

## 相关文件

| 文件 | 说明 |
|------|------|
| `jf-open-pro-capture-skill.md` | 技能文档 |
| `scripts/capture.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://developer.jftech.com)
- [设备云抓图](/xm-workspace/xm-webs/openapi/设备云抓图.md)
- [获取设备接口访问令牌](/xm-workspace/xm-webs/openapi/smart-alarm/获取设备接口访问令牌.md)
- [杰峰云抓拍定价](https://aops.jftech.com/#/pricing?lang=zh&tab=MEDIA_PROCESSING)
- [签名算法](/xm-workspace/xm-webs/openapi/smart-alarm/签名算法.md)
- [时间戳算法](/xm-workspace/xm-webs/openapi/smart-alarm/时间戳算法.md)
