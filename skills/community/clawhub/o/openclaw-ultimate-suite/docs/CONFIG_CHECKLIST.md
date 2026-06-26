# 🔧 需要配置的 API 和 CLI 清单

## ✅ 已配置

### CLI 工具
| 工具 | 版本 | 状态 | 用途 |
|------|------|------|------|
| **gh (GitHub CLI)** | 2.88.1 | ✅ 已安装 | GitHub 仓库管理 |
| **op (1Password CLI)** | 2.32.1 | ✅ 已安装 | 密钥管理 |
| **ollama** | - | ✅ 已运行 | 本地模型推理 |

### 模型配置
| 模型 | 类型 | 上下文 | 用途 |
|------|------|--------|------|
| **qwen3.5:397b-cloud** | 云端 | - | 主模型，复杂任务 |
| **qwen3.5:35b-a3b** | 本地 | - | 中等任务，23GB |
| **qwen3.5:9b** | 本地 | - | 快速简单任务，6.6GB |
| **kimi-k2.5:cloud** | 云端 | 128k | 长上下文处理 |
| **minimax-m2.5:cloud** | 云端 | - | 特定任务 |
| **qwen3-coder:480b-cloud** | 云端 | - | 编码专用 |
| **deepseek-v3.1:671b-cloud** | 云端 | - | 深度分析 |

---

## ⚠️ 需要配置

### API 密钥
| API | 用途 | 状态 | 配置方式 |
|-----|------|------|----------|
| **IRONCLAW_API_KEY** | IronClaw 安全检测 (60 req/min) | ❌ 未配置 | 注册 https://ironclaw.io |
| **Xiaohongshu API** | 小红书自动化 | ❌ 未配置 | xiaohongshu-mcp 技能文档 |
| **TikTok API** | TikTok 数据采集 | ❌ 未配置 | tiktok-crawling 技能文档 |
| **SearXNG** | 免费 web 搜索 | ❌ 未部署 | openclaw-free-web-search 技能 |

### 服务部署
| 服务 | 用途 | 状态 | 配置方式 |
|------|------|------|----------|
| **SearXNG** | 自托管搜索引擎 | ❌ 未部署 | Docker 部署或租用实例 |
| **Playwright** | 浏览器自动化 | ⚠️ 需初始化 | `playwright install` |
| **SMTP/IMAP** | 邮件摘要 | ❌ 未配置 | email-daily-summary 技能 |

### 可选 CLI
| 工具 | 用途 | 状态 | 安装命令 |
|------|------|------|----------|
| **gcloud** | Google Cloud | ❌ 未安装 | `brew install gcloud` |
| **sops** | 密钥加密 | ❌ 未安装 | `brew install sops` |
| **jq** | JSON 处理 | ⚠️ 检查 | `brew install jq` |

---

## 🎯 优先级配置

### P0 - 立即配置
1. **Playwright 初始化** (免费)
   ```bash
   playwright install
   playwright install-deps
   ```
   **用途**: 网页自动化、数据采集

### P1 - 可选配置
2. **SearXNG 部署** (免费，可选)
   ```bash
   # Docker 部署
   docker run -d -p 8080:8080 searxng/searxng
   ```
   **用途**: 自托管搜索引擎 (无 API 成本)

### P2 - 按需配置
3. **小红书 Cookie** (如需发布)
   - 参考：`skills/xiaohongshu-mcp/SKILL.md`

4. **邮件服务** (如需摘要)
   - 参考：`skills/email-daily-summary/SKILL.md`

---

## 📋 配置检查脚本

```bash
#!/bin/bash
# scripts/check-config.sh

echo "🔍 检查配置状态..."

# CLI 工具
echo -n "gh: "; gh --version 2>&1 | head -1
echo -n "op: "; op --version 2>&1 | head -1
echo -n "ollama: "; ollama --version 2>&1 | head -1

# 环境变量
echo -n "IRONCLAW_API_KEY: "; if [ -n "$IRONCLAW_API_KEY" ]; then echo "✅ 已配置"; else echo "❌ 未配置"; fi

# Playwright
if command -v playwright &> /dev/null; then
  echo "playwright: ✅ 已安装"
else
  echo "playwright: ❌ 未安装"
fi

# 模型
echo "📊 可用模型:"
ollama list

echo "✅ 检查完成"
```

---

## 🛡️ 安全建议

1. **使用 1Password 存储 API 密钥**
   ```bash
   op read "ironclaw-api-key"
   export IRONCLAW_API_KEY=$(op read "ironclaw-api-key")
   ```

2. **不要硬编码密钥**
   - 使用环境变量
   - 使用 `.env` 文件 (加入 `.gitignore`)
   - 使用 1Password CLI

3. **定期轮换密钥**
   - 设置提醒每 90 天轮换
   - 使用 1Password 自动轮换

---

*最后更新：2026-03-15 15:22 GMT+8*
`)
   - 使用 1Password CLI

3. **定期轮换密钥**
   - 设置提醒每 90 天轮换
   - 使用 1Password 自动轮换

---

*最后更新：2026-03-15 15:22 GMT+8*
