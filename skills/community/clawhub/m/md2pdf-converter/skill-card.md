## Description: <br>
Converts Markdown documents to professional PDFs with Unicode, Chinese font, and colorful Twemoji support using Pandoc, WeasyPrint, and a local emoji cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianxingleo](https://clawhub.ai/user/tianxingleo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document authors use this skill to convert Markdown reports or documents into PDFs with full Unicode, Chinese character rendering, code highlighting, tables, and colorful emoji support. It is useful when a local conversion workflow is needed after the initial emoji asset setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First run downloads about 150MB of Twemoji assets from GitHub and stores them under ~/.cache/md2pdf. <br>
Mitigation: Use only in environments that permit this download, or pre-verify and vendor the Twemoji archive before deployment. <br>
Risk: The converter relies on a hardcoded helper script path when generating the emoji mapping. <br>
Mitigation: Fix or parameterize the helper script path before using the skill in managed or multi-user environments. <br>
Risk: Cache cleanup commands can remove the local emoji cache and force another download. <br>
Mitigation: Review cache cleanup steps before running them and preserve approved cached assets where repeatable offline conversion is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianxingleo/md2pdf-converter) <br>
- [Twemoji 14.0.0 archive](https://github.com/twitter/twemoji/archive/refs/tags/v14.0.0.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated PDF files from the converter script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [First run downloads and caches Twemoji assets; subsequent conversions can run offline from the local cache.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
