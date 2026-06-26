# 贡献指南 🤝

感谢你对 Investment Framework Skill 的关注！欢迎贡献代码、文档、数据源或投资建议。

---

## 📋 行为准则

- **理性讨论**：投资相关讨论保持理性、基于数据
- **风险提示**：所有投资建议必须包含风险提示
- **合规第一**：不得推荐具体产品，不得承诺收益
- **尊重他人**：保持友好、包容的讨论氛围

---

## 🚀 如何贡献

### 1. 报告问题 (Issues)

发现问题？请创建 Issue 并包含：
- 问题描述（清晰、具体）
- 数据错误（如数据不准确、来源过期）
- API 问题（如调用失败、数据格式变化）
- 复现步骤

### 2. 提交代码 (Pull Requests)

贡献代码前请：
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 3. 新增数据源

欢迎添加新的数据源：
- 数据来源必须是官方或权威渠道
- 提供 API 文档和使用示例
- 添加数据缓存机制
- 编写数据验证测试

### 4. 改进报告模板

优化报告模板：
- 增加新的分析维度
- 优化数据结构
- 补充使用示例

---

## 📝 代码风格

### 脚本规范

- Shell 脚本遵循 Google Shell Style Guide
- Python 脚本遵循 PEP 8
- 添加必要的注释和文档字符串
- 错误处理完善

### 数据规范

- 数据格式统一为 JSON
- 包含数据来源和时间戳
- 实现缓存机制（避免重复调用）
- 数据验证（检查完整性）

---

## 🔧 开发环境

### 前置要求

- OpenClaw v1.0+
- Python 3.8+
- Bash
- Git
- curl（API 调用）

### API 配置

```bash
# 设置 API Key（环境变量）
export QVERIS_API_KEY="your-api-key"
export TTFUND_API_KEY="your-api-key"

# 或使用配置文件
cp config/api_keys.example.json config/api_keys.json
# 编辑 config/api_keys.json 填入你的 API Key
```

### 本地测试

```bash
# 克隆仓库
git clone https://github.com/lj22503/investment-framework-skill.git

# 进入项目目录
cd investment-framework-skill

# 测试数据获取脚本
bash scripts/fetch-market-data.sh
bash scripts/fetch-northbound.sh

# 生成测试报告
bash scripts/generate-daily-report.sh
```

---

## ⚠️ 合规要求

**所有贡献必须遵守：**

- ❌ 不得推荐具体基金/股票
- ❌ 不得承诺收益/保本
- ❌ 不得使用"稳赚""必涨"等违规表述
- ✅ 必须包含风险提示
- ✅ 数据标注来源和时间
- ✅ 使用真实 API 数据，禁止模板填充

---

## 📖 资源

- [投资框架文档](docs/) - 详细文档
- [报告模板](docs/REPORT_TEMPLATES.md) - 报告结构说明
- [API 指南](DATA_API_GUIDE.md) - 数据 API 使用
- [OpenClaw 文档](https://docs.openclaw.ai) - OpenClaw 官方文档

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。贡献代码即表示你同意将贡献内容以 MIT 许可证发布。

---

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

**特别感谢：**
- 数据提供方（QVeris、东方财富、港交所等）
- 开源社区贡献者
- 投资建议审核者

---

## 📬 联系方式

- GitHub Issues: [提交问题](https://github.com/lj22503/investment-framework-skill/issues)
- 邮箱：[联系作者](mailto:your-email@example.com)
