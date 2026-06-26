---
name: marila-skill-publish
description: 用于发布和更新 OpenClaw 技能到 ClawHub，并同步 GitHub Release。用户提到“发布技能”“发到 ClawHub”“发布这个 skill”“写完就发布”“上线这个技能”等场景时使用。包含完整发布步骤、版本规范、发布前检查清单、GitHub Release 同步规则和常见问题处理。
version: 1.0.8
metadata:
  openclaw:
    requires:
      bins:
        - clawhub
        - git
        - gh
    homepage: https://github.com/aliramw/dingtalk-ai-table
---

# ClawHub 技能发布流程

本文档总结了从 0 到发布一个 ClawHub 技能的完整流程和经验。

## 📋 前置要求

- Node.js >= 18
- `clawhub` CLI (`npm install -g clawhub`)
- Git
- GitHub CLI (`gh`)
- ClawHub 账号（已登录）
- GitHub 账号（用于 push 和 GitHub Release）

## 🧰 环境检查与补装

先检查命令是否存在：

```bash
which git
which gh
which clawhub
```

如果缺命令：

```bash
# macOS（推荐）
brew install git gh
npm install -g clawhub

# Ubuntu / Debian
sudo apt update
sudo apt install -y git gh
npm install -g clawhub
```

验证：

```bash
git --version
gh --version
clawhub --version
```

## 🔐 GitHub 鉴权与 Git 初始化

如果用户还没登录 GitHub，先做这个：

```bash
# 登录 GitHub CLI
gh auth login

# 验证登录状态
gh auth status
```

如果用户本机 Git 还没初始化身份，先配置：

```bash
git config --global user.name "你的名字"
git config --global user.email "you@example.com"
```

如果仓库还没绑远程：

```bash
git remote add origin https://github.com/<user>/<repo>.git
# 或
# git remote add origin git@github.com:<user>/<repo>.git
```

发布前最少确认这 4 件事：

```bash
git status
git remote -v
gh auth status
clawhub whoami
```

## ✅ 发布顺序（必须按此顺序，不能错）

发布前，**先检查** `references/clawhub-review-checklist.md`，确认元数据、README、脚本行为、凭证声明和示例参数已经一致。

1. **确定版本号** — 同步修改 `SKILL.md` 和 `package.json` 的 version 字段
2. **更新 CHANGELOG.md** — 在顶部追加新版本记录
3. **先过一遍 checklist** — 特别检查 `requires.bins` / `requires.env` / `primaryEnv` / 本地文件行为说明
4. **push + GitHub Release** — `git add -A && git commit && git push`，然后 `gh release create v0.x.x --title "v0.x.x" --notes "..."`
5. **发布到 ClawHub** — `clawhub publish <路径> --slug <名> --version x.x.x --changelog "..."`
6. **如需立即让当前 agent 使用最新技能定义，再手动同步到 agent 工作空间** — `cp <技能目录>/SKILL.md ~/.openclaw/workspace/skills/技能名/SKILL.md`

**硬规则：** 以后凡是发布 OpenClaw 技能，**每次 ClawHub 发布都必须同步创建对应的 GitHub Release**。不允许只发技能不发 release。

**新增硬规则：** 发布前必须过一遍 `references/clawhub-review-checklist.md`。尤其是带脚本、凭证、工作区文件读写的技能，不检查就发，极容易被 ClawHub 审核打回。

**敏感操作提示：** 同步到 `~/.openclaw/workspace/skills` 属于对 agent 工作区的写操作，只应在受信任环境中显式执行，不应在公共或不受信任场景下默认执行。

---

## 🚀 完整流程

### 1. 准备技能文件夹

```bash
# 创建技能目录
mkdir -p ~/my-skill
cd ~/my-skill

# 初始化 Git
git init
```

### 2. 创建必需文件

#### SKILL.md（必需）

```markdown
---
name: my-skill
description: 简短描述技能功能
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - MY_API_KEY
      bins:
        - curl
    primaryEnv: MY_API_KEY
    homepage: https://github.com/username/my-skill
---

# 技能说明文档

## 功能描述
...

## 使用方法
...
```

**⚠️ 关键：元数据必须准确声明**

