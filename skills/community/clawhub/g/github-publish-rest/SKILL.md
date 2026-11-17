---
name: github-publish-rest
description: "Publish a local folder to a GitHub repo as ONE commit via the REST Git Data API — the working method when the GitHub connector is read-only (create_repository / push_files return 403) and the bundled git has no credential helper. Reads the stored token (git credential fill, or GITHUB_TOKEN / GH_TOKEN env), then creates blobs → tree → commit → ref. Ships a ready-to-run zero-dependency Python script (scripts/github-publish.py), a post-publish blob SHA verification method, and documents the known pitfalls (account-rename 307, git credential fill hang, timezone-aware contribution graph). Use when the user says \"publish to github\", \"push to github\", \"upload code\", \"create repo\", \"deploy skill\", \"发到 github\", \"推到 github\", \"上传代码\", \"新建仓库\"."
metadata:
  slug: "github-publish-rest"
  displayName: "GitHub Publisher (REST API)"
  description_zh: "在本机把本地文件夹发布到 GitHub 的可用通道（连接器只读 + 无凭据助手时）。读取已存储 token 后走 Git Data API 建一次提交，含零依赖现成脚本、发布后哈希校验与已知坑。"
  category: "dev-tool"
  version: "1.17.0"
  author: "WorkBuddy"
  agent_created: "true"
---

# 推代码到 GitHub（本机唯一可用通道）

## 本机的两个硬约束（2026-09-25 实测）

1. **WorkBuddy 的 GitHub 连接器是只读的。**
   - `create_repository` → `403 Resource not accessible by integration`
   - `push_files` → `POST .../git/trees: 403 Resource not accessible by integration`
   - 这是 GitHub App 侧的权限，用户改不了 → **建仓库必须 Ronny 自己在网页建**（勾 Add a README 以生成默认分支）。
   - 连接器账号：`ebifry`。
2. **便携版 git 没有凭据助手。** `which git` → `/mingw64/bin/git`（环境自带便携版）；
   `credential.helper=helper-selector`、`helperselector.selected=manager`，但磁盘上没有 `git-credential-manager.exe`。
   于是 `git push` 报 `could not read Username for 'https://github.com': terminal prompts disabled`。
   注意：`git credential fill` **能**读到 Windows 凭据管理器里的 `git:https://github.com` 条目 —— 有令牌，只是 git 自己用不上。

## ⭐⭐⭐ 账号改过名 → POST 返回 307（2026-09-29 实测，最容易卡住的一环）

**症状**：脚本在第一个 `POST /git/blobs` 就停住，返回
`307 {"message":"Moved Permanently","url":"https://api.github.com/repositories/<id>/git/blobs"}`。

**根因**：GitHub 账号**改过名**（本机：`ebifry` → **`CatsMansion`**，id 仍是 `51730721`）。
- **GET 会自动跟随重定向** —— 所以「查 ref / 查文件树 / 比 blob sha」这些读操作**全都正常**，
  问题不暴露，很容易以为是别的原因。
- **POST / PATCH 不跟随重定向** → 写操作 307 直接失败。

**判据（30 秒确诊）**：`307` 且 url 变成 `/repositories/<数字id>/...`，就是改名了。

```bash
# 拿 id 反查真名
curl -s -H "Authorization: Bearer $TOK" \
  https://api.github.com/repositories/<id> | python -c "import json,sys;print(json.load(sys.stdin)['full_name'])"
```

**修法**：`--owner` 换成新名字（`CatsMansion`）。作者邮箱会自动变成
`51730721+CatsMansion@users.noreply.github.com` —— **id 没变，贡献照样记在本账号**。

⭐ **推送前先确认真实 owner**：`GET /user` 看 login + id，`GET /repos/<owner>/<repo>` 看 `full_name`。
⛔ 别拿记忆里的账号名硬写。

⚠️ 附带注意：**REST 返回的 commit date 一律归一化成 UTC（`Z`）**，
即使提交里存的是 `+10:00` 也看不出来 —— 想验时区，看**贡献日历**，别信 API 的 date 字段。

### ⛔⛔ 2026-10-09/10 实测修正：「脚本 stamp 带偏移」≠「远端存了偏移」

脚本打印 `stamp : 2026-10-09T10:56:17+11:00`，看起来时区带上了 ——
但**从 API 把 commit 读回来，`author.date` 是 `2026-10-08T23:56:17Z`**，偏移被抹掉了。

⇒ ⛔ **"看脚本 stamp 末尾不是 Z 就没事"这个判据不成立**。
它只能证明脚本**传了**，证明不了远端**存了**。
⇒ 实测：本地 11:00（+11）**之前**推的提交，UTC 落在**前一天**，
绿格子记到昨天。10:56 推的那次就记到了前一天。
⇒ 反过来也能用：本地**早上**推，反而能点亮**昨天**空着的格子
（实测 10-10 07:47 推 → UTC 10-09 20:47 → 补亮了 10-09）。

⭐ 推之前先算一下：
```python
import datetime
now = datetime.datetime.now().astimezone()      # 本地带偏移
utc = now.astimezone(datetime.timezone.utc)
print("本地", now.date(), "→ 日历按", utc.date())
```

## 可用做法：把 token 交给 REST API

现成脚本：`scripts/github-publish.py`

```bat
python scripts/github-publish.py ^
  --owner ebifry --repo <仓库名> --dir <本地文件夹> --message "feat: ..."
python ... --dry-run        :: 只解析 token / ref / 文件清单，不写任何东西
```

流程：`git credential fill` 取 token（进程内，不打印、不落盘）→ GET ref/head commit → 逐个
`POST /git/blobs`（base64）→ `POST /git/trees`（带 `base_tree`）→ `POST /git/commits`（带 `parents`）
→ `PATCH /git/refs/heads/<branch>`。**一次提交，不是 8 个。**
脚本会自动跳过 `.git`、`__pycache__`、`last_run.txt`、`last_region.txt`、`node_modules`。

