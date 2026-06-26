# 贡献指南 🤝🐾

感谢你对 Investment Buddy Pet 的关注！欢迎贡献代码、宠物人格设计、或陪伴话术。

---

## 📋 行为准则

- **温暖友好**：保持宠物陪伴的温暖基调
- **合规第一**：不得推荐具体产品，不得承诺收益
- **尊重多样性**：12 只宠物代表不同投资风格，无优劣之分
- **建设性反馈**：提出问题的同时，欢迎提供解决方案建议

---

## 🚀 如何贡献

### 1. 报告问题 (Issues)

发现问题？请创建 Issue 并包含：
- 问题描述（清晰、具体）
- 宠物人格不一致
- 话术不当（如违规表述）
- 技术 bug（脚本错误、文件缺失）

### 2. 提交代码 (Pull Requests)

贡献代码前请：
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 3. 设计新宠物

欢迎设计新的投资宠物人格：
- 填写 `pets/template.json` 模板
- 设计独特的投资风格和沟通风格
- 编写代表性口头禅（10+ 条）
- 说明适合人群和使用场景

### 4. 优化陪伴话术

改进现有话术：
- 增加情绪安抚场景
- 优化历史数据引用
- 补充投资教育内容
- 保持宠物人格一致性

---

## 📝 代码风格

### 宠物配置 (pets/*.json)

```json
{
  "pet_type": "songguo",
  "name": "松果",
  "emoji": "🐿️",
  "investment_style": "谨慎定投",
  "communication_style": "温暖",
  "suitable_for": ["保守型新手", "安全感需求者"],
  "catchphrases": ["慢慢来，比较快", "囤积使人快乐"],
  "description": "一只谨慎的松鼠，喜欢慢慢囤积坚果..."
}
```

### 脚本规范

- Python 脚本遵循 PEP 8
- 添加必要的注释和文档字符串
- 错误处理完善
- 日志记录清晰

### 模板文件 (templates/*.md)

- 使用 Markdown 格式
- 包含必要的占位符（如 `{date}`, `{pet_name}`）
- 结构清晰，便于阅读

---

## 🔧 开发环境

### 前置要求

- OpenClaw v1.0+
- Python 3.8+
- Git

### 本地测试

```bash
# 克隆仓库
git clone https://github.com/lj22503/investment-buddy-pet.git

# 进入项目目录
cd investment-buddy-pet

# 测试宠物匹配脚本
python scripts/pet_match.py test

# 测试心跳引擎
python scripts/heartbeat_engine.py start --pet-type songguo

# 查看宠物配置
cat pets/songguo.json
```

---

## ⚠️ 合规要求

**所有贡献必须遵守：**

- ❌ 不得推荐具体基金/股票
- ❌ 不得承诺收益/保本
- ❌ 不得使用"稳赚""必涨"等违规表述
- ✅ 宠物陪伴不替代专业投资建议
- ✅ 市场波动时提供历史数据支持
- ✅ 引导用户学习投资框架，而非跟风操作

---

## 🎨 宠物设计指南

### 投资风格分类

| 风格 | 特点 | 代表宠物 |
|------|------|---------|
| 谨慎定投 | 慢慢积累，安全第一 | 松果🐿️、慢慢🐢 |
| 理性分析 | 数据驱动，逻辑严密 | 智多星🦉 |
| 激进成长 | 追求高收益，承受高风险 | 孤狼🐺 |
| 稳健配置 | 平衡风险收益 | 稳稳🐘、狐狐🦊 |
| 趋势交易 | 顺势而为，果断决策 | 鹰眼🦅 |
| 指数投资 | 被动投资，长期持有 | 豚豚🐬 |
| 集中投资 | 重仓少数标的 | 狮王🦁 |
| 分散投资 | 风险分散，稳健前行 | 蚁蚁🐜 |
| 逆向投资 | 别人恐惧我贪婪 | 驼驼🐪 |
| 成长投资 | 关注长期成长潜力 | 角角🦄 |
| 行业轮动 | 捕捉行业机会 | 马马🐎 |

### 沟通风格分类

- **温暖**：情感支持，安抚情绪
- **理性**：数据分析，逻辑推理
- **果断**：直接建议，不拖泥带水
- **平静**：平和语气，长期视角
- **机智**：幽默风趣，轻松交流
- **远见**：长期视角，战略思维

---

## 📖 资源

- [SKILL.md](SKILL.md) - 技能说明文档
- [README.md](README.md) - 项目介绍
- [pets/](pets/) - 宠物配置目录
- [scripts/](scripts/) - 脚本目录
- [templates/](templates/) - 模板目录
- [OpenClaw 文档](https://docs.openclaw.ai) - OpenClaw 官方文档

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。贡献代码即表示你同意将贡献内容以 MIT 许可证发布。

---

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

**特别感谢：**
- 宠物人格设计师
- 陪伴话术撰写者
- 合规审核者

---

## 📬 联系方式

- GitHub Issues: [提交问题](https://github.com/lj22503/investment-buddy-pet/issues)
- 邮箱：[联系作者](mailto:your-email@example.com)
