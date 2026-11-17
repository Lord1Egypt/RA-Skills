# Industry-Specific Patent & Trade Secret Guide

Different industries have fundamentally different patent/trade-secret dynamics. This guide provides vertical-specific signals, verification strategies, and common pitfalls.

---

## 1. Semiconductor

### Patent vs. Trade Secret Dynamics
- **Manufacturing processes** (lithography, etching, deposition, packaging): Overwhelmingly trade secrets. TSMC, Samsung, Intel do NOT patent their process recipes. The 6-indicator trade secret assessment will almost always score 4+.
- **Chip architectures / designs** (ISA, microarchitecture, interconnects): Strong patent coverage. ARM, x86, RISC-V are heavily patented.
- **EDA tools / design methodologies**: Mixed. Some patented, some trade-secret algorithms.

### Key Signals
- A foundry's process node advancement without corresponding patents → trade secret, not gap
- Fabless companies (e.g., MediaTek, UNISOC) lacking process patents → expected, they don't manufacture
- Equipment makers (e.g., ASML, AMAT, LAM) → strong patent portfolios, less trade secret reliance

### Verification Strategy
- **Teardown > everything else**: Chip teardowns (TechInsights, ICWorks) are the gold standard
- **Patent gap in chip design**: meaningful signal for IP licensing (e.g., ARM architecture license)
- **Patent gap in manufacturing**: almost always trade secret, do not infer supplier dependency
- **Financial cross-validation**: check foundry customer concentration in annual reports

### Common A-Share Examples
- SMIC (中芯国际): Process patents are sparse vs. TSMC; this reflects technology gap + trade secret strategy, not external sourcing
- Hygon (海光信息): x86 license from AMD → genuine IP dependency
- Cambricon (寒武纪): AI chip architecture patents → strong internal IP

---

## 2. Pharmaceuticals

### Patent vs. Trade Secret Dynamics
- **Compound patents** (small molecule structures): Heavily patented. The molecule IS the product.
- **Manufacturing processes** (synthesis routes, purification, formulation): Often trade secrets. Same drug, different manufacturers may use different routes.
- **Clinical trial data**: Regulatory exclusivity + trade secrets, not patents.
- **Biologics / Biosimilars**: Complex mix. Cell line development and culture conditions are trade secrets.

### Key Signals
- Drug A has expired compound patent but no generic versions → manufacturing process is the barrier (trade secret or new process patent)
- Biologic has zero process patents → expected, cell culture conditions are trade secrets
- ANDA (generic drug application) filings → reveals which companies are trying to enter

### Verification Strategy
- **Patent expiry + generic entry timing**: The most reliable signal
- **DMF (Drug Master File) filings**: Companies filing DMFs for an API are the actual suppliers
- **CDE (药审中心) registration data**: China-specific regulatory filings
- **Procurement/tender data**: Hospital procurement records, centralized drug procurement (集采)

### Common A-Share Examples
- Hengrui (恒瑞医药): Strong compound + formulation patents → internal R&D driven
- WuXi AppTec (药明康德): CDMO, process patents + trade secrets → client dependency analysis
- Generic manufacturers (Huahai 华海, Hisun 海正): Watch ANDA filing pipeline for target identification

---

## 3. New Energy / Battery

### Patent vs. Trade Secret Dynamics
- **Battery chemistry** (cathode materials, electrolyte formulations): Strong patent coverage. CATL, LG Energy, Panasonic all file aggressively.
- **Manufacturing process** (coating, stacking, formation): Mixed. Some patented equipment designs, some process know-how.
- **BMS (Battery Management System)**: Software-heavy, patent + trade secret mix.
- **Recycling processes**: Emerging patent landscape, rapidly evolving.

### Key Signals
- Battery maker without cathode material patents → likely sourcing from material suppliers
- EV maker without battery patents → definitely sourcing from battery makers (BYD is the exception — vertically integrated)
- Separator / electrolyte additive patents → strong signal of capability depth

### Verification Strategy
- **Supply agreement announcements**: Battery supply contracts are often publicly announced (e.g., CATL → Tesla/NIO/XPeng)
- **Product certification**: EV models must list battery suppliers for regulatory approval
- **Capacity expansion + customer matching**: When B expands capacity and A launches new models → timing correlation
- **Teardown**: EV battery pack teardowns explicitly identify cell manufacturers

