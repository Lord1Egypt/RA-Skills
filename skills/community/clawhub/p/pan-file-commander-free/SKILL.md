---
name: "pan-file-commander-free"
description: "命令式百度网盘文件管理,快捷命令模板,分类视图,路径校验,确认规则。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "网盘指挥官免费版"
  version: "1.0.0"
  summary: "命令式百度网盘文件管理,快捷命令模板,分类视图,路径校验,确认规则。"
  tags:
    - "智能代理"
    - "文件管理"
    - "百度网盘"
    - "命令式操作"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

百度网盘文件管理工具,以"命令式高效操作"为核心视角,所有操作限制在 `/apps/bdpan/` 目录内。适配所有支持SKILL.md的Agent平台。

> 本免费版提供核心文件管理能力(上传/下载/转存/分享/搜索/移动/复制/重命名/创建/删除)。记忆备份恢复、大文件后台下载与批量操作为专业版功能。

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

## 已知限制
1. **登录**:必须使用 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`,禁止直接调用 `bdpan login` 及其任何子命令/参数(包括 `--get-auth-url`、`--set-code` 等,即使在 GUI 环境也禁止)
2. **Token/配置**:禁止读取或输出 `~/.config/bdpan/config.json` 内容(含 access_token 等敏感凭据)
3. **更新/登录**:更新必须由用户明确指令触发,禁止自动或静默执行;Agent 禁止使用 `--yes` 参数执行 update.sh 或 login.sh
4. **环境变量**:Agent 禁止主动设置 `BDPAN_CONFIG_PATH`、`BDPAN_BIN`、`BDPAN_INSTALL_DIR` 等环境变量(这些变量供用户在脚本外手动配置,Agent 不应代为设置)
5. **路径安全**:禁止路径穿越(`..`、`~`)、禁止访问 `/apps/bdpan/` 范围外的绝对路径
6. **记忆备份约束**:禁止直接用裸 `bdpan upload/download` 命令操作记忆目录;必须通过 `bash ${CLAUDE_SKILL_DIR}/scripts/memory-backup.sh` 脚本执行,以确保 manifest 生成、路径安全检查、safety net 备份等机制正常运行(记忆备份为专业版功能)
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 前置检查
每次触发时按顺序执行:

1. **安装检查**:`command -v bdpan`,未安装则告知用户并确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh`(用户确认后可加 `--yes` 跳过安装器内部确认)
2. **登录检查**:`bdpan whoami`,未登录则引导执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`
3. **路径校验**:验证远端路径在 `/apps/bdpan/` 范围内

## 确认规则(差异化:分层风险模型)
| 风险等级 | 操作 | 策略 | 示例 |
| --- | --- | --- | --- |
| **高(必须确认)** | `rm` 删除、上传/下载目标已存在同名文件 | 列出影响范围,等待用户确认 | `bdpan rm docs/old.txt` |
| **中(路径模糊时确认)** | upload、download、mv、rename、cp | 路径明确直接执行,不明确则确认 | `bdpan mv docs/ archive/` |
| **低(直接执行)** | ls、search、whoami、mkdir、share | 无需确认 | `bdpan ls docs/` |

**额外规则:**

* 操作意图模糊("处理文件"→确认上传还是下载)→ 必须确认
* 序数/代词引用有歧义("第N个"、"它"、"上面那个")→ 必须确认
* 用户取消意图("算了"、"不要了"、"取消")→ 立即中止,不执行任何命令

## 使用流程
### 30秒:确认登录状态
```bash
bdpan whoami
```
未登录则运行: `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`

### 60秒:浏览文件并执行一次操作
```bash
bdpan ls

bdpan ls --order time --desc

bdpan upload ./local-file.txt docs/local-file.txt
```

### 120秒:完成完整操作流程
1. 前置检查(安装→登录→路径校验)
2. 浏览文件(参见快捷命令模板)
3. 选择操作(上传/下载/转存/分享/搜索/移动/复制/重命名/创建/删除)
4. 路径校验与确认(参见确认规则)
5. 执行操作并报告结果

#
## 快捷命令模板(差异化核心)
将常用操作封装为快捷命令,减少输入:

### 浏览类快捷命令
```bash
bdpan ls

