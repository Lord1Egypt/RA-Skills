## Description: <br>
Capture product tour video segments using browser automation and screen recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to capture screenshots from a live Next.js web app, generate a full-screen product tour page, and publish a walkthrough for demos, onboarding, or hackathon judging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a target Next.js repository and overwrite tour-related files. <br>
Mitigation: Run it in a staging branch or disposable copy, and confirm the repository path, output directory, generated files, and build command before execution. <br>
Risk: The workflow may publish a public /tour page containing screenshots from live pages. <br>
Mitigation: Use sanitized or staging data, avoid authenticated or production-only pages, and review all screenshots before deployment. <br>
Risk: Browser automation fetches external pages and requires ffmpeg for capture-related workflows. <br>
Mitigation: Confirm outbound network access is expected and that required local binaries are installed before running capture steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/product-tour-capture) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript interfaces, shell command examples, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a screenshot capture manifest, generated tour page, QA status, live tour URL, and deployment timestamp when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
