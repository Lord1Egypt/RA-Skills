## Description: <br>
Deploy and manage Netlify sites with npx netlify, including auth, linking, preview deploys, production releases, and config checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy web projects to Netlify from the terminal, including first deploys, preview deploys, production releases, site linking, monorepo setup, and netlify.toml checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can use an existing Netlify CLI login and send deployment artifacts and metadata to Netlify. <br>
Mitigation: Install only when Netlify is an approved deployment target for the project, and review preview deploy output before promotion. <br>
Risk: Production deploys can publish unreviewed changes. <br>
Mitigation: Require explicit user confirmation before running npx netlify deploy --prod. <br>
Risk: Environment-variable commands can expose or alter sensitive configuration. <br>
Mitigation: Require explicit approval for env:set and env:import operations, and keep secrets out of ~/netlify-deploy/memory.md. <br>


## Reference(s): <br>
- [Netlify Documentation](https://docs.netlify.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/netlify-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
