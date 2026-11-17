<!-- operations/source_directory.md —— 法规/准则原文查询源目录 -->

# 法规/准则原文查询源目录

> 硬触发：搜索决策流程命中、需 fetch 准则/法规原文时——先读本文件取对应入口再 fetch，不靠记忆拼 URL。
>
> 定位：古立特所有权威源入口总表（操作参考，非知识内容）。`references/knowledge/` 各 md 不单独保留 URL 目录，统一由此表管理。
>
> 加载：按需——`operations/routing_index.md`「L-1 前置闸」命中（“查最新/核实文号/税率优惠截止”）时读本表取具体入口；日常回答不读。
>
> 权威衔接：本文件落实 `SKILL.md` 的知识来源分层。现行法规、准则、税率、文号与效力状态以核实后的官方原文为最高权威；内置 knowledge 负责专业解释，不得覆盖更新后的官方事实。

---

## 源的两层分级（引用纪律）

| 层级 | 是什么 | 引用时怎么用 |
|---|---|---|
| **官方源** | 财政部/税务总局/中注协/证监会/交易所/国家法律法规数据库等一手发布 | 引用准则/法规/税率原文**必须落这里**，注明"根据 CAS 14 第十四条"式出处 |
| **非官方聚合源** | MaoDocs、中国会计视野法规库等第三方聚合站，内容**较准确、检索快** | 作快速定位与条文速查的入口；正式引用前回官方源核对，注明"经…核对" |

> 铁律衔接：准则/法规原文以官方源为准。聚合源查到的条文，正式交付引用前必须能在官方源对上，否则标"待官方核实"。

---

## 交叉验证方法（核实现行政策的标准动作）

> 用途：L-1 命中、或答案正确性依赖现行政策时执行。目标是确认「现在有效的是哪一版、数字/期限/文号是否准确、有没有被后续文件替代或延续」，而不是找到一条看似相关的旧规定就收工。

### 三步交叉验证

```
① 定位（聚合源，快）
   └─ 用「2.2 视野法规库」或「2.1 MaoDocs」按关键词/文号快速找到候选文件，
      拿到准确的文号、发文机关、发文日期。

② 核实（官方源，准）
   └─ 拿文号回对应官方源（税务走 1.2 税务总局法规库，会计走 1.1 财政部会计司，
      法律走 1.5 国家法律法规数据库）核对原文，确认：
      ├─ 文号、条文、数字、期限与聚合源一致；
      ├─ 效力状态 = 现行有效（不是已废止 / 已修改 / 被替代）；
      └─ 有无“自 X 年 X 月 X 日起执行”“有效期至”等时间限定。

③ 时点校验（防止“旧政策当现行”）
   └─ 按“今天”判断：
      ├─ 优惠类：确认当前是否仍在优惠期内、是否有延续公告（很多优惠靠后续公告逐年/逐期延期）；
      ├─ 比例/税率类：确认没有更新的公告调整了数字；
      └─ 只找到旧文时，主动检索“是否有更新/延续”，别停在第一条命中。
```

### 冲突消解规则（两处对不上时）

| 情形 | 处理 |
|---|---|
| 聚合源与官方源数字/文号不一致 | 以官方源为准，标注“经…核对” |
| 两份官方文件都像有效 | 后发文件、专门规定、更高层级优先；仍不清晰则并列列出各自文号与生效条件，提示用户以主管税务机关口径为准，不替用户拍板 |
| 只查到旧文、找不到现行版本 | 不假设旧文仍有效；标“待官方核实（截至查询日仅检索到 X 号文，未确认是否被替代/延续）” |
| 无法联网核实 | 给内置知识作参考，加时效标签“以最新官方为准”，并给出用户可自行核实的官方入口 |

### 交付时的核实标注（供 routing_flow 维度A「引用核实」落地）

- 已双源核实：`根据〔文号〕第 X 条（经〔官方源〕核对，现行有效，截至〔查询日〕）`
- 仅单源或存疑：`〔结论〕（待官方核实：仅〔来源〕检索到，未在官方源对上）`
- 涉及优惠期限：必须写清`执行期间 / 有效期至`，不得只给比例不给期限。

