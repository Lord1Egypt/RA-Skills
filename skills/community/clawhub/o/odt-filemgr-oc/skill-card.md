## Description: <br>
Create, parse, and edit ODT (OpenDocument Text) files locally using Python and odfdo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juicyroots](https://clawhub.ai/user/juicyroots) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to inspect, create, extract text from, and update local ODT files, including documents that are downloaded from or later uploaded to NextCloud by a separate skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editing commands can overwrite or materially change important ODT documents. <br>
Mitigation: Inspect documents first, work on a copy or temporary file, and review the edited result before replacing or uploading the original. <br>
Risk: The skill depends on the external odfdo Python package being installed in the agent environment. <br>
Mitigation: Install only when that package is acceptable for the environment and keep dependency installation scoped to the intended runtime. <br>


## Reference(s): <br>
- [ODT File Manager Reference](REFERENCE.md) <br>
- [ClawHub skill page](https://clawhub.ai/juicyroots/odt-filemgr-oc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated tool output may be plain text or JSON metadata summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on local ODT files and requires Python 3.10+ with the odfdo package installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
