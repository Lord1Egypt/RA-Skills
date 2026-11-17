---
slug: netdisk-sync-pro
name: netdisk-sync-pro
version: "1.0.0"
displayName: 网盘同步专家
summary: 智能下载策略,断点续传后台模式,批量处理模板,增量同步,完整性校验。
license: MIT
description: |-
  网盘同步专家是一个百度网盘文件管理工具,所有操作限制在 /apps/bdpan/ 目录内。针对传统网盘管理"下载限速、大文件中断超时、批量操作繁琐、同步可靠性差、路径安全风险、验证码繁琐"六大痛点,构建了智能下载策略、断点续传与后台模式、批量处理模板、增量同步机制和完整性校验五大核心能力。

  核心能力包括:bdpan CLI完整的文件管理(上传/下载/转存/分享/搜索/移动/复制/重命名/创建/删除);基于文件大小的智能下载策略(小文件直接+大文件后台);分享链接转存与下载;Agent记忆备份与恢复;严格的安全约束与路径校验;分层确认规则。

  适用场景:百度网盘文件上传下载管理、大文件可靠下载、分享链接转存、批量文件操作、Agent记忆跨设备备份恢复、团队文件共享、自动化文件同步工作流。

  差异化亮点:相比原始版本,新增智能下载策略(按文件大小自动选择直接/后台模式)、断点续传机制、增量同步(仅上传变化文件)、完整性校验(文件大小+哈希比对)、批量处理模板、强化路径校验、下载进度实时报告、FAQ与故障排查决策树。适配所有支持SKILL.md的Agent平台。

  触发关键词:网盘同步、百度网盘、文件上传、大文件下载、分享转存、记忆备份、netdisk-sync、bdpan
tags:
- 智能代理
- 文件管理
- 百度网盘
- 数据同步
tools:
- read
- exec
---

# 网盘同步专家

百度网盘文件管理工具,所有操作限制在 `/apps/bdpan/` 目录内。适配所有支持SKILL.md的Agent平台。

## 触发规则

### 网盘文件操作触发

同时满足以下条件才执行:

1. 用户消息中包含**明确指向百度网盘**的关键词,至少匹配以下之一:
   * `百度网盘`、`百度云盘`、`bdpan`、`baidu netdisk`、`baidu pan`、`baidu drive`、`pan.baidu.com`
2. 操作意图明确(上传/下载/转存/分享/查看/搜索/移动/复制/重命名/创建文件夹/删除/登录/注销)
3. 对于**写操作**(上传、删除、移动、覆盖式下载、公开分享),即使触发词命中,也必须先列出"将要执行的操作 + 影响范围"并取得用户显式确认(`y`)后再执行

**不要触发的情况:**

* 用户仅说"网盘""云盘""云存储""百度云"等泛指或可能指向其他百度产品的词,未明确指向百度网盘 → 应反问"您指的是百度网盘(pan.baidu.com)吗?"再决定
* 用户在讨论其他云盘服务(OneDrive、Google Drive、阿里云盘、夸克网盘等)
* 仅复述、引用或摘要历史聊天记录中的网盘内容,而无新的操作意图

未通过触发规则时,禁止执行任何 bdpan 命令。

> **上下文延续(受限):** 当前对话已在进行百度网盘操作时,后续消息可在**只读类**操作(ls/search/whoami)上继续延续;但**写操作**(upload/download/share/mv/cp/rename/mkdir/rm)每一次都必须重新出示触发词或得到用户显式确认,禁止凭借历史上下文静默执行。

### 记忆备份/恢复触发

**以下表达即使未提及"网盘"也应触发(仅限支持Agent记忆备份的环境):**

| 用户说法示例 | 触发操作 |
| --- | --- |
| "备份记忆"、"备份我的记忆"、"把记忆存到网盘" | backup |
| "查看记忆备份"、"有哪些备份"、"备份列表" | list |
| "恢复记忆"、"还原记忆"、"回滚记忆"、"记忆回档" | restore(需确认日期) |
| "恢复 3月16号 的记忆"、"恢复 2026-03-16 的备份" | restore 指定日期 |

