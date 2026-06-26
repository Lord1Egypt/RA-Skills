## Description: <br>
Extracts structured product information, including model, quantity, price, currency, and images, from PDF quotations and product catalogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, catalog operators, and ecommerce teams use this skill to extract product rows and product images from PDF quotations or catalogs into structured outputs for review and downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local PDFs and can write extracted text, tables, images, and spreadsheets to disk; catalog layout errors may also produce incorrect extracted product data. <br>
Mitigation: Use PDFs you are comfortable processing locally, verify output paths, install required Python PDF/image/spreadsheet libraries in a controlled environment, and manually review extracted products, prices, currencies, and image matches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/newton-quotation-pdf-extraction) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with Python code and local extraction outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce extracted text, images, tables, Excel files, and structured product records depending on the PDF workflow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
