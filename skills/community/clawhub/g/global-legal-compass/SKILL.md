# Global Legal Compass (全球法律罗盘)

## Description
A comprehensive multi-jurisdiction legal intelligence skill spanning 9 major jurisdictions (US, EU, UK, China, Japan, India, Singapore, Australia, UAE) and 10 legal domains. Provides cross-border legal research, regulatory comparison, contract analysis, compliance mapping, case law search, IP strategy, data privacy assessment, sanctions screening, M&A threshold analysis, and international dispute resolution guidance. Integrates with WorldLII, EUR-Lex, BAILII, Indian Kanoon, PKULaw, and 15+ other authoritative legal databases.

**Keywords**: legal, law, compliance, regulation, contract, litigation, GDPR, IP, patent, trademark, M&A, arbitration, sanctions, privacy, corporate, tax, cross-border, international law, case law

## Triggers
- "what are the legal requirements for [action] in [jurisdiction]"
- "compare [regulation/law] between [country A] and [country B]"
- "is this contract clause enforceable in [jurisdiction]"
- "what are the M&A filing thresholds in [country/region]"
- "data privacy obligations for [use case] across multiple jurisdictions"
- "search case law on [legal question] in [jurisdiction]"
- "international arbitration options for [type of dispute]"
- "IP protection strategy for entering [market]"
- "is [entity/country] subject to sanctions"
- "employment law comparison: [country A] vs [country B]"
- "what is the statute of limitations for [claim] in [jurisdiction]"
- "regulatory landscape for [industry/sector] in [region]"
- "double tax treaty benefits between [country A] and [country B]"

## Capabilities

### 1. Multi-Jurisdiction Legal Research
Search and compare laws across 9 core jurisdictions with structured comparison:
| Jurisdiction | Legal System | Case Law DB | Statute DB | Language |
|---|---|---|---|---|
| United States | Common Law | Google Scholar / CourtListener / PACER | USC / CFR | English |
| European Union | Civil Law (Supranational) | EUR-Lex / CURIA | TFEU / GDPR / DSA | 24 languages |
| United Kingdom | Common Law | BAILII / Supreme Court | UK Public General Acts | English |
| China | Socialist/Civil Law | Wenshu / PKULaw | Civil Code / PIPL | Chinese |
| Japan | Civil Law | Courts.go.jp | JLTP | Japanese |
| India | Common Law | Indian Kanoon / SCC | DPDP Act 2023 | English |
| Singapore | Common Law | Singapore Law Watch | PDPA | English |
| Australia | Common Law | AustLII / FedCourt | Corporations Act | English |
| UAE | Civil/Islamic Law | DIFC / ADGM | DIFC Laws | Arabic / English |

### 2. Legal Domain Coverage (10 Domains)

**Contract Law**
- Cross-border contract analysis under CISG (97 contracting states)
- Clause enforceability checks: force majeure, limitation of liability, indemnification, governing law, dispute resolution
- Common Law vs Civil Law divergence points (consideration vs cause, good faith obligations, penalty clauses)
- Boilerplate audit: entire agreement, severability, assignment, waiver, notices

**Corporate Law & Governance**
- Entity type comparison across jurisdictions (LLC / GmbH / Ltd / K.K. / 有限公司 / Pte Ltd)
- Fiduciary duty standards by jurisdiction
- M&A deal structures: share purchase vs asset purchase vs merger
- Cross-border investment screening: CFIUS (US), FDI screening (EU), NSIA (UK), FDI Policy (India)

**Intellectual Property**
- Patent strategy: PCT filing roadmap, first-to-file vs first-to-invent, grace periods
- Trademark: Madrid Protocol designation strategy, use requirements by jurisdiction
- Copyright: Berne Convention coverage, fair use (US) vs fair dealing (UK/Commonwealth) vs enumerated exceptions (EU/CN)
- Trade secret: DTSA (US) vs EU Directive vs CN Anti-Unfair Competition Law
- AI-generated content IP status (emerging, jurisdiction-dependent)

