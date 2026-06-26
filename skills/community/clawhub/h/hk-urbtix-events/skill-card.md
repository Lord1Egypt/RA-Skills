## Description: <br>
Fetches and returns detailed Hong Kong URBTIX event performances by parsing natural language questions with date, venue, and event filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenho1394](https://clawhub.ai/user/stevenho1394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer natural-language questions about Hong Kong URBTIX performances, including event dates, times, venues, and official ticket links. <br>

### Deployment Geography for Use: <br>
Global, with outputs focused on Hong Kong URBTIX event information. <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the documented URBTIX/Tencent COS endpoint and stores cached public XML in the OpenClaw workspace. <br>
Mitigation: Deploy only in environments where that outbound request and local cache storage are acceptable. <br>
Risk: Ticketing and schedule information can change after the cached XML is fetched. <br>
Mitigation: Verify important purchases and attendance plans on the official URBTIX site before acting. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/stevenho1394/hk-urbtix-events) <br>
- [Publisher profile](https://clawhub.ai/user/stevenho1394) <br>
- [URBTIX batch XML distribution](https://fs-open-1304240968.cos.ap-hongkong.myqcloud.com/prod/gprd/URBTIX_eventBatch_YYYYMMDD.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Structured data] <br>
**Output Format:** [Markdown table answer plus JSON object containing matches and clarification status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include official ticket links, cached public XML lookup results, or a clarification message when the query cannot be matched.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and plugin metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
