# 仓库元数据：About / Topics / Release / Social preview

> 这些是 GitHub 页面上"仓库名以外"的全部信号，也是搜索与 AI 抓取最先读到的东西。文案可直接复制。

## 1. About description（仓库右上角）

GitHub 只显示一行、约 350 字符，截断前要说完。两个版本，二选一（英文覆盖面更广，中文转化更高）：

**中文（推荐，你的受众主要在国内）**

```text
把 Markdown 排成微信公众号图文并推进草稿箱 · Agent Skill + CLI · 离线生成 / 一键 push · 纯脚本无大模型 · MIT
```

**英文**

```text
Type Markdown, get a WeChat Official Account article in the draft box — inline HTML, editorial cards, native SVG folds, 1800x766 cover. Agent Skill + CLI, pure script, MIT.
```

要点：前 12 个字里必须出现"微信公众号"和"Markdown"，因为这是别人输入的两个词。

## 2. Topics（上限 20，建议填满 12 个）

```text
wechat
wechat-official-account
wechat-mp
微信公众号
markdown-to-wechat
typesetting
publisher
draft
svg-fold
agent-skill
claude-skill
ai-skill
```

保留原有的 `wechat / markdown / publisher / svg-fold / ai-skill`，其余是新增。中文 topic 能命中中文搜索，别删。

## 3. Homepage

第一周先填博客上的案例页（`https://shxuk.cn/...`），等 `skills.sh` 收录后改成 `https://skills.sh/shxuk/mpress`。空着是最亏的状态。

## 4. Release v1.2.0

打 tag 的意义不在版本号，在于让目录站、AI 和路过的开发者看到"这项目还活着"。release notes 直接贴：

~~~~markdown
## mpress 1.2.0

更名发布：`wechat-article-publisher` → **mpress**（旧地址 301 重定向，star / issue / 提交历史全部保留）。

### 安装

```bash
npx skills add shxuk/mpress     # 装进 Claude Code / Cursor / Codex 等
npm i -g mpress                 # 或当 CLI 用
```

### 这一版改了什么

- 仓库、Skill 名、CLI 标识统一为 `mpress`
- README 重写：30 秒上手、实测耗时、能力边界、FAQ
- 明确运行时**不调用大模型**：渲染是纯脚本，同输入同输出
- 修掉 `SKILL.md` 里指向不存在文档的死链

### 实测

排版环节：手工 30 分钟 – 2 小时 → `mpress push` **5 秒左右**（从回车到草稿出现在后台）。

完整变更：https://github.com/shxuk/mpress/commits/main
~~~~

命令：

```bash
git tag -a v1.2.0 -m "mpress 1.2.0"
git push origin v1.2.0
```

（AGENTS.md 规定 push 前必须先 `git status` 审查，这条纪律不变。）

## 5. Social preview（1280×640）

这是链接被转发到微信群、X、Slack 时的缩略图。默认是灰块，等于白丢一次点击。

构图（左图右字，2 秒能读完）：

```text
┌────────────────────────────────┬──────────────────────────────┐
│                                │  mpress                      │
│   手机端文章截图（竖版）         │  把 Markdown 排成公众号图文    │
│   裁切到 55% 宽，右边出血         │                              │
│   ← assets/preview-components   │  手排 30 分钟 – 2 小时         │
│      .png 取中间一段             │  → 一条命令 5 秒               │
│                                │                              │
│                                │  Agent Skill · MIT · 纯脚本    │
└────────────────────────────────┴──────────────────────────────┘
```

规则：

- 字号按 1280 宽来定：主标题 72–88px，副标题 36–44px，最小不低于 28px（缩略图会再缩一次）。
- 底用 `#007275`（主题墨青）压 88% 不透明，文字纯白，最稳。
- **不要**把 README 的 badge、二维码、GitHub logo 塞进去，缩略图里全是噪点。
- 上传路径：仓库 → Settings → General → Social preview → Upload。

## 6. 顺手做掉的两项设置

- **Settings → Features → Discussions** 打开。目录站和 AI 会把"有 discussion"读成活跃信号，成本为零。
- **Issues** 加两个模板（`.github/ISSUE_TEMPLATE/`）：`排版问题`（附源 Markdown 片段）、`推送失败`（附退出码）。你现在的 FAQ 里写"带着文章样例来提 issue 最好"——模板就是这句话的落地。

## 7. 打勾清单

- [ ] About description 换成新版
- [ ] Topics 补齐 12 个
- [ ] Homepage 填上
- [ ] Social preview 上传 1280×640
- [ ] 打 `v1.2.0` tag 并发 release notes
- [ ] Discussions 打开
- [ ] issue 模板加到 `.github/`
