# iFinD Finance Data Skill

> 本文件记录资金交易 skill 如何协同调用同花顺 iFinD 金融数据 skill。资金交易 skill 不直接维护 iFinD MCP 配置或密钥；数据获取交给 `$ifinD-finance-data` skill。

## 目录

- 用途
- 外部 Skill
- 使用原则
- 资金交易常用查询
- 查询工作流
- 失败处理
- 安全规则

## 用途

当任务涉及实时或历史金融数据时，优先调用 iFinD 金融数据 skill，而不是让模型凭记忆回答。

适合查询：

- 资金利率和回购相关数据。
- 债券基本信息、行情、估值、特殊指标、评级等。
- 宏观经济指标，如 CPI、PPI、PMI、社融、M2、GDP、工业增加值等。
- 财经新闻、公告和政策相关资讯。
- 指数、板块、基金、股票等辅助数据。

## 外部 Skill

资金交易 skill 只依赖 iFinD skill 的名称，不依赖某台机器上的绝对路径。

推荐安装方式：将 iFinD skill 与本 skill 放在同一个 skills 根目录下，例如：

```text
skills/
├── interbank-funding-trader/
└── ifind-finance-data/
```

目录名可以因安装包版本不同而变化，触发以 iFinD skill 的 frontmatter `name` 为准。当前 iFinD skill 的名称为：

```text
ifinD-finance-data
```

显式调用时使用：

```text
使用 $ifinD-finance-data 查询 ...
```

该 iFinD skill 自己维护 `mcp_config.json` 和调用脚本。资金交易 skill 不复制、不生成、不保存 iFinD MCP 配置。

## 使用原则

- 涉及“最新”“今天”“近期”“历史序列”“实际数据”的问题，先调用 `$ifinD-finance-data`。
- 查询结果必须标注数据日期、指标名称、口径和来源。
- 如果 iFinD skill 返回失败、无结果或权限不足，明确说明，不要编造数据。
- 如果不确定具体宏观指标名称，先用 iFinD 的 `search_edb` 搜索，再用 `get_edb_data` 取数。
- 债券数据优先使用 iFinD 的 `bond` 服务；宏观和资金面指标优先使用 `edb` 服务；新闻公告使用 `news` 服务。
- 单次 query 控制主体和指标数量，通常不超过 5 个。

## 资金交易常用查询

### 宏观和资金面指标

使用 `$ifinD-finance-data` 的 `edb` 服务：

- `search_edb`：不确定指标名称时先搜索。
- `get_edb_data`：确认指标后获取数据。

示例需求：

```text
查询 R001、R007、DR001、DR007 最近 30 个交易日数据。
查询 M2、社融存量同比最近 24 个月数据。
查询 CPI、PPI、PMI 最近一年数据。
查询 OMO 或公开市场操作相关指标。
```

### 债券和押品相关数据

使用 `$ifinD-finance-data` 的 `bond` 服务：

- `bond_basic_info`：债券基本信息、发行期限、发行总额、主体信息。
- `bond_market_data`：行情、估值、久期、凸性等。
- `bond_financial_data`：发债主体财务指标。
- `bond_special_data`：信用债评级、回购、可转债条款等特殊指标。

示例需求：

```text
查询某批债券的主体评级、债项评级、托管地和债券类型。
查询某只信用债的最新估值和隐含评级相关信息。
查询某主体资产负债率、ROE 等财务指标。
```

### 新闻和公告

使用 `$ifinD-finance-data` 的 `news` 服务：

- `search_news`：财经新闻。
- `search_notice`：公告。
- `search_trending_news`：热点事件。

示例需求：

```text
搜索某发行主体最近一个月的负面新闻。
搜索某主体公告中与债务、评级、担保、违约相关内容。
```

## 查询工作流

1. 判断是否需要真实数据。
2. 选择 iFinD 服务类型：`edb`、`bond`、`news` 等。
3. 如指标名称不确定，先搜索；如明确，直接查询。
4. 将查询结果转回资金交易语境：
   - 对资金面：解释 R/DR、分层、历史分位、趋势。
   - 对押品：解释评级、主体、托管地、黑名单或验券字段。
   - 对宏观：解释对资金面的可能影响，避免过度因果化。
5. 标注数据来源和日期。

## 失败处理

如果 iFinD skill 不可用：

- 说明“未能通过 iFinD 获取实时数据”。
- 给出需要查询的指标清单或 iFinD query 建议。
- 不要用模型记忆填充具体数值。

如果返回结果和内部券库或账户准入规则冲突：

- 验券以内部券库和账户准入规则为准。
- iFinD 数据可作为补充核验来源，不直接覆盖内部准入结果。

## 安全规则

- 不在资金交易 skill 中保存 iFinD 密钥。
- 不复述 iFinD `mcp_config.json` 中的 token。
- 不把 iFinD 查询结果中的敏感账户或内部字段暴露给外部对手。
- 开源资金交易 skill 时，不包含 iFinD 的密钥、配置或本地下载包。
