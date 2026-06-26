# 快速搜索地址提取工具使用指南

## 概述

`quick_search_url_extractor.py` 是基于"快速写源"订阅源核心技术的智能工具，能够自动识别和生成网站的搜索地址。

## 功能特性

### 1. 智能表单识别
- 自动扫描页面中的所有`<form>`表单
- 提取表单的`action`、`method`属性
- 分析所有输入字段

### 2. 多策略搜索字段识别

工具使用四种策略来识别搜索关键词字段：

**策略1：单一字段**
```javascript
if (names.length == 1) {
    value = "{{key}}"
}
```
如果表单只有一个输入字段，自动识别为搜索字段。

**策略2：常见字段名**
```javascript
['q', 'wd', 'query', 'search', 'key', 'keyword', 'k', 's']
```
匹配这些常见的搜索字段名。

**策略3：字段名包含关键词**
```javascript
if ('search' in name || 'key' in name) {
    return name
}
```
识别字段名中包含"search"或"key"的字段。

**策略4：文本类型且无默认值**
```javascript
if (field['type'] == 'text' && !field['value']) {
    return field['name']
}
```
识别文本类型且没有默认值的字段。

### 3. 自动生成搜索地址

**GET请求：**
```
/search?q={{key}}
```

**POST请求：**
```
/search,{"method":"POST","body":"key={{key}}&page=1"}
```

**带编码配置：**
```
/search,{"method":"POST","body":"key={{key}}","charset":"GBK"}
```

### 4. 发现规则自动提取
自动识别网站上的分类、排行、推荐等链接：
```javascript
['sort', 'list', 'rank', 'tag', 'shuku', 'fenlei', 'Soft', 'allvisit', 'paihang', 'quanben']
```

### 5. 书源草稿生成
自动生成包含OG元数据的书源框架：
```json
{
  "bookSourceName": "快速生成的书源_1773468883",
  "bookSourceUrl": "https://example.com",
  "searchUrl": "/search?q={{key}}",
  "ruleBookInfo": {
    "name": "[property=\"og:novel:book_name\"]@content",
    "author": "[property=\"og:novel:author\"]@content",
    "coverUrl": "[property=\"og:image\"]@content",
    "intro": "[property=\"og:description\"]@content"
  }
}
```

## 使用方法

### 基本用法

```bash
# 进入tools目录
cd tools

# 运行工具
python quick_search_url_extractor.py https://www.example.com
```

### 示例输出

```
======================================================================
快速搜索地址提取工具
======================================================================
目标网站: https://www.example.com

正在获取: https://www.example.com
✓ 状态码: 200
✓ 编码: UTF-8
✓ 大小: 45231 字符

找到 2 个表单

--- 表单 1 ---
Action: https://www.example.com/search
Method: POST
字段数: 3
  - q (type=text, value=, placeholder=请输入关键词)
  - type (type=hidden, value=novel)
  - page (type=hidden, value=1)

✓ 识别为搜索表单!
✓ 搜索字段: q
✓ 搜索地址: https://www.example.com/search,{"method":"POST","body":"q={{key}}&type=novel&page=1"}

发现 15 个潜在的发现规则链接

======================================================================
分析结果
======================================================================

✓ 成功识别 1 个搜索表单

表单 1:
  搜索字段: q
  搜索地址: https://www.example.com/search,{"method":"POST","body":"q={{key}}&type=novel&page=1"}

✓ 发现规则 (5 个):
  - 玄幻小说: /xuanhuan
  - 都市小说: /dushi
  - 科幻小说: /kehuan
  - 排行榜: /rank
  - 全本小说: /quanben

✓ 书源草稿已生成
  草稿文件: book_source_draft_1773468883.json

⚠️  注意: 书源草稿需要您补充以下内容:
  1. ruleSearch 的所有规则
  2. ruleToc 的所有规则
  3. ruleContent 的所有规则

======================================================================
分析完成!
======================================================================
```

## 高级用法

### 自定义请求头

如果网站需要特定的请求头，可以修改脚本中的 `headers` 参数：

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; wv)...',
    'Referer': 'https://www.example.com',
    'X-Requested-With': 'XMLHttpRequest'
}

