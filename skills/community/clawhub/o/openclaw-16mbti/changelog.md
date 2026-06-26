# 更新日志 (Changelog)

所有关于 `openclaw-16mbti` Skill 的重要变动均记录于此。本日志遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范，采用[语义化版本控制](https://semver.org/lang/zh-CN/)。

## [Unreleased]

- 等待上机测试与 prompt 微调反馈。

---

## [1.0.0] - 2026-03-09

### Added (新增)
- **核心逻辑接入 (SKILL.md)**：完成了中枢调用文件的设计，支持对 `task_mode` 和 `output_style` 的精确识别。
- **三种输出模式路由**：
  - 【单流派设定】 `single`
  - 【极性推演对立】 `compare`
  - 【系统智能发牌】 `recommend`
- **红线与免责阻断机制**：在配置文件底层强制写死“反医疗诊断”、“反招聘筛选”的高优阻断逻辑。
- **全系角色组件包 (profiles/)**：
  - NT 架构组 (INTJ, INTP, ENTJ, ENTP)
  - NF 价值组 (INFJ, INFP, ENFJ, ENFP)
  - SJ 稳健组 (ISTJ, ISFJ, ESTJ, ESFJ)
  - SP 临场组 (ISTP, ISFP, ESTP, ESFP)
- **机器可读索引配置**：生成了 `03_personality_profiles.json` 与 `.yaml` 以供外部流程调用。
- **配套帮助文档**：创建了 `README.md`，使用案例说明 `examples.md`，出厂测试验证标准 `tests.md`。

### Changed (变更)
- *无 (首次发布)*

### Fixed (修复)
- *无 (首次发布)*
