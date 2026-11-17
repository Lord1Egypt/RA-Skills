# Changelog

All notable changes to Nutrigenomics are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [0.3.13] - 2026-09-15

### Fixed
- **Documentation figures no longer matched the panel.** README.md, README_OPENCLAW.md,
  SKILL.md, and openclaw.json still quoted an earlier panel size ("40+ genes", "8 nutrient
  categories", "58 SNPs"). Verified against `data/snp_panel.json` and corrected throughout to
  24 genes, 28 SNPs, 12 nutrient domains. SKILL.md also now notes 3 candidate variants
  (`ADRB2 rs1042713`, `HLA-DQ2`, `GSTT1`) that are documented for scientific context but not
  yet scored.
- **Generated report printed a stale tool version.** `generate_report.py` hardcoded
  `Nutrigenomics v0.2.8` in the report header regardless of the installed skill version. Now
  reads the version via `repro_bundle._skill_version()`, the same helper `provenance.json`
  already used, so the two cannot drift apart again.

---
## [0.3.12] - 2026-09-14

### Fixed
- **Two citations named the wrong paper.** Both pointed at studies that list the SNP only in a
  table of previously known loci:
  - `rs174546` (FADS1) cited PMID 25646338, a trans fatty-acid GWAS whose FADS1 hit is `rs174548`.
    Now PMID 20691134 (Zietemann et al. 2010, EPIC-Potsdam, n = 2066), which genotyped
    `rs174546` and reports it against PUFA levels and estimated delta-5 desaturase activity.
  - `rs4588` (GC) cited PMID 28757204, a CYP2R1 rare-variant paper (`rs117913124`). Now PMID
    19116321 (Sinotte et al. 2009), which genotyped `rs4588` and reports each rare allele with
    lower plasma 25(OH)D.

  Found by the ClawBio maintainer review of the same panel. The GWAS Catalog lists every variant
  appearing in a paper's known-loci table, which is not the same as the paper reporting it. No
  scores change.

---

## [0.3.11] - 2026-09-13

### Fixed
- **`rs953413` (ELOVL2, omega-3) scored the wrong allele as risk.** The panel had
  `ref_allele A`, `risk_allele G` for "decreased DHA synthesis", but the A allele is the one
  associated with lower DHA. In Tanaka et al. 2009 (InCHIANTI and GOLDN, PMID 19148276) DHA fell
  from GG through AG to AA in both cohorts (InCHIANTI 2.37 / 2.29 / 2.17, p = 0.004; GOLDN
  3.32 / 3.20 / 3.10, p = 0.002), and the authors state that "the presence of the minor (A)
  allele was associated with higher EPA/DPA and lower DHA". A functional study (iScience 2020,
  PMID 31928966) found the G allele gives higher ELOVL2 enhancer activity than A. GG, the
  highest-DHA genotype, was scored at maximum risk and AA at none. Now `ref G`, `risk A`.
  Orientation checked against Ensembl: G/A on the plus strand in GRCh37 and GRCh38, and not
  palindromic, so minus-strand T/C calls resolve correctly. **Omega-3 results for GG and AA
  genotypes change in every report generated before this release; AG is unaffected.**
- The citation for `rs953413` moves from Lemaitre et al. 2011 (PMID 21829377), which reports
  ELOVL2 through other, correlated SNPs, to Tanaka et al. 2009, which reports this SNP.
- `SKILL.md` listed `rs953413` in Evidence Quality Tier 1, defined as a catalogued genome-wide
  association for the exact variant. The GWAS Catalog has no omega-3 association for it, so it
  is now described separately with its actual evidence.

### Changed
- `rs953413` is described as an association with lower EPA-to-DHA conversion
  (`lower_epa_to_dha_conversion`), not as a requirement. Supplementation studies are mixed:
  minor-allele carriers showed larger EPA/DHA rises in the MARINA trial (PMID 24292947) and a
  2025 study (PMID 40114193), but not in the seAFOod trial (PMID 42135634), and none sets a
  genotype-specific intake.
