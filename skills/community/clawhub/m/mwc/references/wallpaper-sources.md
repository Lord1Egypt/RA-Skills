# 壁纸源配置

## 优先级

| 优先级 | 源            | 需要 Key   | 质量 | 说明                     |
| ------ | ------------- | ---------- | ---- | ------------------------ |
| 1      | Bing 每日壁纸 | 否         | 高   | 每日更新，4K 高清        |
| 2      | Unsplash      | 否（可选） | 高   | ID 池直连 / API 实时搜索 |
| 3      | Picsum        | 否         | 中   | 兜底方案                 |

## Bing 每日壁纸

**免费**，不需要 API Key。

```python
# API 端点
BING_API = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8"

# 图片 URL 拼接
# 返回 JSON 中 images[0].url 为相对路径
# 完整 URL: https://cn.bing.com + url
```

### 参数说明

- `format=js` — 返回 JSON 格式
- `idx=0` — 0=今天，1=昨天，最大7
- `n=8` — 返回图片数量（1-8）
- `mkt=zh-CN` — 市场区域

### 响应示例

```json
{
  "images": [
    {
      "url": "/th?id=OHR.Example_ZH-CN1234_1920x1080.jpg",
      "title": "壁纸标题",
      "copyright": "版权信息"
    }
  ]
}
```

## Unsplash（双模式）

### 模式 1：ID 池直连（默认，无需 API Key）

内置高质量图片 ID 池，按分类组织：

```python
# 分类 ID 池
UNSPLASH_PHOTO_IDS = {
    "nature": ["1470071459604-3b5ec3a7fe05", ...],
    "mountain": ["1506905925346-21bda4d32df4", ...],
    "forest": [...],
    "ocean": [...],
    "city": [...],
    "space": [...]
}

# URL 构造
url = f"https://images.unsplash.com/photo-{photo_id}?w=3840&h=2160&fit=crop&q=85"
```

**优点：**

- 无需配置，开箱即用
- 稳定可靠，无 API 限制

**缺点：**

- 只能在预设 ID 中随机
- 无法自由搜索关键词

### 模式 2：API 实时搜索（需配置）

配置环境变量后启用自由搜索：

```bash
export UNSPLASH_ACCESS_KEY="your_access_key"
```

**API 端点**

```python
UNSPLAPH_RANDOM = "https://api.unsplash.com/photos/random"

headers = {
    "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
}

params = {
    "query": "Shanghai rain",
    "orientation": "landscape",
    "content_filter": "high"
}
```

**使用示例**

```bash
# 自由关键词搜索
uv run scripts/change.py --query "Shanghai rain night"
```

### 免费额度

- 50 次/小时（Demo）
- 5000 次/小时（Production，需申请）

## Picsum（兜底）

**免费**，无需配置。

```python
# 随机图片
PICSUM_URL = "https://picsum.photos/3840/2160?random={seed}"

# 指定图片 ID
PICSUM_ID_URL = "https://picsum.photos/id/{id}/3840/2160"
```

### 参数

- `?grayscale` — 灰度
- `?blur={1-10}` — 模糊程度

## 在代码中配置

编辑 `scripts/change.py` 中的 `WALLPAPER_SOURCES`：

```python
WALLPAPER_SOURCES = {
    "bing": {
        "api": "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1",
        "base_url": "https://cn.bing.com",
        "priority": 1
    },
    "unsplash": {
        "api": "https://api.unsplash.com/photos/random",
        "requires_key": True,
        "priority": 2
    },
    "picsum": {
        "url": "https://picsum.photos/3840/2160?random={seed}",
        "priority": 3
    }
}
```

## 命令行参数

### 新增功能

```bash
# 自由关键词搜索（需要配置 UNSPLASH_ACCESS_KEY）
uv run scripts/change.py --query "Shanghai rain"

# 从 URL 直接设置
uv run scripts/change.py --url "https://example.com/wallpaper.jpg"

# 从本地文件设置
uv run scripts/change.py --file ~/Pictures/my-wallpaper.jpg
```

### 完整参数列表

```bash
--ask-rating      # 设置后询问评分
--category NAME   # 壁纸分类（nature/mountain/forest/ocean/city/space）
--color-tone TONE # 色调（dark/bright/warm/cool）
--query TEXT      # 自由关键词搜索
--source SOURCE   # 指定图片源（bing/unsplash/picsum）
--url URL         # 直接从 URL 设置
--file PATH       # 从本地文件设置
--download-only   # 仅下载不设置
--count N         # 下载数量（与 --download-only 配合）
```
