# API参考文档

## 命令行接口

### 基本语法

```bash
python extractor.py <URL> [OPTIONS]
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| URL | 字符串 | 是 | 要提取的网页地址 |
| --format | 字符串 | 否 | 输出格式：json（默认）或 text |
| --no-images | 标志 | 否 | 不提取图片链接 |
| --no-links | 标志 | 否 | 不提取外链 |

## 函数接口

### validate_url(url)

验证URL格式是否合法。

**参数**：

- url (str)：待验证的URL字符串

**返回值**：

- bool：URL格式合法返回True，否则返回False

**示例**：

```python
if validate_url("https://example.com"):
    print("URL合法")
```

### clean_text(text)

清理文本内容，移除多余空白。

**参数**：

- text (str)：原始文本

**返回值**：

- str：清理后的文本

### extract_content(html, base_url)

从HTML内容中提取结构化信息。

**参数**：

- html (str)：网页HTML源码
- base_url (str)：网页基础URL

**返回值**：

- dict：包含提取结果的字典

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| url | str | 原始URL |
| title | str | 网页标题 |
| meta_description | str | meta描述 |
| content | str | 正文内容 |
| images | list | 图片链接列表 |
| links | list | 外链列表 |
| extracted_at | str | 提取时间 |
| stats | dict | 统计信息 |

### fetch_url(url)

获取网页内容。

**参数**：

- url (str)：目标URL

**返回值**：

- str：网页HTML内容

**异常**：

- requests.RequestException：网络请求异常

## 输出格式详解

### JSON输出

```json
{
  "url": "https://example.com",
  "title": "页面标题",
  "meta_description": "页面描述，最多200字符",
  "content": "正文内容，自动清理，最多5000字符",
  "images": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.png"
  ],
  "links": [
    {
      "url": "https://other-site.com",
      "text": "链接文本，最多100字符"
    }
  ],
  "extracted_at": "2024-01-01T12:00:00",
  "stats": {
    "images_count": 5,
    "links_count": 20,
    "content_length": 1500
  }
}
```

### 文本输出

文本格式仅输出核心内容，不包含详细链接列表，适合快速查看。

## 扩展开发

如需扩展功能，可以修改以下位置：

1. extract_content() - 添加新的提取规则
2. clean_text() - 调整文本清理逻辑
3. main() - 添加新的命令行参数

## 性能考虑

- 默认超时时间：10秒
- 图片数量限制：20个
- 链接数量限制：50个
- 正文长度限制：5000字符

## 安全注意事项

1. 不要提取恶意网站的链接
2. 注意处理重定向和相对URL
3. 敏感信息不要在URL中明文传递
