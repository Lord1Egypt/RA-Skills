## Description: <br>
Helps an agent prepare, quality-check, publish, verify, and locally register normal Marktplaats.nl sale advertisements through a gated workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roelbroersma](https://clawhub.ai/user/roelbroersma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create and manage individual Marktplaats.nl listings with copy quality, preflight, live verification, and local register checks. It is intended for normal sale advertisements, not bulk posting, account-security bypass, buyer messaging, or unauthorized paid options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with a logged-in Marktplaats account, which may expose account or listing data if used without clear user control. <br>
Mitigation: Use it only after explicit per-ad posting or editing instructions, keep saved snapshots private, and avoid sharing session-related data. <br>
Risk: Optional probe and fetch paths may collect broader or more privacy-sensitive page data than the core workflow needs. <br>
Mitigation: Prefer Marktplaats URLs, use browser-session probes only for the active listing task, and avoid raw cookies or cookie files unless the operator understands the saved-output privacy impact. <br>
Risk: Publication or paid-option choices could create unintended marketplace actions or costs. <br>
Mitigation: Stop unless copy-QA, preflight, live verification, and register-update gates pass, and require explicit approval before publishing, editing, or enabling paid options. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/roelbroersma/marktplaats-publisher) <br>
- [Marktplaats.nl](https://www.marktplaats.nl) <br>
- [README](README.md) <br>
- [English Guide](references/guide-en.md) <br>
- [Nederlandse Handleiding](references/handleiding-nl.md) <br>
- [Robust Posting Checklist](references/robust-posting-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON-backed ad records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are gated by copy-QA, preflight, live verification, and register-update checks before publication-related actions continue.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
