## Description: <br>
StackAI helps agents use StackAI through the OOMOL oo CLI to inspect connector schemas, run deployed flows, and retrieve run metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to access a connected StackAI account through OOMOL, run deployed StackAI flows, and fetch run metadata without handling raw API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path includes a visible CLI installer risk from running remote install scripts. <br>
Mitigation: Install only if OOMOL is trusted, and review the oo CLI install guide or installer script before running the curl-to-bash or PowerShell setup. <br>
Risk: The run_flow action executes a deployed StackAI flow rather than performing a read-only lookup. <br>
Mitigation: Inspect the live connector schema, construct the payload from that schema, and confirm the intended flow inputs and effects before execution. <br>
Risk: The skill requires a connected StackAI account and sensitive credentials managed through OOMOL. <br>
Mitigation: Use the OOMOL connection flow rather than raw tokens, and install the skill only when connecting that StackAI account through OOMOL is intended. <br>


## Reference(s): <br>
- [ClawHub StackAI skill page](https://clawhub.ai/oomol/oo-stack-ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [StackAI homepage](https://www.stack-ai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; action results are returned as normalized JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