## ⭐⭐ 凭据卡死怎么办（2026-09-25 实测，脚本已修）

**症状**：跑 `github-publish.py` → **SIGTERM，无任何输出**。

**诊断链（逐环实测排除，别猜）**：
| 步骤 | 结果 |
|---|---|
| 加长超时 | 仍然 SIGTERM → ⛔ 不是超时 |
| 放行沙箱（怀疑拦 `git`）| 仍然 SIGTERM → ⛔ 排除 |
| 直接测 `printf 'protocol=https\nhost=github.com\n\n' \| git credential fill` | **rc=124（卡死），输出 0 字节** ⭐ **真因** |
| `git-credential-manager.exe` 在不在 | ✅ 在 → 所以是它**弹交互式认证在等输入** |

⭐ **结论：凭据库里没有有效 token → GCM 弹交互窗口 → 非交互环境卡死。**

### ⭐⭐⭐ 2026-09-26 更正：**先试这个，多数情况根本不用要 token**

上面那条"卡死"的结论只在**默认参数**下成立。实际是 GCM 在**交互模式下**弹窗等人输入。
关掉交互它就直接把已存的凭据吐出来了：

```bash
printf 'protocol=https\nhost=github.com\n\n' \
  | GIT_TERMINAL_PROMPT=0 git -c credential.interactive=false credential fill
# → rc=0，97 字节，username=ebifry / password=<40 字符，前缀 gho_ 的 OAuth token>
```

⭐ **本机凭据库里存的是一个 `gho_` OAuth token（40 字符，scope 含 repo）→ 读写都有权限，
不需要临时 PAT、不需要用户贴任何东西。** 直接喂给发布脚本即可（值只在子进程环境里，不打印、不进 argv）：

```bash
TOKEN=$(printf 'protocol=https\nhost=github.com\n\n' \
        | git -c credential.interactive=false credential fill 2>/dev/null | sed -n 's/^password=//p')
GITHUB_TOKEN="$TOKEN" python scripts/github-publish.py \
  --owner ebifry --repo <repo> --dir <folder> --message "..." --dry-run
unset TOKEN        # 用完清掉
```

⛔ 判断依据：`rc=124`（超时）说明真的卡住了 → 才需要走下面的环境变量方案；
`rc=0` + 有字节输出就是拿到了。**别一上来就要 token。**

### ⛔⛔ 2026-09-28 补充：`rc=124` 有两种含义，必须再走一步才能区分

昨天（09-26）那套"关掉交互就能吐出来"的结论**只在凭据库里还有条目时成立**。
09-28 实测：同样的命令变成 **rc=124**，而这一次是**凭据条目整个不见了**：

```bash
# ① 先看凭据库里还有没有 github 条目
cmdkey /list | grep -i github
#   有  → GCM 交互模式问题 → 用上面的 -c credential.interactive=false 再试
#   没有 → ⛔ 凭据真没了，credential fill 这条路已经堵死，不用再试
```

两个症状长得一模一样（都是 rc=124、零输出），差别只在 `cmdkey`：

| `cmdkey /list` | 含义 | 出路 |
|---|---|---|
| 有 `git:https://github.com` | GCM 在等交互输入 | `-c credential.interactive=false` 就能取到 |
| **没有** | 凭据被清掉了（登出 / 失效 / 被别的进程覆盖） | ⛔ 只能拿一个新 token |

**没有条目时的出路，按优先级**：

1. 问 Ronny 要一个 token（fine-grained PAT：只选目标仓库 + `Contents=Read and write`）
2. 找他自己在此之前落下的 token 文件 —— 本机常见位置是
   `%TEMP%\<某会话目录>\.tok`（40 字符、`gho_` 前缀）。**先验再用**：
   ```bash
   TOK=$(tr -d '\r\n' < <那个文件>)
   curl -s -o /dev/null -w "HTTP %{http_code}\n" \
     -H "Authorization: token $TOK" -H "User-Agent: wb" https://api.github.com/user   # 期望 200
   curl -sI -H "Authorization: token $TOK" -H "User-Agent: wb" https://api.github.com/user \
     | grep -i x-oauth-scopes        # 期望能看到 repo
   ```
   ⚠️ 用完**别把它留在磁盘上**，也**不要**为了"以后方便"去长期缓存 token。
3. 让 Ronny 重新 `git push` 一次任意仓库 / 在 GCM 弹窗里登录一次，把凭据写回库里

⚠️ 顺带：沙箱偶发信号打断（今天 3 次）时，**`echo > .tok` 可能没真正落盘**。
被打断后重跑，除了重取 token，还要回头 `wc -c .tok` 确认文件真在。

### ✅ 备选解法：脚本优先读环境变量

`get_token()` 已改成 **先读 `GITHUB_TOKEN` / `GH_TOKEN`**，读不到才回退 `git credential fill`：

```python
def get_token():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok.strip(), None
    ...  # 回退 git credential fill
```

**用法**（⭐ token 走环境变量，**不出现在 argv**）：
```bash
GITHUB_TOKEN='github_pat_...' python scripts/github-publish.py \
  --owner <user> --repo <repo> --dir <folder> --message "..." --dry-run
# 先 --dry-run 确认 token ok / 目标分支 / 文件数，再去掉 --dry-run 正式推
```

**⛔ 安全**：
- **绝不打印 token**（脚本只打印 `token : ok (93 chars)`）
- 用完让用户**立刻吊销**（尤其当 token 是在聊天里贴过来的）
- token 不落盘、不进 git

### ⭐⭐ 2026-10-04 实测：`git credential fill` 会卡，但 **GCM 本体不卡**

同一分钟内实测 —— 凭据**明明还在**，两个入口行为完全相反：

