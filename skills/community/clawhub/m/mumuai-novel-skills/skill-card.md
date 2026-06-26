## Description: <br>
A MuMu novel-management skill that helps an agent bind or create a single novel project, generate and materialize outlines, trigger chapter batches, audit chapters with RAG, and approve or rewrite published content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crypto-2042](https://clawhub.ai/user/crypto-2042) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and writing teams use this skill to operate a MuMu-backed fiction workflow for one bound novel project, including initialization, outline expansion, batch chapter generation, RAG-based review, foreshadow tracking, and chapter approval or rewrite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authenticate to MuMu and publish, approve, or overwrite chapters when review commands are run. <br>
Mitigation: Use a limited-purpose MuMu account and double-check project_id and chapter_id before approving or rewriting content. <br>
Risk: MuMu credentials or a session file can expose access to the configured MuMu server. <br>
Mitigation: Set MUMU_API_URL, MUMU_USERNAME, and MUMU_PASSWORD explicitly, protect any session file, and leave MUMU_SESSION_FILE unset unless the file can be secured. <br>
Risk: The workflow depends on the configured MuMu server for project state and generated content. <br>
Mitigation: Install and run the skill only when the target MuMu server and endpoint are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/crypto-2042/mumuai-novel-skills) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/crypto-2042) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some helper scripts can emit JSON; review and rewrite actions can update a MuMu project.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