> 与铁律衔接：交叉验证不是每问必做，而是「答案会因政策变动而对错」时的强制动作；纯方法论、纯准则原理类问题不触发。

---

## 一、官方源（一手权威）

### 1.1 财政部会计司

> 适用：会计准则解释/实施问答/应用案例原文、政策动态、课题申报

| 子频道 | URL |
|--------|-----|
| 工作动态 | https://kjs.mof.gov.cn/gongzuodongtai/ |
| 工作通知 | https://kjs.mof.gov.cn/gongzuotongzhi/ |
| 政策发布 | https://kjs.mof.gov.cn/zhengcefabu/ |
| 政策解读 | https://kjs.mof.gov.cn/zhengcejiedu/ |
| 会计准则与动态 | https://kjs.mof.gov.cn/kjzydd/ |
| 国际动态 | https://kjs.mof.gov.cn/guojidongtai/ |
| 课题申报 | https://kjs.mof.gov.cn/zaixianfuwu/ketishenbao/ |

### 1.2 国家税务总局法规库

> 适用：税务公告、规章、规范性文件、税收协定；确认政策时效和最新税率
> 站点：https://fgk.chinatax.gov.cn

| 分类 | URL |
|------|-----|
| 法律（税收相关） | https://fgk.chinatax.gov.cn/zcfgk/c100010/listflfg_fg.html |
| 行政法规 | https://fgk.chinatax.gov.cn/zcfgk/c100009/listflfg_fg.html |
| 税务部门规章 | https://fgk.chinatax.gov.cn/zcfgk/c100011/list_guizhang.html |
| 税收规范性文件（公告） | https://fgk.chinatax.gov.cn/zcfgk/c100012/listflfg.html |
| 财政部 税务总局公告 | https://fgk.chinatax.gov.cn/zcfgk/c100013/listflfg.html |
| 工作通知 | https://fgk.chinatax.gov.cn/zcfgk/c102424/listflfg.html |
| 国务院文件 | https://fgk.chinatax.gov.cn/zcfgk/c102416/listflfg.html |
| 税收协定 | https://fgk.chinatax.gov.cn/zcfgk/c102440/listflfg.html |

### 1.3 中国注册会计师协会（中注协）

> 适用：执业准则、通知公告、年报审计快报、执业质量检查通告、事务所排名

| 频道 | URL |
|------|-----|
| 官网首页 | https://www.cicpa.org.cn |
| 专业标准 | https://www.cicpa.org.cn/ztzl1/Professional_standards/ |
| 通知公告 | https://www.cicpa.org.cn/xxfb/tzgg/ |
| 年报审计快报 | https://www.cicpa.org.cn/xxcx/annual_audit |
| 执业质量检查通告 | https://www.cicpa.org.cn/xxcx/kjsswszyzljc |
| 事务所综合评价排名 | https://www.cicpa.org.cn/ztzl1/swszhpm/ |
| 行业知识库（需CPA证登录） | https://cmis.cicpa.org.cn |

### 1.4 证券与金融监管机构

> 适用：上市公司公告、交易所规则、金融监管政策

| 机构 | URL | 用途 |
|------|-----|------|
| 中国证监会 | https://www.csrc.gov.cn | 监管规则、行政处罚、发审信息 |
| 上海证券交易所 | https://www.sse.com.cn | 上市规则、业务规则 |
| 深圳证券交易所 | https://www.szse.cn | 上市规则、业务规则 |
| 北京证券交易所 | https://www.bse.cn | 上市规则、业务规则 |
| 巨潮资讯网 | https://www.cninfo.com.cn | 上市公司公告/年报 |
| 中国人民银行 | https://www.pbc.gov.cn | 货币政策、利率、金融稳定 |
| 国家金融监督管理总局 | https://www.nfra.gov.cn | 银行业/保险业监管 |
| 国家外汇管理局 | https://www.safe.gov.cn | 外汇管理政策 |

