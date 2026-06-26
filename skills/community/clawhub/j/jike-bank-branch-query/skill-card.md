## Description: <br>
银行支行、联行号查询；根据银行名称、省市代码、支行关键词查询支行名称、联行号、省份和城市，也支持查询银行列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to look up Chinese bank branch names, branch clearing numbers, province and city details, and matching bank lists through the Jike Data API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank and branch search terms are sent to the third-party Jike Data API. <br>
Mitigation: Install only if the deployment trusts jikeapi.cn and is comfortable sharing those lookup terms with that service. <br>
Risk: Passing the AppKey on the command line or storing unrelated secrets in the script directory .env file can expose credentials. <br>
Mitigation: Prefer the documented JIKE_BANK_BRANCH_QUERY_KEY environment variable and keep unrelated secrets out of the skill directory. <br>
Risk: Changing JIKE_API_BASE_URL can redirect requests to an unintended endpoint. <br>
Mitigation: Set JIKE_API_BASE_URL only when intentionally pointing the skill at a trusted API endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-bank-branch-query) <br>
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike Data bank branch query endpoint](https://api.jikeapi.cn/v1/bank/branch/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Terminal table or JSON, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JIKE_BANK_BRANCH_QUERY_KEY environment variable; can also use the generic JIKE_APPKEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
