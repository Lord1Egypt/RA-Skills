---
name: shorturl
description: 短网址生成服务。使用场景：(1) 用户需要缩短长网址 (2) 提供自定义短网址后缀 (3) 选择不同短网址域名。API: https://www.shorturl.bot/api/urls/shorturl
---

# ShortURL - 短网址生成

## 快速使用

用户只需提供长网址即可缩短：

```
请帮我缩短这个网址：https://example.com/very-long-url-path
```

使用内置脚本调用 API：

```bash
node shorturl/scripts/shorten.js <长网址> [域名] [自定义后缀]
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| url | 是 | - | 需要缩短的长网址 |
| domain | 否 | https://surl.bot/ | 短网址域名 |
| backHalf | 否 | 空 | 自定义短网址后半部分 |
| memberId | 否 | 空 | 会员ID |

## 可用域名

- `https://surl.bot/` (默认)
- `https://2s.gg/`
- `https://goes.cx/`
- `https://shrn.cc/`
- `https://gshrn.com/`
- `https://tvb.bz/`

## 输出格式

**默认**：只返回缩短后的网址

如需完整信息，可修改脚本添加 `--full` 参数。

## API 响应示例

```json
{
  "id": "abc123",
  "url": "https://example.com/very-long-url",
  "short": "https://surl.bot/xyz",
  "_ts": 1709999999999,
  "ownerId": "user123",
  "submitterIp": "1.2.3.4"
}
```

## 使用示例

```bash
# 使用默认域名缩短
node shorturl/scripts/shorten.js "https://example.com/very-long-url"

# 使用其他域名
node shorturl/scripts/shorten.js "https://example.com/very-long-url" "https://2s.gg/"

# 自定义后缀
node shorturl/scripts/shorten.js "https://example.com/very-long-url" "https://surl.bot/" "my-custom"
```

## 依赖

- Node.js (内置 http/https 模块，无需额外安装)
