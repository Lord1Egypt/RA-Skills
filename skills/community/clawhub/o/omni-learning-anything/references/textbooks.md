# 中国大陆中小学教材学习

Use this route when the learner wants material aligned to a specific mainland China primary, junior secondary, or general high school textbook. Keep the current intake, plan approval, and output workflows. Reuse known preferences and ask only questions that change the result.

## Identify the book and learning scope

1. Run `textbooks resolve --query '…'`. Use `textbooks catalog` for subjects in each stage. School years can mean different things in 五四 and 六三 systems. Distinguish edition, upper/lower or full volume, and high school 必修 / 选择性必修 modules. Distinguish 人教 A/B, PEP/精通 and language starting grades when they affect matching.
2. Ask for the most important missing choices together. With a grade alone, ask which subject or whether the learner wants all subjects. For all subjects, show the proposed list and editions, then make a separate textbook archive per confirmed subject or volume. With an unclear edition, ask if alignment to the learner's school matters. If it does, use the learner's cover/copyright page or a current local school adoption list; never ask for a child's name or exact school address. If they have no preference, `--allow-default` may select the applicable 统编版 or recommend 人教版 for grade-three math. State the recommendation in the plan. An older publisher description supports broad adoption of 人教 math, not a current nationwide market-share rank. Keep school-specific choices and uncertain editions explicit.
3. Confirm whether they want a volume, chapter, concept, formula, or identified exercises. Do not ask for a broader scope when the request is already precise. The source inventory pins an upstream snapshot and supports available books by the same workflow. Discuss an inaccessible or mismatched source only when it affects the current request. Use an authorized local copy when needed.

## Acquire, inspect, and bind

The agent runs these commands. The learner can stay in chat.

```sh
python scripts/omni_learning.py textbooks resolve --query '人教版小学三年级上册数学，重点学倍的认识'
python scripts/omni_learning.py --project /actual/archive textbooks acquire --book BOOK_ID
python scripts/omni_learning.py --project /actual/archive textbooks locate --material-id MATERIAL_ID --sha256 PDF_SHA --query '倍的认识'
python scripts/omni_learning.py --project /actual/archive textbooks bind --book BOOK_ID --material-id MATERIAL_ID --sha256 PDF_SHA --pages ACTUAL_PAGES --focus '倍的认识'
python scripts/omni_learning.py --project /actual/archive textbooks figure --book BOOK_ID --sha256 PDF_SHA --page ACTUAL_PAGE --box X0 Y0 X1 Y1 --caption '原图的学习用途'
```

- Install the selected dependencies from `scripts/requirements-textbooks.txt`. `acquire` fetches one pinned book, checks Git blob sizes and hashes, rejoins numbered byte segments, and stores the exact PDF privately in the archive. For a local authorized copy, use `--local-pdf /actual/book.pdf`. If its bytes differ, inspect the title, publisher, copyright page and edition with the learner before setting `--confirm-local-edition`. A confirmed local copy retains its own checksum and has no GitHub source URL. Existing material-mode workflows remain available for a local book outside the index.
- Open the actual cover, copyright page and relevant contents. A filename match is a candidate, especially when the user asks for a new revision, a regional series, or the current school edition. Never label an unverified PDF as the latest edition. Record the checked edition and ISBN when present. Printed and physical PDF page numbers may differ.
- `locate` matches the actual PDF text layer by phrase, including normalized formulas where extractable. Review the proposed pages and the visual formula or diagram. For a chapter use the real contents and boundaries. For a concept or formula bind only the pages actually needed; explain related ideas without expanding to unrelated chapters. If exact matches are unavailable, inspect the relevant pages visually and try a source-backed spelling or formula variant. Do not infer a page from a search snippet.
- When selected pages are scanned or their text is broken, use `textbooks ocr --book BOOK_ID --material-id MATERIAL_ID --sha256 PDF_SHA --pages ACTUAL_PAGES` before initialization. OCR is local and processes up to eight chosen pages at a time, using Swift/Vision on macOS or Tesseract with Simplified Chinese and English language data. It returns a new material ID for the same PDF. Recheck text, equations and punctuation against the actual page before citing. A failed source may require an accessible authorized copy. For longer scans, pass the newest returned material ID into the next OCR batch to retain the previously recognized pages. Exclude intentionally blank and unrelated pages from the binding.
- Copy the binding into staging config, including its strict material selection. Follow [materials](materials.md) for exact citations and [content](content.md) for writing. The approved scope records both the verified PDF identity and the learner's focus. Retargeting an existing course requires review and new approval.

## Teach at the learner's level

| Learner | Explanation and practice |
| --- | --- |
| 小学一至二年级 | Start with something observable. Use short sentences, one action per instruction, and a question the learner can answer by looking or pointing. |
| 小学三至六年级 | Start with a familiar scene and the original picture. Connect it to the new term or symbol. Show the reasoning in short steps and provide an original similar problem and a self-check. |
| 初中 | Explain relations and why a method works. Compare common errors, connect text to diagrams or symbols, and ask for a brief reason in the check. |
| 高中 | Preserve definitions, conditions, derivations and units. Compare methods where relevant and include transfer practice appropriate to the learner's baseline. |

Adapt for each subject and learner. A narrow concept guide can use one worked example and one short check. Keep new examples and exercises visibly distinct from textbook text. If the request concerns a textbook passage, use short attributed evidence and original explanations. The reviewable plan and materials must label the actual book and chapter/page scope.

## Use original textbook pictures

Use only an actual relevant illustration, diagram, graph, or figure from the bound textbook for the teaching figure. Inspect the original page, crop that figure using top-left normalized coordinates, and retain the returned caption/credit and `textbook_ref`. Do not redraw, generate an alternative illustration, remove attribution, or use a decorative thumbnail in its place. The renderer checks book version, selected page, same-page evidence citation, and the exact original crop. If the intended page has no relevant image, offer a relevant original figure within an agreed expanded scope or explain the image constraint. A simple text-only preview may be offered outside the required illustrated delivery.

Keep source PDFs and working extracts in the learner's private archive. A public file host or a free-to-read PDF does not grant public redistribution permission. Shared examples need their own permission or a documented public-domain/compatible open-license source.
