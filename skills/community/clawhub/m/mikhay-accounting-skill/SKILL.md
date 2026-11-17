---
slug: mikhay-accounting-skill
displayName: "Accounting|记账 - 资产管理/信用卡/预购清单/年月统计"
version: 0.4.2
summary: "Accounting / 中文个人记账。账户和类别由用户定义，可配置别名；流水、资产快照、信用卡和愿望清单分开存放；合计只抄脚本；退款不是收入；净额写成同一条。"
license: MIT
name: mikhay-accounting-skill
description: Chinese personal accounting workflow for CSV/JSON/XLSX ledger, asset, and wishlist files. Use when the user asks to import, export, record, classify, validate, summarize, store, analyze records, or evaluate planned purchases with fields like 时间, 收支类型, 金额, 类别, 子类, 账户, 备注, tags, note; supports user-defined accounts and categories with aliases in data/accounts.json and data/categories.json, 支出, 收入, 还款, 转账, 退款, 报销, zero and netted amounts, trip/event/person/nature tags, day or month shards, transfer pairs, multi-currency CNY totals, included and excluded accounts, credit-card snapshot methods, payday forecast, third-party bill conversion, and monthly reports. Local ledger only; files are not uploaded.
metadata:
  openclaw:
    homepage: https://github.com/MikhayEeer/mikhay-accounting-skill
---

# Mikhay 记账

技能版本 `0.4.2`，账本字段 `schema_version` 仍是 `0.3.0`（记录格式向后兼容）。空版本、`0.2.0` 和 `0.3.0` 都有效。合计必须来自脚本，never hand math。没跑脚本就不要报数字。

## 重新导入会覆盖整份分片

`import_ledger.py` 默认拒绝覆盖。任一目标路径已存在且没有 `--overwrite` 时，整批中止，不写任何文件。`--overwrite` 会整文件替换该分片，新账单里没有的旧流水会丢失。先备份 `data/`。这道门由脚本执行（写入前检查路径是否存在），不是只靠先问用户。

## 隐私

面向中文个人账本。流水、资产快照和愿望清单只留在本地 `data/`、`raw/`、`exports/`。脚本不会上传这些文件。

## 不做什么

- 不把退款或报销记成收入，不把转账、还款或投资记成花销。
- 不自动改写历史「收入/报销」。旧写法继续算收入，只给警告。是否改成新的「报销」类型，由用户自己决定。`scripts/migrate_0_3.py` 只预览，`--apply` 会拒绝。
- 待报销仍算实际花销。到账时优先直接改原支出的净额（全额改 0，部分改差额，多出来的改成收入）；需要保留原始金额时才另记一条 `报销`，用 `reimburse_of` 指向原支出，并把原支出改成 `已报销`。不要报「预计实际花销」。
- 投资账户计入净资产。不查行情，不设定时任务去更新市值。只有用户要求时才记快照。用户想定期更新，自己设定时任务。
- 购买前不把愿望清单写成 `支出`，也不替用户估价格。
- 不主动做预算或消费建议。不猜发薪日，不把提醒和行情做成定时任务。不画图表，不做录入表单，不做 OCR，不直连银行。
- 不静默改分类。没有 `--overwrite` 时不覆盖已有分片。用户没要求时不写差额调整。
- 不手算合计，不跳过范围内的分片。

取舍见 `references/design-rationale.md`。

## 账户和类别由用户定义

默认清单只是推荐，不是硬编码枚举。第一次给用户记账时，按用户实际的钱包、银行卡、信用卡写 `data/accounts.json`，按用户实际的分类习惯写 `data/categories.json`；两个文件都可选，但强烈建议一开始就建。

- 账户：`账户`、`别名`、`账户类型`（资产/负债）、`纳入`（included/excluded）、`信用卡`、`投资账户`。自然语言里的「微信」「建行」「花呗」通过别名归一到正式账户名。`别名` 还可以写成 `{"名称","起","止"}` 记录改名历史。`replace_defaults: true` 可以整表替换默认清单。
- 设置：`data/settings.json` 的 `base_currency`（默认 `CNY`）决定记账本位币；`invest_out_subcategory` 可改默认的 `赎回`。多币种流水按原币另列一节，主合计用本位币。
- 类别：`categories` 下每个类目的子类列表，配 `category_aliases`、`subcategory_aliases` 归一旧叫法。某个类目写了就以配置为准，没写的类目沿用默认。
- 校验默认**只警告**未知账户和未知类别；`validate_ledger.py --strict` 才把它们升级成错误。自定义账户不要等脚本放行，直接写进配置。
- 导入关键词表在 `data/import_rules.json`：`category_keywords`、`fallback`、`source_accounts`。不改就用内置推荐表。
- 全部脚本都支持 `--accounts`、`--categories`、`--settings`（导入另有 `--import-rules`）；不给路径时自动找账本旁边或工作目录下的 `data/` 同名文件。

