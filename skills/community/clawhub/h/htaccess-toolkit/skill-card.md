## Description: <br>
Generate, validate, lint, and explain Apache .htaccess files for redirects, security headers, caching, CORS, file protection, and configuration audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to create, lint, explain, and audit Apache .htaccess configuration for common web hosting tasks such as HTTPS redirects, CORS, caching, security headers, file protection, and WordPress hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .htaccess rules can break site access, redirects, CORS, caching, strict security headers, or HSTS behavior if deployed without review. <br>
Mitigation: Review generated output, keep a backup of existing server configuration, and test changes in staging before production deployment. <br>
Risk: Permanent redirects and HSTS settings may persist in browsers and caches after a mistake is corrected. <br>
Mitigation: Validate redirect and HSTS choices carefully before release, especially when enabling preload or broad permanent redirects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/htaccess-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown, JSON, and Apache .htaccess configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate .htaccess file content, lint findings, preset lists, and directive explanations; script output supports text, JSON, and Markdown modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
