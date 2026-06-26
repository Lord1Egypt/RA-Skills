## Description: <br>
锁相环（PLL）PI 控制器参数计算工具，用于电力电子和新能源领域的锁相环设计与调试，支持从目标带宽和阻尼比计算 PI 参数，以及从已知 PI 标幺值参数反推闭环带宽和阻尼比。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncepuee](https://clawhub.ai/user/ncepuee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to tune and analyze SRF-PLL PI controller parameters for power electronics and renewable energy systems. It supports forward design from target bandwidth and damping ratio, and reverse analysis from known per-unit PI gains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Engineering results can be misleading if voltage, frequency, damping ratio, or units are assumed silently. <br>
Mitigation: Confirm Unom, f0, zeta, bandwidth, PI gain values, and units with the user before relying on calculated PLL parameters. <br>
Risk: The bundled MATLAB functions are stored as .txt files, which may not run directly as MATLAB function files. <br>
Mitigation: Rename or convert the script files to .m function files before execution and review the formulas for the target system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ncepuee/pll-designer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with formulas and MATLAB code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may ask for missing Unom, target bandwidth, or PI gain inputs before calculating; f0 and zeta defaults should be stated when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
