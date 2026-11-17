# Contributing

感谢你帮助 Project Engineering 变得更可靠。

提交改动前请遵循以下原则：

1. 用真实、可复现的工程场景说明问题，不为单个偶发现象堆叠通用规则。
2. 保持 `SKILL.md` 精简；仅在特定模式需要的细节放入 `references/`。
3. 脚本必须默认安全、只读、无密钥，并避免执行目标仓库的代码或构建插件。
4. 新增规则应说明它改变了 Agent 的什么决策，以及为什么现有指导不足。
5. 运行全部测试，并在 Pull Request 中写明验证结果和兼容性影响。

```bash
python -m unittest discover -s scripts -p "test_*.py"
python scripts/project_inventory.py --repo . --format json
```

Bug 报告请包含最小复现场景、期望行为和实际行为，但不要上传私有源码、日志、Token 或其他敏感信息。
