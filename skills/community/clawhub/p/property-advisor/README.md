# Property Advisor

OpenClaw 优先的房产搜索、地图增强与房源发布编排 skill。

这个仓库不再是“只会分析文档的纯决策层”，而是一个完整的执行型编排层。C 端找房链路：

1. 解析用户的房产需求
2. 读取本地画像并根据 source routing 选择可执行上游 source adapter
3. 预检所选上游 skill 运行环境
4. 通过上游 skill 搜索房源并补齐详情
4. 保存原始房源快照
5. 显式调用仓库内的 `public-osm-map-context-skill`
6. 生成带证据的地图结论
7. 输出固定 8 列候选表

B 端发布链路：

1. 识别用户是找房还是发布房源
2. 判断出租 / 出售
3. 自动路由发布市场：英国/Gumtree 走 `gt-core-skill publish-listing`，其他市场默认走 `ok-core-skill publish-property`
4. 抽取发布字段与房源强项，中文平方米会换算为 OK 表单使用的 sqft
5. 有位置、地址或 postcode 时调用 bundled `public-osm-map-context-skill`
6. 信息不足时返回分级 readiness 和深入追问，不调用发布命令
7. 默认只 dry-run 或填表，不自动提交
8. 用户确认后才允许真实发布；GT 真实发布还需要 Gumtree `publish_endpoint`

## 当前能力

- 自动根据请求路由市场：
  - 非英国默认走 `ok-core-skill`
  - 英国城市 / postcode / 学校 / 大学 / Tube / Council Tax 等信号默认走 `gt-core-skill`
- 本地画像与记忆：
  - 默认目录 `~/property-advisor/`
  - `profile.md` 保存角色、预算、城市、通勤目的地、房型、偏好 source 和硬性要求
  - `searches/` 保存搜索历史
  - `watched/` 保存关注房源
- source routing：
  - 新增 `--source`，保留 `--market` 兼容
  - OK/GT 是当前已实现 source adapter，实际抓取分别依赖 `ok-core-skill` / `gt-core-skill`
  - Zillow、Rightmove、Domain、PropertyGuru 等作为已知外部 source 登记，未接入 adapter 时清晰降级
  - 输出保留真实 `resolved_source_id`，但不声称本 skill 自身具备所有平台抓取能力或已覆盖所有平台
- 自动发现 `ok-core-skill` 路径
- 自动发现 `gt-core-skill`：
  - 优先已安装的 OpenClaw / Codex skill 目录
  - 回退本地桌面开发路径
- 固定优先使用 `uv run python scripts/cli.py`
- `uv` 不可用或 smoke 失败时回退到 `ok-core-skill/.venv/bin/python`
- `gt-core-skill` Bridge 版优先走 `uv run python scripts/cli.py`
- `gt-core-skill` API 版作为受控降级 fallback
- 显式调用 bundled `public-osm-map-context-skill/scripts/cli.py`
- 输出固定候选表：
  - `候选房源`
  - `状态`
  - `价格`
  - `位置`
  - `已满足`
  - `缺失/未知`
  - `淘汰原因/风险`
  - `房源链接`
- 缺少原帖链接的房源 fail-closed，不会被点名展示
- B 端发布支持：
  - `business_publish` 意图识别
  - 发布 readiness 分级与上下文追问
  - 发布字段完整度检查
  - 基于用户字段与地图 assessments 的证据化标题/描述生成
  - OK `publish-property` dry-run / 填表 / 确认发布
  - GT `publish-listing` dry-run / 确认发布 endpoint 透传

## 项目结构

```text
Property-Advisor/
├── SKILL.md
├── agents/openai.yaml
├── scripts/cli.py
├── property_advisor/
│   ├── analysis.py
│   ├── gt_client.py
│   ├── map_client.py
│   ├── models.py
│   ├── ok_client.py
│   ├── orchestrator.py
│   ├── routing.py
│   └── source_client.py
├── public-osm-map-context-skill/
│   ├── scripts/cli.py
│   └── tests/
├── references/
│   ├── data-contract.md
│   ├── map-context-contract.md
│   ├── output-contract.md
│   └── response-examples.md
└── tests/
```

## 运行规则

### 市场路由

- 默认 `market=auto`
- 命中英国语义时走 `gt-core-skill`
- 混合英国和非英国高置信地理信号时，返回澄清错误，不静默混用

### Source routing 与本地记忆

- 默认 `source=auto`
- `market=ok|gt` 仍可用，但新链路会同时写入 `resolved_source_id`
- 用户明确指定外部平台时不会自动改写为 OK/GT；如果 adapter 未接入，会返回清晰错误
- 搜索默认读取并更新 `~/property-advisor/profile.md`
- 如需禁用本地记忆，搜索时加 `--no-memory`
- 如需使用临时记忆目录，传 `--memory-dir /path/to/dir`

