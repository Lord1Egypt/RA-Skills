## Description: <br>
Generate .htaccess files for Apache web servers, including redirect rules, URL rewrites, security headers, HTTPS enforcement, IP blocking, caching rules, custom error pages, hotlink protection, and nginx-to-Apache conversions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to generate Apache .htaccess configuration for redirects, rewrites, security headers, HTTPS enforcement, caching, compression, CORS, IP blocking, error pages, directory indexes, and hotlink protection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated web-server configuration could accidentally overwrite an existing .htaccess file or change live-site behavior. <br>
Mitigation: Generate to stdout or a temporary file first, review the rules, and back up any existing .htaccess before using --output against a production path. <br>
Risk: Incorrect redirects, rewrites, CORS, caching, or security header choices can cause site outages, unexpected access changes, or misleading protection. <br>
Mitigation: Review generated directives against the target Apache modules and test them in a staging environment before production deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text Apache .htaccess configuration and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print generated configuration to stdout or write it to a specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
