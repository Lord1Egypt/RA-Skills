# marila-skill-publish

马锐拉的 ClawHub 技能发布流程与经验总结，专门用于发布和更新 OpenClaw 技能到 ClawHub，并同步 GitHub Release。也覆盖 Git / GitHub CLI 安装、GitHub 鉴权、Git 初始化这些前置步骤。

## 📖 内容

本技能包含完整的 ClawHub 技能发布指南，基于实际发布 `dingtalk-ai-table` 技能的经验总结。

### 涵盖内容

- ✅ 完整的技能发布流程
- ✅ Git / GitHub CLI 安装说明
- ✅ GitHub 鉴权与 Git 初始化说明
- ✅ SKILL.md 元数据规范
- ✅ 常见问题与解决方案
- ✅ 版本更新流程
- ✅ 安全注意事项
- ✅ 最佳实践

## 🚀 使用

这是一个**文档技能**，主要用于参考和查阅。

```bash
# 安装技能
clawhub install marila-skill-publish

# 查看文档
cat ~/.openclaw/workspace/skills/marila-skill-publish/SKILL.md
```

## 📝 快速参考

### 发布命令

```bash
# 先发 GitHub Release（必做）
gh release create v1.0.0 --title "v1.0.0" --notes "更新说明"

# 再发布到 ClawHub
clawhub publish . --slug my-skill --version 1.0.0 --changelog "更新说明"

# 使用 sync 也一样：GitHub Release 不能省
clawhub sync
```

### 硬规则

- 发布任何 OpenClaw 技能时，**每次 ClawHub 发布都必须同步创建一个对应版本的 GitHub Release**
- 不允许只发技能、不发 release
- 发布前必须先检查 `references/clawhub-review-checklist.md`
- 如需同步到 agent 工作区，必须明确这属于敏感写操作，只在受信任环境执行

### 必需文件

- `SKILL.md` - 技能主文档（含 frontmatter 元数据）
- `package.json` - 包信息
- `README.md` - 使用说明
- `CHANGELOG.md` - 版本历史

### 关键元数据

```yaml
metadata:
  openclaw:
    requires:
      env: [YOUR_ENV_VAR]
      bins: [your-cli-tool]
    primaryEnv: YOUR_ENV_VAR
    homepage: https://github.com/user/repo
```

## 🔗 相关资源

- [ClawHub 过审 Checklist](references/clawhub-review-checklist.md)

- [ClawHub 技能市场](https://clawhub.ai/skills)
- [dingtalk-ai-table 技能](https://clawhub.ai/aliramw/dingtalk-ai-table)

---

**版本：** 1.0.0  
**作者：** 马锐拉 (@aliramw)  
**日期：** 2026-02-27
