# Output Contracts

## Report contract (Markdown)
- Title
- Context (2-3 lines)
- Key architecture/process points
- Risks / limitations
- Action items

## Quiz contract (JSON/Markdown/HTML)
- Array of 5-10 multiple-choice questions
- Each item:
  - `question`
  - `choices` (>=4)
  - `answer`
  - `explanation`

## Flashcards contract (JSON/Markdown/HTML)
- Array of 8-20 cards
- Each item:
  - `front`
  - `back`
  - `tags` (optional)

## Mind Map contract (JSON)
- Tree structure with:
  - `label`: node text
  - `children`: array of child nodes (recursive)
- Root node represents the main topic
- Max depth: 4 levels

## Slides contract (PDF/PPTX)
- Downloaded file (PDF default, PPTX available via `--format pptx`)
- If generation fails: provide error summary

## Audio contract (MP3)
- If success: provide audio artifact path + duration
- If fail: provide error summary + retry count + fallback decision
- Post-process with `scripts/compress_audio.sh` for Telegram 50MB limit

## Video contract (MP4)
- If success: provide video artifact path
- If fail: provide error summary + retry count + fallback decision
- Check file size — Telegram 50MB limit applies (no compression script)

## Infographic contract (PNG)
- Downloaded PNG file
- Options: orientation (landscape/portrait/square), detail (concise/standard/detailed)
- If generation fails: provide error summary
- Deliver via Telegram as photo for better preview

## Data Table contract (CSV)
- CSV file with UTF-8 BOM (Excel-compatible)
- Structure defined by user description in generate command
- If generation fails: provide error summary

## Delivery status contract

Provide a compact table/list covering all 9 artifact types:
- report: success|fail (+ path)
- quiz: success|fail (+ path)
- flashcards: success|fail (+ path)
- mind-map: success|fail (+ path)
- slide-deck: success|fail (+ path)
- audio: success|fail (+ path or reason)
- video: success|fail (+ path or reason)
- infographic: success|fail (+ path or reason)
- data-table: success|fail (+ path)

Only include entries for artifacts that were requested by the user.
