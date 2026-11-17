# 自带 Azure 应用注册指南

> 仅当不使用**内置默认应用**、想注册自己的 Azure 应用时阅读本节；其余情况可跳过。
>
> 背景：本工具的登录采用"设备码流程"——终端显示一个验证码，在浏览器中打开 microsoft.com/link 输入后完成授权。默认应用已内置该流程的全部配置；自带应用只需注册并提供一个 Client ID。

## 为什么需要 Client ID

- **Client ID（应用程序 ID）**：应用在微软身份体系中的唯一标识。设备码登录仅需要此项。
- **不需要 Tenant ID / Client Secret**：这两者仅用于"服务器后台无人值守"场景（机密客户端）。本工具采用公共客户端 + 设备码流程，任何要求填写这两项的界面均可忽略。

## 注册步骤

1. 打开 https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
2. 使用 Outlook 账户登录
3. **新建注册** → 填写应用名称 → 账户类型选择 **"仅个人 Microsoft 帐户"**
4. **身份验证** → 添加平台 → **"移动和桌面应用程序"** → 勾选 `https://login.microsoftonline.com/common/oauth2/nativeclient`
5. 身份验证页底部 → **"允许公共客户端流"** → 设为 **"是"** → 保存
6. **API 权限** → 添加权限 → Microsoft Graph → 委托权限 → 依次添加三个权限：`User.Read`、`Calendars.ReadWrite`、`MailboxSettings.Read`（各自的用途见 `configuration.zh-CN.md` 的连接步骤表）
7. 回到 **概览** 页，复制顶部 **"应用程序(客户端) ID"**

## 认证

从项目根目录运行。

```bash
python scripts/outlook_setup.py <你的Client ID>
```

之后的流程与默认应用完全一致：脚本打印验证码 → 浏览器打开 `https://www.microsoft.com/link` 输入 → Outlook 账户授权。token 自动续期。

## 常见失败

| 症状 | 原因与解决 |
|------|-----------|
| 设备码报"找不到应用" | 账户类型未选择"个人 Microsoft 帐户"，或"允许公共客户端流"未开启 |
| 403 Forbidden | `Calendars.ReadWrite` 委托权限未添加 |
| 验证码过期 | 重新运行 `python scripts/outlook_setup.py` 再试一次 |
