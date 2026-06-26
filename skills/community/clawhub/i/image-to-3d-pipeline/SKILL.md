---
name: image-to-3d-pipeline
description: 一键将商品图片转换为高质量3D模型的自动化流水线（图片预处理 → AI增强 → 3D生成）
user-invocable: true
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["TRIPOSR_API_KEY"],
        "optional": ["REMOVE_BG_API_KEY", "UPSCALE_API_KEY"]
      },
      "primaryEnv": "TRIPOSR_API_KEY"
    }
  }
---

# Image to 3D Pipeline - 商品图片一键转3D模型

将任意商品图片自动转化为高质量3D模型的端到端流水线工具。

## 功能特性

- 🖼️ **图片预处理** - 自动去除背景、标准化图片
- ✨ **AI 增强** - 提升图片质量（可选）
- 🎯 **3D 生成** - 调用 Tripo3D 生成 3D 模型（快手开源）
- 📦 **多格式输出** - 支持 GLB/OBJ/USDZ 格式

## 使用前提

需要获取以下 API Key：

1. **TRIPOSR_API_KEY** - 必需
   - 方案A: Replicate API - https://replicate.com/baaas/triposr
   - 方案B: 自托管 - 部署 Tripo3D 开源版
   - 推荐先用 Replicate 测试，效果好再自托管

2. **REMOVE_BG_API_KEY** - 可选
   - 访问 https://www.remove.bg/api 获取
   - 或使用开源 rembg

3. **UPSCALE_API_KEY** - 可选
   - 访问 https://upscale.ai/ 获取
   - 用于提升图片质量

## API 定价参考

### Replicate (Tripo3D)
| 方案 | 价格 |
|------|------|
| Replicate 按量 | 约 $0.005-0.01/次 |
| 自托管 (A100) | 约 ¥2-3/小时，批量免费 |
| Multi Image to 3D | 5-15 credits |

## 工作流

```
输入图片 → 背景去除 → 图片增强 → Tripo3D 生成 → 输出模型
```

## 使用方法

### 基本调用

用户提供商品图片 URL 或上传图片即可自动生成 3D 模型。

### API 调用示例 (Replicate)

**1. 提交 Tripo3D 任务**

```bash
curl -X POST "https://api.replicate.com/v1/predictions" \
  -H "Authorization: Token $TRIPOSR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "abc123...",  // Tripo3D model version
    "input": {
      "image": "https://example.com/product.jpg"
    }
  }'
```

**响应：**
```json
{
  "id": "pred_abc123",
  "status": "starting"
}
```

**2. 查询任务状态**

```bash
curl "https://api.replicate.com/v1/predictions/pred_abc123" \
  -H "Authorization: Token $TRIPOSR_API_KEY"
```

**3. 任务完成响应：**
```json
{
  "status": "succeeded",
  "output": {
    "glb": "https://replicate.delivery/..."
  }
}
```

## 完整流程实现

### Step 1: 图片预处理（去除背景）

```bash
# 使用 remove.bg API
curl -X POST "https://api.remove.bg/v1.0/removebg" \
  -H "X-Api-Key: $REMOVE_BG_API_KEY" \
  -F "image_url=https://example.com/product.jpg" \
  -F "size=auto" \
  -o no_bg.png
```

### Step 2: 调用 Tripo3D 生成 3D

```bash
# 提交任务
TASK_RESPONSE=$(curl -s -X POST "https://api.replicate.com/v1/predictions" \
  -H "Authorization: Token $TRIPOSR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://your-processed-image-url.png",
    "enable_pbr": true,
    "background_color": "ffffff"
  }')

TASK_ID=$(echo $TASK_RESPONSE | jq -r '.task_id')

# 轮询结果（每20秒检查一次）
while true; do
  STATUS=$(curl -s "https://api.meshy.ai/v2/image-to-3d/$TASK_ID" \
    -H "Authorization: Bearer $MESHY_API_KEY" | jq -r '.status')
  
  if [ "$STATUS" == "SUCCEEDED" ]; then
    echo "3D模型生成完成！"
    break
  elif [ "$STATUS" == "FAILED" ]; then
    echo "生成失败"
    break
  fi
  
  echo "等待生成中... ($STATUS)"
  sleep 20
done
```

## 输出格式说明

| 格式 | 用途 | 兼容性 |
|------|------|--------|
| GLB | Web/移动端 AR | 最佳，WebXR 直接支持 |
| GLTF | Web 3D | 通用 |
| OBJ | 3D 软件导入 | Blender、Maya 等 |
| USDZ | iOS AR Quick Look | 苹果生态专用 |

## 错误处理

常见错误：
- `INVALID_API_KEY` - API Key 无效
- `IMAGE_TOO_LARGE` - 图片超过 20MB
- `RATE_LIMIT_EXCEEDED` - 请求频率超限
- `PROCESSING_FAILED` - 模型生成失败

## 进阶用法

### 批量处理

支持批量提交多个图片任务：

```bash
# 批量生成（需要企业版 API）
for img in "${images[@]}"; do
  curl -X POST "https://api.meshy.ai/v2/image-to-3d" \
    -H "Authorization: Bearer $MESHY_API_KEY" \
    -d "{\"image_url\": \"$img\", \"enable_pbr\": true}" &
done
```

### 自定义参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| enable_pbr | 启用 PBR 材质 | true |
| background_color | 背景色（十六进制） | 透明 |
| texture_resolution | 纹理分辨率 | 1024 |
| target_model | 输出格式 | glb |

## 注意事项

1. **任务时间** - 3D 生成通常需要 2-5 分钟，请耐心等待
2. **不要重复提交** - 任务有内部重试机制，重复提交会浪费资源
3. **图片质量** - 建议使用清晰、光线均匀的商品图片
4. **版权** - 确保上传的图片有合法使用权

---

**一句话介绍**：自动将商品图片转化为高质量3D模型的端到端流水线工具