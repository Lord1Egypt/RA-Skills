## Description: <br>
Laravel Docs Reader gives agents and developers version-aware Laravel documentation lookup, PSR-12 Laravel code skeletons, and Laravel 10/11/12 version-difference guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[relunctance](https://clawhub.ai/user/relunctance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill while working in Laravel projects to look up version-specific framework guidance, generate conventional Laravel snippets, and check PSR-12 or Laravel 10/11/12 migration differences before editing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Laravel code or command guidance may be incorrect for a specific application context. <br>
Mitigation: Review generated code before applying it in a Laravel project. <br>
Risk: Separate cloned scripts or token-based publish commands could carry risks outside normal skill use. <br>
Mitigation: Inspect any external repository or script before running cloned PHP tools or token-based publish commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/relunctance/laravel-docs-reader) <br>
- [README](artifact/README.md) <br>
- [Version Detection Logic](artifact/references/version-detection.md) <br>
- [Laravel Version Diff (10 / 11 / 12)](artifact/references/version-diff.md) <br>
- [PSR-12 Coding Standard Quick Reference](artifact/references/psr-12.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with PHP/Laravel code snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include version notes, caveats, and references to bundled Laravel guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill specification) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
