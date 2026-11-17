# 🔒 Vibe Codebase Audit - 中文使用指南

## 📋 简介

**Vibe Codebase Audit** 是专为 AI 生成代码设计的全面安全审计工具，支持智能体原生集成、多提供者支持和依赖安全扫描。

> 🎉 **v2.0 新功能**: 智能体原生审计（无需 API key）、多提供者支持、依赖扫描、配置审计

---

## ⚡ 快速开始

### 方法1：智能体原生审计（推荐，零配置）

```python
# 无需 API key！直接使用当前智能体的 LLM
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="agent_llm"  # 使用当前智能体的 LLM
)
```

### 方法2：使用您的 API Key

```python
# 使用您自己的 OpenAI/Claude/其他 API
result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="openai",  # 或 "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### 方法3：命令行使用

```bash
# 使用智能体的 LLM（无需 API key）
python vibe_audit_enhanced.py /path/to/project --provider agent_llm

# 使用 OpenAI
python vibe_audit_enhanced.py /path/to/project --provider openai

# 使用本地 Ollama 模型
python vibe_audit_enhanced.py /path/to/project --provider ollama

# 增量审计（仅审计变更文件）
python vibe_audit_enhanced.py /path/to/project --incremental --base-branch main
```

---

## 🆕 v2.0 新功能

### 1. 🤖 智能体原生集成
- **零配置** - 无需 API key
- 使用您当前智能体的 LLM 连接
- 与 OpenCode、Hermes、OpenClaw 无缝集成
- 成本更低 - 利用已有的智能体订阅

### 2. 🔌 多提供者支持
- **Agent LLM** - 使用当前智能体（推荐）
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - 性价比高的选择
- **Qwen/通义千问** - 阿里云模型
- **Ollama** - 运行本地模型（免费！）
- **OpenRouter** - 访问 100+ 模型

### 3. 📦 依赖安全扫描
- 检查已知漏洞（CVE）
- 检测过期依赖
- 许可证合规检查
- 支持：npm, pip, maven, cargo, go mod

### 4. ⚙️ 配置安全检查
- 暴露的 .env 文件检测
- CORS 错误配置检测
- 调试模式检测
- SSL 验证检查

### 5. 🚀 性能优化
- **智能缓存** - 不重复扫描未变更文件
- **增量审计** - 仅审计变更文件
- **差异审计** - 对比提交间的安全状态
- **并行处理** - 更快的扫描

### 6. 🛡️ 自定义规则引擎
- 定义您自己的安全模式
- YAML/JSON 规则定义
- 项目特定规则

---

## 📊 工具对比

| 工具 | 速度 | 准确度 | 功能 | API Key | 最佳用途 |
|------|------|--------|------|---------|----------|
| `vibe_audit_enhanced` | 中速 | 高 | 所有功能 | 可选 | **生产环境** |
| `vibe_audit_scan` | 快 | 中 | 基础 | 无需 | 快速检查 |
| `vibe_audit_multi_model` | 慢 | 最高 | AI 共识 | 需要 | 关键项目 |
| `vibe_audit_incremental` | 很快 | 中 | Git 感知 | 可选 | CI/CD |

**推荐**：使用 `vibe_audit_enhanced` 并设置 `primary_provider="agent_llm"`

---

## 🎯 使用场景

### 发布前安全审计
```python
result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    primary_provider="agent_llm",
    enable_dependency_scan=True,
    enable_config_scan=True
)

if result['summary']['risk_level'] in ['CRITICAL', 'HIGH']:
    print("⛔ 请勿发布 - 发现严重安全问题！")
    for finding in result['findings']:
        print(f"  - {finding['severity']}: {finding['issue']}")
else:
    print("✅ 可以安全发布！")
```

### CI/CD 集成
```yaml
# GitHub Actions 示例
- name: 安全审计
  run: |
    python vibe_audit_enhanced.py . \
      --provider agent_llm \
      --incremental \
      --base-branch main
    
- name: 检查结果
  run: |
    if [ $(jq '.summary.risk_score' audit-report.json) -gt 50 ]; then
      echo "风险分数过高！"
      exit 1
    fi
```

### PR 安全审查
```python
# 仅审计变更文件
result = vibe_audit_incremental(
    project_path="/path/to/project",
    base_branch="main"
)

# 审计这些特定文件
for file in result['changed_files']:
    print(f"检查 {file}...")
```

---

## 🔧 配置

### 基础配置 (.vibe-audit.yaml)

```yaml
version: "1.0"

audit:
  primary_provider: agent_llm
  fallback_provider: openai
  cache_enabled: true
  parallel_workers: 4

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4"
  
  ollama:
    base_url: "http://localhost:11434"
    model: "llama2"

dependency:
  enabled: true
  check_vulnerabilities: true

config:
  enabled: true
  check_env_files: true
