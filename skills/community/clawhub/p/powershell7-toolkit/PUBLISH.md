# 技能上架材料 · PowerShell 7 工具链 v1.1.5

> 面向 **WorkBuddy 开放平台**（open.workbuddy.cn）的提交材料，逐栏可照抄。
> 本文件不进分发包，也不进 GitHub 仓库。

---

## 〇、提交包（用哪一个）

| 包 | 路径 | 结构 | 用在哪 |
|---|---|---|---|
| **平台提交包** | `H:\WorkBuddyData\Claw\ps7-toolkit-1.1.5-workbuddy.zip` | 第一层是 `powershell7-toolkit/`，11 个文件，58KB | **开放平台上传用这个** |
| SkillHub 包 | `H:\WorkBuddyData\Claw\ps7-toolkit-1.1.5.zip` | 根目录直接是 `SKILL.md` | `clawhub skill publish` |

平台要求「解压后第一层就是技能目录 `{skill-name}/SKILL.md`，别多套一层 `skills/`」，所以两个包结构不同，**别传错**。
平台限制：仅 `.zip`、≤ 3MB、目录最多两层。我们 58KB、两层，符合。

### 官方 Frontmatter 必填字段（对照已核）

| 字段 | 必填 | 我们的值 |
|---|---|---|
| `description` | **是** | 症状驱动描述（287 字），含用途 + 触发词 |
| `description_zh` | **是** | 同上（中文） |
| `description_en` | **是** | 英文版 |
| `version` | **是** | `"1.1.5"` |
| `author` | **是** | `"欣欣 (YUJIANYU)"` |
| `name` | 否 | `powershell7-toolkit`（与目录名一致） |
| `display_name` / `display_name_en` | 否 | `PowerShell 7 工具链` / `PowerShell 7 Toolkit` |
| `allowed-tools` | 否 | 未填（技能靠自带脚本执行，不需要额外工具白名单） |
| `user-invocable` / `disable-model-invocation` | 否 | 未填（保持可被 AI 自动触发） |

---

## 一、操作路径（后台四步）

```
发布管理 → 技能 → 右上角「创建」
  → ① 配置技能：拖入 ps7-toolkit-1.1.5-workbuddy.zip（自动解包、生成技能 ID）
  → ② 确认信息：左侧补充展示信息，右侧看预览
  → ③ 提交审核（官方口径 7 个工作日，实测约 18 小时）
  → ④ 通知中心收到「已通过」→ 回列表点「发布」→ 选「公开发布」
```

**前置条件**：个人主体认证（身份证 + 实名手机号 + 可收验证码的邮箱 + 人脸识别），
以及「设置 → 开发者信息」填完（头像 512×512、昵称 2–20 字符、简介 20–120 字、联系方式）。
开发者信息没填完，后台创建入口不解锁。

---

## 二、表单逐栏填写

### ① 配置技能（上传页）

| 项 | 填写 |
|---|---|
| 上传文件 | `ps7-toolkit-1.1.5-workbuddy.zip` |

上传后平台自动解析，技能 ID 由平台生成，不用手填。

### ② 确认信息（这一步字段最多）

| 表单项 | 填写内容 |
|---|---|
| 市场展示名称 | `PowerShell 7 工具链` |
| 版本号 | `1.1.5`（从包里读，不可改） |
| 头像 | 用包内 `assets/icon.png`，或从本地重传同一张（512×512、PNG、9.7KB） |
| 市场展示分类 | 建议选：**开发者工具**、**效率工具**、**系统与运维**（按平台实际选项挑，多选） |
| 服务类目 | 首选 **工具-办公**；若有「工具-开发者」优先用它，最多 5 个 |
| 介绍（卡片简介） | 见下方「三、简介文案」 |

> 名称、版本、`description_*`、`category` 这类字段是从 `SKILL.md` 解析出来的，页面上改不了。
> 要改就回 `SKILL.md` 改完重新打包上传。

### ③ 提交审核

提交前核对：名称、分类、类目、头像、简介。提交后进审核队列。

### ④ 审核通过后

回「发布管理 → 技能」，状态「待发布」→ 点「发布」→ 选「**公开发布**」（全部用户可见）。
选「专用发布」只有自己账号下的 Buddy 应用能看到，**我们要的是公开发布**。

---

