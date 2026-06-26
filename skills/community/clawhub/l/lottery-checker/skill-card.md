## Description: <br>
中国体育彩票查奖工具（大乐透批量查询）。检查用户提供的大乐透号码是否中奖，支持单注或多注批量查询，自动生成精美报表，显示各奖项中奖人数和金额。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sudaqinnishui](https://clawhub.ai/user/sudaqinnishui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to check one or more China Sports Lottery Super Lotto tickets against the latest draw and view prize status, prize distribution, jackpot, and sales information. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Displayed draw results or prize amounts could be tampered with on a hostile network because the script accepts unverified HTTPS responses. <br>
Mitigation: Confirm winnings and prize amounts through an official lottery source before relying on the result. <br>
Risk: The tool is a convenience checker and is not authoritative for redemption decisions. <br>
Mitigation: Use local sports lottery sales points, lottery center announcements, or official channels for final redemption confirmation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sudaqinnishui/lottery-checker) <br>
- [Publisher profile](https://clawhub.ai/user/sudaqinnishui) <br>
- [China Sports Lottery API endpoint](https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry) <br>
- [China Sports Lottery](https://www.lottery.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one or more Super Lotto number strings and an optional JSON output flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
