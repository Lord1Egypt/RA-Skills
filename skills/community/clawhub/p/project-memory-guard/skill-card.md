## Description: <br>
Enforce project boundaries and memory writeback rules before anything enters project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams that maintain project memory use this skill to validate proposed memory writes, reject incomplete records, and reroute ambiguous content for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project memory records may retain raw content that includes private or unnecessary details. <br>
Mitigation: Review, redact, and delete sensitive raw content according to the project's memory retention practices before relying on stored records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunbinnju-star/project-memory-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Structured validation decision with normalized record fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes accept, reject, or reroute decisions with destination, contamination risk, missing fields, and reason.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
