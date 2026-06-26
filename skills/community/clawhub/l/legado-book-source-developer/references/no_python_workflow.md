# 无 Python 环境工作流（MCP 工具优先）

当系统没有 Python 环境时，优先检查宿主系统已配置的 MCP 工具，利用它们完成书源开发全流程。

## Step 0: 检查可用 MCP 工具

先扫描当前环境有哪些 MCP 工具可用：

```
# 检查是否有文件系统 MCP
list_files / read_file / write_file

# 检查是否有浏览器 MCP  
browser_navigate / browser_snapshot / browser_screenshot

# 检查是否有代码执行 MCP
execute_command / run_code / run_python

# 检查是否有 HTTP/网络 MCP
http_get / fetch / curl
```

**根据可用工具选择对应方案。**

## 方案 A: 有浏览器 MCP

浏览器 MCP 是最佳选择，能获取真实渲染后的页面。

### 获取页面源码
```
# 打开搜索页
browser_navigate(url="https://example.com/search?q=测试")

# 获取页面快照（含HTML结构）
browser_snapshot()

# 截图辅助分析
browser_screenshot()
```

### 分析搜索接口
```
# 打开开发者面板方式：先导航到搜索页，执行搜索，查看网络请求
browser_navigate(url="https://example.com")
# 触发搜索操作后
browser_snapshot()  # 查看实际发出的请求
```

### 获取多页面
```
browser_navigate(url="https://example.com/book/123")      # 详情页
browser_navigate(url="https://example.com/book/123/toc")  # 目录页
browser_navigate(url="https://example.com/book/123/ch/1") # 内容页
```

## 方案 B: 有 HTTP/网络 MCP

直接用网络工具获取源码。

### 获取 HTML
```
http_get(url="https://example.com/search?q=测试")
http_get(url="https://example.com/book/123")
http_get(url="https://example.com/book/123/toc")
http_get(url="https://example.com/book/123/ch/1")
```

### POST 请求（搜索接口）
```
http_post(
    url="https://example.com/api/search",
    headers={"Content-Type": "application/json"},
    body='{"keyword":"测试","page":1}'
)
```

### 获取 JS 文件
```
http_get(url="https://example.com/static/search.js")
```

## 方案 C: 有代码执行 MCP

用代码执行环境运行分析脚本。

### 直接运行 tools/ 下的脚本
```
# 如果 MCP 支持执行 shell 命令
execute_command("cd skills/legado-book-source-developer/tools && python3 analyze_url.py https://example.com")

# 或 bash 版（无需 Python）
execute_command("cd skills/legado-book-source-developer/tools && bash analyze_url.sh https://example.com")
```

### 内联代码分析
```
run_python(code="""
import requests
from bs4 import BeautifulSoup
r = requests.get('https://example.com/search?q=test')
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.title)
for item in soup.select('.book-list .item'):
    print(item.select_one('.title').text)
""")
```

## 方案 D: 有文件系统 MCP + 浏览器

组合使用：浏览器抓取 → 文件系统存储 → 代码执行分析。

```
# 1. 浏览器获取页面
browser_navigate(url="https://example.com/search?q=测试")
html = browser_snapshot()

# 2. 存储到文件
write_file(path="search_result.html", content=html)

# 3. 如果有代码执行，运行分析
execute_command("grep -o 'class=\"[^\"]*\"' search_result.html | sort -u | head -20")
```

## 通用流程（不论哪种方案）

### 1. 获取 5 个关键页面
- 首页
- 搜索结果页（含关键词）
- 书籍详情页
- 目录页
- 章节内容页

### 2. 识别搜索接口
- URL 模式（GET/POST）
- 参数名和格式
- 是否需要签名/加密

### 3. 推断 CSS 选择器
从获取的 HTML 中找：
- 列表容器（多个重复子元素）
- 书名、作者、封面、链接的位置
- 内容区域的定位

### 4. 参考知识库
```
search_knowledge("CSS选择器格式 提取类型 @text @href @src")
get_real_book_source_examples(limit=5)
get_book_source_templates(limit=3)
```

### 5. 验证并创建书源
在宿主系统中导入 JSON 测试，或直接调用：
```
edit_book_source(complete_source='[{"bookSourceName":"...", ...}]')
```

## 注意事项

- **编码问题**: 浏览器 MCP 自动处理编码；HTTP MCP 需检查 Content-Type
- **动态页面**: 如果页面内容由 JS 渲染，必须用浏览器 MCP（HTTP MCP 只拿到模板）
- **反爬虫**: 浏览器 MCP 天然绕过大部分反爬；HTTP MCP 需手动设 Headers/Cookie
- **大文件**: 设置合理的截断限制，避免上下文溢出
