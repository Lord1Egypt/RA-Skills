## Description:

Search GIF providers with CLI/TUI, download results, and extract stills/sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent for gifgrep CLI workflows that search GIF providers, preview results, download GIFs, and extract still images or sprite sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external gifgrep CLI installed from a Homebrew tap or Go module.

Mitigation: Install only after deciding that the upstream tap or Go module is acceptable for the environment.

Risk: Commands using --download or --reveal can create files in ~/Downloads or open Finder.

Mitigation: Use those options only when local file creation or Finder reveal behavior is intended.

Risk: Provider API keys may be supplied through GIPHY_API_KEY or TENOR_API_KEY.

Mitigation: Provide only the provider credentials needed for the selected GIF source.

## Reference(s):

- [Gifgrep homepage](https://gifgrep.com)
- [ClawHub Gifgrep release](https://clawhub.ai/utromaya-code/skills/gif-search-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that download GIFs to ~/Downloads, reveal files in Finder, or configure provider API keys.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
