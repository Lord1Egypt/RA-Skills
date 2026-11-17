# JF Open API 文档

杰峰（JF Tech）开放平台 API 完整参考。

## 基础信息

**开放平台：** https://developer.jftech.com  
**API 文档：** https://docs.jftech.com  
**基础 URL：** `https://api.jftechws.com/aisvr/v3/gateway/api`

## 认证机制

### 请求头参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `uuid` | 开放平台用户 uuid | ✅ |
| `appkey` | 应用 appKey | ✅ |
| `sign` | 请求签名 | ✅ |
| `timestamp` | 当前时间戳（毫秒） | ✅ |
| `authorization` | 用户登录 token | ✅ |

### 签名算法

```python
import hashlib
import time

def generate_sign(appkey: str, secret: str) -> tuple:
    timestamp = int(time.time() * 1000)
    sign_str = f"{appkey}{timestamp}{secret}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign, timestamp
```

**注意：** 签名有效期 5 分钟，超时需重新生成。

## AI 智搜 API

### 搜索视频

**端点：** `POST /viewsearch/searchVideo`

**完整 URL：** `https://api.jftechws.com/aisvr/v3/gateway/api/viewsearch/searchVideo`

**请求体：**
```json
{
    "sn": "设备序列号",
    "user": "用户 ID",
    "searchContent": "搜索内容"
}
```

**请求示例：**
```bash
curl -X POST "https://api.jftechws.com/aisvr/v3/gateway/api/viewsearch/searchVideo" \
  -H "Content-Type: application/json" \
  -H "uuid: your-uuid" \
  -H "appkey: your-appkey" \
  -H "sign: generated-sign" \
  -H "timestamp: 1703275200000" \
  -H "authorization: your-token" \
  -d '{
    "sn": "48de8c1c1c20a4a3",
    "user": "admin",
    "searchContent": "戴帽子的人"
  }'
```

**成功响应：**
```json
{
    "code": 2000,
    "msg": "success",
    "data": {
        "videos": [
            {
                "st": 1703275200,
                "et": 1703275260,
                "matchRate": 0.95,
                "queryTags": ["person", "hat"],
                "eventTime": "2024-12-23 10:00:00",
                "vidsz": 1048576,
                "picfg": 1
            }
        ]
    }
}
```

**响应字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `st` | int | 录像开始时间（Unix 秒） |
| `et` | int | 录像结束时间（Unix 秒） |
| `matchRate` | float | 匹配度（0-1） |
| `queryTags` | array | 检测到的标签列表 |
| `eventTime` | string | 事件触发时间（格式化） |
| `vidsz` | int | 视频大小（字节） |
| `picfg` | int | 是否有缩略图（1=有，0=无） |

### 搜索参数说明

**searchContent 支持的内容：**

| 类别 | 示例 | 说明 |
|------|------|------|
| 人物特征 | "戴帽子的人"、"穿红色衣服的人"、"戴口罩的人" | 基于人形检测 + 属性识别 |
| 车辆 | "车"、"白色轿车"、"卡车"、"摩托车" | 基于车辆检测 |
| 动物 | "狗"、"猫"、"鸟" | 基于动物检测 |
| 行为 | "跑步"、"摔倒"、"打架" | 基于行为分析（需支持） |

## 云存回放 API

### HLS 播放地址

**端点：** `POST /viewsearch/playback/hls`

**请求体：**
```json
{
    "sn": "设备序列号",
    "user": "用户 ID",
    "st": 1703275200,
    "et": 1703275260
}
```

### RTMP 播放地址

**端点：** `POST /viewsearch/playback/rtmp`

**请求体：** 同上

### FLV 播放地址

**端点：** `POST /viewsearch/playback/flv`

**请求体：** 同上

### WebRTC 播放地址

**端点：** `POST /viewsearch/playback/webrtc`

**请求体：** 同上

**响应示例：**
```json
{
    "code": 2000,
    "msg": "success",
    "data": {
        "url": "https://playback.jftechws.com/.../playback.m3u8"
    }
}
```

## 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 2000 | 成功 | - |
| 10001 | 参数错误 | 检查请求参数格式和必填字段 |
| 10002 | 签名失败 | 检查 appKey/secret 和时间戳同步 |
| 10003 | 权限不足 | 检查 authorization token 是否有效 |
| 12504 | 设备未开通服务 | 登录开放平台绑定套餐卡 |
| 12505 | 设备不在线 | 检查设备网络连接 |
| 12506 | 无云存录像 | 检查设备云存套餐和时间范围 |

## 套餐卡说明

AI 智搜功能需要设备开通相应套餐：

1. **AI 智搜套餐** - 支持语义搜索功能
2. **云存套餐** - 支持视频存储和回放

**绑定步骤：**
1. 登录 https://developer.jftech.com
2. 进入「套餐管理」
3. 选择对应套餐购买
4. 绑定到设备序列号
5. 等待 1-5 分钟生效

## 限流说明

| 接口 | 限流 | 说明 |
|------|------|------|
| 搜索视频 | 10 次/分钟 | 单用户单设备 |
| 回放地址 | 20 次/分钟 | 单用户单设备 |

**建议：** 搜索结果缓存 5 分钟，避免重复请求。

## 相关文档

- [套餐卡使用说明](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh)
- [云存回放 API](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672)
- [开放平台 SDK](https://github.com/jftech/open-platform-sdk)