## 三、简介文案（「介绍」栏，按平台字数限制取舍）

**短版（约 60 字，卡片用）：**

> 一键把 Windows 自带的 PowerShell 5.1 升级到 PowerShell 7，补上 6 个 Rust 命令行工具，顺手根治中文乱码。

**长版（详情页用，可直接整段粘贴）：**

> 解决 Windows 命令行中文乱码（mojibake）与 AI 助手调用 PowerShell 5.1 频繁报错的问题。
>
> 它做三件事：① 把系统里的 PowerShell 5.1 换成 / 补上 PowerShell 7（pwsh）；② 装上 6 个 Rust 写的命令行工具——ripgrep（检索）、fd（找文件）、fzf（模糊选择）、bat（带高亮的 cat）、delta（git diff 美化）、jq（处理 JSON）；③ 把 UTF-8 编码打通到 profile、控制台与文件关联，并把 pwsh、Windows Terminal 设为默认。
>
> 当 AI 助手在 Windows 上执行命令出现这些症状时，基本都是 5.1 太老所致：报「字符串缺少终止符」、中文输出乱码、内联命令的引号被拆散、连接 GitHub 下载超时、脚本里不能用 `&&` 或 `?:` 三元运算、`Select-String` 检索太慢。
>
> 安装器探测优先：机器上已有 pwsh 就直接复用，绝不重复下载；六个工具也优先复用系统已装的。全程免管理员（只写 `HKCU` 与用户目录）、幂等（连跑两次结果一致）、可断网（`-ZipPath` 指定本地包）。自带六段体检脚本与 38 项回归测试。

**英文（若表单要求）：**

> Fixes Chinese mojibake and the recurring errors that AI assistants hit when calling Windows PowerShell 5.1. Installs PowerShell 7 (pwsh) plus six Rust CLI tools — ripgrep, fd, fzf, bat, delta, jq — wires UTF-8 through profiles, console and file associations, and makes pwsh + Windows Terminal the default. Probe-first: reuses existing installations instead of re-downloading. No admin rights, idempotent, offline-installable, with a six-section health check and 38 regression tests.

---

## 四、「试试这样问我」（示例提问，填 4~5 条）

1. 帮我在 Windows 上装好 PowerShell 7，顺便把 rg、fd、fzf 这几个工具也装上
2. 我的命令行中文一直是乱码，`rg` 搜出来的中文也是乱码，帮我修一下
3. AI 跑 PowerShell 老报「字符串缺少终止符」，还有 `&&` 不能用，是什么问题？
4. 用 rg 帮我搜一下这个目录里所有 TODO，别用 Select-String，太慢了
5. 帮我体检一下 PowerShell 环境：pwsh、rg、fd、fzf、bat、delta、jq 是不是都正常

---

## 五、权限声明（审核重点，如实填）

### 需要的权限

| 权限 | 具体位置 | 用途 | 可否关闭 |
|---|---|---|---|
| 用户级文件写入 | `%LOCALAPPDATA%\ps7-toolkit` | 存放 pwsh 与六个工具 | 是（`-ToolsRoot` 可装到任意盘） |
| 用户级注册表写入 | `HKCU\Environment`（PATH）、`HKCU\...\App Paths\pwsh.exe`、`HKCU\Software\Microsoft\Classes\.ps1`、`HKCU\Console\%%Startup` | 让 `pwsh` 能直接敲、双击 `.ps1` 用 pwsh 打开、默认终端设为 Windows Terminal | 是（`-SkipDefaults` 全跳过） |
| 用户 profile 追加 | `Documents\PowerShell\...profile.ps1`（7.x）<br>`Documents\WindowsPowerShell\...profile.ps1`（5.1） | 写入 UTF-8 输出编码设置 | 是（同上） |
| 配置文件改写 + 备份 | Windows Terminal / VSCode 的 `settings.json`；改前生成 `settings.json.ps7bak` | 加一条 PowerShell 7 profile 并设为默认 | 是（同上） |
| 网络访问（仅安装阶段） | `api.github.com`、`github.com`、`aka.ms`、`gh-proxy.com`、`ghfast.top`、`ghproxy.net` | 下载官方发布包；镜像仅国内加速回退 | 否（断网用 `-ZipPath` 或复用已装版本） |

### 明确不做的事

