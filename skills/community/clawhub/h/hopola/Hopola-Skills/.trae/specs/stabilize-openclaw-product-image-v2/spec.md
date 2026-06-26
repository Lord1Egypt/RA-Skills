# OpenClaw 商品图参考图稳定化 Spec

## Why
当前在 OpenClaw 场景下，参考图生成商品图存在高频失败，且商品图工具名与预期不一致（应使用 `image_praline_edit_v2`）。需要统一调用路径与前置校验，确保可稳定走通。

## What Changes
- 统一商品图固定工具为 `image_praline_edit_v2`，并移除旧工具名依赖。**BREAKING**
- 强化参考图输入归一化：显式 URL、会话上传图、本地缓存引用统一映射为可访问 URL。
- 新增“非链接图片先上传”门禁：当输入不是 URL 格式时，必须先调用上传子技能，成功后再进入商品图生成。
- 新增商品图调用前置校验（工具可用性、必填参数、图片可访问性、语言一致性）。
- 新增 OpenClaw 失败场景结构化错误输出与可执行重试建议。
- 更新主技能与商品图子技能文案，明确“商品图请求必须路由到 product-image 子技能并使用 v2 工具”。

## Impact
- Affected specs: 商品图生成路由、上传归一化、OpenClaw 集成稳定性、错误处理策略
- Affected code: `SKILL.md`、`subskills/product-image/SKILL.md`、`subskills/hopola-product-images/SKILL.md`、`config.template.json`、`examples.md`、`scripts/check_tools_mapping.py`

## ADDED Requirements
### Requirement: 参考图商品图稳定调用
系统 SHALL 在 `task_type=product-image` 或 `stage=generate-product-image` 时，保证参考图输入可被归一化并稳定进入商品图生成流程。

#### Scenario: 参考图 URL 成功生成
- **WHEN** 用户提供公网可访问的 `product_image_url`
- **THEN** 系统完成前置校验并调用商品图工具生成结果

#### Scenario: 会话图片自动补齐后生成
- **WHEN** 用户仅提供会话上传图片引用
- **THEN** 系统先上传并回填 URL，再进入商品图确认与生成

#### Scenario: 非链接图片先上传再生成
- **WHEN** 用户提供本地路径、附件引用、markdown 图片等非 URL 格式输入
- **THEN** 系统必须先调用上传子技能获取可访问 URL，上传成功后才允许进入生成阶段

#### Scenario: 参考图不可访问
- **WHEN** 参考图 URL 返回 4xx/5xx 或超时
- **THEN** 系统返回结构化错误，并提供重传或替换链接的重试建议

### Requirement: OpenClaw 调用前置校验
系统 SHALL 在调用商品图工具前执行 OpenClaw 兼容检查，避免无效请求进入远端工具。

#### Scenario: 工具不可用
- **WHEN** 工具发现结果中不存在 `image_praline_edit_v2`
- **THEN** 系统中断调用并输出“工具不可用”结构化错误

#### Scenario: 参数不完整
- **WHEN** 请求缺少 `image_list`、`prompt`、`output_format` 或 `size`
- **THEN** 系统中断调用并返回缺失字段列表

## MODIFIED Requirements
### Requirement: 商品图固定工具策略
系统 SHALL 将商品图固定工具从旧工具名迁移为 `image_praline_edit_v2`，并在主技能、子技能、配置和示例中保持一致。

#### Scenario: 常规商品图请求
- **WHEN** 用户触发商品图生成
- **THEN** 系统仅使用 `image_praline_edit_v2` 发起生成调用

## REMOVED Requirements
### Requirement: 使用旧商品图工具名
**Reason**: 旧工具名在 OpenClaw 侧稳定性与兼容性不足，导致失败率上升。  
**Migration**: 将所有商品图工具引用统一替换为 `image_praline_edit_v2`，并同步更新映射与校验脚本。
