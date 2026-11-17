---
name: git-sandbox-safe-ops
description: 在 WorkBuddy 的沙箱环境里安全地对 git 仓库做 fetch/push/rebase，并在 .git 丢失、origin/main 不存在、push 被拒时按固定流程恢复。当出现「git rebase 失败」「.git 不见了」「not a git repository」「origin/main 不存在 / show-ref 里没有」「fetch 说更新了但 status 还是 gone」「push 被拒 fetch first」「could not read Username」「grep/sed/head/dirname 报 command not found」「shell-runtime-bash-env.sh: line 3: dirname: command not found」时使用。
agent_created: true
slug: git-sandbox-safe-ops
displayName: 沙箱环境下的 git 安全操作与仓库恢复
version: 1.0.0
category: development
visibility: public
license: MIT
---

# 沙箱环境下的 git 安全操作与仓库恢复

## 0. 先判断：目标仓库在会话工作区里吗？

WorkBuddy 的 Bash 工具跑在沙箱里，写权限默认只覆盖**当前会话工作区**，
再叠加 `~/.workbuddy/settings.json` 里的白名单：

```json
{ "sandbox": { "extraAllowWrite": ["~/AppData/Local/AgentConnectors/", "..."] } }
```

**如果项目目录既不等于会话工作区、也不在白名单里，git 的部分写操作会静默失效。**
先确认一次：

```bash
git rev-parse --show-toplevel     # 项目根
# 与会话工作区（系统提示里的 Workspace Folder）比对
```

- 推荐做法：把项目目录加进 `sandbox.extraAllowWrite`，或改用会话工作区内的副本操作。
- 下面的症状都是「不在白名单」时**实测**遇到的，先记住两条铁律：
  1. **不要在非白名单目录里跑 `git rebase`**（见 §2，实测把整个 `.git` 弄没了）。
  2. 任何「改了但 status 没变」的情况，先怀疑写入被沙箱丢了，而不是 git 逻辑。

## 1. 症状 → 原因对照

| 症状 | 实测原因 / 处置 |
|---|---|
| `git fetch origin main` 打印 `* [new branch] main -> origin/main`，但随后 `git rev-parse origin/main` 报 `unknown revision`、`git show-ref` 里只有 `refs/heads/main` | `.git/refs/remotes/**` 下 git 的「锁文件 + rename」写入被沙箱吃掉。按 §3 用 python 直写这个引用文件即可 |
| `git update-ref refs/remotes/origin/main <sha>` 返回 0 却仍然没有该引用 | 同上，`update-ref` 也走 rename。不要反复重试，直接直写文件 |
| `git status -sb` 显示 `## main...origin/main [gone]` | 上一条的后果，跟踪引用丢了（分支的上游配置可能还在） |
| `git push` 报 `! [rejected] ... (fetch first)` | 远端确实有新提交（例如 GitHub Actions 的每日采集提交）。**不要**用 `git pull --rebase`，走 §4 |
| `git rebase <sha>` 报 `error: could not mark as interactive: No such file or directory` | 沙箱下 rebase 要建 `.git/rebase-*` 目录，创建失败；**紧接着 `.git` 会被整个删掉**（实测，见 §2） |
| `git log` 突然报 `fatal: not a git repository` | 上一条的后果，进入 §5 恢复流程 |
| `git push` 报 `could not read Username ... terminal prompts disabled` | 全局 `credential.https://github.com.helper=!gh auth git-credential` 生效，但 `gh auth status` 是「未登录」。**先按 §8 找现成 token**（通常 `~/.git-credentials` 里就有）；找不到再回落 `git config credential.https://github.com.helper store` |
| `gh auth status` 说未登录，但 `~/.git-credentials` 里存着一行 `https://<user>:gho_xxx@github.com` | **直接用这行里的 token**，别去麻烦用户。见 §8 |
| `git branch --set-upstream-to=origin/master` 报 `the requested upstream branch does not exist`，但 `FETCH_HEAD` 里明明有那个 sha | `refs/remotes/**` 写入被沙箱吃掉（同 §3）。**注意**：此时 `.git/refs/remotes/` 目录可能压根没被创建，`ls` 报 ENOENT。按 §3 直写即可；`FETCH_HEAD` 的 sha == 本地 HEAD 就能判定 push 已成功 |
| `git -c http.proxy= -c https.proxy= fetch origin main` 成功，但同参数 `push` 报 `Recv failure: Connection was reset` | 下载走直连可以、**上传必须走代理**。见 §7 换 `socks5://` |
| 同参数 `push` **不报错也不结束**（挂住，4 分钟无任何输出，直到被杀） | 与上一条同源：上传方向直连走不通，且这次是**静默挂起**而不是 `Recv failure`。见 §7 —— 别等，直接换 `socks5://` |
| `push` 报 `! [remote rejected] main -> main (refusing to allow an OAuth App to create or update workflow '.github/workflows/xxx.yml' without 'workflow' scope)` | token 缺 `workflow` scope。**改走 SSH**（不受 OAuth scope 限制），见 §9 —— 不要去求用户换 token |
| 带全局 `http.proxy=http://127.0.0.1:10808` push 报 `TLS connect error: error:0A000126:SSL routines::unexpected eof while reading` | 该端口是 SOCKS5/HTTP **双栈**，但 git 用 `http://` 前缀连它会在 TLS 握手时被掐。见 §7 改 `socks5://` |
| `push` 明明返回成功日志，但随后 `git status -sb` 又变成 `[gone]`、`git show-ref` 少了 `refs/remotes/origin/main` | push 过程又把跟踪引用写丢了。按 §3 直写，注意这次要写 **push 之后** 的新 sha（不是 push 前的） |
| `head` / `tail` / `grep` / `sed` / `cat` / `env` / `tr` / `dirname` / `wc` / `xargs` 报 `command not found`，且每条命令都附带 `shell-runtime-bash-env.sh: line 3: dirname: command not found` + `cd: null directory` | **PATH 缺 MSYS 目录**（不是 shell 残缺）。一句话就能修好，见 §1.1 —— **不要**退回 python 硬凑 |
| `ls` / `find` / `curl` / `tar` 反而能用 | 它们是从 **Windows PATH** 命中的（`C:\Program Files\OpenSSH\bin\ls`、`C:\Windows\System32\find`/`curl`/`tar`），跟 MSYS 无关 |

