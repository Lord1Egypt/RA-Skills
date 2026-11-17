# P0 source analysis (2026-11-12)

Source: https://github.com/xiaoyang111222/cn-math-taxonomy

## Verified repository components
- `data/topics.json`: knowledge-node records; upstream README documents mastery criteria, sample diagnostic question and curriculum alignments.
- `data/dependencies.json`: `topicId`, `prerequisiteId`, `strength` (`hard` or `soft`), `reason`.
- `diagnose/engine.js`: original CommonJS/browser-compatible diagnostic implementation providing graph building, session, question, answering, summarization, grade targeting and results.
- `package.json`: scripts for Node/Python engine, question, UI and data validators.
- Browser UI is static/PWA and uses local chart libraries.

## Architecture decisions
1. **Do not reuse upstream code or data**. Its top-level repository LICENSE and README specify CC BY-NC 4.0. The `package.json` `license: ISC` field conflicts with these explicit files; treat effective permission as restricted until clarified with rights holder. Third-party vendored components have separate MIT licenses. This package contains a new implementation and new example data only.
2. Preserve graph and mastery concepts rather than source code. Use independent subject DAGs; cross-domain references, if needed, must live outside the prerequisite-edge relation.
3. Separate graph core and diagnosis from app state. Academy provides auth, persistence, privacy, UI, and question evaluator.
4. Use conservative screening: no mastery inferred from descendant success; status `weak` only after two wrong attempts. No claims of psychometric validity.
5. Use standard JSON with explicit provenance/quality fields in production datasets; the bundled demonstration is illustrative, not reviewed curriculum.

## P0 findings / limitations
- Repository-level `package.json` declared ISC while README and LICENSE explicitly say CC BY-NC 4.0 — do not interpret this as permission for commercial reuse.
- Original author notes unresolved teacher review of prerequisite edges, question validity and alignment; consuming upstream assertions as certified teaching material would be unsafe.
- Current package tests the *independent DAVYLAB engine*, not the upstream engine or the deployed Academy.
- A later P2 integration must implement audited question scoring, adaptive question selection, session privacy, accessibility and source/licensing governance.

## Provenance
Read-only analysis of public README.md, LICENSE, package.json, first records of dependencies.json and opening of diagnose/engine.js via connected GitHub source. No upstream source files are distributed here.
