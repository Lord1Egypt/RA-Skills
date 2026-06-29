---
name: jd-link-converter
description: |
  将京东移动端分享短链接（3.cn/u.jd.com）或移动端商品链接（item.m.jd.com）转换为PC端纯净商品链接（item.jd.com）。
  当用户需要解析京东短链接、转换移动端链接为PC端链接、或批量处理京东商品链接时使用此技能。
  触发场景包括用户粘贴京东分享链接、提到"京东链接转换"、"短链接转长链接"、"京东PC链接"、"3.cn解析"等。
author: mousounikki
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# 京东链接转换工具

我是京东链接转换工具，负责将移动端分享链接自动转换为PC端纯净商品链接。

## 触发条件

当用户消息中出现以下任一模式时触发本技能：

| 模式 | 示例 |
|------|------|
| 3.cn 短链接 | `https://3.cn/2RKwn3-g` |
| u.jd.com 短链接 | `https://u.jd.com/abc123` |
| 移动端商品页 | `https://item.m.jd.com/product/100198170140.html` |
| 关键词触发 | 「京东链接转换」「短链接转长链接」「3.cn解析」「京东PC链接」 |

## 执行协议

### Step 1: URL 分类与提取

从用户消息中提取所有匹配的 URL，按以下规则分类：

| 类型 | 识别规则 | 处理方式 |
|------|----------|----------|
| 3.cn 短链接 | 匹配 `https?://3\.cn/` | 需 HTTP 解析 |
| u.jd.com 短链接 | 匹配 `https?://u\.jd\.com/` | 需 HTTP 解析 |
| 移动端商品页 | 匹配 `item\.m\.jd\.com` | 直接提取 ID |
| PC端商品页(含参数) | 匹配 `item\.jd\.com/\d+` | 去参数 |
| 纯商品 ID | 6-12 位纯数字 | 直接拼接 |

### Step 2: 链接解析

**短链接（3.cn / u.jd.com）：**

执行脚本进行 HTTP 解析：
```bash
python3 {baseDir}/scripts/jd_link_converter.py "<short_url>"
```

脚本会模拟京东 App User-Agent 跟踪 302 重定向，获取实际商品页面 URL。

**重要：** 3.cn 短链接必须使用 `jdapp;iPhone;...` 的 UA 才能正确跳转到商品页，普通浏览器 UA 会被重定向到京东首页。

也可使用 WebFetch 工具手动跟踪重定向，但需注意 UA 问题。

**移动端 / PC端链接：**

无需 HTTP 请求，直接用正则提取商品 ID。

### Step 3: 生成 PC 端链接

从 URL 中提取 6-12 位数字商品 ID，拼接为：

```
https://item.jd.com/{id}.html
```

### Step 4: 输出结果

对每个输入链接，输出结构化结果：

| 原始链接 | 类型 | 商品 ID | PC 端链接 |
|----------|------|---------|-----------|
| `https://3.cn/2RKwn3-g` | 短链接 | 100198170140 | `https://item.jd.com/100198170140.html` |

批量转换时，以表格形式输出所有结果。

## 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| 短链接解析超时 | 提示用户提供移动端长链接或商品 ID |
| 短链接已过期/失效 | 提示链接已失效，建议重新获取分享链接 |
| 非京东链接 | 跳过，不处理，提示用户确认链接是否正确 |
| 商品 ID 提取失败 | 提示 URL 格式异常，请检查链接完整性 |
| 网络不可用 | 使用内联正则从已知格式的 URL 中直接提取 ID（见下方内联方案） |
| 3.cn 重定向到首页 | 提示可能 UA 被拦截，建议直接提供 item.m.jd.com 链接 |

## 内联转换方案（无需脚本，Agent 可直接执行）

当脚本不可用或网络受限时，Agent 可直接使用以下正则提取商品 ID：

```python
import re

# 从各种京东 URL 格式中提取商品 ID
patterns = [
    r'item\.m\.jd\.com/product/(\d{6,12})\.html',
    r'item\.m\.jd\.com/(\d{6,12})\.html',
    r'item\.jd\.com/(\d{6,12})\.html',
    r'item\.jd\.com/(\d{6,12})',
]

def inline_extract(url: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
```

对于纯商品 ID（6-12 位数字），直接拼接：
```python
pc_url = f"https://item.jd.com/{product_id}.html"
```

## URL 格式速查

详细格式参考：`{baseDir}/references/url_formats.md`

### 快速参考

| 输入格式 | 转换结果 |
|----------|----------|
| `https://3.cn/xxx` | HTTP 解析 → 提取 ID → `item.jd.com/{id}.html` |
| `https://u.jd.com/xxx` | HTTP 解析 → 提取 ID → `item.jd.com/{id}.html` |
| `https://item.m.jd.com/product/{id}.html?utm_*=...` | 去参数 → `item.jd.com/{id}.html` |
| `https://item.jd.com/{id}.html?cu=true` | 去参数 → `item.jd.com/{id}.html` |
| `100198170140`（纯 ID） | 直接拼接 → `item.jd.com/{id}.html` |
