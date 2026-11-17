# 快速开始（第一次用，5 分钟）

> 这份文件只解决一件事：**让你从零跑到「草稿箱里出现第一篇稿」**。
> 想搞懂每一步的为什么，看 `SKILL.md` 和 `references/`。

---

## 0. 你会做四次「复制粘贴」和四次「回车」

```
装环境 → ①扫码登录 → ②让智能体写稿(6 件套) → ③渲染封面 → ④入草稿箱 → ⑤回读验证 → 草稿箱里看到它
```

四条命令的顺序就是 ①③④⑤，别跳步——尤其**第 4 条（入草稿箱）之前必须先有封面**。

---

## 1. 环境准备（约 3 分钟）

### 1.1 装 Python

要求 **Python 3.10 或更高**（3.11 / 3.12 / 3.13 都可以）。检查：

```bash
python --version
```

看到 `Python 3.1x.x` 就绪。没有的话去 python.org 下安装包，安装时**勾上「Add Python to PATH」**。

> macOS 上如果 `python` 命令不存在，把下面所有命令里的 `python` 换成 `python3`。

### 1.2 装脚本依赖

在**解压出来的包目录**里（能看到 `scripts/` 这一层）执行：

```bash
pip install -r scripts/requirements.txt
```

期望输出：最后几行是 `Successfully installed ...`（会装上 playwright、pillow 等）。

### 1.3 装浏览器内核（只需一次，约 100-300MB）

```bash
playwright install chromium
```

期望输出：`Downloading Chromium ...` 然后完成。这一步会下载一个专用浏览器，**登录窗口用的就是它**。

### 1.4 自检环境（三条都通了再往下）

```bash
python -c "import playwright; print('playwright ok')"
python -c "from PIL import Image; print('pillow ok')"
python scripts/gzh_login.py --help
```

第三条要能看到参数说明（`--profile`、`--port`）。**看不到 `--help` 说明你不在包目录里**，先 `cd` 到解压目录。

---

## 2. 四步首跑

以下命令里的路径都是示例，按你放文件的位置改；**`--profile` 目录会存登录凭据，别放共享盘或 Git 仓库里**。

### 第 1 步｜扫码登录（只在首次和掉线时做）

```bash
python scripts/gzh_login.py --profile ./gzh-profile --port 9333
```

**期望输出**：弹出一个**可见的浏览器窗口**并显示登录二维码（若脚本能抓到二维码，还会同时打印 `QR_PATH: <图片路径>`）→ 你用**管理员本人微信**扫码 → 脚本打印 **`LOGIN_OK`** 后退出。

**想先查一下当前登录态**（不启动浏览器、不打扰你）：

```bash
python scripts/gzh_login.py --check --profile ./gzh-profile
```

- 还登录着 → 打印 `LOGIN_ALREADY`（退出码 0），可以直接跳到第 2 步；
- 已失效 → 打印 `LOGIN_REQUIRED 登录态已失效，需要重新扫码`（退出码 2），跑上面那条扫码命令。

**成功后你会得到**：`./gzh-profile/` 目录（里面是登录凭据）。**约 4 天有效**，过期后重跑这条命令。

**出错先看**：窗口没出现 / 窗口跑到屏幕外 → `references/06-坑清单.md` **A1**；扫了没反应 → 二维码约 2-5 分钟失效（A2、A3），重跑出新的码。

### 第 2 步｜让智能体写出 6 件套

在豆包智能体里说一句（照抄）：

```
按规范写一篇公众号：选题你从今天的热点里挑一个最合适的，先告诉我为什么选它。
```

**期望输出**：选题判断（含三关自查）→ 5 个候选标题（带字节数）+ 最终标题 → 正文 → 排版 HTML → 配图清单 → 封面文案 → 摘要。

把这 6 样存成文件（命名随意，建议见 `SKILL.md` 第四节）：

```
最终标题.txt   正文.md   排版.html   配图清单.md   封面文案.md   摘要.txt
```

### 第 3 步｜渲染封面两张

```bash
python scripts/render_cover.py --title "文章标题" --out-dir ./out
```

（`"文章标题"` 换成你的最终标题，**不要带方括号和引号**）

**期望输出**：`./out/` 目录里出现两张图：

```bash
ls -l ./out
```

- 一张 **900×383** 的首图：`./out/cover_900x383.png`
- 一张 **383×383** 的方图：`./out/cover_383x383.png`

（可选参数：`--tag "深度"` 会在左上角加一个小标签，属于装饰，缩略图下看不清，不放信息也行。）

**自检**（尺寸对不对，一眼可查）：

```bash
python -c "
from PIL import Image
import glob
for f in sorted(glob.glob('./out/*.png')):
    im=Image.open(f); print(f, im.size, round(im.size[0]/im.size[1],3))
"
```

