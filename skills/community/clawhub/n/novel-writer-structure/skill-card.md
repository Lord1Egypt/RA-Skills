## Description: <br>
A Chinese-oriented structured novel-writing workflow that guides an agent through prewriting analysis, drafting, self-checks, prose polishing, revision, and metadata updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxiao00j](https://clawhub.ai/user/wuxiao00j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and writing agents use this skill to draft novel chapters from an existing outline while maintaining timeline, character state, foreshadowing, and continuity notes. It is intended for projects that need a repeatable chapter workflow with explicit self-checks and prose refinement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may use stale or overly broad outline and state-tracking context, causing continuity errors or unintended project bleed-through. <br>
Mitigation: Keep outline, timeline, character, foreshadowing, and state-tracking files limited to the active writing project and update them between chapters. <br>
Risk: Generated fiction may still miss the author's intended voice, characterization, or pacing despite the workflow checks. <br>
Mitigation: Review chapter drafts and checklist results before accepting them, with particular attention to dialogue voice, character actions, and scene transitions. <br>


## Reference(s): <br>
- [State Tracking Template](references/state-tracking-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML-style update blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces writing strategy, chapter draft text, checklist results, prose revision guidance, and state-tracking updates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
