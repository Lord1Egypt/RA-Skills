# 参与贡献

<p align="center">
  <strong>欢迎一起把这个 skill 做得更好 🐰</strong><br>
  <sub>无论是修个错别字、补充人格原型，还是改进整个 QA 流程，都非常欢迎</sub>
</p>

---

## 贡献方式

### 报告问题

提交 Issue 时请包含：
- OpenClaw 版本（`openclaw --version`）
- 具体触发了什么问题
- 期望行为 vs 实际行为
- 相关的 SOUL.md / SKILL.md 内容（如果涉及）

### 功能建议

直接开 Issue 描述你的想法。说清楚：
- 你在用什么场景
- 现在缺什么
- 理想的解决方案是什么

### 提交 Pull Request

```bash
# 1. Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/<your-username>/Multi-Agent-Orchestration.git
cd Multi-Agent-Orchestration

# 3. 创建分支
git checkout -b feat/my-improvement

# 4. 改完后提交
git add .
git commit -m "feat: 描述你的改动"

# 5. 推送并创建 PR
git push origin feat/my-improvement
```

---

## 特别欢迎的贡献方向

### 人格原型扩充
- 补充 `references/persona-library.md` 里缺少的角色
- 为特定行业提供专属人格建议（法律、医疗、教育等）
- 提供经过实测效果好的 SOUL.md 示例

### 提示词质量
- 从 prompts.chat 或其他来源补充更好的职责提示词
- 优化现有 Worker 模板的工作原则和输出格式
- 验证不同模型下人格激活的实际效果

### 访谈问题库
- 补充 `templates/interview_questions.md` 中特定行业的问题
- 优化问题措辞，让 AI 更容易提炼出有效信息

### 多语言支持
- 欢迎提交其他语言的 README 翻译
- 模板文件的多语言版本

### 真实案例
- 分享你用这个 skill 组建的团队配置
- 提供 examples/ 目录下的实际使用示例

---

## Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat:     新功能或新内容
fix:      修复问题
docs:     文档更新
refactor: 结构调整（不影响功能）
```

示例：
```
feat: 新增法律顾问人格原型
fix: 修正 Manager SOUL.md 模板中的 session key 错误
docs: 补充中文安装说明
```

---

## 行为准则

- 保持友善，欢迎不同水平的贡献者
- 对反馈保持开放
- 专注于让这个 skill 对使用者真正有用

---

<p align="center">
  <sub>感谢每一位贡献者 🐰</sub>
</p>
