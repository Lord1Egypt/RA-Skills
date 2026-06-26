# Microsoft Outlook Skill - 世纪互联版安装指南

本文档帮助你完成 OpenClaw Outlook Skill 的完整配置，支持世纪互联（21Vianet）版 Microsoft 365。

---

## 步骤概览

```
在 Azure 世纪互联门户注册应用（15分钟）
        ↓
配置 API 权限（委托权限）
        ↓
配置身份验证（启用公共客户端流）
        ↓
配置环境变量
        ↓
运行授权流程（首次）
        ↓
完成 ✅
```

---

## 第一步：在世纪互联 Azure 门户注册应用

### 1.1 访问 Azure 世纪互联门户

打开：**https://portal.azure.cn/**

用你的管理员账号登录。

### 1.2 注册新应用

1. 左侧菜单 → **Microsoft Entra ID**（旧称 Azure Active Directory）
2. 左侧 → **应用注册**
3. 点击 **+ 新建注册**
4. 填写：
   - **名称**：`OpenClaw Outlook`（任意）
   - **支持账户类型**：选择"**仅此组织目录中的账户**"（重要！）
   - **重定向 URI**：留空，后面再填

5. 点击**注册**

### 1.3 记录重要信息

注册完成后，在**概述**页面复制并记录：

```
Application (client) ID：← 这是你的 OUTLOOK_CLIENT_ID
Directory (tenant) ID：  ← 这是你的 OUTLOOK_TENANT_ID
```

### 1.4 创建 Client Secret

1. 左侧菜单 → **证书和密码**
2. 点击 **+ 新建客户端密码**
3. 添加说明（如 `OpenClaw Skill`）
4. 选择过期时间（建议 24 个月）
5. 点击**添加**
6. **立即复制**生成的密码值（只显示一次！）

> ⚠️ 这个密码值就是你的 `OUTLOOK_CLIENT_SECRET`

### 1.5 配置 API 权限（委托权限）

> ⚠️ **重要**：本 Skill 使用设备码流（Device Code Flow）实现用户自行授权，需要**委托权限**，不是应用程序权限！

1. 左侧菜单 → **API 权限**
2. 点击 **+ 添加权限**
3. 选择 **Microsoft Graph**
4. 选择**委托权限**（不是应用程序权限！）
5. 搜索并添加以下权限：

**邮件权限：**
- `Mail.ReadWrite` - 读取和写入邮件
- `Mail.Send` - 发送邮件

**日历权限：**
- `Calendars.ReadWrite` - 读取和写入日历

**其他：**
- `User.Read` - 读取用户信息
- `offline_access` - 获取刷新令牌（必需！）

6. 搜索每个权限 → 勾选 → 点击**添加权限**

7. 重要：找到你刚添加的权限，点击 **授予管理员同意**（Grant admin consent）

### 1.6 配置身份验证（关键步骤！）

> ⚠️ **此步骤至关重要**，必须按以下说明配置才能正常使用设备码流！

1. 左侧菜单 → **身份验证**
2. 找到 **"高级设置"** 部分
3. **勾选** "允许公共客户端刷新令牌流"（启用以下移动和桌面流）
   - 或者找到 "将应用程序视为公共客户端" 设置为 "是"
4. 点击 **保存**

配置示意：

![核心配置](./核心配置.png)

### 1.7 配置平台（重定向 URI）

1. 点击 **+ 添加平台**
2. 选择**移动和桌面应用程序**
3. 选择**公共客户端/原生客户端**
4. 重定向 URI 填入：
   ```
   http://localhost:8080
   ```
5. 点击**配置**

---

## 第二步：配置环境变量

### 2.1 设置环境变量

创建或编辑 `.env` 文件，填入以下配置：

```bash
OUTLOOK_CLIENT_ID="你的Application(client)ID"
OUTLOOK_TENANT_ID="你的Directory(tenant)ID"
OUTLOOK_CLIENT_SECRET="你的客户端密码值"
```

---

## 第三步：运行授权流程

### 3.1 安装依赖

```bash
pip install requests
# 或
pip3 install requests
```

### 3.2 执行 OAuth 设备码授权

```bash
PYTHONIOENCODING=utf-8 python3 /path/to/outlook_auth.py authorize
```

你会看到类似输出：

```
===== 授权信息 =====
请在浏览器打开: https://microsoft.com/deviceloginchina
输入代码: XXXXXXXX
===================

等待用户在浏览器完成授权...
```

**操作步骤：**

1. 打开显示的 URL（`https://microsoft.com/deviceloginchina`）
2. 输入显示的设备码
3. 用你的**世纪互联公司账号**登录（your-name@company.partner.onmschina.cn）
4. 点击"授权"

> ⚠️ **注意**：必须使用公司/组织账号登录，不要使用个人 Microsoft 账号！

### 3.3 测试连接

```bash
PYTHONIOENCODING=utf-8 python3 /path/to/outlook_auth.py test
```

看到 `连接正常` 即表示配置成功。

---

## 故障排查

### 错误：/me request is only valid with delegated authentication flow

**原因**：
1. 获取的是应用程序 token 而不是用户委托 token
2. API 权限配置成了应用程序权限而不是委托权限
3. "允许公共客户端刷新令牌流" 未启用

**解决**：
1. 确认 API 权限是**委托权限**（Delegated permissions）
2. 确认已勾选"允许公共客户端刷新令牌流"
3. 删除 `~/.outlook-microsoft/credentials.json` 后重新授权

### 错误：AUTH_003 权限不足

**原因**：Azure 应用未正确配置权限或未授予管理员同意

**解决**：
1. 确认添加了 `Mail.ReadWrite`、`Mail.Send`、`Calendars.ReadWrite` 等委托权限
2. 确认点击了**授予管理员同意**按钮
3. 确认应用注册时选择了"仅此组织目录中的账户"

### 错误：refresh_token 为 null

**原因**：
1. 授权时没有包含 `offline_access` scope
2. "允许公共客户端刷新令牌流" 未启用
3. 使用了个人 Microsoft 账号而不是公司账号授权

**解决**：
1. 确认 scope 包含 `offline_access`
2. 启用"允许公共客户端刷新令牌流"
3. 使用公司账号重新授权

### 其他问题

使用 `status` 命令查看详细状态：
```bash
PYTHONIOENCODING=utf-8 python3 /path/to/outlook_auth.py status
```

---

## 世纪互联 vs 全球版关键差异

| 配置项 | 世纪互联版 | 全球版 |
|--------|-----------|--------|
| 登录端点 | `login.chinacloudapi.cn` | `login.microsoftonline.com` |
| Graph API | `microsoftgraph.chinacloudapi.cn` | `graph.microsoft.com` |
| 门户 | `portal.azure.cn` | `portal.azure.com` |

> ⚠️ **不要使用全球版的门户或端点**，世纪互联版本是独立部署的，所有 URL 都不同。

---

## 清理/重置

如果需要重新授权，删除 credentials 文件后重新授权：

```bash
rm ~/.outlook-microsoft/credentials.json
PYTHONIOENCODING=utf-8 python3 /path/to/outlook_auth.py authorize
```
