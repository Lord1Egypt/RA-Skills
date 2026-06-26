# Changelog

## v3.0.4 — Chinese Localization (2026-05-26)

- README.md fully localized to Chinese.
- SKILL.md description localized to Chinese.
- Public version: 3.0.4.

## v3.0.3 — Patch Release (2026-05-26)

- Version bump to 3.0.3.

## v3.0.1 — Stable Release / Branch D + F Cross-Validation Complete (2026-05-25)

- Branch D (Developmental/Educational): Cross-validated with working memory updating across development test case.
- Branch F (fMRI/EEG Neuroimaging): Cross-validated with subsequent memory fMRI test case.
- Cross-type validation now covers all 9 branches: A–I.
- Public version updated to 3.0.1.

## v3.0.0 — Stable Release (2026-05)

- Stable release after cross-type validation across all 9 branches: A, B, C, D, E, F, G, H, I.
- Default output changed to standard mode (was close-reading in v2.x).
- Retains quick, standard, and close-reading modes.
- Mode-adaptive user-visible prompt replaces fixed close-reading prompt.
- Added Module H: Writer Transfer Packet for downstream integration with academic-results-writer.
- All source-verification, causal-language, anti-template-contamination, branch-specific guardrails retained.
- Public version: 3.0.0 | Internal version: psychology-results-reverse-analysis-v3.0-bridge

---

## v2.8 (2025-04–05) — Branch H Qualitative + Branch G Neuroimaging + Branch B Reinforcement

### v2.8 patch 7
- Branch B: Added cross-paper template text contamination check (B7b).
- Branch B: Added PROCESS/SEM sign consistency check (B7c).
- Branch H / CGT: Expanded H6 from 4→8 demographic audit rules; added H6a Diagnosis Counting Rule.
- Cross-type validation: Branch B ✅ (Huang et al. 2022), Branch H / CGT ✅ (Kuek et al. 2024).

### v2.8 patch 6
- Branch G: Added neuroimaging coordinate-based meta-analysis subbranch (G9–G17).
- Rules: ALE ≠ pooled ES (G10), functional decoding ≠ moderator analysis (G11), MACM guardrail (G12), absence evidence caution (G13), coordinate-label consistency (G14), caption-method threshold mismatch (G15), Discussion model separation (G16), G0 source verification fields (G17).
- Cross-type validation: G / neuroimaging ✅ (Kohn et al. 2014).

### v2.8 patch 3
- Branch H: Added Qualitative Study dedicated rules (H1–H9).
- Rules: Results full-scan (H1), theme heading detection (H2), supplementary appendix statement (H3), reflexivity grading (H4), intercoder reliability epistemology-sensitive (H5), demographic table audit (H6), theme count inconsistency (H7), Module C structure + quote extraction (H8), G0 source verification (H9).
- Cross-type validation: Branch H ⚠️ (Barnett et al. 2021).

### v2.8 patch 2
- Clinical RCT: Absence Claim Confidence Rule (Rule 4), Derived Clinical Metric Labeling Rule, Standardized Effect Size Precision Rule, C1c dose-response ambiguity severity adjustment.
- Clinical RCT Module F output depth rules: standard mode condensed, full slides only on request.
- Added Cross-Type Validation Status table.

### v2.8 patch 1
- Branch C1: Clinical Intervention RCT dedicated rules (C1a–C1h).
- Rules: AE/safety check (C1a), prognostic-vs-AE distinction (C1b), session attendance direction ambiguity (C1c), clinical significance separation (C1d), active comparator strength (C1e), Module B 14-block structure (C1f), G0 source verification fields (C1g), active comparator source check (C1h).
- Cross-type validation: Clinical RCT ✅ (Eisendrath et al. 2016).

---

## v2.7 (2025-03–04) — Branch B Survey + Branch I Simulation

### v2.7 patch 6
- Module B: Added B0 Results Heading Detection Rule (universal mandatory pre-check).
- Branch B: Anti-template whitelist for clinical/health survey domain (clinical diagnosis / DSM / ICD).
- Module E: Anti-duplication rule for evidence stratification tables.
- Branch B cross-validation: Li et al. (2021).

### v2.7 patch 5
- Branch I: Methodological / Simulation Study dedicated rules (I1–I6).
- Rules: Simulation Study Profile (I1), N/A rule (I2), Module B structure (I3), Module D chart rules (I4), evidence boundary (I5), anti-template contamination (I6).
- Cross-type validation: Branch I ✅ (Carter et al. 2019).

### v2.7 patch 4
- Three-axis classification system (Article Type × Domain × Data Modality) fully implemented.
- Branch G meta-analysis rules (G1–G8).
- Branch B survey/correlational rules (B1–B9).
- Cross-type validation: Branch G ✅ (Bolier et al. 2013), Branch B ✅ (Li et al. 2021).

---

## v2.5 (2025-02–03) — Foundation Release

- Initial multi-branch release with Branches A–F.
- Study Profile first workflow.
- Phase 0.5 Evidence Validation Rules (Day/Session, Stimulus Pool, Design Taxonomy).
- Module A–G specifications with branch-specific guidance.
- Causal Language Ladder by study design.
- Template pollution prevention framework.
- Psychometric / Clinical Screening Tool Branch Rules (Rules 1–9).
- Branch C intervention subtype classification (C1–C6).
- Cross-type validation: Branch A ✅ (Dimsdale-Zucker et al. 2018), Branch C ✅, Branch E ✅ (Kroenke et al. 2001).

---

## v2.0 (2025-01) — Multi-Branch Architecture

- Introduced adaptive branching (A–E initially).
- Module A–G structure.
- File-first output policy.

---

## v1.x (2024) — Single-Branch Prototype

- Initial release focused on cognitive neuroscience / fMRI experiments.
- Single-branch analysis with 14 function labels.
- Basic Study Profile and Module structure.
