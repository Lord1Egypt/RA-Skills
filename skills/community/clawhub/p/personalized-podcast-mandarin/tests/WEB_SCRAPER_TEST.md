# Web Scraper 测试文档

## 测试目标
验证 `src/web_scraper.py` 能够正确提取网页正文内容。

## 测试方法

### 测试1：标准新闻文章
**操作步骤**:
1. 在下方 `test_urls` 列表中添加一个新闻文章URL
2. 运行测试: `pytest tests/test_web_scraper.py -v`

**预期结果**:
- 成功获取HTTP 200响应
- 提取的正文长度 > 500字符
- 不包含导航栏、广告等无关内容

**待输入测试URL**:
```python
test_urls = [
    # 请在此处添加您要测试的URL
    # 示例: "https://www.example.com/news/article",
]
```

---

### 测试2：技术博客文章
**操作步骤**:
1. 添加技术博客URL到测试列表
2. 运行测试

**预期结果**:
- 正确提取代码块和正文
- 保留段落结构

**待输入测试URL**:
```python
tech_blog_urls = [
    # 请在此处添加技术博客URL
]
```

---

### 测试3：错误处理
**操作步骤**:
1. 添加无效URL（如404页面）
2. 运行测试

**预期结果**:
- 抛出 `WebScraperError` 异常
- 异常信息包含失败原因

**待输入测试URL**:
```python
invalid_urls = [
    # 请在此处添加无效URL
    # 示例: "https://www.example.com/404-not-found",
]
```

---

## 运行测试命令

```bash
cd d:/vscode/AI-podcast/ai-podcast-dual-host
pytest tests/test_web_scraper.py -v
```

## 测试报告模板

测试完成后，请填写以下结果：

| URL | 状态 | 提取字数 | 备注 |
|-----|------|----------|------|
| | | | |
| | | | |
