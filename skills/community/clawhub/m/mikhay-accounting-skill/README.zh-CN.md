[English](README.md) · [中文](README.zh-CN.md)

# Mikhay 记账技能

技能版本 `0.4.2`（见 `SKILL.md` frontmatter）。账本 `schema_version` 仍是 `0.3.0`，记录格式保持兼容。未改动的 `0.2.0` 账本仍能通过校验，统计结果不变。

安装：`npx skills add MikhayEeer/mikhay-accounting-skill`

主页：https://github.com/MikhayEeer/mikhay-accounting-skill

协议：MIT，版权人 MikhayEeer。全文见 [LICENSE](LICENSE)。

面向中文个人账本，处理 CSV、JSON、XLSX。给代理看的操作说明在 `SKILL.md`（中文）。常见错误见 `references/faq.md`，报错恢复见 `references/troubleshooting.md`。

显示名：`Accounting|记账 - 资产管理/信用卡/预购清单/年月统计`。

## 隐私

本技能面向中文个人账本。流水、资产快照和愿望清单只留在本地的 `data/`、`raw/`、`exports/`。脚本不会上传账本。

## AI native 记账和传统记账的区别

这不是又一个记账 App。账留在本地文件里，由 agent 按脚本记账，而不是填一屏表单。

1. **入口只有对话。** 文字、语音转写、截图都发给你正在用的 agent。截图能不能认出来，取决于你选的模型有没有视觉（VL）能力。本技能不做 OCR，也没有单独的截图导入入口。识别之后，由 agent 按 `categories.md` 整理成标准记录。
2. **账户和类别是用户自己的数据。** 技能只自带一套推荐清单，agent 应该把用户真实的账户（含 `别名`）写进 `data/accounts.json`，把真实分类写进 `data/categories.json`。「微信」「建行」「花呗」会通过别名归一到正式账户名。未知账户或类别默认只警告，`validate_ledger.py --strict` 才当错误。没把握就在备注写 `待确认` 并问一次，然后把答案写进配置，不要硬塞默认值。
3. **校验是安全网。** 每次写入后，对涉及的分片跑 `validate_ledger.py` 和 `lint_ledger.py`。合计只抄脚本输出，模型不手算。技能没法强制挂钩子；这两个命令没跑，就不要说「已记录」。
4. **预算是花钱前问一句。** 不做信封预算表。你说「想买某样东西」，agent 对照愿望清单的额度桶、信用敞口和冷静期给出判断（`analyze_wishlist.py`）。
5. **提醒和市值交给你自己的定时任务。** 技能只把到期事项写成数据：还款日、续费日、冷静期结束、固定支出缺月。它不查行情，也不自己跑定时器。想定期提醒，或想定期记一笔市值快照，在宿主 agent 上自己设定时任务，避免这个技能为了轮询把 token 花掉。
6. **本地纯文本。** JSON 和 CSV 放在 `data/`。用 git 还是网盘备份，由你决定。不做云同步。
7. **刻意不做的：** 图表和看板、手动录入表单、App 内 OCR、银行直连和自动同步、行情追踪和收益率、完整的拆分交易、多人共享账本、信封预算界面、广告和理财推荐。

账本里已经写成「收入/报销」的旧记录保持原样，仍然算收入。`scripts/migrate_0_3.py` 只打印预览，`--apply` 会拒绝。要不要改成新的「报销」类型，由用户自己决定。agent 看到旧写法时要说明这一点，不要擅自改写。

待报销的钱算实际花销。到账时优先改原记录，而不是新增第二条：全额报销把金额改成 `0`，部分报销保留剩余金额，多报的部分把这条改成 `收入` 的差额；需要时把 `报销状态` 写成 `已报销`。只有原记录无法改动时，才另记一条 `报销` 并用 `reimburse_of` 指向原支出。退款和 AA 同理：一件事一条记录，`0` 是合法金额。不报「预计实际花销」。

投资账户计入净资产。市值只来自用户要求记下的快照，有快照才打印浮动盈亏，不预测行情。

## 账户、类别与别名

账户和类别是配置，不是代码。所有脚本都会自动读取账本旁边或工作目录下的 `data/accounts.json`、`data/categories.json`，每个命令也支持 `--accounts PATH` / `--categories PATH`。