期望：首图 `900×383`（比例 2.35），方图 `383×383`（比例 1.0）。**出现 900×500 就是错的**，重跑。

### 第 4 步｜写进草稿箱

```bash
python scripts/gzh_save.py --title "标题" --md 正文.md --cover ./out/cover_900x383.png \
       --digest-file 摘要.txt --profile ./gzh-profile --port 9333
```

**期望输出**：末尾一行 **`DRAFT_OK appmsgid=<一串数字>`**。

`appmsgid` 是什么：公众号给这篇草稿分配的**唯一编号**，第 5 步要用它。

- 有排版 HTML 想直接传？把 `--md 正文.md` 换成 `--html 排版.html`（**二选一，别同时给**）。
- 不确定参数名 → `python scripts/gzh_save.py --help`。
- 报错 → 先看 `references/05-登录与入稿通道.md` 的「失败现象对号入座表」。

### 第 5 步｜回读验证（唯一验收判据）

```bash
python scripts/gzh_verify.py --appmsgid <上一步那串数字> --profile ./gzh-profile --port 9333
```

**期望输出**：三项核对结果 —— **标题一致 / 图片数 / 正文非空**，三项都过才算成。

想让它核对得更严，把预期值也传进去（推荐）：

```bash
python scripts/gzh_verify.py --appmsgid <数字> --expect-title "你的最终标题" --expect-images 3 \
       --profile ./gzh-profile --port 9333
```

（`--expect-images` 填 **1（表头图）+ N（正文插图）**。不给这两个参数也照样能验。）

> **`DRAFT_OK` 不算成功，看到三项核对结果才算成功。**
> 然后打开公众号后台的草稿箱，肉眼确认排版和封面；确认没问题再点群发。

---

## 3. 出错先看哪一条（按现象索引）

| 你看到的 | 先看 |
|:--|:--|
| 浏览器窗口没弹出来 / 窗口跑到屏幕外面 | `references/06-坑清单.md` **A1** |
| 扫了码登录没成功（二维码过期 / 被刷新打断） | `references/06-坑清单.md` **A2、A3** |
| 提示 profile 被占用 / 目标已关闭（TargetClosedError） | `references/06-坑清单.md` **A4** |
| 保存报参数错误（200002）/ 返回 ret 非 0 | `references/06-坑清单.md` **B1、B2**；`references/05-登录与入稿通道.md` 失败对照表 |
| `DRAFT_OK` 但草稿箱里没有 | `references/06-坑清单.md` **B3**（模板 token 过期，重登） |
| 摘要是正文开头那句，不是我写的 | `references/06-坑清单.md` **E7**（摘要被自动覆盖） |
| 草稿里样式丢了 / 排版乱了 | `references/06-坑清单.md` **D1-D5**；**E5**（别在后台编辑器保存） |
| 图片不显示、显示成一条缝（高度 0） | `references/06-坑清单.md` **C1、C2** |
| 回读说正文是空的 | `references/06-坑清单.md` **E2**（列表接口不返回正文，要开编辑器读） |
| 回读列表偶发空数组 | `references/06-坑清单.md` **E3**（限流，sleep 后重试） |
| 封面被切、被裁 | `references/04-封面规范.md`（安全区与 900×500 问题） |
| 封面文字出乱码错字 | `references/04-封面规范.md`（中文必须 HTML 叠字） |
| 标题存不进去 / 被截断 | `references/02-写作与合规红线.md`（64 字节算法与禁用引号） |
| 不知道写什么 | `references/01-选题与竞调.md` |
| 想搞懂为什么不用官方接口 | `references/05-登录与入稿通道.md` |

---

## 4. 目录一览

```
gzh-fullauto-skill/
├── SKILL.md                  ← 主文档：人设指令 + 八步流程 + 6 件套契约 + 红线
├── README-快速开始.md         ← 本文件
├── references/
│   ├── 01-选题与竞调.md
│   ├── 02-写作与合规红线.md
│   ├── 03-排版与配图.md
│   ├── 04-封面规范.md
│   ├── 05-登录与入稿通道.md
│   └── 06-坑清单.md
├── scripts/                  ← 执行端（登录／渲染封面／入草稿箱／回读）
│   ├── gzh_login.py
│   ├── gzh_save.py
│   ├── gzh_verify.py
│   ├── render_cover.py
│   └── requirements.txt
└── assets/
    └── design-template.html  ← 排版底稿（土金板，全内联）
```

## 5. 三条纪律（省你很多返工）

1. **凭据只在本地的 `gzh-profile/` 里**，不要发给任何人、不要传进任何网盘；豆包智能体一个账号密码都不需要。
2. **每次入稿前先跑第 1 步确认登录态**（它会告诉你是否已登录）。稿子写完了才发现登不进去，最费时间。
3. **每天别在同一个对话里连着写多篇**——智能体会串味。一篇一个对话最稳。