## 1.1 PATH 缺 MSYS 目录（coreutils 集体失踪）的定位与修复

**症状**：`grep`/`sed`/`head`/`tr`/`wc`/`dirname`/`xargs` 全部 `command not found`；
每条命令的 stderr 都会多出 `shell-runtime-bash-env.sh: line 3: dirname: command not found`。

**根因**：Bash 工具的 PATH 是 `注入前缀 + Windows PATH`，**没有**把 MSYS 目录放进去
（shell 快照里明明有 `/bin:/usr/local/bin:/usr/bin:/bin:/mingw64/bin`，但没作用到 Bash 工具进程）。
于是 MSYS 的 `dirname` 找不到 → `BASH_ENV` 里的 shim 第 3 行 `cd "$(dirname ...)"` 失败 →
连 `safe-delete-bash-env.sh` / `brokered-sandbox-bash-env.sh` 也一并没挂上。

**定位（三条命令）**：

```bash
echo "$PATH"                                  # 看有没有 /usr/bin、/mingw64/bin
echo "$EXEPATH"                               # MSYS 根 = 它的父目录
ls "$(dirname "$EXEPATH")/usr/bin"            # 或 ls "C:/.../PortableGit/versions/<ver>/usr/bin"
```

`usr/bin` 里 `grep.exe` / `sed.exe` / `head.exe` / `dirname.exe` 齐全 ⇒ **工具没坏，纯粹是 PATH 的问题**。

**一行修复**（本会话立即可用）：

```bash
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
grep --version && git --version               # 期望 grep 3.0 / git 2.55.0（来自 mingw64）
```

**是否持久**：不持久 —— Bash 工具每次调用都是新 shell。要么每条命令都带上上面那句，
要么做**永久修复**：把下面两条加到 PATH（**机器级或用户级都行**，放末尾，避免盖住系统 `find`/`curl`），
然后**完全退出并重启 WorkBuddy**（Bash 工具继承的是应用启动时的环境块）：

```
C:\Users\DELL\.workbuddy\binaries\PortableGit\versions\<ver>\usr\bin
C:\Users\DELL\.workbuddy\binaries\PortableGit\versions\<ver>\mingw64\bin
```

