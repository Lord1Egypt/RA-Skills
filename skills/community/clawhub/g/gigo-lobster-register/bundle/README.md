# GIGO Lobster Taster v2 题包

50 题 agent 评测题包，配套 specs 与 harness 参考实现。

## 快速导航

- 总体设计：`../2026-04-24-lobster-eval-v2-design.md`
- 接入步骤：`INTEGRATION.md`
- 协议规范：`specs/`
- 题库：`tasks/`（50 个目录）
- 云端 rubric 包：`rubrics/`
- 参考 harness：`harness_reference/`
- CI 自检：`ci/`

## bundle_version

`v2.0.0`

云端排行榜按此版本号分桶，不同版本互不可比。

## 目录结构

```
bundle/
├─ README.md                  # 本文件
├─ INTEGRATION.md             # 研发接入步骤
├─ CHANGELOG.md
├─ specs/                     # 6 份协议文档
├─ tasks/                     # 50 个题目目录
├─ rubrics/                   # judge_rubric.md 单独打包给云端
├─ harness_reference/         # 参考实现，非产品代码
└─ ci/                        # 自检脚本
```

## 评分维度

| emoji | 维度 | 权重 | 评估方式 |
|---|---|---|---|
| 🥩 | 肉质（任务完成度） | 30% | pytest / state_hash |
| 🧠 | 脑子（规划推理） | 20% | pytest(goal) / llm_judge |
| 🦀 | 爪子（工具使用） | 15% | trace |
| 🛡️ | 壳（安全边界） | 15% | rule |
| 👻 | 灵魂（人格沟通） | 10% | llm_judge |
| 💰 | 钱包（成本） | 5% | 全局 token 聚合 |
| 🦵 | 脚力（速度） | 5% | 全局耗时聚合 |

## License

内部资料，不公开发行。
