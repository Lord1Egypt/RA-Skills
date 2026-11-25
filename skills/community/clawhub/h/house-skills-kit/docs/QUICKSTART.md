# 快速上手（QUICKSTART）

> 面向**真正要用它干活的人**：案场顾问、二手经纪人、策划、营销负责人、购房者。
> 读完这一页大约 5 分钟，之后你应该能：装好、问对、拿到能直接用的交付物。

## 0. 先搞清楚这是什么

> 只想快点找到该用哪个技能 → **[技能地图 SKILL-MAP.md](SKILL-MAP.md)**；想看完整上手流程 → 继续往下读。

不是软件包，不需要 `pip install`，不联网、不调 API。

一个技能 = 三件东西：

| 文件 | 作用 | 什么时候读 |
|---|---|---|
| `SKILL.md` | 技能说明书：适用角色、触发场景、**必问信息**、输出格式、合规红线 | 每次用之前先读（1~2 分钟） |
| `<topic>-playbook.md` | 方法正文：Part 1..N，每 Part 是"玩法 → 示例 → 翻车警示" | 需要动手做时读对应 Part，**不要一次全读** |
| `README.md` | 安装者视角：适用谁、怎么用、输出纪律 | 装的时候看一次 |

`skills/calc-toolkit/` 是唯一的可执行部分：纯 Python 标准库，20 个计算器，跑之前在命令行里跑。

---

## 1. 三种装法（选一种就行）

### 装法 A：Claude Code（最省事，一行命令）

用仓库自带的安装脚本，别手工 `cp -r`：

```bash
bash tools/install_skills.sh --list                       # 先看 26 个技能与一句话说明
bash tools/install_skills.sh --target ~/.claude/skills    # 用户级：所有项目都能用
bash tools/install_skills.sh --target .claude/skills      # 项目级：只在这个项目生效
bash tools/install_skills.sh --target ~/.claude/skills --only owner-sell-home-advisor,broker-lease-sop
bash tools/install_skills.sh --target .claude/skills --link   # 符号链接：改仓库即生效（自己二次开发用）
```

安装脚本的三条纪律：

1. 只写 `--target` 指定的目录，不碰别处；`/` 和家目录本身会被拒绝
2. **目标里已有内容默认不覆盖**（防止冲掉你改过的版本），要覆盖加 `--force`；被跳过时退出码为 2
3. 每次写一份 `house-skills-kit.manifest.json`：版本 + 每个技能 `SKILL.md` 的 sha256 + 安装时间，升级时能一眼看出哪些技能变了

手工装也行（不推荐，容易漏文件）：`mkdir -p ~/.claude/skills && cp -R skills/* ~/.claude/skills/`。

之后在对话里直接说业务话（见第 3 节场景），Claude Code 会自己挑对应技能。

### 装法 B：Codex / 其他 agent 运行时（AGENTS.md 路由）

把仓库放进工作区，然后在 `AGENTS.md` 里加这段路由规则（可直接粘）：

```markdown
## 房产技能库路由

处理任何房产相关任务前，先读 `house-skills-kit/skills/<技能名>/SKILL.md`，按其中的「必问信息」先把缺的字段问齐，再按「输出格式」交付。

- 二手房：房源委托 → broker-listing-sop；客户配房/议价 → broker-client-deal-sop；成交后过户与交房 → resale-transaction-sop；交房当天的专业验收 → handover-inspection-advisor
- 一手案场：首次接待 → sales-reception-sop；判客分级 → sales-lead-grading；异议 → sales-objection-handling；谈价逼定 → sales-closing-sop；按揭 → sales-mortgage-sop；开盘执行 → sales-opening-sop
- 策划：蓄客排期 → presale-marketing-sop；竞品踩盘 → competitive-intel-sop；物料与示范区 → marketing-materials-sop；活动 → activity-organization-sop；价格优惠 → pricing-incentive-release-sop；开盘战役 → launch-integrated-campaign-sop；工程播报 → engineering-progress-broadcast-sop；老带新 → customer-advocacy-referral-sop
- 决策层：甲方经营/去化卡壳 → developer-sales-advisor；渠道与佣金政策 → channel-management-advisor
- 购房者：buyer-first-home-advisor
- 业主：要卖房 → owner-sell-home-advisor；要出租 → owner-rental-advisor
- 自媒体：property-media-creator
- 用之前先看该技能 README 的「什么时候不要用我」，场景不对就换技能，不要硬用
- 一切数字测算 → skills/calc-toolkit（禁止口算）
```

