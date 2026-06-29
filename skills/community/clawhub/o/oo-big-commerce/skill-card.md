## Description: <br>
Operates a BigCommerce catalog through OOMOL's big_commerce connector, supporting product read, create, list, update, and delete workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and commerce operators use this skill to let an agent inspect and manage BigCommerce catalog products through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change BigCommerce catalog product data. <br>
Mitigation: Confirm the exact action, product target, and JSON payload with the user before running create or update actions. <br>
Risk: Delete actions can remove BigCommerce catalog products. <br>
Mitigation: Require explicit approval for the target product ID before running destructive actions. <br>
Risk: One-time CLI installation and account connection steps involve external commands and account authorization. <br>
Mitigation: Run setup only after an auth or connection failure and only from trusted OOMOL sources. <br>


## Reference(s): <br>
- [BigCommerce homepage](https://www.bigcommerce.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-big-commerce) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live BigCommerce product read, write, and delete actions through the oo CLI when the user approves the requested operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
