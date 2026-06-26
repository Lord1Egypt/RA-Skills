## Description: <br>
杰峰设备列表查询技能（开发版）。查询开发者账号下绑定的设备列表，支持分页查询和按设备序列号条件查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators with a JFTech Open Platform account use this skill to list bound devices, page through device records, or query up to 100 devices by serial number. <br>

### Deployment Geography for Use: <br>
China mainland, Asia, Europe, and North America <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose device passwords or login tokens in terminal output or JSON logs. <br>
Mitigation: Run it only in trusted terminals, avoid shared logs for JSON output, and rotate affected credentials if output may have been exposed. <br>
Risk: The API host is controlled by the JF_ENDPOINT environment variable. <br>
Mitigation: Set JF_ENDPOINT only to official JFTech API hosts before execution. <br>
Risk: Signed requests use developer-account credentials. <br>
Mitigation: Use credentials for an account you control and store JF_UUID, JF_APP_KEY, and JF_APP_SECRET outside shared shell history or committed files. <br>


## Reference(s): <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-device-list) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Text, JSON] <br>
**Output Format:** [Command-line output in simple text, table, or JSON formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JFTech credentials and may return device serial numbers, usernames, passwords, nicknames, and login tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
