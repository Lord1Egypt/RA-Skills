## Description: <br>
CNIPA撤三（连续三年不使用）双轨证据引擎，用于构建答辩证据链并执行质证审计。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisngzhongling](https://clawhub.ai/user/jisngzhongling) <br>

### License/Terms of Use: <br>
Commercial License <br>


## Use Case: <br>
Trademark and legal operations professionals use this skill to process local evidence for China trademark non-use cancellation matters, generate defense or cross-examination materials, and review period coverage, evidence mapping, and risk level. It supports local CLI, desktop, and Web UI workflows for document production and human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file controls and evidence processing can expose sensitive case materials or overwrite generated outputs. <br>
Mitigation: Run the skill in a dedicated virtual environment on trusted evidence files, keep outputs outside evidence directories, and review generated documents and validation JSON before submission. <br>
Risk: The local Web UI or desktop server could expose case files if bound beyond localhost. <br>
Mitigation: Keep the Web UI bound to 127.0.0.1 and do not expose the desktop or web server on a network unless access controls are reviewed. <br>
Risk: The organize-directory workflow includes cleanup behavior that can remove files in the chosen target directory. <br>
Mitigation: Use --organize-dir only with a disposable output folder and confirm the path before running. <br>
Risk: Generated evidence assessments and legal documents may be incomplete or incorrect if source evidence is missing, noisy, or misclassified. <br>
Mitigation: Treat outputs as technical support rather than legal advice, verify evidence mappings manually, and require professional review before case submission. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisngzhongling/jiang-irac-nonuse-evidence) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/jisngzhongling) <br>
- [README](artifact/README.md) <br>
- [Install Guide](artifact/INSTALL.md) <br>
- [Legal Disclaimer](artifact/DISCLAIMER.md) <br>
- [License](artifact/LICENSE.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON diagnostics, DOCX reports, XLSX casebooks, and merged PDF evidence bundles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local evidence indexes, defense reasons, risk reports, validation JSON files, audit logs, and rule-profile records for human review.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
