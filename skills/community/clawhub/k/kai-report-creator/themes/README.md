# Custom Themes

Place folders here to add your own themes to kai-report-creator.

## Directory Structure

```
themes/
  your-theme-name/
    reference.md   ← Style description (AI reads and generates CSS variables)
    theme.css      ← Direct CSS definitions (optional, takes priority over reference.md)
```

Both files are optional and can be used independently or together:

| Case | Behavior |
|------|----------|
| Only `reference.md` | AI reads style description and derives `:root` CSS variables |
| Only `theme.css` | CSS variables used directly, fully predictable output |
| Both present | `theme.css` takes priority; `reference.md` serves as style documentation |

## Usage

```bash
/report --theme your-theme-name "Report topic"
```

Or specify in `.report.md` frontmatter:

```yaml
theme: your-theme-name
```

## reference.md Format

```markdown
# Theme Name — Style Reference

One sentence description. Inspiration / aesthetic / mood.

---

## Colors

​```css
:root {
  --primary:      #...;   /* Main color: headings, links, accents */
  --bg:           #...;   /* Page background */
  --surface:      #...;   /* Card background */
  --text:         #...;   /* Body text */
  --text-muted:   #...;   /* Secondary text */
  --border:       #...;   /* Borders / dividers */
}
​```

## Typography

Font choices. Serif or sans-serif? Geometric or humanist? Google Fonts links.

## Layout

Whitespace style, card border-radius, max-width preferences.

## Best For

Brand reports, research docs, internal newsletters...
```

## theme.css Format

Define `:root` CSS variables to override the base theme defaults.

```css
:root {
  --primary:      #C2410C;
  --primary-light:#FFF7ED;
  --accent:       #EA580C;
  --bg:           #FFFBF7;
  --surface:      #FFFFFF;
  --text:         #1C1917;
  --text-muted:   #78716C;
  --border:       #E7E5E4;
  --font-sans:    'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
  --radius:       6px;
}
```

See `templates/themes/corporate-blue.css` for all available variables.

## Notes

- Directories starting with `_` (e.g. `_example-warm-editorial`) are ignored and won't appear in theme lists
- Theme names support only letters, numbers, and hyphens: `my-brand`, `warm-editorial`
- Custom themes take priority over built-in themes with the same name

## Sharing Themes

Publish your theme folder as a git repo — others clone it into their `themes/` directory:

```bash
git clone https://github.com/yourname/report-theme-mybrand \
  ~/.claude/skills/report-creator/themes/mybrand
```
