# GHS Safety Data Sheet Drafter (OSHA HCS 2024)

**Platforms:** Claude · Openclaw · Codex
**Domain:** Chemical Safety / EHS / Regulatory Affairs / Product Stewardship

## Purpose

Turns product identification, composition, and hazard data into a DRAFT 16-section Safety Data Sheet compliant with the U.S. OSHA Hazard Communication Standard 29 CFR 1910.1200 as amended in May 2024 (aligned to UN GHS Revision 7), against a compliance clock that includes the **May 19, 2026** deadline for substances and the **January 19, 2027** deadline for mixtures. Produces the SDS in OSHA Appendix D's required 16-section order, a GHS label preview (signal word, pictograms, H-statements, P-statements), a concentration-range disclosure worksheet for trade-secret (CBI) claims, a section-by-section authoring-gap list, an evidence index, and an open-questions list — for SDS author / industrial hygienist / EHS manager / regulatory affairs review and sign-off before publication.

## When to Use

- A chemical manufacturer, importer, or formulator must update an existing SDS to the HCS 2024 standard before the **May 19, 2026** (substances) or **January 19, 2027** (mixtures) compliance deadline
- A product steward is drafting an SDS for a new product (substance or mixture) before it ships
- A regulatory-affairs specialist is preparing a U.S. SDS for an imported product that currently has only a non-U.S. SDS (EU CLP, REACH-style, or other national format)
- An EHS manager needs to convert internal hazard data (composition, tox studies, physical-and-chemical data) into a publishable SDS
- A distributor needs a downstream-compliant SDS where the upstream supplier's SDS is missing required sections or is out of date
- An incident-response team needs to verify an SDS reflects the current product formulation after a reformulation, a recall, or a regulatory inventory change

## What It Does

**Phase 1: Scope and Compliance Clock**
1. Confirms scope (single substance vs mixture vs article — articles do not require an SDS), the product identifier on the label, intended use, and the jurisdictions in scope (default U.S. OSHA HCS 2024 — flag EU CLP, UK CLP, Canada WHMIS 2015 amended, Australia WHS, GHS-aligned national systems as out-of-scope-but-named where the user wants alignment)
2. Records the compliance clock: HCS 2024 effective dates — **May 19, 2026** substances, **January 19, 2027** mixtures — and the prior HCS 2012 baseline so the author knows which deltas to expect

**Phase 2: Sections 1, 3, 9 — Identification, Composition, Physical-and-Chemical**
3. **Section 1 (Identification)** — product identifier exactly as on the label, other means of identification, recommended use, restrictions on use, supplier name / address / phone, emergency phone (24/7 with country code)
4. **Section 3 (Composition / Information on Ingredients)** — ingredients with CAS number, EC number where available, common synonyms, concentration **range** (allowed under HCS 2024 with CBI claim), and per-ingredient hazard classification flags; includes a **Concentration Range Disclosure** worksheet for trade-secret claims that respects HCS 2024's revised range bands
5. **Section 9 (Physical and Chemical Properties)** — physical state, appearance, odour, odour threshold, pH, melting / freezing point, boiling point, flash point, evaporation rate, flammability, UEL / LEL, vapour pressure, vapour density, relative density, solubility, partition coefficient, auto-ignition temperature, decomposition temperature, viscosity, particle characteristics; explicit "Not applicable" vs "No data available" distinction

**Phase 3: Section 2 — Hazard Classification and Label**
6. Walks classification per OSHA Appendix A: physical hazards (explosives, flammable gas / aerosol / liquid / solid, oxidizing, gases under pressure, self-reactive, pyrophoric, self-heating, water-reactive, organic peroxide, corrosive to metals, desensitized explosives), health hazards (acute toxicity, skin corrosion / irritation, eye damage / irritation, respiratory / skin sensitization, germ-cell mutagenicity, carcinogenicity, reproductive toxicity, STOT-SE, STOT-RE, aspiration), environmental hazards (aquatic acute / chronic, hazardous to the ozone layer), with category-level rationale
7. For mixtures, applies the HCS 2024 mixture rules (bridging principles, additivity for acute toxicity, cut-off / concentration limits per hazard class) and flags any classification that requires test data rather than calculation
8. Produces the **GHS Label Preview**: product identifier, signal word (Danger / Warning), pictograms (GHS01–GHS09), H-statements with H-codes, P-statements (Prevention / Response / Storage / Disposal — selected per OSHA Appendix C precedence rules), supplier identifier

**Phase 4: Sections 4–8, 10 — Response and Handling**
9. **Section 4 (First-Aid)** — by route (inhalation, skin, eye, ingestion), most-important symptoms, indication of immediate medical attention
10. **Section 5 (Firefighting)** — suitable / unsuitable extinguishing media, specific hazards, advice for firefighters (PPE, special protective equipment)
11. **Section 6 (Accidental Release)** — personal precautions, environmental precautions, containment / cleanup methods
12. **Section 7 (Handling and Storage)** — safe-handling precautions, incompatibilities, storage conditions, specific end use
13. **Section 8 (Exposure Controls / Personal Protection)** — control parameters (OSHA PEL, ACGIH TLV, NIOSH REL, manufacturer OEL where set), engineering controls, individual protection (eye, skin, respiratory — with specific filter / cartridge / glove material recommendations)
14. **Section 10 (Stability and Reactivity)** — reactivity, chemical stability, possibility of hazardous reactions, conditions to avoid, incompatible materials, hazardous decomposition products

