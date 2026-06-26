## Description: <br>
End-to-end Meta Facebook and Instagram advertising system orchestrator covering strategy research, creative generation, campaign delivery, and post-campaign optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LanbowAI](https://clawhub.ai/user/LanbowAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan, create, launch, monitor, and optimize Meta advertising campaigns through guided research, creative generation, and lanbow-ads CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use powerful Meta ad-management credentials and change paid advertising campaigns. <br>
Mitigation: Install only when the lanbow-ads CLI is trusted, use a test ad account with a low budget, grant the narrowest scopes possible, and manually approve campaign activation, budget, targeting, media upload, and credential-storage steps. <br>
Risk: Advertising tokens, app secrets, Gemini keys, or long-lived system-user tokens may be exposed if pasted into chat. <br>
Mitigation: Use platform secret fields or environment variables for credentials, and only provide optional secrets such as META_APP_SECRET or GEMINI_API_KEY when the requested workflow requires them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LanbowAI/lanbow-claw-skill) <br>
- [Lanbow homepage](https://lanbow.com/) <br>
- [Lanbow Claw Skill guide](https://lanbow.com/blog/lanbow-claw-skill) <br>
- [lanbow-ads npm package](https://www.npmjs.com/package/lanbow-ads) <br>
- [Meta Ad Account Setup Guide](references/meta-account-setup.md) <br>
- [Lanbow Ads CLI](references/ad-delivery.md) <br>
- [Meta Ads CLI Commands Reference](references/ad-delivery-commands.md) <br>
- [Ads Strategy Researcher](references/strategy-research.md) <br>
- [AI Ad Creative Image Generation](references/creative-generation.md) <br>
- [Post-Campaign Review](references/post-campaign-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, campaign configuration, strategy reports, review plans, and generated creative file references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the lanbow-ads CLI, Meta Marketing API, web research tools, and Google Gemini for creative generation when the user supplies the required credentials.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