ClawHub 安全分析会检查声明与实际代码是否一致：
- `requires.env` - 代码中引用的所有环境变量
- `requires.bins` - 代码中调用的所有 CLI 工具
- `primaryEnv` - 主要凭证变量名

#### package.json

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "技能描述",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/my-skill.git"
  },
  "clawhub": {
    "requiresBinaries": ["curl"],
    "credentials": [
      {
        "name": "MY_API_KEY",
        "description": "API 密钥说明",
        "docs": "https://example.com/docs"
      }
    ]
  }
}
```

#### README.md

```markdown
# my-skill

简短介绍。

## 安装

```bash
clawhub install my-skill
```

## 配置

1. 获取凭证...
2. 配置环境变量...

## 使用

...
```

#### CHANGELOG.md

```markdown
# Changelog

## [1.0.0] - 2026-02-27

### 新增
- 初始版本
```

### 3. 推送到 GitHub

```bash
git add -A
git commit -m "Initial commit"
git remote add origin https://github.com/username/my-skill.git
git push -u origin main
```

### 4. 发布到 ClawHub

```bash
# 方式一：直接发布
clawhub publish . --slug my-skill --name "My Skill" --version 1.0.0 --changelog "初始版本"

# 方式二：使用 sync（推荐）
clawhub sync
```

### 5. 验证发布

```bash
# 检查技能信息
clawhub inspect my-skill

# 查看网页
open https://clawhub.ai/username/my-skill
```

## ⚠️ 常见问题与解决方案

### 问题 1: `fetch failed` 错误

**症状：**
```
✖ fetch failed
Error: fetch failed
```

**原因：** 网络问题、服务端暂时不可达或本机登录状态异常

**解决：**
```bash
# 检查网络连接
curl -I https://clawhub.ai

# 重新登录
clawhub login
clawhub whoami
```

### 问题 2: `SKILL.md required` 错误

**症状：**
```
Error: SKILL.md required
```

**原因：**
- 文件不存在
- 文件名大小写错误（必须是 `SKILL.md` 或 `skill.md`）
- 当前目录错误

**解决：**
```bash
ls -la SKILL.md
pwd
clawhub publish /absolute/path/to/skill --slug my-skill ...
```

### 问题 3: 发布超时（Timeout）

**症状：**
```
✖ Timeout
Error: Timeout
```

**原因：** 服务器响应慢或网络问题

**解决：**
```bash
# 检查服务器状态
curl -I https://clawhub.ai

# 重试发布
clawhub publish . --slug my-skill ...

# 或使用 sync
clawhub sync
```

### 问题 4: 元数据不一致（审核失败）

**症状：** 审核反馈 "metadata mismatch"

**原因：** SKILL.md frontmatter 声明与实际代码不符

**解决：** 确保 frontmatter 准确声明：

```yaml
---
name: my-skill
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - ACTUAL_ENV_VAR_USED_IN_CODE
      bins:
        - actual_binary_used_in_code
    primaryEnv: ACTUAL_ENV_VAR_USED_IN_CODE
    homepage: https://github.com/username/repo
---
```

### 问题 5: ClawHub 登录失败

**症状：**
```
- Verifying token
✖ fetch failed
```

**解决：**
```bash
# 重新登录
clawhub login
clawhub whoami

# 如仍失败，在受信任环境中人工检查本机 ClawHub 登录状态
```

### 问题 6: `gh release create` 或 `git push` 失败

**常见原因：**
- 没安装 `gh`
- GitHub CLI 未登录
- Git 没配置 `user.name` / `user.email`
- 仓库没配置 `origin`
- 当前账号对仓库无 push 权限

**排查顺序：**
```bash
which gh
gh auth status
git config --global --get user.name
git config --global --get user.email
git remote -v
```

**解决：**
```bash
# 安装 gh
brew install gh

# 登录 GitHub
gh auth login

# 配置 Git 身份
git config --global user.name "你的名字"
git config --global user.email "you@example.com"

