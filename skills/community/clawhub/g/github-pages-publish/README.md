# GitHub Pages 发布技能（Static Site Publisher）

把你**已经做好的网页**安全地发布到 GitHub Pages，生成谁都能打开的公开链接。

这是一个**通用技能包**，核心是纯 Python 脚本 `deploy.py`，不绑定任何特定平台——既可作为 AI 助手的技能使用，也能直接在命令行独立运行。

---

## 它能帮你做什么

- 手里有一个 HTML 网页文件，想发给别人看 → 一键发到网上，得到链接
- 有一个完整的网站文件夹 → 整站上线
- 只想开启自动发布 → 一步搞定

## 特点（为什么安全省心）

- **只新增、不误删**：只创建/更新你指定的文件，绝不覆盖或删除你之前发布的任何内容
- **不碰你电脑**：只读你指定的文件，不动其他任何本地文件
- **零依赖**：纯 Python 标准库，无需安装任何第三方包，也不需要 git

---

## 两种使用方式

### 方式一：作为 AI 助手技能使用（对话式）

本技能遵循通用 skill 规范（`SKILL.md`），可被以下平台加载：

- **WorkBuddy**
- **OpenClaw**
- 其他支持 skill 规范的 AI Agent 平台

安装：把 `github-pages-publish/` 文件夹放进对应平台的技能目录（例如 WorkBuddy 的 `~/.workbuddy/skills/`），然后在对话里直接说：

- 「把这个网页发到网上」
- 「部署这个 HTML 文件」
- 「帮我把这个文件夹上线成网站」
- 「生成一个能分享的网页链接」

### 方式二：直接命令行运行（不依赖 AI）

`deploy.py` 是纯 Python 脚本，任何装了 Python 的电脑都能直接跑：

```bash
# 发单个网页 → 生成独立链接
python deploy.py --file 页面.html --remote-path 页面.html --repo 仓库名 --token <令牌>

# 发整个网站文件夹 → 整站上线
python deploy.py --dir 网站文件夹 --repo 仓库名 --token <令牌>

# 只开启 Pages（文件已上传时）
python deploy.py --enable-only --repo 仓库名 --token <令牌>
```

令牌来源：`--token` 参数 > 环境变量 `GITHUB_TOKEN` > `GH_TOKEN`。

---

## 前提条件

| 条件 | 说明 |
|------|------|
| GitHub 账号 | 免费注册即可 |
| GitHub 令牌（PAT） | 需要「写文件」权限 |

### 生成令牌（约 1 分钟）

1. 打开 https://github.com/settings/tokens
2. 点「Generate new token」→「Generate new token (classic)」
3. 只勾选 **`repo`** 这一个权限
4. 生成后复制那串 `ghp_` 开头的字符

> ⚠️ 用完后可以去同一个页面删掉（Delete），更安全。

---

## 安全说明

- 免费版 GitHub Pages **全网公开**，任何人都能访问，**不要放敏感信息、客户数据、密钥**
- 本技能只做「发布已有文件」，不做后端、数据库、登录等动态功能
- 发布完成后建议撤销临时令牌

---

## 目录结构

```
github-pages-publish/（本仓库，即技能文件夹）
├── README.md              # 使用说明
├── SKILL.md               # 技能说明（给 AI 看的指令）
├── scripts/
│   └── deploy.py          # 部署脚本（三种模式，纯标准库）
└── references/
    └── pages-api.md       # API 参考 + 自定义域名 + 故障排查
```

---

## 常见问题

**Q：发布后打不开（404）？**
首次发布要等 1–3 分钟，稍等再刷新。

**Q：上传报 403？**
令牌缺写权限——fine-grained 令牌要把 Contents 改成 Read and write，或改用 classic 令牌勾 `repo`。

**Q：能绑自己的域名吗？**
可以，见 `references/pages-api.md` 的「自定义域名」小节。

**Q：更新网页后怎么让线上同步？**
重新发布一次即可，GitHub Pages 会自动刷新。

**Q：这个脚本只能在 WorkBuddy 里用吗？**
不是。`deploy.py` 是纯 Python，任何环境都能直接运行；`SKILL.md` 遵循通用 skill 规范，WorkBuddy、OpenClaw 等平台都能加载。
