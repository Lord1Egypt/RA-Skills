## Description:

Configure Proxmint proxies in code and tools. Use when the user wants to route curl, Python (requests, httpx, aiohttp, Scrapy), Node.js, Go, Playwright, Puppeteer or Selenium traffic through Proxmint, choose between HTTP and SOCKS5, keep proxy credentials out of source code, or confirm which IP their requests exit from.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prian3003](https://clawhub.ai/user/prian3003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure HTTP or SOCKS5 Proxmint proxies in scripts, applications, crawlers, and browser automation, while keeping credentials in environment variables and checking the resulting exit IP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default examples place proxy credentials in an HTTP connection to the proxy gateway, which may expose the login to network observers.

Mitigation: Before using password authentication, ask the provider for a supported encrypted connection. Where appropriate, allowlist a fixed server IP and connect without sending a password; destination HTTPS alone does not protect proxy authentication.

## Reference(s):

- [Client snippets](artifact/references/clients.md)
- [Proxmint documentation](https://proxmint.com/docs)
- [Proxmint service status](https://proxmint.com/status)
- [ClawHub skill page](https://clawhub.ai/prian3003/skills/proxmint-proxy-setup)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configuration examples read credentials from environment variables and do not include actual passwords.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
