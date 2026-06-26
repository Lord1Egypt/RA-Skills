# 可灵图像生成 API 参考

详细 API 文档，供需要了解完整参数时使用。

## 环境变量

```bash
export KLING_ACCESS_KEY="your_access_key"
export KLING_SECRET_KEY="your_secret_key"
```

## API 端点

```
https://api-beijing.klingai.com
```

## 鉴权方式

使用 Access Key 和 Secret Key 生成 JWT Token。

**请求头：**
```
Authorization: Bearer <token>
Content-Type: application/json
```

---

## 1. 图像生成 (Image Generation)

标准文生图和图生图接口。

**接口：** `POST /v1/images/generations`

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_name` | string | 是 | 模型名称：kling-v1, kling-v1-5, kling-v2, kling-v2-new, kling-v2-1, kling-v3 |
| `prompt` | string | 是 | 正向提示词，最多2500字符 |
| `negative_prompt` | string | 否 | 负向提示词 |
| `image` | string | 否 | 参考图片 (URL或Base64) |
| `image_reference` | string | 否 | 图片参考类型：subject, face |
| `image_fidelity` | float | 否 | 图片参考强度 [0,1] |
| `human_fidelity` | float | 否 | 面部参考强度 [0,1]，仅subject类型 |
| `element_list` | array | 否 | 主体参考列表 |
| `resolution` | string | 否 | 清晰度：1k, 2k (默认1k) |
| `n` | int | 否 | 生成数量 [1,9] (默认1) |
| `aspect_ratio` | string | 否 | 宽高比：16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9 (默认16:9) |
| `watermark_info` | object | 否 | 水印信息 `{"enabled": true}` |
| `callback_url` | string | 否 | 回调通知地址 |
| `external_task_id` | string | 否 | 自定义任务ID |

### 查询任务

- 单个任务：`GET /v1/images/generations/{id}`
- 任务列表：`GET /v1/images/generations?pageNum=1&pageSize=30`

---

## 2. 图像 Omni (Omni-Image)

支持多图参考、主体参考的高级图像生成。

**接口：** `POST /v1/images/omni-image`

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_name` | string | 是 | kling-image-o1, kling-v3-omni |
| `prompt` | string | 是 | 提示词，支持 `<<<image_1>>>` 格式引用图片 |
| `image_list` | array | 否 | 参考图列表，最多10张 |
| `element_list` | array | 否 | 主体参考列表 |
| `resolution` | string | 否 | 1k, 2k, 4k (默认1k) |
| `result_type` | string | 否 | 结果类型：single, series (默认single) |
| `n` | int | 否 | 生成数量 [1,9]，series时无效 |
| `series_amount` | int | 否 | 组图数量 [2,9]，series时有效 |
| `aspect_ratio` | string | 否 | 宽高比 |
| `watermark_info` | object | 否 | 水印信息 |
| `callback_url` | string | 否 | 回调地址 |
| `external_task_id` | string | 否 | 自定义任务ID |

### 查询任务

- 单个任务：`GET /v1/images/omni-image/{id}`
- 任务列表：`GET /v1/images/omni-image?pageNum=1&pageSize=30`

---

## 3. 扩图 (Image Expansion)

智能扩展图像边界。

**接口：** `POST /v1/images/editing/expand`

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `image` | string | 是 | 参考图片 (URL或Base64) |
| `up_expansion_ratio` | float | 是 | 向上扩展比例 [0,2]，基于原图高度 |
| `down_expansion_ratio` | float | 是 | 向下扩展比例 [0,2]，基于原图高度 |
| `left_expansion_ratio` | float | 是 | 向左扩展比例 [0,2]，基于原图宽度 |
| `right_expansion_ratio` | float | 是 | 向右扩展比例 [0,2]，基于原图宽度 |
| `prompt` | string | 否 | 正向提示词 |
| `n` | int | 否 | 生成数量 [1,9] |
| `watermark_info` | object | 否 | 水印信息 |
| `callback_url` | string | 否 | 回调地址 |
| `external_task_id` | string | 否 | 自定义任务ID |

**限制：** 新图片整体面积不得超过原图片3倍

### 查询任务

- 单个任务：`GET /v1/images/editing/expand/{id}`
- 任务列表：`GET /v1/images/editing/expand?pageNum=1&pageSize=30`

---

## 其他 API

### 4. 多图参考生图 (Multi Image to Image)

**接口：** `POST /v1/images/multi-image-to-image`

### 5. 智能补全主体图 (AI Multi Shot)

**接口：** `POST /v1/images/ai-multishot`

### 6. 虚拟试穿 (Virtual Try-On)

**接口：** `POST /v1/images/virtual-try-on`

---

## 任务状态

| 状态 | 说明 |
|------|------|
| `submitted` | 已提交 |
| `processing` | 处理中 |
| `succeed` | 成功 |
| `failed` | 失败 |

## 图片限制

- **格式：** jpg, jpeg, png
- **大小：** 不超过10MB
- **尺寸：** 不小于300px
- **宽高比：** 1:2.5 ~ 2.5:1
- **Base64：** 不要添加 `data:image/png;base64,` 前缀
