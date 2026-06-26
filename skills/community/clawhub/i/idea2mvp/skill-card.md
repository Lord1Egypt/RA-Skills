## Description: <br>
Helps users discover product ideas, validate market and technical feasibility, and build MVPs using structured research, reporting, coding, and optional email workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MorvanZhou](https://clawhub.ai/user/MorvanZhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to move from early product exploration through idea validation to a runnable MVP, with Chinese-language guidance, market research, competitive analysis, implementation planning, and optional report delivery by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores profile details, preferences, search results, reports, credentials, cache data, and logs under .skills-data/idea2mvp. <br>
Mitigation: Treat .skills-data/idea2mvp as sensitive local data, keep it out of version control, avoid storing unnecessary personal details, and delete cached data when it is no longer needed. <br>
Risk: The security summary flags authenticated browser automation for XiaoHongShu as risky. <br>
Mitigation: Disable or skip XiaoHongShu Playwright automation unless the user accepts the account and session risk, and clear browser cache data after use. <br>
Risk: The skill can email reports or attachments using configured SMTP credentials. <br>
Mitigation: Review generated content and attachment paths before sending, store SMTP credentials only in .skills-data/idea2mvp/.env, and send email only after an explicit user request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MorvanZhou/idea2mvp) <br>
- [Find Ideas Guide](references/find-ideas.md) <br>
- [Validate Ideas Guide](references/validate-ideas.md) <br>
- [Idea Expansion Methodology](references/idea-expansion.md) <br>
- [Evaluation Framework](references/evaluation-framework.md) <br>
- [Build MVP Guide](references/build-mvp.md) <br>
- [Frontend Design Guide](references/frontend-design.md) <br>
- [Email Notification Guide](references/send-email.md) <br>
- [Feasibility Report Template](assets/report-template.md) <br>
- [Product Hunt Developer Token Setup](https://www.producthunt.com/v2/oauth/applications) <br>
- [Agent Browser Skill](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language conversational guidance, Markdown reports, source files, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local runtime files under .skills-data/idea2mvp and may send email only when the user requests it and SMTP configuration is present.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
