## Description: <br>
Automate Linear task processing with Discord notifications and git sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentchan](https://clawhub.ai/user/vincentchan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workflow owners use this skill to connect Linear task intake with Discord notifications, agent task handling, Linear status updates, and optional git synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Linear and Discord events can drive an agent to update tasks, send messages, perform broad work, and push git changes without clear approval boundaries. <br>
Mitigation: Review before installing, keep Discord triggering scoped, and require human approval before enabling unattended task execution or git push. <br>
Risk: The workflow depends on Linear API keys, Discord bot tokens, and webhook URLs. <br>
Mitigation: Use dedicated low-privilege tokens, treat webhook URLs and bot tokens as secrets, and rotate credentials if they are exposed. <br>
Risk: External automation services can continue triggering the workflow after setup. <br>
Mitigation: Document how to pause each Make, Pipedream, or Zapier automation and disable integrations when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vincentchan/linear-autopilot) <br>
- [Make.com Setup Guide](references/make-setup.md) <br>
- [Pipedream Setup Guide](references/pipedream-setup.md) <br>
- [Zapier Setup Guide](references/zapier-setup.md) <br>
- [Make.com](https://make.com) <br>
- [Pipedream](https://pipedream.com) <br>
- [Zapier](https://zapier.com) <br>
- [Linear GraphQL API endpoint](https://api.linear.app/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and workflow setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to update Linear issues, send Discord notifications, write task outputs, and optionally commit and push git changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