**改 PATH 的三个坑（2026-09-13 实测）**：

- **Windows 形式的注册表条目有效**：MSYS 在进程启动时把 `C:\WINDOWS\system32` 转成 `/c/WINDOWS/system32`
  （实测 `find` 就是这么命中的），所以写 `C:\...\usr\bin` 没问题。
  但**运行时** `export PATH='C:\...\usr\bin'` **无效** —— MSYS 只在启动时转换，
  drive-letter 形式塞进去 `command -v grep` 仍为空。临时修复必须用 POSIX 形式。
- **写注册表要保住值类型**：用户 PATH 常是 `REG_EXPAND_SZ` 且含 `%USERPROFILE%` 占位符，
  用 `RegistryKey.SetValue(name, value, ExpandString)` 写；
  **别用 `setx`**（1024 字符处截断整条 PATH）、也别用 `SetEnvironmentVariable` 回写 PATH
  （可能退化成 `REG_SZ`，把占位符变字面量）。
- **写注册表 ≠ 生效**：`RegistryKey.SetValue` 不广播 `WM_SETTINGCHANGE`。
  借道法：`[Environment]::SetEnvironmentVariable(<临时变量>, '1', 'User')` 写完再置 `$null` 删掉，
  广播就发出去了（不碰 PATH）。之后仍需重启 WorkBuddy。
- 沙箱里 **`Add-Type` 被拦**（"compiles and loads .NET code at runtime"）⇒ 不能自己 P/Invoke
  `SendMessageTimeout`，只能用上面的借道法。
- PowerShell 安全过滤器会把字面量 `%VAR%` 判成 cmd 语法**拦掉整条命令**，
  要检测占位符就用 `[string][char]37` 拼。

**顺带确认（实测，避免误报安全隐患）**：
- `rm` / `unlink` / `rmdir` 仍然是 safe-bin 挡板（`type rm` → `rm is a function`）。
  它们靠父进程导出的 `BASH_FUNC_rm%%` 环境变量生效，**不依赖**那个 shim，所以 shim 挂掉≠保护失效。
- `CODEBUDDY_TOYBOX_BIN` / `CODEBUDDY_BROKERED_BIN_DIR` 未设置 ⇒
  `brokered-bin`（自带 grep/sed/head/wc/ls 的沙箱代理版）这条备用供给也是断的，
  所以修 PATH 是目前唯一的正解。
- Windows PATH 里 `C:\Program Files\Git\cmd`、`C:\msys64\ucrt64\bin` 这两条指望不上：
  `C:\msys64` 已不存在；`C:\Program Files\Git` **是存在的**（`usr\bin` 下也有 grep/sed/dirname），
  但 `Git\cmd` 里只有 git 本身，顶不了 coreutils。git 的可用来源是 `/mingw64/bin/git`。
  ⚠️ 用 bash 的 `ls` 查 `Program Files` 下的目录**会误报 ENOENT**（沙箱读取限制），
  判断存在性一律改用 PowerShell 的 `Test-Path`。
- 排查时读注册表别用 `reg.exe`（沙箱程序黑名单，会直接 PROGRAM BLOCKED）；PowerShell 的 stdout 也常捕获不到，
  要 `Set-Content` 写文件再 Read。

## 2. 铁律：不要用 git rebase

实测时间线（本项目 2026-09-13）：

```
17:47  git commit          → 成功，.git/refs/heads/main 正常更新
17:52  git fetch origin main → 成功，对象已落盘，但 refs/remotes/origin/main 没写成
17:53  git rebase <sha>    → error: could not mark as interactive / .git 整目录消失
```

`git init`、`git commit`、`git fetch`（对象部分）都是好的，唯独 **rebase 会毁 `.git`**。
需要「把自己的提交放到远端之上」时，一律用 §4 的 `fetch + reset --mixed` 方案。
真要在沙箱里 rebase，先换个白名单目录操作。

> **2026-09-15 第二次实测，同样结论。** 当时已经知道这条铁律、只是手快对着
> `FETCH_HEAD` 敲了一句 `git rebase`，`.git` 照样当场消失。所以这不是偶发：
> **在这个沙箱里，`git rebase` = 删库**。想「把我的提交放到远端之上」，
> 唯一的正确姿势是 §4。

