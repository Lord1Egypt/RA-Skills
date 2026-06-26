## Description: <br>
Review automotive Embedded C code against MISRA C:2012 rules, flag violations with rule numbers and ASIL classification, and provide MISRA-compliant replacement code for non-compliant lines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[budhadityarano](https://clawhub.ai/user/budhadityarano) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review automotive embedded C snippets for MISRA C:2012 issues, ISO 26262 ASIL relevance, and candidate compliant replacements. It is intended as review assistance for code authors and reviewers, not as a substitute for certified MISRA tooling or qualified safety review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIL classifications and replacement code can be incomplete or incorrect for safety-critical automotive software. <br>
Mitigation: Treat outputs as draft review guidance and verify them with certified MISRA tooling and qualified safety reviewers before use in safety-critical development. <br>
Risk: Broad automotive and safety trigger terms may activate the skill outside a deliberate MISRA review workflow. <br>
Mitigation: Use explicit review prompts and confirm that the output is relevant before applying any suggested code changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/budhadityarano/misra-automotive-c) <br>
- [README](artifact/README.md) <br>
- [MISRA mandatory rules reference](artifact/misra-mandatory.md) <br>
- [MISRA required rules reference](artifact/misra-required.md) <br>
- [ISO 26262 ASIL mapping](artifact/iso26262-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown violation reports with tables and C code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes rule numbers, categories, ASIL classifications, severity, explanations, compliant replacement code, and summary counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
