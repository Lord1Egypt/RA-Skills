## Description: <br>
Personal Wiki helps an agent ingest IMA notes, Evernote notes, and local files into a structured local Markdown wiki, then query, lint, and generate demo scripts from that wiki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to maintain a local Markdown knowledge base from private note sources and user-provided files, then retrieve, clean up, or repurpose that knowledge for responses and demo scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private IMA or Evernote notes and local files placed in the wiki raw folder. <br>
Mitigation: Install only for workflows where that access is intended, keep credentials private, and avoid ingesting secrets that should not be reused by the agent. <br>
Risk: The skill persists extracted knowledge into local Markdown files, which may include sensitive source content. <br>
Mitigation: Keep the wiki directory private and review generated wiki updates before relying on or sharing them. <br>
Risk: Generated wiki pages or demo scripts may contain incorrect summaries or stale information. <br>
Mitigation: Review generated pages, index updates, log entries, and demo outputs before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heavenchenggong/personal-wiki) <br>
- [IMA agent interface](https://ima.qq.com/agent-interface) <br>
- [Evernote developer token](https://app.yinxiang.com/api/DeveloperToken.action) <br>
- [Wiki schema template](wiki-template/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell and Python code blocks plus local Markdown wiki files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read private note content or local raw files and may write or update local wiki pages, index, and ingest log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
