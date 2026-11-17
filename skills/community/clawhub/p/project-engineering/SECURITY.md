# Security Policy

## Supported versions

安全修复仅保证进入最新发布版本。请始终安装 ClawHub 的 `latest` 或 GitHub `main` 的已发布版本。

## Reporting a vulnerability

请不要在公开 Issue 中提交 Token、私钥、内部仓库内容或可直接利用的敏感细节。使用 GitHub Security Advisory 的私密报告入口联系维护者；如果该入口暂不可用，只公开提交不含利用细节的通知，请求维护者建立私密沟通渠道。

报告建议包含：受影响版本、触发条件、潜在影响、最小安全复现和建议修复。维护者会先确认接收，再根据风险安排修复与披露。

## Trust model

`project_inventory.py` 设计为只读扫描器，不执行目标仓库的构建、包管理脚本或项目代码。安装任何第三方 Skill 前，仍应审阅 `SKILL.md`、脚本、权限声明和发布来源。