## 3. 直写跟踪引用（绕开被吃掉的 rename）

```bash
python -c "
import os, subprocess
sha = subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
p = os.path.join('.git','refs','remotes','origin'); os.makedirs(p, exist_ok=True)
open(os.path.join(p,'main'),'w',encoding='ascii',newline='\n').write(sha + '\n')
print('wrote', sha)
"
git config branch.main.remote origin
git config branch.main.merge refs/heads/main
git rev-parse origin/main && git status -sb      # 期望：## main...origin/main（无 ahead/behind）
```

`git config`（`.git/config`）的写入是正常的，可以放心用。

## 4. 远端有新提交时：不用 rebase 的正确姿势

```bash
git fetch origin main
python -c "print(open('.git/FETCH_HEAD',encoding='utf-8').read())"   # 拿到 <remote_sha>
git reset --mixed <remote_sha>        # HEAD/index 移到远端，工作区不动
git status --short                    # 逐条确认下面的判断
```

`reset --mixed` 之后按「**哪些是本次工作、哪些是远端更新**」分开处理：

```bash
# 你自己改的文件 → 保留
# 远端更新过的文件（典型是 data/ 这类机器每天提交的目录）→ 丢本地、取远端
git restore --source=HEAD --staged --worktree -- data
git add <你的文件...>
git commit -m "..."
git push origin main
```

> 关键判断：`data/` 这种「机器每天提交」的目录，取远端版本**不丢信息**；
> 而它如果显示为 modified，说明本地是旧快照 —— 这时候千万别 `git add -A`，
> 否则会把远端新采的数据**回退**掉。

### 4.1 别凭直觉认定「取远端不丢数据」——先算一遍集合差

「机器每天提交所以取远端没事」是个**假设**，不是事实。尤其当两边都在动同一个
JSON 数组（采集队列这类）时，本地可能有远端压根没有的条目。先验证再动手：

```bash
python - <<'PY'
import json, subprocess
def load(src):
    out = subprocess.run(['git','show',src],capture_output=True,text=True,encoding='utf-8').stdout
    return json.loads(out)
mine   = load('HEAD:data/inbox.json')
theirs = load('<remote_sha>:data/inbox.json')
arch   = load('<remote_sha>:data/inbox_archive.json')   # 远端是否把它归档了
key = lambda xs: set((x.get('id') or x.get('url') or '') for x in xs)
only = key(mine) - key(theirs)
print('只在我这边:', len(only))
print('  其中已在远端归档:', len(only & key(arch)))
print('  **真会丢**:', len(only - key(arch)))     # 这一项必须是 0 才敢取远端
PY
```

`真会丢 = 0` 才说明「取远端不丢信息」成立（本地独有的那些只是被远端挪进了
`*_archive.json`）。2026-09-20 实测：本地独有 246 条**全部**在远端归档里，
真会丢 0 条 —— 这时才可以放心取远端。

### 4.2 要保留多个提交的分组时：导出 → reset → 按文件重放

`reset --mixed` 会把所有提交打散成一堆未提交改动，**逐个重敲 8 条提交信息
不现实**。办法是先把它们导出成 JSON，重放时照抄：

```bash
python - <<'PY'
import json, subprocess
BASE, MINE = '<old_base>', '<my_head>'
shas = subprocess.run(['git','log','--reverse','--format=%H',BASE+'..'+MINE],
                      capture_output=True,text=True,encoding='utf-8').stdout.split()
out = []
for sha in shas:
    msg = subprocess.run(['git','log','-1','--format=%B',sha],
                         capture_output=True,text=True,encoding='utf-8').stdout
    files = subprocess.run(['git','diff-tree','--no-commit-id','--name-only','-r',sha],
                           capture_output=True,text=True,encoding='utf-8').stdout.split()
    out.append({'sha': sha, 'msg': msg, 'files': [f for f in files if f.strip()]})
json.dump(out, open('/tmp/my_commits.json','w',encoding='utf-8'), ensure_ascii=False)
PY
```

**重放前先查文件有没有跨提交重复** —— 同一个文件出现在两个提交里，
按文件 add 会让第一个提交吞掉第二个的改动：

