## Description: <br>
Real-time Laravel package search via Packagist API with local cache. Supports 22 scenes, quality scoring, and cross-references to laravel-docs-reader for official documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[relunctance](https://clawhub.ai/user/relunctance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to find, compare, and select Laravel packages for common application needs such as authentication, payments, queues, search, testing, AI integration, and administration. It returns ranked recommendations with rationale, Composer install commands, compatibility notes, and configuration examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package does not include the local PHP search helper that the skill tells agents to run. <br>
Mitigation: Use the skill as a static Laravel package reference unless the exact helper script path and source are separately verified before execution. <br>
Risk: Package recommendations may be based on external package metadata, cached results, or reference tables that can become stale. <br>
Mitigation: Verify candidate packages against Packagist, the package repository, and the target Laravel version before installing or deploying them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/relunctance/laravel-package-search) <br>
- [Scene Category Index](references/scene-index.md) <br>
- [Top 20 Laravel Packages](references/top20-packages.md) <br>
- [Packagist API search endpoint](https://packagist.org/api/search.json?q=) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with inline Composer commands and PHP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked package recommendations, alternatives, cautions, compatibility notes, Packagist links, and Laravel documentation cross-reference guidance.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