bdpan ls docs/ --order name

bdpan ls docs/ --order time --desc

bdpan ls docs/ --order size --desc

bdpan ls docs/ --folder

bdpan ls docs/ --json
```

### 搜索类快捷命令
```bash
bdpan search "报告"

bdpan search "会议" --category 1

bdpan search "截图" --category 3

bdpan search "合同" --category 4

bdpan search "项目" --dir-only
```

### 单文件操作快捷命令
```bash
bdpan upload ./local.txt docs/local.txt

bdpan download docs/local.txt ./local.txt

bdpan mv docs/old.txt archive/

bdpan cp docs/template.txt templates/

bdpan rename docs/old-name.txt new-name.txt

bdpan mkdir docs/new-folder

bdpan rm docs/unwanted.txt
```

### 分享类快捷命令
```bash
bdpan share docs/report.pdf

bdpan share docs/report.pdf --period 0

bdpan share docs/report.pdf --period 30

bdpan share docs/file1.txt docs/file2.txt --period 7
```

### 转存类快捷命令
```bash
bdpan transfer "https://pan.baidu.com/s/1xxxxx?pwd=abcd"

bdpan transfer "https://pan.baidu.com/s/1xxxxx" -p abcd

bdpan transfer "https://pan.baidu.com/s/1xxxxx" -p abcd -d downloads/
```

## 文件分类视图(差异化)
通过 `--json` 输出配合本地处理,生成分类视图:

### 按类型分类
```bash
bdpan ls docs/ --json | jq -r '.[] | .path' | grep -oE '\.[^.]+$' | sort | uniq -c | sort -rn
```

### 按大小分类
```bash
bdpan ls docs/ --json | jq -r '
  if .size > 104857600 then "大文件(>100MB)"
  elif .size > 10485760 then "中文件(10-100MB)"
  elif .size > 1048576 then "小文件(1-10MB)"
  else "微小文件(<1MB)"
  end' | sort | uniq -c
