## Description:

Fetches and summarizes recent papers from arXiv and Hugging Face, providing JSON digests and optional local API access for customizable research updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agents use this skill to install and run Agentic Paper Digest, tune paper-source settings, fetch recent arXiv and Hugging Face papers, and return JSON digests or local API results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bootstrap installs and updates mutable code from the upstream GitHub main branch with the user's local permissions.

Mitigation: Review and pin the upstream repository commit before installation, and run the skill in an isolated workspace.

Risk: Environment loading can expose API keys or other secrets from .env to the local paper pipeline.

Mitigation: Keep only required values such as SKILLBOSS_API_KEY in .env, avoid valuable unrelated secrets, and restrict file permissions.

Risk: The API stop helper may terminate unrelated services that use port 8000 or match the paper_finder process pattern.

Mitigation: Check active processes before running stop_api.sh and avoid using it on shared development hosts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-agentic-paper-digest-skill)
- [Agentic Paper Digest Project](https://github.com/matanle51/agentic_paper_digest)
- [SkillBoss Setup Guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration edits, and JSON digest output from the underlying paper pipeline]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration, environment files, a virtual environment, and a SQLite data store under PROJECT_DIR.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
