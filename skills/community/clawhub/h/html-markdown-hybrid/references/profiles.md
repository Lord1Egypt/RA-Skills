# html-to-markdown skill structure

```
html-to-markdown/
├── SKILL.md
├── package.json
├── scripts/
│   ├── html_to_markdown.mjs
│   └── markdown_to_html.mjs
└── references/
    └── profiles.md
```

## Presets
- `article`: readability-first cleanup for blog/news/article pages
- `docs`: preserve docs structure and markdown-ish content blocks
- `forum`: prefer post/thread content while removing signatures and sidebars
- `custom`: start minimal and override selectors manually

## Capabilities
- HTML file / raw HTML / URL / directory / URL list → Markdown
- Markdown string / file / directory → HTML
- Metadata frontmatter
- Quality report JSON
- Relative URL absolutization via `--base-url`
- Image output style control via `--image-style`
- Themed standalone HTML output (`light`, `github`, `minimal`)

## Guidance
- Use `--engine best` when quality matters more than speed.
- Use `--profile article` for most web pages.
- Use `--profile docs` for docs portals and knowledge bases.
