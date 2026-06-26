# ClawHub listing copy

## Product identity
m78armor : openclaw security configuration check

## Recommended slug
m78armor-security-check

## Recommended short pitch
Read-only local configuration review and hardening assessment for the OpenClaw instance itself. Finds baseline gaps, risky exposure, weak defaults, and drift indicators with operator-grade risk explanations. Not a network scanner.

本地只读 OpenClaw 配置检查与加固评估。识别基线缺口、暴露面、弱默认值与配置漂移，并给出面向运维人员的风险解释。不是网络扫描器。

## Recommended tags
openclaw, config, security-check, baseline, drift-check, hardening, local-first, bilingual, post-install

## Positioning line
This is a post-install configuration check and hardening assessment for the OpenClaw instance itself, not a target-network scanner.

这是面向 OpenClaw 实例自身的安装后配置检查与加固评估，不是目标网络扫描器。

## Suggested v1.0.0 changelog
Initial public release. Read-only local configuration review and hardening assessment for OpenClaw baseline gaps, risky exposure, weak defaults, and drift indicators. Supports --lang zh and --lang en with locale auto-detection fallback. Exit code 1 on high-risk findings for CI/pipeline integration. Includes --quiet flag for suppressing upgrade CTA in automated environments.

v1.0.0 首次公开发布。本地只读 OpenClaw 配置检查与加固评估，涵盖基线缺口、暴露面、弱默认值与配置漂移。支持 --lang zh 和 --lang en，自动区域检测回退。高风险发现时退出码为 1，支持 CI/流水线集成。包含 --quiet 标志用于自动化环境中抑制升级提示。

## Sample prompts
Use these sample prompts in OpenClaw after install:
- `run m78armor : openclaw security configuration check`
- `check this openclaw instance for risky security configuration gaps`
- `review local openclaw configuration baseline and hardening issues`
- `检查这个 OpenClaw 实例的安全配置问题`
- `执行本地 OpenClaw 配置基线与加固评估`
