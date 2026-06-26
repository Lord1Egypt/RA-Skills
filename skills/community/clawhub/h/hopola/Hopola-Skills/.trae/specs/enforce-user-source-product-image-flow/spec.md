# 商品图源图强约束 Spec

## Why
当前商品图链路在部分执行场景中未严格绑定用户上传/提供的商品源图，出现了“未使用用户图而自行生成参考图”的问题。需要将“缺图先询问、有图先上传、再用上传链接生图”变成不可绕过的硬门禁。

## What Changes
- 增加商品图前置门禁：未提供 `product_image_url` 且无可解析会话图片时，禁止调用任何商品图工具，必须先返回“请先提供商品图片”询问引导。
- 增加上传优先规则：用户给的是本地文件、会话图片、Markdown 图片或非公网 URL 时，必须先调用上传子技能并回填 `product_image_url`。
- 增加调用绑定规则：调用 `image_praline_edit_v2` 时，`args.image_list` 必须且只能包含“上传后得到的最终链接（或用户显式给出的公网源图链接）”。
- 增加防误生成规则：商品图任务严禁使用本地合成、占位图、文生图结果作为商品参考图替代。
- 增加可追溯输出：商品图响应必须包含 `tool_name_used`、`source_image_url_used`、`source_image_origin`、`precheck_report`。

## Impact
- Affected specs: 商品图意图识别与执行门禁、上传归一化、商品图工具调用约束、结果可追溯协议
- Affected code: `.trae/skills/Hopola/SKILL.md`、`.trae/skills/Hopola/subskills/product-image/SKILL.md`、`.trae/skills/Hopola/subskills/upload/SKILL.md`、`.trae/skills/Hopola/examples.md`、`.trae/skills/Hopola/scripts/validate_release.py`

## ADDED Requirements
### Requirement: 缺少商品源图时必须先询问
系统 SHALL 在任意商品图请求中检查是否存在可用商品源图输入；若不存在，系统只能返回询问与补充指引，不得进入生成。

#### Scenario: 用户未提供商品图片
- **WHEN** 用户仅输入“生成商品图”且未提供任何可用 `product_image_url` 或会话图片
- **THEN** 系统返回缺少商品图源图提示与下一步指引（上传商品图片或提供公网链接）
- **THEN** 系统不调用 `image_praline_edit_v2` 及任何替代生成工具

### Requirement: 非公网源图必须先上传再生成
系统 SHALL 对本地路径、会话附件、Markdown 图片引用、非公网 URL 先执行上传子技能，成功后再生成。

#### Scenario: 用户提供会话上传图片
- **WHEN** 用户提供会话图片但未给公网 URL
- **THEN** 系统先调用上传子技能并获得稳定可访问链接
- **THEN** 将该链接回填到 `product_image_url` 并作为后续唯一参考图链接

### Requirement: 参考图参数必须绑定上传结果链接
系统 SHALL 在调用 `image_praline_edit_v2` 前校验 `args.image_list` 与已确认源图链接的一致性。

#### Scenario: 生成调用参数校验通过
- **WHEN** 上传或显式公网源图校验通过，且用户确认使用该图
- **THEN** `tool_name_used` 为 `image_praline_edit_v2`
- **THEN** `args.image_list` 仅包含 `source_image_url_used`
- **THEN** 生成成功后输出可追溯字段 `source_image_url_used` 与 `source_image_origin`

#### Scenario: 调用参数与确认源图不一致
- **WHEN** `args.image_list` 包含非确认源图链接或为空
- **THEN** 返回结构化错误并终止调用

## MODIFIED Requirements
### Requirement: 商品图执行门禁
现有商品图执行门禁补充为：`source_image_confirmed=true` 仅表示“用户确认”，不能替代“源图可用链接已就绪”；两者必须同时满足后才可调用 `image_praline_edit_v2`。

## REMOVED Requirements
### Requirement: 本地替代生成兜底
**Reason**: 本地替代参考图会破坏用户商品一致性，导致“不是用户衣服”的错误结果。  
**Migration**: 统一迁移到“缺图询问 → 上传归一化 → 固定工具调用”链路，彻底移除本地/占位兜底路径。
