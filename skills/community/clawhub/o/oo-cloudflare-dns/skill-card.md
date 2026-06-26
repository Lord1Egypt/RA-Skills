## Description: <br>
Cloudflare DNS lets an agent operate Cloudflare DNS through an OOMOL-connected account using the oo CLI to list, read, create, update, and delete zones and DNS records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Cloudflare accounts, zones, and DNS records, then perform approved DNS record changes through an OOMOL-connected Cloudflare DNS account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect Cloudflare DNS write or delete payloads can disrupt domains and services. <br>
Mitigation: Review the exact target, payload, and expected effect with the user before approving create, update, or delete actions. <br>
Risk: Cloudflare access is mediated through an OOMOL-connected account and oo CLI setup. <br>
Mitigation: Only install the oo CLI or connect the Cloudflare DNS account when the user trusts OOMOL and intends to grant this access. <br>


## Reference(s): <br>
- [Cloudflare DNS homepage](https://www.cloudflare.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector calls and JSON responses that include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.3 (source: artifact metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
