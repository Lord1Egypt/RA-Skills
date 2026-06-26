# OpenClaw 上传合规加固 Spec

## Why
当前 OpenClaw 上传链路可用，但在 ClawHub 安装扫描中被标记为可疑，核心原因是凭证元信息不一致、外部上传策略端点暴露、请求日志默认过于详细。需要在不影响现有功能的前提下完成合规加固。

## What Changes
- 统一并明确凭证元信息，补齐主技能与上传子技能中的必需凭证说明，并处理历史命名兼容。
- 将外部上传策略端点改为“配置优先 + 安全约束 + 可审计说明”，避免硬编码造成审查风险。
- 调整请求日志策略为默认最小化输出，保留可控调试能力并强化敏感字段脱敏。
- 增加“兼容模式”要求：所有合规改动不得破坏现有搜索→生成→上传→报告主流程。

## Impact
- Affected specs: OpenClaw 凭证管理、上传策略获取、日志与审计策略、发布合规检查
- Affected code: `.trae/skills/Hopola/SKILL.md`、`.trae/skills/Hopola/README.zh-CN.md`、`.trae/skills/Hopola/config.template.json`、`.trae/skills/Hopola/subskills/upload/SKILL.md`、`.trae/skills/Hopola/scripts/maat_upload.py`

## ADDED Requirements
### Requirement: 凭证声明一致性与兼容性
系统 SHALL 在技能文档、模板配置、运行时代码中使用一致的凭证语义，并对历史字段提供兼容读取，不中断既有部署。

#### Scenario: 旧配置仍可运行
- **WHEN** 用户环境中仅配置历史凭证字段
- **THEN** 上传链路仍可成功获取策略并完成上传，同时输出一次性兼容提示而非失败

#### Scenario: 新安装按统一字段配置
- **WHEN** 用户按最新文档配置凭证
- **THEN** 不出现字段歧义，安装扫描可识别为声明清晰

### Requirement: 上传策略端点安全约束
系统 SHALL 对上传策略端点采用“可配置、可校验、可审计”的策略，默认值与文档保持一致，并提供主机级安全约束。

#### Scenario: 使用默认可信端点
- **WHEN** 用户未覆盖上传策略端点
- **THEN** 系统使用内置可信端点并正常上传

#### Scenario: 使用自定义端点
- **WHEN** 用户通过环境变量覆盖上传策略端点
- **THEN** 系统执行主机约束校验并记录结构化审计信息，不泄露敏感参数

### Requirement: 请求日志最小披露
系统 SHALL 将请求日志默认设置为关闭，仅在显式开启调试时输出，并确保请求头、token、策略与签名参数被脱敏。

#### Scenario: 默认运行
- **WHEN** 用户未开启调试日志
- **THEN** 上传链路不输出完整请求/响应明文，功能保持不变

#### Scenario: 调试运行
- **WHEN** 用户显式开启调试日志
- **THEN** 系统输出必要排障信息且敏感字段均为脱敏值

### Requirement: 功能无损兼容
系统 SHALL 在完成合规加固后维持“搜索→生成→上传→报告”现有功能行为与输入输出契约。

#### Scenario: 现有工作流回归
- **WHEN** 用户按现有调用方式执行技能
- **THEN** 产物上传成功率与失败时结构化错误行为不劣化

## MODIFIED Requirements
### Requirement: OpenClaw 上传日志策略
原有“可打印请求与响应用于排障”的能力调整为“默认关闭、显式开启、敏感字段强制脱敏、输出级别可控”。

## REMOVED Requirements
### Requirement: 默认详细请求日志输出
**Reason**: 默认详细日志会放大安装审查风险并可能暴露业务上下文信息。  
**Migration**: 改为默认关闭；需要排障时由用户显式开启调试开关，并沿用脱敏输出。
