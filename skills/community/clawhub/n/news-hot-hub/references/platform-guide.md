# 平台接入指南

## 目录

1. [概述](#概述)
2. [脚本规范](#脚本规范)
3. [接入步骤](#接入步骤)
4. [平台现状](#平台现状)
5. [认证说明](#认证说明)
6. [常见问题](#常见问题)

---

## 概述

本文档指导如何为 news Hot Hub 接入新平台或实现已有平台的真实抓取逻辑。每个平台是一个独立的 Python CLI 脚本，放在 `scripts/` 目录下。

## 脚本规范

### 文件命名

- 使用平台英文名小写，如 `zhihu.py`, `weibo.py`
- 数字开头的平台名加前缀，如 36氪 → `kr36.py`

### CLI 接口约定

每个脚本必须支持以下基本结构：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""<平台名>数据获取 — <Platform> Fetcher"""

import argparse
import json
import sys
from datetime import datetime


def _now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _output(data_type, data):
    result = {
        "type": data_type,
        "timestamp": _now(),
        "count": len(data),
        "data": data,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def fetch_hot_search(limit=50):
    """获取热搜/热榜数据"""
    items = []
    # ... 实际抓取逻辑 ...
    return items


def main():
    parser = argparse.ArgumentParser(description="<平台名>数据获取")
    sub = parser.add_subparsers(dest="command")

    p_hs = sub.add_parser("hot-search", help="获取热搜榜")
    p_hs.add_argument("--limit", type=int, default=50, help="结果数量")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "hot-search":
        data = fetch_hot_search(limit=args.limit)
        _output("hot_search", data)


if __name__ == "__main__":
    main()
```

### 输出规范

- **stdout**：仅输出 JSON 数据
- **stderr**：错误信息和警告
- **退出码**：0 = 成功，1 = 失败
- **编码**：UTF-8，`ensure_ascii=False`

### 每条数据必须包含的字段

| 字段    | 类型   | 说明                         |
| ------- | ------ | ---------------------------- |
| `title` | string | 标题（用于跨平台对比和展示） |
| `url`   | string | 原始链接                     |

其他字段按平台特性自由添加（如 `heat`, `author`, `rank` 等）。

---

## 接入步骤

### 1. 创建脚本

在 `scripts/` 下新建 `<platform>.py`，按上述模板实现。

### 2. 注册平台

编辑 `scripts/hub.py`，在 `PLATFORMS` 字典中添加：

```python
"newplatform": {
    "name": "新平台",
    "script": "newplatform.py",
    "default_cmd": "hot-search",
    "commands": ["hot-search"],
},
```

### 3. 添加别名

在 `ALIASES` 中添加缩写：

```python
"np": "newplatform", "新平台": "newplatform",
```

### 4. 更新文档

- `references/data-schema.md`：添加新平台的数据格式
- `references/architecture.md`：更新平台注册表说明
- `SKILL.md`：在触发词中添加新平台关键词

### 5. 测试

```bash
# 单独测试脚本
python scripts/newplatform.py hot-search --limit 5

# 通过 hub 调度测试
python scripts/hub.py fetch newplatform --limit 5

# 检查状态
python scripts/hub.py status
```

---

## 平台现状

| 平台     | 脚本         | 状态     | 认证               | 说明                                             |
| -------- | ------------ | -------- | ------------------ | ------------------------------------------------ |
| 知乎     | `zhihu.py`   | ✅ 已实现 | Cookie（部分接口） | 支持 hot-search/hot-question/hot-video/topic/all |
| AIBase   | `aibase.py`  | ✅ 已实现 | 无需认证           | 支持 hot-search/news/daily/all，附带正文内容     |
| 微博     | `weibo.py`   | ⏳ 脚手架 | —                  | V2 待实现                                        |
| 今日头条 | `toutiao.py` | ⏳ 脚手架 | —                  | V2 待实现                                        |
| V2EX     | `v2ex.py`    | ⏳ 脚手架 | —                  | V2 待实现                                        |
| 36氪     | `kr36.py`    | ⏳ 脚手架 | —                  | V2 待实现                                        |

---

## 认证说明

### AIBase

AIBase 所有命令均无需认证，直接访问公开页面即可。

### 知乎

知乎的 `hot-search` 命令无需认证即可使用。以下命令需要设置 `ZHIHU_COOKIES` 环境变量：

- `hot-question`（热门话题）
- `hot-video`（热门视频）
- `topic`（关键词搜索）

获取 Cookie 方法：

1. 浏览器登录知乎
2. 打开 DevTools → Network → 任意 zhihu.com 请求
3. 复制 Request Headers 中的 `Cookie` 值
4. 设置环境变量：`export ZHIHU_COOKIES="key1=val1; key2=val2"`

### 其他平台

V2 实现时根据各平台 API 特性决定认证方式。优先使用无认证的公开接口。

---

## 常见问题

### Q: 脚手架脚本返回 not_implemented 怎么办？

这是预期行为。V1 版本只有知乎实现了真实抓取，其他平台是占位脚手架。`hub.py` 会正确识别并在结果中标注失败原因。

### Q: 如何判断平台脚本是否可用？

```bash
python scripts/hub.py status
```

### Q: 新增平台需要修改 hub.py 的调度逻辑吗？

不需要。只需在 `PLATFORMS` 注册表中添加条目，调度逻辑自动适配。

### Q: 脚本超时怎么办？

hub.py 默认 30 秒超时。如果平台 API 响应慢，可以在平台脚本内部实现重试逻辑（参考 zhihu.py 的 `Retry` 配置）。