## 30 秒上手

1. 没有 `data/` 时按 `storage.md` 建空目录，不要编造余额。
2. 改数据前读 `schema.md`；分类前读 `categories.md`，并把账户、类别写入配置。
3. 写入之后立刻对涉及的分片跑 `scripts/validate_ledger.py` 和 `scripts/lint_ledger.py`。没跑就不要说「已记录」。
4. 回复先列错误和警告，再抄脚本总数。

## 触发示例

原话决定模块。对话全文在 `references/triggers.md`。

1. 「午饭 35，微信」→ 记账 → `支出`，金额 `-35`，`食品餐饮/午餐`，账户 `微信钱包`。
2. 「昨天午饭退了 10」→ 记账 → 直接把原支出从 `-35` 改成 `-25`；全额退就改成 `0`，不另记收入。
3. 「机票 500，报销 500」→ 记账 → 原支出改成 `0`，`报销状态=已报销`；报销 520 就改成 `收入` `+20`。一件事只留一条。
4. 「AA 之后我只花了 50」→ 记账 → 原支出改成 `-50`，不新增退款行。
5. 「支付宝还花呗 500」→ 记账 → `还款` `+500`，`note` 写 `target_account=花呗`。
6. 「建行转支付宝 200」→ 记账 → 两条 `转账`，同一 `pairid`，金额一负一正。
7. 「这个月花了多少」→ 汇总 → 只跑该月分片，报花销毛额、退款、净额。
8. 「导入这份支付宝账单」→ 导入 → `import_ledger.py` 后校验。已有分片时脚本直接拒绝；备份并确认替换后才加 `--overwrite`。
9. 「建行余额现在是 8000」→ 资产 → 追加快照；和推算不一致就先报差额。
10. 「想买机械键盘，399」→ 愿望清单 → 只写 wishlist，不写账本。
11. 「花呗这个月要还多少」→ 预测 → `summarize_assets.py --forecast`，只报账单、还款额、还款日和本月现金流，不猜发薪日。
12. 「这次旅行花了多少」→ 标签 → `summarize_tags.py` 扫完全部分片，报毛额和净额。

## 常见陷阱

细节在 `references/faq.md`，恢复步骤在 `references/troubleshooting.md`。

- 退款或报销又写成了新记录。优先直接改原记录的净额，`0` 是合法金额；只有原记录不能改时才用 `退款`/`报销` 行。
- `pairid` 只有一条。补上另一条，金额相反、账户不同；或改成单边并写 `target_account=`。
- 外币对不上。`金额` 用本位币，且等于 `original_amount * fx_rate`（误差 0.01 以内）。
- 类别或账户不在清单里。默认清单只是推荐：写进 `data/categories.json` / `data/accounts.json` 后重跑校验。当场不确定就在备注写 `待确认` 并问用户，不要硬塞默认值。
- 账户写成了别名。别名会归一到配置里的正式名；回复时用正式名，不要两个名字混用。
- 没有 `data/`、JSON 损坏，或同一账单导入了两次。先停写，说清原因，再问下一步。

## 错误处理

出错时不要只回「已记录」或「有问题」。说明类别、原因、卡住的字段或路径，以及下一步。完整分类见 `references/troubleshooting.md`。

- 缺字段：列出缺项并提问，不要用空字符串凑记录。
- 格式错误：指出哪个值和 `schema.md` 不符，并给出改后的样子。
- 校验失败：贴出 `INVALID` 的第一条原因，改完再跑 `validate_ledger.py`。只有警告时，说明缺的账户或类别要写进哪个配置文件。
- 找不到文件：说明路径不存在。按 `storage.md` 建空目录，不要编余额。
- 文件损坏：引用 JSON 解析错误。保留坏文件。从 `raw/` 重导到新路径，或在备份后用 `--overwrite` 替换。没有该标志时脚本不会覆盖。
- 重试：校验和汇总可以重跑。导入在目标已存在时失败退出，除非加上 `--overwrite`。没备份、用户没明确要替换时不要加这个标志。同一条 `INVALID` 重复出现就停。

