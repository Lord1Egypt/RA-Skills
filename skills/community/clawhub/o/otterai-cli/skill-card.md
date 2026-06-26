## Description: <br>
Use when the user mentions Otter, Otter.ai, or wants to find, search, download, export, or manage meeting notes, transcripts, recordings, or audio from calls, standups, syncs, or interviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erickhchan](https://clawhub.ai/user/erickhchan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents assist users who manage Otter.ai meeting content by proposing or running otter CLI commands to list, search, retrieve, download, upload, and organize transcripts, recordings, speakers, folders, and groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable access to privacy-sensitive Otter.ai meeting transcripts, recordings, and account content. <br>
Mitigation: Install only when the agent should use the user's Otter.ai account, and confirm before uploads, downloads, trashing, moving, renaming, or speaker-tagging meeting content. <br>
Risk: Persistent username and password environment variables can expose Otter.ai credentials. <br>
Mitigation: Prefer otter login with keychain storage over long-lived OTTERAI_USERNAME and OTTERAI_PASSWORD environment variables. <br>


## Reference(s): <br>
- [Otterai Cli on ClawHub](https://clawhub.ai/erickhchan/otterai-cli) <br>
- [Publisher profile](https://clawhub.ai/user/erickhchan) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown, JSON] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command options and Markdown download guidance for Otter.ai transcript workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
