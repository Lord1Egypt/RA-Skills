---
name: newspaper_download
description: 报刊 PDF 下载工具。通过 CLI 命令查询已收录的报刊更新、定位指定期次、获取 PDF 下载链接。查询不鉴权，下载需要 Import Token。Newspaper/magazine PDF download tool. Use CLI commands to query collected issues, locate specific issues, and get PDF download links.
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python3"]
      }
    }
  }
---

# 报刊 PDF 下载工具

## ⚠️ 使用规则（必须遵守）

1. **只通过 CLI 命令调用** — 运行 `python3 {baseDir}/scripts/get_data.py <command>`，不要自己写脚本，不要用 curl/requests 直接调 API
2. **所有命令加 `--no-save`** — 输出直接打印 JSON 到终端，不落盘
3. **先读 config.json** — 执行任何命令前，先读取 `{baseDir}/config.json` 检查 `import_token` 是否已配置
4. **报纸名支持中英文和缩写** — `纽约时报`、`NYT`、`The New York Times` 都能识别

## 第一步：检查配置

每次使用前先读取 `{baseDir}/config.json`：

```json
{
    "api_base": "https://pick-read.vip/api",
    "import_token": "imp-xxx..."
}
```

- 如果 `import_token` 为空 → 告知用户：请到 pick-read.vip 账户页生成导入令牌并填入 config.json
- 如果 `import_token` 已填写 → 直接执行命令，无需再传 `--token` 参数

## 工作流 A：查看今天更新了什么

```bash
python3 {baseDir}/scripts/get_data.py updates --no-save
```

返回示例：
```json
{
  "type": "recent_updates",
  "total": 12,
  "items": [
    {"issue_id": "abc123", "pub_name": "Financial Times", "issue_date": "2026-04-01", "page_count": 20},
    {"issue_id": "def456", "pub_name": "The New York Times", "issue_date": "2026-04-01", "page_count": 46}
  ]
}
```

可选参数：`--days 3`（最近3天）、`--limit 5`（最多5条）

**如果今天 total=0**，尝试 `--days 2` 查看昨天的更新。

## 工作流 B：查询某份报纸并获取下载链接

```bash
python3 {baseDir}/scripts/get_data.py issue-info "纽约时报" --no-save
```

返回示例（config.json 有 token 时）：
```json
{
  "type": "issue_info",
  "matched": true,
  "issue_id": "abc123",
  "pub_name": "The New York Times",
  "issue_date": "2026-04-01",
  "page_count": 46,
  "download_url": "https://pick-read.vip/api/import-pdf/abc123?token=imp-xxx"
}
```

可选参数：`--issue-date 2026-03-31`（指定日期）

**把 `download_url` 直接给用户，这就是 PDF 下载地址。**

## 工作流 C：批量获取下载链接

```bash
python3 {baseDir}/scripts/get_data.py download-links --no-save
```

返回示例：
```json
{
  "type": "download_links",
  "has_token": true,
  "total": 12,
  "items": [
    {"issue_id": "abc123", "pub_name": "Financial Times", "issue_date": "2026-04-01", "page_count": 20, "download_url": "https://pick-read.vip/api/import-pdf/abc123?token=imp-xxx"},
    {"issue_id": "def456", "pub_name": "The New York Times", "issue_date": "2026-04-01", "page_count": 46, "download_url": "https://pick-read.vip/api/import-pdf/def456?token=imp-xxx"}
  ]
}
```

可选参数：`--days 2`（最近2天）、`--pub-name "Financial Times"`（按刊物筛选）、`--limit 5`

## 工作流 D：组合任务示例

用户说"帮我下载纽约时报和华尔街日报"：

```bash
# 步骤1: 获取纽约时报
python3 {baseDir}/scripts/get_data.py issue-info "纽约时报" --no-save

# 步骤2: 获取华尔街日报
python3 {baseDir}/scripts/get_data.py issue-info "华尔街日报" --no-save
```

从返回的 JSON 中提取 `download_url`，提供给用户即可。

## 报纸名称对照表

| 用户可能的输入 | 会匹配到 |
|---|---|
| `纽约时报` / `NYT` | The New York Times |
| `华尔街日报` / `WSJ` | The Wall Street Journal |
| `金融时报` / `FT` | Financial Times |
| `华盛顿邮报` / `wapo` | The Washington Post |
| `洛杉矶时报` / `LA Times` | Los Angeles Times |
| `中国日报` | China Daily |
| `卫报` / `Guardian` | The Guardian |

## 禁止事项

- ✘ 不要用 curl、wget、requests 等直接调用 API
- ✘ 不要自己拼 URL 或写 HTTP 请求代码
- ✘ 不要猜测 API 端点路径
- ✘ 不要编造下载链接
- ✘ 检索失败时不得编造内容，应如实告知用户

## 故障排查

| 现象 | 原因 | 解决 |
|---|---|---|
| `download_url` 为 null | config.json 中 import_token 为空 | 让用户到 pick-read.vip 生成令牌 |
| `matched: false` | 报纸名未匹配到 | 换个名称试试，或用 `updates` 查看有哪些报刊 |
| `total: 0` | 指定日期无更新 | 用 `--days 2` 或 `--days 3` 扩大范围 |
| `EOF occurred in violation of protocol` | 系统代理/VPN 干扰 TLS | 脚本已内置代理绕过，正常重试即可 |
| 命令报错 | 网络问题或服务端问题 | 重试一次，仍失败则告知用户 |
