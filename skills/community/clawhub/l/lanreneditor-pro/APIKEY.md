# API Key 管理文档

本文档说明如何在排版平台中管理 API Key，以及如何在 OpenClaw Skill 中使用。

---

## 什么是 API Key

API Key 是访问排版平台 API 的凭证，用于：

- 🔌 **OpenClaw Skill** - 在 OpenClaw 中直接调用排版服务
- 🤖 **第三方集成** - 其他自动化工具接入
- 🔧 **开发者调用** - 程序化访问 API

---

## 管理 API Key

### 打开管理页面

1. 登录排版平台
2. 点击右上角 **⚙️ 设置**
3. 找到 **🔑 API 密钥** 区域
4. 点击 **管理 API Key** 按钮

### 生成新密钥

1. 点击 **➕ 生成新密钥**
2. 填写密钥名称（如：OpenClaw Skill）
3. 选择有效期（可选）
4. 点击 **生成**
5. **立即复制并保存密钥**（只显示一次！）

### 密钥信息

每个密钥显示以下信息：

| 字段 | 说明 |
|------|------|
| 名称 | 密钥的标识名称 |
| 密钥 | 脱敏显示，生成时可见完整密钥 |
| 状态 | 启用中 / 已禁用 |
| 权限 | 该密钥拥有的权限 |
| 调用次数 | 本小时已调用 / 限制次数 |
| 创建时间 | 密钥生成时间 |
| 有效期 | 永久或到期日期 |
| 最近使用 | 最后一次调用时间 |

### 操作

- **📋 查看日志** - 查看该密钥的 API 调用记录
- **✅ 启用 / 🚫 禁用** - 临时停用密钥
- **🗑️ 删除** - 永久删除密钥（不可恢复）

---

## 在 OpenClaw Skill 中使用

### 1. 获取 API Key

按照上述步骤在排版平台生成 API Key。

### 2. 配置 Skill

在 OpenClaw Gateway 中配置 Skill：

```yaml
# skill.yaml 中的配置项
config:
  - name: apiBaseUrl
    label: SaaS 平台地址
    value: https://open.tyzxwl.cn  # 你的平台地址
    
  - name: apiKey
    label: API 密钥
    value: wemd_xxxxx...  # 你生成的密钥
```

或在 OpenClaw 界面中填写：

| 配置项 | 值 |
|--------|-----|
| SaaS 平台地址 | `https://open.tyzxwl.cn` |
| API 密钥 | `wemd_xxxxxxxxxxxxxxxx` |

### 3. 开始使用

配置完成后，即可在 OpenClaw 对话中使用：

```
用户：写一篇关于 AI 的文章发布到公众号
OpenClaw：✅ 已发布到草稿箱！
```

建议在 Skill 目录执行一次 `npm install`，确保 `axios` 依赖已安装。

---

## API 权限说明

API Key 按套餐计划获得以下权限：

| 权限 | 免费版 | 基础版 | 专业版 | 企业版 |
|------|--------|--------|--------|--------|
| 获取模板列表 | ✅ | ✅ | ✅ | ✅ |
| 获取模板分类 | ✅ | ✅ | ✅ | ✅ |
| 获取公众号列表 | ✅ | ✅ | ✅ | ✅ |
| 发布到草稿箱 | 10次/月 | 100次/月 | 500次/月 | 不限 |
| 预览排版 | ✅ | ✅ | ✅ | ✅ |
| 查询额度 | ✅ | ✅ | ✅ | ✅ |
| 绑定公众号数 | 1个 | 3个 | 10个 | 不限 |
| 保存自定义模板 | 3个 | 20个 | 不限 | 不限 |

---

## 安全建议

- **不要将 API Key 写入前端代码或公开仓库**
- 为不同用途生成不同的密钥，方便管理和撤销
- 定期检查密钥调用日志，发现异常及时禁用
- 不再使用的密钥请及时删除

---

## 常见问题

**Q: 密钥丢了怎么办？**
A: 密钥只在生成时显示一次，丢失后需要删除旧密钥并重新生成。

**Q: 调用返回 401 错误？**
A: 请检查密钥是否正确、是否已禁用、是否已过期。

**Q: 调用返回 429 错误？**
A: 请求频率超限，请降低调用频率或联系 lanren0405@163.com 申请提升限制。

每个 API Key 拥有以下权限：

| 权限 | 说明 |
|------|------|
| `templates:read` | 读取模板列表和分类 |
| `accounts:read` | 读取绑定的公众号 |
| `publish:write` | 发布文章到微信草稿箱 |
| `quota:read` | 查询发布额度和公众号绑定情况 |

---

## 速率限制

每个 API Key 默认限制：

- **100 次/小时**
- 超过限制将返回 `429 Too Many Requests`

如需提高限制，请联系管理员。

---

## 安全建议

### ✅ 应该做的

- 为不同用途创建独立的 API Key
- 设置合理的有效期（建议 90 天）
- 定期轮换密钥
- 禁用不再使用的密钥
- 监控 API 调用日志

### ❌ 不应该做的

- 将 API Key 提交到代码仓库
- 在客户端暴露 API Key
- 与他人共享 API Key
- 使用永久有效的密钥

---

## 故障排查

### 问题："无效的 API Key"

**原因**：
- 密钥输入错误
- 密钥已过期
- 密钥已被禁用或删除

**解决**：
1. 检查密钥是否正确复制
2. 在管理页面确认密钥状态
3. 重新生成密钥

### 问题："请求过于频繁"

**原因**：超过速率限制

**解决**：
1. 等待下一个小时重置
2. 减少调用频率
3. 联系管理员提高限制

### 问题："无法连接到排版平台"

**原因**：
- 平台地址错误
- 网络问题
- 平台服务异常

**解决**：
1. 检查 `apiBaseUrl` 配置
2. 确认平台可访问
3. 联系管理员

---

## API 端点

使用 API Key 可以访问以下端点：

### 获取模板列表
```
GET /api/skill/templates?category=&search=&page=1&limit=20
Headers: X-API-Key: {your_api_key}
```

返回内置模板和用户自定义模板（用户模板排在前面）。

### 获取模板分类
```
GET /api/skill/templates/categories
Headers: X-API-Key: {your_api_key}
```

### 获取公众号列表
```
GET /api/skill/accounts
Headers: X-API-Key: {your_api_key}
```

### 发布文章
```
POST /api/skill/publish
Headers: X-API-Key: {your_api_key}
Content-Type: application/json

Body: {
  "content": "文章内容（Markdown）",
  "title": "标题",
  "templateId": "tech-blue",
  "accountId": "公众号AppID（可选）",
  "author": "作者（可选）",
  "digest": "摘要（可选）",
  "coverImage": "封面图URL（可选）",
  "contentSourceUrl": "阅读原文链接（可选）",
  "autoGenerateCover": true
}
```

### 查询发布状态
```
GET /api/skill/publish/status?taskId=xxx
Headers: X-API-Key: {your_api_key}
```

### 查询额度
```
GET /api/skill/quota
Headers: X-API-Key: {your_api_key}
```

返回当前套餐名称、发布额度使用情况及公众号绑定数量。

---

## 更新日志

### v1.0.0
- ✅ API Key 生成与管理
- ✅ 调用日志查看
- ✅ 速率限制
- ✅ 启用/禁用控制
