## Description:

Parse, search, filter, and export Kindle highlights and notes from "My Clippings.txt" through the kindle-clip command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonding](https://clawhub.ai/user/emersonding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI agents, and readers use this skill to locate Kindle highlights, filter them by book, author, keyword, or date, and export selected notes to Markdown for research, summaries, or personal knowledge management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release depends on an external kindle-clip project and release channel that handles private Kindle clippings.

Mitigation: Install from a pinned source build or verified release, and review the external project before allowing it to process private reading data.

Risk: Curl-piped shell installation can execute mutable remote code.

Mitigation: Prefer manual release download, Homebrew installation, or source builds over curl-piped installers.

Risk: Exported notes may contain private reading data and can be sent to services such as Telegram in chained workflows.

Mitigation: Review exported Markdown before saving it in shared locations or sending it to third-party services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emersonding/skills/kindle-clip-cli)
- [Publisher profile](https://clawhub.ai/user/emersonding)
- [Kindle Clip Processor repository](https://github.com/emersonding/kindle-clip-processor)
- [Kindle Clip Processor releases](https://github.com/emersonding/kindle-clip-processor/releases)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)
- [EXAMPLES.md](artifact/EXAMPLES.md)
- [RECIPES.md](artifact/RECIPES.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and optional exported Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read a configured Kindle clippings path from an explicit argument, KINDLE_CLIP_PATH, or ~/.config/kindle-clip/config.json.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