### 1.5 经济法律与公共信息

| 资源 | URL | 用途 |
|------|-----|------|
| 国家法律法规数据库 | https://flk.npc.gov.cn | 法律/行政法规/地方性法规原文 |
| 国家市场监督管理总局 | https://www.samr.gov.cn | 公司法/反垄断/注册登记 |
| 国家企业信用信息公示系统 | https://www.gsxt.gov.cn | 工商信息查询 |
| 国务院国资委 | https://www.sasac.gov.cn | 国资监管/国企改革 |
| 中国裁判文书网 | https://wenshu.court.gov.cn | 司法判例/涉诉查询 |
| 国家审计署 | https://www.audit.gov.cn | 审计公告/预算执行审计 |
| 国家统计局 | https://www.stats.gov.cn | 宏观经济数据/行业统计 |

### 1.6 国务院与部委政策

| 资源 | URL | 用途 |
|------|-----|------|
| 国务院政策文件库 | https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?q=&t=zhengcelibrary&orpro= | 行政法规/国务院决定/部门规章/产业政策（鼓励/限制/淘汰）/行政审批改革 |
| 中国政府网 | https://www.gov.cn | 国常会决定、部委联合发文、政策解读总入口 |

### 1.7 国际税收

| 资源 | URL |
|------|------|
| OECD BEPS 规则及行政指引 | https://www.oecd.org/tax/beps/ |

---

## 二、非官方聚合源（准确、检索快，作速查入口）

> 说明：以下站点内容较准确、结构化好、检索方便，适合准则/法规原文速查与知识库未覆盖的细节。**正式引用前回官方源核对。**

### 2.1 MaoDocs 板块入口表

> 站点：https://docs.maoyanqing.com/ ｜ 访问方式：rendered 模式 fetch 对应页面
> 用途：准则原文、应用指南、解释、案例、实施问答的结构化速查

| 古立特知识文件 | MaoDocs 板块 | 入口 URL |
|---|---|---|
| `references/knowledge/accounting/accounting_core.md` / `references/knowledge/accounting/accounting_advanced.md` | 会计 → 企业会计准则 | https://docs.maoyanqing.com/accounting/ent/cas/ |
| `references/knowledge/accounting/accounting_core.md` / `references/knowledge/accounting/accounting_advanced.md` | 会计 → 准则应用指南 | https://docs.maoyanqing.com/accounting/ent/casg/ |
| `references/knowledge/accounting/accounting_core.md` / `references/knowledge/accounting/accounting_advanced.md` | 会计 → 准则解释 | https://docs.maoyanqing.com/accounting/ent/casi/ |
| `references/knowledge/accounting/cas_application_cases.md` | 会计 → 应用案例 | https://docs.maoyanqing.com/accounting/ent/casc/ |
| `references/knowledge/accounting/cas_practical_judgments.md` | 会计 → 实施问答 | https://docs.maoyanqing.com/accounting/ent/casq/ |
| `references/knowledge/specialized/government_npo_accounting.md` | 会计 → 政府会计准则制度 | https://docs.maoyanqing.com/accounting/gov/ |
| `references/knowledge/specialized/government_npo_accounting.md` | 会计 → 非营利组织会计制度 | https://docs.maoyanqing.com/accounting/npo/ |
| `references/knowledge/audit/audit.md` | 审计 → 执业准则 | https://docs.maoyanqing.com/auditing/csa/ |
| `references/knowledge/audit/audit_procedures.md` | 审计 → 应用指南 | https://docs.maoyanqing.com/auditing/csag/ |
| `references/knowledge/audit/audit.md` | 审计 → 问题解答 | https://docs.maoyanqing.com/auditing/csaq/ |
| `references/knowledge/audit/audit.md` | 审计 → 职业道德守则 | https://docs.maoyanqing.com/auditing/csce/ |
| `references/knowledge/analysis/statement.md` | 证券 → 会计监管风险提示 | https://docs.maoyanqing.com/securities/rwas/ |
| `references/knowledge/analysis/statement.md` | 证券 → 监管报告 | https://docs.maoyanqing.com/securities/asr/ |
| `references/knowledge/investment/investment.md` | 证券 → 信息披露要求 | https://docs.maoyanqing.com/securities/idcosp/ |
| `references/knowledge/investment/investment.md` | 证券 → 交易所规则 | https://docs.maoyanqing.com/securities/rules/ |
| `references/knowledge/investment/investment.md` | 证券 → 监管规则适用指引 | https://docs.maoyanqing.com/securities/garr/ |
| `references/knowledge/compliance/economic_law.md` | 证券 → 证券法 | https://docs.maoyanqing.com/securities/sl/00.html |
| `references/knowledge/compliance/economic_law.md` | 证券 → 上市公司监管指引 | https://docs.maoyanqing.com/securities/rlc/ |
| `references/knowledge/audit/internal_control.md` | 内控 → 企业内部控制规范 | https://docs.maoyanqing.com/control/ent/ |
| `references/knowledge/audit/internal_control.md` | 内控 → 行政事业单位内控 | https://docs.maoyanqing.com/control/api/ |
| `references/knowledge/investment/forensic_accounting.md` | 评估 → 资产评估准则 | https://docs.maoyanqing.com/appraisal/aas/ |
| `references/knowledge/investment/forensic_accounting.md` | 评估 → 评估专家指引 | https://docs.maoyanqing.com/appraisal/aaeg/ |
| `references/knowledge/investment/forensic_accounting.md` | 评估 → 资产评估法原文 | https://docs.maoyanqing.com/appraisal/aal/ |