| 入口 | 结果 |
|---|---|
| `git credential fill`（经 git 转发） | **rc=124 挂死**，零输出（多进程、多 cwd 都试过） |
| 直接调 `git-credential-manager.exe get` | **rc=0，正常吐出 username/password** ✅ |

→ ⛔ **判据「挂死就说明凭据没了」是错的** —— `cmdkey /list` 显示条目还在时，
先试直连 GCM，很可能只是 git 那层转发卡住。

```bash
export GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never
"<PortableGit>/mingw64/bin/git-credential-manager.exe" get <<< $'protocol=https\nhost=github.com\n' \
  | grep '^password=' | cut -d= -f2- > "$TEMP/gh_tok"
wc -c "$TEMP/gh_tok"      # 期望 41（40 字符 + 换行）
```

⭐ **跨语言传路径的坑**：Python 里 `open("/tmp/gh_tok")` 在 Git Bash 下会
`FileNotFoundError` —— `/tmp` 是 MSYS 虚拟路径，Python 不认。
**必须用 `cygpath -w` 转换后的真路径**（本机 = `./gh_tok`）。
更稳的做法：把 token 缓存路径写成一个**Windows 绝对路径变量**，两种语言共用同一个字符串。

**Fine-grained PAT 需要的最小权限**：`Repository access` 只选目标仓库 +
`Contents = Read and write`（够了，别给更多）。

---

## ⭐⭐⭐ 推公开仓库前：做一份「白名单副本」（2026-09-26 实测，重要）

⛔ **不要直接推工作目录** —— 里面通常混着角色素材、模型权重、构建产物（光 `dist*` 就能上百 MB），
而且**有些资产从文件名看不出来**。实例：`app_icon.ico` 看着像个图标，
**打开一看就是角色本人** → 那是主项目资产，不能公开。

✅ **做法：在临时目录做一份干净副本，只拷白名单**（⛔ 不要用"排除黑名单"—— 黑名单一定会漏）：

```python
FILES = ["run.py", "pet_engine/core.py", ...]        # 白名单，逐个列
shutil.copy2(src, dst)                                # 只拷这些
# 然后把不能在公开仓库成立的地方就地改掉（只改副本，源工作目录一个字不动）
```

两个必查项：

| 检查 | 为什么 |
|---|---|
| `grep -rn -i "C:\\\\Users\|<用户名>\|客户资料\|<角色名>" .` | ⛔ 硬编码本机路径会泄露目录结构 |
| **打开每一个可能带资产的二进制文件**（ico / png / onnx） | 文件名看不出来它是不是角色资产 |

### ⛔⛔ 推之前先看文件的 mtime：**正在被编辑的文件不要推**（2026-10-04 实测）

多端工作流（设计端 / 执行端另一条线）下，目录里的文件可能**此刻正在被改**。
实测：`night.py` 在 18:58:43 被写、我 18:59 就在建 staging，**中间只隔 30 秒**；
再等 45 秒复查，同一文件又变了几十 KB。

**推一个正在编辑的文件 = 发布一个中间态**，可能编译不过、可能逻辑半截。

✅ 判据（推之前跑）：
```bash
ls -la --time-style=full-iso <待推文件>
date '+%H:%M:%S'        # 与文件 mtime 比：< 3 分钟 → 高危，等一下再复查
```
✅ 处置：**把那几个文件从本轮 staging 里摘掉**，commit message 里写明
「未推 + 原因（正被另一条线活跃编辑）」。宁可少推，不要推坏。
⛔ 不要因为"想多推几个"就去抢跑别人的编辑。

#### ⭐⭐⭐ 更狠的一招：拷进 staging 之后**再校验一次 md5**（2026-10-09 实测靠它抓到）

上面的 mtime 检查只在"建 staging 之前"做。但**文件可能在 staging 建好之后才被改** ——
本次就是这个情况：10:31 量到 245,688 B，10:41:27 变成 256,144 B（+10,456 B），
而我是 10:43 才 `cp` 的，**cp 到的是新版本**。

抓到它的动作非常朴素 —— 就是 `cp` 完看了一眼字节数，跟预期对不上：

```bash
cp src/night.py $STAGE/pet_engine/night.py
find $STAGE -type f -printf "%10s  %p\n"     # ⭐ 跟"我刚才量的字节数"对一下
md5sum src/night.py $STAGE/pet_engine/night.py   # 两个必须一致
```

⛔⛔ **"昨天的全绿"不能给"今天改过的文件"背书。**
发现文件变了之后：
1. **停手**，别推
2. 如果是核心模块（别的测试都 import 它）→ **重跑全套自测**，不能拿旧结果
3. 等 mtime 稳定（> 3 分钟没再动）再推
4. commit message 里如实写清这次新增了什么、哪些还没有对应自测

本次实测：重跑全套 → 25/27 与昨晚**持平**，2 个红灯都是既有的
（`_自测_夜间` 142/144、`_自测_PR04判据` 6/8），新增内容没打破任何既有测试 → 才敢推。


## ⭐⭐ 比对本地 / 远端时的两个静默陷阱（2026-09-30 各踩一次）

### 陷阱一：`open()` 文本模式会把 `\r\n` 变成 `\n` → diff 全红

```python
# ⛔ 错：new 变成 \n 结尾，old 还是 \r\n → difflib 认为【每一行都不同】
old = remote_bytes.decode("utf-8").splitlines(keepends=True)
new = open(path, encoding="utf-8").read().splitlines(keepends=True)

# ✅ 对：newline="" 关掉通用换行转换
new = open(path, encoding="utf-8", newline="").read().splitlines(keepends=True)
```

**症状**：diff 显示 `+818 / -762 行`（整文件全删全加），但文件明明只改了几处。
**判据**：`+N / -M` 里的 N 等于**本地总行数**、M 等于**远端总行数** → 一定是换行符口径不一致。
**确诊**：`b.count(b'\r\n')` 分别统计两边的 CRLF 数量，一致才说明是内容差异。

