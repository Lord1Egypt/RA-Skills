# Kindle-Clip-CLI

Parse, print, search, filter and export Kindle highlights and notes from the command line.

## What this skill does

This skill provides the `kindle-clip` CLI tool for processing Kindle's "My Clippings.txt" file. It's designed to be AI agent-friendly, with clean Markdown output and intuitive filtering options.

**Key capabilities:**
- Parse and list all books from Kindle clippings
- Print highlights and notes for specific books or all books
- Search across all notes by keyword, date range, author, or book title
- Export results to Markdown files
- Filter by date ranges, book titles, authors, or keywords

## Installation

### Recommended: Manual Install (macOS/Linux)

1. Download the latest binary for your platform from [GitHub Releases](https://github.com/emersonding/kindle-clip-processor/releases).
2. Make it executable: `chmod +x kindle-clip`
3. Move `kindle-clip` to a directory in your PATH (e.g., `~/bin` or `/usr/local/bin`):
   ```bash
   mv kindle-clip /usr/local/bin/kindle-clip
   ```

### Build from Source

```bash
git clone https://github.com/emersonding/kindle-clip-processor.git
cd kindle-clip-processor
go build -o ./bin/kindle-clip ./cmd/kindle-clip
# Move ./bin/kindle-clip to your PATH
```

## Commands

### Set default path

Save the path to your Kindle clippings (usually found in `~/Documents/Kindle/`):

```bash
kindle-clip set ~/Documents/Kindle/My\ Clippings.txt
```

This saves the path to `~/.config/kindle-clip/config.json`. Useful for repeated operations without specifying the path each time.


### List books

List all books with highlights:

```bash
# Using saved path
kindle-clip list

# Using explicit path
kindle-clip list ~/Documents/Kindle

# Filter by author
kindle-clip list --author "Yuval Noah Harari"

# Verbose mode (includes clip counts and date ranges)
kindle-clip list --verbose

# Export to file
kindle-clip list --export-md ./books.md
```

### Print highlights

Print all highlights and notes:

```bash
# Print all highlights from all books
kindle-clip print

# Print highlights for a specific book
kindle-clip print --book "Sapiens"

# Filter by date range
kindle-clip print --from 2024-01-01 --to 2024-12-31

# Combine filters
kindle-clip print --book "Thinking, Fast and Slow" --from 2024-01-01

# Export to Markdown file
kindle-clip print --book "Sapiens" --export-md ./sapiens-notes.md

# Verbose mode (includes Kindle metadata)
kindle-clip print --verbose
```

### Search notes

Search for specific keywords across all notes:

```bash
# Search for a keyword
kindle-clip search confidence

# Search with filters
kindle-clip search bias --author "Daniel Kahneman"

# Search and export results
kindle-clip search metacognition --export-md ./metacognition-notes.md

# Search with date range
kindle-clip search "system 1" --from 2024-01-01
```

## Common Options

All `list`, `print`, and `search` commands support:

- `--from YYYY-MM-DD` - Include notes created on/after this date
- `--to YYYY-MM-DD` - Include notes created on/before this date
- `--book TEXT` - Include only notes whose book title matches TEXT (case-insensitive)
- `--author TEXT` - Include only notes whose author matches TEXT (case-insensitive)
- `--query TEXT` - Include matching note text (used in search command)
- `--export-md PATH` - Save Markdown output to a file
- `--verbose` - Include Kindle metadata in output

## Output Format

### Book List

Compact by default:
```markdown
# Books

- **Sapiens (Yuval Noah Harari)**
- **Thinking, Fast and Slow (Daniel Kahneman)**
```

Verbose mode adds clip counts and date ranges:
```markdown
# Books

- **Sapiens (Yuval Noah Harari)**
  - clips: 42
  - first: 2024-01-15T10:30:00Z
  - last: 2024-02-20T14:22:00Z
```

### Highlights and Notes

Organized by book with Markdown formatting:

```markdown
# Sapiens (Yuval Noah Harari)

> Culture tends to argue that it forbids only that which is unnatural. But from a biological perspective, nothing is unnatural. Whatever is possible is by definition also natural.

> **Note**: This connects to the social construction argument in sociology.

# Thinking, Fast and Slow (Daniel Kahneman)

> The confidence that individuals have in their beliefs depends mostly on the quality of the story they can tell about what they see, even if they see little.
```

Notes are prefixed with `> **Note**:` while highlights use plain `>` blockquotes.

## Path Resolution

`kindle-clip` resolves the clippings file path in this order:

1. Explicit file or directory argument
2. `KINDLE_CLIP_PATH` environment variable
3. Saved config in `~/.config/kindle-clip/config.json`

If you provide a directory instead of a file, it looks for:
- `<dir>/documents/My Clippings.txt` (Kindle's typical location)
- `<dir>/My Clippings.txt` (fallback)

## Use Cases for AI Agents

### Research Assistant

When a user asks "What did I highlight about cognitive biases?":

```bash
kindle-clip search "cognitive bias" --export-md ./cognitive-bias-notes.md
```

### Book Summary

When a user asks "Show me my notes from Sapiens":

```bash
kindle-clip print --book "Sapiens" --export-md ./sapiens-summary.md
```

### Reading Timeline

When a user asks "What books did I read in 2024?":

```bash
kindle-clip list --from 2024-01-01 --to 2024-12-31 --verbose
```

### Cross-Book Research

When a user asks "Find all my notes about decision-making":

```bash
kindle-clip search "decision making" --export-md ./decision-making-research.md
```

## Tips for AI Agents

1. **Always use `--export-md`** when the user might want to save or review results later
2. **Use `--verbose`** when users need full context or metadata
3. **Combine filters** for precise results (e.g., `--book "Sapiens" --from 2024-01-01`)
4. **Case-insensitive matching** - filters are case-insensitive, so "sapiens" matches "Sapiens"
5. **Partial matches work** - `--book "Think"` will match "Thinking, Fast and Slow"
6. **Set the path once** - Use `kindle-clip set` at the start of a session for cleaner commands

## Error Handling

If `kindle-clip` is not installed, guide the user to install it using the installation instructions above.

If no path is configured, prompt the user to either:
1. Run `kindle-clip set <path>` to save a default path
2. Provide a path explicitly in each command
3. Set the `KINDLE_CLIP_PATH` environment variable

## Dependencies

- Go binary (no runtime dependencies once built)
- Works on macOS, Linux, and Windows (amd64 and arm64)

## Repository

Source code and releases: https://github.com/emersonding/kindle-clip-processor

## License

See the main repository for license information.