**Data Privacy & Protection**
- 8-regime comparison matrix: GDPR / CCPA/CPRA / PIPL / LGPD / DPDP Act / APPI / PIPA / PDPA
- Cross-border data transfer mechanisms: SCCs, BCRs, adequacy decisions, CBPR, APEC
- Data breach notification timeline by jurisdiction (72 hours GDPR, "without undue delay" CCPA, etc.)
- DPO requirement, DPIA triggers, data subject rights comparison

**Employment & Labor**
- At-will (US) vs just-cause (most other jurisdictions) termination frameworks
- Non-compete enforceability map (California ban vs global variance)
- Remote work / work-from-home: tax nexus, employment law applicability, permanent establishment risk
- Gig worker classification trends globally (Uber cases across jurisdictions)

**International Trade & Sanctions**
- Sanctions screening workflow: OFAC SDN + EU Consolidated + UNSC + OFSI + DFAT
- Export control classification: ECCN (US), Dual-Use Regulation (EU), military end-use
- WTO dispute resolution process overview
- FTA utilization analysis: rules of origin, cumulation, tariff preference

**International Tax**
- OECD BEPS 2.0 Pillar 1 & 2 implementation status by jurisdiction
- Withholding tax rates on dividends/interest/royalties under major tax treaties
- Permanent establishment risk assessment for digital/remote business models
- Transfer pricing documentation: master file, local file, CbCR requirements

**Dispute Resolution & Arbitration**
- Arbitration venue selection guide: ICC vs SIAC vs HKIAC vs LCIA vs SCC vs DIAC
- New York Convention enforcement (172 states)
- Investment treaty arbitration (ICSID)
- Litigation vs arbitration trade-off analysis for specific disputes

**Competition / Antitrust**
- Merger control thresholds: US (HSR ~$119.5M), EU (€2.5B+ / €100M+), CN (¥12B+ / ¥800M+), UK (share of supply)
- Abuse of dominance standards: US (consumer welfare) vs EU (special responsibility) vs CN (internet platform rules)
- Cartel enforcement and leniency programs
- Digital markets regulation: DMA (EU), proposed US legislation, platform antitrust in Asia

**Crypto / Digital Assets Law**
- MiCA (EU) comprehensive crypto regulation
- SEC vs CFTC jurisdiction (US) — Howey test for digital assets
- VASP licensing: HK SFC, Singapore MAS, Dubai VARA
- FATF Travel Rule implementation status by jurisdiction
- Stablecoin regulation, CBDC legal frameworks, DeFi liability

### 3. Research & Output Framework

**For any legal query, follow this structure:**

```
Step 1: JURISDICTION IDENTIFICATION → Which jurisdictions are relevant?
Step 2: DOMAIN CLASSIFICATION → Which legal domains apply?
Step 3: PARALLEL SEARCH → Execute jurisdiction-specific + domain-specific searches
Step 4: COMPARATIVE ANALYSIS → Side-by-side comparison where multiple jurisdictions
Step 5: REGULATORY CITATION → Cite specific statutes/articles with public URLs
Step 6: CASE LAW REFERENCE → Where relevant, cite key precedents with court + date
Step 7: RISK FLAG → Highlight non-compliance penalties, liability exposure, timing urgency
Step 8: DISCLAIMER → Explicitly: "This is legal information, not legal advice. Consult local counsel."
```

### 4. Output Formats

**Regulatory Comparison (Multi-Jurisdiction)**:
| Aspect | US | EU | China | Singapore | Japan |
|--------|----|----|-------|-----------|-------|
| Statute | ... | ... | ... | ... | ... |
| Scope | ... | ... | ... | ... | ... |
| Penalty | ... | ... | ... | ... | ... |
| Key Date | ... | ... | ... | ... | ... |

