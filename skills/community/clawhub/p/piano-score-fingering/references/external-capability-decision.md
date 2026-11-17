# Optional External Capabilities

The skill runs in agent hosts with local file and script execution. Add external tools only for concrete reliability gaps.

## Eligibility

Prefer free/open-source, common, cross-platform local tools obtainable through ordinary domestic/international channels. Do not upload scores, require paid APIs, impose region-specific services, or introduce unclear licenses. Bundled code needs MIT-compatible terms; separately installed programs retain their own terms and remain process/code/data separate. Do not automatically download programs, models, or dependencies.

## Optional local OMR

Audiveris can provide candidate MusicXML for PDF/images, followed by original-page review through create_semantic_review_ledger.py. It is AGPL-3.0 and separately installed; no binaries, models, or source are bundled. See structured-omr.md.

Probe OCR languages using setup_audiveris_language.py --probe. Only explicit download authorization permits fetching a needed language, usually eng, from official tesseract-ocr/tessdata into Audiveris user configuration. Users can remain in the conversation; this does not authorize silent downloads.

Historical Apple Silicon/Audiveris 5.11.0 trials exported three private PDFs in approximately 38–159 seconds, all with engine risks. A GUI launcher later failed during Java AWT registration; headless use of the official bundled Java/JAR resolved that startup route. Successful export is not evidence of correct score facts.

Whole-score trials showed local differences such as Morning Grass 420 OMR heads versus 413 MXL notes, and Tears 323 versus 311. Transactional attachment blocks only mismatched page/measure/hand scopes. Equal global counts still do not verify rhythm, octaves, or ties. Actual timing and risk counts vary by source/runtime; retain current receipts.

## Experimental Oemer

Oemer is an MIT image-to-MusicXML project with ONNX/OpenCV dependencies and separate model downloads. It does not directly accept PDF: render a page PNG first. An installed user-selected oemer command may produce a second local candidate under the same review/anchor rules.

A local Tears trial failed to finish within 120 seconds; the wrapper therefore treats Oemer as experimental with a 90-second single-page default. A timeout preserves its report and falls back. Do not bundle its model or outputs or infer suitability solely from its code license.

## Not selected as defaults

- **PianoPlayer as a second runtime:** the bundled core already derives from this project. Historical anchor-free comparisons were inconsistent: on Canon the external solver scored 32/67 versus the then-current 31/67; on Greensleeves it scored 8/14 versus 12/14. This does not justify another dependency/voting stage.
- **Chirality:** historical release constraints included AGPL-3.0-or-later, Python 3.14, and separately downloaded models. Not bundled. https://pypi.org/project/chirality/
- **lumikey Transformer:** licensing was unclear when evaluated. Historical three-score raw agreement was 184/298 versus the then-current 191/298, with repeated-note/chord violations; safety repair reduced it to 175/298. No runtime integration. https://github.com/lumikey/piano-fingering-model
- **AutoFingering:** MIT code does not settle training-data/weight licensing. PIG access and trained parameters are separate dependencies; historical dataset access was restricted to nonprofit academic use. https://github.com/thegreatkwanghyeon/autofingering
- **Ramoneda autoregressive models:** PyTorch and training-layout dependencies lack a stable arbitrary-MusicXML CLI. A historical trial gained only one anchor overall, 171/298 versus 170/298, while one piece regressed. No integration. https://github.com/PRamoneda/Automatic-Piano-Fingering
- **Sheet Music Transformer:** MIT research code with pretrained piano models requires PyTorch/OpenCV/model downloads and emits bekern rather than directly usable MusicXML/page anchors. A separate lossless conversion/audit chain would be needed. https://github.com/antoniorv6/SMT
- **General OCR:** digits alone do not establish notehead ownership.

These historical trials are diagnostic, not current accuracy claims. Retest current sources and versions before relying on them.

## External evaluation resources

Keep all downloaded data outside the distributed skill:

| Resource | Evidence and limits |
| --- | --- |
| ThumbSet: https://zenodo.org/record/6433702 | Partial noisy crowdsourced labels for 2,523 pieces; useful for stress/anchor checks, not expert accuracy proof. |
| PianoVAM: https://github.com/yonghyunk1m/PianoVAM-Code | Performance/video labels under CC BY-NC 4.0; internal research, not MIT package data. |
| https://github.com/PRamoneda/ICASSP22 | Fingers directory includes algorithm outputs; candidate comparisons, not human truth. |

PIG requires registration and its redistribution restrictions must be respected. RoboPianist documents this boundary: https://github.com/google-research/robopianist/blob/main/docs/dataset.md . Do not mirror or bypass registration.

## Reconsideration conditions

Require a declared benchmark with at least three pieces and 100 frozen editorial anchors, a clear gain after ignoring original fingers, no removal of failures, preserved local delivery/geometry/recovery checks, and authorized offline-capable dependencies. Licenses for code, weights, and data must each be appropriate.
