# CONTRIBUTING · 发布检查清单

> 任何一次改动这个 skill（加卡、改卡、改 SKILL.md / references / gotchas / assets），
> 无论你是人还是 AI 助手，**发布前必须逐条走完下面 6 步**，缺一不可。
> 目的：防止"改了但没发出去""发了但没跑闸门""版本号对不上"这三类事故。

## 发布前 6 步清单

### 1. 跑隐私闸门（硬门槛，退出码语义）

```bash
<你的隐私闸门脚本路径> <本 skill 所在目录>
```

- **退出码 1**（隐私命中）→ 禁止发布，先清理
- **退出码 3**（有提示项）→ 看清楚是什么：
  - 若提示是「素材图需人眼确认」→ 图片是原创自生成、已去水印的，可以放行（图片正则扫不了是固有限制）
  - 若提示是「软署名 / 审核规避措辞」→ 必须清掉再发（否则 ClawScan 会判 suspicious）
- **退出码 0** 或"文本层 0 命中 + 仅剩图片提示" → 可发布

### 2. bump 版本（三处同步，一个都不能漏）

- SKILL.md frontmatter 的 `version`
- README.md 顶部的版本标注 + 「版本历史」段
- （ClawHub 的版本号在 publish 时用 `--version` 显式指定）

**规则**：加卡 = minor（+0.1，如 1.1.0 → 1.2.0）；改已有卡/修 bug = patch（+0.0.1）；架构大改 = major。

### 3. git commit + push（别只 commit）

```bash
cd <本 skill 所在目录>
git add -A
git commit -m "feat/chore: <说明>"
# 网络代理坑：若 push 报 HTTP2 framing / 502，用下面这条绕过
git -c http.version=HTTP/1.1 -c http.proxy= -c https.proxy= push origin main
```

**检查**：`git status` 应显示 `Your branch is up to date with 'origin/main'`，而不是 `ahead of ... by N commits`。

### 4. 重新 publish ClawHub

```bash
cd <本 skill 所在目录>
clawhub skill publish . --version <新版本> --changelog "<一句话说明>"
```

**检查**：`clawhub inspect marketing-poster-recipes` 应显示 `Latest = <新版本>` 且 `Moderate CLEAN`。
（刚 publish 后会有几分钟 pending.publication 的扫描窗口，属正常。）

### 5. 打包 zip 回传资料库

打包要求：zip 第一层直接是 `SKILL.md`（不能多套一层目录），跳过 `.git` 和隐藏文件。

```bash
cd <本 skill 所在目录>
python3 -c "
import zipfile, os
out = '/tmp/marketing-poster-recipes-v<VERSION>.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk('.'):
        if '.git' in root: continue
        for f in files:
            if f.startswith('.'): continue
            full = os.path.join(root, f)
            z.write(full, os.path.relpath(full, '.'))
"
```

然后回传资料库原节点（外层只留最新一个 zip）。

### 6. 回写工作区记忆

把本次改动（加了几张卡、版本号、push/publish 状态）写进工作区记忆的当日日志，
这样其它对话醒来能看到"这个 skill 刚动过、当前是什么状态"。

## 三类事故的"急救"对照

| 症状 | 诊断 | 处理 |
|---|---|---|
| `git status` 显示 ahead of origin | 只 commit 没 push | 走第 3 步 push |
| ClawHub `Latest` 是旧版本 | 改了没重新 publish | 走第 4 步 |
| 版本号三处不一致 | bump 漏了某处 | 走第 2 步补齐 |
| 新案例图带水印 | 生图后没去水印 | 用图片处理 erase 去水印，再回第 1 步跑闸门 |

## 一句话心法

**改动 ≠ 发布。发布 = 闸门 + 版本 + push + publish + 归档，五件套一个不能少。**
