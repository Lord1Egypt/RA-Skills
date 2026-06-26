# Supported File Formats

## v0.0.1 - Full Support

| Category | Extensions |
|----------|------------|
| Markdown | .md, .markdown |
| Python | .py |
| JavaScript | .js, .mjs, .cjs |
| TypeScript | .ts, .tsx |
| JSX/React | .jsx |
| Java | .java |
| Go | .go |
| Rust | .rs |
| C | .c, .h |
| C++ | .cpp, .hpp, .cc, .hh |
| Shell | .sh, .bash, .zsh |
| YAML | .yaml, .yml |
| JSON | .json |
| TOML | .toml |
| SQL | .sql |
| Plain Text | .txt |
| CSV | .csv |

## Excluded Paths

Automatically excluded from scanning:
- .git/
- node_modules/
- .obsidian/
- __pycache__/
- .venv/, venv/
- dist/, build/

## Not Supported (v0.0.1)

Planned for future versions:

| Format | Extensions | Planned |
|--------|------------|---------|
| PDF | .pdf | v0.1.0 |
| Word | .docx, .doc | v0.1.0 |
| Excel | .xlsx, .xls | v0.1.0 |
| PowerPoint | .pptx, .ppt | v0.1.0 |
| Keynote | .key | v0.2.0 |
| Audio | .mp3, .wav | TBD |
| Video | .mp4, .mov | TBD |

## File Size Handling

| Size | Handling |
|------|----------|
| < 100 lines | Read entirely |
| 100-500 lines | Read entirely, summarize by sections |
| > 500 lines | Read in chunks |
