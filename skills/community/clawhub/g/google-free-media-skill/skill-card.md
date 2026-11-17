## Description:

Helps agents scaffold browser-automation workflows for generating AI images with Google Gemini and short videos with Google Flow while tracking free-tier quotas.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[pbseiya](https://clawhub.ai/user/pbseiya)

### License/Terms of Use:


## Use Case:

Developers and creators can use this skill as a demonstration scaffold for image and video generation workflows that call local Node.js scripts, check free-tier quotas, and prepare browser automation for Google Gemini and Google Flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can report generation flow completion while operating as an incomplete demo scaffold.

Mitigation: Treat generated placeholder JSON as demonstration output and verify that real image or video files exist before using results downstream.

Risk: Browser automation may reuse Google session data.

Mitigation: Use a dedicated Google account and store any reusable browser profile or session data in a protected, isolated location.

Risk: Shell command construction should be fixed before execution from untrusted paths.

Mitigation: Run the scripts only from trusted directories until command invocation is hardened and dependencies are pinned with a lockfile.

Risk: Automating Google free-tier web interfaces may create service-terms or availability risk.

Mitigation: Review the applicable Google service terms and keep selectors, quotas, and fallback behavior under manual review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pbseiya/skills/google-free-media-skill)
- [Google Gemini](https://gemini.google.com)
- [Google Flow](https://labs.google/flow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JavaScript CLI scripts, JSON configuration, and local script output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Demo scripts can write placeholder JSON outputs until real Puppeteer or Playwright browser automation is implemented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
