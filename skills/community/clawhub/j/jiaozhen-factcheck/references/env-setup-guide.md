# tencent-news-cli API Key 配置指南

## 获取 API Key

1. 打开浏览器访问 [API Key 获取页面](https://news.qq.com/exchange?scene=appkey)
2. 按页面引导完成获取

## 设置 API Key

打开终端（macOS / Linux）或 PowerShell（Windows），执行：

```sh
tencent-news-cli apikey-set YOUR_KEY
```

> `YOUR_KEY` 替换为实际获取到的 Key 值，不需要加引号。

验证：

```sh
tencent-news-cli apikey-get
```

## 清除 API Key

仅在需要重置时执行：

```sh
tencent-news-cli apikey-clear
```

## 常见问题

- **未设置 API Key / `API Key not set`** → 前往上述获取页面取得 Key，执行 `tencent-news-cli apikey-set YOUR_KEY`，再执行 `tencent-news-cli apikey-get` 验证
- **`API Key 无效` / `invalid api key` / `unauthorized` / `401` / `403` / 鉴权失败** → 当前 Key 无效、过期或无权访问；重新前往获取页面生成正确 Key，再执行设置和验证命令。不得把此类错误解释成“无数据”“额度用完”或普通网络失败
- **`operation not permitted`** → 确认在有写入权限的终端中执行命令
- **找不到 `tencent-news-cli` 命令** → 重新打开终端，或参考 [安装指南](installation-guide.md) 重新安装

> `YOUR_KEY` 仅作为占位符。真实 Key 只能由用户在本地终端填写，不应发送给智能体，也不得在回复、日志或报告中回显。
