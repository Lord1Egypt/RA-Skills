## Description: <br>
Use this skill when working with this repository's `gsc` CLI, including Google Cloud OAuth client setup, CLI authentication, troubleshooting auth/config issues, and running all supported commands (site, sitemap, url inspection, analytics, doctor, config). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NmadeleiDev](https://clawhub.ai/user/NmadeleiDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site owners, and SEO operators use this skill to install, authenticate, operate, and troubleshoot the `gsc` command-line interface for Google Search Console workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets and stored Google Search Console credentials can expose account access if mishandled. <br>
Mitigation: Keep OAuth client JSON and stored credentials private, and use the `--readonly` scope for read-only tasks. <br>
Risk: CSV output paths can overwrite files or place Search Console data in unintended locations. <br>
Mitigation: Choose CSV destinations deliberately and review output paths before running commands that write files. <br>
Risk: Installing an untrusted CLI package or source repository can introduce supply-chain risk. <br>
Mitigation: Install only when the `google-search-console-cli` package or source repository is trusted for the environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI command examples, OAuth setup steps, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
