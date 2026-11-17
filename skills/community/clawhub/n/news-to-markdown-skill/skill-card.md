## Description:

Converts article URLs into clean Markdown, with specialized extraction for 17 news and publishing platforms, optional image localization, and fallback fetching for dynamic pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflows use this skill to turn article URLs into Markdown for reading, archiving, summarization, or downstream publishing. It is commonly paired with a search skill that finds article URLs before this skill extracts each article body.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can execute a locally resolved npm package without independently verifying the installed package version or integrity.

Mitigation: Review the package before installing, install the pinned version explicitly, and run the skill in an isolated or low-privilege environment.

Risk: Floating npx examples can introduce package version drift at execution time.

Mitigation: Use the pinned npm install path for regular use and reserve npx only for disposable sandbox trials.

Risk: Running the launcher from an untrusted project directory may expose package resolution behavior to local dependency substitution.

Mitigation: Do not run the launcher from untrusted directories unless package resolution is fixed or the environment is isolated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipingme/skills/news-to-markdown-skill)
- [news-to-markdown npm package](https://www.npmjs.com/package/news-to-markdown)
- [news-to-markdown source repository](https://github.com/sipingme/news-to-markdown)
- [news-to-markdown audit entry point](https://github.com/sipingme/news-to-markdown/blob/main/src/index.ts)
- [browser-web-search companion skill](https://github.com/sipingme/browser-web-search-skill)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown text or Markdown files, optionally with downloaded image files and frontmatter metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article metadata, localized image paths, or no metadata when requested.]

## Skill Version(s):

3.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
