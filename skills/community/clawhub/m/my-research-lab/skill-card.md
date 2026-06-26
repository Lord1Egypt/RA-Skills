## Description: <br>
My Research Lab is a self-evolving personal research assistant that tracks a user's research direction, gathers daily discoveries, runs deeper discussions, and turns promising ideas into project tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iriswong31](https://clawhub.ai/user/iriswong31) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run a persistent personal research workflow: configure a research direction, receive daily research briefings, archive findings, run periodic brainstorms, and track follow-up projects. Developers and operators may use its reference docs to configure schedules, storage, push channels, source skills, and memory-backed preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep running through scheduled research and brainstorming tasks. <br>
Mitigation: Confirm the exact schedules, timeouts, push destinations, and pause or deletion process before enabling automations. <br>
Risk: The skill reads memory and local configuration to personalize research, rankings, and follow-up tasks. <br>
Mitigation: Review the memory fields, configuration files, and archived outputs regularly, and keep each research lab in an isolated configuration and storage location. <br>
Risk: The skill can send or archive personalized outputs through email, webhooks, local files, or storage skills. <br>
Mitigation: Use scoped SMTP or webhook credentials, verify recipients and storage paths, and prefer least-privilege push and storage integrations. <br>
Risk: Research summaries and project guidance may include incorrect, stale, or unsuitable recommendations, especially for regulated domains. <br>
Mitigation: Review generated briefings before acting on them and include domain-specific disclaimers for health, medical, legal, or investment topics. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Cold Start Workflow](references/cold-start.md) <br>
- [Three-Layer Operation Rules](references/three-layers.md) <br>
- [Self-Evolving Engine Rules](references/self-evolving.md) <br>
- [Scheduled Prompt Templates](references/cron-prompts.md) <br>
- [Configuration Schema](references/config-schema.md) <br>
- [Channels and Tools Guide](references/channels-and-tools.md) <br>
- [Source Skills Registry](references/source-skills-registry.md) <br>
- [Nuwa Skill Reference](https://github.com/nuwa-skill) <br>
- [AIHOT Skill Reference](https://aihot.virxact.com/aihot-skill/) <br>
- [ClawHub Skill Page](https://clawhub.ai/iriswong31/my-research-lab) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Configuration, Guidance] <br>
**Output Format:** [Markdown and HTML briefings with JSON configuration records and concise task guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create scheduled automations, memory updates, archives, and push notifications when configured.] <br>

## Skill Version(s): <br>
3.3.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
