## Description: <br>
Uses the OOMOL oo CLI to search, retrieve metadata for, and verify Addressfinder addresses in Australia and New Zealand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run Addressfinder autocomplete, address metadata retrieval, and address verification through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose commands that authenticate to services or use an OOMOL-connected Addressfinder account. <br>
Mitigation: Review proposed oo commands before execution and run setup or authentication steps only after a relevant failure or explicit user approval. <br>
Risk: Address verification requests may send address data to the connected Addressfinder service. <br>
Mitigation: Confirm that the address data is appropriate to submit through the connected account before running verification actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-addressfinder) <br>
- [Addressfinder Homepage](https://addressfinder.com/au) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the oo CLI and should inspect the live connector schema before sending an action payload.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
