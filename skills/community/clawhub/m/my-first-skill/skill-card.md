## Description: <br>
分析招标Excel文件，提取项目信息，存入MySQL数据库，并支持查询、时间跟踪和报告生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwh0709](https://clawhub.ai/user/zwh0709) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and agents use this skill to analyze tender files, import project records into MySQL, query upcoming deadlines, and generate tender-analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled database configuration uses root-style MySQL credentials and broad database authority. <br>
Mitigation: Replace the bundled credentials before use and run with a dedicated least-privilege MySQL account. <br>
Risk: The custom SQL option can modify or delete database data if unsafe SQL is entered. <br>
Mitigation: Disable or restrict custom SQL for normal users, and allow it only for operators who understand the database impact. <br>
Risk: Excel imports write to MySQL and can update existing tender records. <br>
Mitigation: Use a test database first, avoid production databases, and back up data before imports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zwh0709/my-first-skill) <br>
- [pandas documentation](https://pandas.pydata.org) <br>
- [MySQL Connector/Python documentation](https://dev.mysql.com/doc/connector-python/en/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Text or Markdown responses with Python command examples, MySQL configuration snippets, and optional Excel report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read Excel input files and write MySQL records or exported Excel reports when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