```json
{
  "accounts": [
    {"账户": "招商银行", "别名": ["招行", "CMB"], "账户类型": "资产"},
    {"账户": "花呗", "别名": ["支付宝花呗"], "账户类型": "负债", "信用卡": true}
  ]
}
```

```json
{
  "categories": {"宠物": ["猫粮", "疫苗"]},
  "subcategory_aliases": {"猫食": "猫粮"}
}
```

`replace_defaults: true` 会丢弃默认清单，让文件成为完整定义。配置之外的账户或类别默认只警告；要硬卡就用 `--strict`。账户上加 `投资账户: true` 可以明确投资方向。别名历史窗口也写在同一个文件里，格式是 `{"名称", "起", "止"}`；不再有单独的 `aliases.json`。

`data/settings.json` 改本位币和赎回标记：

```json
{"base_currency": "CNY", "invest_out_subcategory": "赎回"}
```

没写 `currency` 的流水用本位币；外币流水会另按原币合计。`data/import_rules.json` 可以替换导入关键词表、兜底类别和来源账户映射，见 `import_rules.md`。

## 导入导出

**重新导入可能丢数据。** `scripts/import_ledger.py` 默认拒绝覆盖已有账本文件，除非显式加上 `--overwrite`。任一目标路径已存在时，整批中止，一个文件都不写。脚本在写入前用 `Path.exists()` 检查。`--overwrite` 会整文件替换每个目标分片；新账单里没有的旧流水会从该文件消失。使用该标志前先备份 `data/`。这道门由脚本执行，不是只靠先问一句。

把 CSV 或 XLSX 导入为标准 JSON：

```bash
python scripts/import_ledger.py raw/bill.csv --output data/imported.json
```

按月拆分导入：

```bash
python scripts/import_ledger.py raw/bill.csv --split-by-month --year-dirs --output data/ledger
```

备份之后，才用 `--overwrite` 替换已有分片：

```bash
python scripts/import_ledger.py raw/bill.csv --shard month --year-dirs --output data/ledger --overwrite
```

把标准 JSON 导出为 CSV：

```bash
python scripts/export_ledger.py data/ledger/2026/2026-06.json --output exports/2026/2026-06.csv
```

真实账本推荐按年月分片：`data/ledger/YYYY/YYYY-MM.json`。按日分片：`data/ledger/YYYY/YYYY-MM/YYYY-MM-DD.json`。

```bash
python scripts/import_ledger.py raw/bill.csv --shard day --year-dirs --output data/ledger
python scripts/import_ledger.py raw/bill.csv --shard month --year-dirs --output data/ledger
```

分片键只用文件名（`os.path.basename`）。`data/ledger/2026/2026-06.json` 的月份键是 `2026-06`。不要截取整段路径，否则会得到错误键 `r/202`。

校验：

```bash
python scripts/validate_ledger.py data/ledger/2026/2026-06.json
python scripts/validate_ledger.py data/ledger
```

## 花销与内部转账

统计一律跑脚本，不要手算。脚本会扫描传入的全部分片。

```bash
python scripts/summarize_ledger.py data/ledger
python scripts/summarize_ledger.py data/ledger --buckets examples/buckets.sample.json
python scripts/summarize_tags.py data/ledger
```

两套口径：

- **花销**：支出毛额减去退款。退款（`收支类型=退款` 或 `refund_of`）不是收入，也不算一笔新的消费。报表同时给出毛额和净额。全额退款、全额报销或 AA 后净额为 0 时，直接把原记录的金额改成 `0`，不要新增记录。
- **内部转账**：账户之间的 `转账`。`pairid` 成对的两条腿只计一次。转账不进入花销。

标签命名空间自由：任何「字母开头的 prefix:suffix」都合法（`trip:`、`event:`、`project:`、`pet:`）。`summarize_tags.py` 对每个标签给出毛额、净额、按日合计，以及类别行上的占比。

可选字段还包括 `currency`（默认是配置的本位币，初始 `CNY`）、`original_amount`、`fx_rate`、`cny_amount`。主合计使用本位币 `金额`，外币流水另按原币列一节。新写出的 JSON 带 `schema_version`。旧账本没有这些字段也能用。

## 净资产与信用卡

