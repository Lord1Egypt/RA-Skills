# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-18

### Fixed
- 重启逻辑改用 `--force` 强制重启
- 添加 .gitignore 忽略敏感配置

## [1.0.0] - 2026-03-18

### Added
- 初始版本发布
- 支持 Windows / Linux / macOS
- 自动检测 Gateway 状态
- 掉了自动重启
- 钉钉机器人通知
- 每日报平安功能

### Features
- ✅ 跨平台支持
- ✅ 钉钉加签验证
- ✅ 多种通知场景
- ✅ 开机自启配置

### Components
- `gateway_monitor.py` - 主程序
- `config.example.py` - 配置示例
- `README.md` - 使用说明
- `CHANGELOG.md` - 更新日志
- `ARCHITECTURE.md` - 架构文档

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本 |

## 计划功能

- [ ] 支持企业微信通知
- [ ] 支持 Telegram 通知
- [ ] 支持邮件通知
- [ ] Web UI 管理界面
- [ ] 支持多 Gateway 监控

---

🦞 小溪 - 2026-03-18