```

### 自定义安全规则 (custom-rules.yaml)

```yaml
rules:
  - id: CUSTOM_001
    name: "危险函数使用"
    severity: high
    patterns:
      - pattern: "eval\\s*\\("
        message: "eval() 可能导致代码注入"
        recommendation: "使用 JSON.parse() 代替"
```

---

## 🌐 提供者设置

### 智能体 LLM（推荐）
```python
# 无需设置！直接使用：
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
# 可选：export OPENAI_MODEL="gpt-4-turbo"
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### DeepSeek
```bash
export DEEPSEEK_API_KEY="sk-..."
```

### 通义千问
```bash
export DASHSCOPE_API_KEY="sk-..."
```

### Ollama（本地，免费）
```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull llama2

# 在审计中使用
primary_provider="ollama"
```

---

## 📈 性能优化

### 启用缓存（默认：开）
```python
result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    use_cache=True  # 缓存结果 7 天
)
```

### 增量审计
```python
# 仅审计上次提交后变更的文件
result = vibe_audit_incremental(
    project_path="/path/to/project",
    base_branch="main"
)
```

### 清除缓存
```python
from vibe_audit_enhanced import AuditCache

cache = AuditCache()
cache.clear()
```

---

## 🔍 检测能力

### 密钥和凭据
- ✅ API keys（OpenAI, Anthropic, AWS, GitHub 等）
- ✅ 认证令牌
- ✅ 数据库凭据
- ✅ SSH 密钥和证书
- ✅ JWT secrets
- ✅ AWS 凭据模式

### 安全漏洞
- ✅ SQL 注入模式
- ✅ 命令注入风险
- ✅ XSS 模式
- ✅ 路径遍历
- ✅ 弱加密
- ✅ CSRF 问题

### 依赖安全（新功能）
- ✅ 已知 CVE 漏洞
- ✅ 过期包
- ✅ 许可证合规
- ✅ npm audit 集成
- ✅ pip audit 集成

### 配置安全（新功能）
- ✅ 暴露的 .env 文件
- ✅ CORS 错误配置
- ✅ 调试模式启用
- ✅ SSL 验证禁用
- ✅ 硬编码 IP

---

## 📝 输出格式

### JSON（默认）
```python
output_format="json"
```

### Markdown
```python
output_format="markdown"
# 结果包含格式化的 markdown 报告
```

### HTML
```python
output_format="html"
# 带样式的交互式 HTML 报告
```

---

## 🚨 风险等级

| 等级 | 分数 | 行动 |
|------|------|------|
| ✅ 安全 | 0 | 可以发布 |
| 🟢 低 | 1-19 | 小问题，建议审查 |
| 🟡 中 | 20-49 | 发布前审查并修复 |
| 🟠 高 | 50-79 | 重要问题，必须修复 |
| 🔴 严重 | 80-100 | **请勿发布** |

---

## 🤝 支持的智能体

| 智能体 | 集成方式 | 设置 | 最佳用途 |
|--------|----------|------|----------|
| **OpenCode** | 原生 skill | 自动发现 | 无缝工作流 |
| **Hermes** | 插件 | 添加到插件目录 | 提交前检查 |
| **OpenClaw** | 模块导入 | 直接导入 | 自定义工作流 |
| **MCP 客户端** | 协议 | 配置服务器 | 标准集成 |

---

## 📚 文档

- **SKILL.md** - 完整文档
- **IMPROVEMENT_ANALYSIS.md** - 功能分析和路线图
- **vibe-audit-config.yaml** - 配置模板
- **custom-rules-example.yaml** - 自定义规则示例

---

## 🆘 迁移指南

### 从 v1.x 到 v2.0

**旧版 (v1.x):**
```python
result = vibe_audit_multi_model(
    project_path="/path/to/project",
    openrouter_api_key="sk-or-..."
)
```

**新版 (v2.0):**
```python
result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    primary_provider="agent_llm",  # 无需 API key！
    enable_dependency_scan=True,   # 新功能
    enable_config_scan=True        # 新功能
)
```

**优势：**
- ✅ 无需 API key
- ✅ 包含依赖扫描
- ✅ 包含配置检查
- ✅ 更好的缓存
- ✅ 更多提供者选项

---

## 🎯 最佳实践

1. **OpenCode/Hermes/OpenClaw 用户**：使用 `primary_provider="agent_llm"`
2. **CI/CD**：使用增量审计 + 缓存
3. **关键项目**：使用多提供者共识
4. **大型代码库**：启用缓存 + 并行处理
5. **团队协作**：创建项目特定的自定义规则

---

## 📞 支持

- **问题反馈**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **文档**: 查看 SKILL.md 了解详情
- **示例**: 查看 examples/ 目录

---

**自信发布。严格审计。安心编程。** 🚀