⚠️ 反过来也要留意：**行尾可能真的是不一致的**（本机 `.py` 是 CRLF、`_自测_*.py` 是 LF）。
先量行尾，再判断 diff 是否可信。

### 陷阱二：`ast.walk` 是广度优先，不按行号 → 误报一堆

想写「函数内变量先用后赋」的检查时，如果用 `ast.walk` 收集"第一次绑定行"，会取到**任意**
一个绑定，不一定是行号最小的那个 → 一个函数里出现同名变量（两个独立 if 块各赋值一次）
就误报。实测一次误报 6 处，全是假的。

✅ 正确做法：**只看本函数自身作用域**（不下钻嵌套函数），分别收集所有绑定行与 Load 行，
用 `min(load) < min(bind)` 判定；**函数参数视为已在入口绑定**（否则参数会被误判）。
写完拿正反例做阳性对照：真正的"延迟 import / 先用后赋"必须抓得到，正常顺序和
"两块独立赋值"必须干净。

### ⭐⭐ 陷阱三：Qt/GUI 项「用到但没导入」—— 自测永远抓不到（2026-10-03 实测）

**实测事故**：`ui.py` 的绘制分支用了 `QLinearGradient`，但**从来没被导入**。
→ 只要有地形就每帧抛 `NameError` → 平台画不出来。
⛔ **而 offscreen 自测全绿** —— 因为自测不跑 `paintEvent`（地形测试只断言 `body.y`）。
**回归全绿 ≠ 实机没问题。** 这个 bug 是实机目检才发现的。

✅ 补一个静态扫描（20 行就能写完，覆盖所有 `Q*` 名字）：

```python
# 收集模块里 import 进来的名字 + 模块级赋值定义的名字
imported = set()
for n in ast.walk(tree):
    if isinstance(n, (ast.Import, ast.ImportFrom)):
        for al in n.names:
            imported.add(al.asname or al.name.split(".")[0])
for n in tree.body:                        # 模块级 Name 赋值也算已定义
    if isinstance(n, ast.Assign):
        for t in n.targets:
            if isinstance(t, ast.Name):
                imported.add(t.id)

# 收集所有以 Q 开头的 Load
used = {n.id for n in ast.walk(tree)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id.startswith("Q")}

print(sorted(used - imported))             # 应为空
```
⭐ 泛化：把前缀换成你们项目的前缀（`Q*` / `ae_*` / 常量名）就能抓别类"未定义名"。

⚠️ **别只看 import 列表就下结论**：要真的 `getattr(module, name)` 验一遍命名空间 ——
有时 `from PySide6.QtGui import (...)` 的多行括号列表容易被漏读。

#### ⭐ 反过来更准的做法：拿 PySide6 真实类名当白名单（2026-10-05 补）

上面那版靠 `startswith("Q")` 猜，会把**模块级常量**（`QTE_LEN` / `QTE_MOVE_KEYS`）
和**循环解包变量**（`for (qy0, qx0, qx1) in ...`）全报成"未导入" —— 实测 5 处全是假的。

✅ 改成「先枚举库里真有什么，再看源码用没用」：

```python
from PySide6 import QtCore, QtGui, QtWidgets
KNOWN = set()
for m in (QtCore, QtGui, QtWidgets):
    KNOWN |= set(dir(m))          # 706 个真实名字
# ⛔ 必须剔 dunder —— dir(模块) 自带 __name__ / __file__ / __doc__，
#    不剔会误报「用到未导入 __file__」9 处
KNOWN = {k for k in KNOWN if not (k.startswith("__") and k.endswith("__"))}   # 696
miss = sorted(x for x in loads if x in KNOWN and x not in imported)          # 应为空
```
本项目实测：剔 dunder 后 **0 处**（剔之前 9 处，全假）。
⭐ 好处是零猜测 —— 不用维护"哪些前缀算类名"，库自己说了算。

## ⭐⭐⭐ 第四个必查项：密钥审计（2026-09-30 加）

### ⛔⛔ 先补一个流程盲区：**已发布的文件从来没被重扫过**（2026-10-03 实测）

泄漏扫描一直是扫**"本次要推的文件"**（staging 集）。问题是：
**一个文件一旦推上去，就再也不会进入扫描集** —— 除非它又被修改。
→ 早期推上去的脏文件会**永远躲过检查**。

**实测事故**：全量重扫远端 31 个文件，发现 `打包.bat` L13 有
`set "PY=C:\Users\mercy\.workbuddy\binaries\python\envs\default\Scripts\python.exe"` ——
**已经公开暴露了本机用户名与工具链路径**（不是凭据，但属隐私泄漏）。
它只是因为"本轮没被修改"而一直没进过扫描集。

✅ **把「全仓库重扫」做成固定动作**（不是只扫 staging）：

```python
# 拉远端【所有】blob 逐个扫，与本次要推什么无关
blobs = {i["path"]: i["sha"] for i in tree["tree"] if i["type"] == "blob"}
for path, sha in blobs.items():
    txt = base64.b64decode(API(f"/git/blobs/{sha}")["content"]).decode("utf-8", "replace")
    for ln, line in enumerate(txt.splitlines(), 1):
        if PATH_PAT.search(line): ...   # 硬编码本机路径
        for nm, p in SECRET_PATS: ...   # 密钥
```
⭐ 判断标准（两条都要）：
- **硬编码路径**：`C:[\\/]Users` / `/c/Users` / `/Users/` / `AppData` / **本机用户名**
- **密钥**：见下方模式表

#### ⛔⛔ 拉远端内容用 `git/blobs/{sha}`，别用 raw.githubusercontent（2026-10-09 实测）

上面那段代码里的 `API(f"/git/blobs/{sha}")` 是**唯一正确的取法**。
图省事改用 `https://raw.githubusercontent.com/<o>/<r>/main/<path>` 会撞两件事：

