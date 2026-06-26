## Description: <br>
Generate polished release notes and changelogs from git history by analyzing commits between tags or refs and categorizing changes into human-readable formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release managers use this skill to summarize git commit history into release notes, changelogs, GitHub releases, and short team announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper inspects local git history and generated notes may expose private commit subjects, bodies, author names, or author emails. <br>
Mitigation: Run it only in intended repositories and review generated notes for sensitive details before publishing. <br>
Risk: The security summary reports that maliciously named refs in an untrusted repository can cause the helper to run unintended local code. <br>
Mitigation: Use the helper only with trusted repositories, branches, and tags until the ref interpolation issue is fixed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/git-release-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown release notes, changelog sections, compact text announcements, and JSON commit data from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports GitHub release, compact, Keep a Changelog, and Slack/Discord announcement styles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
