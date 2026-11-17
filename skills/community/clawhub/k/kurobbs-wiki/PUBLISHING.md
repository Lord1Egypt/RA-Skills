# 📤 kurobbs-wiki 发布操作清单（作者专用）

> 本文档是**作者本人**在发布/更新本 skill 到各市场时使用的操作清单。
> 面向使用者/读者的内容请看 [README.md](README.md)，这里不放。

---

## ✅ 发布前检查（每次发布前过一遍）

- [ ] `SKILL.md` frontmatter 完整：`name` / `description` / `license` / `metadata.author` / `metadata.version` / `metadata.tags` / `metadata.compatibility`
- [ ] `README.md` 里的安装命令已用真实仓库名（`npx skills add <owner>/kurobbs-wiki` 的 `<owner>` 已替换）
- [ ] `LICENSE` 文件存在，且与 `SKILL.md` 的 `license: MIT` 一致
- [ ] `scripts/*.py` 语法通过：
  ```bash
  python -X utf8 -c "import py_compile; py_compile.compile('scripts/wikiquery.py', doraise=True)"
  ```
- [ ] 隐私检查：`.gitignore` 已排除 `__pycache__/` 和 `~/.kurobbs-wiki-cache/`（账号数据），确保不误传

---

## 🚀 推送到 GitHub

本 skill 的公开仓库：`https://github.com/Alphamancer/kurobbs-wiki`

独立仓库在本地 `temp/_kurobbs_release/`。每次改完源文件后，把改动的文件复制过去再推送：

```bash
cd "D:\BaiduSyncdisk\agent demo2\cogni-agent\temp\_kurobbs_release"
git add -A
git commit -m "更新说明"
git push origin main
```

> ⚠️ 不要直接用 `git push` 推 cogni-agent 大仓库——市场以独立 skill 仓库为单位收录。

---

## 📦 提交到各市场

| 平台 | 方式 | 说明 |
|------|------|------|
| **SkillsMP** | 放在 GitHub 后提交仓库 URL | 自动爬取 GitHub，2 星以上收录 |
| **Skills.sh** | 放在 GitHub 后提交仓库 URL | 主分发枢纽，`npx skills add <owner>/<repo>` 收录 |
| **ClawHub** | `clawhub.ai` 直接上传 | 支持中文，MIT 无审核门槛，最快见效果 |
| **LobeHub** | `lobehub.com/zh` 提交 | 中文玩家为主，贴合鸣潮受众 |
| **awesome-claude-skills** | 提 PR 收录 | 开源权威榜单，长期曝光 |

安装命令统一：`npx skills add Alphamancer/kurobbs-wiki`

---

## 🔄 更新流程（skill 改版后）

1. 在 `skills/kurobbs-wiki/` 里改源文件（走 self-modify）
2. 复制改动的文件到 `temp/_kurobbs_release/`
3. `git add -A && git commit && git push origin main`
4. 各市场会自动抓取 GitHub 更新（ClawHub 等需手动重传的另说）

---

## ⚠️ 已知注意事项

- **私有 API 无官方文档**：库街区字段可能随版本变化，更新前先 `tree --refresh` 确认 API 仍可用。
- **别把密钥写进脚本**：目前脚本用公开无鉴权 API，无密钥风险；若以后加登录凭据，务必用环境变量，绝不硬编码。
