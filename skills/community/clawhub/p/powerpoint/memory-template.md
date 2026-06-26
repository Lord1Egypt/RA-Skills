# Memory Template — PowerPoint

Create `~/powerpoint/memory.md` with this structure:

```markdown
# PowerPoint Memory

## Status
status: active
version: 1.0.0
last_verified: YYYY-MM-DD
platform: macOS
control_path: osascript
ppt_attach_mode: attach-existing | launch-new | mixed

## Safety Defaults
- Delete slide: ask every time
- Close without save: blocked unless user confirms
- Overwrite exports: ask every time
- Risky cleanup: prefer Save As or deck copy first

## Environment Notes
- PowerPoint version:
- Default control shell:
- Typical deck locations:
- Preferred export folder:
- Known slideshow policy:

## Deck Notes
- Store only presentation identifiers, stable paths, and non-sensitive structure notes
- Never paste slide contents, secrets, or personal information here

## Recent Incidents
- YYYY-MM-DD: short failure signature -> short fix
```

## Storage Rules

- Keep only reusable environment facts and safety preferences.
- Do not store slide body content unless the user explicitly asks for a local note.
- Put repeatable failures in `~/powerpoint/incidents.md`.
- Put non-sensitive recurring deck metadata in `~/powerpoint/deck-notes.md`.

## Optional Companion Files

`~/powerpoint/incidents.md`:

```markdown
# PowerPoint Incidents

## YYYY-MM-DD
- Symptom:
- Presentation:
- Cause:
- Fix:
```

`~/powerpoint/deck-notes.md`:

```markdown
# Deck Notes

## Presentation: /absolute/path/to/file.pptx
- Default view:
- Common export target:
- Known quirks:
- Slideshow notes:
```