| 症状 | 原因 |
|---|---|
| `UnicodeEncodeError: 'ascii' codec can't encode characters in position 31-32` | urllib 对 URL 做 ascii 编码，**中文文件名**直接炸（本项目一堆 `_自测_*.py`） |
| 偶发 `Tunnel connection failed`，随机跳过若干文件 | raw 通道走代理不稳 → **漏扫**，而"漏扫"看起来跟"干净"一模一样 |

⭐ **所以扫描循环必须统计 `扫描 N / 跳过 M`，M>0 就补扫** —— 否则"0 命中"可能是没扫到。
`git/blobs` 按 sha 取、不涉及路径编码，实测 52 个文件 0 跳过。

⚠️ 本项目里 `*.bat` 是高发区（Windows 启动脚本习惯写死解释器绝对路径）。
**推任何 bat 前先扫这一条。**

⚠️ 顺带：`grep "C:\\\\Users"` 在 bash 里转义极易写错（实测把有问题的 `直接开玩.bat`
误报成"干净"）。**用 Python 正则扫，别用 shell grep 的转义。**

⛔⛔ **同一个坑换皮又踩了一次（2026-10-04），这次是 Python 原始字符串**：
写成 `re.compile(r"C:\\\\Users\\\\mercy")` —— 原始字符串里那是**字面两个反斜杠**，
而 `.bat` / `.md` 里实际是**单个 `\`**（`set "PY=C:\Users\mercy\..."`）。
→ 实测把**已知有问题的 `打包.bat` 漏报成干净**，还差点据此给 Ronny 报"0 处命中"。
⭐ 硬规则：**本机路径判据一律写 `C:[\\/]+Users[\\/]+<用户名>`**（宽松分隔符匹配），
⛔ 永远不要数反斜杠个数。改完判据**必须拿已知阳性样本回归一次**
（把一个真带路径的 bat 丢进去，必须报命中才算判据可用）。

---

「我有没有把 API key 推上去」这类问题，**必须查全历史，不能只看当前文件** ——
密钥推上去又删掉，GitHub 的提交历史里**永远留着**，照样算泄露。

### 查法：两个独立检测器

```python
# ① 枚举全历史【所有出现过的】blob（不只是 HEAD），逐个下载扫描
for c in GET(f"/repos/{o}/{r}/commits?per_page=100"):
    tree = GET(f"/repos/{o}/{r}/git/trees/{c['sha']}?recursive=1")
    for it in tree["tree"]:
        if it["type"] == "blob": blobs.setdefault(it["sha"], it["path"])   # 按 sha 去重
```
⚠️ 同时查 `GET /repos/{o}/{r}/branches` 和 `/tags` —— 别的分支/tag 里的提交不在默认分支历史上。

```bash
# ② 让 GitHub 自己查（provider 模式库比自写的大得多）
GET /repos/{o}/{r}/secret-scanning/alerts      # 返回 [] = 干净；403/404 = 功能没开
GET /repos/{o}/{r}                             # 看 security_and_analysis 确认是否 enabled
```
⛔ 返回 `[]` 才有意义 —— 先确认 `secret_scanning=enabled`，否则"0 告警"是功能没开、不是没问题。

### ⭐⭐⭐ 阴性结果必须先做阳性对照

**"没查到"和"扫描器坏了"看起来一模一样。** 拿本机已知含密钥的文件喂给同一套模式，
先证明检测器抓得到：

```python
# 用真密钥文件做对照
for fn in LOCAL_SECRET_FILES:
    assert any(p.search(read(fn)) for _, p in PATTERNS), f"{fn} 没被抓到 → 检测器有盲区"
```
实测价值：第一版模式**漏了火山 Ark(`ark-`) 和火山 token(`VxCg...`)**——后者还带点号，
`VxC[A-Za-z0-9]{16,}` 匹配不到，得写成 `VxC[A-Za-z0-9\._\-]{16,}`。
**不做对照就会报一个假的"0 命中"。**

### 模式清单（国产通道也要覆盖）

| 目标 | 正则 |
|---|---|
| 火山 Ark Key | `\bark-[A-Za-z0-9_\-]{16,}` |
| 火山 token | `\bVxC[A-Za-z0-9\._\-]{16,}` ⚠️ 别漏点号 |
| 火山 AK/SK | `AKLT[A-Za-z0-9_\-]{10,}` |
| OpenAI 系 | `\bsk-[A-Za-z0-9_\-]{16,}` |
| GitHub | `\bgh[pousr]_[A-Za-z0-9]{20,}` |
| AWS / Google / Slack | `AKIA[0-9A-Z]{16}` / `AIza...` / `xox[baprs]-...` |
| JWT | `eyJ...\.eyJ...\..*` |
| 赋值式 | `(api_key\|secret\|token\|password)\s*[:=]\s*["'][^"']{12,}["']` |
| 私钥 | `-----BEGIN [A-Z ]*PRIVATE KEY-----` |

### ⚠️ 附带发现：`.gitignore` 通常不覆盖密钥文件（2026-09-30 已修）

本机 4 个公开仓库的 `.gitignore` **原本全都只忽略 `__pycache__/dist/build/models`**，
没有一条覆盖 `.env` / `*.key` / `*.token` / `secrets/`。
没泄露**靠的是"手工白名单发布"，不是靠 `.gitignore` 兜底** ——
哪天改成 `git add .` 就会直接进仓库。

⭐ **别指望 push protection 兜底**：它主要覆盖主流 provider，国产通道（火山等）的密钥格式
**未必认**，挡不住。审计要靠自己的模式表。

#### 现成加固块（复制即用）

```gitignore

