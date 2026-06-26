## Description: <br>
Lightpanda Browser helps agents install and use the lightweight Zig-based Lightpanda headless browser for web scraping, content extraction, and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install Lightpanda, fetch web pages as HTML or Markdown, and integrate lightweight browser-based extraction into scraping, monitoring, and RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing a nightly browser binary or Docker image can introduce supply-chain risk. <br>
Mitigation: Prefer a pinned Lightpanda release when available and verify checksums or signatures if the project provides them. <br>
Risk: Web scraping can violate site terms or access restrictions. <br>
Mitigation: Scrape only sites you are authorized to access and keep robots.txt-aware fetching enabled where applicable. <br>
Risk: A running browser container or debugging endpoint can remain exposed after use. <br>
Mitigation: Bind local services to localhost when possible and stop or remove the Docker container after the task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/lightpanda) <br>
- [Lightpanda Linux nightly binary](https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux) <br>
- [Lightpanda macOS nightly binary](https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command examples for local binaries, Docker deployment, and page extraction to HTML or Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
