## Description: <br>
查询指定出发站到到达站的火车班次信息，包括车次号、出发/到达时间、历时、票价和余票，并通过聚合数据（juhe.cn）API 实时查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up train schedules, booking availability, fare details, and filtered route options between Chinese railway stations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends train search details, including route, date, and filters, to Juhe. <br>
Mitigation: Use it only when sharing those query details with Juhe is acceptable for the user and use case. <br>
Risk: A Juhe API key is required and can be exposed if passed on shared command lines or stored insecurely. <br>
Mitigation: Prefer the JUHE_TRAIN_KEY environment variable or a protected .env file, and avoid passing the key as a command-line argument on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-train-tickets) <br>
- [Juhe train ticket query API documentation](https://www.juhe.cn/docs/api/id/817) <br>
- [Juhe Data](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and tabular train lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_TRAIN_KEY API key; queries include departure station, arrival station, date, and optional filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