### 装法 C：普通对话里临时用（不装）

把**一个** `SKILL.md` 全文粘进对话，说"按这个技能的标准帮我处理下面这件事"。需要更细的方法时，再把对应 Part 粘进去。

---

## 2. 装完先验证（3 条命令，30 秒）

```bash
# ① 计算器能跑（月供）
python3 skills/calc-toolkit/mortgage.py --price 1000000 --downpay 30 --years 30
```

真实输出（节选，含参数来源与版本，说明数字可追溯）：

```
＝ 月供试算 ｜ 本金 700,000 元 ｜ 30年（360期） ｜ 全国默认档
【商贷 利率3.10%】
方案            月供        利息总额
等额本息        2,989 元    376,081 元
等额本金        首月 3,753   326,404 元
参数来源：commercial_rate = 来源[全国默认档] 版本[2026.08 通用档]
```

```bash
# ② 渠道跳点能算（全额跳档 vs 分段累进，差多少一目了然）
python3 skills/calc-toolkit/commission.py --scene channel --amount 30000000 --tiers '20000000:0.02;999999999:0.025'

# ③ 仓库自检（30 个技能 / 0 错误才算装对了）
python3 tools/validate_skills.py --quiet
```

---

## 3. 四个真实场景，看一遍就会用

### 场景一：二手经纪人接到一个"预算 150 万想看两房"的客户

1. 读 `skills/broker-client-deal-sop/SKILL.md` → 它的「必问信息」里有七问：预算/首付/贷款方式/区域/面积段/房龄/时间窗。
2. **先把没答的问齐**（这就是它跟"直接给房源列表"的区别）。
3. 交付：配房清单（三维打分排序）→ 带看方案（一场三套 + 二选一）→ 议价方案（三档让步 + 每档对价）。
4. 数字：月供、税费、佣金全部跑 `calc-toolkit`，把命令和输出一起给客户看。

### 场景二：策划要做本月竞品报告

1. 读 `skills/competitive-intel-sop/SKILL.md`。
2. 按「六模块采集清单」去踩盘（价值主张/展示面/销售力/价格/销控/服务），每条情报记采集日期。
3. 交付：踩盘记录 → 百分制打分表 → 周监控四指标（供应/成交/去化/价格，三源交叉）→ 月报（含三条我方应对建议）。

### 场景三：购房者自己判断"该不该买这一套"

1. 读 `skills/buyer-first-home-advisor/SKILL.md`。
2. 答完需求七问 → 出「预算三线」（舒适线/上限线/极限线，含月供）。
3. 交付：候选盘打分卡对比 → 看房检查清单 → **结论必须三选一：买 / 不买 / 再看**，附三条理由与下一步。

### 场景四：业主自己卖房或出租

1. 卖房读 `skills/owner-sell-home-advisor/SKILL.md`，出租读 `skills/owner-rental-advisor/SKILL.md`。
2. **先过「必问信息」**：卖房要问清"最晚什么时候必须拿到钱"、权属状态（抵押/共有/租约/户口/学位）、底线净得；出租要问清空置多久、能否配家具、是否配合备案。
3. 数字：
   - 卖房——`tax.py`（卖方税费）+ `commission.py --scene resale`（中介费，**费率用小数 0.01=1%**）+ `prepay.py`（解押）+ `deposit.py`（定金违约）→ 出「净得价」
   - 出租——`rent.py --net`（毛/净回报，**空置与税负用百分数 15=15%**）+ `holding.py`（空置一个月亏多少）+ `buy_vs_invest.py`（出租 vs 出售 vs 理财、打平涨幅）
4. 交付：卖房给「卖房决策一页纸」，出租给「出租决策一页纸」；两页纸都有模板，填不满说明还没到能挂牌/能带看的状态。

---

## 4. 使用纪律（这六条决定你能不能拿到能用的东西）

