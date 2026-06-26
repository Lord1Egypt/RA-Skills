---
name: xiangji-service
description: 象寄翻译服务，支持文本翻译和图片翻译。Use when: (1) 翻译文本内容到其他语言，(2) 翻译带文字的图片到目标语言，(3) 批量翻译图片。支持多种翻译引擎（百度/阿里云/Google/DeepL/ChatGPT等）。
---

# 象寄翻译服务

象寄翻译服务提供高质量的文本翻译和图片翻译功能，支持多种翻译引擎，覆盖全球多种语言。

## 官方资源

- **官网**: https://www.xiangjifanyi.com/
- **API 文档**: https://openapi-doc.xiangjifanyi.com/
- **微信客服**: xiangjifanyi（扫码或直接添加微信在线客服）

## 功能特点

- **文本翻译**: 支持多语言文本翻译，可选择不同翻译引擎
- **图片翻译**: 智能识别图片中的文字并翻译，支持本地文件和URL两种方式
- **批量处理**: 支持批量翻译多张图片
- **多种引擎**: 支持阿里云、Google、百度、DeepL、ChatGPT 等多种翻译引擎

---

## 前置条件

使用前需要获取以下密钥：

| 密钥类型 | 说明 | 用途 |
|----------|------|------|
| TextTransKey | 文本翻译密钥 | 文本翻译，在请求头 `X-API-Key` 中传递 |
| ImgTransKey | 图片翻译服务标识码 | 图片翻译，用于签名计算 |
| UserKey | 用户密钥 | 图片翻译，用于签名计算 |

