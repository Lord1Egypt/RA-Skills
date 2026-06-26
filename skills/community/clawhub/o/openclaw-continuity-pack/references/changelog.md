# Changelog

## v0.5.0 - 2026-04-03

- 以当前 workspace 维护中的 continuity source 为准重新整理分发包，并提升版本以覆盖已存在的 `0.4.0` registry release
- 补回根目录 `README.md`、`references/upgrade-maintenance.md` 与 `scripts/continuity_doctor.py`，让安装、升级巡检与维护路径重新完整
- 保留并重新分发当前 source 中已包含的 `assets/patch/thread-continuity.patch`、`LICENSE` 与 silent continuity / 80-85-88-90 文档体系
- 对齐 `SKILL.md`、`distribution.md` 与发布入口说明，使包内资源清单和实际文件结构一致

## v0.3.0 - 2026-03-30

- 将分发包同步到 Codex 已验证通过的 live continuity 行为
- 重新生成 `assets/patch/thread-continuity.patch`，对齐最新 runtime/UI 改动，并纳入 `src/gateway/thread-rollover.test.ts` source-side 对齐测试
- `assets/workspace/AGENTS.md` 与 `assets/workspace/SESSION_CONTINUITY.md` 改为 80/85/88/90 静默 continuity 策略，移除 `shorten prose` / `compact user update` / `convergence mode` 一类旧规则
- 更新 `overview / usage / install / verify / release-notes / distribution / files-to-replace`，明确普通聊天页不再显示 continuity/context 提示，且高-context 回答质量不再依赖“先缩短再切”

## v0.2.1 - 2026-03-29

- 新增 `scripts/install_continuity_pack.py` 作为统一安装入口，收口 workspace-only / continuity-only / full continuity 三条路线
- `bootstrap_workspace.py` 支持 `--workspace auto`，可从当前 workspace / 常见环境变量 / `~/.openclaw/workspace` 自动识别目标路径
- 安装文档与 `SKILL.md` 首屏改成优先使用统一安装脚本，并补充 ClawHub 安全提示说明
- 清理本地测试留下的 `__pycache__` 等临时产物，继续保持 source / package 脱敏

## v0.2.0 - 2026-03-29

- 将 source pack 收紧为更适合 ClawHub 分发的 skill 结构
- 新增 `agents/openai.yaml` 作为发布元数据入口
- 新增 `scripts/apply_runtime_patch.py`，把 patch 检查/应用/重建收成正式脚本
- `bootstrap_workspace.py` 新增 `--profile continuity`，支持只装 continuity 规则层
- 清理 `SKILL.md` 与发布文档中的本机视角描述，改成通用发布说明

## v0.1.0 - 2026-03-29

- 首次整理为可分发 continuity pack
- 提供可复用 workspace continuity 模板
- 提供脱敏后的 `openclaw.example.json`
- 提供仅包含正式运行时代码的 `thread-continuity.patch`
- 提供安装、部署、回滚、验证说明
- 明确区分正式运行时代码与验收辅助文件
