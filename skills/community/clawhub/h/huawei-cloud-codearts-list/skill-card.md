## Description:

Lists Huawei Cloud CodeArts projects, repositories, pipelines, and deployment tasks through read-only APIs, with filtering, paging, and table or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers can inventory CodeArts resources in a selected Huawei Cloud region and project, then review the results as a table, JSON, or a compact name and ID list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SDK fallback reads Huawei access keys from environment variables into process memory.

Mitigation: Use a read-only Huawei identity, keep credentials out of chat, and run the skill in an environment you trust.

Risk: Command-override variables can change the CLI executable or inject arguments, and the write-intent guard does not sandbox replacement programs.

Mitigation: Leave command-override variables unset unless you have reviewed and trust their configuration.

Risk: The installer download and live cloud behavior or downloaded dependencies have not been independently verified by the supplied security evidence.

Mitigation: Verify installer downloads against Huawei-published checksums and confirm the intended region and project before querying.

## Reference(s):

- [KooCLI official quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Verification method and API details](artifact/references/verification-method.md)
- [Least-privilege IAM policies](artifact/references/iam-policies.md)
- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Full-field table, raw JSON array, or compact name and ID inventory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can be filtered by resource, region, project, name, and status; results are paged automatically.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
