# 亚太市场覆盖 / APAC coverage: Hong Kong (China), Singapore, Japan

## 中文摘要（下方为英文详版）

本文同样只是「哪些源值得核实」的地图——`templates/official-sources.apac.yml` 里每条都带 `verify_before_use: true`。

- **三个市场的成交价可得性完全不同**，这决定 Price 维度能做到哪一层：
  - **中国香港 ✅** 土地注册处 IRIS 的土地登记册记载成交代价，是唯一能核实单套成交价的官方口径（按次收费，不是开放数据）。
  - **新加坡 ⚠️ 一半** 组屋转售是真正的交易级开放数据（1990 起，data.gov.sg）；私宅只有 URA 的 caveat，
    而 caveat 属自愿登记、覆盖率约 80–90%、异常值被剔除、2015-05-25 起「新售」不是 caveat 而是发展商每周申报的 OTP。
  - **日本 ❌** 没有单套级成交价，只有 MLIT 的成約価格情報（REINS 加工）与取引価格情報（当事人问卷），
    都到同区同类型的区间为止，**不得伪造单套成交价**。
- **退出机制差别最大**：中国香港签临时买卖合约即绑定、新加坡 OTP 定金即具约束力，两地均无冷静期；
  日本没有法定冷静期，但有「手付解除」与「融资特约」两个**必须写进契约**的退出阀门。
- **外国人门槛形态不同**：日本基本无取得限制但有申报义务（非居住者 20 天内向日本银行报告、
  登记时申报国籍、重要土地等調査法的事前届出）；新加坡是**税务型**门槛（ABSD 60% 且须现金）；
  中国香港自 2024-02-28 撤辣后已无限购型印花税，剩下按揭与资金来源审查。
- **已记录的口径冲突**（标 `conflict: true`，不取平均）：新加坡 SSD 的 4 年制（2025-07-04 起）vs 3 年制、
  组屋贷款成数 75% vs 80%、物業税自住 0–32% vs 旧表 0–16%；中国香港按揭保险的分档；日本登録免許税的床面积门槛。
- **亚太挂牌平台同样未注册为 scraper 模块**（中原/美联、PropertyGuru/99.co、SUUMO/LIFULL HOME'S 等），
  只能走 generic 兜底。
- **新增市场** = 在 `templates/` 下补成对的两个文件；`scripts/` 里没有硬编码的市场清单。

---

## Why these three, and what each can actually prove

| Market | Transaction-level sold price | What the registry can reach | The pitfall that decides most deals |
|---|---|---|---|
| 🇨🇳🇭🇰 Hong Kong (China) | ✅ Land Registry IRIS records the consideration | 成交数据 (per unit, paid per search) | 实用面积 vs 建筑面积、僭建与维修令、大厦大维修分摊、土地契约年期（多至 2047） |
| 🇸🇬 Singapore | ⚠️ HDB resale yes; private only via URA caveats | 成交数据 for HDB, partial for private | ABSD 60% payable in cash, lease decay (99-year), MOP and quota rules, caveat coverage |
| 🇯🇵 Japan | ❌ nothing at unit level | 公开统计 / 开放登记 only | 再建筑不可 (road frontage), 旧耐震, 修繕積立金 shortfalls, hazard zones |

### Hong Kong (China)

- AVD Scale 2 has been the only residential stamp duty since **2024-02-28**, when SSD, BSD and NRSD were all cut to
  0%. Rates were re-cut again **from 2026-02-26** (flat HK$100 up to HK$4m, top marginal 6.5% above ~HK$109.6m).
  Residential rates no longer differ between first-time and repeat buyers.
- Financing: LTV 70% for owner-occupied up to HK$30m, 60% above, 50% for non-owner-occupied; DSR unified at 50%
  since 2024-10-16; the stress test has been suspended since 2024-02-28. **Banks lend on the lower of valuation and
  price**, so a low valuation eats the down payment before the deal is even signed.
- Recurring: rates at 5% of rateable value, government rent at 3%, management fee plus whatever the incorporated
  owners resolve for major works.

### Singapore

- BSD (1–6%) + ABSD (SC 0/20/30, PR 5/30/35, foreigner 60%, entity 65%; US/EFTA nationals get citizen treatment),
  plus SSD on exit. ABSD cannot be paid with CPF — it is cash, within 14 days.
- Foreigners can buy condos (and post-MOP ECs), cannot buy HDB flats, and need SLA approval for landed property.
- Property tax is on **Annual Value**, not price: owner-occupied 0–32%, non-owner-occupied 12–36%, non-residential
  flat 10%.
- The free URA transaction search is genuinely useful and genuinely incomplete; treat it as "most of the market",
  never as "the market".

### Japan

- Acquisition tax 4% standard, 3% for residential under the special measure; registration and licence tax has
  reduced rates; stamp duty uses reduced bands; consumption tax applies to buildings only when the seller is a
  taxable business, which is why two second-hand listings at the same price can differ by millions of yen.
- No restriction on foreign ownership as of 2026-09, but: 20-day BOJ report for non-residents (from 2026-04-01),
  nationality at registration (from FY2026), and prior notification inside Special Monitoring Zones for land or
  buildings of 200㎡ or more. Buying from a non-resident seller obliges the buyer to withhold 10.21%.
- Cheap Japanese property is cheap for a reason: non-rebuildable plots, pre-1981 seismic standards, boundary
  problems, or a hazard zone. Finding the reason before committing is the whole job.

## Known conflicts, deliberately left visible

Both variants stay in `templates/policy-notes.apac.yml` under `conflict: true`:

- **Singapore:** SSD holding period (4 years at 16/12/8/4% for purchases on or after 2025-07-04 vs the older
  3-year 12/8/4% schedule); HDB loan LTV (75% since 2024-08-20 vs the still-circulating 80%); property tax bands
  (0–32% owner-occupied vs the pre-increase 0–16% tables still online).
- **Hong Kong:** the mortgage insurance tiers by property value.
- **Japan:** the floor-area threshold for the reduced registration tax (50㎡ vs the 2026 reform's 40㎡).

## How to call it

```bash
node scripts/scan.mjs official --market apac   # all 18 entries
node scripts/scan.mjs official --market jp     # one market
node scripts/scan.mjs official 路線価          # keyword across name / city / notes
node scripts/doctor.mjs                        # market coverage + is profile.yml market.code registered?
```

Adding a market means adding one block to `templates/official-sources.<family>.yml` and one to
`templates/policy-notes.<family>.yml`; `scan.mjs` and `doctor.mjs` discover both by filename.
