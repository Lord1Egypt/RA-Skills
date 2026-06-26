# price-check

> English docs: [README.md](README.md)

[OpenClaw](https://openclaw.ai/) skill，做**三件事**让你网购决策更省心：

1. **搜全网最低价** —— 一次查询，22+ 个国内电商平台横向对比（淘宝/天猫、京东、拼多多、苏宁、唯品会、考拉、抖音、快手、1688）。同关键词的配件、翻新机、套装、激活可疑、SKU 不匹配等混淆商品自动过滤掉，只留**真正可信的购买候选**
2. **告诉你"该不该买"** —— 不只是给价格列表，而是给"强烈推荐 / 可以买 / 再等等 / 数据质量不足"的明确建议，附**具体依据**（"可信最低价 ¥X 比 N 平台中位数 ¥Y 低 K%"），并自动拉取**直接可点击的购买链接**（淘宝淘口令、京东短链）
3. **监控历史价** —— 每次查询自动写入本地 SQLite，**多查几次同商品后**自动激活"该商品历史最低 ¥X / 最高 ¥Y / 当前处于低位/中位/高位"识别，能捕捉"先涨后降"的假促销陷阱

可选叠加：把每次查询自动同步到飞书多维表格，方便手机/电脑跨设备刷历史 + 标记"已购"。

在你的 OpenClaw bot 飞书对话里说一句：*"iPhone 17 Pro 256G 现在合适入手吗？哪里最便宜？"* —— 你会拿到一份完整 6 段报告：警告区 / 最划算+链接 / Top 3 候选表 / 历史价 / 我的建议 / 透明度。

## 内部实现细节

- **多平台实时比价** —— 一次查询拉 22+ 候选，数据来源 `maishou88.com`（v0.5 起内置客户端，不依赖外部 skill）
- **三层噪音过滤**先做完 verdict 才有意义：
  1. **价格层** —— 剔除底部 outlier（`price < raw_median × 0.3`），过滤掉配件 / 数据线 / 钢化膜等同关键词杂物
  2. **信任层** —— 7 档 condition 识别（refurbished / bundle / accessory / activation_questionable / parallel_import / trusted_domestic / unknown）+ 店铺信任度（Apple 自营 / 京东自营 / 品牌官方旗舰店）
  3. **相关性层** —— title token 命中率（含 G ↔ GB 等价匹配），匹配度 < 0.75 或多型号堆砌（"V8 V10 V11 V12 V15" 这种模糊 listing）会被过滤
- **verdict 升降档** —— 当前价处于该商品历史低位时升档"强烈推荐"；命中"先涨后降"时降档"别买"
- **本地优先的历史价** —— 不依赖外部接口，越用越准，识别你的购物偏好
- **零配置即用** —— 装上就能跑。飞书同步默认关闭，不用就完全不用配（不需要装 lark-cli）

## 架构

```
用户问"X 多少钱合适买"
    ↓
OpenClaw bot (Molty) 识别触发词
    ↓
调用：uv run bin/price_check.py "X"
    ↓
shopmind._fetch_search_items()         # 数据层（不修改上游）
    ↓
[1] _filter_outliers()                 # 价格层
    ↓
[2] _select_best_deal()                # 信任层 × 相关性层
    ↓
_enrich_with_urls()                    # 并发拉 buy_url / 淘口令
    ↓
LocalDBHistoryProvider.get_history()   # 读本地 SQLite 积累的快照
    ↓
compute_verdict() + compute_trap_warning()
    ↓
JSON 到 stdout  +  写本地 SQLite  +  （可选）飞书 Bitable 同步
    ↓
Bot 渲染 6 段报告（C 模式：警告 / best_deal+链接 / Top 3 表 / 历史价 / 我的建议 / 透明度）
```

## 依赖

- **必须**：`python3` ≥ 3.10、`uv`（OpenClaw skill metadata 自动处理）
- **可选**：`lark-cli`（只在启用飞书同步时需要）

> v0.5+ **自包含**，不依赖任何外部 skill。`maishou88.com` 数据层客户端在 `bin/_data_layer.py`，衍生自 [shopmind-price-compare](https://clawhub.ai/skills/shopmind-price-compare) —— 详见 致谢段。

## 安装

```bash
# 通过 OpenClaw（推荐 — skill 自动识别）
openclaw skills install price-check
# 或手动 clone 到 OpenClaw workspace：
git clone https://github.com/yuxiaoyang2007-prog/price-check.git \
  ~/.openclaw/workspace/skills/price-check
```

## 用法

### 直接 CLI

```bash
uv run ~/.openclaw/workspace/skills/price-check/bin/price_check.py "iPhone 17 Pro 256G"
# stdout 输出 JSON
```

CLI 参数：

- `--source <N>` —— 限制单平台（0=全部，1=淘宝，2=京东，3=拼多多 ...）
- `--page <N>` —— 翻页
- `--no-cache` —— 忽略 30 分钟查询缓存，强制重新拉数据

### 通过 OpenClaw bot（自然语言）

在飞书里对你的 OpenClaw bot 说：

```
"iPhone 17 Pro 256G 现在合适入手吗？哪里买最便宜？"
"戴森 V15 比价"
"Switch 2 港版 哪里买"
```

Bot 识别触发词（`比价` / `值不值得买` / `哪里买` / `多少钱合适` 等），调脚本，按 C 模式 6 段格式渲染报告回你。

## 可选：启用飞书多维表格同步

把每次查询（best_deal + Top 3 + 历史价）同步到飞书 Bitable，方便手机/PC 飞书 App 跨设备浏览。**默认关闭**，想用才需要做。

1. 装 `lark-cli`
2. 在飞书云空间建一张空多维表格
3. 把你的飞书 Bot 应用授权为该 Bitable 的编辑者
4. 跑一次性配置脚本：

```bash
uv run ~/.openclaw/workspace/skills/price-check/bin/setup_feishu.py \
  'https://your-tenant.feishu.cn/base/<BASE_TOKEN>?...'
```

脚本会自动建 31 个字段（查询词 / verdict / best_deal 价格 / 平台 / 店铺 / 标题 / 链接 / Top2 链接 / Top3 链接 / 匹配度 / Condition / 中位数 / 历史最低 / 历史最高 / 历史均价 / 当前位置 / Trap 提示 / 标记已购等），并把配置写到 `~/.openclaw/data/price-check/config.json`。

如需关闭：编辑该 config，把 `feishu_sync.enabled` 改成 `false`。

## 配置

所有可选配置都在 `~/.openclaw/data/price-check/config.json` —— 完整字段参考 [config.example.json](config.example.json)。主要分组：

- `storage.cache_ttl_seconds` —— 查询缓存 TTL（默认 1800 秒）
- `history_provider.type` —— `local_db`（默认）或 `noop`
- `history_provider.min_query_history` —— market 历史价生效的最低查询次数（默认 3）
- `history_provider.min_goods_history` —— 商品历史价生效的最低快照数（默认 2）
- `feishu_sync.enabled` —— opt-in 开关（默认 false）
- `feishu_sync.base_token` / `table_id` / `lark_cli_profile` —— 由 `setup_feishu.py` 自动写入

## 本地数据布局

```
~/.openclaw/data/price-check/
├── price-check.db       # SQLite — 三张表：queries / price_snapshots / query_cache
└── config.json          # 可选 — 不存在时走默认值
```

直接用 sqlite3 命令查历史：

```bash
sqlite3 ~/.openclaw/data/price-check/price-check.db \
  "SELECT queried_at, query, verdict FROM queries ORDER BY id DESC LIMIT 20"

# 备份
cp ~/.openclaw/data/price-check/price-check.db ~/Backups/

# 重置（删除所有数据）
rm -rf ~/.openclaw/data/price-check/
```

## Roadmap

- **v0.5** —— SKU 关键词模糊匹配（如 "V12 plus" 与 query "V12 Pro" 同义识别）
- **v0.5** —— 运营商京东自营店单独识别一档（中国联通 / 移动 / 电信 —— 当前算可信但实际是合约机风险偏高）
- **v0.6** —— `best_deal.url` 改回按需拉取；飞书 Bitable 加价格历史可视化图
- **v1.0** —— `HistoryProvider` 接入外部数据源（慢慢买 / 什么值得买 / 京东价保 API 等）

## 隐私

- **所有数据本地保存**。SQLite 是本地文件，除非你主动启用飞书同步，否则不会有任何外部写入
- `config.json` 里可能含飞书 `base_token`，**不要**提交到版本控制（已在 `.gitignore` / 仓库路径外）
- 本 skill **不**追踪任何用户身份 / 购买记录 / PII

## License

MIT —— 详见 [LICENSE](LICENSE)。

## 致谢

**`maishou88.com` 数据层客户端**（`bin/_data_layer.py`）**衍生自** [shopmind-price-compare v2.2.0](https://clawhub.ai/skills/shopmind-price-compare)，作者 **[xiaohaook](https://clawhub.ai/users/xiaohaook)**。具体 HTTP 端点、请求体格式、默认 headers、OPENID 种子、items 构造逻辑均复用自上游 —— 全部归功原作者。

我们选择内化该数据层（而非把 shopmind 作为独立 skill 依赖），是为了让 `price-check` 自包含——用户只需装一个 skill。**如果原作者对此有异议，我们会立即改成 clean-room 重写**。

其他：

- 运行平台：[OpenClaw](https://openclaw.ai/) —— agent runtime
- 历史价灵感来自 [慢慢买](https://www.manmanbuy.com/)
