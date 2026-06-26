## Description: <br>
Internationalization and localization layer for OpenClaw that auto-detects language, enforces correct diacritics, formats dates and currency per locale, and pipes output through a post-processing cleaner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bloommediacorporation-lab](https://clawhub.ai/user/bloommediacorporation-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to localize assistant behavior for multilingual conversations, especially Romanian and German output. It configures language detection, locale formatting, cultural tone, and optional response cleanup before text reaches the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently rewrite assistant responses before the user sees them. <br>
Mitigation: Enable it only where response rewriting is acceptable, and inspect or disable the processor for code, legal, medical, safety-critical, quoted, identifier-heavy, or mixed-language content. <br>
Risk: The advertised language scope is not fully consistent across evidence, with Romanian and German emphasized while processor files also include French and Spanish behavior. <br>
Mitigation: Confirm the active language and supported-language list before deployment, and validate output for each enabled language. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bloommediacorporation-lab/openclaw-i18n-skill) <br>
- [Project Website](https://bloommediacorporation-lab.github.io/openclaw-i18n-skill/) <br>
- [Bloom Media](https://bloommedia.ro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code snippets and cleaned text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post-process assistant responses by removing non-Latin characters, normalizing whitespace, and applying language-specific diacritic and typo fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
