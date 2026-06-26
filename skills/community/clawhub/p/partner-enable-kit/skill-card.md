## Description: <br>
Generates reviewable partner enablement kits for channel or partner workflows, including partner profiles, required materials, FAQs, blockers, version differences, and update cadence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, partner operations teams, and channel enablement teams use this skill to turn partner type, product scope, and target scenario inputs into a structured Markdown enablement draft. It is intended for reviewable content preparation, not for publishing internal sensitive policy or replacing formal partnership agreements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Partner enablement inputs may include confidential partner details, internal policy material, or personal information. <br>
Mitigation: Provide only materials approved for this workflow, redact sensitive inputs before use, and review generated Markdown before sharing. <br>
Risk: Generated drafts can be incomplete or misleading when required partner type, product scope, or target scenario details are missing. <br>
Mitigation: Use the generated pending-confirmation items as review gates and fill missing facts before turning a draft into an executable checklist. <br>
Risk: The bundled script can write output to a local path when invoked with --output. <br>
Mitigation: Choose output paths deliberately and use dry-run or stdout output when file creation is not intended. <br>
Risk: Dormant audit modes in the script can scan local files if the bundled specification is modified to enable them. <br>
Mitigation: Do not modify the bundled specification to enable audit modes unless local file-scanning behavior is intentional and approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/partner-enable-kit) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>
- [Example Output](artifact/examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown draft by default, with optional JSON report from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script can print to stdout or write a local output file when --output is supplied; dry-run mode avoids writing files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
