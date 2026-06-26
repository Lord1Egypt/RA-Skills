## Description: <br>
Web-first skill for working with Proof documents via proofeditor.ai, including collaborative Markdown editing, comments, suggestions, and provenance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dshipper](https://clawhub.ai/user/dshipper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to create or join Proof collaborative Markdown documents, edit content, and add comments or suggestions while preserving authorship and presence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared document content, access tokens, and presence or activity data are sent to proofeditor.ai when the skill is used. <br>
Mitigation: Install only for workflows where this data sharing is acceptable; treat Proof links and tokens as sensitive and prefer bearer or header token use. <br>
Risk: Private drafts may be stored and edited in Proof if the user chooses to use the hosted service. <br>
Mitigation: Avoid using the skill for private drafts unless Proof storage is acceptable; keep repo-tracked Markdown local unless the user asks to move or share it in Proof. <br>


## Reference(s): <br>
- [Proof homepage](https://www.proofeditor.ai) <br>
- [Proof agent documentation](https://www.proofeditor.ai/agent-docs) <br>
- [Proof agent setup](https://www.proofeditor.ai/agent-setup) <br>
- [Proof agent discovery JSON](https://www.proofeditor.ai/.well-known/agent.json) <br>
- [ClawHub skill page](https://clawhub.ai/dshipper/proofeditor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown guidance with curl examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Proof share tokens, agent presence, and by-attribution for document reads and writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
