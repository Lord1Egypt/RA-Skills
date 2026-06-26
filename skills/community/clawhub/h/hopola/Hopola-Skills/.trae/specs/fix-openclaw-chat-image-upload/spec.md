# OpenClaw 对话图片上传兼容修复 Spec

## Why
用户在 OpenClaw 中使用最新技能包后，仍出现“对话图片上传失败”，且返回链接形态与本地实测不一致。需要统一上传输入与输出行为，避免渠道差异导致失败。

## What Changes
- 增加 OpenClaw 对话图片引用解析与归一化规则，兼容带双斜杠、渠道前缀路径与会话附件路径。
- 增加上传结果 URL 标准化规则，确保返回稳定且可访问的统一格式链接。
- 增加上传失败诊断信息规范，区分“输入解析失败 / 上传失败 / 可访问性校验失败”。
- 补充 OpenClaw 场景回归验证用例（单图、会话图、异常 URL）。
- **BREAKING**：上传阶段对非法或不可归一化 URL 将直接失败并返回结构化错误，不再静默兜底。

## Impact
- Affected specs: 上传子技能、会话图片归一化、上传结果返回规范
- Affected code: `subskills/upload/SKILL.md`、`SKILL.md` 上传规则段、`scripts/maat_upload.py`、上传调用与 URL 校验相关脚本/配置

## ADDED Requirements
### Requirement: OpenClaw 对话图片输入归一化
系统 SHALL 在上传前对 OpenClaw 对话图片引用执行统一归一化，输出可上传的本地文件路径或标准 URL。

#### Scenario: 会话图片引用可解析
- **WHEN** 输入包含 OpenClaw 会话图片引用（附件句柄、本地缓存路径、或渠道 URL）
- **THEN** 系统产出归一化后的上传输入，并记录来源类型

#### Scenario: 渠道 URL 含异常分隔符
- **WHEN** 输入 URL 存在重复斜杠或渠道特定路径前缀
- **THEN** 系统完成标准化并保持资源定位语义不变

### Requirement: 上传结果链接标准化与可访问性保证
系统 SHALL 对上传返回链接执行标准化与可访问性验证，仅返回稳定可访问链接。

#### Scenario: 上传成功且链接可访问
- **WHEN** MAAT 返回上传 URL
- **THEN** 系统返回标准化 URL，并通过 HEAD/GET 校验

#### Scenario: 上传成功但链接不可访问
- **WHEN** 上传结果 URL 校验失败
- **THEN** 系统返回结构化错误并给出重试建议，不返回不可用链接

## MODIFIED Requirements
### Requirement: 上传阶段处理 local/session 图片
系统 SHALL 在上传阶段统一处理 local/session 图片，并在 OpenClaw 渠道下执行输入归一化、上传、URL 标准化、可访问性校验四步流水。

## REMOVED Requirements
### Requirement: 宽松接收未标准化 URL
**Reason**: 宽松输入会在不同调用渠道产生不一致行为，导致“本地可用、线上失败”。  
**Migration**: 调用方应传入可归一化图片引用；若提供 URL，需满足标准格式或可被规则转换。
