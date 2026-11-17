# Optional Structured Evidence for Visual Scores

Use for PDF/images when local OMR is installed. This reference does not authorize installation, model downloads, cloud recognition, or score uploads.

A missed rest, ledger-line pitch, accidental, or chord member changes the event sequence before fingering. Local OMR proposes voices, rhythm, harmony, and keys; the source page remains authoritative.

Audiveris is separately installed AGPL-3.0 software. Do not bundle its code, models, or binaries. Discovery supports PATH, macOS app bundles, and default Windows installs. A host with CLI execution can operate it without GUI interaction.

1. Invoke an installed engine with user authorization into a new candidate directory.
2. Prefer original structured MusicXML/MXL for semantics and original PDF/images for coordinates. OMR MusicXML supplies candidate semantics.
3. create_semantic_review_ledger.py combines candidate reports and visual templates. Compare heads, rests, durations, clefs, keys, accidentals, ties, and chord members by measure. Queue discrepancies/engine risks; the ledger cannot unlock facts.
4. Take head centers from current pages. Re-engraved coordinates cannot be mapped to the original PDF. Attach .omr geometry transactionally by page/measure/hand only where counts and chord clustering agree.
5. Preserve actual page measure counts, including trailing rests. A mismatch blocks only that scope, without shifting later measures.
6. Complete visual delivery requires independent raw-page counts and four geometry audits. OMR-only delivery remains review-required.

run_optional_omr.py requires --allow-local-omr, rejects existing output directories, and writes started/running/failure/success receipts. Preserve reports after failure/timeout and fall back to visual facts without endless retries.

Audiveris runs serially under an OS lock; default queue timeout is 30 seconds. Geometry statistics use a separate process capped at 30 seconds; a timeout adds risk without blocking the candidate report. Unsolved rhythms, missing time offsets, and unlinked symbols enter semantic_risk_signals for focused review even when MXL export succeeds.

Structured inputs need no OMR. PDF/images plus OMR use two-source review; visual-only inputs remain supported within independently confirmed scopes. Deliver unresolved crops and recovery files instead of inferred notes.

Official CLI: https://audiveris.github.io/audiveris/_pages/guides/advanced/cli/
Export limitations: https://audiveris.github.io/audiveris/_pages/tutorials/quick/export/
