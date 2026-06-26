# 即梦 AI 图片生成 4.0 API 参考

## 接口信息

| 项目 | 内容 |
|------|------|
| Endpoint | `https://visual.volcengineapi.com` |
| 签名算法 | HMAC-SHA256 V4（火山引擎标准） |
| Region | `cn-north-1` |
| Service | `cv` |
| req_key | `jimeng_t2i_v40` |
| Version | `2022-08-31` |

## 调用流程（异步两步）

```
第一步 提交任务
  POST https://visual.volcengineapi.com?Action=CVSync2AsyncSubmitTask&Version=2022-08-31
  → 返回 task_id

第二步 轮询结果（每 3s 查一次，最多等 120s）
  POST https://visual.volcengineapi.com?Action=CVSync2AsyncGetResult&Version=2022-08-31
  → data.status: in_queue / generating / done / not_found / expired
  → done 时从 data.image_urls 取图片 URL（有效期 24h）
```

## 提交任务请求体参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| req_key | string | ✅ | 固定值 `jimeng_t2i_v40` |
| prompt | string | ✅ | 提示词，最长 800 字符，中英文均可 |
| image_urls | array | ❌ | 参考图 URL，0~10 张，JPEG/PNG，最大 15MB，最大 4096×4096 |
| size | int | ❌ | 生成面积，范围 [1024×1024, 4096×4096]，默认 4194304（2K） |
| width | int | ❌ | 精确宽度，需与 height 同时传 |
| height | int | ❌ | 精确高度，需与 width 同时传 |
| scale | float | ❌ | 文本影响强度 0~1，默认 0.5（图生图时有效） |
| force_single | bool | ❌ | 强制只输出 1 张，默认 false |
| min_ratio | float | ❌ | 宽高比下限，默认 1/3 |
| max_ratio | float | ❌ | 宽高比上限，默认 3 |

> **分辨率优先级**: width+height > size > 默认 2K 自动比例

## 官方推荐宽高预设

| 分辨率 | 比例 | 宽×高 |
|--------|------|-------|
| 1K | 1:1 | 1024×1024 |
| 2K | 1:1 | 2048×2048 |
| 2K | 4:3 | 2304×1728 |
| 2K | 3:2 | 2496×1664 |
| 2K | 16:9 | 2560×1440 |
| 2K | 21:9 | 3024×1296 |
| 4K | 1:1 | 4096×4096 |
| 4K | 4:3 | 4694×3520 |
| 4K | 3:2 | 4992×3328 |
| 4K | 16:9 | 5404×3040 |
| 4K | 21:9 | 6198×2656 |

## 查询任务请求体参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| req_key | string | ✅ | 固定值 `jimeng_t2i_v40` |
| task_id | string | ✅ | 提交任务返回的 task_id |
| req_json | string | ❌ | JSON 序列化字符串，配置 return_url / logo_info 等 |

### req_json 示例
```json
{
  "return_url": true,
  "logo_info": {
    "add_logo": false
  }
}
```
> 注意：req_json 需先 JSON.stringify 后再作为字符串传入

## 任务状态说明

| status | 含义 |
|--------|------|
| in_queue | 已提交，排队中 |
| generating | 处理中 |
| done | 完成（再判断 code 和 image_urls） |
| not_found | 未找到（无此任务或已过期 12h） |
| expired | 已过期，需重新提交 |

## 业务错误码

| code | 说明 | 可重试 |
|------|------|--------|
| 10000 | 成功 | — |
| 50411 | 输入图片审核未通过 | ❌ |
| 50511 | 输出图片审核未通过 | ✅ |
| 50412/50413 | 文本审核未通过/含敏感词 | ❌ |
| 50429 | QPS 超限 | ✅ |
| 50430 | 并发超限 | ✅ |
| 50500/50501 | 内部错误 | ❌ |

## 计费说明

- 按**输出图片张数**计费（不是按调用次数）
- 默认 AI 自动判断输出数量（可能输出多张）
- 若对费用敏感，使用 `force_single: true` 强制单图

## 获取 API Key

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 进入「智能视觉」→「即梦 AI」→「立即开通」（有免费试用额度）
3. 进入「访问控制」→「密钥管理」→ 创建 Access Key / Secret Key
4. 配置环境变量：
   ```powershell
   # Windows（永久）
   setx JIMENG_ACCESS_KEY "你的AccessKey"
   setx JIMENG_SECRET_KEY "你的SecretKey"
   ```
