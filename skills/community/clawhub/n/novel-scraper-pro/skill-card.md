## Description: <br>
Novel Scraper Pro helps agents fetch web novel chapters, complete paginated chapters, resume interrupted runs, and save formatted TXT files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download public web novel chapters from supported sites, batch chapter ranges, verify continuity, and merge results into local TXT files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-supplied web pages and may save downloaded novel text plus progress files locally. <br>
Mitigation: Use it only for public, intended URLs and periodically clean output, progress, and cache directories on shared machines. <br>
Risk: Browser-based SPA mode can fetch pages with a larger execution and privacy surface than static page retrieval. <br>
Mitigation: Enable SPA/browser mode only for sites that require it and avoid private, internal, or authenticated URLs. <br>
Risk: Large batch downloads can consume disk space through TXT output, catalog files, progress state, and cache entries. <br>
Mitigation: Set bounded chapter ranges, monitor local storage, and remove stale generated files when runs complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuzhihui886/novel-scraper-pro) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Supported site selectors](artifact/configs/sites.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated TXT novel files and JSON progress or catalog files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves downloaded novel text, progress state, catalogs, and cache files locally.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence and changelog, released 2026-04-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
