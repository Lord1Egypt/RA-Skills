# ClawHub发布检查清单

## ✅ 发布前检查

### 1. 环境检查

- [ ] **ClawHub CLI已安装**
  ```bash
  clawhub --cli-version
  ```
  预期输出：`🦞 ClawHub CLI v0.23.1`

- [ ] **已登录ClawHub**
  ```bash
  clawhub whoami
  ```
  如果未登录，执行：`clawhub login`

### 2. 文件完整性检查

- [ ] **核心文件存在**
  - [ ] `SKILL.md` - 主技能文档
  - [ ] `skill.json` - ClawHub元数据
  - [ ] `README.md` - 英文说明
  - [ ] `README_中文.md` - 中文说明
  - [ ] `.opencode/opencode.json` - OpenCode配置

- [ ] **脚本文件存在**
  - [ ] `scripts/note.py`
  - [ ] `scripts/loop_detector.py`
  - [ ] `scripts/generate_report.py`
  - [ ] `scripts/retrospect_ir.py`
  - [ ] `scripts/apply_updates_ir.py`

- [ ] **Playbook文件存在**
  - [ ] `playbooks/常见事件处置速查.md`
  - [ ] `playbooks/Linux应急响应现场手册.md`
  - [ ] `playbooks/Windows应急响应现场手册.md`
  - [ ] `playbooks/AI基础设施应急响应手册.md`
  - [ ] `playbooks/善后与横向定损检查单.md`
  - [ ] `playbooks/取证与证据规范.md`
  - [ ] `playbooks/CTF应急题解题模板.md`

- [ ] **多智能体文件存在**
  - [ ] `multi_agent/ARCHITECTURE.md`
  - [ ] `multi_agent/DEPLOYMENT_GUIDE.md`
  - [ ] `multi_agent/agents/ic_agent.yaml`
  - [ ] `multi_agent/agents/analyst_agent.yaml`
  - [ ] `multi_agent/agents/scribe_agent.yaml`
  - [ ] `multi_agent/agents/advisor_agent.yaml`
  - [ ] `multi_agent/workflows/standard_ir.yaml`
  - [ ] `multi_agent/framework/agent_framework.py`

- [ ] **8国语言README**
  - [ ] `README.md` (English)
  - [ ] `README_中文.md` (中文)
  - [ ] `README_日本語.md` (日本語)
  - [ ] `README_한국어.md` (한국어)
  - [ ] `README_Français.md` (Français)
  - [ ] `README_Deutsch.md` (Deutsch)
  - [ ] `README_Español.md` (Español)
  - [ ] `README_Português.md` (Português)

### 3. 隐私与安全检查

- [ ] **无个人信息**
  - 已检查所有Python脚本：✅ 无个人信息
  - 已检查所有YAML配置：✅ 无个人信息
  - 已检查所有JSON文件：✅ 无个人信息

- [ ] **无敏感数据**
  - 无硬编码的API密钥
  - 无真实的邮箱地址
  - 无真实的电话号码
  - 无密码或令牌

- [ ] **示例数据清晰标注**
  - 配置文件中的`email_addresses`、`api_keys`等字段为示例性配置

### 4. 元数据检查

- [ ] **skill.json完整**
  ```json
  {
    "name": "Corporate Emergency Response Guidance Skill",
    "slug": "corporate-emergency-response-guidance",
    "version": "1.0.0",
    "description": "...",
    "author": {...},
    "license": "MIT",
    "keywords": [...],
    "categories": [...]
  }
  ```

- [ ] **版本号正确**
  - 当前版本：1.0.0
  - 符合语义化版本规范

- [ ] **作者信息**
  - 组织名称：Enterprise Incident Response Team
  - 邮箱：incident-response@example.com（示例）

### 5. 功能测试

- [ ] **单智能体模式测试**
  ```bash
  python scripts/note.py --phase triage --set incident_name="Test"
  ```

- [ ] **多智能体框架测试**
  ```bash
  python multi_agent/framework/agent_framework.py
  ```

- [ ] **报告生成测试**
  ```bash
  python scripts/generate_report.py --out reports/test-report.md
  ```

### 6. 文档质量

- [ ] **主文档完整性**
  - SKILL.md包含完整的使用说明
  - 包含单智能体和多智能体两种模式
  - 包含AI基础设施应急内容

- [ ] **README质量**
  - 8国语言README完整
  - 快速开始指南清晰
  - 性能指标明确

- [ ] **代码注释**
  - Python脚本有完整注释
  - 关键函数有文档字符串

---

## 🚀 发布步骤

### Step 1: Dry Run（预览）

```bash
clawhub skill publish . --dry-run
```

检查输出，确认无误。

### Step 2: 实际发布

```bash
clawhub skill publish . \
  --slug corporate-emergency-response-guidance \
  --name "Corporate Emergency Response Guidance Skill" \
  --tags latest \
  --changelog "Initial release with multi-agent support"
```

### Step 3: 验证发布

```bash
clawhub skill inspect corporate-emergency-response-guidance
```

---

## 📋 发布后任务

- [ ] **验证在线展示**
  - 访问 https://clawhub.ai/skill/corporate-emergency-response-guidance
  - 检查描述、标签、分类是否正确

- [ ] **创建GitHub Release**
  - 标签：v1.0.0
  - 标题：Initial Release
  - 说明：包含多智能体支持、AI基础设施应急、8国语言文档

- [ ] **社区通知**
  - 在GitHub Discussions发布公告
  - 社交媒体分享（可选）

- [ ] **监控使用情况**
  - 关注GitHub Stars/Forks
  - 收集用户反馈
  - 监控Issues

---

## ⚠️ 常见问题

### Q1: ClawHub登录失败
**解决方案**：
```bash
clawhub login
```
按照提示完成设备流程登录。

### Q2: 发布权限不足
**解决方案**：
- 确认已创建ClawHub账户
- 确认账户有发布权限
- 如需组织发布，确认是组织成员

### Q3: Slug已被占用
**解决方案**：
- 修改`skill.json`中的`slug`字段
- 选择唯一的URL名称

### Q4: 文件过大
**解决方案**：
- 删除不必要的临时文件
- 压缩大型文档
- 使用`.clawhubignore`排除文件

---

## 📞 获取帮助

- **ClawHub文档**: https://docs.clawhub.ai
- **GitHub Issues**: https://github.com/your-org/corporate-emergency-response-guidance-skill/issues
- **社区支持**: https://discord.gg/clawhub

---

## ✅ 发布完成确认

发布成功后，请确认：

- [ ] Skill在ClawHub上可见
- [ ] README显示正确
- [ ] 安装测试成功
- [ ] 文档链接有效

**恭喜！你的Skill已成功发布到ClawHub！**

---

<div align="center">

**用AI赋能应急响应，让安全更高效**

Made with ❤️ by Enterprise Incident Response Team

</div>
