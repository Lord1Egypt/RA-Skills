## Description: <br>
Generates editable ProcessOn diagrams from natural-language requests, including flowcharts, architecture diagrams, ER diagrams, org charts, timelines, roadmaps, infographics, and sketch redraws. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leilizhang](https://clawhub.ai/user/leilizhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and teams can use this skill to turn diagram requests or code context into ProcessOn-hosted diagrams with preview and online editing links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and diagram content are sent to ProcessOn's cloud diagram service. <br>
Mitigation: Use the skill only for content appropriate for ProcessOn processing and avoid submitting confidential or regulated material unless the deployment has approved that data flow. <br>
Risk: Browser authorization and persistent token storage can leave access available after the task is complete. <br>
Mitigation: Review the requested authorization, revoke access when no longer needed, and delete the cached token after use on shared or sensitive machines. <br>
Risk: The setup flow may install or invoke npm tooling such as mcporter globally. <br>
Mitigation: Preinstall and verify the required tooling from trusted sources, or review the install path before enabling the skill in managed environments. <br>
Risk: The artifact behavior strongly steers agents toward broad use and in-band update prompts. <br>
Mitigation: Review skill behavior before deployment and constrain when the skill may be invoked if the environment requires narrower tool use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leilizhang/skills/processon-diagramgen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with authorization guidance, command invocations, and ProcessOn preview and edit links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser authorization and ProcessOn cloud diagram generation; generated diagrams are returned as hosted preview and editing links.] <br>

## Skill Version(s): <br>
2.5.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
