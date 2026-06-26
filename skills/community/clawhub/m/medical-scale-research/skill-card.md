## Description: <br>
医学量表信息检索与标准化报告生成。通过浏览器自动化检索量表背景、版权、CDISC 映射、统计方法等信息，生成飞书云文档并保存到量表知识库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinget-svg](https://clawhub.ai/user/kevinget-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical researchers, biostatisticians, medical research staff, and OpenClaw users use this skill to research medical scales, collect background and licensing information, recommend CDISC SDTM/ADaM mappings, and generate standardized Feishu reports for a knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may retrieve, store, or publish copyrighted medical scale instruments without enough user control. <br>
Mitigation: Require confirmation before downloads, screenshots, uploads, or Feishu publication, and verify each scale license permits local storage and cloud sharing. <br>
Risk: Feishu document and wiki permissions can expose generated reports or copied scale materials beyond the intended audience. <br>
Mitigation: Restrict Feishu destinations, sharing settings, and wiki locations before use. <br>
Risk: The artifact contains a hard-coded local download path for scale PDFs. <br>
Mitigation: Change the download path to an approved workspace location before running the skill. <br>
Risk: CDISC mappings and statistical recommendations may be incomplete or inappropriate for a specific protocol. <br>
Mitigation: Treat generated mappings and analysis code as draft guidance and have qualified clinical data standards and biostatistics reviewers confirm them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevinget-svg/medical-scale-research) <br>
- [Publisher profile](https://clawhub.ai/user/kevinget-svg) <br>
- [README](artifact/README.md) <br>
- [Scale report template](artifact/templates/scale-report.md) <br>
- [CDISC mapping rules](artifact/rules/cdisc-mapping.json) <br>
- [SGRQ example report](artifact/examples/SGRQ-example.md) <br>
- [CDISC](https://www.cdisc.org/) <br>
- [Mapi Research Trust](https://eprovide.mapi-trust.org/) <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown report, Feishu document link, knowledge-base archival confirmation, and inline SAS/R code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download or screenshot official scale materials, create Feishu cloud documents, archive reports to a knowledge base, and provide CDISC mapping recommendations that require human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
