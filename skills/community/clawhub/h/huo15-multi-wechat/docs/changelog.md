# Changelog

## 1.1.0 (2026-07-30)

- **核心修复**：新增可执行文件重命名步骤，修复 `open` 命令无法多开的问题
- **根因**：macOS Launch Services 按可执行文件名做缓存映射，副本可执行文件名与原版相同（都叫 `WeChat`）时，`open WeChat2.app` 被重定向到原版
- **方案**：重命名副本可执行文件（`WeChat` → `WeChat2`/`WeChat3`）并更新 `CFBundleExecutable` + 重新签名 + 注册 Launch Services
- 脚本新增 `lsregister` 重新注册步骤
- 更新 SKILL.md / README.md 原理说明，明确两层锁机制

## 1.0.0 (2026-07-30)

- 初次发布
- 通过复制完整微信应用 + 修改 CFBundleIdentifier + 重新签名实现多开
- 附带 `scripts/multi_wechat.sh` 脚本，支持创建任意数量副本
- 包含封号风险评估与注意事项文档
