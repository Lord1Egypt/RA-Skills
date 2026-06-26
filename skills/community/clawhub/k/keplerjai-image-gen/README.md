# 🎨 ThinkZone Image Skill 使用指南

## 📋 目录

- [简介](#简介)
- [支持的模型](#支持的模型)
- [快速开始](#快速开始)
- [API 参考](#api-参考)
- [使用示例](#使用示例)
- [常见问题](#常见问题)

---

## 简介

**ThinkZone Image Skill** 是基于 BytePlus Seedream 系列的 AI 图片生成工具，支持 5 个不同的模型，提供从快速预览到高质量商业级的多种选择。

### 特性

- ✅ 支持 5 个 BytePlus Seedream 模型
- ✅ 高质量图片生成（最高 3K 分辨率）
- ✅ 批量生成（最多 15 张）
- ✅ 图生图功能
- ✅ 可重复生成（支持 seed 参数）

---

## 支持的模型

### 🎨 图片生成模型（5 个）

| 模型 | Model ID | 说明 | 推荐场景 | 相对速度 |
|------|----------|------|----------|----------|
| **Seedream 5.0** | `seedream-5-0-260128` | 最新版本，高质量图片生成 | 高质量需求、商业用途 | ⭐⭐⭐ |
| **Seedream 4.5** | `seedream-4-5-251128` | 稳定版本，快速生成 | 日常使用、快速迭代 | ⭐⭐⭐⭐ |
| **Seedream 4.0** | `seedream-4-0-241215` | 经典版本 | 兼容性需求 | ⭐⭐⭐⭐ |
| **Seedream 3.0** | `seedream-3-0-240820` | 基础版本 | 测试、开发 | ⭐⭐⭐⭐⭐ |
| **Seedream Lite** | `seedream-lite-240601` | 轻量快速版 | 快速预览、头像生成 | ⭐⭐⭐⭐⭐ |

### 📐 尺寸说明

| 尺寸 | 分辨率 | 总像素 | 适用场景 |
|------|--------|--------|----------|
| `2K` | ~2048×2048 | ~4.2M | 标准质量、社交媒体 |
| `3K` | ~3072×3072 | ~9.4M | 高质量、打印 |
| 自定义 | 宽×高 | ≥3.7M | 特殊需求 |

**注意**：图片尺寸必须 ≥ 3686400 像素（约 1920×1920）

---

## 快速开始

### 1. 配置环境变量

```bash
export THINKZONE_API_KEY="your_api_key_here"
export THINKZONE_BASE_URL="https://open.thinkzoneai.com"
```

### 2. 安装依赖

```bash
# 确保已安装 Python 3.7+
python --version
```

### 3. 测试运行

```bash
# 使用默认模型（Seedream 5.0）
python scripts/gen_image.py --prompt "一只可爱的猫咪"

# 指定模型
python scripts/gen_image.py \
  --prompt "科幻城市夜景" \
  --model seedream-5-0-260128 \
  --size 2K
```

---

## API 参考

### 基础信息

- **Base URL**: `https://open.thinkzoneai.com`
- **Endpoint**: `/v3/images/generations`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Authorization**: `Bearer {API_KEY}`

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `model` | string | 是 | - | 模型 ID，见上方模型列表 |
| `prompt` | string | 是 | - | 图像描述文本 |
| `size` | string | 否 | `2K` | 输出尺寸：`2K`、`3K` 或 `宽 x 高` |
| `output_format` | string | 否 | `jpeg` | 输出格式：`png`、`jpeg` |
| `response_format` | string | 否 | `url` | 返回格式：`url`、`b64_json` |
| `watermark` | boolean | 否 | `true` | 是否添加水印 |
| `n` | integer | 否 | `1` | 生成数量（1-15） |
| `seed` | integer | 否 | - | 随机种子 |
| `image` | string/array | 否 | - | 参考图（URL 或 Base64） |
| `sequential_image_generation` | string | 否 | - | 批量生成：`auto`、`disabled` |
| `sequential_image_generation_options` | object | 否 | - | 批量配置：`{max_images: 4}` |

### 响应格式

#### 成功响应

```json
{
  "data": [
    {
      "url": "https://..."
    }
  ],
  "usage": {
    "generated_images": 1,
    "output_tokens": 32768
  }
}
```

#### 错误响应

```json
{
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "账户余额不足"
  }
}
```

---

## 使用示例

### 示例 1：单张图片生成

```bash
python scripts/gen_image.py \
  --prompt "一只穿宇航服的虾在太空中漂浮，科幻风格，高质量" \
  --model seedream-5-0-260128 \
  --size 2K \
  --no-watermark
```

### 示例 2：批量生成 4 张

```bash
python scripts/gen_image.py \
  --prompt "中国风山水画，水墨画风格" \
  --model seedream-4-5-251128 \
  --size 2K \
  --max-images 4 \
  --sequential_image_generation auto
```

### 示例 3：高质量商业图

```bash
python scripts/gen_image.py \
  --prompt "未来科技城市，霓虹灯，赛博朋克风格，8K 质量，细节丰富" \
  --model seedream-5-0-260128 \
  --size 3K \
  --output-format png \
  --no-watermark
```

### 示例 4：可重复生成

```bash
# 使用相同的 seed 可以生成相同的图片
python scripts/gen_image.py \
  --prompt "测试图片" \
  --seed 12345 \
  --model seedream-5-0-260128
```

### 示例 5：cURL 调用

```bash
curl -X POST "https://open.thinkzoneai.com/v3/images/generations" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedream-5-0-260128",
    "prompt": "一只可爱的猫咪",
    "size": "2K",
    "n": 1,
    "watermark": false
  }'
```

---

## 常见问题

### Q1: 如何选择合适的模型？

**A:** 
- **商业用途/高质量需求** → 选择 `Seedream 5.0`
- **日常使用/快速迭代** → 选择 `Seedream 4.5`
- **测试/开发** → 选择 `Seedream 3.0` 或 `Seedream Lite`

### Q2: 图片生成的尺寸限制是什么？

**A:** 
- 最小尺寸：≥ 3686400 像素（约 1920×1920）
- 可选尺寸：`2K`（~2048×2048）、`3K`（~3072×3072）
- 自定义尺寸：宽×高（必须满足最小像素要求）

### Q3: 批量生成最多可以生成多少张？

**A:** 单次最多生成 **15 张** 图片。

### Q4: 生成的图片 URL 有效期多久？

**A:** 图片 URL 有效期为生成后 **24 小时**，请及时下载保存。

### Q5: 如何去除水印？

**A:** 添加 `--no-watermark` 参数或在 API 请求中设置 `"watermark": false`。

### Q6: 账户余额不足怎么办？

**A:** 访问 [ThinkZone AI 平台](https://open.thinkzoneai.com) 进行充值。

### Q7: 支持哪些图片格式输入？

**A:** 支持 JPEG、PNG、WEBP、BMP、TIFF、GIF 格式。

### Q8: 如何获得可重复的结果？

**A:** 使用 `--seed` 参数指定相同的随机种子，可以生成相同的图片。

---

## 故障排除

### 错误：AccountOverdueError

**原因**：账户余额不足  
**解决**：充值账户余额

### 错误：HTTP 503 Service Unavailable

**原因**：服务暂时不可用  
**解决**：等待几分钟后重试

### 错误：Unsupported model

**原因**：使用了不支持的模型  
**解决**：检查模型 ID 是否正确，见上方模型列表

### 错误：Size must be >= 3686400 pixels

**原因**：图片尺寸太小  
**解决**：使用 `2K` 或 `3K`，或自定义更大的尺寸

---

## 相关链接

- **ThinkZone AI 平台**: https://open.thinkzoneai.com
- **BytePlus ModelArk**: https://www.byteplus.com/en/modelark
- **Seedream 官方文档**: https://www.byteplus.com/en/seedream
- **GitHub 仓库**: （待添加）

---

## 更新日志

### v1.0.0 (2026-03-16)
- ✅ 初始版本
- ✅ 支持 5 个 BytePlus Seedream 模型
- ✅ 添加图片生成脚本
- ✅ 添加测试脚本
- ✅ 完整文档

---

*最后更新：2026-03-16*