- **不需要管理员权限**，不弹 UAC，全程用户级。
- **不写 `HKEY_LOCAL_MACHINE`**。
- **不修改系统区域设置**（不动 `HKLM\...\Nls\CodePage\ACP`），不影响老的 GBK 程序。
- **不劫持 `powershell.exe`**，系统自带的 5.1 原样保留。
- **不装服务、不加计划任务、不改防火墙、不碰杀软配置**。
- **不收集数据、不上报遥测、不需要 API Key**。
- 脚本内无硬编码凭证，无 `Invoke-Expression`、无 base64 载荷、无混淆。

### 数据流向

仅在有下载动作时向上述域名发起 GET 请求获取公开二进制，无任何出站上报。所有被改动的配置文件都会在同目录留一份 `.ps7bak`。

---

## 六、使用说明（技能详情页「怎么用」/ 审核说明）

### 给终端用户

1. 在技能目录下执行：`powershell -ExecutionPolicy Bypass -File ".\scripts\install.ps1"`
2. 重开终端 / 常用应用（PATH 才会刷新）
3. 验证：`pwsh -v` 显示 7.x；`rg --version` 显示 ripgrep；完整状态跑 `.\scripts\verify.ps1`

### 给 AI 助手

1. 先 `scripts\install.ps1 -CheckOnly` 看现状（只读）
2. 再 `scripts\install.ps1` 部署
3. 用 `scripts\verify.ps1 -Json` 拿机器可读体检结果
4. 之后按 `SKILL.md` 规范执行：命令走 `pwsh`；复杂脚本写成 `.ps1` 再 `-File`（避免内联引号被拆散）；检索用 `rg` 不用 `Select-String`；给 5.1 跑的 `.ps1` 存 UTF-8 with BOM

### 常用参数

| 参数 | 说明 |
|---|---|
| `-CheckOnly` | 只体检、零改动（建议第一步） |
| `-ToolsRoot` | 自定义安装根目录（默认 `%LOCALAPPDATA%\ps7-toolkit`） |
| `-ZipPath` | 用本地安装包，跳过自动搜索（断网 / 内网） |
| `-Mirror` | 自定义下载镜像，插到内置列表最前 |
| `-SkipDefaults` | 只装不配，PATH / 注册表 / 快捷方式全不碰 |
| `-SkipRustTools` | 只装 PowerShell 7 |
| `-Force` | 把 pwsh 也放进 `-ToolsRoot`（已装则复制，1 秒完成） |

---

## 七、包内文件

```
powershell7-toolkit/
├── SKILL.md                      AI 执行说明书（何时调用、怎么装、怎么用）
├── README.md                     给人看的使用文档
├── CHANGELOG.md                  版本记录（1.1.0 → 1.1.5）
├── LICENSE                       MIT
├── assets/icon.png               512×512 图标
├── scripts/install.ps1           主安装器（探测优先 + 自动下载兜底）
├── scripts/setup-defaults.ps1    默认化（profile / 注册表 / 关联 / 快捷方式 / 终端 / VSCode）
├── scripts/verify.ps1            六段体检，支持 -Json
├── scripts/wt-config.ps1         配置文件定点改写（JSONC 安全、带备份）
├── scripts/smoke-test.ps1        38 项回归测试（隔离沙箱，退出码可接 CI）
└── references/troubleshooting.md 常见踩坑与排错
```

---

## 八、已知风险与缓解（审核说明栏可贴这张表）

| 风险 | 缓解 |
|---|---|
| 会改用户 PATH 与注册表默认项 | 全在 `HKCU` 与用户目录；`-SkipDefaults` 可完全跳过；SKILL.md 第八节逐项列改动点与撤销命令 |
| 通过第三方镜像下载二进制 | 优先官方 `api.github.com` 取真实下载地址、官方 `aka.ms` 短链；镜像仅国内加速回退；可用 `-Mirror` 指定自有源 |
| 下载后无哈希校验 | 已如实声明；来源为各项目官方 GitHub Releases，二进制可 `--version` 核对 |
| 改写终端 / 编辑器配置 | 文本级定点修改，只动必要字段；改前生成 `.ps7bak`，改后自检能否解析，解析失败不落盘 |
| 关联 `.ps1` 双击执行 | 仅改 `HKCU\Software\Microsoft\Classes\.ps1`，删键即还原；实际执行仍受系统执行策略约束 |
| 卸载需手动 | README 与 SKILL.md 都给步骤：删目录 + 删 3 处注册表项 + 删 profile 段落 |

