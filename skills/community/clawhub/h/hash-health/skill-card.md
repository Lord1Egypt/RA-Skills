## Description: <br>
Hash Health supports personal nutrition tracking, meal logging, medication management, and daily health dashboard workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devak208](https://clawhub.ai/user/devak208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to log meals from text or food images, review nutrition history, manage medication records, and ask nutrition questions through their Hash Health account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send food photos, meal details, medication details, and account requests to the hosted Hash Health service. <br>
Mitigation: Install only if the user trusts Hash Health with this data and has configured HASH_HEALTH_TOKEN through environment settings rather than chat. <br>
Risk: Broad triggers can log or save health and meal data sooner than a user expects. <br>
Mitigation: Use explicit wording for save, log, or track actions, and avoid invoking the skill during casual food or health discussion when data should not be sent or stored. <br>
Risk: Meal and medication deletion actions can remove account records. <br>
Mitigation: Confirm the exact meal or medication record before deletion and look up the record identifier instead of guessing it. <br>


## Reference(s): <br>
- [Hash Health ClawHub page](https://clawhub.ai/devak208/hash-health) <br>
- [Hash Health homepage](https://hash-claude-mcp.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown text with JSON-RPC tool call guidance and nutrition or medication summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HASH_HEALTH_TOKEN and sends requested health, meal, image, and medication data to the user's Hash Health account.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