## 按需阅读

- 字段和符号：`schema.md`。定位或写入分片：`storage.md`。
- 分类与 `data/categories.json`：`categories.md`。账户、别名、投资账户与 `data/accounts.json`、余额、信用卡：`accounts.md`。本位币、导入关键词：`schema.md` 与 `import_rules.md`。
- 第三方账单：`import_rules.md`。愿望清单：`wishlist.md`。
- 常见错误：`references/faq.md`。报错和恢复：`references/troubleshooting.md`。
- 设计取舍：`references/design-rationale.md`。示例对话：`references/triggers.md`。
- 端到端：`examples/workflow-import-monthly.md`、`examples/workflow-credit-repay.md`、`examples/workflow-fix-records.md`。

## 脚本

- `scripts/summarize_ledger.py`：花销和内部转账。
- `scripts/summarize_tags.py`：标签合计，扫完整棵给定目录。
- `scripts/summarize_assets.py`：计入净资产、备查、`--cc-method`、`--forecast`（只报账单与本月现金流）。
- `scripts/project_assets.py`：最近快照加上之后的流水，得到推算余额。
- `scripts/validate_ledger.py`：相信文件之前先跑；加 `--strict` 才把自定义账户/类别当错误。`scripts/lint_ledger.py`：只读，查近似重复、别名和固定支出缺月。
- `scripts/import_ledger.py <file> --shard month --year-dirs --output data/ledger`：转到标准 JSON。目标已存在则整批失败；备份后加 `--overwrite` 才会替换。
- `scripts/export_ledger.py`：导出 CSV。`scripts/analyze_wishlist.py`：购买压力。`--due` 给出冷静期到期清单。
- `scripts/summarize_items.py`：订阅和物品，不进净资产。`scripts/migrate_0_3.py`：只预览，不改文件。

## 数据规则

- `收支类型` 只接受 `支出`、`收入`、`还款`、`转账`、`退款`、`报销`、`投资`。
- `金额` 可以是 `0`：全额退款、全额报销、AA 净额为 0 都保留原记录，只把金额改成 0。
- `支出` 为负；`收入`、`还款`、`退款`、`报销` 为正。成对转账和投资一正一负。净额超过支出时，把这条改成 `收入` 的差额。
- 实际花销 = 支出毛额 − 退款 − 已报销。待报销先留在实际花销里。内部转账和投资净投入分开报，不进花销，也不进收入。
- 缺币种即 `base_currency`（默认 `CNY`，可改）。主合计用本位币 `金额`，外币另列原币合计。
- 标签命名空间自由：任何「字母开头的 prefix:suffix」都合法（`trip:`、`event:`、`project:`、`pet:` 都行）。裸标签只警告。`item_id` 不是标签。
- 账户由 `data/accounts.json` 定义，带 `别名`（含改名历史窗口）；分 `included` 与 `excluded`（备查）。净资产分开打印。基金、证券用 `account_policy` 或账户配置的 `投资账户: true` 声明，计入净资产。类别由 `data/categories.json` 定义。
- 信用卡默认 `debt_only`：只报欠款和还款日。方法 A（最近快照 + 快照后流水）。输出要写明算法。
- 新 JSON 写 `schema_version` `0.3.0`。没有该字段或仍是 `0.2.0` 也有效。
- 直接改快照时，若和推算不一致，先报差额，再问要不要调整。市值快照只在用户要求时追加。

## 回复

任何写入之后，先跑 `validate_ledger.py` 和 `lint_ledger.py`，回复开头列出错误和警告。脚本没法强制挂钩子，所以没跑这两个命令就不能说「已记录」。

- 先抄脚本总数，再写类别要点和占比。
- 查过资产就写明信用卡算法。有待报销就列出明细和已等待天数，不要把它从实际花销里扣掉，也不要用固定天数判断是否异常。
- 警告和 `待确认` 单独列出。看到旧的「收入/报销」时告诉用户：统计仍按收入，改不改由用户决定。
- 失败时写原因和下一步，不要只做简短确认。
- 用户没要时不要倾倒全部流水。提醒和市值更新交给用户自己的定时任务，不要在技能里轮询。
