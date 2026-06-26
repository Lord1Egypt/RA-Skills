# 数据安全与隐私保护声明

## ⚠️ 重要提示

**Li_python_sec_check** 是一个 Python 安全规范检查工具，包含本地检查和可选的 LLM 智能分析功能。

---

## 🔒 数据安全说明

### 默认行为（安全）

✅ **所有核心检查都在本地执行**，不会发送任何数据到外部：

1. 项目结构检查
2. Dockerfile 规范检查
3. requirements.txt 检查
4. Python 版本检查
5. 不安全加密算法检测
6. SQL 注入风险检测
7. 命令注入风险检测
8. 敏感信息硬编码检测
9. 调试模式检测
10. flake8 代码质量检查
11. bandit 安全扫描
12. pip-audit 依赖漏洞扫描
13. **隐私信息泄露检查**
14. **数据安全检查**

### LLM 功能（可选，默认禁用）

⚠️ **仅在显式启用 `--llm` 参数时**，才会调用外部 API：

```bash
# ⚠️ 此命令会发送代码到外部 API
python scripts/python_sec_check.py /path/to/project --llm
```

**发送的数据包括**:
- 代码片段（用于分析）
- 扫描结果（用于生成修复建议）

**不发送的数据**:
- 完整源代码文件
- 项目结构信息
- 用户凭证

---

## 🛡️ 安全使用建议

### 1. 敏感代码项目

```bash
# ✅ 推荐：仅使用本地检查
python scripts/python_sec_check.py /path/to/sensitive-project

# ❌ 避免：不要启用 LLM
# python scripts/python_sec_check.py /path/to/sensitive-project --llm
```

### 2. 企业环境

```bash
# ✅ 推荐：使用私有 API 端点
export LLM_API_BASE=https://internal-llm.your-company.com/v1
export LLM_API_KEY=your-internal-key
python scripts/python_sec_check.py /path/to/project --llm
```

### 3. 开源项目

```bash
# ✅ 可以使用公共 LLM API
python scripts/python_sec_check.py /path/to/open-source-project --llm
```

---

## 📋 环境变量配置

| 变量 | 说明 | 默认值 | 建议 |
|------|------|--------|------|
| `LLM_API_KEY` | LLM API 密钥 | 无 | 仅在需要 LLM 时设置 |
| `LLM_API_BASE` | LLM API 端点 | https://dashscope.aliyuncs.com | 企业用户应设置为私有端点 |

---

## 🔍 网络行为说明

### 本地检查（默认）

- ❌ **不**发起任何网络请求
- ❌ **不**发送任何数据到外部
- ✅ 所有分析在本地完成

### LLM 分析（可选）

- ✅ 仅在 `--llm` 参数启用时
- ✅ 发送代码片段到配置的 API 端点
- ✅ 接收分析结果和建议

---

## 📊 数据流向图

```
默认模式（安全）:
┌──────────────┐
│  你的代码    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  本地检查    │ ← 不发送任何数据
│  14 项检查    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  本地报告    │
└──────────────┘

LLM 模式（可选）:
┌──────────────┐
│  你的代码    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  本地检查    │
│  14 项检查    │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  LLM 分析    │────▶│  外部 API    │ ⚠️ 会发送数据
│  (可选)      │◀────│  (可配置)    │
└──────┬───────┘     └──────────────┘
       │
       ▼
┌──────────────┐
│  增强报告    │
└──────────────┘
```

---

## 🎯 最佳实践

### 1. 默认禁用 LLM

```bash
# ✅ 推荐：默认不使用 LLM
python scripts/python_sec_check.py /path/to/project
```

### 2. 审查 LLM 代码

在使用 LLM 功能前，建议审查 `scripts/llm_analyzer.py`：

```bash
# 查看 LLM 模块代码
cat scripts/llm_analyzer.py | head -50
```

### 3. 使用隔离环境

```bash
# 在容器或 VM 中运行
docker run --rm -v $(pwd):/app python:3.9 \
  python scripts/python_sec_check.py /app
```

### 4. 定期检查更新

```bash
# 更新技能到最新版本
clawhub update Li_python_sec_check
```

---

## 📞 联系方式

如有数据安全相关问题：

- **GitHub Issues**: https://github.com/your-repo/Li_python_sec_check/issues
- **ClawHub**: 技能页面评论

---

## 📝 更新日志

### v0.0.2 (2026-03-21)
- ✅ 添加明确的数据安全声明
- ✅ LLM 功能默认禁用警告
- ✅ 添加隐私保护说明
- ✅ 说明网络行为和 API 端点

### v0.0.1 (2026-03-21)
- 初始发布

---

**最后更新**: 2026-03-21 19:15  
**版本**: 0.0.2  
**作者**: 北京老李

*Li_python_sec_check - 安全、透明、可信赖的 Python 代码检查工具* 🔒🐍
