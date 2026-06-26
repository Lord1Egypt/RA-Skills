## Description: <br>
Builds an OpenClaw multi-agent HQ system with a mother-bot, core sub-bots, org design, role files, dispatcher rules, task state machine, blackboard protocol, and onboarding docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyandlg123321-maker](https://clawhub.ai/user/happyandlg123321-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, team leads, and OpenClaw workspace maintainers use this skill to turn a multi-agent idea or scattered bot notes into a small, teachable, installable HQ operating skeleton. It focuses on concrete files, routing rules, task cards, review loops, and newcomer acceptance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated bot profiles, dispatcher rules, task cards, blackboard entries, or upgrade logs may be treated as operating context by future agents before they have been reviewed. <br>
Mitigation: Install the skill in a scoped workspace and review generated operating files before relying on them. <br>
Risk: Secrets or unverified instructions placed into shared persistent files may be reused by later agents. <br>
Mitigation: Keep secrets out of generated shared files and verify instructions before adding them to persistent workspace context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happyandlg123321-maker/openclaw-multi-agent-hq-builder) <br>
- [Publisher profile](https://clawhub.ai/user/happyandlg123321-maker) <br>
- [Install guide](references/install-guide.md) <br>
- [Acceptance checklist](references/acceptance-checklist.md) <br>
- [Minimal examples](references/minimal-examples.md) <br>
- [Test prompts](references/test-prompts.md) <br>
- [Publish checklist](references/publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file lists, checklists, templates, and inline path examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outputs should be reviewed before they become persistent operating context for other agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
