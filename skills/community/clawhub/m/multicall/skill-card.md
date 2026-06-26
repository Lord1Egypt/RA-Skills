## Description: <br>
Analyze multicall operations. Use when you need to understand multicall mechanisms, evaluate protocol security, or reference on-chain concepts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can invoke this skill for multicall-related command guidance, status checks, entry management, search, export, statistics, and configuration tasks. Reviewers should note the server security summary identifies its actual behavior as a local data-storage utility rather than a blockchain security analyzer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence says the skill is advertised as a blockchain multicall analyzer, but behaves like a local entry manager. <br>
Mitigation: Review it as a local data-storage utility and verify behavior before relying on it for blockchain or protocol security analysis. <br>
Risk: Commands can persist, export, remove, or reconfigure local data, with default storage under ~/.multicall. <br>
Mitigation: Do not store secrets or sensitive prompts in it; set MULTICALL_DIR to a controlled directory and review exported files before sharing. <br>


## Reference(s): <br>
- [Multicall ClawHub skill page](https://clawhub.ai/ckchzh/multicall) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write, copy, delete, export, or mutate local data under ~/.multicall unless MULTICALL_DIR is changed.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
