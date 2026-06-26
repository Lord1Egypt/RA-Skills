## Description: <br>
Headout helps agents search and read Headout bookings, products, cities, categories, inventory, variants, and pricing through OOMOL's oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Headout booking, product, city, category, inventory, variant, and pricing data from a connected Headout account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on OOMOL's oo CLI and connected Headout credentials. <br>
Mitigation: Install only if you trust OOMOL's oo CLI, and review the OOMOL and Headout connection setup before use. <br>
Risk: Future write or destructive Headout connector actions could change account state. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before running any action marked write or destructive. <br>


## Reference(s): <br>
- [Headout homepage](https://www.headout.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash command snippets and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OOMOL-connected Headout account and live schema inspection before constructing connector payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
