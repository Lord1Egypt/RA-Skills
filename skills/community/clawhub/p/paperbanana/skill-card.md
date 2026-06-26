## Description: <br>
Generate publication-quality academic diagrams from paper methodology text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwzhu-pku](https://clawhub.ai/user/dwzhu-pku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, and developers use PaperBanana to turn methodology text and figure captions into academic diagrams or plots for papers and presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged runner depends on project modules outside the three-file skill and can execute code from the surrounding project environment. <br>
Mitigation: Use it only with the complete, trusted PaperBanana/PaperVizAgent project, and review project code and dependencies before execution. <br>
Risk: The skill may send supplied paper content to external model providers and can make expensive parallel model and image-generation calls. <br>
Mitigation: Avoid confidential unpublished material unless provider data policies are acceptable, use limited-scope API keys, and tune candidate and critic settings to control cost. <br>
Risk: First-run execution may download PaperBananaBench data before generating outputs. <br>
Mitigation: Run in an environment with approved network access and storage, or prefetch and verify required data before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dwzhu-pku/paperbanana) <br>
- [PaperBanana paper (arXiv:2601.23265)](https://arxiv.org/abs/2601.23265) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [PNG image file(s) with newline-delimited absolute file paths on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit multiple candidate image files when num-candidates is greater than 1.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