extractor = QuickSearchUrlExtractor(url, headers=headers)
```

### Cloudflare过盾

如果检测到Cloudflare验证，可以使用内置浏览器：

```python
# 修改 fetch_page 方法
if webSrc.match(/Just a moment/){
    try {
        webSrc = java.startBrowserAwait(url, "验证", false).body();
    } catch(e) {
        webSrc = java.startBrowserAwait(url, "验证").body();
    }
}
```

### 处理动态加载

如果网站使用JavaScript动态渲染，需要：

1. 使用浏览器开发者工具分析网络请求
2. 提取实际的API接口
3. 手动配置搜索地址

## 输出文件

工具会生成以下文件：

```
tools/
├── book_source_draft_时间戳.json    # 书源草稿
└── analysis_report_时间戳.json      # 分析报告（如果扩展）
```

## 书源草稿说明

生成的书源草稿包含：

1. **基础信息**
   - 书源名称
   - 书源URL
   - 搜索地址（自动生成）

2. **OG元数据规则**（如果页面有）
   - 书名：`[property="og:novel:book_name"]@content`
   - 作者：`[property="og:novel:author"]@content`
   - 封面：`[property="og:image"]@content`
   - 简介：`[property="og:description"]@content`

3. **发现规则**（如果检测到）
   - 分类链接
   - 排行榜链接
   - 推荐链接

## 需要补充的内容

书源草稿生成后，您需要补充：

### 1. 搜索规则
```json
"ruleSearch": {
  "bookList": ".book-list .item",      // 需要补充
  "name": ".title@text",                // 需要补充
  "author": ".author@text",             // 需要补充
  "kind": ".category@text",             // 需要补充
  "lastChapter": ".last-chapter@text",  // 需要补充
  "bookUrl": "a@href",                  // 需要补充
  "coverUrl": "img@src"                 // 需要补充
}
```

### 2. 目录规则
```json
"ruleToc": {
  "chapterList": "#chapter-list li",    // 需要补充
  "chapterName": "a@text",              // 需要补充
  "chapterUrl": "a@href",               // 需要补充
  "nextTocUrl": ""                      // 需要补充
}
```

### 3. 内容规则
```json
"ruleContent": {
  "content": "#content@html",           // 需要补充
  "nextContentUrl": ""                  // 需要补充
}
```

## 常见问题

### Q1: 工具找不到搜索表单？

**可能原因：**
1. 网站使用AJAX动态加载
2. 搜索功能是纯JavaScript实现
3. 需要登录才能访问

**解决方法：**
1. 使用浏览器开发者工具查看Network请求
2. 手动分析JavaScript代码
3. 查看页面的API接口

### Q2: 识别的搜索字段不对？

**可能原因：**
1. 表单有多个字段
2. 字段名不符合常见模式
3. 有隐藏字段干扰

**解决方法：**
1. 手动查看表单结构
2. 修改脚本中的识别逻辑
3. 使用浏览器验证

### Q3: POST请求的body不正确？

**可能原因：**
1. 字段值获取错误
2. 有额外的参数
3. Content-Type不对

**解决方法：**
1. 使用浏览器开发者工具复制cURL
2. 对比生成的参数
3. 手动调整body

### Q4: 生成的书源无法搜索？

**检查清单：**
- [ ] searchUrl是否正确
- [ ] 字段名是否正确
- [ ] 编码是否正确（GBK vs UTF-8）
- [ ] 是否需要特殊的请求头
- [ ] 搜索页HTML结构是否分析正确

## 与quick_analyze.py的区别

| 特性 | quick_analyze.py | quick_search_url_extractor.py |
|------|------------------|-------------------------------|
| 主要功能 | 全面分析网站结构 | 快速获取搜索地址 |
| 表单识别 | 基础识别 | 智能多策略识别 |
| 发现规则 | 不支持 | 自动提取 |
| 书源草稿 | 完整草稿 | 框架草稿 |
| 适用场景 | 首次分析 | 快速开始 |

## 最佳实践

### 1. 先用此工具快速开始
```bash
python quick_search_url_extractor.py https://example.com
```

### 2. 检查生成的搜索地址
- 使用浏览器测试搜索地址
- 确认参数是否正确
- 验证返回的HTML

### 3. 补充完整的书源规则
- 使用quick_analyze.py获取更多细节
- 手动分析HTML结构
- 编写完整的CSS选择器

### 4. 验证书源
```bash
python validate_book_source.py book_source_draft_xxx.json
```

## 技术原理

### 表单识别算法

```python
# 1. 查找所有表单
forms = soup.find_all('form')

# 2. 分析每个表单
for form in forms:
    action = form.get('action', '')
    method = form.get('method', 'GET').upper()
    inputs = form.find_all(['input', 'select', 'textarea'])
    
    # 3. 智能识别搜索字段
    search_field = identify_search_field(inputs)
    
    # 4. 生成搜索地址
    if search_field:
        search_url = generate_search_url(action, method, inputs, search_field)
```

### 搜索字段识别策略

```python
def identify_search_field(fields):
    # 策略1: 单字段
    if len(fields) == 1:
        return fields[0]['name']
    
    # 策略2: 常见字段名
    for field in fields:
        if field['name'] in ['q', 'wd', 'query', 'search', 'key']:
            return field['name']
    
    # 策略3: 字段名包含关键词
    for field in fields:
        if 'search' in field['name'].lower():
            return field['name']
    
    # 策略4: 文本类型
    for field in fields:
        if field['type'] == 'text' and not field['value']:
            return field['name']
    
    return None
```

## 更新日志

### v1.0 (2026-03-15)
- 初始版本
- 实现基础表单识别
- 智能搜索字段识别
- 自动生成搜索地址
- 发现规则提取
- 书源草稿生成

## 许可证

本工具遵循与Legado书源开发技能相同的许可证。

## 参考资源

- [快速写源订阅源原理分析](../references/快速写源订阅源原理分析.md)
- [Legado官方文档](https://legado.yuewen.com/)
- [书源开发指南](../QUICKSTART.md)
