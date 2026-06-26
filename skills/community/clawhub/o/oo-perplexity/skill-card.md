## Description: <br>
Operate Perplexity through an OOMOL-connected account using the oo CLI for search, model listing, chat completions, and embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to interact with Perplexity through OOMOL-managed credentials. It supports web search, available model discovery, Sonar chat completions, and embedding generation after inspecting each live action schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL account and may operate on service data through server-side credentials. <br>
Mitigation: Install only when comfortable connecting the service through OOMOL, and confirm payloads before actions marked as write or destructive. <br>
Risk: The documented first-time setup includes remote installer commands for the oo CLI. <br>
Mitigation: Review the oo CLI install guide or installer before running remote install commands. <br>


## Reference(s): <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Perplexity](https://www.perplexity.ai) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
