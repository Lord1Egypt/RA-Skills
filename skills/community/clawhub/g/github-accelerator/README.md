# github-accelerator

> GitHub 访问加速技能：直连优先 · 镜像兜底 · 用前探测
> An Agent Skill that keeps GitHub usable when `github.com` is slow or blocked (common on CN networks): direct-first, with automatic fallback to verified mirrors for clone / raw files / releases.

`SKILL.md` 遵循开放 Agent Skills 标准（Anthropic 发起，OpenClaw / Claude Code / Hermes / Codex 等通用），核心逻辑封装在自包含脚本 `gh_accel.sh` 中，仅依赖 `bash + curl + git`。

---

## 背景

2026-09 实测（腾讯云服务器，CN 网络）：`api.github.com`、git HTTPS、各 GitHub CDN（raw/objects/codeload）**直连可用**，唯独 `github.com` 网页与 git 端点**间歇超时**（约 80% 失败率；DNS 固定解析到一个本身不通的 IP，改 hosts 无效）。国内镜像站因此成为刚需——但这类站点**寿命以月计**，需要梯次备份 + 用前探测。

## 特性

- **gh CLI / API 永走直连**——`api.github.com` 基本不受网络干扰，是最高优先级通道
- **网页内容绕过网页**——README / 源文件用 `gh api` 直连取，不看 github.com 页面
- **下载自动降级**：直连 → `ghfast.top` → `gh-proxy.com`
- **clone 自动降级**：直连 → `gitclone.com` → `gh-proxy.com`
- **传输安全护栏**：仅接受 GitHub 官方域名 URL；拒绝查询串/内嵌凭据；先写临时文件、拒绝覆盖已有文件；支持 `--sha256` 校验通过才落盘
- **clone 目录保护**：目标目录已存在且非空时直接拒绝，失败清理只用非递归 `rmdir`
- **本地私有代理**：`~/.config/gh-accelerator/proxies.conf` 一行接入自建域名，自动优先于公共镜像（见 SKILL.md §5.1）
- **`check` 实时探测**：直连 + 全部下载镜像 + clone 通道，一目了然
- **已知死亡镜像黑名单**，附于 SKILL.md 与脚本注释，避免重复踩坑

## 安全与隐私

公共镜像本质是**不可信第三方转发方**：它们能看到完整仓库 URL、客户端 IP 和访问时间，也可能截断或篡改下载内容。因此：

- 只用于**公开仓库的只读内容**；私有仓库、Release 附件中的敏感产物不要走公共镜像
- 绝不把带 token/凭据的 URL 交给镜像（脚本会拒绝查询串与内嵌凭据）
- 下载后用官方公布的 sha256 校验：`gh_accel.sh dl --sha256 <hash> <url>`
- 经镜像 clone 后先确认 `git remote get-url origin`，push 前务必 `set-url` 回官方源
- 更信任自建代理时优先用 `~/.config/gh-accelerator/proxies.conf` 接入
- 本技能**不执行任何仓库写入**（push / commit / ref 更新均不在此范围内）

## 目录结构

```
github-accelerator/
├── SKILL.md            # 技能本体（跨 Agent 的 SKILL.md 标准格式）
├── README.md
└── scripts/
    └── gh_accel.sh     # 自包含加速工具
```

## 安装

把整个目录拷贝到目标 Agent 的 skills 目录：

| Agent | 目录 |
|---|---|
| Hermes Agent | `~/.hermes/skills/web/github-accelerator/` |
| OpenClaw | `~/.openclaw/skills/github-accelerator/` |
| Claude Code | `~/.claude/skills/github-accelerator/` |
| 其他支持 Agent Skills 的 Agent | 装到其个人 skills 目录（格式同标准，零修改） |

或发布后一键安装（ClawHub）：

```bash
clawhub install github-accelerator
```

## 快速开始（30 秒）

```bash
# 1. 探测当前网络下直连与镜像的实时状态（每台机器网络不同，先跑这个）
scripts/gh_accel.sh check
```

预期输出：

