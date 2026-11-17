# Changelog

本文件遵循 semver-light：`patch`(x.y→x.y.1) = 修正 typo/补充说明；`minor`(x.y→x.y+1) = 新增步骤/场景/检查项；`major`(x.y→y.0) = 架构重构/流程重写。

## [1.1.0] — 2026-08-28

- **新增合规硬边界**：语料作者、文中人物及真实人名全部匿名化（v1.1.0 起）；输出契约强制虚构人物与化名，禁止真实人名及可识别的真实人物/机构/事件（见 `templates/output.md` 与 `honest-boundaries.md`）。
- 新增 `honest-boundaries.md`：语料溯源、证据等级、已知局限（单语料过拟合、题材依赖、人称未验证）与失败模式预告。
- 新增 `tests/adversarial.md`：6 条模糊修正对抗测试，强化 Style Drift 防御。
- 新增 `examples/positive.md` 与 `examples/negative.md`：正反仿写教学配对。

## [1.0.0] — 2026-08-27

- 初版发布：基于单篇现象级自述长文编译风格指纹、14 条创作原则、12 条启发法、10 条反模式、判断回路（Judge/Critique/Revision）与结构模板。
