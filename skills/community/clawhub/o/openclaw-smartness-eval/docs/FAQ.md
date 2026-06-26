# FAQ / 常见问题

---

## General / 基础问题

### Q: What is this project? / 这个项目是什么？

**EN:** OpenClaw Smartness Eval is a 12-dimension evaluation framework for measuring AI agent intelligence. It combines automated task tests, real runtime telemetry, and anti-gaming probes to produce a structured, reproducible score.

**CN:** OpenClaw Smartness Eval 是一个 12 维度的 AI Agent 智能评估框架。它通过自动化测试、真实运行数据和反作弊探针，输出结构化、可重复的智能度评分。

---

### Q: Do I need OpenClaw to use this? / 必须用 OpenClaw 才能使用吗？

**EN:** The evaluation engine (`eval.py`) reads state files and scripts from an OpenClaw workspace. Without a workspace, the tests will find no data and scores will use fallback defaults. However, you can study the framework design (rubrics, formulas, architecture) for your own evaluation system.

**CN:** 评估引擎需要读取 OpenClaw 工作区的状态文件和脚本。没有工作区的话，测试会找不到数据，分数会使用默认值。但你可以参考框架设计（评分量表、公式、架构）来构建自己的评估系统。

---

### Q: What Python version is required? / 需要什么 Python 版本？

**EN:** Python 3.9 or higher. The project uses only the Python standard library — no external packages needed.

**CN:** Python 3.9 或更高版本。项目仅使用 Python 标准库，无需安装额外依赖包。

---

### Q: What operating systems are supported? / 支持什么操作系统？

**EN:** macOS and Linux. Windows is not officially supported but may work with minor path adjustments.

**CN:** macOS 和 Linux。Windows 未正式支持，但做少量路径调整后可能可用。

---

## Evaluation / 评估相关

### Q: Why does my score fluctuate between runs? / 为什么每次评分有波动？

**EN:** Several factors cause minor fluctuations:
- **Time window**: Different data falls in/out of the 3/7/30-day window
- **Anti-gaming probes**: Randomly generated inputs vary each run
- **Runtime state**: Real metrics change as the workspace operates

Use `deep` mode with repeated runs to get a confidence interval that quantifies this variance.

**CN:** 几个因素会导致小幅波动：
- **时间窗口**：不同数据随时间进出 3/7/30 天窗口
- **反作弊探针**：每次随机生成不同输入
- **运行状态**：真实指标随工作区运行变化

使用 `deep` 模式重复运行可获得置信区间来量化这种方差。

---

### Q: What does `--llm-judge` send externally? / `--llm-judge` 会发送什么数据？

**EN:** Only a summary of dimension scores, key evidence metrics, and risk flags. **No raw logs, user messages, or personal data** are sent. The feature is off by default and requires:
1. Explicit `--llm-judge` flag
2. A valid `DEEPSEEK_API_KEY` or `OPENAI_API_KEY` environment variable

**CN:** 仅发送维度分数摘要、关键证据指标和风险标记。**不会发送原始日志、用户消息或个人数据**。该功能默认关闭，需要：
1. 显式传入 `--llm-judge` 参数
2. 设置 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY` 环境变量

---

### Q: How are anti-gaming probes different from regular tests? / 反作弊探针和普通测试有什么区别？

**EN:** Regular tests are deterministic — same inputs every time. Anti-gaming probes inject randomized inputs at evaluation time to test whether the agent can handle novel scenarios, preventing overfitting to known test cases.

**CN:** 普通测试是确定性的——每次输入相同。反作弊探针在评估时注入随机输入，测试 Agent 能否处理未知场景，防止针对已知测试的过拟合。

---

### Q: What happens if some data files are missing? / 如果缺少某些数据文件会怎样？

**EN:** The evaluation engine handles missing files gracefully. Each missing data source gets a fallback default value (usually 0 or empty). The evaluation will still produce a score, but affected dimensions will be lower. No crashes.

**CN:** 评估引擎会优雅处理缺失文件。每个缺失的数据源会使用默认回退值（通常为 0 或空）。评估仍会生成评分，但受影响的维度分数会偏低。不会崩溃。

---

### Q: Can I add custom dimensions? / 能添加自定义维度吗？

**EN:** Not yet in v0.2.x. Custom dimension plugins are planned for v1.0 (see [ROADMAP.md](./ROADMAP.md)). For now, you can adjust existing dimension weights in `config/config.json` and modify rubric descriptions in `config/rubrics.json`.

**CN:** v0.2.x 版本暂不支持。自定义维度插件计划在 v1.0 实现（见 [ROADMAP.md](./ROADMAP.md)）。目前可以在 `config/config.json` 中调整现有维度权重，在 `config/rubrics.json` 中修改评分描述。

---

## Security / 安全相关

### Q: Is it safe to run test commands? / 运行测试命令安全吗？

**EN:** Yes. All test commands pass through `validate_command()` before execution:
- Only `python3` interpreter is allowed
- Inline code (`-c`, `exec(`) is blocked
- Absolute paths and path traversal (`..`) are rejected
- Only whitelisted path prefixes are permitted

Any command that fails validation is blocked and recorded as `BLOCKED_UNSAFE_COMMAND`.

**CN:** 安全。所有测试命令在执行前经过 `validate_command()` 校验：
- 仅允许 `python3` 解释器
- 禁止内联代码（`-c`、`exec(`）
- 拒绝绝对路径和路径穿越（`..`）
- 仅允许白名单路径前缀

未通过校验的命令会被阻止，并记录为 `BLOCKED_UNSAFE_COMMAND`。

---

### Q: Does this tool make network requests? / 这个工具会发起网络请求吗？

**EN:** **Not by default.** The only network feature is `--llm-judge`, which must be explicitly enabled. All other functionality is completely offline.

**CN:** **默认不会。** 唯一的网络功能是 `--llm-judge`，必须显式启用。其他所有功能完全离线运行。

---

## Contributing / 贡献相关

### Q: How can I contribute? / 如何参与贡献？

**EN:** See [CONTRIBUTING.md](../CONTRIBUTING.md). Good first contributions:
- Improve scoring formulas with better metrics
- Add new test definitions to `config/task-suite.json`
- Improve report visualization
- Translate documentation

**CN:** 详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。推荐的首次贡献方向：
- 用更好的指标改进评分公式
- 在 `config/task-suite.json` 中添加新测试
- 改进报告可视化
- 翻译文档

---

### Q: How do I report a security issue? / 如何报告安全问题？

**EN:** See [SECURITY.md](../SECURITY.md). Please report security vulnerabilities privately via GitHub Security Advisories rather than public issues.

**CN:** 详见 [SECURITY.md](../SECURITY.md)。请通过 GitHub Security Advisories 私密报告安全漏洞，而非公开 Issue。
