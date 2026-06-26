## Description: <br>
Converts article URLs into clean Markdown, with optimized extraction for major news and content platforms, optional image localization, and workflows that can pair with browser-web-search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflows use this skill to fetch user-provided article URLs, extract readable article bodies, and produce Markdown outputs for summarization, archiving, or downstream publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party npm package for article conversion. <br>
Mitigation: Install the fixed package version through the launcher path, audit the package source before use, and avoid the npx fallback for routine workflows. <br>
Risk: Fetching user-provided URLs and saving Markdown or images can bring untrusted remote content into the local workspace. <br>
Mitigation: Use trusted URLs, keep outputs in scoped directories, and review generated Markdown and downloaded images before reuse or publication. <br>
Risk: Dynamic-page support through Playwright or broad article scraping can expand browser, network, and filesystem exposure. <br>
Mitigation: Run Playwright or broad scraping in a sandbox or container, and install browser binaries only when dynamic rendering is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sipingme/news-to-markdown-skill) <br>
- [news-to-markdown GitHub](https://github.com/sipingme/news-to-markdown) <br>
- [news-to-markdown npm Package](https://www.npmjs.com/package/news-to-markdown) <br>
- [browser-web-search Skill](https://github.com/sipingme/browser-web-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown, optional local image files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write Markdown files and downloaded images locally when output flags are used.] <br>

## Skill Version(s): <br>
3.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
