# File format, import/export, shortcuts, automation

## The `.iapresenter` bundle

A presentation is a macOS package (a folder that Finder shows as one file; UTI
`net.ia.presenter.package`). Elsewhere it is just a directory.

```
My Talk.iapresenter/
├── text.md          # the Markdown deck (UTF-8)
├── info.json        # metadata; theme & preset selection
├── assets/          # images/videos referenced as /assets/<file>
└── thumb.png        # written by the app on save (first slide) – optional
```

`info.json` fields (verified on 2.0.2):

```json
{
  "type": "net.daringfireball.markdown",
  "creatorIdentifier": "net.ia.presenter",
  "version": 2,
  "transient": false,
  "net.ia.presenter": {
    "template": "san francisco",
    "preset": "Default",
    "localFileIdentifier": "8E86E2F9-…"       ← added by the app; omit when generating
  }
}
```

- `template`: theme `Name` lowercased, spaces kept (`"new york"`, `"san francisco"`).
  Unknown values fall back to the default theme without an error.
- `preset`: preset `Name` inside that theme (`"Default"`; Helvetica has `"Light"`/`"Dark"`).
- Other Design-inspector choices (header/footer text, logo, slide numbers, text size,
  aspect ratio, transitions) are stored by the app in the bundle when you change them in
  the UI; leave them to the app.

Other extensions: `.iaptemplate` (iA Presenter Template – a bundle saved as a template),
plain `.md` / `.txt` (open directly; the app treats the text as a deck), and a zipped
bundle (`net.ia.presenter.package.zip`) when sharing from iOS.

Documents can live anywhere; iCloud copies sit in
`~/Library/Mobile Documents/iCloud~net~ia~presenter/Documents/`.

## Generating a bundle

`scripts/new_deck.py source.md "My Talk.iapresenter" --theme tokyo --assets ./img --open`

- copies `source.md` to `text.md`, writes `info.json`, copies every file referenced as
  `/assets/<name>` from `--assets` dirs (or next to the source) into `assets/`, and lists
  missing ones.
- `--convert-images` rewrites `![alt](path)` into content blocks (`/assets/file` + `title:`).
- `--force` overwrites an existing bundle's `text.md`/`info.json` (assets are merged).

Then `scripts/lint_deck.py "My Talk.iapresenter"`.

## Import

File → Import → Markdown/Text: creates a slide for every `#`/`##` heading, keeps
paragraphs as speaker notes, and copies `![alt](image.png)` images into the bundle
(may ask for file access). Import options are checkboxes in the open panel; keep them on.

## Export (File → Export, or the Share tab of the Inspector)

| Format | Notes |
|---|---|
| PDF | 8 layouts: text and images, side by side, 1 slide/page (bleed / white frame / with notes), 1 per page + notes placeholders, 2 per page, 3 per page + placeholders. Slides only or with notes; orientation & paper size; **compress PDF** option (2.0.2). |
| PPTX (beta) | opens in PowerPoint/Keynote/Google Slides. Keeps text styling, simple lists, plain/image backgrounds, images (png/jpg, partial svg), mp4 video, basic tables, code with highlighting, math. Custom fonts must be installed on the target machine. |
| Images | png/jpeg per slide into a folder, filename prefix; pick an aspect ratio first (Settings → Presentation, e.g. 1:1 for social). |
| HTML | full package (presentation.htm + graphics + theme + engine). Upload preserving the folder; rename `presentation.htm` → `index.html` for GitHub Pages. Interactive & responsive. |
| Markdown | plain `.md` with notes; local images exported into a `media/` folder. |
| Web Sharing | one-click hosted link; only for licenses bought from iA directly (not App Store). |

Aspect ratio: Settings → Presentation → Layout: Responsive (default) or 4:3, 16:9,
9:16, 4:5, 1:1.

## Shortcuts worth knowing

| Action | Keys |
|---|---|
| Slide break | ⇧⌘- |
| Add empty slide (layout picker) | ⌘T |
| Body text (insert TAB) | ⇥ |
| Title / Subtitle / Heading / Subheading | ⌘1 / ⌘2 / ⌘3 / ⌘4 |
| Ordered / unordered / task list | ⇧⌘L / ⌘L / ⌥⌘L |
| Blockquote | ⌘> |
| Bold / Italic / Strikethrough / Highlight | ⌘B / ⌘I / ⌥⌘U / ⇧⌘U |
| Footnote / Link / Comment | ⌃⌘K / ⌘K / ⌘/ |
| Inline code / inline math | ⌥⌘` / ⌃⌘M |
| Focus mode | ⌘D |
| Thumbnails / Inspector | ⇧⌘S (⌃⌘S in older builds) / ⌥⌘I |
| Presentation preview window | ⌘R |
| Play / stop presentation | ⌥⌘P |
| Previous / next / first / last slide (editor) | ⌥⌘↑ / ⌥⌘↓ / ⌥⌘← / ⌥⌘→ |
| Duplicate document | ⇧⌘S |

Presenting: ←/→ change slides, ↑/↓/Space scroll the notes; the timer sits in the
toolbar; the notes cursor changes color (blue → purple → red → orange → gold) as you
progress. 2.0 adds a Command Palette for formatting/export/slide actions.

## Automation notes (macOS)

- Open a deck: `open -a "iA Presenter" "My Talk.iapresenter"`. The app is a standard
  document app; it is **not** AppleScript-scriptable (no sdef) – exports need the UI.
- Preview for self-checking: with the Thumbnails sidebar visible, every slide is
  rendered live in the left column. The sidebar state is stored in the app's prefs
  (`~/Library/Containers/net.ia.presenter/Data/Library/Preferences/net.ia.presenter.plist`):
  `showThumbnails` (bool) and `"NSSplitView Subview Frames Document Split View"`
  (sidebar width / collapsed flag). With the app quit, `defaults write <plist> showThumbnails -bool true`
  and a wider first frame (e.g. `"0, 0, 330, 900, NO, NO"`) make every launch show ~5 rendered
  thumbnails – handy when UI scripting is not permitted. Restore the user's values afterwards. `scripts/preview_deck.sh deck.iapresenter out.png`
  opens the deck and captures the screen (requires Screen Recording permission for your
  terminal; inside sandboxed agents run the capture outside the sandbox).
- The app watches the theme in use and re-renders on file change; edits to `text.md` of
  an *open* bundle from outside are picked up too, but prefer closing the document first
  to avoid "file changed" conflicts.
- Speaking-time estimate = words in notes ÷ speaking rate (default 110 wpm, Settings →
  Presentation). Hover a thumbnail for the per-slide time; the editor shows the total.