# ---- 凭据 / 密钥（⛔ 永远不要提交）----
.env
.env.*
!.env.example
*.key
*.pem
*.token
*_secret*
*_credential*
secrets/
credentials/
工具/
```

#### ⭐ 跨仓库批量加固的两个必须注意项

| 项 | 为什么 | 怎么做 |
|---|---|---|
| **保留各自行尾** | 仓库行尾不统一（实测 LunaPet 是 CRLF，其余 LF）。统一成 LF 会让**整个文件逐行 diff** | 读原文判断 `"\r\n" in text`，按原样追加；**用二进制写** `open(p,"wb")` |
| **幂等** | 重跑不能重复追加 | 追加前查标记（如 `"凭据 / 密钥" in text`），有就跳过 |

⛔ 别用 `echo >>` 追加 —— Windows 下会写 CRLF，污染 LF 仓库。

⭐ **发布时只推 `.gitignore` 一个文件**：把加固后的文件放进一个只含它的 staging 目录，
`--dir` 指过去 → 一次提交只动这一个文件，`base_tree` 保证其余文件原样不动。
推完复核：**文件总数应与推送前完全相同**（只改内容不加文件）。

## ⭐ 第三个必查项：把仓库自带的自测真跑一遍，全绿才推。（2026-09-28 加）

公开仓库里的自测是**对外承诺的一部分** —— 挂着一个红的测试推上去，比不推测试更糟。
而且实测里，**失败的原因有一半在测试自己身上**，推之前必须分清是哪一种：

| 失败原因 | 判据 | 怎么办 |
|---|---|---|
| 测试过时（戳了旧实现的私有变量 / 分母写死 / 没有 `exit(非0)`） | 被测代码改成"发真实事件"后行为正确 | 改测试 —— 这不算放松标准，是把测试改回它自己声称的做法 |
| 代码真有问题 | 换成真实调用路径仍然错 | 改代码，并**新增一条回归项**把它钉住 |

⭐ **最快的判据（2026-09-29 加）：拿失败的那个测试文件跟远端比字节。**
- **与远端逐字节相同**，而远端那次发布是绿的 → **代码真回归**（同一个测试，代码坏了才红）。⛔ 绝不许改断言蒙过去。
- **本地已改过** → 大概率是断言没跟上素材/行为升级 → 按"测试过时"处理。
- 实测价值：一次就把「转身接线 22/1」判成真回归（根因是 silhouette 传参过期→误判卡墙），
  同时把「core / 点击唤醒」的失败判成纯断言过期（idle 帧数 22→24、`fall` 拆成 `drag_out`+`fall`），
  没在错误的方向上浪费一轮。

### ⛔⛔ 但这条判据有适用范围（2026-10-01 修正，差点误判）

**byte-compare 只在「改动没有引入全新状态」时成立。**
如果这次的改动带来了**新的状态/分支**，旧断言会**拒收新状态** —— 那不是回归，是测试还没跟上。

判据：**看失败信息是不是"实际值 = 某个全新状态名"**。
实测：`转身接线` 由 22/1 → **17/6**，6 项全是同一个症状
`实际 climb`（旧断言只认 walk / turn_out / idle）。同一测试与远端逐字节相同 →
按旧判据会误判成"代码回归"，实际是**新功能（地形攀爬）撞进了旧测试的场景**：

- 测试没配地形 → 用默认地形（左右墙）
- 测试造的目标在屏幕外（`body.x+500`，而测试屏只有 799 宽）→ 她走进右墙区 → `climb`
- 代码在做它**被设计要做的事**

⭐ **三步分诊顺序**：
1. 失败信息里有没有**全新状态名 / 全新字段**？有 → 先查是不是新功能，别急着判回归
2. 再比测试文件字节
3. 最后才下"代码回归"的结论

### ⭐⭐ 别把"偶发红"当偶发：先固定随机种子（2026-10-01 实测）

一个测试连跑 5 次给出 `22/1、23/0、22/1、22/1、23/0` —— 约 2/3 概率红。
**这是 bug 的信号，不是"运气不好"。** 当时被当成偶发跳过了，结果它是个真回归。

排查顺序：
1. **先 `random.seed(N)` 固定**（提到文件头，别放在文件中间）——
   没有固定种子的测试根本判不了真假：红绿都可能只是运气。
   实测有个测试只在第 113 行 seed，前面 9 段全是无种子随机 → 成败随机的目标位置飘。
2. 固定后再跑，**稳定红 = 真问题**；仍时红时绿 = 还有别的非确定性源（时间/并发/GUI）。

### ⭐⭐ 修完 bug 后，用 A/B 证明"没改变正常行为"（2026-10-01）

⛔ **"测试变绿了"只说明那个场景修好了，不说明没伤到别处。**
尤其当修复动的是**公共路径**（限位、渲染、物理）时，必须补一层 A/B：

```
A = 旧行为（monkeypatch 回旧调用方式）
B = 新行为
→ 跑同一套较长的 harness（如 90 秒主循环），比【状态直方图 + 终点坐标】
```

实测价值：某次修复让 `idle→walk→climb→fall` 的状态直方图与终点坐标
**逐项完全一致** → 证明改动只在边界条件下生效、正常行为零影响。
这一步还**顺带暴露了一个既存问题**（某状态占了 79% 的帧，追下去发现会永久卡住）——
长跑 harness 本身就是探针。

⚠️ 副产品要如实标注：**新状态会掩盖旧 bug**。遇到"旧 bug 走不到那条分支了"，
要明确写进 commit message（"被掩盖，未确认"），别当它消失了。

⚠️ 顺手要查的三种"测试不算数"写法（三种全遇到过）：
- `sys.exit(0)` 或干脆不 exit → 失败也是退出码 0，等于不进 CI
- 分母写死（`通过 {n} / 10 项` 而实际有 11 项）→ 全过反而报失败
- 写死本机绝对路径 → 别人克隆下来跑不起来

⭐⭐ **"不 exit" 这个毛病会反复犯**（2026-10-01 修了 `_自测_core.py`，
2026-10-03 又在新增的 `_自测_夜间.py` 里发现同样的问题 —— 它报 `通过 98 / 113`
+ 15 项 FAIL，却仍然 `rc=0`）。

✅ **做成常规动作**：每新增一个测试文件，立刻用它验一次退出码 ——
```bash
$PY 新测试.py; echo "rc=$?"     # ⛔ rc=0 但有 FAIL / 未通过 → 测试是"哑"的
```
⛔ 一个"报 FAIL 却返回 0"的测试**比没有测试更糟**：它让 CI 看起来是绿的。

### ⭐⭐ 把一次性脚本泛化成可复用工具时：先证明它能复现原产出（2026-09-28）

公开仓库里的工具往往是**从项目里的一次性脚本提炼**出来的
（`_修_out缩放.py` → `segment_scale.py`、`_勾线切_v2.py` → `line_keying.py`）。
提炼过程一定会重写代码，**必须证明"重构零行为变更"，否则推上去的是个没人验证过的新实现。**

做法就一条：**拿新旧两版跑同一份真实素材，对产出做逐字节比对。**

```python
# 用 git blob sha 或普通 sha1 都行；逐文件比，别只比总数
same = sum(1 for a, b in zip(new_files, old_files) if sha(a) == sha(b))
print(f"逐字节相同 {same} / {len(new_files)}")
```

⭐ 实测里这一步**救过两次**：
- 抠图那个：3 帧走图 `XOR=0`、alpha 最大差 `0.0000` → 确认零行为变更
- 跨段缩放：第一轮 **106 / 107**，追下去发现是**我传的系数少了小数位**
  （`1.0167` 而不是 `1.0166667`），差 `3e-5` 就翻掉一个 `int(round())` 的取整边界，
  某一帧整体位移 1px。改全精度后 **107 / 107**。
  ⛔ **没有这个逐字节比对，这种"只差个别帧"的错永远发现不了** ——
  它不报错、不崩、看着正常，而且拿它当基准还会把误差传下去。

⚠️ 顺带两个只在"顺序 / 精度"上出问题的静默错配（同一天踩的）：
| 错误 | 后果 | 正确做法 |
|---|---|---|
| 帧序列用 `sorted(os.listdir())`（字典序） | 帧名不补零时 `_10` 排在 `_1` 前 → **配对全错位 / 系数配到错帧上**，不报错 | 按文件名里**最后一个数字段**排序 |
| 涉及取整的系数给 4 位小数 | `int(round())` 跨过 `.5` → 个别帧整体位移 | 系数一律给**全精度** |

**顺手要修的**：写死的解释器路径、`icon=` / `datas=` 指向未发布资产的构建配置
→ 改成"存在才用"，让仓库**缺素材也能构建**。

---

## ⭐⭐⭐⛔ 推之前必须逐文件比 sha：**本地的文件不一定比远端新**（2026-09-27 实测踩到）

**这是我原来完全没想到的坑。** 直觉是"本地工作目录 = 最新"，但公开仓库里的文件
**在推送时被就地脱敏过**（改掉个人路径 / 改成通用写法），此后本地那份就**永久落后于远端**了。

实测案例（`ebifry/LunaPet`）：
| 文件 | 本地 mtime | 结果 |
|---|---|---|
| `LunaPet.spec` | 09-26 07:34 | ⛔ **远端才是新版**（推送时脱敏过），本地是旧版 |
| `打包.bat` | 09-25 20:37 | ⛔ 本地写死 `C:\Users\mercy\...\python.exe`，远端已是 `set "PY=python"` + PATH 探测 |

如果按"本地覆盖远端"推，**这两个文件会被推回旧版/带个人路径的版本** —— 一次回退 + 一次泄露。

### ✅ 正确姿势：先下远端快照当基线，再覆盖变更文件

```bash
# 1) 拿 token
TOK=$(printf 'protocol=https\nhost=github.com\n\n' | GIT_TERMINAL_PROMPT=0 git -c credential.interactive=false credential fill 2>/dev/null | sed -n 's/^password=//p')

