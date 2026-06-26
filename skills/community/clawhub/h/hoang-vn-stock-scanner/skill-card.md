## Description: <br>
Chuyen gia phan tich chung khoan Viet Nam (VN-Index, HoSE, HNX, UPCoM) dung de lay tin tuc thi truong tu CafeF va tra cuu chi so co ban cua ma co phieu Viet Nam qua TCBS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoanghust2003](https://clawhub.ai/user/hoanghust2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market analysts use this skill to retrieve recent Vietnamese stock-market news, filter rumor or insider-trading related headlines, and look up ticker fundamentals such as P/E, P/B, EPS, dividend yield, market capitalization, exchange, and industry. The skill helps an agent summarize those results and provide brief market-impact commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market news, rumors, and public ticker data can be inaccurate, incomplete, delayed, or market-sensitive. <br>
Mitigation: Treat returned market information as untrusted input, verify it against authoritative financial sources, and avoid presenting summaries as investment advice. <br>
Risk: The bundled scanner disables HTTPS certificate verification for its external requests. <br>
Mitigation: Confirm the command points to the bundled scanner on the user's machine, review network behavior before use, and consider enabling certificate verification in trusted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoanghust2003/hoang-vn-stock-scanner) <br>
- [CafeF market news RSS](https://cafef.vn/tin-tuc-su-kien.rss) <br>
- [TCBS public ticker overview endpoint](https://apipubaws.tcbs.com.vn/tcanalysis/v1/ticker/{ticker}/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-backed ticker or news summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ticker lookups require a Vietnamese stock ticker; news scans can optionally use comma-separated keywords.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