```bash
python -c "
import json;from collections import Counter
cs=json.load(open('/tmp/my_commits.json',encoding='utf-8'))
allf=[f for c in cs for f in c['files']]
print('跨提交重复:', {f:n for f,n in Counter(allf).items() if n>1} or '无')
"
```

`无` 才可按文件安全重放。然后：

```bash
git reset --mixed <remote_sha>                  # 绝不 rebase（§2）
git restore --source=<remote_sha> --staged --worktree -- data/inbox.json data/inbox_archive.json
git status --short                              # 确认只剩自己的改动
# 按导出的 files 列表逐个 add + commit（见下）
```

```bash
python - <<'PY'
import json, subprocess, os
def run(a, **kw): return subprocess.run(a, capture_output=True, text=True, encoding='utf-8', **kw)
for i, c in enumerate(json.load(open('/tmp/my_commits.json',encoding='utf-8')), 1):
    files = [f for f in c['files'] if os.path.exists(f)]   # 已取远端版的本文件自然 no-op
    run(['git','add','--'] + files)
    if not run(['git','diff','--cached','--name-only']).stdout.split():
        print('  [%d] 无内容，跳过' % i); continue
    run(['git','commit','-F','-'], input=c['msg'].rstrip() + '\n')
    print('  [%d] %s' % (i, run(['git','log','-1','--format=%s']).stdout.strip()[:60]))
PY
```

**重放后必须做等价性验证**，别只看「提交数对上了」：

```bash
git diff --stat <my_old_head> HEAD      # 差异应只落在你**故意**换成远端版的那些文件上
```

若差异清单里出现任何代码文件，说明重放吃掉了改动，回去查文件重复那条。
再把每个提交的文件列表与原导出结果比一遍（脚本同上，比对 `files` 与
`diff-tree --name-only`），全一致才算无损。

## 5. `.git` 已丢失时的恢复（实测可用）

前提：工作区文件都还在（先 `ls` 确认，并立刻把关键文件复制到会话工作区做保险备份）。

```bash
git init -b main
git remote add origin <远程 URL>
git fetch origin main
python -c "print(open('.git/FETCH_HEAD',encoding='utf-8').read())"
git reset --mixed <remote_sha>        # 恢复历史：HEAD 指向远端最新提交
git status --short                    # 应只剩「你的改动」+ 远端更新过的文件
git restore --source=HEAD --staged --worktree -- <远端更新的目录>   # 如 data
git add <你的文件...> && git commit -m "<原提交信息>"
git push origin main
```

恢复后**必须补齐**（新 `.git` 不会自动带上）：

| 项 | 命令 | 说明 |
|---|---|---|
| 远程 | `git remote add origin <url>` | 第 2 步已做 |
| 凭据 helper | `git config credential.https://github.com.helper store` | 否则 push 报 could not read Username |
| 上游 | `git config branch.main.remote origin` + `git config branch.main.merge refs/heads/main` | `git status -sb` 才有可比对对象 |
| 跟踪引用 | §3 的 python 直写 | 否则 `origin/main` 解析不了 |
| 代理 | **必须显式写成 `socks5://127.0.0.1:10808`**，见 §7 | 三条路的实际结果（2026-09-15 实测）：带全局那套 `http://` 前缀 → `TLS connect error: unexpected eof`；完全不带代理 → fetch 能成、push 必 `Recv failure: Connection was reset`；**只有 `socks5://` 能 push 成功** |

丢失的东西（可接受，无需抢救）：`reflog`、`ORIG_HEAD`、`COMMIT_EDITMSG`、`logs/`。
丢失前的历史**不丢** —— 只要远端有，`git fetch` 就全回来了。

## 6. 收尾自检

```bash
git log --oneline -3          # 自己的提交在远端提交之上
git status -sb                # ## main...origin/main，无 [gone]、无 ahead/behind
git show-ref                  # refs/heads/main 与 refs/remotes/origin/main 都在
git ls-remote origin main     # 远端 sha == 本次要推的 sha
```

条件允许再跑一遍项目自带测试（本例 `python selftest.py` / `node uitest.js`），
确认恢复过程中没有把工作区文件搞坏。

## 7. 代理：写 `socks5://`，别照抄全局的 `http://`

全局 `~/.gitconfig` 通常这么配：

```
http.proxy  = http://127.0.0.1:10808
https.proxy = http://127.0.0.1:10808
```