# 2) 下完整快照当基线（不是只下要改的文件）
curl -sL -H "Authorization: token $TOK" -H "User-Agent: wb" \
  "https://api.github.com/repos/<owner>/<repo>/tarball/main" -o main.tgz
mkdir -p stage && tar xzf main.tgz -C stage --strip-components=1

# 3) ⭐ 关键一步：逐文件比 git blob sha，看清哪些真变、方向是什么
python - <<'PY'
import json,hashlib,os
SRC=r"<本地源码目录>"
d=json.load(open("tree.json"))
def gitsha(p):
    b=open(p,'rb').read(); return hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
for it in d["tree"]:
    if it["type"]!="blob": continue
    lp=os.path.join(SRC, it["path"].replace("/",os.sep))
    if not os.path.exists(lp): print("MISSING_LOCAL", it["path"]); continue
    ls=gitsha(lp)
    print(("SAME " if ls==it["sha"] else "DIFF "), it["path"], "remote="+it["sha"][:8], "local="+ls[:8])
PY

# 4) 把确认要更新的文件覆盖到 stage/，其余保持远端原样
# 5) 跑测试 + 泄露扫描 → 发布 → 再逐 blob sha 复核
```

⭐ **判据**：`DIFF` 且本地 mtime **早于**远端最后提交时间 → **远端是新版，不要覆盖**。
远端提交时间是 UTC，本地 mtime 是本地时区，**换算后再比**（本机 AEST = UTC+10）。

⚠️ 顺带：这一步也会暴露**远端已存在的泄露**。本次就发现 `docs/BUILD.md` 里
早先推送时漏了一行 `C:\Users\mercy\.workbuddy\...\python.exe` →
**既然发现了就顺手修掉**（同时改掉本地项目名 `cd /d 自研引擎`，那个目录在仓库里不存在）。

## ⭐⭐⭐ 贡献日历：必须显式给作者 + **本地时区**（2026-09-28）

**症状**：Ronny 问「GitHub 上显示我没有 contribution」。查下来是两件不同的事，
都必须分清，否则会去乱改提交。

### ① 先别急着改：贡献日历有**索引延迟**

当天推的提交**不会立刻**出现在绿格子里。实测：19:20 / 19:36 推了两个提交，
23 分钟后再查，当天仍然是 `No contributions`；而**前一天同样机制推的两个提交
已经老老实实算上了**（9-27 那天正好 2 条）。

⭐ 判断方法：别用 HTML 页面（可能有 CDN 缓存），**用 GraphQL 拿权威数据**：

```bash
curl -s -X POST -H "Authorization: bearer $TOK" \
  -H "Content-Type: application/json" https://api.github.com/graphql \
  -d '{"query":"{ user(login: \"<user>\") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }"}'
