# Hopola Skill 路由排查与修复计划

## Summary
- 目标：定位“商品图请求未走 `subskills/product-image/SKILL.md`”的根因，并修复 Skill 文档中导致可被绕过的约束缺口。
- 成功标准：自然语言商品图请求（如“帮我生成商品图，key:xxx”）在执行策略上只能进入商品图子技能链路；若条件不满足，返回结构化拦截错误而不是本地替代生成。

## Current State Analysis
- 主技能已声明商品图请求必须路由到商品图子技能，见 `Hopola/SKILL.md` 的规则段（`task_type=product-image` 或 `stage=generate-product-image` 必须进入子技能）。
- 商品图子技能已定义确认门禁、源图门禁、参数门禁和错误码，见 `Hopola/subskills/product-image/SKILL.md`。
- 但当前文档仍存在执行层可绕过空间：
  - 缺少“自然语言意图到 `task_type/stage` 的显式映射规则”，导致“帮我生成商品图”这类输入可能未先标准化到商品图路由。
  - 缺少“禁止本地脚本/PIL 等离线替代生成”的硬性规则，仅限制了不允许 create 工具替代商品源图。
  - 缺少“必须输出网关调用证据（工具名、调用回执字段）”的约束，导致链路可被静默替换而不易被发现。
  - 发布校验脚本 `scripts/validate_release.py` 仅检查关键 token 存在，不校验上述执行约束是否完整。

## Proposed Changes
- 文件：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/SKILL.md`
  - 增加“意图归一化路由规则”：凡用户表达“商品图/主图/详情图/场景图”等诉求，必须先标准化为 `task_type=product-image` 且进入 `stage=generate-product-image`。
  - 增加“禁止本地替代生成”规则：禁止使用本地脚本、PIL 或离线合成替代 Gateway + 子技能链路。
  - 增加“链路可审计性”规则：响应中需包含 `tool_name_used=image_praline_edit_v2` 与关键回执字段（不暴露密钥）。

- 文件：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/subskills/product-image/SKILL.md`
  - 增加“自然语言入口兼容说明”：当上游仅给自然语言请求时，先输出结构化确认卡并等待确认，不允许直接生成。
  - 增加“禁止绕过执行器”规则：若未满足确认/预检，必须返回 `structured_error`，不得走本地图像处理回退。
  - 增加“key 字段使用边界”：`key` 仅可作任务标识，不得替代源图确认、不得跳过门禁。

- 文件：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/examples.md`
  - 新增“纯自然语言商品图请求”示例（含 key 和会话上传图），展示正确分两轮：先确认卡、后生成调用。
  - 新增“错误示例”片段：未确认源图时的标准拦截输出。

- 文件：`/Users/youpengtu/Hopola-Skills/.trae/skills/Hopola/scripts/validate_release.py`
  - 扩展商品图门禁校验 token，确保新增约束（意图归一化、禁止本地替代、调用证据）在主技能和商品图子技能中均存在。
  - 目标是让发布前自动阻断“文档规则不完整”。

## Assumptions & Decisions
- 假设本次问题核心在 Skill 规范约束不够“可执行且可审计”，而不是网关工具不可用。
- 决策采用“文档约束 + 发布校验双保险”，避免再次出现执行层自由回退。
- 不在本次修复中变更业务工具映射（`image_praline_edit_v2` 仍是唯一商品图首选与固定工具链）。

## Verification
- 文档一致性检查：
  - 主技能与商品图子技能均包含“NL 意图归一化、禁止本地替代、证据回执”规则。
  - 示例覆盖“自然语言输入 + key + 会话图”的正确流程。
- 发布校验：
  - 运行 `scripts/validate_release.py`，确认新增校验项通过。
- 行为验收（人工演练）：
  - 输入“帮我生成商品图，key:xxx”时，第一轮应返回确认卡/补全字段请求；
  - 未确认源图时必须返回 `PRODUCT_IMAGE_UNCONFIRMED_SOURCE`；
  - 确认后才允许进入 `image_praline_edit_v2` 调用路径。
