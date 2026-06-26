# 翔云护照识别 API 文档

> 官方产品页：https://www.netocr.com/products.html
> 更新时间：2026-05

---

## 接口概述

通过翔云证件识别接口（typeId=13），对图片中的护照进行结构化信息提取，支持中国护照及多国护照。

识别输出字段包括：
- 护照号码
- 姓名 / 拼音
- 性别
- 出生日期 / 出生地点
- 签发日期 / 有效期限
- 签发机关
- 国籍 / 签发国
- 机读区（MRZ）

---

## 接口地址

| 上传方式 | 接口地址 |
|---------|---------|
| Base64 图片流 | `https://netocr.com/api/recogliu.do` |
| File 文件格式 | `https://netocr.com/api/recog.do` |

- **请求方式：** `POST`
- **Content-Type：** `multipart/form-data`

---

## 请求参数

### 方式一：Base64 图片流（recogliu.do）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `img` | String | ✅ | 图片的 Base64 编码字符串 |
| `key` | String | ✅ | 用户 ocrKey（个人中心获取） |
| `secret` | String | ✅ | 用户 ocrSecret（个人中心获取） |
| `typeId` | Integer | ✅ | 固定值 **13**（护照识别专属编号） |
| `format` | String | ✅ | 返回格式：`json` 或 `xml`（为空默认返回 xml） |

### 方式二：文件上传（recog.do）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | MultipartFile | ✅ | 上传文件，字段名**必须**为 `file` |
| `key` | String | ✅ | 用户 ocrKey |
| `secret` | String | ✅ | 用户 ocrSecret |
| `typeId` | Integer | ✅ | 固定值 **13** |
| `format` | String | ✅ | 返回格式：`json` 或 `xml` |

---

## 响应格式（JSON）

### 成功响应示例

```json
{
  "message": {
    "status": 0,
    "value": "识别完成"
  },
  "cardsinfo": [
    {
      "type": "13",
      "items": [
        {"desc": "护照号码", "content": "E12345678"},
        {"desc": "姓名", "content": "张三"},
        {"desc": "拼音", "content": "ZHANG SAN"},
        {"desc": "性别", "content": "男"},
        {"desc": "出生日期", "content": "1990-01-01"},
        {"desc": "出生地点", "content": "北京"},
        {"desc": "签发日期", "content": "2020-06-01"},
        {"desc": "有效期限", "content": "2030-06-01"},
        {"desc": "签发机关", "content": "国家移民管理局"},
        {"desc": "国籍", "content": "中国"},
        {"desc": "签发国", "content": "中国"}
      ]
    }
  ]
}
```

**注意：** Base64 接口（recogliu.do）和文件上传接口（recog.do）可能返回不同格式，本 Skill 同时兼容 `cardsinfo` 和 `responseCode/inferredValue` 两种格式。

---

## 错误码说明

| 状态码 | 含义 |
|--------|------|
| `0` | 识别成功 |
| `-1` | 识别失败（图片质量不佳或未检测到护照） |
| `-2` | 参数错误 |
| `-3` | 服务次数不足（需充值） |
| `-4` | 认证失败（key/secret 错误） |
| `-5` | 余额不足 |

---

## 图片规格要求

| 类型 | 建议规格 |
|------|---------|
| 普通图片 | 大小约 200KB，位深度 24 以上 |
| 扫描图像 | 分辨率 300DPI，文件小于 3MB |
| 支持格式 | JPG、PNG、BMP |
| 最大文件 | 不超过 10MB |

- 建议护照正面平放拍摄，避免反光、遮挡
- 文字清晰可辨，对比度适中

---

## Python 调用示例

```python
import requests

# 文件上传方式（推荐）
with open("passport.jpg", "rb") as f:
    resp = requests.post(
        "https://netocr.com/api/recog.do",
        files={"file": ("passport.jpg", f)},
        data={
            "key": "YOUR_OCR_KEY",
            "secret": "YOUR_OCR_SECRET",
            "typeId": "13",
            "format": "json",
        },
        timeout=30,
    )
print(resp.json())
```

```python
# Base64 方式
import requests, base64

with open("passport.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

resp = requests.post(
    "https://netocr.com/api/recogliu.do",
    data={
        "img": img_b64,
        "key": "YOUR_OCR_KEY",
        "secret": "YOUR_OCR_SECRET",
        "typeId": "13",
        "format": "json",
    },
    timeout=30,
)
print(resp.json())
```

---

## 注意事项

1. `typeId` **固定为 13**，调用时不可修改，否则返回非护照识别结果
2. `key` 和 `secret` 在翔云平台注册后，进入「个人中心」→「我的 API」获取
3. 每次调用消耗一定额度，请确保账户余额充足
4. 建议护照页面内容清晰完整，无遮挡、无强反光
5. 文件上传方式（recog.do）比 Base64 方式（recogliu.do）对图片大小限制更友好
