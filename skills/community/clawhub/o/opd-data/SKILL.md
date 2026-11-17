---
name: opd-data
description: 查询 OPD 金融数据接口（api.originp.com）：A股上市公司基本信息、证券与行业分类、行情交易（日/周/月线、大宗交易、停复牌、异动）、财务报表与财务指标、融资融券与股权质押、IPO/增发/配股/分红、处罚诉讼担保等重大事项、股东/高管/股本等股权治理数据。当用户询问上市公司或股票相关数据时使用本技能。
version: 1.0.2
metadata: {"openclaw": {"requires": {"bins": ["python"]}, "primaryEnv": "OPD_API_KEY"}}
---

# OPD 金融数据查询

通过 OPD 数据接口（`https://api.originp.com`）查询 A 股上市公司数据，共 62 个接口、6 大类。

## 权限与数据流声明

本技能的全部外部行为如下，超出此范围的行为均非本技能所为：

- **网络**：仅访问 `https://api.originp.com`（`OPD_BASE_URL` 仅接受 `*.originp.com` 的 https 地址，脚本强制校验），发送查询参数与 `X-API-Key` 请求头；不向任何第三方地址发送数据。
- **环境变量**：仅读取 `OPD_API_KEY`（密钥）与 `OPD_BASE_URL`（调试用接口地址）。
- **文件**：仅读写 `~/.opd/api_key`（密钥保存位置，唯一落盘文件），不访问其他文件。
- **依赖**：仅使用 Python 标准库，不执行 `pip install`，不下载任何可执行文件。
- **图表**：可视化需求委托 `echarts-ai-skill` 技能处理（执行其 Node.js 脚本生成 HTML，并由用户本地浏览器打开查看）；本技能脚本不自行绘图或访问网络获取图表资源。
- **密钥**：不在对话中索取、回显或转发密钥；配置一律由用户在本地终端完成。

## 环境准备（首次使用，一次性）

1. **获取 API Key**：由 OPD 平台分配，形如 `opd_xxx`。注册/订阅等管理操作在 `https://data.originp.com/` 完成（该站提供页面服务）；`https://api.originp.com` 为接口调用地址，专供程序调用、不含页面。注意：除 Key 外还需**订阅所需接口**（试用或购买套餐），未订阅的接口调用会返回 BIZ_INTERFACE_FORBIDDEN。
2. **配置 API Key（推荐：终端交互输入）**：指引用户在本地终端运行：
   ```bash
   python scripts/opd_query.py --set-key
   ```
   按提示粘贴 Key（从标准输入读取，不进入命令历史，也不经过对话），保存到 `~/.opd/api_key`，脚本自动读取，**无需重启**即可生效。

   > **安全提示**：不要请用户把 API Key 粘贴到对话消息中发送——对话记录可能被留存、转发或用于训练；也不要用 `--set-key <Key>` 带值形式执行（Key 会留在 shell 命令历史）。若用户已把密钥发进对话，提醒其尽快在 OPD 平台重置该 Key。
3. **（可选，兼容旧方式）配置环境变量** `OPD_API_KEY`：
   - Windows（用户级，需在配置后**重启 OpenClaw Gateway** 才会对 Agent 生效）：
     ```powershell
     [Environment]::SetEnvironmentVariable("OPD_API_KEY", "opd_你的Key", "User")
     ```
   - Linux/macOS：在 shell 配置文件中加入 `export OPD_API_KEY=opd_你的Key`
4. **验证配置**：
   ```bash
   python scripts/opd_query.py --check
   python scripts/opd_query.py co_info --fields sec_code --limit 1
   ```
   返回 JSON 中 `code=0` 即成功；`--check` 会显示掩码与 Key 来源（`--api-key` 参数 / 环境变量 / 配置文件）。

## 调用方法

使用本技能目录下的 `scripts/opd_query.py`（命令中的 `scripts/opd_query.py` 相对本技能目录，如 `~/.openclaw/workspace/skills/opd-data/`；在其他目录执行时请使用完整路径）：

```
python scripts/opd_query.py <接口短名> --fields <字段1,字段2,...> [--过滤参数 值 ...] [--limit N] [--offset N]
```

示例：

```bash
# 查询平安银行的证券简称与董事长
python scripts/opd_query.py co_info --fields sec_code,sec_name,chairman --sec_code 000001

# 查询 2024 年全年日行情收盘价（日期 between：两个边界逗号分隔）
python scripts/opd_query.py daily_quote_hist --fields trade_date,close --sec_code 000001 --trade_date 2024-01-01,2024-12-31 --limit 300
```

## 调用规范