**获取密钥**: 登录 [象寄控制台](https://www.xiangjifanyi.com/console/workspace) 获取相关密钥。

---

## 文本翻译

使用 `scripts/text_translate.py` 进行文本翻译。

### 基本用法

```bash
python scripts/text_translate.py \
  --api-key YOUR_TEXT_TRANS_KEY \
  --texts "你好世界" \
  --source-language CHS \
  --target-language ENG
```

### 批量翻译

```bash
python scripts/text_translate.py \
  --api-key YOUR_TEXT_TRANS_KEY \
  --texts "你好世界" "今天天气很好" "欢迎使用象寄翻译" \
  --source-language CHS \
  --target-language ENG
```

### 指定翻译引擎

```bash
python scripts/text_translate.py \
  --api-key YOUR_TEXT_TRANS_KEY \
  --texts "Hello, how are you?" \
  --source-language ENG \
  --target-language CHS \
  --vendor DeepL
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--api-key` | 是 | 文本翻译密钥 (TextTransKey) |
| `--texts` | 是 | 要翻译的文本（可多个，空格分隔） |
| `--source-language` | 是 | 源语言代码 |
| `--target-language` | 是 | 目标语言代码 |
| `--vendor` | 否 | 翻译引擎，可选值见下表 |

### 支持的翻译引擎

| Vendor | 说明 |
|--------|------|
| Aliyun | 阿里云翻译 |
| Google | Google 翻译 |
| Papago | Papago 翻译（韩语优势） |
| Baidu | 百度翻译 |
| DeepL | DeepL 翻译（欧洲语言优势） |
| Chatgpt | ChatGPT 翻译 |
| GoogleLLM | Google 大模型翻译 |

---

## 图片翻译

使用 `scripts/image_translate.py` 进行图片翻译，支持本地文件和 URL 两种方式。

### 本地文件翻译

翻译本地图片文件中的文字：

```bash
python scripts/image_translate.py \
  --img-key YOUR_IMG_TRANS_KEY \
  --user-key YOUR_USER_KEY \
  --file /path/to/image.png \
  --source-language JPN \
  --target-language ENG
```

### URL 翻译（批量）

翻译网络图片（支持批量）：

```bash
python scripts/image_translate.py \
  --img-key YOUR_IMG_TRANS_KEY \
  --user-key YOUR_USER_KEY \
  --urls "https://example.com/image1.jpg" "https://example.com/image2.jpg" \
  --source-language CHS \
  --target-language ENG
```

### 高质量翻译

使用 `BestQuality` 模式获得更高质量的翻译结果：

```bash
python scripts/image_translate.py \
  --img-key YOUR_IMG_TRANS_KEY \
  --user-key YOUR_USER_KEY \
  --file /path/to/image.png \
  --source-language JPN \
  --target-language ENG \
  --qos BestQuality
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--img-key` | 是 | 图片翻译服务标识码 (ImgTransKey) |
| `--user-key` | 是 | 用户密钥 (UserKey)，用于签名 |
| `--file` | 二选一 | 本地图片文件路径 |
| `--urls` | 二选一 | 图片 URL 列表（可多个，空格分隔） |
| `--source-language` | 是 | 源语言代码 |
| `--target-language` | 是 | 目标语言代码 |
| `--qos` | 否 | 翻译质量：`LowLatency`（偏好速度）或 `BestQuality`（偏好质量） |
| `--need-watermark` | 否 | 是否添加水印：`1`=是，`0`=否（默认 1） |
| `--need-rm-url` | 否 | 是否返回去文字图片链接：`1`=是 |
| `--engine-type` | 否 | 翻译引擎类型（`5`=ChatGPT） |
| `--sync` | 否 | URL 翻译时：`1`=同步返回（默认），`2`=异步返回 |

### 签名计算

图片翻译接口需要签名验证，签名方法：

```python
Sign = md5(CommitTime + "_" + UserKey + "_" + ImgTransKey).lower()
```

脚本会自动计算签名，只需提供 `--user-key` 和 `--img-key`。

---

## 支持的语言

### 常用语言代码

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| `CHS` | 中文简体 | `CHT` | 中文繁体 |
| `ENG` | 英语 | `JPN` | 日语 |
| `KOR` | 韩语 | `DEU` | 德语 |
| `FRA` | 法语 | `ESP` | 西班牙语 |
| `RUS` | 俄语 | `PT` | 葡萄牙语 |
| `ITA` | 意大利语 | `TH` | 泰语 |
| `VIN` | 越南语 | `ID` | 印尼语 |

> 完整语言列表见 [references/languages.md](references/languages.md)

---

## API 端点

| 功能 | 端点 |
|------|------|
| 文本翻译 | `POST https://api.tosoiot.com/task/v1/text/translate` |
| 图片翻译（文件） | `POST https://api2.tosoiot.com/` |
| 图片翻译（URL 批量） | `POST https://api.tosoiot.com/` |

---

## 错误码

| Code | 说明 |
|------|------|
| 200 | 响应成功 |
| 101 | 请求超时 |
| 102 | 系统错误 |
| 104 | 参数错误 |
| 105 | 该语向不支持 |
| 107 | 翻译错误 |
| 110 | 账号没有开通服务 |
| 113 | 账号服务没有开通或者欠费 |
| 120 | 额度不足 |

---

## 使用示例

### 示例 1：翻译日文图片为英文

```bash
python scripts/image_translate.py \
  --img-key YOUR_IMG_KEY \
  --user-key YOUR_USER_KEY \
  --file /path/to/japanese_manga.png \
  --source-language JPN \
  --target-language ENG \
  --qos BestQuality
```

### 示例 2：翻译中文文本为日语

```bash
python scripts/text_translate.py \
  --api-key YOUR_API_KEY \
  --texts "你好，欢迎使用象寄翻译服务" \
  --source-language CHS \
  --target-language JPN \
  --vendor Chatgpt
```

### 示例 3：批量翻译电商图片

```bash
python scripts/image_translate.py \
  --img-key YOUR_IMG_KEY \
  --user-key YOUR_USER_KEY \
  --urls "https://example.com/product1.jpg" "https://example.com/product2.jpg" \
  --source-language CHS \
  --target-language ENG
```

### 示例 4：使用 DeepL 翻译欧洲语言

```bash
python scripts/text_translate.py \
  --api-key YOUR_API_KEY \
  --texts "Guten Tag, wie geht es Ihnen?" \
  --source-language DEU \
  --target-language FRA \
  --vendor DeepL
```

---

## 联系方式

如有问题或需要技术支持，请通过以下方式联系：

- **微信客服**: xiangjifanyi（扫码或直接添加微信在线客服）
- **官网**: https://www.xiangjifanyi.com/
- **API 文档**: https://openapi-doc.xiangjifanyi.com/
