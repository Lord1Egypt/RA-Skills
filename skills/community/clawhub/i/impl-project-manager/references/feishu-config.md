# 飞书应用配置

## 应用信息

- **应用名称：** 项目管理助手
- **App ID：** cli_aa9d0e7045f81cc8
- **App Secret：** oZ6exMRCZ9imHRkF28agUhxHFArbltk8

## 需要开通的权限

在飞书开放平台 → 应用详情 → 权限管理 中开通以下权限：

| 权限 | 权限标识 | 用途 |
|------|----------|------|
| 查看文档 | `docx:document:read` | 读取项目文档 |
| 编辑文档 | `docx:document:write` | 更新项目文档 |
| 查看表格 | `sheet:spreadsheet:read` | 读取项目数据表格 |
| 编辑表格 | `sheet:spreadsheet:write` | 更新计算字段和状态 |
| 表格全部权限 | `sheets:spreadsheet` | 创建表格、读写表格 |
| 云空间权限 | `drive:drive` | 设置表格分享权限 |

## 默认权限规则

所有新建表格自动设置为**组织内可编辑**（`link_share_entity: tenant_editable`），确保 PM 可直接在飞书客户端编辑表格数据。

设置方式：调用 `drive/v1/permissions/{token}/public?type=sheet` API，PATCH `link_share_entity` 为 `tenant_editable`。

## 操作步骤

1. 登录 https://open.feishu.cn/app
2. 进入刚创建的应用
3. 左侧菜单 → 权限管理 → 搜索以上权限并开通
4. 左侧菜单 → 版本管理 → 创建版本 → 申请发布
5. 等待管理员审批通过（个人账号自己是管理员，直接通过）

## Token 说明

- 使用 tenant_access_token（企业自建应用凭证）
- Token 有效期 2 小时，过期自动刷新
- 不使用 user_access_token，避免用户授权流程
