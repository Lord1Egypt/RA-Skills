# Google Scholar API Skill - 安全说明

## 🔒 安全注意事项

### API 密钥管理
1. **不要提交真实密钥**：代码中只包含占位符 `your_serpapi_key_here`
2. **使用环境变量**：推荐设置 `export SERP_API_KEY="你的密钥"`
3. **密钥轮换**：定期更新 API 密钥
4. **权限最小化**：只授予必要的 API 权限

### 配置文件
- 所有敏感信息都应存储在环境变量或配置文件中
- 配置文件不应提交到版本控制系统
- 使用 `.gitignore` 排除配置文件

### 使用示例
```bash
# 正确：使用环境变量
export SERP_API_KEY="你的真实密钥"
python scripts/google_scholar_search.py "搜索词"

# 错误：硬编码在代码中
# api_key = "0430eec327584814b9f88f4740880444cb52b49fc31af526a46926499946f53a"  # ❌ 不要这样做！
```

## 📞 安全事件响应
如果怀疑 API 密钥泄露：
1. 立即在 SerpAPI 仪表板撤销密钥
2. 生成新的 API 密钥
3. 更新所有使用该密钥的地方
4. 监控异常使用情况
