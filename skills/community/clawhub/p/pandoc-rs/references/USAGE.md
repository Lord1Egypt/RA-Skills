# Pandoc Rs Usage Guide

A WebAssembly-based document converter that runs via `openclaw-wasm-sandbox` plugin.

## ⚠️ Important: Required --work-dir Parameter

**Always specify `--work-dir <directory>`** when using `wasm-sandbox-run` with pandoc-component.wasm. This parameter grants the sandbox access to the host filesystem.

**`<directory>`** should be the directory containing the input files (or current working directory).

```bash
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /path/to/working/directory -- \
  <command> [args...]
```

Without `--work-dir`, file operations will fail with "No such file or directory" errors.

## WASM File

**Download URL:** `https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/pandoc-rs/files/pandoc-component.wasm`

**Local cached path:** `~/.openclaw/wasm/pandoc-component.wasm`

**Download command:**
```bash
openclaw wasm-sandbox download \
  "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/pandoc-rs/files/pandoc-component.wasm" \
  ~/.openclaw/wasm/pandoc-component.wasm
```

## Tool: wasm-sandbox-run

**Required command structure:**

```bash
openclaw wasm-sandbox run <wasm-file> \
  --work-dir <directory> -- \
  <command> [args...]
```

### Required Options

| Option | Required | Description |
|--------|----------|-------------|
| `--work-dir <dir>` | **Yes** | Directory containing input files (e.g., `/tmp`, `/home/user/docs`) |

## Available Commands

### stats - Document Statistics

Analyze document word count, characters, paragraphs, and reading time.

```bash
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /path/to/docs -- \
  stats --input document.md -f markdown
```

**Options:**
- `-i, --input <INPUT>` - Input file
- `-f, --from <FROM>` - Input format (default: markdown)
- `-v, --verbose` - Show detailed analysis

### validate - Document Validation

Validate document structure.

```bash
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /path/to/docs -- \
  validate --input document.md -f markdown
```

**Options:**
- `-i, --input <INPUT>` - Input file
- `-f, --from <FROM>` - Input format (default: markdown)

### plugins - List Available Plugins

Show available conversion plugins.

```bash
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /path/to/docs -- \
  plugins
```

**Available Plugins:**
- `toc-generator` - Generate table of contents
- `line-numbers` - Add line numbers to code blocks
- `lazy-load-images` - Enable lazy loading for images

### convert - Document Conversion

Convert documents between formats.

```bash
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /path/to/docs -- \
  convert input.md output.html \
  --input-format markdown \
  --output-format html
```

**Arguments:**
- `<INPUT>` - Input file path
- `<OUTPUT>` - Output file path

**Options:**
- `--input-format <FORMAT>` - Input format
- `--output-format <FORMAT>` - Output format
- `--highlight <true|false>` - Enable syntax highlighting
- `--toc <true|false>` - Generate table of contents
- `--line-numbers <true|false>` - Add line numbers to code blocks
- `--lazy-load <true|false>` - Enable lazy loading for images
- `--lang <LANG>` - Language/locale (default: en)

### Supported Formats

- `markdown` - Markdown format
- `html` - HTML format
- `latex` - LaTeX format
- `docx` - Word document (input only)

## Usage Examples

### Example 1: Analyze a Markdown Document

```bash
# Create test file
echo '# Hello World\n\nThis is **bold** text.' > /tmp/test.md

# Analyze document (note: --work-dir /tmp grants access to /tmp)
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /tmp -- \
  stats --input test.md -f markdown
```

Output:
```
Analyzing document: test.md

=== Document Statistics ===
Words: 8
Characters: 40
Paragraphs: 1
Reading time: ~1 minutes
```

### Example 2: Validate a Document

```bash
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /tmp -- \
  validate --input test.md -f markdown
```

Output:
```
Validating document: test.md
✓ Document is valid!
```

### Example 3: Convert Markdown to HTML

```bash
openclaw wasm-sandbox run ~/.openclaw/wasm/pandoc-component.wasm \
  --work-dir /tmp -- \
  convert test.md output.html \
  --input-format markdown \
  --output-format html
```

## Common Errors

### "No such file or directory"

**Cause:** Missing `--work-dir` parameter or incorrect directory path.

**Solution:** Always specify `--work-dir <directory>` pointing to where your input files are located.

### "File not found"

**Cause:** Input file is outside the directory granted by `--work-dir`.

**Solution:** Ensure the input file is within the `--work-dir` directory, or use a parent directory.

## Limitations

- **Docx output:** Converting to Docx format is not fully supported in the sandbox environment.
- **Supported operations:** For reliable results, use `stats`, `validate`, and `plugins` commands.