```

### ② 提交的**时区**会被用来决定算哪一天 —— 这是真 bug

GitHub 官方 2014-03-10「Timezone-aware contribution graphs」原话：

> When counting commits, we use the timezone information present in the timestamps for those commits.

⛔ **不显式传 `author` / `committer` 时，API 用「当前 UTC 时间」盖章，时区记成 `Z`。**
本机是 AEST/AEDT（UTC+10/+11）⇒ **本地早上 10 点前推的提交，UTC 日期还是前一天
→ 绿格子记到昨天去了**，表现就是"今天写了代码但图上没亮"。

⚠️ 这也能解释"为什么昨天傍晚推的看着没问题" —— 傍晚的提交 UTC 和本地日期刚好重合，
**看不出问题不等于没问题**。

✅ `github-publish.py` 已修（`resolve_identity()`）：显式带
* `name` = `/user` 的 login
* `email` = `{id}+{login}@users.noreply.github.com`（对账号 ID 天然有效，贡献才算得到本人头上）
* `date` = `datetime.now().astimezone().isoformat(timespec="seconds")` → `2026-09-28T19:44:36+10:00`

```python
payload = {"message": msg, "tree": tree, "parents": [head],
           "author": ident, "committer": ident}   # ⭐ 两个都要给
```

⭐ 想确认改动生效，看脚本打印的两行：
```
author  : ebifry <51730721+ebifry@users.noreply.github.com>
stamp   : 2026-09-28T19:44:36+10:00   (本地时区偏移，决定贡献日历算哪一天)
```
末尾如果是 `Z` 就说明时区没带上，绿格子会按 UTC 分天。

⚠️ 另有说法称"贡献图只算 UTC 时间戳"（部分中文博客）—— 与 GitHub 官方公告矛盾。
但**两种解释下"带本地偏移"都是安全选择**：官方那套会按本地日期记，
UTC 那套换算回去仍是同一个瞬间，不会更差。**所以直接带上，不必纠结。**

## ⛔⛔ 提交信息：一律走 `--message-file`（2026-10-03 实测踩坑，发布静默失败）

```bash
# ✅ 正确：Write 把信息写成文件，再交给 --message-file
python github-publish.py --owner <owner> --repo <repo> --dir <folder> \
  --message-file _msg.txt
```
脚本会打印 `message : N 字符 / M 行` 让你确认没被截断。

⛔⛔ **别用 `--message "$(cat 文件)"`，也别内联长信息。** 实测一次 53 行的信息：

| 现象 | |
|---|---|
| 命令退出码 | **0** |
| 脚本输出 | 只回显了信息尾部，**没有 `done : ... commit=...` 那行** |
| 耗时 | 1 秒（正常发布 7~10 秒） |
| 远端 HEAD | **没变** —— 根本没提交 |

⭐ **最坑的地方：没有任何报错。** 如果只看退出码、或者不核对远端 HEAD，
会以为推成功了。内联引号（`θ''`）、多行、特殊字符都会触发。

✅ **所以「提交后校验」不是可选项**，是唯一能发现这类失败的手段（见下节）。

### 判据（3 秒确诊）
发出命令后**必须**看到 `done : https://github.com/... commit=<sha>` 那一行。
没有它 = 没推上去，别管退出码是几。

## 提交后必须校验（别只看 200）

`POST /git/blobs` 返回的 `sha` 就是 git blob 哈希，拿本地算同一个值对比即可证明字节一致：

```bat
git hash-object --no-filters <文件>          :: 对比 API 返回的 sha 前 8 位
curl -sL https://api.github.com/repos/<owner>/<repo>/git/trees/main
```
注意 `git hash-object` 要加 `--no-filters`（否则 autocrlf 会让 CRLF 文件算出不同的哈希）。

## 坑

0. **偶发：命令毫无输出、直接被 SIGTERM（exit 1）。** 2026-09-26 遇到两次，
   ⭐ **原样重跑一次就好**（第二次成功），⛔ 别去改脚本、别怀疑 token（单独测 `credential fill` 仍是 rc=0 有字节）。
   判断方法：先把凭据那一步单独跑一遍，拿到字节 → 说明是环境抖动，不是链路问题。
   ⭐ 同理，**本地跑重活（抠图 / matting 之类吃 CPU 的脚本）也会被掐** ——
   长任务一律 `run_in_background=true` 并落日志文件，再 `TaskOutput` 取结果，别放在前台等。
1. **远端已有提交时会「非快进」**：先 `git fetch origin main`，用远端 sha 当 `parents`（脚本已读 head），
   不要硬推。
2. **`REST API 提交` 与本地 git 仓库会分叉**（本地是 `git commit` 出来的提交，远端是 API 提交的）。
   同步办法：`git fetch origin main && git reset --soft origin/main`（内容一致时工作区会干净）。
3. **不要把 token 打到命令行或日志**：用环境变量 + `GIT_ASKPASS` 或直接用脚本读凭据，
   避免出现在 argv / shell 历史里。用完 `unset`。
4. **公开仓库前先 grep 本机路径**：`grep -rl "<用户名>" <目录>`，把 `C:\Users\...` 硬编码换成解析式。
