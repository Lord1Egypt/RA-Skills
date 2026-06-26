# Tasks
- [x] Task 1: 对齐商品图工具名与路由约束
  - [x] SubTask 1.1: 将主技能与商品图子技能中的固定工具名统一为 `image_praline_edit_v2`
  - [x] SubTask 1.2: 更新配置映射与工具检查逻辑，确保仅校验/允许 `image_praline_edit_v2`
  - [x] SubTask 1.3: 更新示例与文档，避免出现旧工具名

- [x] Task 2: 强化参考图输入归一化与前置校验
  - [x] SubTask 2.1: 明确 URL/会话图/本地缓存输入的归一化顺序与回填规则
  - [x] SubTask 2.2: 对非 URL 输入强制先调用上传子技能，成功回填 URL 后再允许生成
  - [x] SubTask 2.3: 增加商品图调用前图片可访问性校验与参数完整性校验
  - [x] SubTask 2.4: 输出统一结构化错误与重试建议

- [x] Task 3: OpenClaw 回归验证与打包
  - [x] SubTask 3.1: 回归验证“公网 URL 成功、会话图成功、不可访问 URL 失败可重试”
  - [x] SubTask 3.2: 执行发布检查脚本并确认通过
  - [x] SubTask 3.3: 生成新发布包并核对产物可上传

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2

# 核验失败新增修复任务
- [x] Task 4: 统一商品图协议文档中的固定工具名
  - 说明：`subskills/hopola-product-images/SKILL.md` 仍出现旧工具名 `image_praline_edit_2_hoppa`，与目标 `image_praline_edit_v2` 不一致。

- [x] Task 5: 清理文档中的旧工具名残留并补充复核
  - 说明：因旧工具名仍在协议文档中出现，未满足“配置、文档、示例不再出现旧工具名”的核验要求。

- [x] Task 6: 补齐当前版本 OpenClaw 回归验证记录
  - 说明：现有 `RELEASE.md` 回归记录停留在 1.0.3，缺少本次版本（1.0.6）对应的 OpenClaw 场景回归结果。

- [x] Task 7: 修复发布检查失败并复跑打包验收
  - 说明：执行 `python3 scripts/validate_release.py` 失败，原因是 `scripts/__pycache__/maat_upload.cpython-314.pyc` 不允许进入发布产物。

- [x] Task 8: 修复商品图协议文档旧工具名残留
  - 说明：重新核验仍发现 `subskills/hopola-product-images/SKILL.md` 存在 `image_praline_edit_2_hoppa`（第 64/70/71 行），导致“固定工具名统一为 `image_praline_edit_v2`”及“文档不再出现旧工具名”未通过。