---

## 九、版本更新说明（若表单有「更新日志」栏）

> **1.1.5** —— 修 8 处「检查看着是绿的、其实什么都没确认」的问题：体检把「全 0 GUID」误报成已配置；
> 默认终端的注册表写入会被配置文件解析失败连带跳过；改写终端 / VSCode 配置会吃掉注释、并删掉用户自建的 profile；
> 改写后会丢原文件 BOM；值本来就对时也会重写一次；独立运行时往 PATH 加一条不存在的目录；
> 备份只在真要改时才生成（等于没有还原点）。回归测试从 23 项扩到 38 项。
> 命令行参数无变化，老用户重跑一次 `setup-defaults.ps1` 即可。

---

## 十、审核可能提的问题与答复

| 可能被问 | 建议答复 |
|---|---|
| 为什么要改注册表和 PATH？ | 不改的话 `pwsh`、`rg` 在新开终端里敲不到，`.ps1` 双击仍会走 5.1。全部在 `HKCU`，`-SkipDefaults` 可一键跳过。 |
| 为什么从第三方镜像下载？ | 国内直连 GitHub Releases 常超时。默认先请求官方 API 拿真实地址，失败才按顺序尝试镜像，官方 `aka.ms` 也在列表内；用户可用 `-Mirror` 换成自有源。 |
| 会不会影响系统自带的 PowerShell？ | 不会。不覆盖、不重定向 `powershell.exe`，5.1 原样保留；新装的 pwsh 是独立目录 + 独立命令。 |
| 卸载干净吗？ | 删安装目录 + 3 处 `HKCU` 项 + 两个 profile 里的标记段落，README「卸载」一节有逐条命令。 |
| 有遥测吗？ | 没有。全部代码可见，无上报端点。 |
| 为什么只有 Windows？ | 脚本依赖 Windows 的注册表、profile 路径、`Expand-Archive` 与 `HKCU` 语义，在 macOS / Linux 上无意义。 |

---

## 十一、已知的坑（真踩过）

1. **包结构**：第一层必须是 `powershell7-toolkit/`。传成根目录平铺会解析失败。所以用 `-workbuddy.zip`，不要用另一个。
2. **`.md` 编码**：`SKILL.md` 必须是 UTF-8（带不带 BOM 都可，平台能识别）；`.ps1` 必须带 BOM，否则 Windows PowerShell 5.1 按 GBK 解析直接报错。
3. **`description` 里不能有尖括号 `< >`**，平台与 ClawHub 都会校验。
4. **YAML 冒号后必须空一格**，值里含 `:`、`#` 要用引号包起来——我们已经全部用双引号。
5. **`category` 不是必填项**。平台官方的 Frontmatter 必填表只有 5 个：
   `description` / `description_zh` / `description_en` / `version` / `author`，我们全部满足。
   文档里 `category` 的示例值是 `writing`，我们填的是 `development`——若提交页报「分类不合法」，
   改这一行或直接删掉，重新打包上传即可。
6. **提交后能改的地方有限**：名称/版本/描述来自包内 `SKILL.md`，页面上改不了，要回文件改再重传。
7. **审核通过 ≠ 已上架**：必须先点「发布」并选「公开发布」，否则一直是「待发布」。

---

## 十二、发布前自检

- [x] ZIP 第一层是 `powershell7-toolkit/`，含 `SKILL.md`
- [x] 大小 58KB（平台限 3MB），目录最多两层
- [x] `SKILL.md` frontmatter 含 `name`（kebab-case）/ `version` / `display_name` / `display_name_en` / `description_zh` / `description_en` / `category` / `author`
- [x] 图标 512×512 PNG，9.7KB（限 500KB）
- [x] 5 个 `.ps1` 均 UTF-8 with BOM，`Parser::ParseFile` 零错误
- [x] 38 项回归测试全绿（隔离沙箱，不碰系统配置）
- [x] 无凭证、无 `Invoke-Expression`、无混淆
- [x] 包内不含 `PUBLISH.md`、不含 `.git`、不含缓存
- [x] GitHub Actions 五项检查全绿
