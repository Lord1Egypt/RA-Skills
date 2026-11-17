# Manual Anki text import

The official text-file guide is https://docs.ankiweb.net/manual/importing/text-files (checked 2026-10-22).

The export is UTF-8 with tab-separated, double-quoted Front/Back fields. Headers declare the separator, columns and `html:false`. Use Anki's manual Import command, select a Basic note type and a destination deck, map Front/Back, and inspect the preview before confirming. Back contains the answer plus its original source ID and evidence quote. No audio, images, cloze templates, AnkiConnect or account synchronization is used.

To prevent accidental spreadsheet formula execution, a field beginning with whitespace/control characters followed by `=`, `+`, `-` or `@` is prefixed with a literal apostrophe. This can appear on the card and can be edited manually after review. Do not remove it merely to open the TSV in a spreadsheet.

The script validates file structure and evidence, not your Anki version, GUI import, scheduling algorithm or the truth of an answer. If the preview is wrong, stop and correct field mapping before import. The local Markdown review checklist operates independently of Anki.