### Common A-Share Examples
- CATL (宁德时代): Dominant patent portfolio, easily identified as supplier via company announcements
- EV makers (NIO 蔚来, XPeng 小鹏): Zero cell patents → 100% external sourcing
- Putailai (璞泰来), Tianci (天赐材料): Material suppliers → use reverse workflow (their customers are battery makers)

---

## 4. Consumer Electronics

### Patent vs. Trade Secret Dynamics
- **Industrial design / appearance**: Strong design patent coverage
- **Internal components**: Component selection is procurement-driven, not IP-driven. Apple doesn't patent the OLED panel itself.
- **Assembly / integration**: Trade secret (Foxconn's assembly process)
- **Software / UX**: Copyright + trade secret + some patents

### Key Signals
- **Patent gap is THE NORM in consumer electronics**: A company not patenting components it buys is expected behavior. A patent gap here is weak signal.
- Component teardowns (iFixit, etc.) → the most reliable data source
- Supplier list in annual report → Apple, Xiaomi, Huawei all publish supplier lists

### Verification Strategy
- **Teardown > supplier list > patent gap**: Reverse priority vs. semiconductor/pharma
- Patent gap in consumer electronics is rarely a meaningful signal — companies consciously don't patent purchased components
- Focus on supplier lists, certification filings (3C certification in China), and teardowns
- **Trade secret assessment**: almost always "trade secret unlikely" → but this doesn't mean supply-chain dependency is confirmed; it means patent gap is the wrong signal here

### Common A-Share Examples
- Xiaomi (小米): Buys panels, chips, cameras → patent gap expected
- Luxshare (立讯精密), Goertek (歌尔股份): Contract manufacturers → their customers are the brand companies (reverse workflow)
- BOE (京东方): Panel maker → use reverse workflow to identify downstream phone/TV brand customers who buy from BOE

---

## 5. Materials / Chemicals

### Patent vs. Trade Secret Dynamics
- **Formulations / recipes**: Classic trade secret domain. Think Coca-Cola, DuPont's Kevlar, 3M's adhesives.
- **Synthesis routes**: Mixed. Some patented (process patents), some trade secrets.
- **Application patents**: How to USE a material → often patented by the user, not the producer. This creates a useful "reverse" patent gap signal.

### Key Signals
- Material user A has application patents for material M but zero production patents for M → A probably buys M
- Material producer B has composition + process patents → strong signal of capability
- High R&D-to-patent ratio → typical for materials companies, not suspicious

### Verification Strategy
- **Customer audits / qualifications**: Materials for electronics/auto/aerospace require lengthy qualification (1-3 years). Once qualified, switching costs are enormous.
- **Capacity expansion alignment**: When B adds capacity and A enters new markets → timing correlation
- **Trade secret assessment**: Often scores high, requiring procurement/teardown evidence to draw conclusions
- **Financial cross-validation**: Check A's raw material procurement categories against B's product line

### Common A-Share Examples
- Shin-Etsu (信越化学), SUMCO: Silicon wafer suppliers → their customers are semiconductor fabs (reverse workflow)
- Weihua (万华化学): MDI patents → downstream polyurethane users as customers
- Rongbai (容百科技), Dangsheng (当升科技): Cathode material suppliers → customers are battery makers

---

## Industry Selection Quick Reference

| If the target is... | Priority verification lead | Patent gap signal strength | Trade secret risk |
|---------------------|---------------------------|---------------------------|-------------------|
| Fabless semiconductor | Patent ownership (licensing) | **Medium** | Low |
| Foundry / process | Teardown + financial | **Weak** — process is trade secret | High |
| Innovative pharma | Patent expiry + ANDA | **Strong** — compounds are patented | Low |
| CDMO / CMO | Procurement + financial | **Weak** — processes are trade secrets | High |
| EV maker | Teardown + announcements | **Strong** — battery cells are outsourced | Low |
| Battery maker | Reverse workflow | **Medium** | Medium |
| Consumer electronics OEM | Teardown + supplier list | **Weak** — patent gap is normal | Low |
| Materials producer | Reverse workflow | **Medium** | High |