**Case Law Brief**:
- Case name + Citation + Court + Date
- Facts (2-3 sentences)
- Issue (legal question)
- Holding (the court's answer)
- Reasoning (legal principles applied)
- Relevance to query

**Compliance Checklist (for specific use case)**:
- [ ] Requirement 1 — applicable under [statute §X]
- [ ] Requirement 2 — deadline [date], penalty [amount]
- ...each item with actionable guidance

**Contract Clause Analysis**:
- Clause text
- Governing law analysis
- Enforceability assessment (by jurisdiction)
- Risk level: HIGH / MEDIUM / LOW
- Suggested negotiation fallback positions

## Workflow

```
User Legal Query
    ↓
[Step 1] Identify jurisdiction(s) + legal domain(s)
    ↓
[Step 2] Parallel web_search across jurisdiction-specific databases
    ↓
[Step 3] web_fetch primary legal sources (statutes, regulations, key cases)
    ↓
[Step 4] Cross-reference with legal_sources.json jurisdictional data
    ↓
[Step 5] Apply domain-specific analysis framework
    ↓
[Step 6] Generate comparative table if multi-jurisdiction
    ↓
Final Output: Structured legal brief with citations + risk flags + disclaimer
```

## Usage Guidelines

1. **No Legal Advice**: Always append disclaimer — "This is legal information for educational/research purposes. For binding legal decisions, consult a qualified attorney in the relevant jurisdiction."
2. **Source Dating**: Every citation must include the effective date or last-updated date. Flag any legal content older than 6 months as potentially outdated.
3. **Primary Sources Preferred**: Prioritize official government legal databases (EUR-Lex, BAILII, Congress.gov) over secondary commentary. Use secondary sources (Lexology, Mondaq) for interpretation only.
4. **Conflict Disclosure**: When legal positions differ between authorities within the same jurisdiction (e.g., circuit split in US), explicitly note both positions.
5. **Emerging Areas**: For rapidly evolving areas (AI law, crypto, gig economy), note "This area is under active legislative/regulatory development" and provide the latest known status.
6. **Language**: Match response to user's language. For non-English jurisdictions, provide both original language statute name and English translation where available.
7. **Sanctions First**: For any cross-border transaction query, always check sanctions applicability before proceeding to substantive analysis.

## Examples

**Query**: "We're a SaaS company expanding to Germany and Japan. What data privacy obligations do we have?"

**Response Structure**:
1. Jurisdiction identification: Germany (GDPR, Member State) + Japan (APPI)
2. GDPR analysis: extraterritorial scope, lawful bases, DPO requirement for processing special categories, SCCs for data transfer, 72-hour breach notification, €20M/4% penalty
3. APPI analysis: domestic scope + cross-border transfer rules (consent + equivalent protection), PPC oversight, ¥100M penalty
4. Comparison table: GDPR vs APPI — scope, DPO, breach timeline, cross-border mechanism, penalty
5. Compliance checklist: 12-step actionable items for SaaS deployment in both jurisdictions
6. Disclaimer

**Query**: "Search US case law on whether clicking 'I agree' constitutes valid electronic signature"

**Response Structure**:
1. Domain: Contract Law / E-SIGN Act (15 U.S.C. § 7001) / UETA
2. Key cases with case briefs: (a) Specht v. Netscape, (b) Register.com v. Verio, (c) Meyer v. Uber, (d) Kauders v. Uber
3. Legal principle synthesis: Clickwrap vs browsewrap, reasonable notice, manifest assent
4. Circuit split notation (if applicable)
5. Practical guidance for enforceable clickwrap design
6. Disclaimer

## References
- `references/legal_sources.json`: 9 jurisdictions × 10 legal domains, 15+ legal databases with URLs, sanction regimes, arbitration venues, data privacy penalty comparison (8 regimes), M&A filing thresholds, entity types, IP treaty framework