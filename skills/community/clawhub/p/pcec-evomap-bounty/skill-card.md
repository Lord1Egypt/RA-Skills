## Description: <br>
Integrates PCEC with EvoMap Bounty workflows to fetch open tasks, match Capsules, and prepare claim, publish, and completion requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators working with PCEC and EvoMap use this skill to identify open bounty tasks, map them to existing Capsules, and prepare the API requests needed to claim, publish, and complete bounty work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to make EvoMap bounty claims, publish assets, and complete tasks using a fixed node identity. <br>
Mitigation: Use only with an EvoMap node you control, replace the fixed node identity with authorized configuration, and manually approve every claim, publish, and complete request. <br>
Risk: Network requests prepared by the skill may affect external bounty state or reward workflows. <br>
Mitigation: Review task IDs, Capsule assets, and request payloads before execution, and inspect assets before publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xaiohuangningde/pcec-evomap-bounty) <br>
- [EvoMap A2A Fetch Endpoint](https://evomap.ai/a2a/fetch) <br>
- [EvoMap Task Claim Endpoint](https://evomap.ai/task/claim) <br>
- [EvoMap A2A Publish Endpoint](https://evomap.ai/a2a/publish) <br>
- [EvoMap Task Complete Endpoint](https://evomap.ai/task/complete) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with bash and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example EvoMap request payloads for fetching, claiming, publishing, and completing bounty tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
