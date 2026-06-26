# 安全说明文档

本文档说明 kindle-download skill 的安全架构和凭证管理建议。

## 安全架构概述

本 skill 采用多层安全防护措施：

1. **输入验证** - 所有用户输入都经过严格验证
2. **路径验证** - 文件路径限制在安全目录内
3. **凭证管理** - 支持环境变量和加密配置文件
4. **进程隔离** - 使用独立脚本，不直接执行 Shell 命令

## 已实现的安全措施

### 1. 输入验证（Shell 注入防护）

**位置**: `scripts/sanitize.js`

**安全设计原则**:
- **白名单优先**: 只允许已知安全的字符
- **深度防御**: 多层过滤，不依赖单一检查
- **明确失败**: 无效输入返回明确错误，不尝试修复

**功能**:
- 检测并过滤所有危险的 Shell 元字符（`; | & $ \` ( ) { } < > !` 等）
- 移除控制字符（空字节、换行符等）
- 限制输入长度（书名最大 100 字符，作者/出版社最大 50 字符）
- 使用白名单验证：只允许中文、英文、数字、空格、基本标点

**关键函数**:
```javascript
// 检查危险字符
function containsDangerousChars(input) {
    // 检查 Shell 元字符
    // 检查控制字符
    // 检查命令替换模式 $() 和 ``
    // 检查变量扩展 ${...}
}

// 验证书名
function validateBookTitle(title) {
    // 先检查危险字符
    // 再进行白名单验证
}
```

### 2. 文件路径验证（路径遍历防护）

**位置**:
- `scripts/sanitize.js` (JavaScript 版本)
- `scripts/send_kindle.py` (Python 版本)

**功能**:
- 检测路径遍历攻击（`../` 等）
- 只允许访问指定的安全目录
- 只接受安全的文件扩展名（`.epub`, `.pdf`, `.mobi`, `.azw3`）

**允许的目录**:
- `/tmp/kindle_downloads/`
- `~/.config/kindle-download/`

### 3. 进程隔离

- 使用独立的脚本执行，而非直接在 Shell 中构建命令
- 所有参数通过脚本内部处理，不依赖 Shell 解析
- 使用 Node.js 和 Python 的安全 API 进行操作
- 不使用 `eval()`, `exec()`, 或其他动态执行方法

## 凭证安全

### 当前状态

配置文件 `auth.json` 包含以下敏感信息：
- SMTP 邮箱授权码
- Z-Library 账户密码

### 推荐的安全实践

#### 选项 1: 环境变量（推荐）

使用环境变量存储敏感信息是**最安全的方式**：

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中设置
export KINDLE_SMTP_EMAIL="your_email@163.com"
export KINDLE_SMTP_AUTH_CODE="your_smtp_auth_code"
export KINDLE_ZLIB_EMAIL="your_zlibrary_email"
export KINDLE_ZLIB_PASSWORD="your_zlibrary_password"
export KINDLE_RECEIVER_EMAIL="your_kindle@kindle.com"
```

**优点**:
- 凭证不存储在文件系统中
- 不会被意外提交到版本控制
- 可以在不同环境间轻松切换
- 符合 12-Factor App 最佳实践

#### 选项 2: 文件权限限制

如果必须使用配置文件：

```bash
# 设置严格的文件权限
chmod 600 ~/.config/kindle-download/auth.json

# 确保目录权限正确
chmod 700 ~/.config/kindle-download

# 验证权限
ls -la ~/.config/kindle-download/auth.json
# 应显示: -rw------- (仅所有者可读写)
```

#### 选项 3: 使用密钥管理工具

考虑使用系统密钥管理工具：

- **macOS**: Keychain
- **Linux**: libsecret / gnome-keyring
- **跨平台**: 1Password CLI, pass, HashiCorp Vault

### 凭证优先级

脚本按以下优先级查找凭证：

1. **环境变量**（最高优先级）
2. 配置文件 `~/.config/kindle-download/auth.json`
3. 旧位置 `~/.openclaw/workspace/skills/kindle-download/auth.json`（兼容）

### 不要做的事情

1. **不要**将 `auth.json` 提交到版本控制系统
2. **不要**在日志中打印凭证信息
3. **不要**在公共场所或共享电脑上存储明文凭证
4. **不要**使用与重要账户相同的密码
5. **不要**在截图或错误报告中包含凭证信息

## 安全检查清单

- [x] 输入验证已实现（白名单 + 黑名单）
- [x] 路径遍历防护已实现
- [x] 文件类型限制已实现
- [x] 目录访问限制已实现
- [x] 进程隔离已实现
- [x] 环境变量支持已实现
- [x] 凭证优先级机制已实现
- [ ] 文件权限已设置为 600（建议用户手动执行）
- [ ] 环境变量配置（推荐用户配置）
- [ ] 密钥管理集成（可选，未来增强）

## ClawHub 审核说明

### 已解决的问题

1. **Manifest 元数据不准确**: ✅ 已修复
   - SKILL.md 现在包含准确的 `requirements` 声明
   - 列出了所有必需的二进制文件、Node 模块、系统依赖

2. **缺少安装说明**: ✅ 已修复
   - 添加了 `INSTALL.md` 文档
   - 详细说明了所有依赖的安装步骤

3. **凭证管理**: ✅ 已改进
   - 支持环境变量（推荐方式）
   - SKILL.md 中明确声明了 `credentials` 字段
   - 添加了安全警告和建议

4. **输入验证问题**: ✅ 已修复
   - 重写了 `sanitize.js`，使用正确的正则表达式
   - 采用白名单优先的安全设计
   - 添加了多层防御机制

### 声明的凭证

以下凭证在 SKILL.md 的 `credentials` 字段中明确声明：

| 凭证名称 | 描述 | 必需 | 敏感 | 来源 |
|---------|------|------|------|------|
| KINDLE_SMTP_EMAIL | SMTP 发送邮箱 | ✅ | 否 | 环境变量/auth.json |
| KINDLE_SMTP_AUTH_CODE | SMTP 授权码 | ✅ | ✅ | 环境变量/auth.json |
| KINDLE_RECEIVER_EMAIL | Kindle 接收邮箱 | ✅ | 否 | 环境变量/auth.json |
| KINDLE_ZLIB_EMAIL | Z-Library 账号邮箱 | ✅ | 否 | 环境变量/auth.json |
| KINDLE_ZLIB_PASSWORD | Z-Library 账号密码 | ✅ | ✅ | 环境变量/auth.json |
| KINDLE_PROXY_SERVER | 代理服务器地址 | ❌ | 否 | 环境变量/auth.json |

### 依赖声明

以下依赖在 SKILL.md 的 `requirements` 字段中明确声明：

**二进制文件**:
- `node` >= 18.0.0
- `python3` >= 3.8.0

**Node.js 模块**:
- `playwright` >= 1.40.0

**系统依赖**:
- Chromium Browser（通过 `npx playwright install chromium` 安装）

**Python 包**:
- `requests` >= 2.28.0

## 报告安全问题

如果您发现安全漏洞，请负责任地报告：

1. 不要公开披露漏洞
2. 通过 GitHub Issues 或私信联系维护者
3. 提供详细的复现步骤
4. 等待修复后再公开披露
