## Description: <br>
Create and manage Obsidian Clip notes from web pages, producing readable summaries and saving them into an Obsidian vault under Clip/YYYY-MM/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstract-sum](https://clawhub.ai/user/abstract-sum) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and note-taking users use this skill to turn a URL into a concise Chinese or English Obsidian Clip note with takeaways, action items, caveats, tags, and a source link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and summarize logged-in or paywalled pages at the user's request, which may include private content. <br>
Mitigation: Use it only with pages the user is comfortable letting the agent read and summarize. <br>
Risk: Clips are persistent local notes in the configured Obsidian vault. <br>
Mitigation: Set OBSIDIAN_VAULT to the intended vault and review saved notes for sensitive content before sharing or syncing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abstract-sum/obsidian-clip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown Obsidian notes with shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent local notes under the configured Obsidian vault in Clip/YYYY-MM/.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
