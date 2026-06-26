## Description: <br>
Convex helps agents manage Convex projects, deployments, keys, domains, and functions through the OOMOL convex connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and administer Convex cloud resources, execute Convex functions, and manage projects, deployments, deploy keys, custom domains, regions, and deployment classes through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Convex projects, deployments, deploy keys, and custom domains, and can run Convex functions, actions, and mutations. <br>
Mitigation: Require explicit user approval for write and destructive operations, and inspect the live action schema before constructing payloads. <br>
Risk: The skill requires trusting OOMOL with Convex access and relies on the oo CLI for authenticated operations. <br>
Mitigation: Use it only with trusted OOMOL-connected accounts, verify CLI installation paths, and avoid automatic pipe-to-shell installation. <br>
Risk: Security evidence says some mutation or execution actions may be understated by the skill's safety labels. <br>
Mitigation: Treat run_function, run_mutation, run_action, deploy-key operations, and deletion actions as sensitive even when labels are absent or incomplete. <br>


## Reference(s): <br>
- [ClawHub Convex Skill](https://clawhub.ai/oomol/oo-convex) <br>
- [Convex Homepage](https://www.convex.dev) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL Convex Connection](https://console.oomol.com/app-connections?provider=convex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce JSON responses from the oo CLI; state-changing actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
