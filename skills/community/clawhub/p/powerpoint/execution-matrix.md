# Execution Matrix — PowerPoint

Use this matrix before writing automation. Choose the path that matches the app state, not the file format.

## Default Interface by Job

| Job | Preferred path | Why |
|-----|----------------|-----|
| Attach to a live PowerPoint session | `osascript` | Official CLI into PowerPoint's scripting dictionary |
| Read active presentation, slide, or view | `osascript` | Keeps actions bound to live app state |
| Add slide, move slide, or read notes | `osascript` | Operates against the current deck and slide order |
| Start or stop slideshow | `osascript` | Must run inside the live PowerPoint session |
| Export current deck to PDF | `osascript` | Uses PowerPoint's own rendering and export path |
| Offline PPTX generation or structural editing | `powerpoint-pptx` | Better fit than live app control |

## Platform Notes

### macOS

- Start with `osascript` for presentation, slide, notes, export, and slideshow actions.
- Keep scripts short and verify active presentation identity before mutation.

## Attach Strategy

### Choose `attach-existing` when

- the deck is already open
- slideshow or presenter state matters
- the user is actively rehearsing or reviewing the presentation

### Choose `launch-new` when

- isolation matters more than preserving the current UI session
- you need a controlled export pass
- the deck should be opened in a clean app instance

### Choose `save-copy-first` when

- the presentation is business-critical
- slide reordering or deletion could be destructive
- export or cleanup behavior is not yet trusted
