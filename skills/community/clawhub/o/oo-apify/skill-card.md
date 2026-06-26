## Description: <br>
Apify (apify.com). Use this skill for Apify requests involving searching, reading data, and running supported Apify connector actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Apify actor metadata, authenticated user details, dataset items, actor run status, and to start Apify actor runs through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start Apify actor runs through a connected account, which may incur cost, consume resources, or expose resulting data. <br>
Mitigation: Require explicit approval of the actor, input payload, expected cost or resource impact, and resulting data access before using run_actor. <br>
Risk: The security verdict is suspicious because write-capable behavior is present while safety labeling treats untagged actions as safe reads. <br>
Mitigation: Review the skill before installation and confirm any action that changes Apify state or accesses sensitive account data. <br>


## Reference(s): <br>
- [ClawHub Apify skill page](https://clawhub.ai/oomol/oo-apify) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Apify homepage](https://apify.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