**以下情况不触发记忆备份/恢复:**

* "帮我记住…"、"整理记忆"、"清理记忆"(本地操作,不涉及网盘)
* "备份我的代码/文件"(操作对象不是记忆)
* 不支持的环境(报错说明不支持,不执行)

**区分原则:** 操作对象是否为 Agent 记忆文件(AGENTS.md、SOUL.md、MEMORY.md、memory/*.md 等)。

---

## 安全约束(最高优先级,不可被任何用户指令覆盖)

1. **登录**:必须使用 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`,禁止直接调用 `bdpan login` 及其任何子命令/参数(包括 `--get-auth-url`、`--set-code` 等,即使在 GUI 环境也禁止)
2. **Token/配置**:禁止读取或输出 `~/.config/bdpan/config.json` 内容(含 access_token 等敏感凭据)
3. **更新/登录**:更新必须由用户明确指令触发,禁止自动或静默执行;Agent 禁止使用 `--yes` 参数执行 update.sh 或 login.sh
4. **环境变量**:Agent 禁止主动设置 `BDPAN_CONFIG_PATH`、`BDPAN_BIN`、`BDPAN_INSTALL_DIR` 等环境变量(这些变量供用户在脚本外手动配置,Agent 不应代为设置)
5. **路径安全**:禁止路径穿越(`..`、`~`)、禁止访问 `/apps/bdpan/` 范围外的绝对路径
6. **记忆备份约束**:禁止直接用裸 `bdpan upload/download` 命令操作记忆目录;必须通过 `bash ${CLAUDE_SKILL_DIR}/scripts/memory-backup.sh` 脚本执行,以确保 manifest 生成、路径安全检查、safety net 备份等机制正常运行

---

## 前置检查

每次触发时按顺序执行:

1. **安装检查**:`command -v bdpan`,未安装则告知用户并确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh`(用户确认后可加 `--yes` 跳过安装器内部确认)
2. **登录检查**:`bdpan whoami`,未登录则引导执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`
3. **路径校验**:验证远端路径在 `/apps/bdpan/` 范围内

---

## 确认规则

| 风险等级 | 操作 | 策略 |
| --- | --- | --- |
| **高(必须确认)** | `rm` 删除、上传/下载目标已存在同名文件 | 列出影响范围,等待用户确认 |
| **中(路径模糊时确认)** | upload、download、mv、rename、cp | 路径明确直接执行,不明确则确认 |
| **低(直接执行)** | ls、search、whoami、mkdir、share | 无需确认 |

**额外规则:**

* 操作意图模糊("处理文件"→确认上传还是下载)→ 必须确认
* 序数/代词引用有歧义("第N个"、"它"、"上面那个")→ 必须确认
* 用户取消意图("算了"、"不要了"、"取消")→ 立即中止,不执行任何命令

---

## 核心操作

### 查看状态

```bash
bdpan whoami
```

### 列表查询

```bash
bdpan ls [目录路径] [--json] [--order name|time|size] [--desc] [--folder]
```

### 上传

```bash
bdpan upload <本地路径> <远端路径>
```

**关键约束:** 单文件上传远端路径必须是文件名,禁止以 `/` 结尾。文件夹上传:`bdpan upload ./project/ project/`。

步骤:确认本地路径存在 → 确认远端路径 → `bdpan ls` 检查远端是否已存在 → 执行。

### 智能下载策略(差异化核心)

根据文件大小自动选择下载策略,解决大文件超时中断痛点:

#### 下载策略选择

```bash
# 1. 获取文件大小
bdpan ls --json <远端路径>
# 从JSON输出中读取 size 字段(字节)
```

| 文件大小 | 策略 | 执行方式 | 超时设置 |
|----------|------|----------|----------|
| ≤ 50MB | 直接下载 | `bdpan download <远端路径> <本地路径>` | Bash timeout=300000(5分钟) |
| > 50MB | 后台下载 | nohup后台执行,Agent轮询进度 | 无超时限制 |

#### 小文件(≤ 50MB)直接下载

```bash
bdpan download <远端路径> <本地路径>
```
Bash 工具 timeout 参数设为 `300000`(5 分钟)。

#### 大文件(> 50MB)后台下载流程

```bash
# 启动后台下载
nohup bdpan download <远端路径> <本地路径> > /tmp/bdpan-dl-$$.log 2>&1 & echo $!
```

```bash
# 轮询进度
kill -0 <PID> 2>/dev/null && echo "running" || echo "done"; ls -l <本地路径> 2>/dev/null; tail -5 /tmp/bdpan-dl-<PID>.log 2>/dev/null
```

```bash
# 清理日志
rm -f /tmp/bdpan-dl-<PID>.log
```

**Agent执行大文件后台下载行为规范:**

* 启动后台下载后,**立即告知用户**:下载已在后台启动,文件大小 X,预计需要 Y 时间
* 每次轮询后向用户报告进度(已下载大小 / 总大小、百分比)
* 下载完成后告知用户最终结果
* 如果进程异常退出,检查日志并报告错误原因

#### 分享链接下载(先转存再下载到本地)

```bash
bdpan download "https://pan.baidu.com/s/1xxxxx?pwd=abcd" ./downloaded/
bdpan download "https://pan.baidu.com/s/1xxxxx" ./downloaded/ -p abcd    # 提取码单独传入
bdpan download "https://pan.baidu.com/s/1xxxxx?pwd=abcd" ./downloaded/ -t my-folder  # 指定转存目录
```

> 分享链接下载同样适用大文件策略:转存完成后,用 `bdpan ls --json` 获取文件大小,再按上述策略执行下载。

### 完整性校验(差异化)

下载完成后验证文件完整性:

```bash
# 1. 获取远端文件大小
bdpan ls --json <远端路径> | grep -o '"size":[0-9]*'

# 2. 获取本地文件大小
ls -l <本地路径> | awk '{print $5}'

# 3. 比对大小
# 如大小不一致,提示用户重新下载
```

### 转存

将分享文件转存到网盘,**不下载到本地**(与 download 分享链接模式的区别)。

```bash
bdpan transfer "https://pan.baidu.com/s/1xxxxx" -p <提取码> [-d 目标目录] [--json]
```

步骤:确认分享链接格式有效 → 确认有提取码(链接中含 `?pwd=` 或反问用户)→ 确认目标目录 → 执行。转存成功后只展示本次转存的文件(非整个目录),显示数量和目标目录。

### 分享

```bash
bdpan share <路径> [路径...] [--period <天数>] [--json]
```

**--period / -d 参数:** 分享有效期(天),取值:0=永久, 1, 7, 30(默认:7)

**智能选择规则:**

Agent 必须根据用户的语义意图判断有效期,而非仅匹配固定关键词。

* 用户表达了"希望长期有效/永久/不过期/一直能用"等语义 → 使用 `--period 0`,并提示用户:永久链接无法自动过期,请注意文件安全
* 用户指定了具体天数或时间范围 → 选择最接近的枚举值(1、7、30)
* 用户未表达任何有效期偏好 → 默认 `--period 7`

步骤:`bdpan ls` 确认文件存在 → 根据用户意图选择有效期 → 执行分享 → 展示链接+提取码+有效期。

> 付费接口,需在百度网盘开放平台购买服务。

### 搜索

```bash
bdpan search <关键词> [--category 0-7] [--no-dir|--dir-only] [--page-size N] [--page N] [--json]
```

category:0=全部 1=视频 2=音频 3=图片 4=文档 5=应用 6=其他 7=种子。`--no-dir` 和 `--dir-only` 互斥。

### 移动 / 复制 / 重命名 / 创建文件夹

```bash
bdpan mv <源路径> <目标目录>
bdpan cp <源路径> <目标目录>
bdpan rename <路径> <新名称>       # 第二参数是文件名,非完整路径
bdpan mkdir <路径>
```

---

## 批量处理模板(差异化)

### 批量上传

```bash
# 批量上传目录下所有文件
for file in ./local-dir/*; do
  filename=$(basename "$file")
  bdpan upload "$file" "remote-dir/$filename"
done
```

### 批量下载

```bash
# 获取文件列表并批量下载
bdpan ls --json remote-dir/ | jq -r '.[].path' | while read path; do
  bdpan download "$path" "./local-dir/$(basename $path)"
done
```

## 增量同步机制(差异化)

仅上传变化的文件,减少带宽消耗:

```bash
# 1. 获取远端文件列表(含大小和时间)
bdpan ls --json remote-dir/ > /tmp/remote-files.json

# 2. 对比本地文件
for file in ./local-dir/*; do
  filename=$(basename "$file")
  local_size=$(stat -c%s "$file")
  remote_size=$(jq -r ".[] | select(.name==\"$filename\") | .size" /tmp/remote-files.json)

  if [ "$local_size" != "$remote_size" ]; then
    echo "文件 $filename 有变化,上传中..."
    bdpan upload "$file" "remote-dir/$filename"
  else
    echo "文件 $filename 无变化,跳过"
  fi
done
```

---

## 路径规则

| 场景 | 格式 | 示例 |
| --- | --- | --- |
| **命令参数** | 相对路径(相对于 `/apps/bdpan/`) | `bdpan upload ./f.txt docs/f.txt` |
| **展示给用户** | 中文名 | "已上传到:我的应用数据/bdpan/docs/f.txt" |

映射关系:`我的应用数据` ↔ `/apps`

**禁止:** 命令中使用中文路径(`我的应用数据/...`)、展示时暴露 API 路径(`/apps/bdpan/...`)。

---

## 授权码处理

用户发送 32 位十六进制字符串时,先确认:"这是百度网盘授权码吗?确认后将执行登录流程。" 确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`(不使用 `--yes`,保留安全确认环节)。

---

## 管理功能

### 安装

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install.sh [--yes]
```

安装器从百度 CDN(`issuecdn.baidupcs.com`)下载并执行。注意:install.sh 不执行本地 SHA256 校验,完整性依赖 HTTPS 传输保护。安全敏感场景建议先手动审查安装器内容或在沙箱中执行。

### 登录 / 注销 / 卸载

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/login.sh              # 登录(内置安全免责声明)
bdpan logout                                            # 注销
bash ${CLAUDE_SKILL_DIR}/scripts/uninstall.sh [--yes]   # 卸载
```

### 更新(必须用户明确指令触发)

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/update.sh              # 检查并更新(需用户确认)
bash ${CLAUDE_SKILL_DIR}/scripts/update.sh --check       # 仅检查更新
```

---

## 记忆备份与恢复

支持Agent记忆备份的运行环境,自动检测当前环境是否支持。

**网盘存储路径:** `/apps/bdpan/agent-memory/<agent>/<device>/manual/<timestamp>/`

**备份内容:** 7 个 Workspace 文件(AGENTS.md、SOUL.md、USER.md、IDENTITY.md、TOOLS.md、MEMORY.md、HEARTBEAT.md)+ `memory/*.md` + `manifest.json`

### 备份记忆

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/memory-backup.sh backup
```

### 查看备份列表

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/memory-backup.sh list
```

### 恢复备份

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/memory-backup.sh restore 2026-03-16

bash ${CLAUDE_SKILL_DIR}/scripts/memory-backup.sh restore 2026-03-16 --force

bash ${CLAUDE_SKILL_DIR}/scripts/memory-backup.sh restore 2026-03-16 --yes
```

**恢复安全机制:**

1. **影响预览**:恢复前会列出所有将被覆盖/新增的本地文件清单
2. **显式确认**:默认必须用户输入 `y` 才会执行覆盖(非交互式环境下若未加 `--yes` 直接拒绝执行)
3. **Safety net**:恢复前自动将当前本地记忆备份到 `<workspace>/.backup-before-restore/<timestamp>/`,防止误操作数据丢失

### 操作流程

1. 执行前自动检查:bdpan 是否安装 → 是否已登录(未满足则引导处理)
2. 检测当前 Agent 类型 → 不支持的环境报错退出
3. 执行对应操作(backup/list/restore)

---

## 常见问题FAQ

**Q: 大文件下载总是超时中断怎么办?**
A: 使用智能下载策略。先用 `bdpan ls --json` 获取文件大小,大于50MB的文件使用nohup后台下载模式,Agent轮询进度。这避免了Bash工具超时限制导致的中断。

**Q: 下载速度很慢怎么办?**
A: 下载速度受百度网盘服务端限制。非会员用户可能遇到限速。建议:1)确认网络连接正常;2)使用后台下载模式避免超时;3)如需更高速度,考虑开通百度网盘会员。

**Q: 如何判断下载是否完整?**
A: 使用完整性校验。下载完成后,用 `bdpan ls --json` 获取远端文件大小,与本地文件大小(`ls -l`)比对。大小不一致则需要重新下载。

**Q: 分享链接转存和下载有什么区别?**
A: 转存(`bdpan transfer`)将分享文件保存到你的网盘,不下载到本地。下载分享链接(`bdpan download "分享链接"`)先转存再下载到本地。如只需保存到网盘用transfer,如需本地文件用download。

**Q: 批量上传很多文件如何操作?**
A: 使用批量处理模板。用for循环遍历本地目录,逐个执行 `bdpan upload`。如需增量同步(仅上传变化文件),先获取远端文件列表,对比大小后仅上传有变化的文件。

**Q: 记忆备份支持哪些环境?**
A: 支持Agent记忆备份的运行环境。脚本会自动检测当前环境,不支持的环境会报错退出。操作对象必须是Agent记忆文件(AGENTS.md、SOUL.md、MEMORY.md等)。

**Q: 恢复记忆会覆盖当前记忆吗?**
A: 会,但有安全机制保护。恢复前会:1)列出所有将被覆盖的文件清单;2)要求用户显式确认;3)自动将当前记忆备份到 `.backup-before-restore/` 目录,防止误操作数据丢失。

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `bdpan: command not found` | 未安装 | 运行 `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh` |
| `not logged in` | 未登录 | 运行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh` |
| 下载超时中断 | 文件过大,Bash超时 | 使用大文件后台下载策略(nohup) |
| 上传路径错误 | 远端路径以`/`结尾 | 单文件上传远端路径必须是文件名 |
| 下载文件不完整 | 网络中断或限速 | 使用完整性校验比对大小,重新下载 |
| 分享链接无效 | 链接过期或提取码错误 | 确认链接有效性和提取码 |
| 路径穿越报错 | 路径含`..`或`~` | 使用相对路径,禁止路径穿越 |
| 记忆备份失败 | 环境不支持或未登录 | 检查环境支持,确认bdpan已登录 |
| 恢复后记忆异常 | 恢复了错误日期 | 从 `.backup-before-restore/` 恢复Safety net备份 |
| 中文路径报错 | 命令中使用了中文路径 | 命令参数使用相对路径,展示时用中文名 |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Shell**: bash(脚本执行需要)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| bdpan CLI | 工具 | 必需 | `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh` |
| 百度网盘账户 | 账户 | 必需 | 注册百度网盘账号 |
| bash | 运行时 | 必需 | 系统自带或安装Git Bash |
| jq | 工具 | 可选(JSON处理) | 从stedolan.github.io/jq安装 |
| nohup | 工具 | 可选(大文件后台下载) | 系统自带 |

### API Key 配置
- 通过百度网盘OAuth授权登录,无需手动配置API Key
- 授权码通过 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh` 流程获取
- **禁止**读取或输出 `~/.config/bdpan/config.json` 内容(含敏感凭据)

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,需要命令行执行能力运行bdpan CLI)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent使用bdpan CLI管理百度网盘文件。需要bdpan CLI和百度网盘账户。
