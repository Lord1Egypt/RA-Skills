## Description: <br>
Create and deploy a festive Chinese New Year (Year of the Horse 2026) animated GIF sticker maker web app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to scaffold a Next.js web app for generating custom Year of the Horse blessing cards and WeChat-compatible animated GIF stickers from short user-provided text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google/Gemini API key use is under-disclosed. <br>
Mitigation: Document required API keys, restrict them by service and deployment origin, and disclose that entered names or text are sent to AI providers. <br>
Risk: Public generation endpoints can consume the deployer's API quota or billing. <br>
Mitigation: Add authentication, rate limiting, request validation, and usage monitoring before making the app public. <br>
Risk: The quick-start production deploy command may publish before deployment settings are reviewed. <br>
Mitigation: Review Vercel project settings, environment variables, and access controls before production deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiafar/horse-sticker-maker) <br>
- [gif.js](https://github.com/jnordberg/gif.js) <br>
- [Google AI Platform Model API](https://aiplatform.googleapis.com/v1/publishers/google/models) <br>
- [Next.js TypeScript Configuration](https://nextjs.org/docs/app/building-your-application/configuring/typescript) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bundled Next.js project files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a deployable template that renders images and GIF stickers; generated app behavior depends on configured Google/Gemini API keys and third-party services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
