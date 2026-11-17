## Description:

用 find_skills.py 在 ClawHub 搜索或列举已装技能，支持 JSON 输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover ClawHub skills, inspect local installed skills, and get readable or JSON-formatted search results for skill selection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using search @file can send selected local file contents to ClawHub as a remote search query.

Mitigation: Do not use search @file with secrets, keys, .env files, private documents, or source files.

Risk: install --execute can install third-party code into the agent environment.

Mitigation: Inspect the target skill and review its source before executing an install.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/jisu-find-skill)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands, guidance]

**Output Format:** [Readable text or structured JSON, with command examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include skill names, ClawHub paths, install hints, descriptions, authors, stars, downloads, and local installation status.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