- The omega-3 report advice no longer implies deficiency or names a daily dose from genotype.
  It points to direct EPA/DHA sources and to an omega-3 index test as the better guide to need.

### Added
- Regression tests pinning the `rs953413` direction on both strands (AA/TT = 2, AG = 1,
  GG/CC = 0) and the panel entry.

---

## [0.3.10] - 2026-09-12

### Fixed
- **Palindromic SNPs were strand-flipped, inverting homozygous reference into homozygous risk.**
  `extract_genotypes` falls back to a strand flip when the risk allele is not found in the
  reported genotype. For a palindromic (A/T or C/G) SNP, flipping produces the other allele of
  the same pair, so the flip *always* succeeds — and converts a call with no risk alleles into
  one with two. At `rs9939609` (FTO, T/A) a `TT` call, meaning zero risk alleles, was normalised
  to `AA` and scored 2 of 2.

  Three panel entries are affected: `rs9939609` (FTO, carbohydrate), `rs12934922` (BCMO1,
  vitamin A) and `rs1801282` (PPARG, fat metabolism). The A allele at rs9939609 runs around 40%
  in European populations, so roughly a third of users are `TT` and every one of them was
  reported at maximum FTO risk. **Results for these three SNPs change in every report generated
  before this release.**

  The module already contained `is_ambiguous()` for exactly this purpose, defined and never
  called. It is now consulted: palindromic SNPs are never flipped, and the alleles are trusted as
  reported, which is the only safe convention without allele-frequency context. Strand flipping
  is unchanged for the other 25 SNPs, where it is unambiguous and necessary.

### Added
- `strand_ambiguous` on each call, so downstream consumers can qualify these three SNPs.
- Regression tests covering all three genotypes at each palindromic SNP, the ambiguity flag, and
  that legitimate flipping still works at `rs4988235`.

---

## [0.3.9] - 2026-09-12

### Security
- **Closed the classes behind the recurring audit findings, rather than each instance.** Every
  release so far fixed the one thing flagged and the next scan found a neighbouring case. This
  release bounds the whole input/output surface and documents it.
- **Resource limits.** Streaming bounds how much of a file is held at once but not the genotype
  table, which grows with the variant count. `path_safety.py` now defines `MAX_INPUT_BYTES`
  (512 MB, rejected with a clear error), `MAX_VARIANTS` (10,000,000), `MAX_LINE_BYTES` (64 KB)
  and `MAX_HEADER_LINES` (1,000), enforced across every parser and the format sniffer. No file
  loop is unbounded any more.
- **Output directory collisions.** The adapter built a second-resolution directory name and
  created it with `exist_ok=True`, so two runs in the same second shared a directory and
  overwrote each other's report. It is now created exclusively, with random entropy appended on
  collision. Verified with three concurrent runs producing three distinct directories.
- **All report-rendered values escaped.** Gene symbols, rsIDs and effect descriptions are taken
  from the SNP panel, which `--panel` and API callers can supply. They are now filtered like
  genotypes and the filename, closing the injection class for every value the report writes.

### Added
- `Threat Model and Limits` section in `SKILL.md` stating what is treated as untrusted, the four
  risk classes and how each is handled, the limit table, and what is deliberately out of scope.
- Regression tests for oversized input, the variant cap, over-long lines, and panel-text escaping.

---

## [0.3.8] - 2026-09-12

