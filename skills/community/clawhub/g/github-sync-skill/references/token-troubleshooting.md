# GitHub Token 故障排查指南

## 常见问题

### 1. Token 无效

**错误信息**:
```
401 Bad credentials
```

**原因**:
- Token 已过期
- Token 被撤销
- Token 复制不完整

**解决方案**:
1. 访问 https://github.com/settings/tokens
2. 检查 Token 状态
3. 重新生成新 Token
4. 更新本地配置

---

### 2. 权限不足

**错误信息**:
```
403 Resource not accessible by personal access token
```

**原因**:
- Token 缺少 `repo` scope
- Token 只有 read 权限

**解决方案**:
1. 访问 https://github.com/settings/tokens/new
2. 创建新 Token
3. **务必勾选** `repo` (Full control of private repositories)
4. 使用新 Token

---

### 3. 用户不匹配

**错误信息**:
```
403 Permission to <owner>/<repo> denied to <user>
```

**原因**:
- Token 属于用户 A，但仓库属于用户 B
- 尝试推送到没有写权限的仓库

**解决方案**:
1. 确认 Token 所有者：
   ```bash
   curl -s -H "Authorization: token <TOKEN>" \
     https://api.github.com/user | jq -r '.login'
   ```
2. 确认仓库所有者与 Token 一致
3. 如不一致，使用正确的 Token

---

### 4. 仓库不存在

**错误信息**:
```
404 Not Found
```

**原因**:
- 仓库名称拼写错误
- 仓库尚未创建

**解决方案**:
1. 检查仓库名称是否正确
2. 手动创建仓库：
   - 访问 https://github.com/new
   - 输入仓库名称
   - 点击 Create repository
3. 或使用 API 创建（需要 Token 有 repo 权限）

---

### 5. 网络超时

**错误信息**:
```
Connection timeout
Failed to connect to api.github.com
```

**原因**:
- 网络连接问题
- 防火墙阻止
- GitHub API 限流

**解决方案**:
1. 检查网络连接
2. 检查代理设置
3. 等待限流解除（通常 1 小时）
4. 使用认证请求提高限流（已登录 5000 次/小时）

---

## Token 安全管理

### 存储建议

✅ **推荐方式**:
```bash
# 1. 环境变量（会话级）
export GITHUB_TOKEN="ghp_xxx"

# 2. Shell 配置文件（持久化）
echo 'export GITHUB_TOKEN="ghp_xxx"' >> ~/.zshrc
source ~/.zshrc

# 3. 密钥管理工具
pass insert github/token
```

❌ **不要**:
- 将 Token 提交到 Git 仓库
- 在公开场合分享 Token
- 使用过期的 Token
- 多人共享同一 Token

### Token 过期处理

1. **设置提醒**: 创建时设置 30-90 天过期
2. **定期轮换**: 每 30 天更新一次
3. **监控使用**: 定期检查 GitHub 安全日志

---

## 快速验证命令

```bash
# 验证 Token 有效性
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user | jq '.login, .type'

# 验证仓库权限
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/kuiilabs/claude-skills | \
  jq '.permissions'

# 查看 Token Scopes
curl -s -I -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com | grep -i x-oauth-scopes
```

---

## 创建 Token 步骤

1. 访问 https://github.com/settings/tokens/new
2. 填写 **Note**: `Claude Code Skills Sync`
3. 设置 **Expiration**: `30 days` (推荐)
4. 勾选 **Scopes**:
   - ✅ `repo` (Full control of private repositories)
5. 点击 **Generate token**
6. **立即复制** Token（只显示一次）
7. 存储到安全位置

---

## 相关资源

- [GitHub Personal Access Tokens 文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GitHub API 限流说明](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [OAuth Scopes 参考](https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps)
