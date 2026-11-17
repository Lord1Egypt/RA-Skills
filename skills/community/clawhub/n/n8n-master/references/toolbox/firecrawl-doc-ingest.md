# Firecrawl Doc Ingest Toolbox

## 何时使用

用 `scripts/toolbox/firecrawl_ingest_docs.py` 把外部 URL 抓成 Markdown，保存到 Skill 的 `references/source/` 目录，再交给 AI compiler 做 wiki、api-card 或 recipe。它适合单页或少量页面的文档抓取，不负责站点级 crawl 队列、去重调度或内容质量清洗。

## 环境变量

```bash
export FIRECRAWL_API_KEY="fc-..."
```

脚本不会打印 API key 或 Authorization header。

## 示例命令

先 dry-run 看请求形态和目标文件名：

```bash
python3 scripts/toolbox/firecrawl_ingest_docs.py \
  "https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/" \
  --source-dir references/source/api-packs/<platform>/raw \
  --dry-run
```

真实抓取并写入 Markdown 和 manifest：

```bash
python3 scripts/toolbox/firecrawl_ingest_docs.py \
  "https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/" \
  --source-dir references/source/api-packs/<platform>/raw
```

传入额外 Firecrawl 请求参数：

```bash
python3 scripts/toolbox/firecrawl_ingest_docs.py \
  "https://docs.n8n.io/" \
  --source-dir references/source/api-packs/<platform>/raw \
  --request-json '{"onlyMainContent":true,"waitFor":1000}' \
  --overwrite
```

## API 形态

脚本默认使用 Firecrawl 当前文档中的 `POST https://api.firecrawl.dev/v2/scrape`，请求体默认是：

```json
{
  "url": "https://example.com",
  "formats": ["markdown"]
}
```

如果团队使用自托管 Firecrawl 或旧版 API，可以通过 `--endpoint` 覆盖；如果响应里没有 `markdown` 或 `content` 字段，脚本会保守失败，并打印脱敏后的响应结构，提醒调用者调整 `--endpoint` 或 `--request-json`。

## 输出

每个 URL 会写成一个稳定文件名：

```text
001-docs-n8n-io-path-a1b2c3d4.md
```

同时写入 `manifest.json`，记录 URL、文件名、抓取时间、endpoint、formats、metadata 和 Markdown sha256。manifest 不包含 API key。

## 安全边界

- 默认不覆盖已有 Markdown；需要覆盖时显式加 `--overwrite`。
- `--dry-run` 不发网络请求，也不创建文件。
- Firecrawl 结果仍需 AI compiler 检查；不要把抓取结果直接当作已验证知识。
- 对需要登录、含隐私或版权敏感的页面，不要用此脚本抓取进 Skill。
