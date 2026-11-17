## Description:

Searches cloud-drive resources across Baidu, Quark, Aliyun, 115, and other providers through a net-disk search API, with keyword filtering, link checks, and Docker deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godzx001-dot](https://clawhub.ai/user/godzx001-dot)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to deploy or connect to a net-disk search API, search cloud-drive resources by keyword and provider, and check shared link availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker deployment and network defaults may expose the search service or rely on mutable, unreviewed artifacts.

Mitigation: Pin the Docker image and skill source to reviewed digests or commits, bind the service to 127.0.0.1 by default, enable strong authentication before any remote exposure, and avoid --network host.

Risk: Deployment commands may execute constructed shell arguments or expose passwords in command output.

Mitigation: Remove eval from deploy.sh, avoid passing passwords in shell commands, and do not print passwords in deployment output.

## Reference(s):

- [NetDisk Search ClawHub page](https://clawhub.ai/godzx001-dot/skills/netdisk-search)
- [API reference](references/api-reference.md)
- [Upstream Pansou project](https://github.com/fish2018/pansou)
- [Upstream Pansou documentation](https://github.com/fish2018/pansou#readme)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON, Markdown tables, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and link-check results may include third-party share URLs and optional extraction codes returned by the configured API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