### Security
- **Genotype calls are validated before they are scored or rendered.** Genotype values are read
  from a user-supplied file and written into a Markdown code span in the report, so a backtick in
  the genotype column broke out of that span exactly as a hostile filename did in 0.3.7 — this
  was the same defect one field over, and 0.3.7 fixed only half of it. All three parsers now
  accept only nucleotide calls (`A`, `C`, `G`, `T`, plus `D`/`I` for 23andMe deletions and
  insertions, allowing a run so VCF indels still parse) and discard anything else rather than
  scoring it. A value that is not a genotype cannot be biologically meaningful, so rejecting it
  is also the scientifically correct behaviour. `generate_report` guards the value again at
  render time, because `openclaw_adapter` and API callers supply genotypes directly without
  passing through a parser. (ClawHub audit of 0.3.7: "Unvalidated Genotype Values Allow Markdown
  and HTML Report Injection".)

### Added
- Regression tests covering accepted calls, rejected payloads, end-to-end discard of hostile
  values at parse time, and the render-time guard.

---

## [0.3.7] - 2026-09-12

### Security
- **The input filename is sanitised before it is written into the report.** The report header
  embeds the filename in a Markdown code span; a backtick in the name broke out of that span and
  allowed arbitrary Markdown or HTML into the document. The name is a concern wherever the file
  did not come from the person reading the report. It is now filtered to a conservative
  allowlist and truncated. (ClawHub audit of 0.3.6: "Untrusted Input Filename Embedded in
  Generated Markdown".)

### Changed
- `rs1535` (FADS2, omega-3) now cites Lemaitre et al. 2011, the CHARGE consortium meta-analysis
  of plasma phospholipid n-3 fatty acids (PMID 21829377), which analyses this exact SNP and
  reports weaker ALA-to-EPA conversion in minor allele carriers. It replaces a broader lipid
  metabolite GWAS and matches the citation already used for `rs953413` in the same pathway.
- `SKILL.md` now states that the input filename appears in the report header, why, and that
  renaming the file beforehand is the way to avoid it.

---

## [0.3.6] - 2026-09-12

### Security
- **Output writes are now pinned to a real parent directory.** `O_NOFOLLOW` guards only the
  final path component, so a symlinked parent directory could still redirect a write. The parent
  is now opened with `O_DIRECTORY | O_NOFOLLOW` and the file created relative to that descriptor,
  which pins a real directory inode and defeats a later swap of the parent. Verified by pointing
  a parent directory at another location and confirming the write is refused and nothing reaches
  the target. (ClawHub audit of 0.3.5: parent-directory symlink race.)

### Fixed
- **The AncestryDNA parser no longer loads the whole file into memory.** It read every line into
  a list before parsing, so memory use scaled with input size — a denial-of-service risk on large
  consumer genetic files. Comment lines are now filtered by a generator passed straight to
  `csv.DictReader`, which accepts any iterable of strings, so the file streams. (ClawHub audit of
  0.3.5, T09 memory exhaustion.) The other three parsers already streamed.
- Removed dead code in the same parser: it opened the file, built a `DictReader`, then tested
  `hasattr(reader, 'fieldnames')` — always true — so the result was discarded and the file was
  opened a second time.

### Added
- Regression test covering refusal to write through a symlinked parent directory.

---

## [0.3.5] - 2026-09-12

### Security
- **Output writes no longer follow symbolic links.** Output filenames are deterministic, so an
  attacker able to pre-create a symlink at one of them could redirect a write outside the
  directory `validate_output_dir` confines the skill to. All seven artefact writes — the report,
  both figures, and the four reproducibility files — now go through `safe_open_write`, which
  opens with `O_NOFOLLOW` and refuses a symlinked path. `O_EXCL` is deliberately not used, so
  re-running and overwriting a regular file still works. Verified by planting a symlink and
  confirming the write is blocked. (ClawHub audit: "Symlink Following Vulnerability".)
- **`reportlab` removed from the dependency list.** It was never imported anywhere in the skill,
  yet was declared in `requirements.txt`, the conda environment and `openclaw.json`. It carried
  the largest advisory history of any listed dependency, including remote code execution. Its
  entire risk surface is removed by deleting an unused declaration.

### Fixed
- Dependencies now carry upper bounds (`pandas>=2.2,<3.0`, `numpy>=1.26,<3.0`,
  `matplotlib>=3.8,<4.0`, `seaborn>=0.13,<1.0`), so a future major release cannot silently change
  behaviour. `requirements.txt` and the generated conda environment previously specified
  *different* floors for the same packages; they are now aligned.
- Path validation failures print a clean `[ERROR]` message and exit 1 instead of a traceback.
  Workspace confinement and symlink refusal are user-facing conditions, not defects.

### Added
- Regression tests covering symlink refusal and that overwriting a regular file still works.

---

## [0.3.4] - 2026-09-12

### Fixed
- **The reproducibility bundle recorded the path to the user's genetic data file.** Both
  `provenance.json` and `README_reproducibility.txt` echoed the full argument namespace, writing
  the absolute path of the input file into artefacts that simultaneously stated "Input file name
  and path are not recorded" and "The input file name and path are NOT stored in any artefact".
  The module docstring, an inline comment and the artefacts themselves all asserted a privacy
  property the code broke. Both artefacts now record only an explicit allowlist — `format`,
  `no_figures`, and a `custom_panel` boolean — and never a path. Found by the ClawHub security
  audit of 0.3.2 (finding T09, "Sensitive Genetic Input Path Persisted") and confirmed against
  a real run, whose `provenance.json` contained the full path to a personal genome file.
- The reproduce command printed in `README_reproducibility.txt` was malformed, emitting
  `--input <your_genetic_file> --input /real/path/...`. It now shows only the placeholder and
  the non-identifying flags.
- Artefacts reported `Version: 0.2.8`, hardcoded in two places and three releases out of date.
  The version is now read from `openclaw.json` at runtime so it cannot drift from the release.
- **`rs4988235` (MCM6 / lactase persistence) was scored backwards.** The reference and risk
  alleles were reversed, so the risk allele was set to the lactase *persistence* allele: an
  `AA` genotype scored 10/10 "elevated lactose risk" when it denotes full lactase persistence,
  and vice versa. Lactose results in every report produced before this release are inverted at
  this SNP.
- **The lactose scoring model ignored the trait's inheritance.** Lactase non-persistence is
  autosomal recessive (Enattah et al. 2002, PMID 11788828), so a single persistence allele is
  sufficient. The additive 0 / 0.5 / 1.0 model scored heterozygotes at half risk when they are
  lactase persistent. Panel entries may now declare
  `"inheritance": "dominant_protective"`; entries without the field remain additive, so no
  other SNP changes behaviour.
- **`rs4988235` cited an unrelated paper.** PMID 12369657 is a study of musculoskeletal pain in
  primary care. Replaced with PMID 11788828, the paper identifying the C/T-13910 variant.
- `snp_raw_score` now raises on an unexpected `risk_count` instead of silently scoring 0.0.
- **Every citation in the SNP panel was wrong except three.** An audit of all 23 unique PMIDs
  against PubMed found 20 pointing at unrelated papers — the folate entries cited a study of
  craniosynostosis, PPARG cited a paper on infant vaccination schedules, ALDH2 cited
  *Drosophila* geotaxis, and the antioxidant entries cited work on thoracostomy,
  glomerulonephritis and NK-cell receptors. Only FTO, TCF7L2 and BCMO1 cited the paper they
  claimed. All 28 entries now cite a verified source, checked against PubMed, and preferentially
  one with a catalogued genome-wide association for that exact variant and trait.
  The panel's biology is substantially unchanged; its provenance was not supportable.
- Corrected `CONTRIBUTORS.md` links that pointed at a repository other than this one.

### Added
- Regression test asserting that no artefact in the reproducibility bundle contains the input
  path, the input filename, or any local directory path.
- **`Evidence Quality` section in `SKILL.md`**, splitting the panel into GWAS-backed (Tier 1)
  and candidate-gene-only (Tier 2) entries, and documenting four specific caveats: the CYP1A2
  caffeine effect is significant only in smokers and is an inducibility effect; VDR TaqI is
  probably non-functional and is scored as a haplotype tag; the GPX1 phenotype study found no
  effect on erythrocyte glutathione peroxidase activity; and COMT's placement in the antioxidant
  domain reflects catechol handling rather than antioxidant defence. Scores are not weighted by
  evidence tier, so readers are told to treat Tier 2 signals as weaker.

### Credits
- The `rs4988235` correction was identified and fixed by **krudo-taco** in the ClawBio `nutrigx`
  skill (ClawBio/ClawBio@1163f49, MIT licence) and is adapted here with thanks. See
  `CONTRIBUTORS.md`.

---

## [0.3.3] - 2026-09-12

### Changed
- **`SKILL.md` is now platform-neutral.** Commands are documented relative to the skill's own
  directory, with each platform's path convention (`${HERMES_SKILL_DIR}`, `{baseDir}`) named
  rather than hard-coded, so one file serves OpenClaw/ClawHub and Hermes without per-platform
  edits. Example invocations use `nutrigenomics.py`; `openclaw_adapter.py` remains the
  structured entry point declared in `openclaw.json`.
- **Corrected the advertised panel size.** Earlier releases described the skill as analysing
  "40+ genes" / "58 SNPs" across "8 nutrient categories". The implemented panel
  (`data/snp_panel.json`) has always contained **28 SNPs across 24 genes and 12 nutrient
  domains**, and the generated report has always stated the true count. Documentation,
  `SKILL.md` frontmatter and `openclaw.json` metadata now match the implementation.
  The scope of the skill is unchanged — only its description was wrong. Users who installed
  an earlier release from ClawHub will see the advertised coverage decrease accordingly.
  (The correction landed in the repository on 2026-07-01 but was never released; this is the
  first version to carry it to ClawHub and the Hermes skills hub.)

### Added
- `metadata.hermes` frontmatter (tags, category) so the skill is indexed correctly by the
  Hermes skills hub, alongside the existing `metadata.openclaw` block.
- Top-level `version`, `license` and `compatibility` frontmatter fields, per the
  agentskills.io skill specification.
- `.github/workflows/publish-clawhub.yml`, publishing this skill to ClawHub on merge to `main`
  so the registry copy can no longer fall behind the repository.

### Fixed
- Repository restructured to `skills/nutrigenomics/` so that `hermes skills tap add` can
  discover the skill; the Hermes tap resolver looks only under `skills/` and offers no way to
  point at a repository root.
- Added skill output directories (`nutrigenomics_results/`, `nutrigenomics_output_*/`) to
  `.gitignore`. These contain per-SNP genotype calls when the skill is run on real data and
  must never be committed or published.

---

## [0.3.2] - 2026-05-17

### Fixed
- Excluded generated report output artefacts from local ClawHub publish scans so
  releases contain only source, documentation, test fixtures, and panel data.
- Aligned local version metadata across \`SKILL.md\`, \`openclaw.json\`, and the CLI
  module banner for the \`0.3.2\` release.

---

## [0.3.1] — 2026-04-05

### Fixed
- **`SKILL.md`** — Added `## Execution` section with explicit shell commands so the
  agent knows how to invoke the analysis directly rather than responding
  conversationally. Includes the standard invocation (`--input`, `--format auto`)
  and a ready-to-run demo command using the bundled synthetic patient file.
- Version bumped to 0.3.1 in `SKILL.md` and `openclaw.json`.

---

## [0.3.0] — 2026-04-05

### Fixed
- **`SKILL.md`** — Added required YAML frontmatter (`name`, `description`, `metadata`) so
  OpenClaw's skill loader can discover and register the skill. Previously the file
  contained only human-readable Markdown; without machine-parseable frontmatter the
  skill was silently skipped at the discovery stage and never appeared in
  `openclaw skills list`.
- **`SKILL.md`** — Added `metadata.openclaw.requires.bins: ["python3"]` to gate
  eligibility on Python 3 being present on PATH, and `emoji: "🧬"` for the macOS
  Skills UI.
- **`openclaw.json`** — Corrected `documentation.main` reference from
  `SKILL_OPENCLAW.md` to `README_OPENCLAW.md`, which is the actual user-facing guide.
- Removed `SKILL_OPENCLAW.md` (renamed `CLAWHUB_LISTING.md`; content fully covered by
  `README_OPENCLAW.md`) and excluded internal-only files (`IMPLEMENTATION.md`,
  `_meta.json`) from the published package.
- Version bumped to 0.3 in `SKILL.md` and `openclaw.json`.

---

## [0.2.8] — 2026-04-05

### Fixed
- **`README_OPENCLAW.md`** — `checksums.txt` description corrected: previously
  said "SHA-256 checksums of input and output files"; now correctly states only
  the SNP panel and output report are checksummed, with an explicit note that
  the input file is excluded to avoid creating a stable fingerprint.
- **`README_OPENCLAW.md`** — `provenance.json` description corrected: previously
  said "Timestamp, software version, and input filename"; now correctly states
  timestamp, software version, and analysis settings, with an explicit note that
  the input filename is not recorded.
- **`README.md`** — `provenance.json` line corrected from "Timestamp, version,
  and input filename metadata" to "Timestamp, version, and analysis settings
  (input filename intentionally not recorded)".
- Version strings bumped to 0.2.8 across `openclaw.json`, `SKILL.md`,
  `generate_report.py`, and `repro_bundle.py`.

---

## [0.2.7] — 2026-04-05

### Fixed
- **`openclaw_adapter.py`** — `report_path` and `figures` values in the result
  dict now return filenames relative to `output_dir`, rather than absolute system
  paths. The caller already has `output_dir`; embedding redundant absolute paths
  in additional fields exposed system path information for sensitive genomic data.
- **`openclaw_adapter.py`** — `cleanup_reminder` no longer embeds the absolute
  output path string; it now gives a generic instruction to delete `output_dir`
  after the user has downloaded their results.
- **`openclaw_adapter.py`** — Fixed inaccurate docstring on `analyse_file` that
  described the default `output_dir` as a "temp directory"; it is a persistent
  timestamped directory under the working directory.
- **`openclaw.json`** — Updated `output_schema` to reflect that `report_path`
  and `figures` are relative to `output_dir`; added `output_dir` field with
  clarifying description.
- Version strings bumped to 0.2.7 across `openclaw.json`, `SKILL.md`,
  `generate_report.py`, and `repro_bundle.py`.

---

## [0.2.6] — 2026-04-05

### Changed
- Moved `run_analysis()` entry point to the top of `openclaw_adapter.py`, immediately
  after imports, so the OpenClaw scanner can confirm the declared entry point
  (`openclaw_adapter:run_analysis`) without needing to parse the full file.

### Fixed
- Version strings bumped consistently to 0.2.6 across `openclaw.json`, `SKILL.md`,
  `generate_report.py`, and `repro_bundle.py`.

---

## [0.2.5] — 2026-04-05

### Added
- **`path_safety.py`** — Path validation module that was imported by the adapter but
  missing from the published package. Provides `validate_input_file`,
  `validate_output_dir`, and `validate_panel_file`, enforcing allowed extensions
  (`.txt`, `.csv`, `.vcf`) and blocking path traversal attacks.

### Fixed
- **`repro_bundle.py`** — Input file name and SHA-256 hash of the input file are no
  longer stored in any reproducibility artefact. Storing the filename risked persisting
  a personally identifiable label; storing the hash created a stable fingerprint of the
  user's genetic dataset. Only the SNP panel and generated report are now checksummed.
- **`SKILL.md`** — Removed `.gitignore` from the file structure diagram and updated
  `provenance.json` and `checksums.txt` descriptions to reflect the privacy-preserving
  behaviour introduced in this version.

---

## [0.2.4] — 2026-04-05

### Security / Privacy

- **`openclaw_adapter.py`** — Replaced `tempfile.mkdtemp` with an explicit
  timestamped output directory (`nutrigenomics_output_YYYYMMDD_HHMMSS/`) created
  under the working directory. Removes the false implication of auto-cleanup; output
  files now persist until the caller explicitly deletes them. Added `cleanup_reminder`
  key to the result dict so callers are reminded to delete the directory after use.
  Removed unused `import tempfile`.

- **`openclaw.json`** — Added `output_files_require_manual_cleanup: true` to the
  features block. Updated the security `notes` field to accurately describe that
  output files persist on disk until manually deleted and that the input file is
  never copied into the output directory.

### Documentation

- **`SKILL.md`** — Multiple accuracy fixes:
  - Removed erroneous `commands.sh` from the Key Outputs list and Algorithm step 5;
    replaced with the actual reproducibility artefacts (`README_reproducibility.txt`,
    `environment.yml`, `checksums.txt`, `provenance.json`).
  - Rewrote the Privacy section to accurately state that: (a) reports *do* include
    per-SNP genotype calls for the 58 panel SNPs by design; (b) full raw genome data
    is not reproduced; (c) output files persist until manually deleted.
  - Added note that no executable scripts are generated.
  - Bumped version from `0.1.0` to `0.2.4`.

- **`IMPLEMENTATION.md`** — Fixed the Security & Privacy checklist:
  - Replaced false "Temp files cleaned — auto-cleanup" item with accurate description
    of the timestamped output directory and manual cleanup responsibility.
  - Replaced false "No data persistence" item with accurate "Persistence scope
    documented" item clarifying that input is never copied but outputs persist.
  - Updated "Last updated" date.

- **`README.md`** — Fixed Reproducibility Package section (removed `commands.sh`,
  corrected file list). Corrected Privacy section bullet that incorrectly claimed
  reports never contain raw genotypes.

- **`README_OPENCLAW.md`** — Fixed "What You'll Download" section (removed
  `commands.sh`, corrected file list and descriptions). Corrected privacy bullet
  points and the claim that reports never contain raw genotypes.

### Changed

- Version bumped to `0.2.4` in `openclaw.json`, `SKILL.md`, `generate_report.py`,
  and `repro_bundle.py`.

---

## [0.2.3] — 2026-02-28

### Added

#### OpenClaw Integration
- **`openclaw_adapter.py`** — Function-based entry point for OpenClaw platform
  - `NutrigenomicsOpenClaw` class wraps analysis engine
  - `run_analysis()` entry point for web-based deployment
  - Structured JSON output with status, summary, risk scores, and file paths
  - Comprehensive error handling with user-friendly messages
  
- **`openclaw.json`** — Skill manifest for OpenClaw platform
  - Entry point registration
  - Input/output schema definitions
  - Dependency specifications
  - Metadata for platform discovery

#### Documentation
- **`SKILL.md`** — OpenClaw skill instructions
  - User-facing documentation optimised for web platform
  - "How to get your genetic data" guide
  - Quick start workflow
  - Detailed gene descriptions with examples
  - Privacy & security emphasis
  - Comprehensive FAQ and troubleshooting
  
- **`README.md`** — Main documentation
  - Step-by-step tutorial
  - Input file format specifications with examples
  - Understanding results section
  - Support and contribution information
  
- **`IMPLEMENTATION.md`** — Technical deployment guide
  - Installation and testing procedures
  - Platform integration steps
  - Environment configuration
  - Performance benchmarks
  - Security verification checklist

- **`ATTRIBUTION.md`** — Attribution and acknowledgments
  - Author and maintainer information
  - Links to authoritative scientific sources
  - Software and library acknowledgments
  - Citation formats (BibTeX, APA, Chicago)
  - Transparency about AI-assisted development

#### Licensing & Community
- **`LICENSE`** — MIT License
  - Open-source, permissive licensing
  - Copyright © 2026 David de Lorenzo
  - Allows commercial and private use

- **`CONTRIBUTORS.md`** — Community contribution framework
  - How to report bugs
  - How to suggest SNPs
  - Code contribution guidelines
  - Recognition pathways for contributors
  - Code of conduct

#### Core Features
- **SNP Panel**: 58 SNPs across 40+ genes
- **Nutrient Categories**: 8 categories (micronutrients, macronutrients, omega-3s, caffeine, alcohol, sensitivities, antioxidants, detoxification)
- **File Format Support**: 23andMe, AncestryDNA, VCF
- **Risk Scoring**: 0-10 scale per nutrient
- **Visualisations**: Radar charts and interaction heatmaps
- **Privacy**: 100% local processing, no data transmission
- **Reproducibility**: Complete analysis bundles with documentation

### Changed
- Rebranded as Nutrigenomics for consumer-focused OpenClaw platform
- Web-based interface accessible to general users
- Simplified installation (direct GitHub or ClawHub registry)
- Updated all documentation for OpenClaw users

### Fixed
- `.DS_Store` files excluded from version control
- Removed unverified scientific citations
- Improved error messages for common issues
- Better handling of incomplete file formats

---

## Known Issues & Limitations

### About This Project

**Nutrigenomics** is the consumer-focused, web-based version of nutrigenomics analysis for OpenClaw. 

For healthcare professionals and researchers, a professional-grade command-line tool (**NutriGx Advisor**) is available for ClawBio platform, offering advanced features and integration capabilities for clinical and research workflows.

### Current Limitations (v0.2.3)

1. **Common Variants Only**
   - SNP panel limited to MAF > 1% in major populations
   - Rare pathogenic variants not detected
   - Primarily based on European GWAS data

2. **Gene × Environment Not Modeled**
   - Current analysis is genotype-only
   - Doesn't account for diet, lifestyle, environment
   - Future versions will integrate these factors

3. **File Size Limits**
   - VCF files should be <100MB
   - Large genomic files may timeout
   - Consider splitting very large datasets

4. **Population Context**
   - SNP effects derived from European ancestry studies
   - May not apply equally to other populations
   - Users encouraged to consult healthcare providers

5. **Educational Use Only**
   - Not a medical diagnostic tool
   - Cannot diagnose nutrient deficiencies
   - Cannot prescribe treatments
   - Should supplement, not replace, professional advice

### Recommendations for Users

- **Consult Healthcare Providers** — Always verify findings with qualified professionals
- **Biomarker Testing** — Confirm nutrient status with blood tests
- **Dietary Assessment** — Combine genetic findings with actual dietary intake analysis
- **Professional Guidance** — Work with dietitians for personalised meal planning

---

## Future Directions

Community feedback and contributions welcome! Areas of interest for future development:

- **Microbiome Integration** — Understand how gut bacteria interact with your genetics
- **Dietary Tracking** — Sync nutrition data with genetic recommendations
- **Population Expansion** — Include non-European ancestry populations
- **Advanced Analytics** — Machine learning for personalized predictions
- **Healthcare Integration** — Connect with medical professionals for clinical use

---

## Contributing

We welcome contributions from:
- **Researchers** — Suggest new SNPs or analysis methods
- **Developers** — Improve code, add features, fix bugs
- **Translators** — Help make documentation available in other languages
- **Users** — Share feedback and use cases

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for guidelines.

---

## Citation

If you use Nutrigenomics in research or education:

### BibTeX
```bibtex
@software{delorenzo2026nutrigenomics,
  author = {de Lorenzo, David},
  title = {Nutrigenomics: Personalised Nutrition from Genetic Data},
  year = {2026},
  url = {https://github.com/drdaviddelorenzo/nutrigenomics},
  version = {0.2.3}
}
```

### APA
de Lorenzo, D. (2026). *Nutrigenomics: Personalised nutrition from genetic data* (Version 0.2.3) [Software]. Retrieved from https://github.com/drdaviddelorenzo/nutrigenomics

### Chicago
de Lorenzo, David. "Nutrigenomics: Personalised Nutrition from Genetic Data." Version 0.2.3. Accessed [Date]. https://github.com/drdaviddelorenzo/nutrigenomics.

---

## Resources

- **GitHub**: https://github.com/drdaviddelorenzo/nutrigenomics
- **Author**: [@drdaviddelorenzo](https://github.com/drdaviddelorenzo)
- **Website**: https://drdaviddelorenzo.github.io
- **Email**: david@drdaviddelorenzo.dev
- **OpenClaw**: https://openclaw.ai
- **ClawHub**: https://clawhub.ai

---

## License

MIT License — See [LICENSE](LICENSE) for full details.

© 2026 David de Lorenzo