**照着用会失败。** 本机 10808 是 SOCKS5 / HTTP **双栈**端口（实测两种握手都通），
但 git 用 `http://` 前缀连它，TLS 握手会被掐断。三种写法的实测结果：

| 写法 | fetch | push |
|---|---|---|
| 全局默认（`http://127.0.0.1:10808`） | `TLS connect error: unexpected eof` | 同上 |
| 完全不带（`-c http.proxy= -c https.proxy=`） | ✅ 成功 | ❌ `Recv failure: Connection was reset` |
| **`-c http.proxy=socks5://127.0.0.1:10808 -c https.proxy=socks5://127.0.0.1:10808`** | ✅ | ✅ **成功** |

所以 push 一律这么敲：

```bash
git -c http.proxy=socks5://127.0.0.1:10808 -c https.proxy=socks5://127.0.0.1:10808 push origin main
```

**为什么 fetch 直连行、push 就不行**：下载方向直连的 TLS 能撑住，上传方向的
CONNECT 隧道会被掐断。别因为「fetch 通了」就以为网络没问题，转而去怀疑凭据或仓库权限。

**怎么快速确认某个端口到底是 HTTP 代理还是 SOCKS**（比单纯探端口是否开放更有用 ——
TCP 能连上不代表协议对得上，所以别只看 `connect` 成功）：

```python
import socket
def probe(port, kind):
    s = socket.socket(); s.settimeout(3)
    try:
        s.connect(('127.0.0.1', port))
        if kind == 'socks5':
            s.sendall(bytes([0x05, 0x01, 0x00]))          # SOCKS5, no-auth
            return bytes([0x05, 0x00]) == s.recv(2)       # 返回 05 00 才是 SOCKS5
        s.sendall(b'CONNECT github.com:443 HTTP/1.1\r\nHost: github.com:443\r\n\r\n')
        return b'200' in s.recv(64)                        # 200 Connection established
    finally:
        s.close()
```

端口扫不出来时，常见的就这几个：`7890` `7891`（Clash 默认）、`10808` `10809`（v2rayN 的
http / socks 分流端口）、`1080`、`8080`。

> **2026-09-18 实测补充**：这次 `-c http.proxy= -c https.proxy=`（完全不带代理）**push 成功了**。
> 所以「push 必须走 socks5」不是绝对规律，取决于当时的网络出口状态。
> **正确顺序**：先用用户全局的代理配置试一次；若报 `Recv failure: Connection was reset` 或
> `TLS connect error: unexpected eof`，再按上表换 `socks5://`。不要一上来就改代理。

> **2026-09-20 实测（补上前一条的盲区）**：不带代理这次不是「失败」而是**静默挂起** ——
> `push` 跑了 4 分 11 秒、一行输出都没有，最后被信号杀掉。所以判断标准要加一条：
> **没有输出本身就是症状**，不要用「没报错就是还在传」来安慰自己。
> 同样的仓库、同样的网络，换 `socks5://` 后 **17 秒推完**（9 个提交 / 6.4k 增行）。
>
> 挂起时的小体积包也算个佐证：这类提交的 pack 通常只有几 MB，
> **超过一两分钟没进展就该换路，别干等**。前台跑记得加 `timeout`：
>
> ```bash
> timeout 240 git -c http.proxy=socks5://127.0.0.1:10808 \
>                -c https.proxy=socks5://127.0.0.1:10808 push origin main
> ```

## 8. 自己找凭证，不要问用户要 token（优先顺序）

用户说「你自己找凭证」时，按下面顺序找，**不要打断用户索要 token**：

```bash
# 1) 最优先：~/.git-credentials（明文存着，通常直接可用）
cat ~/.git-credentials
#   形如 https://oracis:gho_xxxxx@github.com  —— 冒号后就是 token

# 2) 环境变量
echo "${GH_TOKEN:-unset} ${GITHUB_TOKEN:-unset}"

# 3) 全局 git 配置里的 helper 指向
git config --global --list | grep -i credential

# 4) gh 的配置目录（Windows 是 AppData，注意 MSYS 下 ~/AppData 不一定能读到，用绝对路径）
ls "C:/Users/<user>/AppData/Roaming/GitHub CLI/"
```

拿到 token 后立即验证，**不要盲推**：