```
== 直连探测 ==
  ✓ api.github.com/zen (200)
  ✓ codeload.github.com/... (200)
  ✗ github.com/ (000)
== 下载镜像（拉测试文件验内容）==
  ✓ ghfast.top
  ✓ gh-proxy.com
  ✗ ghproxy.net
== clone 镜像（ls-remote 探测公开仓库）==
  ✓ https://gh-proxy.com/https://github.com
```

```bash
# 2. 下载文件（自动降级；--sha256 校验通过才落盘）
scripts/gh_accel.sh dl --sha256 <official-hash> \
  https://github.com/OWNER/REPO/releases/download/v1.0.0/app-linux-amd64

# 3. 克隆仓库（自动降级）
scripts/gh_accel.sh clone OWNER/REPO

# 4. 克隆走官方源失败时，看 README/单文件内容（需 gh CLI）
gh api repos/OWNER/REPO/readme --jq .content | base64 -d
```

完整命令参考见 SKILL.md（`dl` / `clone` 均支持 `--no-direct` 强制走镜像链，便于测试；`GH_ACCEL_LANG=en` 可切换英文输出）。

## 新机器首次使用

1. **先跑 `check`**——直连基线因机器/网络而异，不要套用本文档的结论
2. 下载失败看输出停在哪一站，`check` 定位是镜像死了还是直连抽风
3. 镜像全灭时：编辑 `scripts/gh_accel.sh` 顶部的 `DL_PROXIES` / `CLONE_PROXIES` 数组换站

## 镜像梯次维护（镜像站易死，务必定期探测）

| 用途 | 梯次（脚本自动按序尝试） | 2026-09-08 实测 |
|---|---|---|
| 文件下载 | ghfast.top → gh-proxy.com | ✅ 稳定 / ⚠️ 波动 |
| 仓库克隆 | gitclone.com → gh-proxy.com 前缀 | ⚠️ 冷缓存 502 / ✅ |
| 网页浏览 | 不要依赖镜像：用 gh api 取内容；要渲染页面让本机浏览器看 | kkgithub / bgithub 实测 clone 404、超时 |
| 已死勿用 | ghp.ci · ghgo.xyz · ghproxy.com · hub.fastgit.org（ghproxy.net 大文件限流） | 已确认 |

找新镜像：`ghproxy.link`（gh-proxy 官方域名发布页）+ 近期「github 加速」文章；**候选必须真实文件 + sha256 实测通过**才可写入梯次。

## 限制与边界

- 收益范围：仅 github.com 网页/端点被干扰的环境；`api.github.com` 不通的网络本技能无法救治（那是更彻底的封锁）
- **镜像只读**：经镜像 clone 后，remote 指向镜像地址，push 前必须 `git remote set-url origin https://github.com/OWNER/REPO.git`
- **本技能只读**：不提供 push、API 提交或 ref 更新通道；`gh api` 示例仅限只读 GET
- `gh api` 取内容依赖目标机器装有并登录 gh CLI；`dl`/`clone` 脚本只需 bash + curl + git
- 不修改全局 git 配置（不写 `url.insteadOf`），全部为单命令级操作，可审计、可回滚

## FAQ / 排错

| 症状 | 原因与处理 |
|---|---|
| `check` 某站显示 `000` | 该通道当前不可达（超时/被墙）。等几分钟重试；确认多次失败则从梯次中移除 |
| 下载全部通道失败 | 跑 `check` 看存活情况 → 换新镜像写入脚本顶部数组 |
| gitclone.com clone 报 502 | 该站冷缓存/不稳定，属正常现象；脚本自动跳到下一镜像，或稍后重试 |
| 直连明明通了却走了镜像 | 直连首试偶发超时即降级——符合设计（重试成本 < 长时间挂起） |
| 经镜像 clone 后 push 报认证失败 | remote 还是镜像地址；按脚本提示 `set-url` 回官方源再 push |
| 有自己的加速域名想接入 | 写入 `~/.config/gh-accelerator/proxies.conf`（模板见 `templates/`），自动优先于公共镜像 |

## License

MIT-0（ClawHub 平台统一要求；本技能无任何附加条款）。分发到其他平台时以平台规定为准，如需 MIT 署名版请自行 fork 调整 frontmatter。
