---
name: jike-book-isbn-query
description: ISBN图书查询。输入 ISBN-10 或 ISBN-13，查询书名、作者、译者、出版社、出版日期、页数、定价、装帧、丛书和封面等信息。适用场景：用户说“查一下 9787115428028 是什么书”“这个 ISBN 对应哪本书”“查询图书出版信息”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"📚","requires":{"bins":["python3"],"env":["JIKE_BOOK_ISBN_QUERY_KEY"]},"primaryEnv":"JIKE_BOOK_ISBN_QUERY_KEY"}}
---

# ISBN图书查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

输入 ISBN 编号，查询：**书名、作者、译者、出版社、出版日期、页数、定价、装帧、丛书、封面**。

## 前置配置

```bash
export JIKE_BOOK_ISBN_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

```bash
python3 scripts/book_isbn_query.py 9787115428028
python3 scripts/book_isbn_query.py 978-7-115-42802-8
python3 scripts/book_isbn_query.py 9787115428028 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/book/isbn/query?isbn=9787115428028&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取 ISBN-10 或 ISBN-13。
2. 清理横杠和空格，校验基础格式。
3. 执行 `python3 scripts/book_isbn_query.py <ISBN>`。
4. 返回图书名称、作者、出版社、出版日期、定价、页数和封面。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `isbn` | ISBN 原始编号 |
| `isbn10` | ISBN-10 |
| `isbn13` | ISBN-13 |
| `title` | 书名 |
| `author` | 作者 |
| `translator` | 译者 |
| `publisher` | 出版社 |
| `publish_date` | 出版日期 |
| `page_count` | 页数 |
| `price` | 定价 |
| `binding` | 装帧 |
| `series` | 丛书 |
| `cover` | 封面 |

## 脚本位置

`scripts/book_isbn_query.py`
