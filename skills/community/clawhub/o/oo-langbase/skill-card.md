## Description: <br>
Operate Langbase through an OOMOL-connected account with schema-first oo CLI connector commands for memory actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Langbase memories through an OOMOL-connected oo CLI account, including schema inspection and create, list, retrieve, and delete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Langbase account through OOMOL using sensitive credentials managed outside the prompt. <br>
Mitigation: Install it only for the intended Langbase account, verify the oo CLI before use, and confirm the active OOMOL connection before running account operations. <br>
Risk: Write and destructive connector actions can create or delete Langbase memories. <br>
Mitigation: Require explicit user confirmation of the exact action, target, payload, and expected effect before running write or destructive actions. <br>


## Reference(s): <br>
- [Langbase homepage](https://langbase.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may execute Langbase connector actions through the user's OOMOL-connected account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
