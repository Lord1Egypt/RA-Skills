## Description: <br>
Scan new meme coins for risks and opportunities, including honeypot detection, liquidity analysis, and holder concentration checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect meme-coin tokens, review liquidity and market signals, and collect checklist guidance before deciding whether deeper independent review is needed. Its outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an undocumented security utility with unrelated commands and local input logging. <br>
Mitigation: Review the bundled scripts before installation and avoid using scripts/script.sh for secrets, passwords, wallet data, API keys, or private text. <br>
Risk: Meme-coin scanner output may be mistaken for complete scam detection or financial advice. <br>
Mitigation: Use scripts/meme.sh only as an informational market-data aid and verify findings with independent scanners and manual contract review. <br>


## Reference(s): <br>
- [Meme Coin Scanner on ClawHub](https://clawhub.ai/bytesagain-lab/meme-coin-scanner) <br>
- [bytesagain-lab publisher profile](https://clawhub.ai/user/bytesagain-lab) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [DexScreener token API](https://api.dexscreener.com/latest/dex/tokens/{}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown-style guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces informational token analysis, market-data summaries, safety checklists, and external scanner links.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
