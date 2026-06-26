# 翔云银行卡识别 API 文档

> 官方产品页：https://www.netocr.com/bankCard.html
> 更新时间：2026-05

---

## 接口概述

支持识别普通横版、竖版、异型银行卡，包含平面字体和凸面字体银行卡，可结构化输出：

- 银行卡卡号
- 银行卡类型（储蓄卡 / 信用卡等）
- 银行卡名称
- 银行名称
- 银行编号

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
| `typeId` | Integer | ✅ | 固定值 **17**（银行卡识别专属编号） |
| `format` | String | ✅ | 返回格式：`json` 或 `xml`（为空默认返回 xml） |

### 方式二：文件上传（recog.do）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | MultipartFile | ✅ | 上传文件，字段名**必须**为 `file` |
| `key` | String | ✅ | 用户 ocrKey |
| `secret` | String | ✅ | 用户 ocrSecret |
| `typeId` | Integer | ✅ | 固定值 **17** |
| `format` | String | ✅ | 返回格式：`json` 或 `xml` |

---

## 响应格式（JSON）

### 成功响应（文件上传接口 recog.do）

```json
{
  "message": {
    "status": 0,
    "value": "识别完成"
  },
  "cardsinfo": [
    {
      "type": "17",
      "items": [
        {"nID": null, "index": null, "desc": "卡号", "content": "4270200014046685"},
        {"nID": null, "index": null, "desc": "银行卡类型", "content": "贷记卡"},
        {"nID": null, "index": null, "desc": "银行卡名称", "content": "牡丹VISA信用卡"},
        {"nID": null, "index": null, "desc": "银行名称", "content": "中国工商银行"},
        {"nID": null, "index": null, "desc": "银行编号", "content": "01020000"},
        {"nID": null, "index": null, "desc": "有效日期", "content": "11/19"},
        {"nID": null, "index": null, "desc": "银行卡持有人", "content": "MR.ZHU ZE FENG"}
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
| `-1` | 识别失败（图片质量不佳或未检测到银行卡） |
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

---

## Python 调用示例

```python
import requests, base64

# Base64 方式
with open("bankcard.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

resp = requests.post(
    "https://netocr.com/api/recogliu.do",
    data={
        "img": img_b64,
        "key": "YOUR_OCR_KEY",
        "secret": "YOUR_OCR_SECRET",
        "typeId": "17",
        "format": "json",
    },
    timeout=30,
)
print(resp.json())
```

```python
# 文件上传方式
import requests

with open("bankcard.jpg", "rb") as f:
    resp = requests.post(
        "https://netocr.com/api/recog.do",
        files={"file": ("bankcard.jpg", f)},
        data={
            "key": "YOUR_OCR_KEY",
            "secret": "YOUR_OCR_SECRET",
            "typeId": "17",
            "format": "json",
        },
        timeout=30,
    )
print(resp.json())
```

---

## 注意事项

1. `typeId` **固定为 17**，调用时不可修改，否则返回非银行卡识别结果
2. `key` 和 `secret` 在翔云平台注册后，进入「个人中心」→「我的 API」获取
3. 每次调用消耗一定额度，请确保账户余额充足
4. 建议图片分辨率足够清晰，卡号区域无遮挡、无强反光
