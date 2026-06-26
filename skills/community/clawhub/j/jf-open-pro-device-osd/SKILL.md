---
name: jf-open-pro-device-osd
description: 杰峰设备 OSD 水印设置技能（开发版）。支持设备实时画面水印设置，可配置通道标题、时间标题、隐私区域等 OSD 叠加属性。
metadata:
  version: 1.0.0
  author: JFTech
  category: video
  tags:
    - 杰峰
    - OSD 水印
    - 通道标题
    - 时间标题
    - 隐私区域
    - 视频叠加
  triggers:
    - 设置 OSD 水印
    - 查询 OSD 配置
    - 通道标题设置
    - 时间标题设置
    - 隐私区域
    - 视频水印
  prerequisites:
    - 配置必需的环境变量
    - 设备需已完成配网和绑定
    - 设备需在线
  region:
    - CN: api-cn.jftechws.com (中国大陆)
    - AS: api-as.jftechws.com (亚洲)
    - EU: api-eu.jftechws.com (欧洲)
    - NA: api-na.jftechws.com (北美洲)
---

# jf-open-pro-device-osd - 杰峰设备 OSD 水印设置技能（开发版）

## 技能描述

支持杰峰设备 OSD（On-Screen Display）水印配置功能：

- **单行 OSD 配置** - 获取/设置单行 OSD 叠加配置
- **多行 OSD 配置** - 获取/设置多行 OSD 叠加配置
- **通道标题** - 设置通道名称显示
- **时间标题** - 设置时间戳显示属性和位置
- **隐私区域** - 设置画面隐私遮挡区域

## 触发词

- 设置 OSD 水印 / 查询 OSD 配置
- 通道标题设置 / 时间标题设置
- 隐私区域 / 视频水印

## 前置条件

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

| 功能 | 地址 | 方法 |
|------|------|------|
| 获取单行 OSD 配置 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST |
| 设置单行 OSD 配置 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST |
| 获取多行 OSD 配置 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST |
| 设置多行 OSD 配置 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST |

## 核心功能

### 1. 单行 OSD 配置（AVEnc.VideoWidget）

**API:** `POST /gwp/v3/rtc/device/getconfig/{token}` / `setconfig/{token}`

**Name:** `AVEnc.VideoWidget`

**配置项：**
| 字段 | 类型 | 说明 |
|------|------|------|
| ChannelTitle | object | 通道标题配置 |
| ├─ Name | string | 通道名称 |
| ├─ SerialNo | string | 设备序列号 |
| ChannelTitleAttribute | object | 通道标题属性 |
| ├─ BackColor | string | 背景色（RGBA） |
| ├─ FrontColor | string | 前景色（RGBA） |
| ├─ EncodeBlend | bool | 编码叠加使能 |
| ├─ PreviewBlend | bool | 预览叠加使能 |
| ├─ RelativePos | int[] | 相对位置坐标 [x1,y1,x2,y2] |
| TimeTitleAttribute | object | 时间标题属性 |
| ├─ BackColor | string | 背景色 |
| ├─ FrontColor | string | 前景色 |
| ├─ EncodeBlend | bool | 编码叠加使能 |
| ├─ PreviewBlend | bool | 预览叠加使能 |
| ├─ RelativePos | int[] | 相对位置坐标 |
| Covers | object[] | 隐私区域配置 |
| CoversNum | int | 隐私区域个数 |

### 2. 多行 OSD 配置

**API:** `POST /gwp/v3/rtc/device/getconfig/{token}` / `setconfig/{token}`

**Name:** `AVEnc.VideoOSD`

**配置项：** 支持多行文本叠加配置

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

### 1. 查询单行 OSD 配置

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-device-osd/scripts

# 查询当前 OSD 配置
python3 osd_config.py --action get-single
```

### 2. 设置通道标题

```bash
# 设置通道标题
python3 osd_config.py --action set-channel-title \
  --title "大门摄像头" \
  --enable

# 关闭通道标题
python3 osd_config.py --action set-channel-title \
  --title "大门摄像头" \
  --disable
```

### 3. 设置时间标题

```bash
# 启用时间标题显示
python3 osd_config.py --action set-time-title --enable

# 设置时间标题位置
python3 osd_config.py --action set-time-title \
  --pos-x 100 --pos-y 50 \
  --enable
```

### 4. 设置隐私区域

```bash
# 添加隐私遮挡区域
python3 osd_config.py --action add-cover \
  --pos-x 1000 --pos-y 1000 \
  --width 500 --height 500
```

### 5. 查询多行 OSD 配置

```bash
# 查询多行 OSD 配置
python3 osd_config.py --action get-multi
```

## 坐标说明

### 相对位置坐标（RelativePos）

坐标值按比例转换为 0-8192 范围：

```
实际像素值
转换公式：坐标值 = (像素值 / 总像素) × 8192

示例：
- 画面宽度 1920 像素
- 标题左上角 X 坐标 100 像素
- 转换后：(100 / 1920) × 8192 ≈ 427
```

**坐标格式：** `[x1, y1, x2, y2]`
- `x1, y1`: 左上角坐标（有效）
- `x2, y2`: 右下角坐标（仅设置左上角时有效）

## 颜色格式

### RGBA 颜色字符串

格式：`"0xRRGGBBAA"`
- RR: 红色分量（00-FF）
- GG: 绿色分量（00-FF）
- BB: 蓝色分量（00-FF）
- AA: 透明度分量（00-FF，00=完全透明，FF=完全不透明）

**示例：**
- `"0x000000FF"` - 黑色，不透明
- `"0xFFFFFFFF"` - 白色，不透明
- `"0x00000080"` - 黑色，半透明

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

1. **坐标范围** - 坐标值必须在 0-8192 范围内
2. **颜色格式** - 使用 0xRRGGBBAA 格式
3. **叠加使能** - EncodeBlend 控制录像叠加，PreviewBlend 控制预览叠加
4. **隐私区域** - 设置后画面相应区域会被遮挡

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/osd_config.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
