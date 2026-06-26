## Description: <br>
Run Pine Script indicators from the command line using pinets-cli for execution, testing, analysis, technical indicator calculations, and crypto market data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alaa-eddine](https://clawhub.ai/user/alaa-eddine) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, trading-tool builders, and technical analysts use this skill to run Pine Script indicators from files or stdin and inspect calculated plots, variables, and market-data-backed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external npm CLI package. <br>
Mitigation: Install pinets-cli only when its package and publisher are trusted, and pin versions where reproducibility matters. <br>
Risk: Pine Script files and piped stdin are executable analysis inputs. <br>
Mitigation: Run only reviewed indicators in a controlled environment, especially when handling third-party scripts. <br>
Risk: Indicator output can be misleading when a long-lookback calculation lacks enough warmup data. <br>
Mitigation: Use warmup values aligned to the longest indicator lookback and validate custom candle data before relying on results. <br>


## Reference(s): <br>
- [PineTS CLI homepage](https://github.com/QuantForgeOrg/pinets-cli) <br>
- [PineTS runtime](https://github.com/QuantForgeOrg/PineTS) <br>
- [ClawHub skill page](https://clawhub.ai/alaa-eddine/pinets) <br>
- [Publisher profile](https://clawhub.ai/user/alaa-eddine) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, JSON] <br>
**Output Format:** [Markdown with inline shell, Pine Script, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes quiet JSON output, warmup controls, plot filtering, custom candle data, and treating Pine Script input as executable.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
