## Description: <br>
Private Search routes OpenClaw web searches through privacy-respecting engines such as Brave Search, Kagi, or SearXNG, with configurable result counts and tracking-parameter stripping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u4ma-kev](https://clawhub.ai/user/u4ma-kev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure agent web searches to use Brave Search, Kagi, or SearXNG and strip tracking parameters from returned URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release makes broad private-search routing claims, while the security review notes that the package may not include the implementation needed to enforce those claims. <br>
Mitigation: Review the installed package behavior and independently verify that agent searches are routed through the intended provider before relying on privacy guarantees. <br>
Risk: The setup script writes search-provider credentials and configuration to an environment file. <br>
Mitigation: Review the target environment file before running setup, protect stored API keys, and rotate any key that may have been exposed. <br>


## Reference(s): <br>
- [Private Search on ClawHub](https://clawhub.ai/u4ma-kev/private-search) <br>
- [Privacy Search Engines Reference](references/privacy-engines.md) <br>
- [Brave Search API Documentation](https://api.search.brave.com/app/documentation/) <br>
- [Kagi API Documentation](https://help.kagi.com/kagi/api/) <br>
- [SearXNG Project](https://github.com/searxng/searxng) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRAVE_API_KEY for the default Brave configuration; KAGI_API_KEY or SEARXNG_URL can be used for alternate providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
