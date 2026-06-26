# 功能列表模板（features.json）

```json
{
  "project": "示例项目名称",
  "created": "2026-03-18",
  "features": [
    {
      "id": "feat-001",
      "name": "用户认证 — 注册功能",
      "description": "用户可以通过邮箱和密码注册账号，注册后自动登录",
      "category": "functional",
      "priority": "high",
      "passes": false,
      "tests": [
        "打开注册页面，输入有效邮箱和密码",
        "点击注册按钮，验证跳转到主页",
        "验证数据库中已创建用户记录",
        "验证用户已自动登录（能看到用户菜单）"
      ],
      "notes": ""
    },
    {
      "id": "feat-002",
      "name": "用户认证 — 登录功能",
      "description": "已注册用户可以通过邮箱和密码登录",
      "category": "functional",
      "priority": "high",
      "passes": false,
      "tests": [
        "打开登录页面，输入已注册的邮箱和密码",
        "点击登录，验证跳转到主页",
        "验证侧边栏显示用户信息",
        "验证刷新页面后仍保持登录状态"
      ],
      "notes": ""
    },
    {
      "id": "feat-003",
      "name": "用户认证 — 密码重置",
      "description": "用户可以通过邮箱接收重置链接来修改密码",
      "category": "functional",
      "priority": "medium",
      "passes": false,
      "tests": [
        "点击'忘记密码'链接",
        "输入注册邮箱，验证收到重置邮件",
        "点击邮件中的链接，设置新密码",
        "用新密码登录验证成功"
      ],
      "notes": ""
    },
    {
      "id": "infra-001",
      "name": "数据库初始化",
      "description": "创建数据库 schema，包括用户表、会话表等",
      "category": "infra",
      "priority": "high",
      "passes": false,
      "tests": [
        "运行 init.sh 脚本",
        "验证数据库已创建",
        "验证所有表已存在且字段正确",
        "验证初始数据已插入"
      ],
      "notes": ""
    },
    {
      "id": "docs-001",
      "name": "API 文档",
      "description": "编写 REST API 的 OpenAPI/Swagger 文档",
      "category": "docs",
      "priority": "low",
      "passes": false,
      "tests": [
        "文档文件存在",
        "每个端点都有描述",
        "请求和响应示例完整"
      ],
      "notes": ""
    }
  ]
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| id | ✅ | 唯一标识符，格式：`feat-NNN`、`infra-NNN`、`docs-NNN`、`perf-NNN`、`fix-NNN` |
| name | ✅ | 功能简短名称 |
| description | ✅ | 功能详细描述，让 Agent 知道"完成"的标准 |
| category | ✅ | 分类：functional / infra / docs / perf / fix / research / writing / analysis |
| priority | ✅ | 优先级：high / medium / low |
| passes | ✅ | 是否完成并验证通过，Agent 只能改为 true，不可删改其他字段 |
| tests | ✅ | 验证步骤列表，Agent 必须全部通过才能将 passes 改为 true |
| notes | ❌ | 备注信息，Agent 可追加遇到的问题和解决方案 |

## Category 前缀

| Category | ID 前缀 | 用途 |
|----------|---------|------|
| 功能开发 | feat- | 业务功能 |
| 基础设施 | infra- | 环境、部署、数据库 |
| 文档 | docs- | 文档编写 |
| 性能 | perf- | 性能优化 |
| 修复 | fix- | Bug 修复 |
| 研究 | research- | 调研、可行性分析 |
| 写作 | writing- | 文案、报告撰写 |
| 分析 | analysis- | 数据分析任务 |
