# 需求示例

做一个后台“文章管理”功能，支持列表、搜索、创建、编辑、删除。

字段：
- id: 主键
- title: 标题，必填
- content: 内容，必填
- status: 状态（draft,active），默认 active
- author_id: 作者ID，必填
- created_at: 创建时间
- updated_at: 更新时间

后台页面要求：
- 列表支持 where[id], like[title], where[status] 和创建时间 between
- 列表返回兼容当前 Admin layui table
- 提供弹窗编辑表单