# 补 remote
git remote add origin https://github.com/<user>/<repo>.git
```

### 问题 7: `SKILL.md required` / `acceptLicenseTerms: invalid value`

**症状 1：**
```bash
Error: SKILL.md required
```

**先判断：**
- 如果目录里真的没有 `SKILL.md`，那就是路径或文件问题
- 如果目录里明明有 `SKILL.md`，但后续又报 `acceptLicenseTerms: invalid value`，那真正的问题通常不是技能文件缺失，而是 **ClawHub CLI 与服务端 publish payload 兼容有坑**

**症状 2：**
```bash
Publish payload: acceptLicenseTerms: invalid value
```

**结论：**
- 这类问题不要盲重试 `clawhub publish`
- 先确认：
  ```bash
  pwd
  ls -la
  sed -n '1,20p' SKILL.md
  clawhub whoami
  ```
- 如果 `SKILL.md` 存在、登录正常，基本可判定为 CLI publish payload bug，而不是技能目录缺文件

**兜底方案（实测可用）：**
1. 正常完成 `git push` 和 `gh release create`
2. 从本机 ClawHub 配置里读取 token：
   - macOS 实测路径：`~/Library/Application Support/clawhub/config.json`
3. 手工向 `https://clawhub.ai/api/v1/skills` 发 `multipart/form-data` 请求：
   - `payload` 内显式带：`slug`、`displayName`、`version`、`changelog`、`tags`、`acceptLicenseTerms: true`
   - 将技能目录中的文本文件逐个作为 `files` 上传
4. 发布成功后，用 `clawhub inspect <slug>` 验证最新版本

**规则更新：**
- 以后遇到 `acceptLicenseTerms: invalid value`，默认按 **CLI bug** 排查，不再把时间浪费在反复重试上
- GitHub Release 成功 + ClawHub CLI 失败，不代表技能不能发布；优先切到手工 API 发布兜底

### 问题 8: ClawHub 审核提示 metadata mismatch

**典型反馈：**
- 功能本身是对的
- 但 registry metadata 没声明实际依赖的二进制或环境变量

**高频遗漏项：**
- `requires.bins`
- `requires.env`
- `primaryEnv`
- `package.json` 里的 `requiresBinaries` / `requiredEnv` / `credentials`

**处理顺序：**
1. 对照代码、脚本、README、SKILL.md，列出真实依赖
2. 同步修复：
   - `SKILL.md` frontmatter
   - `package.json`
   - README / 示例命令
3. 升一个 patch 版本
4. 重新走：`git push` → `gh release create` → `ClawHub publish`

**硬规则：**
- 只要 skill 里用了 CLI、环境变量、本地沙箱目录，就必须把声明写全；不写全，审核很容易打回

## 📝 版本更新流程

```bash
# 1. 更新版本号
# 修改 SKILL.md frontmatter 中的 version
# 修改 package.json 中的 version

# 2. 更新 CHANGELOG.md
# 在顶部添加新版本记录

# 3. 提交并推送
git add -A
git commit -m "chore: bump version to 1.0.1"
git push

# 4. 先发 GitHub Release（必做）
gh release create v1.0.1 --title "v1.0.1" --notes "修复 xxx"

# 5. 再发布新版本到 ClawHub
clawhub publish . --slug my-skill --version 1.0.1 --changelog "修复 xxx"

# 或使用 sync（前提：GitHub Release 也要同步创建）
clawhub sync
```

## 🔐 安全注意事项

1. **凭证安全**
   - 不要在代码中硬编码密钥
   - 使用环境变量或 `mcporter config` 存储
   - 在 `.gitignore` 中排除敏感文件

2. **脚本审查**
   - 如果包含脚本文件，建议在文档中说明需要审查
   - 建议用户先在测试环境验证

3. **元数据准确性**
   - 准确声明所有依赖的环境变量和二进制文件
   - 这有助于安全分析和用户理解

## 📚 参考资源

- 技能格式规范：https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md
- 安全规范：https://github.com/openclaw/clawhub/blob/main/docs/security.md
- ClawHub 技能市场：https://clawhub.ai/skills

## 💡 最佳实践

1. **小步迭代** - 每次发布只做一个主要改动
2. **详细 Changelog** - 清晰记录每个版本的变更
3. **测试先行** - 在发布前充分测试技能功能
4. **文档完善** - 好的文档减少用户问题
5. **语义化版本** - 遵循 semver (major.minor.patch)

---

*最后更新：2026-02-27*
*作者：马锐拉 (@aliramw)*
