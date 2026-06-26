# Retouch

## Overview

该 reference 只处理预设修图。
当前版本不覆盖 AI 修图、AI 追色、滤镜 / 换背景 / 去路人或智能裁剪。

## Tools

- `get_preset_suit_list`
- `apply_preset_suit`

## Preconditions

应用预设前，优先确认：

- 目标项目或项目图片上下文
- 目标图片范围
- 当前可用预设列表

如果项目或图片范围不清楚，先回 `projects.md`。

## Matching Policy

面对模糊修图诉求时：

1. 先获取 `get_preset_suit_list`
2. 基于预设名称、风格词、场景词做匹配
3. 如果存在一个明显高匹配预设，直接使用
4. 如果没有唯一高匹配预设，给用户 2 到 4 个候选

## Direct Apply

只有在以下情况才直接执行：

- 用户说的就是某个预设名，或与某个预设极接近
- 某个候选明显强于其他候选
- 不需要用户额外做审美判断

## Ask The User To Choose

以下情况应给出 2 到 4 个候选，让用户选择：

- 只说“修一下”
- 同时表达多个方向，例如“暖一点但保留通透”
- 有多个候选都合理

## Execution Rules

- 不看预设列表就不直接调用 `apply_preset_suit`
- 不编造预设名、预设 ID 或额外参数
- 目标图片不明确时，不默认对整个项目执行

## Out Of Scope

如果用户要的不是预设修图：

- 直接说明当前版本只支持预设修图
- 不顺带讲其他未暴露修图能力
