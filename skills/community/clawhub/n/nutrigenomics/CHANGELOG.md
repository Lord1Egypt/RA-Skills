# Changelog

All notable changes to Nutrigenomics are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
