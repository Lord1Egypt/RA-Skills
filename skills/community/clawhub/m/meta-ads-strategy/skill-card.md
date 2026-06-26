## Description: <br>
Run Facebook and Instagram ads end-to-end with guidance for Meta ads strategy, creative, copy, campaign structure, targeting, budgeting, ROAS tracking, Pixel setup, and an ad brief workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeannen](https://clawhub.ai/user/jeannen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertisers, founders, marketers, and agent users use this skill to plan, create, launch, and optimize Meta campaigns for Facebook and Instagram. It helps users build ad briefs, assess readiness, write copy, choose creative, structure campaigns, set budgets, configure tracking, and diagnose ROAS or performance issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent toward ad-account actions that spend money or change campaigns, budgets, Pixel setup, customer-data setup, or publishing state. <br>
Mitigation: Require explicit user approval before campaign creation, publishing, budget changes, Pixel or customer-data setup, and every AdKit or Ads Manager action. <br>
Risk: The skill may persist project-specific advertising preferences and briefs in local files. <br>
Mitigation: Review every proposed file read or write, and avoid storing sensitive payment, customer, or account-recovery information in persistent notes. <br>
Risk: Some account-safety guidance may be overconfident about platform enforcement outcomes. <br>
Mitigation: Treat the guidance as advisory, follow Meta platform policies, and do not rely on VPN or spare-account advice to avoid enforcement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeannen/meta-ads-strategy) <br>
- [AdKit homepage](https://adkit.so) <br>
- [When Should a SaaS Run Ads?](https://adkit.so/resources/when-to-run-ads-for-saas) <br>
- [AdKit Ad Library](https://adkit.so/features/ad-library?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, templates, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update ad-process.md and ad-brief.md when the user approves persistent project notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
