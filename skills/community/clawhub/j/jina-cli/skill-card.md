## Description: <br>
Reads web content and searches the web using Jina AI Reader API. Use when extracting content from URLs, reading social media posts (X/Twitter), or web searching for current information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackfeng0614-prog](https://clawhub.ai/user/jackfeng0614-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to read web pages, social posts, and web search results through Jina AI Reader and Search. It helps convert public web content into JSON, Markdown, plain text, HTML, or screenshot links for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow uses a remote shell installer and downloads a Jina CLI binary. <br>
Mitigation: Install only when the GitHub installer and binary source are trusted, and inspect the installer before execution in sensitive environments. <br>
Risk: Forwarding browser cookies can expose authenticated session data to the CLI and Jina service. <br>
Mitigation: Use public URLs and searches by default; pass cookies only when credential forwarding is intentional and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackfeng0614-prog/jina-cli) <br>
- [Jina CLI install script](https://raw.githubusercontent.com/geekjourneyx/jina-cli/main/scripts/install.sh) <br>
- [Jina Reader API endpoint](https://r.jina.ai/) <br>
- [Jina Search API endpoint](https://s.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [CLI output as JSON or Markdown, with optional text, HTML, or screenshot URL response formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read batches of URLs from a file and may save extracted content to an output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
