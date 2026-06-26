# Tasks
- [x] Task 1: 收紧商品图前置门禁与询问流程
  - [x] SubTask 1.1: 在主技能明确“缺少商品图片仅询问，不得生成”
  - [x] SubTask 1.2: 在商品图子技能补充缺图结构化错误与提示模板

- [x] Task 2: 固化“先上传后生成”的入参归一化
  - [x] SubTask 2.1: 明确非公网输入必须调用上传子技能并回填 `product_image_url`
  - [x] SubTask 2.2: 明确上传失败时终止生成并返回可执行重试建议

- [x] Task 3: 强制绑定 image_praline_edit_v2 参考图参数
  - [x] SubTask 3.1: 增加 `image_list` 与确认源图链接一致性校验规则
  - [x] SubTask 3.2: 补充 `source_image_url_used`、`source_image_origin`、`tool_name_used` 输出要求

- [x] Task 4: 更新示例与发布校验规则
  - [x] SubTask 4.1: 在 examples 增加“缺图询问 / 上传后生成 / 错参拦截”示例
  - [x] SubTask 4.2: 在发布校验中增加关键字段与禁用本地替代路径检查

- [x] Task 5: 执行回归验证并记录结果
  - [x] SubTask 5.1: 验证“未给商品图被询问，不触发生成”
  - [x] SubTask 5.2: 验证“给任意商品会话图先上传，再以上传链接生成”
  - [x] SubTask 5.3: 验证“image_list 非确认链接时被拦截”

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 3
- Task 5 depends on Task 4
