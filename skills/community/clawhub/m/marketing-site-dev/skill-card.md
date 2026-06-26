## Description: <br>
Opinionated end-to-end workflow for shipping a bilingual static company marketing site to Volcengine using Astro, React islands, Tailwind, TOS, CDN, HTTPS hardening, and scripted deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenshowinnovation](https://clawhub.ai/user/tenshowinnovation) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold, configure, deploy, and verify a bilingual company or product marketing site for mainland-China-oriented delivery on Volcengine. It is most relevant when the domain is ICP-filed and the project needs scripted TOS, CDN, DNS, certificate, cache, and HTTPS setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful Volcengine credentials and can change DNS, CDN, and TOS storage resources. <br>
Mitigation: Use least-privilege or temporary credentials, review scripts before execution, and back up existing DNS records and bucket contents. <br>
Risk: Deployment scripts bypass local proxy environment settings. <br>
Mitigation: Confirm that bypassing proxy settings is acceptable in the target environment before running the scripts. <br>
Risk: The workflow is specialized for Volcengine and mainland-China delivery. <br>
Mitigation: Install and use it only when that deployment target is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenshowinnovation/marketing-site-dev) <br>
- [Publisher profile](https://clawhub.ai/user/tenshowinnovation) <br>
- [Phase 1 static site guide](references/phase-1-static-site.md) <br>
- [Phase 2 Volcengine deploy guide](references/phase-2-volcengine-deploy.md) <br>
- [Landmines](references/landmines.md) <br>
- [Verification checklist](references/verification.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code, shell commands, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or copy Astro project files, Volcengine deployment scripts, CDN payloads, and verification commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
