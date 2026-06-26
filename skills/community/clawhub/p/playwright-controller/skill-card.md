## Description: <br>
Browse webpages with Playwright, wait for loading, capture screenshots, and extract page or element text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MRchenkuan](https://clawhub.ai/user/MRchenkuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to collect rendered webpage content, page screenshots, and selected element text for analysis or documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI loads the crawler from a developer-only absolute path, which may fail or execute an unintended local file. <br>
Mitigation: Review or patch the command to require the packaged local crawler module before installation or use. <br>
Risk: Captured screenshots and extracted page text are saved to disk and may include sensitive page content. <br>
Mitigation: Avoid authenticated or sensitive pages unless local capture is intended, and write outputs to a directory that can be inspected and deleted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MRchenkuan/playwright-controller) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Console status text plus PNG screenshots and extracted text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes screenshots, extracted content, and error notes to a configurable local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
