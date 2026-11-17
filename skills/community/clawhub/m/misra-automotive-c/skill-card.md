## Description:

Review automotive Embedded C code against MISRA C:2012 rules, flag violations with rule numbers and ASIL classification, and provide MISRA-compliant replacement code for non-compliant lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[budhadityarano](https://clawhub.ai/user/budhadityarano)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embedded software engineers use this skill to review automotive C snippets for MISRA C:2012 issues, ASIL relevance, and replacement code patterns before formal safety and static-analysis review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a certified MISRA checker or a source of production-ready safety code.

Mitigation: Use it as AI-assisted review only, then verify findings and replacements with qualified static analysis, platform documentation, and human safety review.

Risk: Broad trigger phrases can activate safety-critical guidance in contexts where the user did not request a formal review.

Mitigation: Review activation phrases before deployment and narrow them for production workspaces that handle automotive or embedded C.

Risk: Generated C replacements may omit project-specific constraints such as compiler behavior, target hardware, timing, or deviation approvals.

Mitigation: Treat replacements as draft patterns and require project-specific engineering review, testing, and documented MISRA deviations where needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/budhadityarano/skills/misra-automotive-c)
- [Skill README](artifact/README.md)
- [MISRA mandatory rules reference](artifact/misra-mandatory.md)
- [MISRA required rules reference](artifact/misra-required.md)
- [ISO 26262 ASIL mapping](artifact/iso26262-mapping.md)
- [Memory and embedded-specific rules](artifact/memory-embedded.md)
- [Control flow reference](artifact/control-flow.md)
- [Preprocessor directives reference](artifact/preprocessor.md)
- [Types and casting reference](artifact/types-and-casting.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown reports with C code snippets and summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs rule numbers, violation categories, ASIL classifications, severity, locations, explanations, replacement code, and compliance summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
