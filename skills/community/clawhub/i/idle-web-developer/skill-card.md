## Description: <br>
Idle Web Developer helps agents scaffold, build, and deploy polished web apps while idle, with optional analytics and waitlist integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaswir](https://clawhub.ai/user/Jaswir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to generate small, polished websites, configure optional analytics and waitlist capture, and deploy the result to Vercel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores deployment and integration credentials for reuse. <br>
Mitigation: Use a least-privileged Vercel token, avoid storing unnecessary secrets, never provide Supabase service-role keys, and inspect or delete .skill-config when finished. <br>
Risk: Generated sites can include analytics or waitlist email collection. <br>
Mitigation: Review each generated site before publishing and update privacy, analytics, and waitlist copy when tracking or email collection is enabled. <br>
Risk: The skill can publish generated sites to Vercel. <br>
Mitigation: Use --skip-deploy or perform a manual review before allowing production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jaswir/idle-web-developer) <br>
- [Skill homepage](https://github.com/jaswirraghoe/idle-web-developer) <br>
- [Website Builder Reference Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated web app files, configuration steps, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May scaffold static or Next.js web apps, write configuration, and deploy to Vercel when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