### ok-core-skill 路径发现

按下面顺序解析：

1. `OK_CORE_SKILL_ROOT`
2. `PROPERTY_OK_SKILL_ROOT`
3. `/Users/a58/Desktop/skills/ok-core-skill`
4. 历史兼容路径 `/Users/a58/Desktop/ok-core-skill/skills/ok-core-skill`

### gt-core-skill 路径发现

按下面顺序解析：

1. `GT_CORE_SKILL_ROOT`
2. `PROPERTY_GT_SKILL_ROOT`
3. 当前工作区 `.agents/skills` 与 `skills`
4. `$CODEX_HOME/skills` / `~/.codex/skills`
5. 本地桌面 `gt-core-skill` 开发路径

Bridge 版优先于 API 版。

### ok-core-skill 执行顺序

固定顺序：

1. `uv run python scripts/cli.py`
2. `ok-core-skill/.venv/bin/python scripts/cli.py`

禁止：

- 直接用裸 `python3 scripts/cli.py` 调 `ok-core-skill`
- 依赖模型临场决定如何调用 `ok-core-skill`

### 地图 skill 执行规则

- 不依赖 nested skill 自动发现
- 始终由编排层显式调用仓库内的 `public-osm-map-context-skill/scripts/cli.py`
- 搜索类场景默认自动跑地图增强

## 本地调试

### 1. 环境预检

```bash
python3 scripts/cli.py doctor --skip-browser-smoke
```

### 2. 走完整编排链路

```bash
python3 scripts/cli.py search \
  --keyword "southbank apartment" \
  --country australia \
  --city melbourne \
  --destination "Melbourne CBD VIC" \
  --budget-max 3500 \
  --bedrooms 1
```

禁用本地记忆：

```bash
python3 scripts/cli.py search \
  --keyword "southbank apartment" \
  --country australia \
  --city melbourne \
  --no-memory
```

### 3. 走英国 GT 链路

```bash
python3 scripts/cli.py search \
  --keyword "studio flat" \
  --query-text "找 London 的 studio flat" \
  --market auto \
  --destination "King's Cross London"
```

### 4. 指定外部 source（未接入时透明降级）

```bash
python3 scripts/cli.py search \
  --query-text "帮我分析 Zillow 上 Austin 的房源" \
  --source zillow
```

### 5. 用地图 fixture 跑稳定回归

```bash
python3 scripts/cli.py search \
  --keyword "southbank apartment" \
  --country australia \
  --city melbourne \
  --destination "Melbourne CBD VIC" \
  --map-fixture-dir public-osm-map-context-skill/tests/fixtures/osm
```

### 6. 保存关注房源

```bash
python3 scripts/cli.py watch \
  --url "https://example.test/listing" \
  --title "Example Listing" \
  --source ok \
  --note "价格合适，等复核"
```

### 7. B 端发布意图识别

```bash
python3 scripts/cli.py route \
  --query-text "我要出租 Dubai Marina 1BR furnished apartment near metro"
```

### 8. B 端 OK 发布 dry-run

```bash
python3 scripts/cli.py publish \
  --query-text "我要出租 Dubai Marina 1BR furnished apartment near metro" \
  --country uae \
  --price 8000 \
  --phone 501234567 \
  --image "/absolute/path/photo.jpg" \
  --dry-run
```

真实发布必须显式追加 `--confirm-submit`。没有图片时可以生成草稿或填表，但确认发布前会要求补至少一张本地绝对路径图片。
英国发布会自动路由到 GT；`--confirm-submit` 时会调用 `publish-listing`，如果 Gumtree session 未配置 `publish_endpoint`，需额外传 `--publish-endpoint`。

## 输出说明

搜索结果默认返回 JSON，其中包含：

- `preflight`
- `selected_source`
- `selected_runtime_mode`
- `routing`
- `raw_listing_snapshots`
- `map_report`
- `candidate_rows`
- `hidden_candidates`
- `rendered_table`

`candidate_rows[*].display_row` 是最终展示层可直接消费的 8 列结构。

## 测试

```bash
python3 -B -m unittest discover -s tests
python3 -B -m unittest discover -s public-osm-map-context-skill/tests
```

目前已覆盖：

- skill 路径发现
- runner 选择与 fallback
- browser smoke 失败分支
- 房源详情补全
- 地图自动调用
- 地图结构化 assessments
- 缺原帖链接 fail-closed
- 最终 8 列候选表 golden test
- B 端发布意图识别、缺字段追问、OK 发布参数安全策略、GT dry-run payload
- B 端发布地图增强、证据化文案、中文面积换算、UK 自动 GT 发布路由
