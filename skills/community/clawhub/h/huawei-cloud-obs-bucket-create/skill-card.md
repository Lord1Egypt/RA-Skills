## Description: <br>
Skill specialized for creating buckets on Huawei Cloud OBS, including bucket name validation, region selection, access permission configuration, and batch bucket creation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to create Huawei Cloud OBS buckets, configure bucket properties such as region, ACL, and storage class, and troubleshoot common bucket creation failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose commands that create Huawei Cloud OBS resources with chosen bucket names, regions, ACLs, and storage classes. <br>
Mitigation: Review the exact bucket name, region, ACL, and storage class before running generated hcloud or batch creation commands. <br>
Risk: Credential handling may expose AK/SK values if users paste secrets into chat or shell history. <br>
Mitigation: Do not share real AK/SK values in chat; use local hcloud configuration and masked credential checks. <br>
Risk: Installer and initialization commands can modify local KooCLI or hcloud configuration. <br>
Mitigation: Verify the KooCLI installer source and back up existing hcloud configuration before rerunning initialization. <br>


## Reference(s): <br>
- [KooCLI Installation Guide](references/cli-installation-guide.md) <br>
- [Common Errors and Solutions](references/trouble-shooting.md) <br>
- [Huawei Cloud KooCLI Documentation](https://support.huaweicloud.com/cli-koocli/koocli_01_0001.html) <br>
- [Register Huawei Account and Complete Real-Name Authentication](https://support.huaweicloud.com/qs-hcli/hcli_02_002.html#hcli_02_002__section544111119366) <br>
- [Create IAM User and Authorize](https://support.huaweicloud.com/qs-hcli/hcli_02_002.html#hcli_02_002__section10273653161410) <br>
- [Get Access Key (AK/SK)](https://support.huaweicloud.com/qs-hcli/hcli_02_002.html#hcli_02_002__section10548184715361) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose hcloud/KooCLI commands and batch bucket creation script usage; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
