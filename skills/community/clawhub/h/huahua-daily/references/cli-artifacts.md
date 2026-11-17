# CLI 文件与完整导出

CLI 只处理不适合经过模型上下文的数据形态。需要环境变量 `HUAHUA_AGENT_TOKEN`，可用 `HUAHUA_API_BASE` 覆盖后端地址。

持久安装该 Python 包后使用 `huahua`。如果 MCP 仅通过推荐的 `uvx` 临时运行、宿主没有 `huahua` 命令，则使用：

```bash
uvx --from git+https://github.com/baiye1997/HuaHuaDailyMCP huahua <子命令>
```

不得因为 CLI 不可用而回退到图片 Base64。

## 诊断

```bash
huahua doctor
```

输出小型 JSON，检查 Token、网络、当前用户和 App 版本。错误写 stderr，退出码为 2。

## 截图识别

```bash
huahua import screenshots \
  --type transactions \
  --file /absolute/path/one.png \
  --file /absolute/path/two.png \
  --result /absolute/path/recognized.json
```

`--type` 支持 `holdings`、`watchlist`、`transactions`。路径必须由用户在当前请求中明确提供；Agent 不得猜测、搜索或扫描路径。限制为最多 10 张、单张 10MB、总计 50MB，并校验真实图片 magic bytes。

识别只生成结果文件，不写入 App。检查摘要和未匹配项后提交：

```bash
huahua import review \
  --type transactions \
  --input /absolute/path/recognized.json \
  --source-note "Agent 识别交易截图" \
  --client-request-id import:transactions:20260820:1
```

结果文件记录原始导入类型；`review --type` 不一致时 CLI 会拒绝。提交后仍需用户在 App 中确认。

## 完整导出

```bash
huahua export portfolio --output /absolute/path/portfolio.json

huahua export nav-history \
  --codes 110022,000001 \
  --start-date 2020-01-01 \
  --end-date 2026-08-20 \
  --output /absolute/path/nav-history.json
```

净值接口单次最多 20 只基金、最长 5 年。大结果写文件，stdout 只返回状态、路径和少量摘要。不要把完整文件内容重新粘贴到对话中；只读取回答当前问题所需的片段。

## 大型报告

报告文件应包含后端 `/api/agent/messages` 所需的 `type`、`title`、`summary`、`payload` 和可选 `clientMessageId`：

```bash
huahua report submit --file /absolute/path/report.json
```

CLI 不提供普通持仓、基金、市场、交易和社区命令；这些继续使用 MCP。