### 2.2 中国会计视野法规库

> 站点：https://law.esnai.cn ｜ 15.7 万条法规，每日更新
> 用途：查具体法规文号、确认法规是否失效、查地方性政策；覆盖税费/会计/财务/审计/评估/金融证券/国资管理等全领域

---

## 三、交易所与跨境电商专项

### 3.1 交易所法律规则（官方）

| 资源 | URL |
|---|---|
| 深交所法律规则 | https://www.szse.cn/lawrules/ |
| 上交所法律法规 | https://www.sse.com.cn/lawandrules/sselawsrules2025/overview/ |
| 北交所法规规则 | https://www.bse.cn/business/overview.html |

### 3.2 跨境电商政策（`references/knowledge/analysis/financial_bp.md`）

| 资源 | URL | 性质 |
|---|---|---|
| 欧盟理事会 | https://www.consilium.europa.eu/ | 官方（关税改革/小包裹新规） |
| 欧盟委员会税务与海关同盟 | https://taxation-customs.ec.europa.eu/ | 官方（IOSS/进口增值税） |
| 中国自由贸易区服务网 | https://fta.mofcom.gov.cn/ | 官方（RCEP税率/原产地规则） |
| 亚马逊全球开店 | https://gs.amazon.cn/ | 平台官方（费用调整/公告） |
| 雨果网 | https://www.cifnews.com/ | 行业媒体（动态/政策解读） |
| 亿邦动力 | https://www.ebrun.com/ | 行业媒体（行业报告/benchmark） |

---

## 使用规则

1. **知识库能答的不联网**：只有 `references/knowledge/` 查不到或需核实时效时才 fetch。
2. **引用纪律**：准则/法规/税率原文引用**必落官方源**；聚合源（MaoDocs/视野）作速查入口，正式引用前回官方源核对。
3. **注明出处**：引用原文注明来源与具体条文（如"根据 CAS 14 第十四条"）。
4. **按需取用**：不一次性大量抓取，只取与当前问题直接相关的页面；MaoDocs 用 rendered 模式。
5. **税务优先走官方**：查公告/规章/协定走「1.2 国家税务总局法规库」。
6. **文号/失效/地方性政策**：先用「2.2 视野法规库」快速定位，再回官方源确认。
7. **URL 失效处理**：fetch 返回 404 时，告知用户"该链接可能已变更，建议手动搜索关键词"。
