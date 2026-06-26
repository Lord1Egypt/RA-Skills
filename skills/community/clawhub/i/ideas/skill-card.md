## Description: <br>
Records everyday ideas, inspiration snippets, and technical concepts with topic tags, status tracking, and keyword search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kazuya-ecnu](https://clawhub.ai/user/kazuya-ecnu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and developers use this skill to capture, organize, search, update, and retire ideas in a local JSON-backed list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ideas are saved locally in a JSON file and may persist beyond the current session. <br>
Mitigation: Avoid storing secrets or highly sensitive information, and confirm the data location before relying on backups or deletion. <br>
Risk: Broad natural-language triggers could capture an idea when the user did not intend to save it. <br>
Mitigation: Use explicit save, update, and delete requests and review saved content when handling sensitive notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kazuya-ecnu/ideas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Plain text or Markdown responses with local JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists idea records, tags, status, and timestamps in a local JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
