# MiniMax Tools 使用示例

## 网络搜索示例

### 基础搜索

```python
from minimax_tools import web_search

# 搜索 Python 教程
result = web_search("Python 教程")
for item in result['results']:
    print(f"{item['title']}: {item['url']}")
```

### 搜索并获取摘要

```python
result = web_search("OpenAI GPT-4 发布")
print(f"找到 {len(result['results'])} 条结果")
print(f"相关搜索: {result.get('related_searches', [])}")
```

## 图片理解示例

### HTTP URL 图片

```python
from minimax_tools import understand_image

# 分析网页图片
result = understand_image(
    prompt="描述这张图片的内容",
    image_url="https://example.com/photo.jpg"
)
print(result)
```

### 本地文件

```python
# 分析本地图片
result = understand_image(
    prompt="这张截图里有什么错误？",
    image_url="/home/user/screenshots/error.png"
)
```

### 产品分析

```python
# 产品图片分析
result = understand_image(
    prompt="分析这个产品的设计和功能特点",
    image_url="https://example.com/product.jpg"
)
```

### 多轮对话式分析

```python
# 连续提问
first_result = understand_image(
    prompt="这张图表展示什么数据？",
    image_url="https://example.com/chart.png"
)

follow_up_result = understand_image(
    prompt="基于上面的图表，预测未来趋势",
    image_url="https://example.com/chart.png"
)
```

## 命令行使用

### 搜索

```bash
# 基本搜索
python -m minimax_tools.web_search "搜索词"

# JSON 输出
python -m minimax_tools.web_search "搜索词" --json
```

### 图片理解

```bash
# 基本分析
python -m minimax_tools.understand_image "描述这张图" "https://example.com/img.jpg"

# 本地文件
python -m minimax_tools.understand_image "这是什么" "/path/to/image.png"

# JSON 输出
python -m minimax_tools.understand_image "分析内容" "https://..." --json
```

## 错误处理

```python
from minimax_tools import web_search, understand_image

try:
    result = web_search("query")
except ValueError as e:
    print(f"参数错误: {e}")
except ConnectionError as e:
    print(f"连接失败: {e}")
except TimeoutError:
    print("请求超时，请重试")
except NotImplementedError as e:
    print(f"功能暂时不可用: {e}")
```