```bash
python scripts/summarize_assets.py data/assets/2026/2026-06.assets.json --cc-method A
python scripts/summarize_assets.py data/assets/2026/2026-06.assets.json --forecast --as-of 2026-06-15
python scripts/project_assets.py data/assets/assets.json data/ledger/2026/2026-06.json
```

账户有 `included` 和 `excluded`（备查）两种。净资产分成「计入净资产」和「备查账户」两段。默认备查示例：Apple Card、公积金、助学贷款、加密货币，可在 `data/accounts.json` 改。

信用卡余额默认用方法 A：最近快照 + 快照之后的流水。方法 B 从零重放该卡流水、不用快照。输出会写明用的是哪一种。

`--forecast` 给出每张卡的预计账单、预计还款、还款日和本月现金流。技能不猜发薪日；想要工资行就自己记账。

## 资产

查询总资产、总负债、净资产、分期和还款提醒：

```bash
python scripts/summarize_assets.py data/assets/2026/2026-06.assets.json
```

记账会影响资产统计。直接改资产快照时，先报差额，再问要不要写调整分录。`project_assets.py --write` 只有带上该标志才会把推算视图写进资产文件。

## 预购清单

分析想买物品的经济压力、购买建议和优先级：

```bash
python scripts/analyze_wishlist.py data/wishlist/2026/wishlist.json --ledger data/ledger/2026/2026-06.json --assets data/assets/2026/2026-06.assets.json
```

预购清单不是账本记录。真正购买之后再写 `支出`。

## 维护者封装

`tools/package_skill.py` 只给维护者用，不是终端用户的记账命令。ClawHub 发布通过 `.clawhubignore` 忽略 `tools/`。打出来的压缩包本身也不含 `tools/` 和 `package_skill.py`。

```bash
python tools/package_skill.py
```

输出位置：

```text
dist/mikhay-accounting-skill.tar.gz
dist/mikhay-accounting-skill.zip
```

包内包含技能、参考文档、导入规则、`scripts/`、虚构示例、两份 README 和 `LICENSE`，不包含 `VERSION`、`tests/`、`.github/`、`tools/`、`data/`、`raw/`、`exports/`、`.claude/`、`.codex/`。`MANIFEST.json` 里的版本与 `SKILL.md` 的 `version` 相同。`.clawhubignore` 同样排除 `tests/` 和 `.github/`，发布到注册表时也不会打进包里。

## 使用 skill 与不使用 skill 的对比

以一份没有放进本仓库的本地样本，做一次本地（Claude Code，GLM-5.2）校验、月度统计、分类 Top 为例。下面的耗时和 token 是当时的量级，不是仓库里的示例文件。

| | 不使用 skill（纯 LLM 推理） | 使用 skill（脚本 + 短指令） |
|---|---|---|
| 输入 token | 需将 schema、类别表、规则口头说明给模型，或模型靠记忆推理，约 2–4k token 规则加上全量记录约 15k token | 先读 SKILL.md，再按需打开 schema、categories 或 references |
| 推理 token | 样本逐条分类、求和、别名归一化，输出长且易错，约 8–15k 输出 token | 几乎不推理，只发 2 条 Bash 命令 |
| 输出 token | 完整报表手写，约 1–2k | 脚本结果，约 300–500 token |
| 延迟 | 单轮 30s 到 1min 以上，多轮纠错更久 | 2 次 Bash 调用，约 3–8s |
| 准确性 | 求和与别名归一化经常出错，上百笔难一次算对 | 确定性正确，与对账文件完全一致 |
| 总 token | 约 25–35k | 约 3–5k |

## 结论

- Token：使用 skill 大约节省 5–8 倍，主要省在不必把规则塞进上下文、不必由模型逐条算账。
- 速度：使用 skill 快约 5–10 倍，从可能需要纠错 2–3 轮变为一次跑通。
- 质量：差距最大。纯 LLM 做金额求和与别名归一化，容易出现几百元误差；脚本是确定性的，零误差。

如需长期记账（录入新交易、按月出报表、查异常），建议把本 skill 放到对应工具支持的 skill 目录下，按「读 schema、跑 validate、跑 summarize、只回报脚本给出的总数与异常」执行。标签、分类占比和净资产都由脚本扫描全部分片后给出，不要手算。

测试：

```bash
python -m pytest -q
```