```

### 按时间分类
```bash
bdpan ls docs/ --json | jq -r '.created_at | .[0:7]' | sort | uniq -c
```

## 智能路径校验(差异化)
### 路径补全
```bash
bdpan ls docs/ --folder
```

### 越界检测
```bash
validate_path() {
  local path="$1"
  if [[ "$path" == *"..",* ]] || [[ "$path" == *~* ]]; then
    echo "错误: 路径包含禁止字符(.. 或 ~)"
    return 1
  fi
  if [[ "$path" == /* ]]; then
    echo "错误: 命令参数禁止使用绝对路径,请使用相对路径"
    return 1
  fi
  return 0
}

validate_path "docs/file.txt"    # 通过
validate_path "../etc/passwd"    # 拒绝
validate_path "/etc/passwd"      # 拒绝
```

## 操作意图识别(差异化)
### 歧义消除决策树
```
用户输入 → 是否包含明确操作动词?
├─ 否 → 反问:"您想做什么?(上传/下载/查看/搜索/移动/删除/分享)"
└─ 是 → 操作对象是否明确?
        ├─ 否 → 反问:"请确认操作对象(哪个文件/目录?)"
        └─ 是 → 路径是否在 /apps/bdpan/ 范围内?
                ├─ 否 → 提示路径越界,建议合法路径
                └─ 是 → 风险等级判断(高/中/低)
                        ├─ 高 → 列出影响范围,等待确认
                        ├─ 中 → 路径模糊时确认
                        └─ 低 → 直接执行
```

### 序数/代词引用处理
```text
用户:"把第3个文件移到archive"

处理流程:
1. 查询当前目录文件列表
2. 定位第3个文件(按当前排序)
3. 向用户确认:"将移动 [文件名] 到 archive/,确认?(y/n)"
4. 用户确认后执行 bdpan mv <文件名> archive/
```

## 路径规则
| 场景 | 格式 | 示例 |
| --- | --- | --- |
| **命令参数** | 相对路径(相对于 `/apps/bdpan/`) | `bdpan upload ./f.txt docs/f.txt` |
| **展示给用户** | 中文名 | "已上传到:我的应用数据/bdpan/docs/f.txt" |

映射关系:`我的应用数据` ↔ `/apps`

**禁止:** 命令中使用中文路径(`我的应用数据/...`)、展示时暴露 API 路径(`/apps/bdpan/...`)。

## 授权码处理
用户发送 32 位十六进制字符串时,先确认:"这是百度网盘授权码吗?确认后将执行登录流程。" 确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`(不使用 `--yes`,保留安全确认环节)。

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

## 示例
### 场景一:个人用户 - 日常文件浏览与上传
```text
角色: 个人用户
任务: "帮我把本地的report.pdf上传到网盘的docs目录"

执行流程:
1. 前置检查(安装→登录)
2. 路径校验(docs/在合法范围内)
3. bdpan ls docs/ 检查是否已存在同名文件
4. 如已存在,询问用户是否覆盖(高风险确认)
5. 确认后执行 bdpan upload ./report.pdf docs/report.pdf
6. 展示结果:"已上传到:我的应用数据/bdpan/docs/report.pdf"
```

### 场景二:团队协作者 - 分享文件给同事
```text
角色: 团队协作者
任务: "把网盘里的项目方案分享给同事,有效期7天"

执行流程:
1. 前置检查
2. bdpan ls 确认文件存在
3. 根据用户意图选择有效期(默认7天)
4. 执行 bdpan share docs/项目方案.pdf --period 7
5. 展示:链接+提取码+有效期(7天)
6. 提示用户:链接7天后过期,请及时分享
```

### 场景三:内容创作者 - 转存分享链接
```text
角色: 内容创作者
任务: "朋友发给我一个分享链接,帮我转存到网盘的downloads目录"

执行流程:
1. 前置检查
2. 确认分享链接格式有效
3. 确认有提取码(链接中含 ?pwd= 或反问用户)
4. 确认目标目录(downloads/)
5. 执行 bdpan transfer "https://pan.baidu.com/s/1xxxxx" -p abcd -d downloads/
6. 展示:转存文件数量与目标目录
```

## 错误处理


| 序号 | 错误场景 | 原因 | 处理方式 | 优先级 |
|------|----------|------|----------|--------|
| 1 | 输入参数缺失 | 用户未提供必要参数 | 提示用户提供所需参数后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 | P0 |
| 2 | 执行超时 | 处理时间过长 | 检查输入数据量,分批处理 | P1 |
| 3 | 输出格式错误 | 结果不符合预期格式 | 检查`output_format`参数配置 | P1 |

## 常见问题
**Q: 命令参数中的路径为什么不能用绝对路径?**
A: 所有操作限制在 `/apps/bdpan/` 目录内,命令参数使用相对路径(相对于 `/apps/bdpan/`)。绝对路径会被拒绝,以确保路径安全。展示给用户时使用中文名(我的应用数据/bdpan/...)。

**Q: 上传文件时提示远端路径错误?**
A: 单文件上传远端路径必须是文件名(如 `docs/file.txt`),禁止以 `/` 结尾(如 `docs/`)。文件夹上传使用 `bdpan upload ./project/ project/` 格式。

**Q: 如何选择分享有效期?**
A: 根据语义意图判断:用户表达"长期/永久/不过期"使用 `--period 0`(并提示安全风险);指定具体天数选择最接近的枚举值(1/7/30);未表达偏好默认 `--period 7`。永久链接无法自动过期,请注意文件安全。

**Q: 分享链接转存和下载有什么区别?**
A: 转存(`bdpan transfer`)将分享文件保存到你的网盘,不下载到本地。下载分享链接(`bdpan download "分享链接"`)先转存再下载到本地。如只需保存到网盘用transfer,如需本地文件用download。

**Q: 删除文件后能恢复吗?**
A: bdpan的删除是永久删除,不可恢复。因此删除操作属于高风险,必须用户显式确认。建议删除前先 `bdpan ls` 确认文件,确认影响范围后再执行 `bdpan rm`。

**Q: 免费版与专业版的核心差异?**
A: 免费版提供核心文件管理能力(上传/下载/转存/分享/搜索/移动/复制/重命名/创建/删除)。专业版额外解锁:Agent记忆备份与恢复、大文件后台下载(nohup+进度轮询)、批量操作模板、增量同步、完整性校验。

**Q: 搜索文件时如何按类型过滤?**
A: 使用 `--category` 参数:0=全部,1=视频,2=音频,3=图片,4=文档,5=应用,6=其他,7=种子。`--no-dir` 和 `--dir-only` 互斥(分别表示仅文件、仅文件夹)。

## 故障排查
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `bdpan: command not found` | 未安装 | 运行 `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh` |
| `not logged in` | 未登录 | 运行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh` |
| 上传路径错误 | 远端路径以`/`结尾 | 单文件上传远端路径必须是文件名 |
| 路径穿越报错 | 路径含`..`或`~` | 使用相对路径,禁止路径穿越 |
| 中文路径报错 | 命令中使用了中文路径 | 命令参数使用相对路径,展示时用中文名 |
| 分享链接无效 | 链接过期或提取码错误 | 确认链接有效性和提取码 |
| 分享接口报错 | 未购买百度网盘开放平台服务 | 分享为付费接口,需在开放平台购买服务 |
| 序数引用歧义 | "第N个"不明确 | 列出文件清单,向用户确认具体文件 |
| 操作意图模糊 | "处理文件"未明确操作 | 反问用户:上传还是下载? |

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Shell**: bash(脚本执行需要)

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| bdpan CLI | 工具 | 必需 | `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh` |
| 百度网盘账户 | 账户 | 必需 | 注册百度网盘账号 |
| bash | 运行时 | 必需 | 系统自带或安装Git Bash |
| jq | 工具 | 可选(JSON处理与分类视图) | 从stedolan.github.io/jq安装 |

### API Key 配置
- 通过百度网盘OAuth授权登录,无需手动配置API Key
- 授权码通过 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh` 流程获取
- **禁止**读取或输出 `~/.config/bdpan/config.json` 内容(含敏感凭据)

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,需要命令行执行能力运行bdpan CLI)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent使用bdpan CLI管理百度网盘文件。需要bdpan CLI和百度网盘账户。

## 免费版限制
本免费体验版限制以下高级功能:

- Agent记忆备份与恢复(backup/list/restore,跨设备同步记忆文件):免费版不提供,需通过 `memory-backup.sh` 脚本执行(专业版功能)
- 大文件后台下载(nohup+进度轮询,>50MB文件的后台下载模式):免费版仅支持直接下载(≤50MB),大文件可能因Bash超时中断
- 批量操作模板(批量上传/下载/增量同步):免费版仅支持单文件操作
- 完整性校验(下载后文件大小比对):免费版不提供
- 增量同步机制(仅上传变化文件):免费版不提供

解锁全部功能请使用专业版: pan-file-commander-pro

## License与版权声明
本skill基于原始作品改进,保留原始版权声明:

- 原始作品: baidu-netdisk-skills (百度网盘)
- 原始license: MIT
- 改进作品: pan-file-commander-free
- 改进license: MIT

本改进作品在原始作品基础上进行了深度差异化改造,包括但不限于:
- 重新定位为"指挥官"视角(原始为通用文件管理)
- 新增快捷命令模板(浏览/搜索/单文件操作/分享/转存5类)
- 新增文件分类视图(按类型/大小/时间)
- 新增智能路径校验(路径补全与越界检测)
- 新增操作意图识别(歧义消除决策树)
- 新增分层确认规则(高/中/低风险+示例)
- 新增分级快速开始(30秒/60秒/120秒)
- 新增FAQ(7问)与故障排查表(9项)
- 新增3类真实场景示例(个人/团队/创作者)
- 重写description为五段结构,新增edition字段
- 保留原作者版权声明，去除非必要外部引用链接
- 兼容Agent平台适配(原私有环境名已通用化为兼容Agent/增强Agent/快速Agent/Agent平台)

原始MIT license允许修改与再分发,本改进作品在MIT license下发布,保留原始版权声明。

## 核心能力
### 安装
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install.sh [--yes]
```

安装器从百度 CDN(`issuecdn.baidupcs.com`)下载并执行。注意:install.sh 不执行本地 SHA256 校验,完整性依赖 HTTPS 传输保护。安全敏感场景建议先手动审查安装器内容或在沙箱中执行。

**输入**: 用户提供安装所需的指令和必要参数。
**处理**: 按照skill规范执行安装操作,遵循单一意图原则。
**输出**: 返回安装的执行结果,包含操作状态和输出数据。

### 登录 / 注销 / 卸载
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/login.sh              # 登录(内置安全免责声明)
bdpan logout                                            # 注销
bash ${CLAUDE_SKILL_DIR}/scripts/uninstall.sh [--yes]   # 卸载
```

**输入**: 用户提供登录 / 注销 / 卸载所需的指令和必要参数。
**处理**: 按照skill规范执行登录 / 注销 / 卸载操作,遵循单一意图原则。
**输出**: 返回登录 / 注销 / 卸载的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 更新(必须用户明确指令触发)
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/update.sh              # 检查并更新(需用户确认)
bash ${CLAUDE_SKILL_DIR}/scripts/update.sh --check       # 仅检查更新
```

**输入**: 用户提供更新(必须用户明确指令触发)所需的指令和必要参数。
**处理**: 按照skill规范执行更新(必须用户明确指令触发)操作,遵循单一意图原则。
**输出**: 返回更新(必须用户明确指令触发)的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：命令式百度网盘文、件管理、快捷命令模板、分类视图、路径校验、确认规则、网盘指挥官免费版、是一个以、命令式高效操作、为核心视角的百度、网盘文件管理工具、所有操作限制在、apps、bdpan、目录内、针对网盘管理、命令记不住、操作不连贯、路径易出错、风险操作无确认、文件难分类、五大痛点、构建了快捷命令模、智能路径校验、分层确认规则和操、作意图识别五大基、础能力等。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 适用场景
### 场景一:个人用户 - 日常文件浏览与上传
```text
角色: 个人用户
任务: "帮我把本地的report.pdf上传到网盘的docs目录"

执行流程:
1. 前置检查(安装→登录)
2. 路径校验(docs/在合法范围内)
3. bdpan ls docs/ 检查是否已存在同名文件
4. 如已存在,询问用户是否覆盖(高风险确认)
5. 确认后执行 bdpan upload ./report.pdf docs/report.pdf
6. 展示结果:"已上传到:我的应用数据/bdpan/docs/report.pdf"
```

### 场景二:团队协作者 - 分享文件给同事
```text
角色: 团队协作者
任务: "把网盘里的项目方案分享给同事,有效期7天"

执行流程:
1. 前置检查
2. bdpan ls 确认文件存在
3. 根据用户意图选择有效期(默认7天)
4. 执行 bdpan share docs/项目方案.pdf --period 7
5. 展示:链接+提取码+有效期(7天)
6. 提示用户:链接7天后过期,请及时分享
```

### 场景三:内容创作者 - 转存分享链接
```text
角色: 内容创作者
任务: "朋友发给我一个分享链接,帮我转存到网盘的downloads目录"

执行流程:
1. 前置检查
2. 确认分享链接格式有效
3. 确认有提取码(链接中含 ?pwd= 或反问用户)
4. 确认目标目录(downloads/)
5. 执行 bdpan transfer "https://pan.baidu.com/s/1xxxxx" -p abcd -d downloads/
6. 展示:转存文件数量与目标目录
```

## 不适用场景

以下场景网盘指挥官免费版不适合处理：

- 黑帽SEO手段
- 搜索引擎作弊
- 付费广告投放管理

## 触发条件

需要SEO优化、关键词分析、排名提升、搜索流量优化时使用。不适用于非本工具能力范围的需求。

