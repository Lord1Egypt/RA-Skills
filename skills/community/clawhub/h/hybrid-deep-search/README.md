# Hybrid Deep Search 🚀

混合深度搜索系统 - 结合 Brave API 快速搜索和 OpenAI Codex 深度分析

## ✨ 特性

- 🎯 **智能路由**: 自动分析查询复杂度,选择最优搜索方案
- ⚡ **快速搜索**: 使用 Brave API,免费、快速
- 🧠 **深度分析**: 使用 OpenAI Codex,智能推理、多源综合
- 💰 **成本优化**: 简单查询用免费方案,复杂查询才用付费方案
- 🔍 **多领域聚焦**: 支持网络、学术、新闻等不同领域
- 📊 **可观测性**: 详细的搜索分析和决策依据

## 🏗️ 架构

```
用户查询
   ↓
查询分析器 (router.py)
   ├─→ 简单问题 → Brave API (web_search)     快速、免费
   ├─→ 复杂问题 → OpenAI Codex (gpt-5-codex) 深度分析、付费
   └─→ 手动模式 → 用户指定
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openai python-dotenv requests
```

### 2. 配置 API

```bash
# Brave API (已内置,无需配置)
# 使用 OpenClaw 的 web_search 工具

# OpenAI Codex API (可选,用于深度搜索)
export OPENAI_API_KEY="sk-your-openai-api-key"
```

### 3. 配置文件

```bash
cp config.json.example config.json
# 编辑 config.json 填入你的配置
```

## 📖 使用方法

### 自动模式 (推荐)

```bash
python3 scripts/deep_search.py "查询内容"
```

系统会自动分析查询复杂度并选择:
- **简单问题** → Brave API (免费、快速)
- **复杂问题** → OpenAI Codex (深度分析、付费)

### 手动指定模式

```bash
# 快速搜索 (Brave API)
python3 scripts/deep_search.py "what is OpenClaw?" --mode quick

# 深度搜索 (OpenAI Codex)
python3 scripts/deep_search.py "compare LangChain vs LlamaIndex" --mode codex
```

### 聚焦模式

```bash
# 学术搜索
python3 scripts/deep_search.py "AI agent frameworks" --mode codex --focus academic

# 新闻搜索
python3 scripts/deep_search.py "latest AI news" --mode quick --focus news

# 视频搜索
python3 scripts/deep_search.py "OpenClaw tutorial" --mode quick --focus youtube
```

## 🎯 复杂度判断规则

### → Brave API (quick)
- 简单事实查询 (what/who/when/where)
- 定义查询
- 快速查找
- 单一主题

**示例:**
```bash
python3 scripts/deep_search.py "what is OpenClaw?"
python3 scripts/deep_search.py "who created Python?"
python3 scripts/deep_search.py "latest AI news today"
```

### → OpenAI Codex (codex)
- 对比分析
- 深度推理
- 多源信息综合
- 复杂问题
- 需要推理/总结

**示例:**
```bash
python3 scripts/deep_search.py "compare LangChain vs LlamaIndex in detail"
python3 scripts/deep_search.py "analyze impact of AI on job market"
python3 scripts/deep_search.py "explain quantum computing applications in healthcare"
```

## 💰 成本对比

| 特性 | Brave API | OpenAI Codex |
|------|-----------|--------------|
| **费用** | 完全免费 | 按使用量计费 |
| **速度** | <2秒 | 5-30秒 |
| **深度** | 基础搜索 | 深度推理 |
| **适用场景** | 快速查找 | 深度分析 |

## 📊 复杂度评分系统

### 评分因素 (总分 0-10)

1. **关键词匹配** (+6分)
   - compare/analyze/explain/why/how...

2. **查询长度** (+2分)
   - >15词 = +2
   - >8词 = +1

3. **疑问句模式** (+1分)
   - 复杂疑问句

4. **技术术语** (+1分)
   - API/framework/architecture...

5. **简单关键词惩罚** (-2分)
   - what is/who is/list of...

### 决策阈值

- **0-2分**: Brave API (quick)
- **3+分**: OpenAI Codex (codex)

## 🔧 高级用法

### 详细输出 (查看路由决策)

```bash
python3 scripts/deep_search.py "query" --verbose
```

输出示例:
```
============================================================
📊 查询分析
============================================================
查询内容: compare LangChain vs LlamaIndex

复杂度评分: 6/10
推荐模式: CODEX
置信度: 95.0%

决策原因:
  1. 复杂度分数 6/10 达到阈值
  2. 检测到对比查询,需要深度分析

🚀 将使用: OpenAI Codex
============================================================
```

### JSON 输出

```bash
python3 scripts/deep_search.py "query" --format json
```

### 批量搜索

```bash
# 创建 queries.txt
echo "query 1" >> queries.txt
echo "query 2" >> queries.txt

# 批量执行
for query in $(cat queries.txt); do
  python3 scripts/deep_search.py "$query" --mode auto
done
```

### 自定义配置

编辑 `config.json`:

```json
{
  "search_settings": {
    "default_mode": "auto",
    "default_focus": "web",
    "max_results": 10,
    "router_threshold": 3,  // 调整阈值
    "verbose": false
  }
}
```

## 🧪 测试路由器

```bash
# 简单查询
python3 scripts/router.py "what is OpenClaw?"

# 复杂查询
python3 scripts/router.py "compare LangChain vs LlamaIndex in detail"
```

## 📁 目录结构

```
hybrid-deep-search/
├── SKILL.md                   # 技能文档 (OpenClaw)
├── README.md                  # 项目说明
├── config.json.example        # 配置示例
├── scripts/
│   ├── deep_search.py        # 主搜索脚本
│   └── router.py            # 查询路由器
└── tests/                   # 测试用例 (可选)
```

## 🔐 安全建议

1. **不要提交 API Key**: 确保 `.env` 或 `config.json` 不包含真实的 API Key
2. **使用环境变量**: 推荐使用环境变量存储敏感信息
3. **限制访问**: 确保 config.json 权限正确

## 🐛 故障排查

### Brave API 无响应

```bash
# 检查 OpenClaw web_search 工具
# 无需额外配置
```

### OpenAI Codex 认证失败

```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置
export OPENAI_API_KEY="sk-..."
```

### Python 依赖

```bash
pip install --upgrade openai python-dotenv requests
```

## 📚 参考资料

- [Brave Search API](https://brave.com/search/api/)
- [OpenAI GPT-5-Codex](https://platform.openai.com/docs/models/gpt-5-codex)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 许可证

MIT License

---

**作者**: Office_bot
**版本**: 1.0.0
**更新**: 2026-02-22
