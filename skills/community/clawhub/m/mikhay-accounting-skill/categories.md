# Categories

The category list is a recommendation, not a hard enum. The shipped starter set is deliberately generic. Agents should align it with the user's real life and write anything custom into `data/categories.json`.

## Where Categories Live

Recommended path:

```text
data/categories.json
```

Shape:

```json
{
  "replace_defaults": false,
  "categories": {
    "宠物": ["猫粮", "疫苗", "玩具"]
  },
  "category_aliases": {"健康医疗": "医疗健康"},
  "subcategory_aliases": {"猫食": "猫粮", "停车": "停车费"}
}
```

- `replace_defaults: true` drops the starter categories entirely, so the file becomes the complete list.
- An entry under `categories` replaces that category's subcategory list. Categories not named in the file keep their starter values.
- `category_aliases` and `subcategory_aliases` normalize old or spoken variants to a canonical name.
- `scripts/validate_ledger.py`, `scripts/import_ledger.py`, and the summarize scripts find `data/categories.json` next to the ledger shard or in the working directory. Any command also accepts `--categories PATH`.
- Unknown category or subcategory is a **warning** by default, not an error. `validate_ledger.py --strict` promotes it to an error when you want a hard gate.

## Starter Categories

```text
- 食品餐饮: 早餐, 午餐, 晚餐, 正餐, 外卖, 买菜, 生鲜, 水果, 零食, 饮料, 饮料酒水, 咖啡, 聚餐, 其他
- 出行交通: 打车, 公交地铁, 加油, 停车费, 高速费, 火车, 飞机, 住宿, 维修, 其他
- 购物消费: 服饰运动, 数码, 日用百货, 礼品, 虚拟充值, 其他
- 服饰美容: 服装, 美容, 其他
- 居家生活: 水费, 电费, 燃气费, 宽带, 物业费, 家政, 其他
- 生活服务: 超市, 快递, 理发, 洗衣, 其他
- 医疗健康: 挂号, 门诊, 药品, 体检, 其他
- 休闲娱乐: 电影, 游戏, 旅游度假, 运动, KTV, 其他
- 教育学习: 书籍, 课程, 考试, 文具, 其他
- 人情往来: 红包, 礼物, 聚会, 其他
- 通讯网络: 话费, 流量, 订阅, 其他
- 收入: 工资, 奖金, 补贴, 利息, 其他
- 还款: 信用卡还款, 贷款还款, 其他
- 转账: 个人转账, 其他
- 退款: 退款, 其他
- 报销: 差旅, 餐饮, 交通, 其他
- 投资: 买入, 赎回, 定投, 其他
```

## Not Shipped On Purpose

Older releases hardcoded one person's habits: 祭祀用品, 棋牌桌游, 白条还款, 月付还款, AI订阅, 外汇, 交通工具, 请客吃饭, 休闲零食, 家居用品, 手机数码, 医院看病, 买药, 检查费, 洗护, 政务, 清洁用品 and 纪念品. They are gone from the default list. Keep them in `data/categories.json` if they fit the current user; do not assume them for someone else.

## Legacy Aliases

The scripts still normalize these automatically:

| Old | New |
|---|---|
| `健康医疗` | `医疗健康` |
| `停车` | `停车费` |
| `高速费用` | `高速费` |
| `酒水饮料` | `饮料酒水` |
| `白条还款` | `信用卡还款` |
| `月付还款` | `信用卡还款` |
| `证券入金` | `买入` |

## Classification Rules

- Any category the user agrees on is valid once written to `data/categories.json`. Do not force a real user's vocabulary into the starter list.
- Prefer reusing an existing subcategory before adding a new one. When the user corrects a name, update `data/categories.json` (or the alias map) so the next record matches.
- `收支类型=收入` should use `类别=收入`; `还款`, `转账`, `报销`, `投资` and `退款` have the same default pairing. A mismatch only warns, so a netted row can keep its original category when the user prefers that.
- `收支类型=退款` may use the expense category being reversed. It must not be reported as `收入`.
- Unknown category or subcategory: put `待确认` in the note and ask the user once. Do not invent silently. Then persist the answer in `data/categories.json`.
