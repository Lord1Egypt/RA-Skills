## Description:

Auto-deploy websites to GitHub Pages with custom domain support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendwealth](https://clawhub.ai/user/sendwealth)

### License/Terms of Use:


## Use Case:

Developers and site maintainers use this skill to configure GitHub Actions workflows that publish static websites, documentation, blogs, portfolios, and static apps to GitHub Pages, including custom domain and HTTPS setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated GitHub Actions workflow can publish website changes automatically after pushes.

Mitigation: Review the workflow before use and consider protected branches or deployment approvals for important sites.

Risk: Unpinned actions or globally installed npm tools may change behavior over time.

Mitigation: Pin GitHub Actions to reviewed commit SHAs and use exact-version project dependencies with a lockfile.

Risk: Preview deployment guidance references a third-party action.

Mitigation: Review any third-party action before adoption and avoid it unless it is needed for the deployment process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sendwealth/skills/github-pages-auto-deploy)
- [Example deployed site](https://sendwealth.github.io/claw-intelligence/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, shell, and HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment workflow and setup guidance; no runtime service or API credentials are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
