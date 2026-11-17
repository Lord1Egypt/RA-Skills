# 欧洲市场覆盖 / European coverage: market shortlist and open-data reality check

## 中文摘要（下方为英文详版）

本文不是事实来源，只是一张「哪些源值得去核实」的地图——`templates/official-sources.eu.yml` 里每条都带
`verify_before_use: true`。

- **选国标准**：不是"热门"，而是**这套房的成交价能不能被任何人逐套复核**。
- **交易级成交价可得性**：英国（Land Registry PPD）、爱尔兰（PSRA PPR）、法国（DVF）✅；荷兰、德国、西班牙 ❌
  → 这三个市场 provenance 从 `suspect` 起步，必须告知用户"挂牌-成交对照无法用成交数据完成"。
- **英国要分清法域**：苏格兰 LBTT、威尔士 LTT 与英格兰 SDLT 是三套税制，`market.country` 必须写清。
- **欧洲挂牌平台未注册为 scraper 模块**：Rightmove/Zoopla、Idealista/Fotocasa、Funda、ImmoScout24、SeLoger、
  Daft.ie 只能走 generic 兜底，不写未经验证的选择器。
- **冷静期/定金差异会改变谈判建议**：法国 compromis 后 10 天可无责退出、荷兰买家 3 天、西班牙 Arras 已带罚则、
  英格兰要 exchange 才绑定。
- **新增一个市场** = 在 `templates/official-sources.<code>.yml` 与 `templates/policy-notes.<code>.yml` 各补一块；
  系统层无需改代码，`node scripts/doctor.mjs` 会自动把它计入「市场覆盖」。
- **画像适配**：`config/profile.yml` 的 `market:` 段决定币种、金额口径（万元 vs 本币整额）与面积单位（㎡ vs sq ft），
  采集流程见 `modes/intake.md` 的 Step 0.5。

---

Nothing here is a fact source by itself — it is a **map of which sources are worth verifying**. Every entry in
`templates/official-sources.eu.yml` carries `verify_before_use: true`; what follows explains why the shortlist looks
the way it does, and where house-ops has to weaken its usual claims.

## Why these six markets

The deciding criterion was not popularity but **whether a deal price can be checked at the unit level by anyone**:

| Market | Transaction-level sold prices | Asset Registry/Cadastre | Typical UK-style pitfall already documented |
|---|---|---|---|
| 🇬🇧 UK (England & Wales) | ✅ HM Land Registry Price Paid Data, free, since 1995 | ✅ INSPIRE polygons, EPC register | Leasehold ground rent, service charges, cladding remediation |
| 🇮🇪 Ireland | ✅ PSRA Property Price Register, since 2010, weekly | ⚠️ fewer layers | mica/pyrite defects in some counties, vague addresses in the register |
| 🇫🇷 France | ✅ DVF (all notarised sales since 2014), Open Licence | ✅ Cadastre Etalab, Géorisques | DMTO surcharge, DPE rental bans, copropriété charges |
| 🇳🇱 Netherlands | ❌ no public sold-price register | ✅ Kadaster BAG/BRK, CBS (WOZ) | erfpacht ground lease, VvE reserves, soft-soil foundations |
| 🇩🇪 Germany | ❌ no nationwide open register | ⚠️ per-state BORIS land values only | GrESt spread 3.5–6.5% by state, cash-only closing costs |
| 🇪🇸 Spain | ❌ no public sold-price register | ✅ Catastro (incl. Valor de Referencia) | Valor de Referencia tax base, unregistered extensions, Arras penalty deposits |

Tier-2 candidates deliberately not registered yet: **Nordics** (Denmark Datafordeler/BBR, Sweden Lantmäteriet,
Norway matrikkelen — all have good registries but no immediately usable per-deal price export), plus **Portugal** and
**Italy** (OMI zonal quotes exist in Italy, IMT/IMI in Portugal, but each needs its own sourcing pass before we put
anything in a registry file that AI will quote).

## What changes for the pipeline

1. **The `成交数据` tier is not universally available.** In DE/NL/ES the best achievable tier is usually
   `公开统计` (aggregate) or `开放登记` (cadastre). Following ADR-0002, that means those markets start at
   `suspect` and must inform the user that the listing-vs-transaction check **cannot** be completed with deal data.
2. **European listing portals are not registered as scraper modules.** Rightmove/Zoopla, Idealista/Fotocasa, Funda,
   ImmoScout24, SeLoger, Daft.ie are currently only reachable through the generic fallback checklist — we refuse to
   hand-write field selectors we have not verified. Adding one follows `scrapers/ADDING_A_PLATFORM.md`.
3. **Recurring costs beat purchase taxes for decision quality.** Service charges and ground rent (UK), erfpacht and
   VvE reserves (NL), copropriété arrears and DPE-driven refurbishment (FR), IBI plus comunidad (ES) are invisible
   in photos and dominate long-run cost.
4. **"Restrictions" are mostly not purchase bans.** EU markets have no purchase-qualification system like mainland
   China; the real gates are KYC/source-of-funds, lending caps, and — for a few countries not yet covered (Denmark,
   Austria, Switzerland) — permit requirements on foreign buyers.
5. **Cooling-off periods differ sharply and change negotiation tactics:** France gives 10 days after compromis,
   the Netherlands gives buyers 3 days, whereas Spain's Arras contract already carries penalties and England only
   binds at exchange. A "we can always walk away" assumption that is true in one market is expensive in another.

## Known conflicts, deliberately left visible

We found public sources that disagree. Both variants stay in `templates/policy-notes.eu.yml` marked
`conflict: true` so any report must surface the disagreement instead of picking a number:

- **Netherlands:** non-owner-occupied residential transfer tax after 2026-01-01 (10.4% vs 8%), and the 2026
  eigenwoningforfait thresholds.
- **Germany:** Bremen's Grunderwerbsteuer rate (5.5% per the 2025-07-01 increase vs still-listed 5.0% calculators).

Resolving them needs a primary-source check (Belastingdienst / Bremen Finanzamt) — exactly the kind of thing
house-ops insists a human verify rather than an AI average out.

## How to call it

```bash
node scripts/scan.mjs official --market eu      # all 17 European registry entries
node scripts/scan.mjs official 伦敦             # keyword across city / name / notes
node scripts/scan.mjs official dvf             # e.g. jump straight to the French registry entry
node scripts/scan.mjs official --market de      # one country only
node scripts/doctor.mjs                         # market coverage + is profile.yml market.code registered?
```

The market dimension also lives in the buyer profile: `config/profile.yml` carries a `market:` block (code, currency,
price scale, area unit, buyer class, tenure preference, minimum lease years) that `modes/intake.md` collects in
Step 0.5 and every report's units follow.

Adding a market = adding one entry block to `templates/official-sources.eu.yml` plus one block to
`templates/policy-notes.eu.yml`. Both files are validated alongside the Chinese ones by the repo self-check.
