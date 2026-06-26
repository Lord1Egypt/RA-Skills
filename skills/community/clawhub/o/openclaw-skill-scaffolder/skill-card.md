## Description: <br>
Generate complete OpenClaw skill projects with SkillPay.me billing pre-wired. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wms2537](https://clawhub.ai/user/wms2537) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate deployable OpenClaw skill project scaffolds with SKILL.md, Cloudflare Worker configuration, TypeScript worker code, billing types, and deployment commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External data sharing and automatic charging behavior may be under-disclosed. <br>
Mitigation: Before installing or deploying, confirm the external endpoint, what setup data is sent, how billing API secrets are stored, when charges occur, and whether generated templates require explicit user consent before charging downstream users. <br>
Risk: Generated scaffolds include billing integration that could charge users before custom skill behavior is reviewed. <br>
Mitigation: Review generated code, deployment commands, and billing flow before publishing or executing a generated skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wms2537/openclaw-skill-scaffolder) <br>
- [OpenClaw Skill Scaffolder endpoint](https://openclaw-skill-scaffolder.swmengappdev.workers.dev/scaffold) <br>
- [SkillPay billing endpoint](https://skillpay.me/api/billing/charge) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [JSON containing generated file contents, deployment commands, and a test command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY; generated projects may include additional environment variables requested by the caller.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
