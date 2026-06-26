---
name: pill-counter
version: 4.0.0
description: |
  药片精确计数工具，支持双模式：
  - OpenCV 本地识别（免费、离线、快速）
  - MiMo V2 Omni AI 识别（更准确、需API密钥）

  支持13种药片形状，输出统计表格和标注图片。
setup: |
  基础依赖（OpenCV模式）：
  ```bash
  pip install opencv-python-headless numpy Pillow
  ```
  AI模式需要配置 MiMo API 密钥（已有则无需额外配置）。
permissions:
  paths:
    - "~/.openclaw/workspace/pill-counter/**"
  write: true
---

# 💊 药片精确计数 Skill v4 - 双模式

## 两种识别模式

| 模式 | 命令 | 精度 | 成本 | 依赖 |
|------|------|------|------|------|
| **OpenCV** | `python3 script.py 图片.jpg` | ⭐⭐⭐ | 免费 | opencv |
| **AI** | `python3 script.py 图片.jpg --ai` | ⭐⭐⭐⭐⭐ | API费用 | MiMo API密钥 |

## 使用方法

### OpenCV模式（默认，免费离线）
```bash
python3 scripts/pill_counter.py 图片.jpg
python3 scripts/pill_counter.py 图片.jpg --save 标注图.jpg --export-csv 统计.csv
```

### AI模式（更准确，需网络+API密钥）
```bash
python3 scripts/pill_counter.py 图片.jpg --ai
python3 scripts/pill_counter.py 图片.jpg --ai --export-csv 统计.csv
```

### 输出格式
```bash
# 文本表格（默认）
python3 scripts/pill_counter.py 图片.jpg

# JSON输出
python3 scripts/pill_counter.py 图片.jpg --output json

# 导出CSV
python3 scripts/pill_counter.py 图片.jpg --export-csv report.csv
```

## 支持的形状（13种）

圆形(小/中/大)、椭圆形、胶囊形、三角形、四方形、菱形、五边形、六边形、八边形、多边形、其他

## AI模式工作原理

1. 读取图片 → 压缩至1024px → base64编码
2. 调用 MiMo V2 Omni API，Prompt 要求逐粒计数+分类
3. 解析AI返回的JSON结果
4. 输出统计表格

## 注意事项

- OpenCV模式：适合规则摆放的药片，重叠场景可能漏检
- AI模式：适合复杂场景，但有API调用费用
- AI模式需要 `~/.openclaw/openclaw.json` 中配置 MiMo API 密钥
- 两种模式可混合使用：先用OpenCV快速看，再用AI精确计数
