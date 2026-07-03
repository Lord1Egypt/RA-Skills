HaluCatch 模块化拆分 — 设计决策说明

## 目录结构

halucatch/                    # 核心包
├── __init__.py               # 导出版本和核心 API（~15 行）
├── config.py                 # MESSAGES + detect_system_locale（~218 行）
├── scanner.py                # scan_folder + _extract_version + _strip_string_literals（~166 行）
├── classifier.py             # classify_skill（~16 行）
├── evaluators/               # 四维评估 + 自检
│   ├── __init__.py           # 聚合导出（~30 行）
│   ├── foundation.py         # check_foundation（~72 行）
│   ├── code_risks.py         # check_code_risks（~56 行）
│   ├── rules.py              # check_rules（~85 行）
│   ├── guardrails.py         # check_guardrails（~133 行）
│   └── methodology.py        # check_methodology（~66 行）
├── reporter.py               # generate_report（~262 行）
├── cli.py                    # parse_args + main（~88 行）
halucatch_core.py             # 向后兼容入口（~30 行，导入 cli.main）

## 设计原则

1. **零依赖**：所有模块仅使用 Python 标准库，不引入外部包。
2. **单一职责**：每个模块对应一个功能边界，模块内高内聚。
3. **AI 可复现**：单文件控制在 200 行以内，AI 可以完整理解每个模块。
4. **向后兼容**：halucatch_core.py 保留，所有现有用法不受影响。
5. **可扩展**：新增评估维度时，只需在 evaluators/ 下新建文件，evaluators/__init__.py 注册即可。

## 依赖关系

```
cli.py → reporter.py → evaluators/__init__.py → config.py
             ↑                        ↑
          scanner.py               classifier.py
```

所有模块都依赖 config.py（MESSAGES）。
scanner.py 和 classifier.py 无依赖。
reporter.py 依赖所有 evaluators 和 scanner 输出。
cli.py 是入口，协调所有模块。
