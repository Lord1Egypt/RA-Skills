## Description: <br>
Network Tools gives agents a unified interface for local command-line network utilities, including web fetches, downloads, DNS lookups, ping, traceroute, whois, IP checks, media downloads, proxy routing, and tool selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[savior-li](https://clawhub.ai/user/savior-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to retrieve web content, download files, inspect network paths, query DNS or whois data, check public IP routing, or use local proxy-aware tools without API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make outbound requests to user-supplied URLs and network diagnostic services, which can expose requested domains, hostnames, IP routing, or other sensitive targets. <br>
Mitigation: Use it only for intended destinations, avoid private URLs, tokens, cookies, and sensitive hostnames, and confirm proxy settings before sending requests. <br>
Risk: The skill can download files or media to local paths. <br>
Mitigation: Review and scan downloaded files before opening or executing them, and choose output paths deliberately to avoid unwanted overwrites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/savior-li/network-tools) <br>
- [README](README.md) <br>
- [Skill documentation](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Command-line text output, downloaded files, and Markdown guidance with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save user-directed downloads to local paths and may route supported commands through an optional local SOCKS5 proxy.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
