# 马德里技能：脚本设计与维护说明

> **用途**：承接 SKILL.md 原 §4.12「配套文件与关键设计要点」。
> **权威范围**：本文件说明脚本的**设计口径与维护规程**；脚本本身（`scripts/*.py`）是计算逻辑的代码权威源，两者冲突时以脚本与官方文件为准。
> **单一维护**：改动规费数值须同步 `references/madrid-fees.md` 与 `scripts/madrid_fee_data.json`，并运行 `py scripts/selftest.py` 通过全部用例后再提交。

配套文件与关键设计要点：

· `scripts/madrid_fee_data.json`：费用数据的**机器可读镜像**（WIPO 官费 + 76 个缔约方单独规费，含计费模式与宽限期费率）；人类可读版为 @references/madrid-fees.md。两者改动须同步，由 `selftest.py` 的「数据一致性」用例逐国比对把关。
· `scripts/madrid_response_times.json`：**答复临时驳回期限**的数据源（WIPO Rule 17(7) 表全 38 成员，含依职权/异议两档、6 种起算基准原文、条件期限脚注）；人类可读版为 @references/madrid-declarations.md §4e-i/§4e-ii，二者一致性由 `selftest.py` 的「答复期限数据与声明文档一致」用例把关（逐成员比对名称与基准词汇）。
· `scripts/madrid_dateutil.py`：共享日期工具（自然月推进、月末与闰年 2/29 兜底、`--today` 复现），被期限与续展脚本复用，不再各自复制实现。
· 规费计算器完全按官方费用表口径实现：附加费在「指定缔约方全部为单独规费国」时不收、后期指定不收附加费、**宽限期附加费按基本费 50%**（653 × 50% = 326.5 → 进位 327，实际应付以官方账单为准）、未列名缔约方按补充费 100 CHF 并标注。
· 驳回期计算**不自作主张**：默认 12 个月并要求核验声明，18 个月须显式 `--declared-18`；`--country protocol` 仅作兼容且会在输出中提醒旧口径已废；12 个月基础上主张异议延长会被直接拦截（第 5 条(2)(c) 以 18 个月声明为前提）。
· 三个脚本均默认 UTF-8 输出（自动重配置 stdout，避免 Windows 管道下 cp936 报错），并支持 `--today`（复现）与 `--ascii`（终端兼容）。脚本输出为估算与提示，最终以官方通知为准。
· **实时核算脚本 `madrid_feecalc_live.py` 是单独规费争议的裁决工具**：官方 Fee Calculator 为 JSF 应用，无法用 HTTP 抓取（缔约方清单与结果均由 JS 触发渲染），须以真实浏览器驱动。脚本依赖 `playwright` + chromium（`pip install playwright` 后执行 `playwright install chromium`；亦会自动在 `%LOCALAPPDATA%\ms-playwright` 下查找已安装的 chrome.exe）。**每次勾选缔约方都会 AJAX 重绘页面，单次点击可能被吞**——脚本内置「勾选 → 回读已勾集合 → 未生效者补勾」最多 4 轮的重试，实务中若 `--countries` 数量多、出现漏勾，以脚本末尾「已勾选 N / M」为准，未达 M 时结果不可用（退出码 2）。
· **两条规费计算路径的分工（不得互相替代）**：`madrid_fee.py` 为**离线快照**计算（无网络/无浏览器即可用，内置 76 个缔约方单独规费 + 已公告的生效日调整，并按 `--date` 生效、按 `--date` 提示跨生效日与未实测组件）；`madrid_feecalc_live.py` 为**官方实测**（浏览器驱动 WIPO Fee Calculator，是金额争议的裁决依据）。**跨费率生效日报价、或离线快照晚于 90 天未更新时，一律以 live 脚本实测为准**；离线脚本的价值在于覆盖 live 脚本不可用的环境与批量预算初算。
· **条约全文可一键重抓**：官方文本更新后，用 `scripts/wipo_lex_fetch.py` 重跑即可（建议先在 `--inspect` 模式下核对首尾与条号计数，再落地）。抓取要点：WIPO Lex 文本页把整份文档内嵌在 `id="printID"` 容器里（**同一页可能含官方脚注所引的他条约原文，属正常内容**）；抓完后务必核对末条（协定第十八条 / 议定书第十六条 / 细则第41条 / 行政规程第19条）以排除截断。
· 脚本运行会在 `scripts/` 下生成 `__pycache__`；为保持「仅 2 级目录」的结构要求，建议以 `py -B selftest.py` 运行（不写字节码），或运行后删除该目录。
· WIPO 官方在线计算器：https://madrid.wipo.int/feecalcapp/

---

## 六、WIPO Fee Calculator 操作步骤（原 §4.8）

WIPO Fee Calculator 使用方法：

```
Step 1: 选择交易类型（New application / Subsequent designation / 等）
           │
           ▼
Step 2: 选择指定缔约方（可多选）
           │
           ▼
Step 3: 输入商品/服务类别数
           │
           ▼
   🔴 CHECKPOINT：检查是否包括集体商标/证明商标（部分缔约方费率不同）
           │
           ▼
Step 4: 系统自动计算各项规费并汇总
           │
           ▼
   🔴 CHECKPOINT：将计算结果与费用表交叉核对，确认无误
```

