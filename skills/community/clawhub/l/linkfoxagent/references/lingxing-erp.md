# 领星 ERP OpenAPI（编排说明）

本说明供 **linkfoxagent** 编排使用。领星数据**不是** LinkFoxAgent 内置 74 工具之一；通过领星官方开放接口拉数时，认证与请求发往 **`openapi.lingxing.com`**（非 LinkFox 自建业务网关）。CLI 脚本已随本 skill 提供：**`scripts/lingxing.py`**（与 `scripts/linkfox.py` 同级），约覆盖 **373** 类接口场景；具体接口名以 **`python3 scripts/lingxing.py --api help`** 与领星官方 OpenAPI 文档为准。

## 何时使用

- 用户提到领星、Lingxing、领星开放接口、领星广告报表、订单 / Listing / 库存 / FBA / 利润、领星 SID、多平台订单等，且需要**拉取 ERP 侧真实数据**时。
- 需已在领星 ERP → **开放接口** 中创建应用，取得 **AppID / AppSecret**。

## 环境变量

```bash
export LINGXING_APP_ID=your_app_id
export LINGXING_APP_SECRET=your_app_secret

# 可选：默认店铺 SID，减少每次在 --params 里传 sid
export LINGXING_SID=your_sid
```

## 脚本用法（须在 linkfoxagent 技能根目录执行）

工作目录为 **`linkfoxagent` 技能根目录**（即同时包含本仓库中的 `SKILL.md` 与目录 `scripts/` 的那一层；其中已有 `scripts/linkfox.py` 与 **`scripts/lingxing.py`**）。在该目录下执行下列命令，勿在任意路径调用。

```bash
# 列出已授权店铺，获取 SID
python3 scripts/lingxing.py --list-stores

# 查看全部接口名（自行对照领星官方文档补全参数）
python3 scripts/lingxing.py --api help

# 单次调用（JSON 参数为一行字符串）
python3 scripts/lingxing.py --api <接口名> --params '<JSON参数>'

# 自动翻页拉全量
python3 scripts/lingxing.py --api <接口名> --params '<JSON参数>' --all

# 自定义每页条数
python3 scripts/lingxing.py --api <接口名> --params '<JSON参数>' --all --page-size 50
```

标准输出为 JSON；翻页进度在 stderr。

## 与 linkfoxagent 的协作方式

- 主会话仍应遵守 **本 agent** `SKILL.md` 中的 **`sessions_spawn`** 等约定；子会话若需调领星，应在任务里写清：**先 `cd` 到 `linkfoxagent` 技能根目录**（见上）再执行 `python3 scripts/lingxing.py ...`，避免路径错误。
- 各接口的必填字段、分页字段、`sid` / 时间格式等以 **领星官方 OpenAPI 文档** 及 **`python3 scripts/lingxing.py --api help`** 所列接口名为准；不同接口差异较大，勿凭猜测拼参数。

## 调用示例

```bash
python3 scripts/lingxing.py --list-stores
export LINGXING_SID=813

python3 scripts/lingxing.py \
  --api spCampaignReports \
  --params '{"report_date": "2024-01-01"}'

python3 scripts/lingxing.py \
  --api mwsOrders \
  --params '{"start_date": "2024-01-01", "end_date": "2024-01-31"}' --all

python3 scripts/lingxing.py \
  --api profitAsin \
  --params '{"sids": "813", "start_date": "2024-01-01", "end_date": "2024-01-31"}'
```

其余模块（新广告报表、财务、仓库、采购、客服、多平台等）在确认接口名后，按同一 `--api` / `--params` / `--all` 形式调用即可。
