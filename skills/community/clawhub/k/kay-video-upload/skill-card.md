## Description: <br>
Automates short-video publishing to Douyin, WeChat Channels, Kuaishou, Xiaohongshu, and Bilibili through local Chrome and Playwright workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kay1003](https://clawhub.ai/user/kay1003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and agents use this skill to prepare local video files and publish them to supported Chinese short-video platforms after the relevant accounts have been logged in. It supports login, cookie reuse, platform-specific publishing, and all-platform publishing from a file-based video directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved platform sessions can be reused to publish public videos across multiple creator accounts. <br>
Mitigation: Use dedicated accounts where possible, protect the scripts/cookies directory, and delete saved cookies when access is no longer needed. <br>
Risk: The all-platform mode can publish the same local videos to every logged-in platform. <br>
Mitigation: Review the target platform and video list before running publish commands, and use all-platform publishing only when that outcome is intentional. <br>
Risk: The Xiaohongshu flow depends on a signing service endpoint configured as XHS_SERVER. <br>
Mitigation: Keep XHS_SERVER on a trusted local endpoint and verify the endpoint before running Xiaohongshu login or publish workflows. <br>
Risk: The setup workflow installs Python packages and Playwright browser components. <br>
Mitigation: Run setup in a controlled environment and review dependency installation before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kay1003/kay-video-upload) <br>
- [Platform notes](references/platforms.md) <br>
- [social-auto-upload upstream project](https://github.com/dreammis/social-auto-upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local cookie files and platform publishing state during login or publish runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