1. **鉴权**：脚本自动读取 Key（优先级：`--api-key` 参数 > 环境变量 `OPD_API_KEY` > 配置文件 `~/.opd/api_key`，见"环境准备"）。缺失或无效时脚本会报错——按下方"错误码与处置"指引用户修复，**不要凭记忆编造数据**。
2. **fields 必填**：各接口返回字段可选值见 references/ 分类文档的"返回字段"表（标注"默认返回"的字段未指定时也会返回）。不传返回 BIZ_PARAM_INVALID。
3. **统一响应**：`{code, message, data}`；业务错误同为 HTTP 200，`code != 0` 即失败。脚本业务错误退出码为 2（网络/HTTP 错误为 1）。
4. **分页**：`limit` 默认 20、最大 5000；`offset` 为位移量。取全量数据时循环翻页直至 data 为空。
5. **多值与区间**：`in` 操作符参数（如 `sec_code`）逗号分隔多值；`between` 操作符参数（如日期）逗号分隔两个边界。
6. **限频**：每分钟 60 次，批量查询时控制节奏。
7. **按需加载**：先在下方速查表确定接口名与额外必填参数，再查阅对应 references/ 文档获取过滤参数与字段可选值；不要一次读取全部参考文档。
8. **数据最小化**：部分接口（如 `co_info`）默认返回联系电话、电子邮箱、统一社会信用代码等敏感字段（见 references/ 文档标注"默认返回"的字段）。查询时应仅选取所需字段，避免无差别全量获取导致敏感信息过度暴露。
9. **Key 安全**：不在对话中索取、回显或转发用户密钥。配置一律指引用户在本地终端完成：`python scripts/opd_query.py --set-key`（标准输入粘贴，不落命令历史）或环境变量方式。Key 仅保存到 `~/.opd/api_key`（**唯一允许的落盘位置**），不得写入其他文件。若用户把密钥粘贴到了对话中，提醒其密钥已进入对话记录、存在泄露风险，建议在 OPD 平台重置后再以本地方式配置。

## 错误码与处置

| 现象 | 原因 | 处置 |
|---|---|---|
| 脚本提示"未配置 API Key" | Key 未配置（环境变量与配置文件均缺失） | 按"环境准备"指引用户在本地终端配置（`--set-key` 交互输入，无需重启；环境变量方式 Windows 下需重启 Gateway） |
| `code=20004`（message：API Key 无效） | Key 错误或已失效 | 指引用户检查/重新获取 API Key，再用 `--set-key` 更新或改环境变量 |
| message 含 `BIZ_INTERFACE_FORBIDDEN` | 未订阅该接口 | 告知用户需在 OPD 平台订阅（试用或购买套餐）该接口后重试 |
| message 含 `BIZ_PARAM_INVALID` | 参数错误 | 检查 `fields` 是否遗漏、过滤参数名与可选值是否正确（对照 references/ 文档） |
| message 含"限频"或大量请求失败 | 超过每分钟 60 次 | 等待约 1 分钟后重试，批量任务放慢节奏 |
| HTTP 5xx / 退出码 1 | 网络或服务端异常 | 稍后重试；持续失败时报告用户服务端异常 |

## 接口速查表

### 基本信息（references/catalog_basic.md，6 个接口）

| 接口 | 名称 | 额外必填参数 |
|---|---|---|
| `co_info` | 公司基本信息 | — |
| `industry_chg` | 公司行业归属的变动 | `sec_code` |
| `security_info` | 证券信息 | — |
| `sector` | 股票所属板块 | — |
| `background` | 股票背景资料 | `sec_code` |
| `intermediary` | 中介机构 | — |

### 交易信息（references/catalog_trading.md，11 个接口）

| 接口 | 名称 | 额外必填参数 |
|---|---|---|
| `daily_quote_latest` | 股票最新日行情 | — |
| `daily_quote_hist` | 股票历史日行情 | `sec_code`、`trade_date` |
| `block_trade` | 公司大宗交易 | `sec_code` |
| `abnormal_info` | 沪深异动证券公开信息 | — |
| `suspend_resume` | 证券交易停复牌信息 | — |
| `weekly_quote` | 股票行情周报 | — |
| `monthly_quote` | 股票行情月报 | — |
| `special_notice` | 证券交易特别提示 | — |
| `multi_market_daily` | 多市场交易日报 | — |
| `weekly_acct_stats` | 一周股票账户情况统计 | — |
| `ipo_approval` | 新股过会情况 | — |

### 财务信息（references/catalog_finance.md，16 个接口）

