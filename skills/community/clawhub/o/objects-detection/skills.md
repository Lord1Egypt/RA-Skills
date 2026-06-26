# OpenClaw Skill + iOS 集成示例：ObjectVision

## 一、Skill 信息

- **Skill 名称**: ObjectVision
- **版本**: 1.0.0
- **类型**: 视觉识别 / 物体识别
- **作者**: YourName
- **描述**: 专业物体识别技能。输入图片，返回场景、物体名称、类别、品牌、材质、价格和置信度。
- **标签**: object recognition, vision, ai, 物体识别
- **License**: MIT

---

## 二、Skill 配置 JSON

```json
{
  "name": "ObjectVision",
  "description": "专业物体识别技能。输入图片，返回场景、物体名称、类别、品牌、材质、价格和置信度。",
  "version": "1.0.0",
  "input_schema": {
    "type": "object",
    "properties": {
      "image_url": {
        "type": "string",
        "description": "要识别的图片 URL"
      },
      "detection_level": {
        "type": "string",
        "enum": ["basic", "full", "professional"],
        "default": "full",
        "description": "识别精度等级，basic: 基础物体, full: 品牌材质, professional: 包含小物件/抽屉内部"
      }
    },
    "required": ["image_url"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "scene": {
        "type": "string",
        "description": "图片场景描述，例如卧室桌面、办公室"
      },
      "objects": {
        "type": "array",
        "description": "检测到的物体列表",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string", "description": "物体名称" },
            "category": { "type": "string", "description": "物体类别" },
            "confidence": { "type": "number", "description": "识别置信度，0-1" },
            "bounding_box": {
              "type": "array",
              "description": "[x, y, width, height] 物体框坐标",
              "items": { "type": "number" }
            },
            "brand": { "type": "string", "description": "品牌，可推理" },
            "material": { "type": "string", "description": "材质，可推理" },
            "estimated_price_range": { "type": "string", "description": "估算价格区间" }
          },
          "required": ["name", "category", "confidence", "bounding_box"]
        }
      }
    },
    "required": ["scene", "objects"]
  },
  "prompt": "You are a professional object recognition engine. Analyze the image provided in 'image_url' and return a JSON with the following: 1. Detect all objects. 2. For each object output: name, category, confidence (0-1), bounding_box [x, y, width, height], brand (if identifiable), material (if inferable), estimated_price_range (if known). 3. Provide scene description. 4. Return only JSON, no explanations. 5. If uncertain, lower confidence score instead of hallucinating.",
  "examples": [
    {
      "input": {
        "image_url": "https://example.com/photo.jpg",
        "detection_level": "full"
      },
      "output": {
        "scene": "office desk",
        "objects": [
          {
            "name": "iPhone 15 Pro",
            "category": "Electronics",
            "confidence": 0.95,
            "bounding_box": [100, 50, 200, 400],
            "brand": "Apple",
            "material": "Titanium",
            "estimated_price_range": "$999-$1299"
          },
          {
            "name": "MacBook Pro 16",
            "category": "Electronics",
            "confidence": 0.92,
            "bounding_box": [300, 60, 600, 400],
            "brand": "Apple",
            "material": "Aluminum",
            "estimated_price_range": "$2499-$2999"
          }
        ]
      }
    }
  ]
}