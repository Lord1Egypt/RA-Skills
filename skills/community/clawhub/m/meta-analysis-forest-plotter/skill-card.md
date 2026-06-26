## Description: <br>
Use when creating forest plots for meta-analyses, visualizing effect sizes across studies, or generating publication-ready meta-analysis figures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to create forest plots and meta-analysis summaries from structured study data for systematic reviews, manuscripts, presentations, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned Python dependencies can make generated plots or calculations difficult to reproduce. <br>
Mitigation: Install from trusted package sources and pin numpy, scipy, matplotlib, and pandas versions in production environments. <br>
Risk: CLI examples or entry points may differ from the packaged script path. <br>
Mitigation: Verify the installed script entry point before execution and prefer the shipped artifact path when invoking the tool. <br>
Risk: Generated plot files can overwrite existing files at the selected output path. <br>
Mitigation: Write outputs to a deliberate directory and review file names before running commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/meta-analysis-forest-plotter) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; generated plot files may be PDF, PNG, SVG, or TIFF when the script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Console summaries include fixed-effect and random-effects estimates, confidence intervals, p-values, and heterogeneity statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact metadata lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
