## Description: <br>
Helps an agent issue, cancel, and retrieve accounting reports for São Paulo NFS-e service invoices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Blackcoffee111](https://clawhub.ai/user/Blackcoffee111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and their agents use this skill to prepare, issue, cancel, and export reports for São Paulo municipal NFS-e invoices. The workflow supports local configuration, customer records, certificate-backed SOAP calls, and human review before production tax actions. <br>

### Deployment Geography for Use: <br>
Brazil (São Paulo municipal NFS-e system) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real São Paulo municipal tax operations, including invoice issuance and cancellation. <br>
Mitigation: Require explicit human confirmation before every production issue or cancel action. <br>
Risk: The skill handles certificate material, .env secrets, debug XML, stored customer records, and exported accounting JSON. <br>
Mitigation: Keep certificate and .env files out of synced or shared folders and source control, restrict file permissions, and periodically delete or protect debug and export files. <br>
Risk: The skill can prepare invoice links or accounting exports for email sharing. <br>
Mitigation: Confirm recipients and attachment contents before every email send. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Blackcoffee111/nota-fiscal-paulistana) <br>
- [São Paulo NFS-e SOAP endpoint](https://nfews.prefeitura.sp.gov.br/lotenfe.asmx) <br>
- [ACBr project reference](http://www.sourceforge.net/projects/acbr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown or text responses with shell commands, JSON command results, configuration updates, and exported accounting JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary RPS payload files, update local configuration and customer files, call municipal SOAP APIs, and produce invoice PDF links or accounting exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
