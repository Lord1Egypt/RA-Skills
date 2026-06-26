# Contributing / 贡献指南

Thanks for your interest in contributing! / 感谢你的贡献意愿！

---

## Development Setup / 开发环境

```bash
git clone https://github.com/xyva-yuangui/smartness-eval.git
cd smartness-eval

# Verify skill structure / 验证技能结构
python3 scripts/check.py

# Run a quick eval to confirm everything works / 确认评估可运行
python3 scripts/eval.py --mode quick --no-probes
```

**Requirements / 环境要求:**
- Python 3.9+
- No external packages needed (stdlib only) / 无需额外依赖

---

## What to Contribute / 可以贡献什么

| Area | Examples | 示例 |
|------|----------|------|
| **Scoring formulas** | Better metric blending, new evidence signals | 更好的指标融合方式 |
| **Test definitions** | New tests in `config/task-suite.json` | 新测试用例 |
| **Safety rules** | Stricter command validation patterns | 更严格的安全校验 |
| **Visualization** | HTML report, chart generation | 报告可视化 |
| **Documentation** | Translations, tutorials, examples | 翻译、教程、示例 |
| **Bug fixes** | Edge cases, fallback handling | 边界情况修复 |

---

## Pull Request Guidelines / PR 规范

### Keep PRs focused / 保持 PR 精简
One PR = one logical change. Avoid mixing unrelated changes.

### PR Checklist / PR 检查清单

- [ ] No unsafe command execution patterns introduced / 未引入不安全的命令执行
- [ ] No absolute-path assumptions / 未使用绝对路径
- [ ] No `exec()`, `eval()`, or `-c` patterns / 无动态代码执行
- [ ] `python3 scripts/check.py` passes / 健康检查通过
- [ ] `python3 scripts/eval.py --mode quick --no-probes` runs successfully / 快速评估可运行
- [ ] `CHANGELOG.md` updated if user-facing change / 用户可感知的变更需更新 CHANGELOG
- [ ] Documentation updated if needed / 如需要则更新文档

### Security-Specific Checklist / 安全专项检查

- [ ] New test commands only use `python3` interpreter
- [ ] All file paths are relative and within allowed prefixes
- [ ] No new external network calls unless explicitly opt-in
- [ ] No hardcoded credentials or API keys

---

## Commit Message Style / 提交信息规范

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add HTML report renderer
fix: handle missing cron-governor-report gracefully
docs: add Chinese translation for FAQ
test: add edge case for empty reasoning store
chore: update CI workflow to Python 3.12
security: block additional unsafe subprocess patterns
```

---

## Bug Reports / 提交 Bug

Please include / 请包含以下信息:

| Field | Description | 说明 |
|-------|-------------|------|
| **OpenClaw version** | e.g., 2026.3.13 | OpenClaw 版本 |
| **OS** | e.g., macOS 15.3, Ubuntu 24.04 | 操作系统 |
| **Python version** | e.g., 3.11.4 | Python 版本 |
| **Exact command** | Full command used | 完整命令 |
| **Error output** | Full traceback / stderr | 完整错误输出 |
| **Data context** | Which state files exist/missing | 状态文件情况 |

---

## Code Style / 代码风格

- Follow existing patterns in `eval.py`
- Type hints for function signatures
- Docstrings for public functions
- No external dependencies (stdlib only)

---

## Questions? / 有疑问？

Open an issue or start a GitHub Discussion. We're happy to help!

有问题请提 Issue 或在 GitHub Discussions 讨论，我们很乐意帮助！
