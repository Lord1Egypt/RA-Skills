# 认证与权限体系

## 凭证文件

所有凭证统一放在 `~/.lark_tokens.json`，**不要**写在技能文件里。

```json
{
  "app_id": "cli_xxxxxxxxxxxxxxxx",
  "app_secret": "your_app_secret_here",
  "user_token": "your_user_access_token_here（可选）"
}
```

## 两种凭证的区别

| 凭证类型 | 获取方式 | 有效期 | 用途 |
|---------|---------|--------|------|
| App Token（tenant_access_token）| 自动用 app_id + app_secret换取 | 2小时，自动续期 | 大多数 API |
| User Access Token | OAuth 用户授权流程 | 2小时，可刷新 | 知识库、云文档搜索 |

## 凭证与工具对照

**只需 App Token（无需 OAuth）：**
- `im_v1_*`（消息）
- `contact_v3_*`（通讯录）
- `calendar_v4_*`（日历）
- `approval_v4_*`（审批）
- `card_v1_*`
- `bitable_v1_*`（多维表格）
- `drive_explorer_*`（云盘）
- `sheets_*`（电子表格）

**需要 User Token：**
- `wiki_v1_node_search`（知识库搜索）
- `wiki_v2_spaces`（知识库空间）
- `docx_builtin_search`（云文档搜索）
- `docx_v1_document_rawContent`（读云文档内容）

## 双层权限模型（重要）

飞书云文档（知识库/云文档）有两套独立权限系统，**必须同时满足**：

1. **应用权限**：飞书管理后台 → 应用 → 权限管理 → 申请对应 API 权限
2. **文档权限**：文档右上角「分享」→「添加应用」→ 搜索并添加应用为协作者

两者缺一不可！常见误区是只申请了应用权限，但文档本身没有把应用加为协作者。

## 常见权限错误排查

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `99991403` + 缺少应用权限 | API 权限未在后台申请 | 飞书管理后台 → 权限管理申请 |
| `99991403` + 文档权限 | 应用未被添加为文档协作者 | 文档「分享」中添加应用 |
| `99991403` + 用户相关 | User Token 未配置或过期 | 检查 `~/.lark_tokens.json` 中 user_token |

## 获取 User Token（OAuth 流程）

如果需要操作知识库或云文档，需获取 User Access Token：

1. 飞书开放平台 → 应用 → 安全设置 → 重定向 URL → 添加 `http://localhost:8080/callback`
2. 引导用户访问授权 URL（包含 scope 权限参数）
3. 用户授权后，飞书回调带 `code` 参数到你的服务器
4. 用 `code` 换取 `user_access_token`

详细步骤参考：[飞书 OAuth 文档](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/authen-v1/oidc-access-token/create)
