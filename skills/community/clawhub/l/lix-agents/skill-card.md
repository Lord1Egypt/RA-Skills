## Description: <br>
Obtain temporary Lix API tokens via CLI with human email approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aakarim](https://clawhub.ai/user/aakarim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to obtain temporary Lix API credentials with user approval, then authenticate calls to Lix services for data enrichment and related API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary API tokens can be exposed through logs, chat transcripts, or command output if handled carelessly. <br>
Mitigation: Treat generated tokens as sensitive, avoid logging or pasting them into shared contexts, and store them only for the intended API workflow. <br>
Risk: Installing or running an unexpected lix-agents CLI build could grant credentials to an untrusted tool. <br>
Mitigation: Verify the lix-agents CLI source and release channel before installation, and approve only token requests the user intentionally initiated. <br>


## Reference(s): <br>
- [Lix API docs](https://lix-it.com/docs) <br>
- [lix-agents GitHub Releases](https://github.com/lix-it/lix-agents/releases) <br>
- [ClawHub Lix Agents listing](https://clawhub.ai/aakarim/lix-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and HTTP header configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary bearer-token usage guidance; tokens should be treated as sensitive credentials.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