| 接口 | 名称 | 额外必填参数 |
|---|---|---|
| `perf_forecast` | 公司业绩预告 | `sec_code` |
| `perf_express` | 公司业绩快报 | `sec_code` |
| `fin_indicators` | 上市公司财务指标 | `sec_code` |
| `bs` | 上市公司资产负债表 | `sec_code` |
| `is` | 上市公司利润表 | `sec_code` |
| `cf` | 上市公司现金流量表 | `sec_code` |
| `bs_fin` | 金融类上市公司资产负债表 | `sec_code` |
| `is_fin` | 金融类上市公司利润表 | `sec_code` |
| `cf_fin` | 金融类上市公司现金流量表 | `sec_code` |
| `rev_by_product` | 分产品主营业务收入 | `sec_code` |
| `rev_by_industry` | 分行业主营业务收入 | `sec_code` |
| `rev_by_region` | 分地区主营业务收入 | `sec_code` |
| `audit_opinion` | 定期报告审计意见 | `sec_code` |
| `pre_disclosure_date` | 定期报告预披露时间 | `sec_code` |
| `top5_suppliers` | 公司前五大供应商信息表 | `sec_code` |
| `top5_customers` | 公司前五大客户信息表 | `sec_code` |

### 融资分配（references/catalog_financing.md，8 个接口）

| 接口 | 名称 | 额外必填参数 |
|---|---|---|
| `margin_trade` | 公司融资融券 | `target_security_code` |
| `pledge_ratio` | 单一股票质押比例 | `sec_code` |
| `issuance_plan` | 公司增发股票实施方案 | — |
| `rights_issue_plan` | 公司配股实施方案 | — |
| `ipo` | 公司首发股票 | — |
| `dividend_cap` | 公司分红转增 | — |
| `ipo_review` | 公司首发股票审核信息 | — |
| `underwriting` | 股票发行中介机构及承销情况 | — |

### 重大事项（references/catalog_events.md，6 个接口）

| 接口 | 名称 | 额外必填参数 |
|---|---|---|
| `penalty` | 公司受处罚记录 | `sec_code` |
| `arbitration` | 公司仲裁 | — |
| `litigation` | 公司诉讼 | — |
| `asset_freeze` | 公司资产冻结 | — |
| `external_guarantee` | 公司对外担保 | — |
| `related_party_trade` | 公司日常关联交易 | — |

### 股权与治理（references/catalog_governance.md，15 个接口）

| 接口 | 名称 | 额外必填参数 |
|---|---|---|
| `actual_controller` | 公司实际控制人 | `sec_code` |
| `capital_chg` | 公司股本变动 | `sec_code` |
| `major_sh` | 主要股东持股 | `sec_code` |
| `sh_count` | 公司股东人数 | `sec_code` |
| `top10_circulating_sh` | 十大流通股东持股变化 | `sec_code` |
| `top10_sh` | 十大股东持股变化 | `sec_code` |
| `major_sh_chg` | 大股东增（减）持情况 | `sec_code` |
| `sh_freeze` | 公司股东股份冻结 | `sec_code` |
| `sh_pledge` | 公司股东股份质押 | `sec_code` |
| `holding_concentration` | 股东持股集中度 | `sec_code` |
| `mgmt_holding` | 上市公司管理层持股及报酬 | `sec_code` |
| `management` | 公司管理人员情况 | `sec_code` |
| `employee` | 公司员工情况 | `sec_code` |
| `restricted_release_date` | 受限股份实际解禁日期 | `sec_code` |
| `restricted_listing_date` | 受限股份流通上市日期 | `sec_code` |

## 图表输出

**统一使用 `echarts-ai-skill` 生成图表（交互式 HTML）。不要探测或使用 matplotlib、mplfinance、pyecharts 等 Python 绘图库**——本机不作为绘图路线，探测它们只会产生报错。也不要执行 `pip install` 安装绘图库。

用户需要可视化时，将查询结果交给 `echarts-ai-skill` 技能渲染（交互式 HTML，浏览器打开查看）：

1. 用本技能查询数据后，将 `data` 数组整理为 `ChartRequest` JSON（`dataset` 即行数组，字段名对应接口返回字段）。
2. 调用 echarts-ai-skill 的命令生成图表（工作目录为其技能目录）：
   ```powershell
   node dist\cli\generate-chart.js --input <request.json> --out <option.json>
   node dist\cli\render-chart.js --input <option.json> --format html --out <输出路径.html>
   ```
3. 用 `start <输出路径.html>` 为用户打开浏览器查看。

**常用图表映射**：

| 需求 | ChartRequest 要点 |
|---|---|
| K 线图 | `chartType: "candlestick"`，`xField: trade_date`，`openField: open`，`closeField: close`，`lowField: low`，`highField: high`（数据来自 `daily_quote_hist`，fields 至少取这五个字段） |
| 折线（趋势） | `goal: "trend"`，`xField` 为日期字段，`series` 为指标字段列表 |
| 柱状（对比） | `goal: "comparison"`，`categoryField` 为分类字段，`valueField` 为数值字段 |
| 饼图（构成） | `goal: "composition"`，一个分类字段 + 一个数值字段（如收入构成 `rev_by_product`） |

复杂需求可用 `rawOption` 透传任意 ECharts 配置。
