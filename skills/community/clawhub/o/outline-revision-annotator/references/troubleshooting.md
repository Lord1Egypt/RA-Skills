# Troubleshooting

## Chinese text turns into `????`

Likely causes:

- Windows PowerShell piped inline Chinese source into `python -`
- the PDF viewer cannot render popup comment text correctly
- the script could not find a usable CJK font

Fix:

- run a real UTF-8 `.py` file instead of inline piped source
- use visible margin note boxes instead of popup comments
- rerun after ensuring the system has a Chinese-capable font

## The PDF note is clickable but not visible

You are probably using PDF popup comments or sticky notes.

Fix:

- render visible boxes into the page margin instead
- keep the explanation text inside the page content, not inside a popup annotation

## The yellow boxes overlap each other

Fix:

- merge nearby paragraphs into one manifest item
- shorten `box_text`
- reduce over-marking; only structural changes should remain

## The wrong text is highlighted

Fix:

- re-check `new_pdf_blocks.json`
- adjust the `blocks` list to cover the correct union of PDF text blocks
- remember that `blocks` are zero-based indexes

## The DOCX report opens but formatting looks plain

The bundled converter is intentionally simple and reliable.

Fix:

- keep markdown structure clean: headings, flat bullets, simple tables
- avoid nested markdown constructs if you want the DOCX export to stay predictable

## Chinese filename issues

Some viewers, browser tabs, or uploaders handle Chinese filenames poorly.

Fix:

- keep the real Chinese filename if the environment supports it
- otherwise also provide an ASCII alias for transport or publishing
