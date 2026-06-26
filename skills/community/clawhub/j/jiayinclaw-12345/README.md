# 网页内容提取器

一个简单易用的网页内容提取工具，可以从任意网页中提取标题、正文、图片和链接信息。

## 功能特性

- 自动提取网页标题和meta描述
- 提取正文内容并自动清理
- 提取所有图片链接
- 提取所有外链
- 输出结构化JSON数据
- 支持命令行参数配置
- 处理相对和绝对URL

## 安装依赖

```bash
pip install requests beautifulsoup4
```

## 使用方法

### 基本用法

```bash
python extractor.py https://example.com
```

### 高级选项

```bash
# 仅文本输出
python extractor.py https://example.com --format text

# 不提取图片
python extractor.py https://example.com --no-images

# 不提取链接
python extractor.py https://example.com --no-links
```

### 与OpenClaw集成

在OpenClaw中安装后，可以直接用自然语言调用：

```
用户：帮我提取 https://news.example.com/article/123 的内容
技能：自动提取并返回结构化数据
```

## 输出格式

```json
{
  "url": "https://example.com",
  "title": "页面标题",
  "meta_description": "页面描述",
  "content": "正文内容...",
  "images": ["图片1", "图片2"],
  "links": [{"url": "链接1", "text": "链接文本"}],
  "extracted_at": "2024-01-01T12:00:00",
  "stats": {
    "images_count": 5,
    "links_count": 20,
    "content_length": 1500
  }
}
```

## 适用场景

- 内容聚合和数据采集
- 文章存档和备份
- 内容分析和处理
- 自动化工作流程
- AI代理的信息提取任务

## 注意事项

1. 请确保有网络连接
2. 部分网站可能有反爬机制
3. 请遵守网站的robots.txt规则
4. 提取的内容仅供个人学习使用

## 技术栈

- Python 3.6+
- BeautifulSoup4 - HTML解析
- requests - HTTP请求
- re - 正则表达式处理

## 许可证

MIT License
