# Tasks
- [x] Task 1: 收敛主技能商品图路由描述
  - [x] SubTask 1.1: 在 `SKILL.md` 明确商品图只能走 `subskills/product-image/SKILL.md`
  - [x] SubTask 1.2: 在执行规则中强调“不得绕过子技能直接触发工具”

- [x] Task 2: 强化商品图子技能源图硬门禁描述
  - [x] SubTask 2.1: 在 `subskills/product-image/SKILL.md` 明确每次调用都要校验 `source_image_confirmed=true`
  - [x] SubTask 2.2: 明确 `image_list` 只能是确认后的 `product_image_url`
  - [x] SubTask 2.3: 明确未满足时统一返回 `PRODUCT_IMAGE_UNCONFIRMED_SOURCE`

- [x] Task 3: 对齐固定协议文案与示例
  - [x] SubTask 3.1: 更新 `subskills/hopola-product-images/SKILL.md` 的确认门禁与调用约束
  - [x] SubTask 3.2: 更新 `examples.md`，增加“每次调用必须携带确认源图”的示例片段

- [x] Task 4: 执行文档一致性与回归校验
  - [x] SubTask 4.1: 运行发布校验脚本，确认门禁关键项检查通过
  - [x] SubTask 4.2: 人工复核关键文档中“源图不可替代”描述一致

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 3
