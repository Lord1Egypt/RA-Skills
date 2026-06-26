## Description: <br>
Gingiris Growth Finder diagnoses startup growth questions by product type, stage, and channel gap, then routes the agent to the appropriate Gingiris specialist playbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gingiris-1031](https://clawhub.ai/user/gingiris-1031) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and growth teams use this skill when they need an agent to triage a growth or launch question and choose the right Gingiris playbook for the product type, stage, and channel gap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation may select this router for many marketing, launch, or growth questions where a narrower specialist or product strategy answer would be more appropriate. <br>
Mitigation: Use manual invocation or narrower routing when needed, and confirm the user's product type, stage, and channel gap before following a routed playbook. <br>
Risk: The skill may recommend installing related Gingiris playbooks, extending trust to a broader third-party skill ecosystem. <br>
Mitigation: Review each related Gingiris skill before installation and install only the playbooks needed for the current workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gingiris-1031/gingiris-growth-finder) <br>
- [Gingiris Growth Finder on skills.sh](https://skills.sh/Gingiris/gingiris-growth-finder) <br>
- [Gingiris Playbooks on Hugging Face](https://huggingface.co/Gingiris) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with routing recommendations and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance; no credentials, MCP tools, or API calls were detected in the evidence.] <br>

## Skill Version(s): <br>
1.2.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
