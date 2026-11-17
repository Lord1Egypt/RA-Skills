# iA Presenter Markdown syntax

Source: the Help bundled inside iA Presenter 2.0.2 (`Help/Markdown.html`), the online
support pages, and live tests. `⇥` below means a **real tab character** at the start of
the line.

## 1. Visible vs. spoken

| Element | Default | To flip it |
|---|---|---|
| Headings `#`…`######` | visible | – (always visible) |
| Paragraph | speaker notes | `⇥paragraph` → visible body text |
| Lists (`-`, `+`, `*`, `1.`, `- [ ]`) | speaker notes | `⇥- item` on every item |
| Blockquote `>` | speaker notes | `⇥> quote` on every line |
| Definition list | speaker notes | `⇥Term` / `⇥: definition` |
| Images / videos / content blocks | visible | – |
| Tables | visible | – (never TAB them) |
| Fenced code ``` | visible | – (never TAB them) |
| Display math `$$…$$` | visible | – |
| Footnotes | visible at slide bottom (if the layout allows) | – |
| `// comment` | author-only (neither slide nor notes) | – |

A TAB paragraph placed **immediately before a heading** (no blank line) renders as a
**kicker** – a small line above the title:

```
⇥Quarterly review
# Numbers that matter
⇥A subtitle line under the title
```

Indented lines that are not TAB-prefixed (4 spaces) are *not* body text. Do not mix.

## 2. Slides

- `---` on its own line = slide break (Format → Slide Break, ⇧⌘-).
- Settings → Editor → "Typing": triple Return can also create a slide (off by default in
  files you generate; just use `---`).
- Blank lines inside a slide separate **cells** (layout units). See `layouts.md`.
- First line of a slide may be `Layout: <Name>` (see `layouts.md`) or `Class: <css-class>`
  (adds a class to that slide for custom-theme CSS).

## 3. Paragraphs and line breaks

Paragraphs are separated by a blank line. Two trailing spaces or a trailing `\` insert a
line break inside a paragraph:

```
⇥Twinkle, Twinkle Little Bat\
⇥How I wonder what you're at!
```

## 4. Headings

```
# Heading 1   – cover title (pair with ### for details)
## Heading 2  – centered section / slide title
### Heading 3 – smaller heading
#### Heading 4 – subheading; combined with an image it becomes a caption
##### / ###### – rarely needed
```

Keyboard: ⌘1–⌘6. Headings are short and always visible; put the explanation in notes.

## 5. Lists

```
⇥- Red        (also + or *)
⇥1. First
⇥- [ ] todo
⇥- [x] done
⇥- Parent
⇥    - nested (4 spaces or a tab after the TAB prefix)
```

Without the TAB prefix the list is speaker notes.

## 6. Emphasis and inline

| Syntax | Result |
|---|---|
| `**bold**` / `__bold__` | bold |
| `*italic*` / `_italic_` | italic |
| `***bold italic***` | bold italic |
| `~~strike~~` | strikethrough |
| `==mark==` | highlight |
| `100m^2`, `y^(a+b)^` | superscript |
| `x~z`, `x~y,z~` | subscript |
| `` `code` `` | inline code |
| `[text](https://…)` | link (also reference style `[text][id]` + `[id]: url`) |

## 7. Blockquotes and definition lists

```
⇥> First level
⇥>
⇥> > Nested

⇥Markdown
⇥: A lightweight markup language.
⇥: Also: a deliberate price reduction.
```

## 8. Footnotes and citations

```
⇥A claim that needs a source[^Inline footnote text].
⇥Another claim[^id].

[^id]: Footnote text.

⇥Attributed statement[p. 23][#Doe:2006].

[#Doe:2006]: John Doe. *Some Big Fancy Book*. Vanity Press, 2006.
```

Footnotes are grouped at the bottom of the slide. `[Not Cited][#key]` includes an uncited
source.

## 9. Code

```
```swift
class Shape {
    var numberOfSides = 0
}
```
```

Fenced blocks only (indented code blocks are not supported). Language name enables
syntax highlighting (highlight.js). Code blocks are visible without a TAB.

## 10. Math (KaTeX)

Inline: `$x+y^2$` or `\(x+y^2\)`. Display: `$$…$$` or `\[…\]`. No space between the
delimiter and the expression. Inside a body paragraph the paragraph still needs its TAB.

## 11. Tables

```
| Name   | Price | Tax |
| :----- | ----: | --: |
| Widget |   10$ |  1$ |
| Gift   |    0$ ||
[Recent transactions]
```

- At least one `|` per line; the header/divider line uses only `| : -` and spaces.
- Alignment: `:--` left, `--:` right, `:-:` center. Cell content must stay on one line.
- The first line and the divider must start at column 0 (no TAB!).
- An extra `|` at the end of a cell merges it with the next one.
- `[Caption]` on the line after the table adds a caption (or `Caption: text` metadata).
- The Inspector has a table generator, and pasted HTML/CSV tables convert to Markdown.
- Any table becomes a chart with `Chart: bar` etc. – see `charts.md`.

## 12. Images and video

Recommended: **content blocks** (a bare path on its own line):

```
/assets/photo.jpg
size: contain
x: left
```

Classic Markdown also works: `![Flowchart](assets/Flowchart.png)` or `<img src="…">`.
For those, omit the leading slash and encode spaces as `%20`. Full details, virtual
folders (`/assets/`, `/Theme/`), remote URLs and every metadata key: `content-blocks.md`.

## 13. Header / footer / logo / slide numbers

Configured per presentation in the **Design** inspector (header & footer text in three
positions, logo, slide number), not in Markdown. Custom themes can hide them per layout
(`.cover-container .header { display: none; }`).

## 14. What the app shows you

- Thumbnails (⇧⌘S / ⌃⌘S depending on version) = rendered slides; hover for speaking time.
- ⌘R presentation preview window; ⌥⌘P play; ⌘D focus mode; ⌥⌘I inspector.
- A slide with notes only and nothing visible triggers a warning (Settings → Presentation).
