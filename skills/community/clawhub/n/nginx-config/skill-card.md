## Description: <br>
Generates Nginx configuration guidance for reverse proxy, SSL/HTTPS, static serving, security hardening, caching, and optimization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to draft Nginx server, reverse proxy, SSL, static site, security hardening, and load-balancing configurations for review before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes an unrelated system-operations helper that can read host and log information and record local command-argument history. <br>
Mitigation: Review before installation; prefer the purpose-aligned scripts/nginx.sh generator, and avoid exposing scripts/script.sh as nginx-config unless it is renamed, documented, and its logging behavior is controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/nginx-config) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Nginx configuration and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated configurations may depend on user-provided domains, backend hosts, document roots, ports, certificate paths, and worker settings.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
