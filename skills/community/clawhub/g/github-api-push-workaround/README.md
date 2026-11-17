[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

# github-api-push-workaround

## English

Root-cause troubleshooting and push templates for pushing git to GitHub / Gitee / AtomGit: 401 = credentials (a dead old PAT left in the helper chain); timeout / hang = channel (the proxy cuts git transport — use no_proxy direct connect); a wave of 401 = value-prefix pitfall (use `--raw` for the bare value). Includes direct-push templates (token via environment variable), the Git Data API fallback (blob→tree→commit→ref), Gitee private-to-public, and AtomGit backend gitcode notes.

### Who reads what
- **AI agent**: read `SKILL.md` (frontmatter name/description decide applicability; body = steps).
- **Human reader**: read `SKILL.md` and `AGENTS.md`.

### Files
- `SKILL.md` — main manual
- `AGENTS.md` — agent manual
- `llms.txt` — AI-readable index

## 中文

git 推 GitHub/Gitee/AtomGit 的根因化排查与推送模板：401=凭据问题（helper 链残留死旧 PAT）、超时/挂死=通道问题（代理掐 git 传输，须 no_proxy 直连）、大面积 401=取值前缀坑（--raw 取裸值）。含直连推送模板（令牌走环境变量）、Git Data API 兜底（blob→tree→commit→ref）、Gitee 私有转公开、AtomGit 后端 gitcode 等实测坑。

### 谁读什么
- **AI 代理**：读取 `SKILL.md`（frontmatter 的 name/description 决定是否适用；正文为执行步骤）。
- **人类读者**：读取 `SKILL.md` 与 `AGENTS.md`。

### 文件
- `SKILL.md` — 主说明书
- `AGENTS.md` — AI 代理说明书
- `llms.txt` — AI 可读索引