**Phase 5: Sections 11–16 — Tox, Eco, Disposal, Transport, Regulatory, Other**
15. **Section 11 (Toxicological Information)** — likely routes of exposure, symptoms by route, acute / chronic effects, LD50 / LC50 with species and route, sensitization, mutagenicity, carcinogenicity (with IARC, NTP, OSHA listings), reproductive toxicity, STOT-SE / STOT-RE, aspiration hazard — every data point cited
16. **Section 12 (Ecological Information)** — aquatic toxicity (acute / chronic with species), persistence and degradability, bioaccumulative potential, mobility in soil, PBT / vPvB assessment (flag if EU CLP is in scope)
17. **Section 13 (Disposal Considerations)** — description of waste residues, safe-handling for disposal, RCRA hazardous-waste codes where applicable, contaminated packaging
18. **Section 14 (Transport Information)** — UN number, UN proper shipping name, transport hazard class(es), packing group, environmental hazards (marine pollutant), special precautions, transport in bulk per IMO instruments; placeholder rows for U.S. DOT 49 CFR, IMDG, IATA, ADR / RID where applicable
19. **Section 15 (Regulatory Information)** — U.S. (TSCA, CERCLA RQ, SARA 311/312 hazard categories, SARA 313 TRI, CWA, CAA HAP, California Proposition 65), Canada (DSL / NDSL, CEPA, WHMIS), EU (REACH registration status, CLP classification, SVHC), other inventories (AICS Australia, IECSC China, ENCS / ISHL Japan, KECI Korea, PICCS Philippines, NZIoC New Zealand) — with explicit "Not listed" vs "Listed" vs "Not assessed" distinction
20. **Section 16 (Other Information)** — revision date, revision number, list of revisions vs previous version, key / legend for abbreviations, references, training advice, "this information is to the best of our knowledge…" boilerplate cleared by counsel / regulatory

**Phase 6: Authoring-Gap List, Evidence Index, Open Questions**
21. Produces a section-by-section authoring-gap list (every required field flagged "PRESENT" / "MISSING DATA — required" / "NO DATA AVAILABLE — disclose so on SDS" / "OPEN — needs research") so the SDS author and EHS manager see exactly what remains before publication
22. Builds the evidence index — supplier-of-record name, ingredient hazard data source (manufacturer SDS, supplier letter, ECHA REACH dossier, OECD eChemPortal, NIOSH Pocket Guide, IARC monograph, NTP RoC, ACGIH TLV booklet, peer-reviewed study), and the date of each — so every classification, exposure limit, and tox figure is traceable
23. Lists open questions (data needed before publication; ambiguous bridging-principle calls; jurisdictional questions; CBI / trade-secret approval status) and the compliance-clock countdown to the next applicable deadline

## Output

An SDS authoring packet consisting of a DRAFT 16-section SDS in OSHA Appendix D order, a GHS Label Preview (signal word, pictograms, H-statements, P-statements, product identifier, supplier identifier), a Concentration Range Disclosure worksheet for trade-secret claims, a section-by-section Authoring-Gap List, a numbered Evidence Index linking every classification / property / tox / eco / regulatory assertion to its source, an Open Questions list, and a Compliance-Clock summary showing days to the May 19, 2026 substances deadline and the January 19, 2027 mixtures deadline. The entire packet is marked **DRAFT — FOR SDS AUTHOR / INDUSTRIAL HYGIENIST / EHS MANAGER / REGULATORY AFFAIRS REVIEW AND SIGN-OFF**.

## Notes

This skill **drafts** a Safety Data Sheet to support — never replace — a qualified SDS author / industrial hygienist / EHS manager / regulatory affairs sign-off. The skill does not classify a substance or mixture as a final regulatory determination; classification under HCS 2024 / GHS Rev. 7 requires human judgment, often supported by test data the skill cannot generate. The skill does not approve trade-secret / CBI claims (only an authorized officer may), does not publish or distribute the SDS, does not generate the GHS-compliant printed label artwork (it generates the label content), and does not handle SDS distribution under HCS 1910.1200(g)(6) (downstream user distribution and access). The skill is U.S. OSHA HCS 2024 by default; EU CLP, UK CLP, Canada WHMIS 2015 amended, and other GHS-aligned national systems are flagged where the user names them but the skill does not silently apply them. Articles (29 CFR 1910.1200(c) definition) and exempted substances (consumer products under FHSA, pesticides under FIFRA labelling, foods, cosmetics, drugs, distilled-spirit and tobacco articles) are flagged as out of scope. The skill never claims that a missing data point is "no hazard" — missing data is disclosed as "No data available" per OSHA Appendix D's stated convention.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
