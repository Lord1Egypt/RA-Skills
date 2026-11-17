> **Bilingual — 中英文皆可适配**  This skill ships both Chinese and English content. The Chinese counterpart of this file is the same name with `.zh` inserted (e.g. `README.zh.md`). The authoritative zh<->en terminology map lives in `references/glossary.yaml`.

# Third-party copyright & license notice (THIRD-PARTY.md)

> This file ships with the "Ontology Agent" product to fulfill the legal retention obligation for open-source components.
> The product itself (architecture / integration / Chinese localization / domestic deep packs / onboarding engine) is
> copyrighted by **Tianjin Weishu Artificial Intelligence Technology Co., Ltd.** (© Weishu).
> The third-party components below retain their copyright under their respective licenses; MIT / Apache-2.0 components
> permit building closed-source, commercial products on top, provided their copyright and license text are retained (this
> file). Each component's license should be finally verified before packaging (items marked * are preliminary records, to
> be verified).

## 1. Open-source components usable as closed-source base (MIT / Apache-2.0 etc., allow closed-source redistribution)

| Component | Repo | License | Used by this product | Notes |
|---|---|---|---|---|
| A1 semantic layer + Agent OS | 1mancompany/onemancompany | Apache-2.0* | entity primitive Entity{id,type,properties,relations} + write validation | semantic layer skeleton |
| A2 three-layer + governance | ibl.ai/ontology | MIT | four-layer architecture paradigm + roles/tools/services governance | architecture/governance spine |
| A4 RDF/OWL engineering | open-ontologies | to verify* | not used yet (future standard ontology upgrade) | not in current product |
| department-skill main axis | chendongqi/OPB-Skills (92) | to verify* | department action main axis (most complete in Chinese) | logic layer main axis |
| department skill | Frog1205/OPC-Skills (18) | MIT | complementary actions | logic layer |
| startup skill | slavingia/skills (10) | to verify* | complementary actions | logic layer |
| temp task force | baifengbai/Solo-Company-Skill (10) | to verify* | cross-dept elastic teaming | logic layer / expert |
| agent OS runtime | codeaudit/OneManCompany | to verify* | runtime reference | integration / runtime |
| OPC diagnosis | sober568/opc-zhinao (domestic) | MIT | five-stage diagnosis | decision / onboarding |
| OPC skill | ReScienceLab/opc-skills | to verify* | complementary | logic layer |
| edge-cloud framework | OpenBMB/edgeclaw (ModelBest) | MIT | edge-cloud sync / secure routing | runtime ② |

> *Items marked "to verify": before packaging, open each repo's LICENSE file to confirm the specific license version and
> copyright holder and complete this table accordingly. MIT / Apache-2.0 licenses permit closed-source redistribution but
> **must retain their copyright notice and license text** — this file fulfills that obligation.

## 2. Components whose content is NOT included

| Component | Repo | License | How this product handles it |
|---|---|---|---|
| OPC methodology | easychen/opc-methodology (9) | CC-BY-NC-SA (attribution + non-commercial + share-alike) | This product includes none of this component's code or text; its license does not require this product to attribute it or include its content. |

## 3. Compliance notes

1. This product is presented externally under the unified brand "Weishu Ontology Agent," without per-place attribution to the sources above.
2. This file exists only for legal compliance retention and does not expose implementation details to product users.
3. Copyright of any third-party component belongs to the original author's statement; Weishu asserts no rights over third-party content.
4. If the product is later open-sourced (L1 template, Phase 9 optional), the open-sourced part must still carry this file and the corresponding licenses.
