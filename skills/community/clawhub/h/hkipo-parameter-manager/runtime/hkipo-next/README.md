# hkipo-next

`hkipo-next` 是面向 Epic 1 重构主线的新 CLI 主干。它与 legacy `scripts/hkipo.py` 并存，但新的发现、快照、评分和复盘能力都应继续落在 `src/hkipo_next/` 下。

## 当前边界

- 新主干入口：`python -m hkipo_next` 或 `hkipo-next`
- 当前已接管能力：`calendar`
- 当前已接管能力：
  - `calendar`
  - `snapshot`
  - `profile`
  - `watchlist`
  - `params`
  - `score`
  - `decision-card`
  - `batch`
- legacy 仍保留但不再扩展的入口：
  - `scripts/hkipo.py`
  - `scripts/hkipo/__main__.py`
  - `scripts/hkipo/*.py` 中的抓取与分析模块仅作为迁移期适配器素材

## 输出契约

- 成功响应：`{"ok": true, "data": {...}, "meta": {...}}`
- 失败响应：`{"ok": false, "error": {...}, "meta": {...}}`
- 固定错误码：`E_ARG` / `E_SOURCE` / `E_RULE` / `E_SYSTEM`
- `meta` 至少包含：`run_id`、`timestamp`、`rule_version`、`schema_version`、`data_status`
- 支持 `json` / `text` / `markdown` 三种渲染格式，且三者共享同一套底层 schema

## 最小 Smoke 基线

```bash
uv run hkipo-next calendar --window deadline --days 7 --format json
uv run hkipo-next calendar --window listing --days 7 --format text
uv run hkipo-next calendar --window deadline --days 7 --format markdown --output artifacts/calendar.md
uv run hkipo-next snapshot 2476 --format json
uv run hkipo-next snapshot 2476 --format markdown --output artifacts/snapshot.md
uv run hkipo-next params save --name baseline --activate --format json
uv run hkipo-next score 2476 --format json
uv run hkipo-next decision-card 2476 --format markdown
uv run hkipo-next batch 2476 1234 --format json
uv run pytest
uv run ruff check src tests
```

## 迁移说明

- 本阶段用 `uv` 管理项目、依赖和锁文件，后续故事继续在该主干下扩展。
- `calendar` 命令通过 `services -> adapters -> legacy data source` 的路径取数，并只通过 `contracts/` 返回结构化对象。
- 后续 `snapshot`、评分、决策卡和批处理能力都必须复用当前的统一元数据、错误码和渲染层，而不是回退到 legacy CLI 直接输出文本。

## 兼容矩阵

| Legacy / 旧习惯 | 新主干命令 | 状态 |
| --- | --- | --- |
| `scripts/hkipo.py overview` | `uv run hkipo-next calendar --window deadline --format text` | 等价替换（受治理输出） |
| 手工拼接单股 IPO 关键信息 | `uv run hkipo-next snapshot <symbol> --format json` | 等价替换（标准化快照） |
| 人工维护打新参数和版本 | `uv run hkipo-next params save/list/show/use` | 等价替换（结构化版本管理） |
| 凭经验输出是否参与 | `uv run hkipo-next score <symbol> --format json` | 等价替换（可解释评分） |
| 手工整理执行清单 | `uv run hkipo-next decision-card <symbol> --format markdown` | 等价替换（结构化决策卡） |
| watchlist / 多标的手工逐个看 | `uv run hkipo-next batch --watchlist --format json` | 等价替换（批量聚合输出） |
| legacy 自由文本输出 | `json/text/markdown` 统一 renderer | 有意破坏性变更 |

## 已记录的破坏性变更

- 新 CLI 不再承诺复刻 legacy 的自由文本格式，统一改为 schema 驱动输出。
- `json` 成为机器权威接口；`text` 和 `markdown` 仅做展示层渲染。
- 输出错误不再直接透传第三方异常文本，而是固定映射到 `E_ARG` / `E_SOURCE` / `E_RULE` / `E_SYSTEM`。
