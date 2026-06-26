## Description: <br>
Manage your PostSyncer social media workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abakermi](https://clawhub.ai/user/abakermi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage PostSyncer social media workflows, including listing workspaces and posts and creating basic scheduled text posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create social posts through the PostSyncer CLI. <br>
Mitigation: Review the workspace ID and post text before allowing an agent to create or publish posts. <br>
Risk: The skill requires a PostSyncer API key for authenticated operations. <br>
Mitigation: Use a revocable, least-privileged API key where available and install only if you trust PostSyncer and the postsyncer CLI. <br>


## Reference(s): <br>
- [PostSyncer Settings](https://app.postsyncer.com/settings) <br>
- [ClawHub skill page](https://clawhub.ai/abakermi/openclaw-postsyncer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POSTSYNCER_API_KEY for authenticated PostSyncer CLI use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
