## Description: <br>
Search GIF providers with CLI/TUI, download results, and extract stills/sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content-focused agents use this skill to search Tenor or Giphy, preview GIF results, download selected files, and extract still images or frame sheets for review, documentation, pull requests, or chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation depends on a Homebrew tap or a Go module using @latest. <br>
Mitigation: Verify trust in the Homebrew tap or Go module source before installing and pin versions where local policy requires reproducibility. <br>
Risk: Provider API keys may be used for Giphy or Tenor requests. <br>
Mitigation: Provide only the required API keys, keep them out of shared logs and prompts, and follow local secret-handling policy. <br>
Risk: Download commands can create files in the user's Downloads folder. <br>
Mitigation: Review selected GIFs before download and use explicit output paths when the destination matters. <br>


## Reference(s): <br>
- [Gifgrep homepage](https://gifgrep.com) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/gifgrep) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded GIF files, still PNG images, sprite sheets, pipe-friendly URLs, or JSON result arrays depending on gifgrep flags.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
