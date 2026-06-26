---
name: skill-security-check
description: Skill 发布前安全检查工具。在发布 skill 到 ClawHub 前，自动扫描敏感信息（API Key、Token、私钥、邮箱、手机号、精确坐标等）。Use before publishing any skill to prevent leaking private data.
---

# Skill 发布前安全检查

在发布 skill 到 ClawHub 前，自动扫描敏感信息，防止隐私泄露。

## 检查项

| 类型 | 检测内容 |
|------|----------|
| 🔑 API Keys | OpenAI `sk-*`, Tavily `tvly-*`, 自定义格式 |
| 🔐 Tokens | 32位以上随机字符串、硬编码 token |
| 🔒 私钥 | RSA/私钥文件特征 |
| 📍 坐标 | 精确到小数点后4位的经纬度 |
| 📧 邮箱 | 个人邮箱地址 |
| 📱 手机 | 中国手机号 |

## 使用方式

### 发布前检查

```bash
# 检查指定 skill
./skill-pre-publish-check.sh /path/to/skill

# 在 skill 目录下运行
cd my-skill
../skill-security-check/skill-pre-publish-check.sh .
```

### 集成到发布流程

```bash
# 发布前自动检查
skill_dir="./my-skill"
./skill-security-check/skill-pre-publish-check.sh "$skill_dir" && \
  clawhub publish "$skill_dir" --slug my-skill --version 1.0.0
```

## 输出示例

### 发现敏感信息

```
🔍 检查 skill: ./my-skill

⚠️ 发现可能的敏感信息:
./my-skill/script.py:api_key = "sk-abc123..."
./my-skill/config.sh:TOKEN="secret_token_here"

❌ 发现敏感信息，请修复后再发布！

修复建议:
  1. 使用环境变量: os.environ.get('API_KEY', '')
  2. 在 SKILL.md 中说明需要配置的环境变量
  3. 示例值使用占位符: your_token, YOUR_API_KEY
```

### 检查通过

```
🔍 检查 skill: ./my-skill

✅ 未发现敏感信息，可以安全发布
```

## 修复建议

### API Key / Token

```python
# ❌ 错误
API_KEY = "sk-abc123..."
TOKEN = "your_actual_token_here"

# ✅ 正确
API_KEY = os.environ.get('API_KEY', '')
TOKEN = os.environ.get('CAIYUN_TOKEN', '')

# 并在 SKILL.md 中说明
```

### 坐标

```bash
# ❌ 错误
LNG="113.9536"
LAT="22.5788"

# ✅ 正确
LNG="${LNG:-}"  # 通过环境变量配置
LAT="${LAT:-}"

# 或使用模糊示例
LNG="116.4"  # 北京示例
LAT="39.9"
```

### 邮箱/手机

```markdown
# ❌ 错误
联系作者: real_email@example.com

# ✅ 正确
联系作者: your_email@example.com
```

## 最佳实践

1. **发布前必检** — 每次发布前运行检查
2. **环境变量** — 所有敏感配置用环境变量
3. **占位符** — 文档示例用 `your_xxx` 占位
4. **.gitignore** — 不要提交 `.env` 文件
5. **定期轮换** — 如有泄露立即轮换密钥
