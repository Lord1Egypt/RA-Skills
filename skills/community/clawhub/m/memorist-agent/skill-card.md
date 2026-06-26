## Description: <br>
Memorist Agent helps capture parents' and family members' life stories through adaptive interviews via WhatsApp, WeChat relay, or direct conversation, then organizes stories into memoir chapters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YinghaoJia](https://clawhub.ai/user/YinghaoJia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and families use this skill to interview relatives, preserve oral histories, track people and places mentioned in stories, and compile collected fragments into private memoir exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores detailed family histories and relationship data locally. <br>
Mitigation: Use it only with informed consent from each narrator, keep the OpenClaw data directory protected, and delete unused narrator data when it is no longer needed. <br>
Risk: Auto-reply and reminder features can send messages to real contacts through messaging channels. <br>
Mitigation: Use allowlists, verify each phone number or account before enabling auto-reply, and confirm that the narrator agrees to being contacted and recorded. <br>
Risk: The skill may modify messaging configuration and install transcription tooling. <br>
Mitigation: Review proposed configuration and install steps before approval, and enable only the channels and speech tools required for the intended workflow. <br>
Risk: Sensitive stories may be sent through WhatsApp or shared with family reviewers. <br>
Mitigation: Prefer relay mode and local exports for sensitive material, and share exports only after narrator review. <br>
Risk: Broad fetch or web search capabilities are listed even though memoir capture is primarily local. <br>
Mitigation: Remove or avoid unused network capabilities unless they are explicitly required for the deployment. <br>


## Reference(s): <br>
- [Memorist Agent ClawHub Page](https://clawhub.ai/YinghaoJia/memorist-agent) <br>
- [README](README.md) <br>
- [Interview Workflow](references/interview-workflow.md) <br>
- [AI Interview Principles](references/interview-principles.md) <br>
- [Compile, Export & Share](references/compile-export-share.md) <br>
- [Spawn & Despawn](references/spawn-despawn.md) <br>
- [Media Requirements & Voice Note Handling](references/media-and-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational text, Markdown memoir chapters, JSON/TXT/Markdown exports, and inline shell or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores narrator profiles, entities, sessions, fragments, chapters, and exports locally under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
