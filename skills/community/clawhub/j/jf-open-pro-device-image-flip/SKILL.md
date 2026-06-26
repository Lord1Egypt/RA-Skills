---
name: jf-open-pro-device-image-flip
description: 杰峰设备画面翻转技能（开发版）。支持画面左右翻转（镜像）、上下翻转设置，适用于摄像头画面方向调整。
metadata:
  version: 1.0.0
  author: JFTech
  category: camera
  tags:
    - 杰峰
    - 画面翻转
    - 镜像
    - 上下翻转
    - 左右翻转
    - 摄像头配置
  triggers:
    - 查询画面翻转配置
    - 设置画面翻转
    - 开启左右翻转
    - 关闭左右翻转
    - 开启上下翻转
    - 关闭上下翻转
    - 画面镜像
    - 画面倒置
    - 摄像头翻转
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

# jf-open-pro-device-image-flip - 杰峰设备画面翻转技能（开发版）

## 技能描述

支持杰峰设备的画面翻转功能，基于杰峰开放平台 OpenAPI 实现：

- **画面左右翻转（镜像）** - 水平翻转画面，类似镜子效果
- **画面上下翻转（倒置）** - 垂直翻转画面，上下颠倒
- **翻转状态查询** - 查询当前画面翻转配置

**适用场景：**
- 摄像头倒装时需要上下翻转画面
- 摄像头镜像安装时需要左右翻转画面
- 特殊安装角度需要调整画面方向

## 触发词

- 查询画面翻转配置 / 设置画面翻转
- 开启左右翻转 / 关闭左右翻转
- 开启上下翻转 / 关闭上下翻转
- 画面镜像 / 画面倒置 / 摄像头翻转

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

| 功能 | 地址 | 方法 | 需要 Token | 需要在线 |
|------|------|------|------------|----------|
| 获取画面配置 | `POST /gwp/v3/rtc/device/getconfig/{token}` | POST | ✅ | ✅ |
| 设置画面配置 | `POST /gwp/v3/rtc/device/setconfig/{token}` | POST | ✅ | ✅ |

**配置名称：** `Camera.Param`

## 核心功能

### 画面翻转参数（Camera.Param）

| 字段 | 类型 | 说明 | 取值 |
|------|------|------|------|
| `PictureFlip` | string | 上下翻转 | `"0x00000000"`=不翻转，`"0x00000001"`=翻转 |
| `PictureMirror` | string | 左右翻转（镜像） | `"0x00000000"`=不翻转，`"0x00000001"`=翻转 |

### ⚠️ 走廊模式影响

当开启**走廊模式（CorridorMode）**时，翻转效果会互换：

| 模式 | PictureFlip | PictureMirror |
|------|-------------|---------------|
| **普通模式** | 上下翻转 | 左右翻转（镜像） |
| **走廊模式** | 左右翻转 | 上下翻转 |

**走廊模式取值：**
- `0`: 普通模式
- `1`: 走廊模式，画面逆时针转 90 度
- `2`: 画面逆时针旋转 180 度
- `3`: 走廊模式，画面逆时针旋转 270 度

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

### 1. 查询画面翻转配置

```bash
cd ~/.openclaw/workspace/skills/developer/jf-open-pro-device-image-flip/scripts

python3 image_flip.py --action get-flip-config
```

### 2. 设置左右翻转（镜像）

```bash
# 开启左右翻转
python3 image_flip.py --action set-mirror --enable true

# 关闭左右翻转
python3 image_flip.py --action set-mirror --enable false
```

### 3. 设置上下翻转

```bash
# 开启上下翻转
python3 image_flip.py --action set-flip --enable true

# 关闭上下翻转
python3 image_flip.py --action set-flip --enable false
```

### 4. 同时设置左右和上下翻转

```bash
# 同时开启左右和上下翻转（相当于旋转 180 度）
python3 image_flip.py --action set-both --mirror true --flip true

# 同时关闭
python3 image_flip.py --action set-both --mirror false --flip false
```

### 5. 重置画面方向

```bash
# 重置为默认（不翻转）
python3 image_flip.py --action reset
```

## 翻转效果说明

### 左右翻转（PictureMirror / 镜像）

```
原始画面：        左右翻转后：
┌─────────┐      ┌─────────┐
│  ABCD   │      │   DCBA  │
│  1234   │  →   │   4321  │
│  EFGH   │      │   HGFE  │
└─────────┘      └─────────┘
```

**适用场景：**
- 摄像头镜像安装
- 画面需要水平对称

### 上下翻转（PictureFlip / 倒置）

```
原始画面：        上下翻转后：
┌─────────┐      ┌─────────┐
│  ABCD   │      │  EFGH   │
│  1234   │  →   │  1234   │
│  EFGH   │      │  ABCD   │
└─────────┘      └─────────┘
```

**适用场景：**
- 摄像头倒装（天花板安装）
- 画面需要垂直对称

### 组合效果

| 左右翻转 | 上下翻转 | 效果 |
|----------|----------|------|
| 关 | 关 | 原始画面 |
| 开 | 关 | 左右镜像 |
| 关 | 开 | 上下倒置 |
| 开 | 开 | 旋转 180 度 |

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

1. **deviceToken 有效期** - 24 小时，过期需重新获取
2. **设备在线要求** - 配置类操作需要设备在线
3. **走廊模式影响** - 开启走廊模式时，翻转效果会互换
4. **立即生效** - 设置后画面会立即翻转，可能需要重新加载视频流
5. **配置保存** - 设置会保存到设备，重启后仍然生效
6. **通道号** - NVR 设备需要指定通道号（0-N）

## 相关文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档 |
| `scripts/image_flip.py` | Python 执行脚本 |
| `scripts/crypto.py` | 签名/时间戳加密工具（复用） |

## 参考文档

- [杰峰开放平台](https://docs.jftech.com)
