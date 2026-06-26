---
name: image-collector
description: "AI 科技日报图片采集工具，从官方来源自动采集新闻配图，支持水印检测、质量检查和关联性验证"
metadata: { "openclaw": { "emoji": "📸", "requires": { "python": ">=3.8", "pip": ["Pillow", "requests"] } } }
---

# image-collector Skill

## 功能概述

自动为 AI 科技日报新闻采集配图，确保：
- ✅ **图片与内容强关联** — 优先从官方来源采集
- ✅ **无水印** — 自动检测并过滤带水印图片
- ✅ **高质量** — 分辨率≥800x600，无明显压缩
- ✅ **不随意贴图** — 关联性验证，拒绝随机图片

## 快速开始

```bash
# 检查依赖
bash ~/.openclaw/workspace/skills/image-collector/scripts/check-deps.sh
```

## 基本用法

```bash
# 为单条新闻采集配图
python3 ~/.openclaw/workspace/skills/image-collector/scripts/collect_images.py \
  --news "苹果国行 AI 凌晨偷跑" \
  --keywords "Apple,Intelligence,Baidu" \
  --source "apple.com"
```

## 图片来源优先级

| 优先级 | 来源类型 | 示例域名 |
|--------|----------|----------|
| **P0** | 官方新闻稿 | apple.com, microsoft.com, openai.com |
| **P1** | 权威媒体 | 36kr.com, bloomberg.com, reuters.com |
| **P2** | 产品截图 | 手动截取（使用 web-access skill） |
| **P3** | 自制图表 | Python matplotlib / Excel |
| **禁用** | 随机图片 | unsplash.com, pixabay.com |
| **禁用** | 微信图片 | mmbiz.qpic.cn |

## 验证流程

1. **来源验证** → 只从白名单来源采集
2. **水印检测** → 四角 + 底部检测，过滤带水印图片
3. **质量检查** → 分辨率≥800x600，宽高比正常
4. **关联性验证** → 文件名关键词匹配评分
5. **✅ 最终输出** → 优化后的图片

## 配合 web-access skill

当自动采集失败时：

```bash
# 1. 用 web-access 打开官网截图
curl -s "http://localhost:3456/new?url=https://www.apple.com/newsroom"

# 2. 截图后手动保存到 article-images/

# 3. 用 image-collector 优化
python3 collect_images.py --optimize /tmp/screenshot.png
```

## 验证标准

### 1. 关联性验证
- [x] 图片主题与新闻标题匹配
- [x] 图片中包含新闻关键词
- [x] 图片来源与新闻主体相关

### 2. 水印检查
- [x] 四角无 Logo 水印
- [x] 底部无公众号名称
- [x] 无明显版权标识

### 3. 质量检查
- [x] 分辨率 ≥ 800x600
- [x] 无明显压缩痕迹
- [x] 色彩正常

---

## 作者

九万
