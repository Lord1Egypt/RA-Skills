---
name: mp-weixin
description: 利用 Python 从微信公众号文章中提取元数据与正文内容。适用于用户需要解析微信文章链接（mp.weixin.qq.com）、提取文章信息（标题、作者、正文、发布时间、封面图），或将微信文章转换为结构化数据的情景。
homepage: https://mp.weixin.qq.com
metadata: { "openclaw": { "emoji": "📰", "requires": { "bins": ["python3"], "pip": ["beautifulsoup4", "requests", "lxml"] } } }
---

# 微信文章提取器 - Python 版本

使用 Python 提取微信公众号文章的标题、作者、内容、发布时间等元数据。

## ✅ 核心优势

相比 JavaScript 版本，Python 版本有以下优势：

- ✅ **无需 npm 依赖**：只用 Python 标准库 + 常用 pip 包
- ✅ **安装快速**：`pip install beautifulsoup4 requests lxml` 即可完成
- ✅ **绕过验证码**：使用微信 User-Agent，提高访问成功率
- ✅ **轻量级**：脚本仅 10KB，无复杂依赖
- ✅ **易维护**：Python 代码更易读易改

## 📦 依赖安装

```bash
pip install beautifulsoup4 requests lxml
```

或使用国内镜像加速：

```bash
pip install beautifulsoup4 requests lxml -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 🚀 使用方法

### 基本用法

```bash
python3 scripts/wechat_extractor.py <微信文章 URL>
```

### 示例

```bash
# 提取单篇文章
python3 scripts/wechat_extractor.py "https://mp.weixin.qq.com/s/xN1H5s66ruXY9s8aOd4Rcg"

# 在 Python 脚本中调用
from scripts.wechat_extractor import WeChatArticleExtractor

extractor = WeChatArticleExtractor()
result = extractor.extract('https://mp.weixin.qq.com/s/xxx')

if result['done']:
    print('标题:', result['data']['msg_title'])
    print('作者:', result['data']['msg_author'])
    print('内容:', result['data']['msg_content'][:500])
```

## 📊 输出数据说明

### 成功响应

```json
{
  "done": true,
  "code": 0,
  "data": {
    // 文章信息
    "msg_title": "文章标题",
    "msg_desc": "文章摘要",
    "msg_content": "<div>HTML 内容</div>",
    "msg_cover": "封面图 URL",
    "msg_author": "作者",
    "msg_type": "post",
    "msg_publish_time_str": "2026/03/14 10:30:00",
    "msg_link": "文章链接",
    
    // URL 参数
    "msg_mid": "mid 参数",
    "msg_idx": "idx 参数",
    "msg_sn": "sn 参数",
    "msg_biz": "__biz 参数",
    
    // 公众号信息
    "account_name": "公众号名称",
    "account_alias": "微信号",
    "account_id": "原始 ID",
    "account_description": "功能介绍",
    "account_avatar": "头像 URL",
    
    // 版权信息
    "msg_has_copyright": true
  }
}
```

### 错误响应

```json
{
  "done": false,
  "code": 1002,
  "msg": "请求超时"
}
```

## ⚠️ 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 1001 | 无法获取文章信息 | 检查 URL 是否正确 |
| 1002 | 请求失败/超时 | 检查网络连接，稍后重试 |
| 2006 | 需要验证码 | 微信反爬机制，稍后重试或使用已登录会话 |
| 2008 | 系统出错 | 查看错误详情，联系开发者 |

## 🎯 使用场景

✅ **适用场景**：
- 提取微信公众号文章内容
- 获取文章元数据（标题、作者、发布时间）
- 批量采集微信文章
- 监控特定公众号更新
- 微信文章归档

❌ **不适用场景**：
- 需要访问需要登录的付费文章
- 需要绕过微信验证码的批量采集
- 需要提取评论区内容

## 💡 最佳实践

### 1. 批量提取

```python
urls = [
    'https://mp.weixin.qq.com/s/xxx1',
    'https://mp.weixin.qq.com/s/xxx2',
    'https://mp.weixin.qq.com/s/xxx3',
]

extractor = WeChatArticleExtractor(timeout=30)

for url in urls:
    result = extractor.extract(url)
    if result['done']:
        print(f"✅ {result['data']['msg_title']}")
    else:
        print(f"❌ {url}: {result['msg']}")
    
    # 避免请求过快
    import time
    time.sleep(1)
```

### 2. 保存为 JSON

```python
import json

result = extractor.extract(url)

with open('article.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
```

### 3. 提取纯文本内容

```python
from bs4 import BeautifulSoup

result = extractor.extract(url)
html_content = result['data']['msg_content']

# 转为纯文本
soup = BeautifulSoup(html_content, 'lxml')
text_content = soup.get_text(separator='\n', strip=True)
print(text_content)
```

## 🔧 高级配置

### 自定义请求头

```python
extractor = WeChatArticleExtractor(timeout=60)
extractor.session.headers.update({
    'User-Agent': '自定义 User-Agent'
})
```

### 使用代理

```python
extractor = WeChatArticleExtractor(timeout=30)
extractor.session.proxies.update({
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
})
```

## 📝 注意事项

1. **验证码问题**：微信有反爬机制，频繁访问可能触发验证码，建议：
   - 控制请求频率（每秒不超过 1 次）
   - 使用固定的 User-Agent
   - 必要时使用已登录的 Cookie

2. **内容完整性**：部分文章可能包含视频、音频等多媒体内容，HTML 内容中会保留引用链接

3. **发布时间**：微信文章的发布时间可能无法精确提取，部分文章只能获取大致日期

4. **公众号信息**：公众号详细信息（微信号、原始 ID 等）需要从页面 JavaScript 中提取，可能不完整

## 🆚 与 JavaScript 版本对比

| 特性 | Python 版本 | JavaScript 版本 |
|------|-----------|---------------|
| 依赖 | pip (bs4, requests) | npm (cheerio, request-promise) |
| 安装速度 | 快（<30 秒） | 慢（可能超时） |
| 代码量 | ~300 行 | ~600 行 |
| 可维护性 | 高 | 中 |
| 验证码处理 | 使用微信 UA 绕过 | 需要额外配置 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 📚 示例输出

```
正在提取文章：https://mp.weixin.qq.com/s/xN1H5s66ruXY9s8aOd4Rcg
---
✅ 提取成功！

📰 文章标题：4B 参数实现理解、推理、生成、编辑一体化！InternVL-U 重磅开源
👤 作者：书生 Intern
📢 公众号：书生 Intern
⏰ 发布时间：2026/03/14 10:30:00
📝 文章摘要：重新定义统一多模态模型的 "效率 - 性能" 边界。
🖼️ 封面图：https://mmbiz.qpic.cn/mmbiz_jpg/...
📄 文章类型：post
🔗 文章链接：https://mp.weixin.qq.com/s/xN1H5s66ruXY9s8aOd4Rcg

📊 公众号信息:
  - 名称：书生 Intern
  - 微信号：未设置
  - 原始 ID: 未设置
  - 功能介绍：未设置

📝 文章内容长度：129134 字符

💾 详细数据已保存到：/tmp/wechat_article.json
```

## 🔗 相关链接

- [微信公众号平台](https://mp.weixin.qq.com)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests 文档](https://docs.python-requests.org/)

---

*Python 版本 by bozoyan · 2026-03-14 · 专为 CoPaw 优化* 📰✨
