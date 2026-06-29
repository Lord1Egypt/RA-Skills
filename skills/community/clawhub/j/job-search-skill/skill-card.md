## Description: <br>
Searches LinkedIn, Poslovi Infostud, and HelloWorld.rs for roles matching a user's target job list, scores each listing against a local resume, and can produce chat digests, optional email digests, daily scheduling, and cover letters on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanishsidhu](https://clawhub.ai/user/tanishsidhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use this skill to search Serbia and remote job boards, compare listings against their resume, and draft application materials for manual review. It is designed to keep application control with the user and does not auto-apply to jobs. <br>

### Deployment Geography for Use: <br>
Global; default searches focus on Serbia and remote roles. <br>

## Known Risks and Mitigations: <br>
Risk: Enabling email requires storing a Gmail App Password in the local config file. <br>
Mitigation: Keep the skill folder private, avoid committing or sharing it, restrict local file access where possible, and rotate or revoke the app password if exposure is suspected. <br>
Risk: The skill reads a local resume and uses scraped job listings to generate scores, summaries, and cover letters. <br>
Mitigation: Review job scores, justifications, and generated cover letters before relying on them or sending application materials. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tanishsidhu/job-search-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown chat output with job scores, justifications, setup commands, configuration edits, and optional cover-letter prose.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON and SQLite state during use; optional email output requires user-provided SMTP configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
