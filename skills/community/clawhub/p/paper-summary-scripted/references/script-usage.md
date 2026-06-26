# Script usage

## Command

```bash
python scripts/process_papers.py   --language "zh-CN"   --paperurls '["https://arxiv.org/abs/1706.03762"]'   --paperfiles '["/absolute/path/to/uploaded-paper.pdf"]'   --output-dir ./runs/paper-summary
```

## Accepted input forms

`--paperurls` accepts arXiv IDs, arXiv abstract URLs, arXiv PDF URLs, and the same list formats below.
`--paperfiles` accepts local paper files in the same list formats below.

- JSON arrays
- newline-separated values
- comma-separated values
- a single raw value

URL inputs are normalized to direct arXiv PDF downloads only.
The script does not parse web pages or use HTML as a paper source.

## Output files

The script writes:

- `manifest.json`: machine-readable per-input status
- `combined_extracted_text.md`: merged text for quick inspection
- `texts/*.txt`: one cleaned text file per successful source
- `downloads/*`: raw downloaded arXiv PDFs for URL inputs

## Manifest fields

Each record contains:

- `index`
- `source_type`
- `source_label`
- `status`
- `error`
- `download_path`
- `extracted_text_path`
- `characters`
- `preview`
- `notes`

## How to use the manifest

1. Ignore failed records for content generation.
2. Read each successful `extracted_text_path` as `cleaned_text`.
3. Generate summary, detailed, and contribution outputs independently from `cleaned_text`.
4. Only after all three are complete, run quality judgment with `cleaned_text + summary + detailed + contribution`.
5. Use `preview` only for quick triage, never as a substitute for the full extracted text.
6. Use `notes` to downgrade confidence when extraction is partial or lossy.
