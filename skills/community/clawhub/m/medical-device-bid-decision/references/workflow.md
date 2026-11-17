<!-- request-identity:start -->
**请求身份**：使用已配置的 API Key，并保留本包的 X-Client，携带下列完整身份头；不得沿用其它包的版本或来源。
```text
X-Client: bid-decision/1.0.5
X-Skill-Package: medical-device-bid-decision/1.0.9
X-Skill-Source: clawhub/zhiliaobiaoxun
```
<!-- request-identity:end -->

# 投标决策分析 · 五步工作流执行手册

> 所有请求带 Header：`X-API-Key` + `X-Client: bid-decision/1.0.5`。
> 工具参数速查见 `api-quick.md`。每步都有「降级策略」——数据缺失时照做，不要中断也不要编造。

## 模式选择

- **完整模式**（默认，12-25 次调用）：五步全做。
- **精简模式**（5-8 次调用）：用户要求快速判断时，只做 ①②③，且 ③ 只分析 Top3 竞争者、跳过逐家深挖。

---

## ① 解析标的（1-3 次调用）

**目标**：项目画像——采购方、预算、标的物、资质门槛、时间线。

1. 用户给了知了标讯链接或 bid_id → `get_bid_detail`（拿 `fulltext` 原文）
2. 用户只给了项目标题 → `search_bids`（keywords=[标题关键词], match_modes=["title"]）定位后再 `get_bid_detail`
3. 用户给了本地招标文件 → 直接读文件解析，再用 `search_bids` 交叉核实该项目是否已发布公告

从原文提取：采购方名称、预算金额、标的物清单（品牌/型号/数量）、资质要求、投标截止时间、评分办法（价格分占比）。

**降级**：站内查不到该项目 → 基于用户提供的信息继续，报告中标注「项目信息来自用户提供，未经站内核实」。

## ② 采购方画像（3-6 次调用）

**目标**：这个采购方好不好打——采购规律、预算水平、有没有明显的偏好供应商。

1. `get_company_profile`（company=采购方）→ 基础画像 + 历史招标次数
2. `query_bids_advanced`（keywords=[采购方全称], match_modes=["caller"], bid_process=[7,8], 近 3 年）→ 历史中标结果：谁在给它供货、金额分布
3. `get_company_partners`（company=采购方, partner_type="供应商"）→ Top 供应商及合作次数/金额

**关键判断**（写进报告）：
- **在位者信号**：某供应商合作次数 ≥3 或近 2 年金额占比 >40% → 明确提示「存在强在位供应商，若本项目为续期类，胜率显著受压」
- **在位者承接能力**：现有 Top 供应商的业务领域（products 字段）与本标的物是否匹配——都不匹配 → 说明这是采购方的新品类需求，竞争相对开放，外部投标者机会上升
- **采购规律**：同类标的物的历史采购频率、单次预算区间 → 判断本项目预算是否异常（预算明显偏离历史区间属于限制性信号之一）

**降级**：采购方在站内无历史记录（新单位/名称变体）→ 先 `search_company` 找全名称变体重试一次；仍无 → 报告标注「采购方历史数据缺失，在位者分析不可用」，置信度降级。

## ③ 竞争预测（4-8 次调用）

**目标**：谁会来投、各家几斤几两。

1. `find_potential_bidders`（bid_id 或 project_title）→ 潜在投标者列表（含与该采购方合作史、区域中标数、匹配产品）
2. 对 Top3-5 家，逐家快查：
   - `search_bids`（keywords=[公司名], match_modes=["winner"], bid_process=[7,8], keywords 加标的物过滤）→ 同类项目中标实力
   - 与采购方的直接合作史（`query_bids_advanced`：caller=采购方 AND winner=该公司）

**关键判断**：
- 每家给出「威胁等级」（高/中/低）+ 依据：与采购方合作次数、同类项目中标量、区域优势
- 若某家同时是②中的强在位者 → 单独标注为「最大威胁」

**降级**：`find_potential_bidders` 无结果（冷门品类）→ 改用 `get_top_suppliers`（keywords=标的物, provinces=[项目省份]）取区域 Top 中标商作为竞争者代理，报告标注推断方式。

## ④ 价格基准（2-5 次调用）

**目标**：报价带——报多少有竞争力、低于多少可能亏。

1. 标的物有明确品牌/型号 → `get_price_trends`（brand+model+product, exclude_keywords=["维保","耗材"]）→ 历史成交单价 min/avg/median
2. 服务类/无明确型号 → `aggregate_bids_advanced`（filters: keywords=标的物+同类范围, bid_type=2, 近 2 年; group_by=["quarter"]）→ 同类项目金额分布与趋势
3. 参考②中该采购方同类项目的历史成交价（最直接的锚点）

**输出**：建议报价带 = [有竞争力下限, 稳妥上限]，注明依据（历史中标价分位数、预算折扣率惯例）。价格分占比高的项目提示低价策略空间。

**降级**：无同型号价格记录 → 用同品类均价 + 明确标注「价格参考基于品类均值而非同型号，误差较大」。

## ⑤ 自家适配（可选，2-4 次调用）

**仅当用户提供了自家公司名时执行。**

1. `search_bids`（keywords=[自家公司], match_modes=["winner","tender"], 标的物过滤）→ 自家同类项目业绩（投标资质佐证）
2. `query_bids_advanced`（caller=采购方 AND winner_tender=自家）→ 与该采购方有无合作史
3. `find_competitors`（company=自家）→ 交叉核对③中的竞争者是否为惯常对手（知己知彼数据）

**输出**：胜率要素清单——业绩匹配度、客户关系、对③中各威胁的相对优劣。

---

## 汇总与结论

按 `report-template.md` 输出。结论三档：

- **建议投**：无强在位者 + 自家（或典型投标者）业绩匹配 + 报价有空间
- **谨慎参与**：存在在位者但非垄断 / 数据缺口影响判断 → 列出「参与前提条件」
- **不建议**：强在位者垄断（近 3 次同类全是同一家）/ 预算明显异常 / 资质硬门槛不满足

每个结论必须给出 2-4 条数据支撑。存在数据缺口时在结论旁标注置信度（高/中/低）。

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: medical-device-bid-decision/1.0.9
X-Skill-Source: clawhub/zhiliaobiaoxun
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