1. **先看边界再看内容**：每个技能的 `README.md` 都有「什么时候不要用我」一节——先确认这个场景该不该用它，再读 `SKILL.md`。用错技能比不用更糟，结论方向会反。
2. **先问后答**：`SKILL.md` 的「必问信息」不齐时，让 AI 追问，别让它猜。猜出来的方案在现场一定被打回。
3. **数字只走 calc-toolkit**：任何价格、税费、月供、佣金、得房率，一律跑脚本，不口算、不给"大概"。
4. **政策现查**：税费、限购、学区、公积金额度，按当地当期公告现查。技能里故意不写城市数字，写死的数字过期比没有更糟。
5. **对内/对外分版**：议价底牌、客户分级、渠道成本属于对内；给客户只出算价单、方案对比与检查清单。
6. **带数据时间戳交付**：每个数字后面写清"取数日期 + 来源"，价格类超过 30 天必须重取。

---

## 5. 常见坑

| 坑 | 后果 | 正确做法 |
|---|---|---|
| 把整个 playbook 一次塞进上下文 | 重点被稀释，答得又慢又泛 | 先 SKILL.md，再按 Part 取用 |
| 不问清就直接要方案 | 方案跟客户不匹配，返工 | 先过「必问信息」清单 |
| 让 AI"帮我估个价" | 编出来的数字会用在真实谈判里 | 跑 `calc-toolkit`，给命令与输出 |
| 技能叠加乱用（同时用 3 个决策层技能） | 结论互相打架 | 按角色选一条主线，其他只做引用 |
| 交付只有结论没有下一步 | 用户看完还是不知道做什么 | 每个交付必须带"下一步动作 + 时间" |

---

## 5.1 参数单位：最容易踩的一脚

同一个仓库里的计算器，参数单位并不统一（历史原因），混用会差 100 倍：

| 工具 | 参数 | 单位 | 正确写法 |
|---|---|---|---|
| `commission.py` | `--buyer-rate` `--seller-rate` | **小数** | `--seller-rate 0.01` = 1% |
| `commission.py` | `--bonus-rate` `--rebate` `--splits` | 小数 | `--rebate 0.3` = 返 30% |
| `efficiency.py` | `--use-coef` | **小数** | `--use-coef 0.88` = 88% |
| `rent.py` | `--vacancy` `--tax-rate` `--maint` `--target-yield` | **百分数** | `--vacancy 15` = 15% |
| `holding.py` | `--vacancy` | **月数** | `--vacancy 1` = 年空置 1 个月 |
| `holding.py` `tax.py` `prepay.py` `mortgage.py` `capacity.py` | `--rate` `--tax-rate` `--agent` | 百分数 | `--rate 3.1` = 3.1% |

写错时工具会拦你：`--use-coef 88` 会直接报错并提示改成 `0.88`；`commission.py --seller-rate 1` 会提示"被当作小数处理 → 100%，若本意是 1% 请写 0.01"。**看到这两种提示不要绕过，改参数重跑。**

---

## 6. 按角色速查

| 你是 | 起手技能 | 常用的下一步 |
|---|---|---|
| 一手案场顾问 | `sales-reception-sop` | `sales-lead-grading` → `sales-closing-sop` |
| 二手房经纪人（买卖） | `broker-listing-sop` / `broker-client-deal-sop` | `calc-toolkit`（佣金、税费） |
| 二手房经纪人（租赁） | `broker-lease-sop` | `calc-toolkit`（`commission.py --scene lease` 佣金分摊） |
| 二手房交易（过户/赎楼/网签/资金监管） | `resale-transaction-sop` | `calc-toolkit`（`tax.py` 买卖分列、`deposit.py` 定金罚则、`loanterm.py`、`status.py`） |
| 交房验收（新房或二手收房） | `handover-inspection-advisor` | `calc-toolkit`（`area_error.py` 面积补退、`efficiency.py` 得房率、`newhome.py` 交房费用） |
| 策划 | `presale-marketing-sop` | `competitive-intel-sop`、`marketing-materials-sop` |
| 营销负责人 | `developer-sales-advisor` | `channel-management-advisor`、`pricing-incentive-release-sop` |
| 购房者 | `buyer-first-home-advisor` | `calc-toolkit`（月供、全成本） |
| 自媒体运营 | `property-media-creator` | `calc-toolkit`、`competitive-intel-sop` |
| 业主（卖房） | `owner-sell-home-advisor` | `calc-toolkit`（卖方税费、中介费、解押、定金） |
| 业主（出租） | `owner-rental-advisor` | `calc-toolkit`（租回报、持有成本、租 vs 卖） |

全量清单与每个技能的一句话说明见仓库 `README.md`；技能编写与内容标准见 `docs/SKILL-AUTHORING-SPEC.md`。
