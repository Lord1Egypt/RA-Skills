# CLI 参数详解

所有搜索命令通过 `uv run {baseDir}/scripts/pansou.py search` 调用。

## 必需参数

| 参数 | 说明 |
|------|------|
| `keyword` | 搜索关键词（位置参数） |

## 可选参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--channels` | - | TG频道，逗号分隔，如 `tgsearchers3` |
| `--conc` | - | 并发数 |
| `--refresh` | false | 强制刷新缓存 |
| `--res` | `merge` | 返回格式：`merge`（按网盘类型分类）、`all`（全部）、`results`（原始列表） |
| `--src` | `all` | 数据源：`all`（全部）、`tg`（仅TG）、`plugin`（仅插件） |
| `--plugins` | - | 插件，逗号分隔，如 `labi,zhizhen,shandian` |
| `--cloud-types` | - | 网盘类型，逗号分隔，如 `quark,aliyun,baidu` |
| `--include` | - | 包含关键词，逗号分隔 |
| `--exclude` | - | 排除关键词，逗号分隔 |
| `--get` | false | 使用 GET 方式请求（默认 POST） |

## 常用组合示例

```bash
# 搜索夸克+阿里云盘
uv run {baseDir}/scripts/pansou.py search "电影名" --cloud-types quark,aliyun

# 指定插件搜索
uv run {baseDir}/scripts/pansou.py search "电影名" --plugins labi,zhizhen

# 仅TG频道
uv run {baseDir}/scripts/pansou.py search "电影名" --src tg

# 包含+排除过滤
uv run {baseDir}/scripts/pansou.py search "觉醒年代" --include 合集,全集 --exclude 预告,花絮

# 强制刷新缓存
uv run {baseDir}/scripts/pansou.py search "电影名" --refresh

# 返回原始结果列表
uv run {baseDir}/scripts/pansou.py search "电影名" --res results
```
