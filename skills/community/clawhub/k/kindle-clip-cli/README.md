# kindle-clip OpenClaw Skill

This is an OpenClaw skill bundle for the `kindle-clip` CLI tool, which helps AI agents parse, search, and export Kindle highlights and notes.

## What's included

- **SKILL.md** - The main skill definition file that AI agents read to understand how to use kindle-clip
- This README - Documentation for humans installing or maintaining this skill

## For Skill Users

If you're using an AI agent with OpenClaw and want to enable Kindle highlights processing:

1. Install this skill in your OpenClaw skills directory
2. Install the `kindle-clip` binary following the instructions in SKILL.md
3. The AI agent will now be able to help you search, filter, and export your Kindle highlights

## For AI Agents

Read SKILL.md for complete usage instructions. Quick reference:

```bash
# List books
kindle-clip list --author "author name"

# Print highlights from a book
kindle-clip print --book "book title" --export-md ./output.md

# Search across all notes
kindle-clip search "keyword" --from 2024-01-01 --export-md ./results.md
```

## Installation

The skill requires the `kindle-clip` binary to be installed and available in PATH. See SKILL.md for installation instructions.

## Use Cases

- **Research Assistant**: Search across all Kindle highlights for specific topics
- **Book Summarization**: Export all notes from a specific book
- **Reading Analytics**: Track reading habits by date, author, or book
- **Knowledge Management**: Export highlights to Markdown for integration with note-taking tools

## Platform Support

The `kindle-clip` binary works on:
- macOS (Intel and Apple Silicon)
- Linux (amd64 and arm64)
- Windows (amd64 and arm64)

## Source Repository

This skill is part of the kindle-clip-processor project:
https://github.com/emersonding/kindle-clip-processor

## Contributing

To improve this skill:

1. Fork the repository
2. Make changes to the skill files in `openclaw-skill/`
3. Test with an AI agent
4. Submit a pull request

## License

See the main repository for license information.
