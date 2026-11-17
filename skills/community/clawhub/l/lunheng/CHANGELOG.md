# Changelog

## 3.0.0 (2026-07-29)

Pipeline v3 — Complete end-to-end pipeline with 7 modules.

### Added
- Reasoning scorer (6-dimension quality evaluation)
- Reasoning enhancer (auto-improve below-threshold reasoning)
- Case search (IMA + local shape_spirit)
- Case divergence analysis (5 patterns)
- Sentencing calculator (11 crime types)
- Style retriever (210 形与神 + 700+ award docs)

### Changed
- Unified config system (config.py, no hardcoded keys)
- Refactored 1701-line pipeline into 5 modules
- 90% cause template coverage (74 types)

## 2.2.0 (2026-07-19)

Phase 2 expansion — 59 cause templates (+90% from 24).

### Added
- 35 new civil cause templates
- Practice Profile mode with cold-start interview
- `refs/` dynamic loading architecture

## 2.0.0 (2026-06-04)

Phase 1 — Core RAG pipeline.

### Added
- Element parser (LLM + Regex hybrid)
- Parallel retriever
- Syllogistic assembler
- Markdown/HTML/DOCX formatters
- Law citation checker (3-layer validation)
- Quality checker
- Consistency checker
