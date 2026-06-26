## Description: <br>
Parse, search, filter, and export Kindle highlights and notes from My Clippings.txt through the kindle-clip command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonding](https://clawhub.ai/user/emersonding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and AI agents use this skill to locate, filter, and export Kindle highlights into Markdown for reading review, book summaries, and knowledge management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save or share private Kindle highlights and notes through exported files or downstream messaging workflows. <br>
Mitigation: Use exports only when intentionally saving results, write them to private locations, avoid synced or shared folders unless desired, and review or redact notes before sending summaries to external services. <br>
Risk: The artifact documents a piped shell installer pattern for installing the CLI. <br>
Mitigation: Prefer Homebrew, manual release downloads, or building from source; inspect installation scripts before execution when a shell installer is used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emersonding/kindle-clip-cli) <br>
- [kindle-clip releases](https://github.com/emersonding/kindle-clip-processor/releases) <br>
- [kindle-clip install script](https://raw.githubusercontent.com/emersonding/kindle-clip-processor/master/scripts/install-kindle-clip.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and exported Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local Kindle clippings, save a default path in user config, and export selected notes to files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
