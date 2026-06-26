## Description: <br>
Paper Reader Deep helps agents extract metadata and key data from PDF papers, analyze their scientific contribution, and produce structured deep-reading reports in Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jibeilindong](https://clawhub.ai/user/jibeilindong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical readers use this skill to process directories of PDF papers, extract basic bibliographic and numerical signals, and create structured reports for deeper AI-assisted critique and follow-up research notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads all PDFs in the directory supplied by the user. <br>
Mitigation: Run it only on directories intended for analysis and avoid confidential or unpublished papers unless that access is approved. <br>
Risk: The skill writes Markdown reports and a summary into the same directory as the PDFs. <br>
Mitigation: Use a working copy or dedicated output directory when preserving the original folder contents matters. <br>
Risk: The skill may query CrossRef for DOI metadata during paper processing. <br>
Mitigation: Avoid network metadata lookup for sensitive paper collections unless external DOI queries are acceptable. <br>
Risk: Generated critique and relevance sections can contain incomplete or placeholder analysis. <br>
Mitigation: Have a qualified reader review the Markdown reports before using them for research decisions or publication planning. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jibeilindong/paper-reader-deep) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Analysis framework](artifact/config/analysis_framework.md) <br>
- [Report template](artifact/config/report_template.md) <br>
- [Section configuration](artifact/config/section_config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates one Markdown report per PDF and a summary report in the supplied PDF directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
