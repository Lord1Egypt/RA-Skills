---
name: pansou
description: 网盘资源搜索引擎。支持百度网盘、阿里云盘、夸克网盘、天翼云盘、UC网盘、移动云盘、115、PikPak、迅雷、123网盘、磁力链接、电驴等12种网盘类型。支持按网盘类型、插件、TG频道过滤搜索结果。当用户需要搜索电影、剧集、软件、学习资料等网盘资源时使用此技能。触发词：搜索网盘、找资源、pan搜、网盘搜索、pansou。
metadata:
  openclaw:
    requires:
      bins:
        - uv
      env:
        - PANSOU_URL
---

## 使用

调用前确认环境变量 `PANSOU_URL` 已配置。部署详见 [PanSou GitHub](https://github.com/fish2018/pansou)。

```bash
# 健康检查（无需认证）
uv run {baseDir}/scripts/pansou.py health

# 验证 token 是否有效，无效自动重新登录
uv run {baseDir}/scripts/pansou.py verify

# 搜索（自动处理认证）
uv run {baseDir}/scripts/pansou.py search "关键词"

# 指定网盘类型
uv run {baseDir}/scripts/pansou.py search "关键词" --cloud-types quark,aliyun,baidu

# 指定插件
uv run {baseDir}/scripts/pansou.py search "关键词" --plugins labi,zhizhen,shandian

# 指定TG频道
uv run {baseDir}/scripts/pansou.py search "关键词" --channels tgsearchers3

# 过滤结果
uv run {baseDir}/scripts/pansou.py search "觉醒年代" --include 合集,全集 --exclude 预告,花絮

# 仅TG / 仅插件
uv run {baseDir}/scripts/pansou.py search "关键词" --src tg
uv run {baseDir}/scripts/pansou.py search "关键词" --src plugin

# 强制刷新缓存
uv run {baseDir}/scripts/pansou.py search "关键词" --refresh

# 使用 GET 方式搜索
uv run {baseDir}/scripts/pansou.py search "关键词" --get
```

Token 自动存储在 `~/.config/pansou/token.json`，过期自动重新登录。

## 安全说明

- `PANSOU_URL` 由用户自行部署或指定，脚本仅向该地址发起 HTTP 请求
- `PANSOU_USER` / `PANSOU_PWD` 仅在服务返回 401 时用于获取 JWT token
- Token 仅通过 HTTP POST 发送至用户指定的 `PANSOU_URL`，不会外泄
- 认证为可选：未启用认证的服务无需设置 `PANSOU_USER` / `PANSOU_PWD`

## 支持的网盘类型

简要列表：`baidu` `aliyun` `quark` `tianyi` `uc` `mobile` `115` `pikpak` `xunlei` `123` `magnet` `ed2k` `others`

完整清单（含各类型对应的插件和说明）见 [references/cloud-types.md](references/cloud-types.md)。

## 搜索参数详解

所有 CLI 参数（`--res`、`--conc`、`--refresh` 等）详细说明见 [references/api-params.md](references/api-params.md)。

## 搜索结果格式

默认 `merge` 模式，按网盘类型分类返回：

```json
{
  "total": 15,
  "merged_by_type": {
    "quark": [
      {"url": "https://pan.quark.cn/s/abcdefgxxxx", "password": "", "note": "标题", "datetime": "...", "source": "plugin:labi"}
    ]
  }
}
```

如需原始消息列表，使用 `--res results`。

## 输出格式注意事项

### 链接展示格式
向用户展示搜索结果中的链接时，**必须使用 Markdown URL 形式**，不要用代码块包裹：

✅ **正确示例**：
```
1. 更新至20集 4K HDR
https://pan.quark.cn/s/abcdefgxxxx
```

❌ **错误示例**：
```
1. 更新至20集 4K HDR
`https://pan.quark.cn/s/abcdefgxxxx`
```

原因：代码块形式的链接无法直接点击，用户体验差。Markdown URL 可以直接点击打开。