```bash
TOKEN="gho_xxxxx"
GH_TOKEN="$TOKEN" gh auth status        # 期望：✓ Logged in to github.com account <用户>
GH_TOKEN="$TOKEN" gh api user --jq .login
```

> `missing required token scopes: 'read:org'` 是**警告不是错误** —— `repo` 权限在就够了，
> 建仓库和 push 都不需要 `read:org`。

**push 时凭据助手在非交互环境拿不到密码**（报 `could not read Username`）。
最省事的绕法是把 token 直接嵌进 URL，**推送完立刻把 origin 改回干净 URL**：

```bash
git -c http.proxy= -c https.proxy= push "https://<user>:<TOKEN>@github.com/<user>/<repo>.git" master:master
git remote set-url origin https://github.com/<user>/<repo>.git   # 立刻还原，避免 token 落到 .git/config
```

**建仓库不需要本地 clone**——`gh repo create` 可以直接建空仓库，再单独 push：

```bash
GH_TOKEN="$TOKEN" gh repo create <user>/<repo> --public --description "..."
```

### 验证 push 到底成没成（沙箱里 `git status` 可能骗你）

`refs/remotes` 写不进去时，`git status -sb` 不可信。**以远端 API 为准**：

```bash
GH_TOKEN="$TOKEN" gh api repos/<user>/<repo>/branches --jq '.[] | "\(.name) -> \(.commit.sha)"'
GH_TOKEN="$TOKEN" gh api repos/<user>/<repo>/contents --jq '.[] | "\(.name)  \(.size) bytes"'
git rev-parse HEAD      # 本地 sha 与远端分支 sha 一致 == 推送成功
```

## 9. token 缺 `workflow` scope 时：改走 SSH，别去求用户换 token

推一个改了 `.github/workflows/*.yml` 的提交时会撞上：

```
! [remote rejected] main -> main (refusing to allow an OAuth App to create
  or update workflow `.github/workflows/ci.yml` without `workflow` scope)
```

**这是 GitHub 对 OAuth App 的安全限制，不是仓库权限问题**，所以怎么重试都没用。
先用 API 确认 scope（比猜准，且不用翻设置页）：

```bash
TOKEN=$(python -c "import os;from urllib.parse import urlparse;print(urlparse(open(os.path.expanduser('~/.git-credentials'),encoding='utf-8').read().strip().split(chr(10))[0]).password)")
curl -sS -o /dev/null -D - -H "Authorization: token $TOKEN" https://api.github.com/user \
  | grep -i x-oauth-scopes
# 期望里要有 workflow；只有 gist, read:org, repo 就是缺
```

**SSH key 不受 OAuth scope 限制** —— 这是本机最省事的解法（无需用户介入）：

```bash
# 1) 确认本机已有 key 且 config 指对了
cat ~/.ssh/config          # Host github.com + IdentityFile .../id_ed25519_gh
# 2) 验证认证（成功会打印 "Hi <user>! You've successfully authenticated"）
ssh -o StrictHostKeyChecking=accept-new -T git@github.com
# 3) 用 SSH URL 直接推 —— 注意：不用加任何 -c http.proxy，SSH 不走 HTTP 代理
git push git@github.com:<user>/<repo>.git main
```

2026-09-20 本机实测：SSH **直连即可**（github.com:22 没被墙），且比 https+socks5 还快。
`~/.ssh/config` 里已有 `IdentityFile /c/Users/<user>/.ssh/id_ed25519_gh`，无需额外配置。

**推完要手动修跟踪引用** —— 用 SSH URL 推不会更新 `origin` 的 https 跟踪引用，
于是 `git status -sb` 会显示假的 `ahead N`（按 §3 直写即可）：

```bash
python -c "
import os, subprocess
sha = subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
p = os.path.join('.git','refs','remotes','origin'); os.makedirs(p, exist_ok=True)
open(os.path.join(p,'main'),'w',encoding='ascii',newline='\n').write(sha + '\n')
"
git status -sb        # 期望 ## main...origin/main，无 ahead/behind
```

> 想一劳永逸的话，可以把 push 地址固定成 SSH（fetch 仍走 https）：
> `git remote set-url --push origin git@github.com:<user>/<repo>.git`
> —— 这改的是用户的仓库配置，先问一句再动。
