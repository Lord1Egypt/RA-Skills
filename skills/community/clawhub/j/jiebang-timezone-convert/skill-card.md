## Description:

时区转换工具，提供全球时区查询和时间转换功能，当用户需要时区转换、世界时钟、不同时区时间对比、时差计算、UTC 转换或跨时区会议时间时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebang-tools](https://clawhub.ai/user/jiebang-tools)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to query current time in named time zones, convert times between time zones, compare time differences, and plan meetings across regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timezone inputs are sent to the external jiebang.site service.

Mitigation: Use the skill only when users are comfortable sending the requested time and timezone values to that service, and document the remote domain and transmitted data before deployment.

Risk: The skill uses an admin-named Jiebang credential.

Mitigation: Replace the admin key with a narrowly scoped token and restrict runtime access to only the credential needed for timezone conversion and lookup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiebang-tools/skills/jiebang-timezone-convert)
- [Jiebang service endpoint](https://www.jiebang.site)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns converted time and timezone information from an external service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
