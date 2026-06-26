# Image Manager Skill

本地图片管理技能，支持索引、压缩、分类、快速查找。

## 功能

- 📁 **分类存储**：按类别（pets/people/food/scenery/receipts/other）自动归档
- 🔍 **快速索引**：基于 JSON 索引文件，支持按标签、日期、类别查找
- 🗜️ **压缩保存**：原图 + 缩略图双存储，查看缩略图不影响原图画质
- 🏷️ **标签系统**：每张图片可附加多标签，支持标签搜索
- 📊 **摘要浏览**：快速浏览某个类别/标签的所有图片

## 目录结构

```
media/
├── images/                    # 原图（保持完整画质）
│   ├── pets/
│   ├── people/
│   ├── food/
│   ├── scenery/
│   ├── receipts/
│   └── other/
├── thumbnails/                # 缩略图（快速预览）
│   ├── pets/
│   ├── people/
│   └── ...
└── index.json                 # 全局索引文件
```

## 快速使用

### 保存图片

```bash
python scripts/save_image.py <image_path> \
  --category pets \
  --tags "包子,白色,长毛" \
  --description "包子坐在地上"
```

### 查找图片

```bash
# 按标签查找
python scripts/search_image.py --tags "包子"

# 按类别查找
python scripts/search_image.py --category pets

# 按日期查找
python scripts/search_image.py --date 2026-03-19

# 按关键词查找（搜索 description 和 tags）
python scripts/search_image.py --keyword "白色"
```

### 浏览摘要

```bash
python scripts/list_images.py --category pets
python scripts/list_images.py --tags "包子"
```

## 索引格式（index.json）

每条记录包含：

```json
{
  "id": "baozi-2026-03-19-001",
  "path": "media/images/pets/baozi-2026-03-19-001.jpg",
  "thumbnail": "media/thumbnails/pets/baozi-2026-03-19-001.jpg",
  "category": "pets",
  "tags": ["包子", "白色", "长毛"],
  "description": "包子坐在地上",
  "saved_at": "2026-03-19T22:33:00+08:00",
  "source": "feishu",
  "size_bytes": 88688,
  "width": 1080,
  "height": 1440
}
```

## 分类说明

| 类别 | 用途 |
|------|------|
| pets | 宠物照片 |
| people | 人物照片 |
| food | 美食/食物 |
| scenery | 风景/地点 |
| receipts | 小票/账单 |
| other | 未分类 |

## 设计原则

- **原图不动**：保存时不做有损压缩，原图完整保留
- **缩略图预览**：生成 300x300 缩略图用于快速浏览
- **索引优先**：查找时只读索引文件，不遍历磁盘
- **标签灵活**：一张图可有多个标签，标签可随时增删
