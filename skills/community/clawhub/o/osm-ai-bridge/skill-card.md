## Description: <br>
OSM AI Bridge connects an agent to Doubao or Gemini through a browser session over Chrome DevTools Protocol for ask, discuss, and verify workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanara-osm](https://clawhub.ai/user/yanara-osm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route questions and discussion prompts to Doubao or Gemini through a browser login, then use the returned AI text in local workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a browser session that may already be logged in. <br>
Mitigation: Use a dedicated browser profile and separate AI accounts instead of connecting it to a normal logged-in browser. <br>
Risk: The skill can inspect browser storage such as cookies and local storage. <br>
Mitigation: Install only if this access is acceptable, and review or delete ~/.openclaw/ai_bridge if you stop using the skill. <br>
Risk: Prompts or page content sent through connected AI services may expose sensitive information. <br>
Mitigation: Do not submit secrets, regulated data, or other sensitive content through the automated browser session. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yanara-osm/osm-ai-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a logged-in browser session and a Chrome DevTools Protocol debugging port.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
