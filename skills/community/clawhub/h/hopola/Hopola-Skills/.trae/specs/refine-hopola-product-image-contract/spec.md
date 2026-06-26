# Hopola 商品图调用契约强化 Spec

## Why
当前商品图链路已具备源图门禁，但“必须走商品图 Skill”与“每次调用必须携带用户提供或确认的源图”在描述层仍不够集中、可执行性不够直观。需要统一主技能与子技能文案，降低调用歧义和回归风险。

## What Changes
- 强化主技能文档中的商品图路由描述，明确 `task_type=product-image` 只能进入商品图子技能链路。
- 强化商品图子技能与协议文档中的调用前置条件，明确每次工具调用都必须带入用户提供或确认的源图 URL。
- 统一“不可替代源图”描述，禁止占位图、代理图、模型生成图作为 `image_list` 输入。
- 补充结构化错误语义，确保未确认源图时统一返回 `PRODUCT_IMAGE_UNCONFIRMED_SOURCE`。
- 补充示例输入与确认卡片说明，体现 `source_image_confirmed` 与最终 `product_image_url` 的强绑定关系。

## Impact
- Affected specs: 商品图生成流程、商品图确认门禁、商品图错误处理规范
- Affected code: `.trae/skills/Hopola/SKILL.md`、`.trae/skills/Hopola/subskills/product-image/SKILL.md`、`.trae/skills/Hopola/subskills/hopola-product-images/SKILL.md`、`.trae/skills/Hopola/examples.md`

## ADDED Requirements
### Requirement: 商品图调用链路唯一入口
系统 SHALL 在 `task_type=product-image` 或 `stage=generate-product-image` 时，仅通过 `subskills/product-image/SKILL.md` 组织调用，不得绕过该子技能直接触发商品图工具。

#### Scenario: 路由成功
- **WHEN** 上游请求进入商品图阶段
- **THEN** 编排流程先进入商品图问询与确认门禁，再进入工具调用阶段

### Requirement: 每次商品图调用必须使用已确认源图
系统 SHALL 在每一次商品图工具调用前校验：`source_image_confirmed=true` 且 `image_list` 仅包含最终确认后的 `product_image_url`。

#### Scenario: 前置校验通过
- **WHEN** 用户已确认源图且 `product_image_url` 可访问
- **THEN** 系统构建 `image_list=[product_image_url]` 并允许调用 `image_praline_edit_v2`

#### Scenario: 前置校验失败
- **WHEN** 源图未确认或 `image_list` 不是确认源图
- **THEN** 系统停止调用并返回 `PRODUCT_IMAGE_UNCONFIRMED_SOURCE`

## MODIFIED Requirements
### Requirement: 商品图前置校验与错误码
系统 SHALL 在商品图调用前统一校验路由、源图确认、URL 可访问性和参数完整性。若校验失败，返回统一 `structured_error`，其中源图确认相关失败必须使用 `PRODUCT_IMAGE_UNCONFIRMED_SOURCE`，并包含可执行重试建议。

## REMOVED Requirements
### Requirement: 无
**Reason**: 本次为描述强化与约束收敛，不移除既有能力。
**Migration**: 无迁移动作，现有调用方按新增文案补齐确认字段与入参约束即可。
