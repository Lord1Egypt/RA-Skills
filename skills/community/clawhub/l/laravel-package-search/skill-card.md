## Description:

Real-time Laravel package search via Packagist API with local cache. Supports 22 scenes, quality scoring, and cross-references to laravel-docs-reader for official documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find, compare, and select Laravel packages for common application needs such as authentication, payments, search, queues, testing, and AI integration. It returns ranked recommendations with reasoning, install commands, configuration snippets, and Laravel documentation cross-references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package recommendations may require outbound requests to Packagist or GitHub and may use locally cached search results.

Mitigation: Run the skill only where those network requests and local cache files are acceptable, and refresh or clear the cache when current package data is required.

Risk: The release evidence notes that the artifact does not contain the referenced search script.

Mitigation: Verify that the installed skill package includes the expected search script before relying on live search, comparison, or recommendation behavior.

Risk: Install commands and configuration snippets for third-party Laravel packages can affect application dependencies and runtime behavior.

Mitigation: Review selected packages, compatibility, and generated commands before applying them to a Laravel project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/relunctance/skills/laravel-package-search)
- [Scene Category Index](references/scene-index.md)
- [Top 20 Laravel Packages](references/top20-packages.md)
- [Packagist Search API](https://packagist.org/api/search.json?q=)
- [Packagist Package Search](https://packagist.org/search?q=laravel&type=library)
- [Official Laravel Packages](https://laravel.com/packages)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with package recommendations, inline composer commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations may depend on live Packagist or GitHub data and a local one-hour cache when the referenced search script is present.]

## Skill Version(s):

2.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
