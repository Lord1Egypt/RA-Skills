## Description: <br>
Guide an installing agent through a staged PPT or slide workflow without constraining its implementation choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[textboy](https://clawhub.ai/user/textboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presentation authors, and agents use this skill to turn a topic, source material, existing outline, or partial draft into a staged presentation workflow with clarification, optional fact-finding, outline, planning draft, review gates, and final deck-plan handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation tasks can involve confidential reports, internal URLs, transcripts, or business plans. <br>
Mitigation: Use approved source material, avoid unnecessary sensitive inputs, and review generated briefs or deck plans before sharing them outside the intended audience. <br>
Risk: Fact-dependent decks can contain stale, incomplete, or misleading claims if external research is unavailable or weak. <br>
Mitigation: Require the agent to label source limitations, distinguish confirmed facts from open questions, and use review gates before expanding high-stakes decks. <br>
Risk: Saved markdown deck plans may persist sensitive presentation content in the local workspace. <br>
Mitigation: Choose an appropriate workspace for confidential work and manage generated ./output files according to local data-handling rules. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/textboy/present-workflow) <br>
- [README](README.md) <br>
- [PPT Agent Workflow Method](references/method.md) <br>
- [Agent Integration Guide](references/agent-integration.md) <br>
- [Reusable Prompts](references/prompts.md) <br>
- [Presentation scenario and style gallery](https://next-slide-jet.vercel.app/gallery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown, structured outlines, planning drafts, research briefs, review notes, and optional local markdown deck-plan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the final approved deck plan or delivered output layer to ./output/<name>.md when the environment supports file output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
