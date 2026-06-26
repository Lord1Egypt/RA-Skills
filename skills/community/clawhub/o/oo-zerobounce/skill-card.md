## Description: <br>
ZeroBounce (zerobounce.net) lets agents read, create, and update ZeroBounce data through the OOMOL oo CLI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to validate email addresses, inspect ZeroBounce account activity and usage, check credit balance, and manage ZeroBounce filter rules through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guidance includes a network-fetched shell installer for the oo CLI. <br>
Mitigation: Install the oo CLI only from a trusted, verified OOMOL source and review the installer before execution. <br>
Risk: The skill can create or update ZeroBounce custom allow/block filter rules. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>


## Reference(s): <br>
- [ZeroBounce homepage](https://www.zerobounce.net) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub ZeroBounce skill page](https://clawhub.ai/oomol/oo-zerobounce) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live oo connector schemas before running actions; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
