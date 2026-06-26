# 🔒 安全提示 | Security Notice

## ⚠️ 重要：保护你的 API Key

### 中文

**本 SKILL 包含的配置文件可能包含敏感的 API Key，请务必：**

1. **不要提交到 Git**
   ```bash
   # 已自动添加到 .gitignore
   echo "config/models.yaml" >> .gitignore
   echo "skills/*/config/models.yaml" >> .gitignore
   ```

2. **使用环境变量**
   ```yaml
   # 推荐方式
   api_key_env: BAILIAN_API_KEY
   
   # 在 .env 文件中设置（不要提交 .env 到 Git）
   BAILIAN_API_KEY=sk-sp-xxx
   ```

3. **定期轮换 API Key**
   - 每 3-6 个月更换一次
   - 如怀疑泄露，立即重置

4. **不要分享配置文件**
   - 分享前先删除或替换 API Key
   - 使用示例配置代替真实配置

### English

**Configuration files in this SKILL may contain sensitive API Keys. Please:**

1. **Don't commit to Git**
   ```bash
   # Already added to .gitignore
   echo "config/models.yaml" >> .gitignore
   ```

2. **Use Environment Variables**
   ```yaml
   # Recommended
   api_key_env: BAILIAN_API_KEY
   
   # Set in .env file (don't commit .env to Git)
   BAILIAN_API_KEY=sk-sp-xxx
   ```

3. **Rotate API Keys Regularly**
   - Every 3-6 months
   - Immediately if compromised

4. **Don't Share Config Files**
   - Remove or replace API Keys before sharing
   - Use example configs instead

---

## 📋 安全清单 | Security Checklist

- [x] API Key 已从示例配置中移除
- [x] .gitignore 已包含 models.yaml
- [x] 使用环境变量代替硬编码
- [x] 添加了安全提示文档

---

**最后更新 | Last Updated**: 2026-03-04
