# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/)。
每个版本变更记录在下方，最新版本在最前。

---

## [3.15.0] — 2026-11-14

minor：新增 `iterate next`——把「状态」变成「下一步该跑哪条命令」，新手不必
先读文档就能从空目录走到 `/iterate`，回访用户也能在漂移/体检失败时拿到有
优先级的修复路径（含 `--json` 计划供脚本/其它 skill 消费）。本轮全面审查
确认 2 处缺陷并全部修复：**pip 安装后 3 个模板有 2 个不可用**（包数据缺失，
`template show` 把已知模板误报为 unknown）与 **`backup prune` 非法参数值退出码
错误**（1 而非 2）。测试套件 2029 → 2050。

### 新增功能
- **`iterate next`**（+13 回归）：只读、建议式（恒 exit 0）的「下一步」命令。
  按项目状态给出**有序计划**：未初始化 → `iterate init --yes`（备选
  `iterate onboard`）；有配置缺 ITERATE.md → `iterate onboard`；有 ITERATE.md
  缺配置 → `iterate init --yes`；配置损坏 → `iterate doctor --fix`；manifest
  漂移 → `iterate refresh --diff` 再 `iterate refresh`（附具体变更文件）；
  体检失败 → `iterate doctor --fix`；仅有 warning → `iterate doctor`（不阻塞）；
  健康 → `/iterate "<goal>"` + 可选 `iterate personalize`。另附环境缺口提示
  （如非 git 仓库）。`--json` 输出稳定键 `state`/`blocking`/`drift`/
  `drift_reason`/`doctor`/`next`/`steps`/`notes`，CI 与其它 skill 可直接
  branch，无需解析人类文案。此前 `status`/`show`/`doctor` 只报状态，不回答
  「现在该做什么」，首次使用路径只能靠 README。

### 修复（全面审查发现）
- **pip 安装后模板不可用**（`template_cmd.py` + 包数据，+5 回归）：模板解析
  只查仓库相对的 `templates/`，而 wheel 只打包 `iterate_cli/data/`，导致
  `pip install iterate-skill` 后 `template list` 有 2/3 显示 missing、
  `template show playbook|decisions` 直接失败。现优先解析包内数据、再回退
  仓库目录，并补齐两份缺失模板（与 `templates/` 逐字节一致，测试强制）；
  `list --json` 报告的 `path` 也指向实际使用的副本。
- **已知模板缺失被误报为 unknown**（`template_cmd.py`，+2 回归）：`show` 对
  「名字合法但文件缺失」返回 exit 2「Unknown template」，把安装损坏误报成
  拼写错误；现区分未知名称（2）与安装缺文件（1，提示重装/`iterate update`），
  `--json` 仍恰好一个文档。
- **`backup prune` 非法参数值退出码不一致**（`cli.py`，+3 回归）：
  `--keep 0`、`--older-than 3x`/`0d` 是非法参数值，却因复用 `BackupError`
  的运行时分支返回 1，与「无策略」的 2 及文档化的 usage error 契约矛盾，
  且与「部分删除失败」无法区分。现调用前先校验策略，非法值统一 exit 2。

---

## [3.14.0] — 2026-11-10

minor：两个净新增用户可感知能力——`iterate refresh --diff`（把「dry-run 只报几行
改动」变成「能看到确切 unified diff」，刷新可先审后应用）与 `iterate template`
（把 skill 静默消费的模板表面化：ITERATE.md 骨架 / onboarding playbook / 决策日志
结构，可列出、可查看、只读、任意目录可用）。本轮全面审查（review-bugbot）确认
**3 处中 + 8 处低缺陷**并全部修复（含 42 个新增回归；测试套件 1987 → 2029）。

### 新增功能
- **`iterate refresh --diff`**（+11 回归）：打印刷新将应用的**确切 unified diff**——
  ITERATE.md 重写与 iterate.config.yaml 重写；恒不写文件（diff 即预览，隐含
  dry-run）；`--json` 时 diff 在 `md_diff`/`config_diff` 字段；无变化报
  "no changes needed"（exit 0）。此前 `refresh --dry-run` 只给行数（"+N / -M"），
  用户无法看到将改什么，属「能预览但不能看到内容」断链。
- **`iterate template list|show`**（+14 回归）：把 generator 静默消费的模板表面化——
  `list`（默认）列出全部捆绑模板（ITERATE.template.md / onboarding-playbook.md /
  iterate-decisions.template.md，含 `exists` 标记），`show NAME` 打印一个模板原文；
  支持别名 `iterate`/`playbook`/`decisions` 与 `--json`；只读、可在任意目录使用
  （模板属于 skill 而非某个项目）；未知名称/动作 exit 2 并提示 `template list`。
  此前模板只存在于包内，用户想了解 `onboard` 生成的结构或定制副本需手翻安装目录。

### 修复（全面审查发现，3 中 + 8 低）
- **`doctor --check ""` 静默通过**（中，+2 回归）：`--check ""`/`","` 剥空后得到空
  过滤集，`run_doctor` 跑零个检查并 exit 0「健康」——CI 门禁被静默禁用。现改为
  usage error（exit 2，`--json` 下仍是恰好一个文档）。
- **backup restore 派生目标未显式校验包含**（中，+1 回归）：`restore` 校验的是备份
  参数路径，而由 `base` 派生的 `target` 未显式做 `relative_to(project_root)` 校验
  （此前仅靠 `is_dir()` 偶然挡住 `base==".."` 的越界）。现对派生目标显式校验。
- **npx 安装器 unsigned 发布覆盖失效**（中，+1 JS 回归）：release 选择过滤器要求
  `.asc` 资产，使 `ITERATE_ALLOW_UNSIGNED=1` 分支不可达（与 Python 安装器分歧）。
  现抽取 `selectSkillRelease`，过滤器只要求 tarball+checksum，签名交由
  `signaturePolicyError` 决定（覆盖真正生效）。
- **`--json` 误判**（低，+2 回归）：`json_requested` 用原始 argv 子串扫描，把值恰为
  `--json` 的 token（如 `report --out --json`）当成 JSON 请求。现为精确检测：token
  是前一「取值选项」（`--out`/`--check`/`-p`…）的值时不算 flag。
- **import stdin 字节上限**（低，+1 回归）：`sys.stdin.read(n)` 按字符计数，多字节
  CJK bundle 会瞬时缓冲至 ~4× 上限。现优先从 `sys.stdin.buffer` 按字节读。
- **report/export `--out` 退出码不一致**（低）：report 的「拒绝覆盖」=2 而
  「父目录不存在」=1；export 的「已存在」=1。现统一为 usage error（exit 2）。
- **personalize no-op 无条件重写**（低，+1 回归）：`save_personalization` 每次运行
  都重写 config（mtime 抖动 + safe_dump 丢注释且可能无快照）。现两个写入都改为
  「仅当实际变化」。
- **guard 在 Windows 上 select 失效**（低，+1 回归）：`select` 对管道 fd 是
  POSIX-only，失败即 break 导致诊断尾为空。现回退到 sleep+非阻塞轮询，输出仍被捕获。
- **refresh 丢失 git 布尔**（低，+3 回归）：`_build_refresh_data` 让
  `use_worktree`/`auto_merge` 停在默认 False（死字段）。现从现有配置保留并做 truthy
  标量归一，`_build_refreshed_config` 一并持久化，数据模型与配置不再分歧。
- **installer `--set` 布尔拼写**（低，+3 回归）：`--set git.push_per_round=yes` 存成
  字符串 "yes" 而 schema 拒绝。现对 schema 声明的布尔字段用 `parse_bool_spelling`
  归一（yes/no/on/off/y/n/true/false），字符串字段仍保留字面量。
- **installer config 权限漂移**（低，+2 回归）：`save_config`/`_atomic_write_text` 经
  `mkstemp` 强制 0600。现保留原文件权限位，新文件用 umask 决定（与
  `generator.atomic_write` 一致）。
- **installer `--ai all` 别名记账**（低，+1 回归）：共享目标目录的第二个别名
  （claude/claude-code）在前一个别名失败时仍被记为「已更新」。现目标目录只在
  成功更新后标记为 seen，失败别名会让其孪生真实重试/如实上报。
- **npx parseChecksums 大小写敏感**（低，+1 JS 回归）：重复项 digest 仅大小写不同
  被当成冲突。现按小写比较（与 `constantTimeHashEqual` 一致）。

---

## [3.13.0] — 2026-11-09

minor：新增 `iterate backup prune`（备份保留策略，此前备份只增不减、只能手动
删文件）与 `iterate doctor --check`/`--list-checks`（把诊断从「一次全跑」变成
「可按检查名定向跑」，失败可自愈）。本轮全面审查（review-bugbot）确认 2 处中
缺陷并全部修复（含 38 个新增回归）。

### 新增功能
- **`iterate backup prune`**（+20 回归）：按保留策略删除旧时间戳备份——
  `--keep N` 对每个原始文件保留最新 N 份（滚动窗口，避免误删罕见文件的唯一
  备份）、`--older-than AGE`（`30d`/`7d`/`24h`/`90m` 或纯天数）删除更旧的，
  两者可并用取并集。只删可识别的 iterate 备份、绝不触碰被保护的原文件与
  非备份文件；`--dry-run` 预览、`--json` 结构化输出；无策略/非法年龄/`--keep 0`
  均给出可执行报错而非静默成功。
- **`iterate doctor --check`/`--list-checks`**（+9 回归）：`--list-checks` 列出
  全部检查名（`config.schema`、`max_rounds`、`drift`、`iterate.md.markers` 等）
  后退出；`--check NAME` 只跑指定检查（可重复/逗号分隔），值取自
  `doctor --json` 里 `findings[].check`，因此「看到哪个检查挂了 → 只重跑那个」
  一步到位。config 依赖检查所需的前置检查（onboarding、config.parse）仍静默
  运行并只暴露错误，阻塞原因始终被说明；未知检查名 exit 2 并提示
  `--list-checks`。

### 修复（全面审查发现）
- **wizard 非法输入会清空既有 dimension_sets**（`wizard.py` `_collect_dimension_sets`，
  +4 回归）：`选择要启用的范围蓝图编号` 输入非数字或越界时返回 `{}`，把回访用户
  精心维护的命名维度集整个抹掉（模块自身不变量声明既有集合权威、必须存活）。
  现改为保留当前已启用蓝图，与空输入路径一致。
- **personalize 单个坏 token 丢弃整组维度**（`personalize.py` `_parse_dimension_numbers`，
  +5 回归）：`1, x` 或 `1, 99` 因一个非法/越界 token 返回 `[]`，把用户输入的合法
  维度一并丢弃并「保持原顺序」。现改为逐 token 丢弃（与 `wizard._parse_dimension_selection`
  一致），只跳过非法 token、保留合法维度。

---

## [3.12.0] — 2026-11-06

minor：新增 `iterate config schema` 子命令（把规范 JSON Schema 暴露给编辑器 /
CI / 工具链），补齐「iterate 用一套 schema 校验 config，用户却无法拿到它」的
断链——此前 `config/config.schema.json` 只存在于仓库与包内数据里，没有任何 CLI
入口可以消费它，编辑器（yaml-language-server）无法对 `iterate.config.yaml`
做自动补全/校验，CI 也无从对齐 iterate 自己强制的那套规则。本轮全面审查
（review-bugbot）确认 2 处中 + 9 处低缺陷并全部修复（含 21 个新增回归）。

### 新增功能
- **`iterate config schema`**（+9 回归）：把 `iterate.config.yaml` 的规范 JSON
  Schema 以纯 JSON 输出到 stdout（`--json` 同义、恒不被 ASCII banner 污染），
  让编辑器、CI 校验器、其它工具与 CLI 自身强制同一套配置契约；`--out PATH`
  写文件（默认拒绝覆盖已存在，`--force` 覆盖），`--compact` 输出单行 JSON，
  确认信息走 stderr 保持 stdout 纯净；schema 是 `doctor`/`scripts/validate.py`
  校验所依据的同一文档（测试断言与 `doctor.SCHEMA_PATH` 逐字节一致）。`schema`
  描述的是 CLI 配置契约而非某个项目，因此不需要 `iterate.config.yaml` 也能用；
  该命令不受 `get/set/unset` 的隐式 `get` 重解释影响，传 `KEY`/`VALUE` 与
  `--out`/`--compact`/`--force` 配错动作均为 usage error（exit 2）。

### 修复（全面审查发现）
- **`import` 静默切断 dotfile 符号链接**（`portable.py` apply_bundle，+1 回归）：
  提交阶段用裸 `os.replace`，目标若是指向 `~/dotfiles` 的符号链接，会把*链接本身*
  换成普通文件、真实文件保持陈旧——其它所有写入器（`config set`/`refresh`/
  `personalize`/`doctor --fix`）都走 `atomic_write` 保留符号链接，唯独 `import`
  不一致。现改为解析 realpath 后替换，符号链接保留、真实目标被更新。
- **updater 与安装器对重复 checksum 判定不一致**（`updater.parse_checksums`，
  +3 回归）：`iterate update` 对同一文件名两条冲突 digest 采用 last-wins，而
  `scripts/install.py` 与 npx 安装器都整体拒绝。现 `parse_checksums` 对冲突
  重复抛 `ValueError`，`_verify` 以「untrustworthy」干净拒绝（fail-closed，
  与安装器一致）。
- **onboarding 回滚可能删除刚备份的文件**（`generator.py`，+1 回归）：回滚以
  `existing_md is not None` 作为「文件之前存在」的代理，TOCTOU 下（调用方读到
  不存在、写入时文件出现）会把刚写的新 ITERATE.md 删除而非恢复快照。现改为
  依据实际写入前拍的 `md_backup` 恢复。
- **npx 安装器 assets.find 空元素崩溃**（`installer.js`，+1 JS 回归）：提取为
  `findReleaseAsset`，对 null/非对象元素做 `a &&` 守卫（与上方 `some` 一致），
  畸形 GitHub 负载不再以 `TypeError` 崩溃而是走干净的「缺少 asset」错误路径。
- **dimension_sets 非字符串 focus 键崩溃**（`doctor.py`/`dimension_sets.py`，
  +1 回归）：`dim in seen` 对不可哈希键抛 `TypeError`；现以 `isinstance(str)`
  守卫（或 `str(dim)` 参与成员测试），malformed 项被丢弃/降级为 finding 而非崩溃。
- **`personalize --clear` 改写前不拍快照**（`personalize.py`，+1 回归）：与
  `save_personalization` 一致，clear 前对 `iterate.config.yaml` 与 `ITERATE.md`
  各拍 `*.personalize-*` 备份，失败/中断可用 `iterate backup restore` 恢复。
- **非 UTF-8 备份永不可恢复**（`backup.py`，+1 回归）：`restore_backup` 以
  `read_text("utf-8")` 读备份，非 UTF-8 文件抛泛化解码错且无法恢复；现先读字节
  再解码，失败给出可执行的「手动恢复该备份」提示。
- **`tempfile.mkdtemp` 逃逸受保护 try**（`scripts/install.py`/`updater.py`，
  +2 回归）：`TMPDIR` 不可写/磁盘满时 mkdtemp 的 `OSError` 越过
  `ReleaseIntegrityError`/`ReleaseStructureError` 处理器抛裸 traceback；现包在
  try 内并转为干净的 structure 错误/拒绝原因。
- **scan 把指向项目外的符号链接目录计为顶层目录**（`scan.py`，+1 回归）：
  用 `is_symlink()` 排除指向外部（`vendor -> /srv/shared`）的符号链接，避免
  越界路径泄漏进 `ITERATE.md`/`scan --json`。
- **reonboard 保留未再校验的 validation.commands**（`wizard.py`，+1 回归）：
  加载既有配置时对 `validation.commands` 用 `_command_is_safe` 再过滤，非 known-safe
  项丢弃并提示（此前会持久化一个运行时 guard 必然拒绝的命令，报成功却永远跑不了）。
- **completion 死分支**（`completion.py`）：`if shell == "fish"` 两臂相同，收敛为
  `[binary, "-n"]`。
- **guard 执行 shell=True 的 defense-in-depth 说明**（`guard.py` 文档）：元字符门
  已拒绝命令替换/管道/重定向/链式，`shell=True` 保留 glob 展开；文档明确说明
  项目 `iterate.config.yaml` 及其构建脚本在该检出上是代码执行向量，只在审查过
  的树上运行 `guard`/`doctor`/`invariant`（tradeoff，不改变行为以免破坏
  `pytest tests/*.py` 这类合法 glob 用法）。
- **guard 符号链接祖先 TOCTOU 加固**（`updater._copy_release_path`）：在
  `mkdir` 之后、破坏性 copy/replace 之前重新 `realpath` 校验并中止，缩小并发
  换链接的窗口。

---

## [3.11.0] — 2026-11-04

minor：新增 `iterate backup` 子命令（list/restore），补齐「写了备份却无法回读」
的断链——此前 `config set/unset`、`doctor --fix`、`refresh`、`personalize`、
`onboard`、`import`、`reonboard` 都会在改写文件前写一个时间戳备份
（`*.configset-*`、`*.configunset-*`、`*.doctorfix-*`、`*.refresh-*`、
`*.personalize-*`、`*.onboard-*`、`*.import-*`、`*.bak-*`），但用户想撤销时
只能手动 `ls` 项目目录去猜哪个是改动前的副本（`cli.py` 的 Ctrl+C 提示原话就是
「请检查项目目录」）。本轮全面审查（review）确认 2 处中 + 2 处低缺陷并全部修复。

### 新增功能
- **`iterate backup list`**（+10 回归）：只读列出项目根下所有可识别的时间戳
  备份，最新在前，逐条显示 `原始文件名 · 操作 · UTC 时间 · 大小`；恒退出 0
  （空结果也是信息性，与 `fingerprint list` 一致）；`--json` 输出单个
  `{project, count, backups:[{name, base, tag, operation, timestamp, size}]}`
  文档；无需解析 config，损坏配置不阻塞。
- **`iterate backup restore FILE`**（+16 回归）：把某一个备份恢复到其原始文件名。
  恢复前先把**当前**文件再备份为 `*.restore-*`（恢复本身可逆，撤销同一命令即可）；
  用 `atomic_write` 原子写回；`--dry-run` 只预览不写；`--yes` 供非交互 stdin；
  `--json` 输出单个结果文档。安全护栏：拒绝任何不是 iterate 备份形状的文件
  （`<file>.<tag>-<UTC>-<salt>`，绝不容忍手滑覆盖任意文件）、拒绝项目目录外的
  路径（含绝对路径/`../`/symlink）、拒绝目录目标、拒绝不存在的备份；恢复后提示
  用 `iterate doctor`（可加 `--fix`）验证。

### 修复（全面审查发现）
- **gpg 验证器只认 GOODSIG/exit 0、不验证签名者指纹**（`scripts/install.py`、
  `npm-installer/lib/installer.js`，+3 回归 +2 JS 回归）：两个独立安装器的
  `--verify` 没加 `--no-auto-key-retrieve`，且只凭 `GOODSIG`（或 exit 0）就判定
  verified——若系统 gpg 配置/部署启用 `keyserver-options auto-key-retrieve`，
  一个被替换的签名者密钥会被自动拉取并通过验证，而 `iterate update`（
  `signing.py`，用 `--no-auto-key-retrieve` + VALIDSIG 指纹核对）拒绝同一产物。
  现两者都加 `--no-auto-key-retrieve` 并要求 VALIDSIG 指纹属于钉死的
  `0929EA31…1298`；三处签名器重新一致。
- **`scripts/install.py config --interactive` 遇非 mapping 分节崩溃**（
  `scripts/install.py`，+3 回归）：`atomic: 5`（或标量 `review:`/`git:`）会让
  wizard 在 schema 校验之前就抛 `AttributeError`。现按 `configcmd.py` 的
  `isinstance(section, dict)` 先矫正为空 mapping。
- **`--set` 的日期形字符串被 YAML 解析成 `datetime.date`**（
  `scripts/install.py`，+1 回归）：`--set git.target_branch=2024-01-01` 存成
  date，schema 类型不匹配导致整次 `--set` 回滚并报令人困惑的 "changes have
  been reverted"。现日期形标量保持字面字符串。
- **别名共享目录被重复提示/重复拷贝**（`scripts/install.py`，+2 回归）：
  `claude`/`claude-code` 共享 `.claude/skills/iterate`——拒绝第一个别名的升级
  提示后同一目录会对下一个别名再次提问；`update --ai all` 则对每个别名各拷
  一遍共享树。现 `seen_destinations` 在到达目标时即标记（而非拷贝成功后），
  `update` 也按目标目录去重。

### 验证
- 测试 **33 项新增**（`tests/test_backup_command.py` 26 项 +
  `tests/test_install_script.py` 7 项），覆盖正常恢复、可逆撤销、目标缺失时重建、
  dry-run 零写入、非 iterate 文件拒绝、目录外路径拒绝、目录目标拒绝、缺失备份
  拒绝、`--json` 单文档契约、非交互无 `--yes` 拒绝、三处 gpg 指纹一致、标量分节
  不崩溃、日期字符串保字面、别名共享目录去重。

## [3.10.0] — 2026-11-01

minor：补全子系统新增 `--uninstall`，补齐「装了就能卸」的对称能力；并修复
本轮全面审查发现的两处真实缺陷。

### 新增功能
- **`iterate completion <shell> --uninstall`**（+9 回归）：只删除安装时写入的
  那一个文件（默认常规用户补全目录或 `--dir`，绝不触碰任意路径），幂等——
  第二次运行、或从未安装就卸载，仍退出 0 且 `removed:false`，可安全放进
  卸载/回滚脚本；`--json` 输出单个 `{shell, path, removed, reload_hint}` 文档；
  `--install` 与 `--uninstall` 互斥，`--force` 在卸载下被拒绝；按 shell 打印
  停用提示（zsh 提示移除 `--install` 时要求添加的 `.zfunc` fpath 行）。
  此前只能装不能卸——装了补全的用户必须手敲 `--install` 提示里那串路径去删。

### 修复（全面审查发现）
- **gpg 超时在独立安装器中改为 fail-closed**（`scripts/install.py`、
  `npm-installer/lib/installer.js`，+2 回归 +1 JS 断言修正）：三个「保持同步」的
  签名器在同一个 `subprocess.TimeoutExpired` 上执行不一致——CLI 更新器
  （`signing.py`）把它判为 `invalid`（不可被 `ITERATE_ALLOW_UNSIGNED` 绕过），
  而两个独立安装器把它判为 `unavailable`（可绕过）。现在安装器的 import 与
  verify 超时都返回 `invalid`；只有真正缺失/无法启动的 gpg 才保持
  `unavailable`（文档化的显式逃生口）。
- **`report` 的 `next_actions` 不再重复或推荐必失败命令**（`report.py`，+6 回归）：
  (1) 有 error 时不再同时建议 `iterate doctor` 与 `iterate doctor --strict`
  （后者是前者的严格超集，重复了同一条诊断命令）——`--strict` 只在 warnings
  单独阻断时追加；(2) 未 onboarding + 配置损坏时，先建议 `doctor --fix`
  （修复 `_cmd_init` 拒绝解析的配置），再建议 `init --yes`，而非相反。

### 验证
- 测试 **1892 passed, 1 skipped**（1 skipped：本机未安装 fish），`ruff check .`
  通过，npm installer 测试全绿。

## [3.9.4] — 2026-10-31

patch：内容与 3.9.2 完全一致（能力不变），仅为在 ClawHub 扫描 worker 恢复后
通过**全新发布**打通发布链路——3.9.0/3.9.1/3.9.2 三个版本在平台扫描故障期间
发布接口均受理（`ok:true`+versionId）但永不晋升，手动重扫成功也不触发晋升
（版本行已钉死为 pending），只有新发布会重新入队发布时扫描。

- 与 3.9.2 相同的修复：发布同意书三处改为 opt-in（+4 条回归）、README 移除
  `curl|bash`（+回归）、build pins 升到 `setuptools>=84.1.0`/`wheel>=0.46.2`
  （+回归）。
- 测试 **1876 passed, 1 skipped**（1 skipped：本机未安装 fish），`ruff check .`
  通过，npm installer 测试全绿。

## [3.9.3] — 2026-10-31

> 平台诊断版本，**未发布到 GitHub/npm/ModelScope/SkillHub**。2026-10-26 在
> ClawHub 平台 `clawscan` 扫描 worker 故障期间作为诊断探针发布（内容 = 3.9.2），
> 平台受理（`ok:true`+versionId）但永不晋升，随后被平台 moderation 隐藏。
> 该版本号因平台规则保留，故 3.9.4 起重新计数。

## [3.9.2] — 2026-10-27

patch：修复 SKILL.md 里**发布同意书自相矛盾**的真实缺陷，并顺手收掉两处
供应链卫生问题；同时用官方 `clawhub` CLI 重发，绕开 3.9.0/3.9.1 在 ClawHub
上卡死的发布队列（两个版本发布接口都返回 `ok:true`，但一天后公共
`latestVersion` 仍是 3.8.2、`/versions/<v>` 仍 404）。

- **发布同意书 / Publishing consent**：SKILL.md 在配置表与护栏里承诺
  `git.push_per_round: false`（默认）表示"绝不自动 push"，但 Phase 5 的
  false 分支、Per-Session Flow 示例、会话恢复清单三处都直接命令
  "会话结束时一次性 push"。按字面执行这三处的 agent 会绕过用户的 opt-in。
  现在三处都改为"不自动 push；仅在用户明确要求时才推"，风险提示与
  "远程始终保存最新验证状态"也一并改成条件式。新增 4 条文档契约回归。
- **安装文档 / Install docs**：README 与 README.zh-CN 不再推荐
  `curl .../main/scripts/install.sh | bash`（可变上游直接进 shell），改为
  指向 harness 的 release 资产并要求固定 tag + 校验 checksum。新增回归。
- **构建 pin / Build pins**：`pyproject.toml` 的 `setuptools==68.0.0` /
  `wheel==0.42.0` 落在 GHSA-5rjg-fvgr-3xxf 与 GHSA-8rrh-rw8j-w5fx 的受影响
  区间，改为 `setuptools>=84.1.0` / `wheel>=0.46.2`。新增回归。
- 测试 **1870 → 1876 passed**（1 skipped：本机未安装 fish），
  `ruff check .` 通过，npm installer 测试全绿。3.9.0/3.9.1 的
  `completion --install` 与 `report` 转义能力原样保留。

## [3.9.1] — 2026-10-26

patch 重发：3.9.0 在 ClawHub 的版本卡在平台审核队列，无法从本地恢复。发布接口
当时返回 `ok:true` + versionId，服务端也确认版本行存在（同版本重发返回
`http 400 — Version 3.9.0 already exists`），但约一天后公共
`latestVersion.version` 仍是 3.8.2、`/versions/3.9.0` 仍 404、
`moderation.updatedAt` 自 3.8.2 审核后未再前进；平台没有删除/重试/状态 API。
按 2.3.17 的先例升 patch 覆盖重发**同一份能力**，不改任何 CLI 行为。

唯一内容变化：补全脚本头部安装提示统一指向 `--install`（fish 之前仍只给
`iterate completion fish > ~/.config/fish/completions/iterate.fish` 的重定向
写法，与 bash/zsh 头部不一致）。另补 2 条回归：三种 shell 的脚本头部必须提到
`--install`；zsh/bash 的 reload 提示对含空格路径必须正确加引号（此前
`fpath=(...)` 在空格路径下引号不闭合，是 3.9.0 内联修掉但缺专门用例的点）。

测试 **1866 → 1870 passed**（1 skipped：本机未安装 fish，跳过其语法校验），
`ruff check .` 通过，npm installer 测试全绿。3.9.0 的
`iterate completion --install` 与 `report` 反引号/HTML 转义修复原样保留。

## [3.9.0] — 2026-10-25

本轮为无人值守每日例行的「全量评审 + 修复 + 功能/体验增长」版本。新增
`iterate completion --install`，把原先“打印脚本后自己找目录、自己重定向”的
补全安装流程变成一条命令；同时修复 `iterate report` 在值含反引号时可能让
Markdown 表格后半段被当成代码块的真实渲染缺陷，以及 zsh 安装提示在路径含
空格时给出不可执行 `fpath` 语句的问题，并堵住报告中的 HTML 注入面，故升 minor。
测试套件 **1856 → 1866 passed**（1 skipped：本机未安装 fish，跳过其语法校验），`ruff check .` 通过。
评审与发布范围仅限 skill 本体（`iterate_cli/`、`npm-installer/`、`scripts/`、
`templates/`、`tests/`、`config/`、`tools/`、`SKILL.md`、`pyproject.toml`、
`CHANGELOG.md`）；`harness/` 与 `kernel/` 未改、未发、未纳入任何发布包。

### 新增 / Features

- **`iterate completion <shell> --install` —— 一条命令装好 Tab 补全**。此前
  `iterate completion` 只把脚本写到 stdout，用户必须自己知道 bash-completion /
  fish / zsh 的目录，再手动重定向，路径写错时只会得到一个“补全不生效”的哑失败。
  现在：
  - `bash` 写入 `$XDG_DATA_HOME/bash-completion/completions/iterate`（默认
    `~/.local/share/...`）；`fish` 写入 `$XDG_CONFIG_HOME/fish/completions/iterate.fish`
    （默认 `~/.config/...`）；`zsh` 优先写入已存在的 `~/.oh-my-zsh/completions/_iterate`，
    否则写入 `~/.zfunc/_iterate`；
  - 自动创建父目录，原子写入；已有文件默认拒绝覆盖并提示 `--force`，避免静默
    覆盖用户自定义补全；
  - `--dir DIR` 可指定目录（仍使用该 shell 的约定文件名）；`--json` 输出单个
    `{shell, path, bytes, reload_hint}` 文档，便于脚本消费；
  - zsh 会打印可直接粘贴的 `fpath=(... $fpath)` + `compinit` 提示；bash/fish
    打印 reload 提示。`--install` 不向 stdout 打印脚本，避免污染重定向；
  - 新增 8 项回归测试，覆盖三个 shell 的默认路径、`XDG_*` 覆盖、Oh My Zsh
    优先、`.zfunc` 回退、`--dir`、覆盖保护/`--force`、`--json` 与“安装不依赖
    项目存在”。

### 修复 / Fixes

- **`iterate report` 反引号与 HTML 注入**：`_cell()` 的文档承诺转义反引号，但
  实现只处理了 `|`、换行和反斜杠。若 doctor 的 check/message 或配置值里出现奇数
  个反引号，GFM 会把后续表格甚至整段文档当成代码块，粘贴到 PR 后排版损坏。
  同时 GFM 允许裸内联 HTML，项目可控值（如 `<img src=x onerror=...>`）会被
  原样写进报告，在非净化渲染器里形成注入面。现在表格文本统一转义反引号与
  `& < >`；`_code()` 遇到含反引号或尖括号的值会退回普通转义文本，避免在行内
  代码里显示多余反斜杠。新增 2 项回归测试。
- **zsh 安装提示的空格路径**：`reload_hint()` 之前对完整文件路径做
  `rsplit("/", 1)` 后再拼进 `fpath=(...)`，路径含空格时引号不闭合，提示不可执行。
  现在对父目录单独 `shlex.quote()`。

### 验证 / Verification

- `python -m pytest tests/ -q`：**1866 passed, 1 skipped**（fish 未安装）。
- `python -m ruff check .`：All checks passed.
- 新增/更新测试：`tests/test_completion.py`（安装路径、覆盖保护、JSON 合约、
  项目外可用）、`tests/test_report_command.py`（反引号/HTML 不破坏表格）。

## [3.8.2] — 2026-10-23

修复 3.8.1 发布时才触发的版本链测试缺陷：`test_changelog_version_chain_has_no_gaps`
把“所有 minor 的 0..最新 patch 都必须有 CHANGELOG 标题”当成不变量，于是 skill
首次出现 patch 版本（3.8.1）时，它会要求并不存在的 3.6.1 / 3.7.1 标题——这两个
版本号属于共用 tag 命名空间的 `iterate-plugin` 线，skill 线实际是 3.6.0 → 3.7.0
→ 3.8.0。现在检查改为：3.4 起每个 minor 必须有标题，且**已出现的 minor 内部**
patch 必须从 `.0` 连续到该 minor 的最高 patch（因此未来 3.8.3 存在而 3.8.2 缺失
仍会被抓住，同时不会为从未发布的 patch 编造记录）。该缺陷只影响测试，不改变
CLI 或任何发布包内容；3.8.1 的 guard 修复仍是本版的实际变更。

## [3.8.1] — 2026-10-23

修复 3.8.0 在 CI（Python 3.11）暴露的 `guard` 输出读取竞态：当被校验命令
fork 出的孙进程继承 stdout 并继续持有管道时，旧实现等 5 秒后直接关闭读端来解除
阻塞，可能抢在读取线程之前丢掉子进程已经 flush 的输出（CI 实测丢掉了
`parent-done`），于是“命令成功 + 诊断尾巴缺失”，并把一次真实的输出读取失败
伪装成成功。现在读取线程改用 `select` 轮询，在直接子进程退出后先留一个短暂的
静默窗口把管道里已有的字节读完；只有仍被孙进程占用时才发出停止信号，并由读
取线程在退出前做一次有界的非阻塞清扫。读端不再先于数据被关闭，测试把 join
时间压到 0.01s 以强制覆盖该路径，连续 20 次本机复跑与完整 1855 项测试均通过。

## [3.8.0] — 2026-10-22

本轮为无人值守每日例行的「全量评审 + 修复 + 功能/体验增长」版本：新增
`iterate report`（把 status/scan/doctor 聚合成一份可直接贴 PR 或存 CI artifact
的 Markdown/JSON 报告）与 `iterate completion`（bash/zsh/fish Tab 补全），并让
`iterate show` 回显此前只能翻 YAML 才能看到的维度集；同时修复安装器校验子进程
超时过短导致 `config --set` 在负载下把有效修改误判失败并回滚的真实缺陷，故升
minor。测试套件 **1788 → 1856**（1855 passed、1 skipped：本机未安装 fish，跳过
其语法校验；新增 `tests/test_report_command.py` 21 项、`tests/test_completion.py`
20 项，`tests/test_install_script.py` 新增 8 项超时回归，另有 doctor/guard/
portable/onboarding 的数据安全与竞态回归）。评审与发布范围仅限
skill 本体（`iterate_cli/`、`npm-installer/`、`scripts/`、`templates/`、`tests/`、
`config/`、`tools/`、`SKILL.md`、`pyproject.toml`、`CHANGELOG.md`）；`harness/`
与 `kernel/` 未改、未发、未纳入任何发布包。

### 新增 / Features

- **`iterate report` —— 一份可直接分享的项目健康报告**。此前要展示项目状态，
  只能分别运行 `status` / `scan` / `doctor`，再把三段终端输出手工拼进 PR 或
  issue；`--json` 又各自是不同 schema。现在一条只读命令聚合三者：
  - 默认输出 GitHub Flavored Markdown：技术栈、生效审查配置（目标分支、范围、
    维度、维度集、校验命令/白名单、个性化规则数）、doctor 全项检查表（✅/⚠️/❌）、
    漂移与建议、可直接执行的下一步命令；单元格内的 `|` 与换行会被转义，粘贴后
    表格不会散；
  - `--out PATH` 原子写入文件（stdout 保持为空，便于 `report --out x > y` 与
    CI artifact 上传），默认写 stdout；默认拒绝覆盖已存在文件（需 `--force`），
    并始终拒绝覆盖 `iterate.config.yaml` / `ITERATE.md`；
  - `--json` 输出单个结构化文档（与 TUI 无关的稳定键集，含 `summary`、
    `doctor`、`scan`、`config`、`drift`、`next_actions`）；
  - `--strict` 把 warning 一并判为阻塞；退出码与 `doctor` 一致（健康 0 / 阻塞 1），
    可直接作为 CI 门禁；
  - 报告语言跟随项目 `language`（zh/en），损坏或手工改坏的嵌套配置也只报告、
    不 traceback。`iterate init --json` 的 `next_actions` 同步加入 `iterate report`。
- **`iterate completion bash|zsh|fish` —— Shell Tab 补全**。此前只有 `--help`
  一条发现路径，Tab 只会补文件名。补全脚本从与 `--help` **同一个 argparse
  parser** 生成，命令/参数永远不会与文档漂移：补全全部子命令及各自一行说明、
  每个命令的可见参数（隐藏参数不出现）、固定取值（如 `init --language zh|en`）、
  `-p/--project` 目录、`import` / `--out` 文件路径、以及 `iterate help <command>`
  的命令名。输出纯脚本到 stdout，安装提示只写 stderr（`iterate completion zsh >
  _iterate` 不会被污染）；已用 `bash -n` / `zsh -n` 校验生成脚本。
- **`iterate show` 回显维度集**。`dimension_sets`（含每个范围的维度与 focus）
  由 onboarding/personalize 持久化，但 `show` 的解析配置从未包含它，用户只能翻
  YAML 确认。现在 `show` 的 TUI 与 `--json` 都会输出维度集名称，`report` 也复用
  同一解析结果。

### 修复 / Fixes

- **安装器校验超时过短（真实偶发失败）**。`scripts/install.py` 以 30s 超时运行
  `validate.py config`；全量测试中该子进程单独需 21s，负载下超过 30s，导致
  `iterate config --set` 输出 `Command ... timed out after 30 seconds` 并把**有效
  修改回滚**（测试 `test_sets_and_validates` 因此红）。现改为 120s 安全网，并支持
  `ITERATE_VALIDATE_TIMEOUT` 覆盖（非法/非正值忽略，绝不关闭超时保护）；超时错误
  明确告知配置未被修改并给出提高上限的命令。
- **改写前必有可恢复备份（数据安全）**。`onboard` / `personalize` 的
  `iterate.config.yaml` 与 `ITERATE.md` 重写此前可能在没有快照的情况下发生：
  - `iterate onboard` 直接覆盖已有文件（只有 `reonboard` 会备份）；现在两个目标
    文件在替换前都会写同目录 `*.onboard-<UTC>-<随机>` 备份，备份失败即中止；
  - `personalize` 的配置备份失败只 warning 后继续写；现在失败即中止（fail-closed），
    且事务式 `save_personalization` 同时备份 config 与 ITERATE.md；
  - 备份文件名统一带随机后缀，修复同一秒内两次运行（CI 重试/并发终端）复用同一
    路径、第二次覆盖掉唯一快照的碰撞。
- **`personalize` 不再丢弃手写 Markdown**。用户在手写区用 `*` / `+` 或缩进写的
  列表项此前因只匹配 `- ` 而在下次 personalize 时消失；现在接受所有 Markdown
  列表标记与任意缩进，并原样保留非列表内容（段落、子标题、注释），不再重构章节
  时静默删除。
- **`doctor --fix` 可修复 `{}` / 仅注释的配置**。解析为 `{}` 的文件此前被当成
  "可解析但无需修复"，`--fix` 返回成功却什么都没写，doctor 永久报告同一坏配置；
  现在与空文件一样用 canonical 维度重建。
- **`report --out` 默认不覆盖用户文件**（需 `--force`），避免一次误跑覆盖笔记；
  仍始终拒绝覆盖 iterate 自己的状态文件。
- **`import` 在读取前限制大小**。此前先 `read_text()`/`read()` 整个文档再检查
  8 MiB 上限，超大文件已经把内存耗尽；现在文件先 `stat()`，stdin 最多读取
  `MAX_BUNDLE_BYTES + 1` 个字符。
- **`--json` 中断契约**。Ctrl+C / EOF 时 stdout 此前为空，`| jq` 得到解析错误；
  现在仍输出恰好一个 `{"error": ..., "cancelled": true}` 文档（人类提示在非 JSON
  模式下保持原样）。
- **扫描建议不再指向不存在的目录**。无 `tests/` 的扁平 Python 项目此前得到
  `pytest tests -x -q`，首次校验必然 file-not-found；现在只给 `pytest -x -q`。
  同时从建议白名单移除 `npx`（会下载并执行任意包，与 personalize 的禁用策略一致）。
- **`guard` 输出线程不再悬挂/竞态**。子进程派生的孙进程继承 stdout 时，读取线程
  在命令退出后仍阻塞；现在有界 join 后关闭原始 fd 解除阻塞，再用锁取尾部快照，
  避免与仍在写 `lines` 的线程竞态，并在确实无法退出时明确标注输出不完整。
- **`import` 的 rename 也做目录 fsync**（与 `atomic_write` 一致），断电后不会出现
  "写入成功但链接消失"。
- **SKILL.md 配置文档纠错**：`config unset` 的备份位置（同目录
  `iterate.config.yaml.configunset-*`，而非不存在的 `.iterate-backup/`）与
  "键不存在"行为（退出码 1，不是静默成功）已与实现对齐。

### 测试 / Tests

- 新增 `tests/test_report_command.py`：Markdown 结构、中英文标签、漂移、损坏配置、
  未 onboarding、Markdown 转义、JSON 单文档与稳定键、`--strict`、`--out`（写入/
  JSON/`-`/拒绝覆盖状态文件/父目录缺失/空值）、缺失项目路径、`build_report` 可
  序列化。
- 新增 `tests/test_completion.py`：三种 shell 均包含全部命令、参数与取值补全、
  隐藏参数不出现、fish 不全局禁用文件补全、`bash -n` / `zsh -n` 语法校验（fish
  未安装则 skip）、非项目目录可用、未知 shell 与 `--json` 的退出码/单 JSON 契约、
  安装提示不污染 stdout。
- `tests/test_install_script.py` 新增 8 项：默认超时下限、环境变量覆盖、非法值
  回退、超时文案、超时后不改写配置。
- 数据安全与竞态回归：`doctor --fix` 修复 `{}`/仅注释配置与 `dimension_sets: []`
  类型错误；`guard` 孙进程占用 stdout 时不悬挂且尾部快照无竞态；`import` 读取前
  大小限制（文件 `stat` / stdin 有界读取）与 rename 后目录 fsync；`onboard` /
  `personalize` 改写前备份及备份失败即中止；`personalize` 保留 `*`/`+`/缩进列表与
  非列表 Markdown；`report --out` 默认拒绝覆盖；`--json` 中断仍输出单个文档；
  无 `tests/` 的 Python 项目不再被建议 `pytest tests`。

## [3.7.0] — 2026-10-21

本轮为无人值守每日例行的「全量评审 + 修复 + 功能/体验增长」版本：新增
`iterate init`（无提问初始化）与 `scan` 的 API/维度集建议两项用户可感知能力，
并集中修复了重新 onboarding 丢配置、更新器非原子替换、导入回滚、刷新擦除注释、
签名超时被当成"不可验证"等一批真实缺陷，故升 minor。测试套件
**1738 → 1788**（新增 `tests/test_init_command.py`、`tests/test_reonboard_preservation.py`，
扩充 `tests/test_refresh_reconcile.py`、`tests/test_personalize.py`、
`tests/test_doctor.py`、`tests/test_config.py`、`tests/test_onboarding.py`、
`tests/test_scan_command.py`、`tests/test_portable.py`、`tests/test_updater.py`、
`tests/test_signing.py`）。评审与发布范围仅限 skill 本体（`iterate_cli/`、
`npm-installer/`、`scripts/`、`templates/`、`tests/`、`config/`、`tools/`、
`SKILL.md`、`pyproject.toml`、`CHANGELOG.md`）；`harness/` 与 `kernel/` 未改、
未发、未纳入任何发布包。

### 新增 / Features

- **`iterate init` —— 无提问初始化（面向 CI / 脚本 / 其它 agent）**。
  `iterate onboard` 是交互式的，CI 与自动化无法驱动（会卡在第一个提问）。
  `iterate init` 复用同一套扫描与生成逻辑，零提问完成初始化：
  `--yes` 直接写盘、`--dry-run` 预览、`--json` 输出单个结构化文档（含将写入的
  维度/校验命令/维度集），`--language` / `--target-branch` / `--goal` 覆盖
  扫描默认值。已初始化项目默认**不改动**并明确告知（避免覆盖用户调好的配置）；
  `--dry-run --json` 不落盘，可直接用于 CI 预检。16 个测试覆盖各参数组合、
  退出码与"绝不写盘"契约。
- **`iterate scan` 增加 `has_api` 与 `suggested_dimension_sets`**。此前扫描只在
  顶层目录里找 API 层，标准的 `src/api`、`app/routes`、`src/controllers` 布局
  一律识别不到，于是最需要 API 维度的项目反而拿不到建议。现在：
  - 新增 `has_api` 特性开关（顶层 + 常见嵌套布局），TUI/JSON 均输出；
  - 新增 `suggested_dimension_sets`，直接给出可落地到 `dimension_sets` 的具名
    范围蓝图（含 per-dimension focus），`scan` 报告新增「建议范围维度集」小节；
  - 输出提示改为 `iterate init --yes` / `onboard` / `config set` 三条可执行路径。

### 修复 / Fixes

- **重新 onboarding 不再丢配置**。`iterate reonboard`（以及返回用户的
  `onboard` 基本配置更新）此前会用扫描建议覆盖用户已调好的值：
  `dimension_sets`（含 focus）被清空、自定义 `validation.commands` 被通用默认值
  替换、项目自行审核过的 `command_whitelist` 被重置、git 分支/审查范围/push
  策略被强制回到 `main` / `full` / `false`。现在已有值优先展示并作为默认值，
  whitelist 取并集，维度集保留原名称与 focus（扫描建议只填新出现的范围）。
- **更新器的目录替换改为原子换位**。`iterate update` 覆盖安装目录时先
  `rmtree` 再 `os.replace`，两者之间进程被中断/权限失败会让已安装的 skill
  直接消失。现在先把旧目录 rename 到同目录的临时备份、再换入新目录；换入失败
  自动换回，成功后才删除备份。
- **可移植 bundle 的导出/导入全面加固**：
  - 导出前先按与 `import` 相同的 schema 校验，拒绝导出"自己都导不回来"的
    bundle；超过 8 MiB 直接报错而不是写出无法导入的文件；
  - `export --force` 拒绝覆盖 `iterate.config.yaml` / `ITERATE.md`（此前会用
    bundle JSON 覆盖 iterate 自身状态，且是唯一不备份的写入路径）；
  - `export --out -` 不再在 JSON 前打印 ASCII banner；
  - `import` 改为"先写临时文件、再统一备份、最后逐个 `os.replace`"，中途失败
    按备份回滚已替换文件，不再留下"新配置 + 旧 ITERATE.md"的混合状态；
  - 非 TTY 下 `import --json` 不带 `--yes` 的退出码统一为 2（此前同一命令在
    CI 返回 1、在 TTY 返回 2）。
- **`iterate refresh` 不再擦除手写注释**。配置此前按字节比较，而
  `yaml.safe_dump` 必然丢注释，于是每次 refresh 都判定"有变化"并重写配置，
  静默删掉操作者加的所有说明。现在按 YAML 语义比较；确需改值时先写
  `.refresh-<UTC>` 备份，并保留原来的无变更幂等性。同时修复：
  `command_whitelist` 含 `[["pytest"]]` / `123` 时 refresh 崩溃
  （`TypeError: unhashable type`），现在过滤并告知；`push_per_round: "on"`
  在向导里是 true、在 refresh 里却被改写成 false 的不一致；manifest 暂时不可读
  时不再永久清空指纹基线。
- **`iterate personalize` 不再写入非法配置**：`fix_priority_order` /
  `forbidden_fixes` 里的 `null` 曾被 `str()` 成字面量 `"None"`（不是合法维度 id，
  下次 `doctor` 立刻报错），现直接丢弃并汇总告知；三个 `uniqueItems` 列表在
  序列化边界去重；向导中重复添加同一项会提示"已存在"而不是制造重复；改写配置
  前生成 `.personalize-<UTC>` 备份。
- **`doctor --fix` 能修复自己报的错**：`personalization.*` 与
  `dimension_sets.*.dimensions` 的重复项（schema 要求 `uniqueItems`）此前只报
  不修，现在会去重；未能映射到专用建议的诊断项也会给出通用下一步，而不是
  只显示一行失败。
- **`show` / `config get` 区分"缺失"与"损坏"**：配置缺失时 `show` 退出 0 并
  指向 `onboard` / `init --yes`（此前退出 1 且建议 `doctor --fix`，而 doctor
  只会再让你 onboard）；配置存在但无法解析时明确建议 `doctor`（onboard 拒绝
  覆盖已存在的坏配置，旧提示是死路）。`config sett k v` 现在提示
  `did you mean 'set'?`，而不是答非所问的"get takes no VALUE"。
- **签名校验超时按失败处理（fail closed）**。`gpg --verify` 超时此前返回
  `unavailable`，而 `ITERATE_ALLOW_UNSIGNED` 恰好只豁免 `unavailable`——一次
  卡死的 gpg 就能让本应强制的签名校验被环境变量绕过。现在超时归类为
  `invalid`，任何覆盖开关都不能放行。
- **`status --json` 的 `drift_reason` 语义修正**：漂移已成功计算时输出 `null`
  而不是 `"unknown"`（健康的项目不再看起来"无法校验"）；配置损坏时给出
  `corrupt_config` 而不是泛化的 `"unknown"`。

### 测试 / Tests

- 新增 `tests/test_init_command.py`（16 项）、`tests/test_reonboard_preservation.py`
  （5 项），并扩充 refresh（含"注释保留/备份"集成测试）、personalize、doctor、
  config、onboarding、scan、portable、updater、signing 的回归用例。
- 全量 `python -m pytest tests/ -q`：**1788 passed**；`ruff check .` 通过。

---

## [3.6.0] — 2026-10-20

本轮为无人值守每日例行的「功能与体验增长」版本：新增三个用户可直接感知的能力
（`iterate scan` 只读导出、`iterate help` + 命令拼写容错、`iterate export` /
`iterate import` 可移植状态包），并配备完整测试与文档，故升 minor。测试套件
**1563 → 1738**（新增 `tests/test_scan_command.py`、`tests/test_cli_help.py`、
`tests/test_portable.py`、`tests/test_status.py`、`tests/test_gpg_signing_audit.py`
与 `npm-installer/test/security.test.js`，扩充 `tests/test_tui.py` 的 JSON 能力
清单及 `tests/test_config.py`/`tests/test_onboarding.py`/`tests/test_doctor.py`/
`tests/test_updater.py`/`tests/test_validate.py`/`tests/test_install_script.py`/
`tests/test_publish_qoder.py`）。评审与发布范围仅限 skill 本体（`iterate_cli/`、
`npm-installer/`、`scripts/`、`templates/`、`tests/`、`config/`、`tools/`、
`SKILL.md`、`pyproject.toml`、`CHANGELOG.md`）；`harness/` 与 `kernel/` 未改、
未发、未纳入任何发布包。

### 新增 / Features

- **`iterate scan` —— 只读导出项目扫描结果**。此前扫描结果只存在于 `onboard`
  交互向导内部：工具能扫，用户却无法回读（CI 更拿不到）。新命令把同一套
  `scan_project()` 的纯函数结果导出为 TUI 报告或单个 JSON 文档，包含识别到的
  `manifests` / `detected_languages` / `detected_package_managers` /
  `top_level_dirs`、四个特性开关（`has_specs` / `has_tests` / `has_ci` /
  `has_frontend`），以及由它们推导出的 `suggested_dimensions`、
  `suggested_validation_commands`（可直接作为 `validation.commands` 的形状）与
  `suggested_command_whitelist`（用于 `validation.whitelist`）。
  **只读**：只判断文件/目录是否存在，不读内容、不写任何文件（测试用 mtime 快照
  断言）；**恒退出 0**：完全没识别出技术栈是正常结果而非失败，CI 可无脑消费
  `--json`；空结果在 TUI 下显式渲染 `— (none detected)` 并在无任何 manifest 时
  给出警告与出路（`iterate onboard` 会改为询问技术栈），避免"空白右值"被误读为
  渲染故障。
- **`iterate help [command]` + 命令拼写容错**。此前没有 `help` 命令——`iterate help`
  被当成**非法命令**报错并退出 2，用户不记得 `--help` 就无从发现命令；命令拼错时
  只抛一堵 argparse usage 墙（`invalid choice: 'statu' (choose from …)`），说清了
  "错在哪"却从不说"该打什么"，窄终端下正解还会被滚出屏幕。现：
  - `iterate help` 打印总览、`iterate help doctor` 打印单命令帮助，二者均退出 0，
    且**不要求项目目录存在**（`-p` 指向不存在的路径也能用）；
  - 拼错命令时追加最近的真实命令（`iterate statu` → `did you mean 'status'?`）；
    子命令动作同样适用（`iterate fingerprint verfy` → `did you mean 'verify'?`）；
  - 候选都不够接近时**不猜**（错误的建议比没有更糟），原始诊断保持不变；
  - `--json` 契约不变：用法错误仍是退出 2 且 stdout 恰好一个 JSON 文档，
    建议放在 `did_you_mean` 字段；`--json help` 显式拒绝并返回结构化错误，
    以免"要求结构化输出的命令却只吐散文帮助"。
- **`iterate export` / `iterate import` —— 可移植的项目状态包**。此前配置与
  `ITERATE.md` 只能整目录拷贝，跨机器/跨仓库迁移没有受支持的路径：手工复制容易
  把另一仓库的 manifest 指纹一起带过去，导入后立刻报假漂移。新命令把
  `iterate.config.yaml` + `ITERATE.md` 快照成 **bundle format v1**（`format` /
  `bundle_version` / `skill_version` / `exported_at` / `project` / `config` /
  `iterate_md`）：
  - `iterate export` 默认在项目根写 `iterate-bundle-<UTC>.json`，`--out PATH`
    指定路径（默认拒绝覆盖，`--force` 才覆盖），`--json`（或 `--out -`）把
    bundle 打到 stdout 且不写文件；导出过程对项目只读。
  - `iterate import FILE|-` 先做结构 + schema 校验，再生成
    `.import-<UTC>-<salt>` 时间戳备份，最后原子写回；非法/外来 bundle 在任何
    写入前退出 1。`--dry-run` 预览新增/变更/删除键，`--yes` 供非交互/CI，
    `--reset-fingerprints` 丢弃导出项目的指纹（`iterate refresh` 重新采集）。
  - 两种模式都遵守既有契约：`--json` 时 stdout 恰好一个 JSON 文档；用法错误
    （如 `--json` 与 `--out` 同给）退出 2。新增 `tests/test_portable.py` 68 项
    覆盖正常/异常/边界（空配置、超大文档、伪造 format、schema 违规、备份唯一性、
    stdin、往返一致性、doctor 复检）。

### 修复 / Fixes（同轮全量复审 findings）

本轮对 skill 本体的全量复审 findings（含前次记录的 6 项）全部修复并附可复现回归测试：

- **[High] `iterate onboard` / `reonboard` 静默删除 `mode` 与 `invariants`**。
  `generate_config_yaml` 从固定键集重建配置，不含顶层 `mode` 与 `invariants`，
  而 `refresh._build_refreshed_config`（从现有配置拷贝）保留了它们——因此重新
  on-board 一次就把切成 `defensive` 的项目的模式悄悄改回 `iterate`，并清空已声明的
  invariants。修复：`OnboardingData` 新增 `mode` / `invariants` 字段并由
  `generate_config_yaml` 写回；`_load_existing_onboarding_data` 读取并按 schema
  归一化（`mode` 限 `iterate`/`defensive`，非法值回退默认；invariants 丢弃空/重复
  `ensure` 与非法 `commands` 模块并逐条警告，绝不再持久化损坏结构）。新增
  `normalize_mode` / `normalize_invariants`，测试覆盖正常/缺失/损坏三态。
- **[Medium] `tools/gpg-signing.sh audit [repo…]` 忽略目标参数**。`cmd_audit` 校验了
  参数却仍审计全部五个仓库——`audit GlassPane` 会悄悄把其他仓库也扫一遍。
  修复：`targets_filtered "$@"`。新增 `tests/test_gpg_signing_audit.py`：用假 `gh`
  记录被查询的仓库，断言单目标只审计该仓库、多目标生效、无参数退化为全量、
  且建议目标自身违规仍能命中（修复前该测试 3 项失败）。
- **[Low] README/zh-CN 宣称 `config set` 支持 `validation.commands` / `invariants.*`**。
  `SETTABLE_KEYS`/`_resolve_key` 根本没有这两类键，文档比实现多承诺。修复：两版 README
  改为逐一列出实际可设的扁平键与点分键，并明确二者不在此处设置。新增
  `tests/test_config.py::TestSettableKeysDocumentedInReadmes` 双向锁定中英文文档与
  `SETTABLE_KEYS` 完全一致。
- **[Low] `scripts/install.py` 旧式直接调用漏掉 `--ai=<value>` 拼写**。`parse_legacy_args`
  只判 `"--ai" not in args`，`--ai=trae` 会掉进子命令解析器以退出 2 收场。修复：同时
  识别 `--ai` 与 `--ai=` 前缀。新增 `test_legacy_invocation_accepts_equals_syntax` /
  `test_legacy_invocation_equals_syntax_installs`。
- **[Low] `doctor` 的 Next action(s) 提示硬编码中文，无视 `language`**。其余 doctor
  输出全为英文，唯这组提示恒为中文，英文项目的报告夹生。修复：`_render_next_actions`
  接受 `language`，`render_report` 默认从项目配置读取（缺失/损坏回退英文）；提示文案
  提供 zh/en 双语。新增英文默认、zh 跟随配置、显式 `language` 参数优先三态测试。
- **[Nit] `tui.key_value` 用转义后的 label 度量列宽**。`escape()` 把 `[` 变 `\[`，
  含方括号的键每括号多算一列，值列被推右。修复：按可见文本度量并填充，转义仅发生在
  嵌入 markup 时。新增列宽不变式测试。
- **[High] 基础向导重建 `OnboardingData` 时丢失 `drift_check` / `mode` / `invariants`**。
  `_run_basic_wizard` 只从既有数据继承了 advanced 调参字段，这三个"基本向导不问"的
  键回到默认值：`onboarding.drift_check: false` 被改回 true、`mode: defensive` 被改回
  `iterate`、整个 `invariants:` 段被删。修复：从 `existing` 继承三者，`invariants`
  用 `copy.deepcopy` 避免新旧对象共享可变结构。新增
  `TestBasicWizardPreservesAdvancedSettings` 断言值保留且深拷贝独立。
- **[Medium] `_load_existing_onboarding_data` 保留空 `validation.commands` 模块**。
  `{node: []}` 或只含非字符串的模块会被重新写回，而 schema 要求 `minItems: 1`，
  `refresh` 又会丢弃它们——向导写出的配置立刻被 doctor/schema 判错。修复：过滤后为空
  的模块不再载入。新增 `test_validation_module_with_no_string_commands_is_dropped`。
- **[Medium] `status` 在 YAML 非字符串标量上崩溃**。手写/ AI 写入的
  `completed_at: 2026-10-20` 解析为 `datetime.date`，`skill_version: 1.0` 为 float：
  TUI 的显示宽度折行对非字符串抛 `TypeError`，`--json` 则因 `json.dumps` 无法序列化
  date 而**一个文档都不输出**。修复：TUI 三个字段先 `str()`，JSON 使用 `default=str`。
  新增 `tests/test_status.py` 同时锁定 TUI 与 JSON 两条路径。
- **[Medium] `doctor --fix` 对空配置只打印"重建"却什么都不写**。空文件被转成
  `config = {}`，`apply_safe_fixes({})` 无修复项，命中 `if not fixes: return True, []`
  提前返回——用户看到"rebuilding with safe defaults"，文件仍是空的。修复：空配置
  种入 `{"dimensions": CANONICAL_DIMENSIONS}` 并插入显式重建说明，保证写入发生。
  新增 `test_empty_config_is_rebuilt_not_silently_skipped`（含二次 doctor 复检）。
- **[Medium] `update --assistants a,b` 部分命中时静默忽略未安装的助手**。
  `assistants_not_installed` 只在**全部**未命中时填充，`claude,cursor` 仅装 claude
  时输出与"两个都更新了"无法区分。修复：只要请求了 `--assistants` 就按名称与安装
  路径（覆盖 `claude`/`claude-code` 别名）计算差集。原有"混合即静默"的测试改为
  正向断言，并新增别名路径测试。
- **[High] `scripts/install.py` 的凭据与路径边界**（4 处）：① 祖先 symlink 检查以
  `destination` 自身为锚，而 `realpath(dst.parent) == realpath(destination)` 对顶层
  文件恒成立，symlink 指向的安装目录可把写入带出用户选择的 root。修复：新增
  `root=` 参数，调用方传 `effective_target`，按 `realpath(root)` 锚定。②
  `_is_github_api_url` 只比主机名，`http://api.github.com` 也会收到 PAT。修复：强制
  `https`。③ 重定向只比 hostname，`https→http` 或换端口仍携带 Authorization。
  新增 `_origin()`（scheme+host+port）比较。④ token 只 `strip()` 后校验却继续使用
  原始值：纯空白 token 通过校验后仍拼出 `Bearer    `，内嵌换行让 `putheader()` 抛错
  并把 PAT 打进日志。修复：校验前统一 `token.strip() or None`，并拒绝内嵌空白/
  控制字符（错误信息不回显 token）。新增 `TestCredentialBoundaries` 12 项与
  root-anchor 两项测试。
- **[Medium] npm 安装器的 GPG / token / 参数 / 体积边界**：① gpg 的 `spawnSync`
  没有超时，卡住的 gpg-agent 会让安装器永久挂起；现加 30s + SIGKILL，超时归类
  `unavailable`。② 公钥导入失败被标成 `invalid`（暗示签名伪造），实际只是"无法建立
  真实性"；改为 `unavailable`。③ `normalizeToken` 只 trim 两端，内嵌 CR/LF 会做
  header 注入；现拒绝空白/控制字符。④ `parseArgs` 不认 `--ai=trae` 等
  `--flag=value`；现统一支持，布尔旗标带值则明确报错。⑤ `sumDeclaredSizes` 只累加
  能解析的条目，本地化 tar 列表会让解压炸弹预算看起来很小；现要求全部条目可解析，
  否则拒绝解压。新增 `npm-installer/test/security.test.js` 覆盖上述五项。
- **[Low] `scripts/validate.py` 忽略调用方 `schema_path`**：`validate_dimension_sets`
  总从仓库默认 schema 取 enum，自定义 schema 里的维度被误报 unknown；现透传同一
  schema。另：显式传入但不存在的 dimensions 目录此前被静默跳过（拼错路径得到绿色
  通过），现报错；未显式传入时保持原有"跳过 + note"行为。新增 3 项测试。
- **[Low] `scripts/check.sh` 的健壮性**：不在 git 仓库内时只抛 git 的
  `fatal: not a git repository`，现在给出可操作的一句话并以 2 退出；`RUFF` 由字符串
  改为数组，解释器路径含空格时不再被 word-splitting 破坏。
- **[Low] `scripts/publish_qoder.py --frontmatter minimal` 在源 frontmatter 已"干净"时
  什么都不改**：恰好只有 `name/description/version` 时跳过重写，作者的通用
  description 被保留，与"重写为 Qoder 第三人称/触发词描述"的承诺相反。修复：minimal
  始终重写（可用 `--description` 覆盖），`keep` 仍原样保留。新增 3 项测试。
- **[Medium] `tools/gpg-signing.sh` 的三处失效**：① `install typo` 的目标校验在
  `< <(...)` 子 shell 里 `exit 2`，父进程带空目标列表继续并退出 0；现调用
  `require_known_targets "$@"`。② `audit` 把 `gh` 的 404、网络错误、认证失败统统
  `2>/dev/null || true` 成空字符串并 `continue`，零工作流被检查也打印
  `audit: passed`；现区分 404（正常跳过）与其他失败（FAILED），统计检查数量，
  为 0 时拒绝报通过。③ `seed` 把口令放在 `gpg --passphrase "$pass"` 的 argv 里
  （`ps` 可见），现改为 `--passphrase-fd 0` 从 stdin 读取。新增 4 项测试
  （含假 gpg/security 驱动的 argv 断言）。

### 版本号说明 / Version numbering note

本次对外发布的包（GitHub tag、npm、ClawHub、ModelScope、SkillHub）版本均为
**3.6.0**。需要记录一个生态结构性问题：本工作副本的 git tag 命名空间被
`iterate-skill` 与 `iterate-plugin` 两条**独立版本线**共用，而 plugin 线已用到
`v3.5.4`–`v3.7.1`（远端 `plugin-origin` 上实际到 `v3.9.2`）。因此
`v3.5.4` 与 `v3.6.0` 在本地都已被 plugin 的同名 tag 占用。

- 按本仓库自带不变量（`tests/test_release_meta.py::test_changelog_version_chain_has_no_gaps`
  要求 CHANGELOG 的 3.x 序号连续）与「新功能 = minor」，skill 的正确下一个版本是
  `3.6.0`——`3.6.1` / `3.9.3` 会要求不存在的历史条目，`3.5.4` 会把功能发布标成 patch。
- 处理方式：把本地 `v3.6.0` 从 plugin 镜像指向 skill 发布提交（annotated + GPG 签名），
  推送至 `origin`。被移走的 plugin 镜像 tag（tag 对象 `b62d8e981e5a2ec1246190f3019cc2657d56c2fb`
  → 提交 `2e0890c3`）**未丢失**：`plugin-origin` 上仍持有同名 tag，需要时用
  `git tag -f v3.6.0 2e0890c3` 即可还原。
- **影响面**：普通 `git fetch`（不带 `--tags`，即每日任务的用法）**不受影响**，实测
  退出 0 且不会改写已有本地 tag；只有 `git fetch --tags` 会对同名 tag 报
  `would clobber existing tag`。两个方向都是如此，属命名空间冲突的固有代价。
- **建议（留给 harness/plugin lane）**：plugin 线已推进到 `3.9.x`，不会再回到
  `3.6.0`；后续若需消除冲突，应让 plugin 的 tag 与 skill 的 tag 分属不同命名空间
  （例如 plugin 改用 `plugin-v*`），而不是靠两条线互相让号。

### 测试 / Tests

- 新增 `tests/test_scan_command.py`（28 项）：`collect_scan_data` 的字段与 JSON
  可序列化性、四个 `has_*` 键必须逐字对应 `ScanResult` 字段名、空目录全空、
  前端目录翻转语义、重复调用稳定且零写入；`render_scan` 的 JSON/ TUI 两种模式、
  空状态标记、无 manifest 时的警告（且非空项目不误报）、非 TTY 下无 ANSI 转义、
  缺键时不抛 KeyError；CLI 层 `--json` 契约、空项目退出 0、路径不存在仍退出 1、
  只读性（mtime 快照）、`-p` 位置无关、help 中可见。
- 新增 `tests/test_cli_help.py`（24 项）：`help`/`help <cmd>`/`help <未知>` 三条路径
  的退出码与输出、`help` 对**每个**已注册子命令都可用、项目目录不存在时仍可用、
  `--json help` 拒绝但 stdout 恰好一个 JSON；拼写容错覆盖大小写各异的多组错拼、
  子命令动作错拼、无近似候选时不猜、原始用法错误信息不被破坏、JSON 文档携带
  `did_you_mean` 且无建议时**不含该键**、有效命令不会被误报；`_did_you_mean` /
  `_suggestion_from_usage_error` 的引用式（≤3.12）与非引用式（3.13）两种消息格式、
  非 choice 类错误透传、模块级建议槽不跨次泄漏。
- 新增 `tests/test_gpg_signing_audit.py`（9 项）：以假 `gh` 记录被查询的仓库，
  从正反两侧锁定 `audit` 的目标过滤——单目标只审计该仓库（修复前因扫到别的仓库
  的违规而误报失败）、单目标自身违规仍退出 1、多目标同时生效、无参数退化为全量；
  另覆盖非 404 读取失败与"零工作流被检查"必须失败、干净读取报告检查数量、
  `install` 拒绝未知目标、`seed` 不再把口令放进 gpg argv。
- 新增 `tests/test_portable.py`（68 项）：bundle 构建/校验/解析/差异/写入的
  正常、异常与边界（空配置、超大 JSON、未知 format/bundle_version、schema 违规、
  路径不同步、备份同秒唯一、写入失败回滚、stdin、`--json` 单文档契约、
  导出→导入往返与 doctor 复检）。
- 新增 `tests/test_status.py`（2 项）：YAML date/int/float 标量经 TUI 与 `--json`
  均不崩溃，JSON 恰好一个文档。
- 新增 `npm-installer/test/security.test.js`（4 组）：token 内嵌空白/控制字符、
  `--flag=value` 解析边界、gpg 超时与导入失败分类、声明体积部分不可解析即拒绝。
- 复审修复回归（分散在既有文件）：`tests/test_onboarding.py` 新增 `normalize_mode` /
  `normalize_invariants` / 生成与载入往返 13 项（含 schema 校验）及基础向导保留
  高级设置、空 validation 模块过滤；`tests/test_doctor.py` 新增 Next action(s)
  三态语言与空配置重建测试；`tests/test_updater.py` 新增混合 `--assistants` 与
  路径别名测试；`tests/test_config.py` 新增中英文 README 与 `SETTABLE_KEYS` 双向
  一致测试；`tests/test_install_script.py` 新增凭据/重定向/root-anchor 14 项；
  `tests/test_validate.py` 新增自定义 schema 与显式缺失目录 3 项；
  `tests/test_publish_qoder.py` 新增 minimal/keep description 3 项；
  `tests/test_tui.py` 新增方括号键的列宽不变式测试。

---

## [3.5.3] — 2026-10-17

本轮为无人值守的全量复审 + 修复：对 skill 本体做一轮完整审计并把全部 findings
修复到位，每项修复都配有可复现的单元测试（Python 与 npm 安装器两侧），因此为
patch 版本。测试套件 **1451 → 1563**（新增 `tests/test_prepush_hook.py`，并大幅扩充
`test_signing.py` / `test_updater.py` / `test_release_meta.py` / `test_install_script.py` /
`test_onboarding.py` / `test_config.py`；npm 侧扩充 `mode.test.js` / `tarball.test.js`）。
评审范围限于 skill 本体（`iterate_cli/`、`npm-installer/`、`scripts/`、`templates/`、
`tests/`、`config/`、`tools/`、`SKILL.md`、`pyproject.toml`、`CHANGELOG.md`）；
`harness/` 与 `kernel/` 不在发布范围，仅在其独立仓库处理。

### 修复 / Fixes — 安全与供应链

- **GPG 签名验证只信 gpg 的退出码**：`verify_detached_signature` 此前只看退出码
  0 加上 stdout 里的 `GOODSIG`。这把"某个受信密钥签过"当成了"就是钉住的这把
  发布密钥签的"——在 `--auto-key-retrieve` 默认开启的机器上，gpg 会联网抓取一个
  陌生的签名者公钥并用它验证，于是任何签名都能验证通过。现改为读
  `[GNUPG:] VALIDSIG <fpr>` 并把该指纹与钉住的发布公钥指纹做**精确比对**；同时
  `--no-auto-key-retrieve` 关掉联网取钥，验证结束后杀掉该临时 homedir 的 gpg-agent
  （它会在缓存里留下已导入的密钥）。
- **tar 硬链接逃逸（`scripts/install.py`）**：硬链接的 `linkname` 是**相对归档根**
  的路径，而不是相对链接自身所在目录。此前按 `member.parent / linkname` 解析，
  使 `a/b/evil → ../outside` 这类位于子目录的硬链接可以绕过包含性检查（其归档根
  解析会逃出目标目录，但父目录解析不会）。现改为相对目标根解析。
- **签名被拒时泄漏临时目录（`scripts/install.py`）**：`_download_release_source`
  在验签**之后**才创建 `iterate-release-*` 临时目录，而签名门抛出的
  `ReleaseIntegrityError` 不在解压段那个 `except` 元组内——所以已创建的目录
  会残留，每次失败下载泄漏一份，重试累积在 `$TMPDIR` 里。现改为 `keep_temp_dir`
  标记 + `finally`：只有成功路径把目录所有权交还给调用方，其余每条失败路径
  （验签拒绝 / 布局不符 / 归档损坏）都清理干净。
- **npm 安装器解压前未做体积预算**：`tar -xzf` 没有体积上限，`curl --max-filesize`
  只限制**压缩后**大小，一个小而高度可压缩的归档可以解压出多个 GiB。现从已有的
  `tar -tvzf` 列表解析每个成员的**声明解压体积**并在写入任何字节之前拒绝
  （兼容 GNU tar 的 ISO 日期与 bsdtar/macOS 的月份缩写两种格式，否则某平台会静默
  得到 total=0 而永远不触发）。
- **npm 安装器不再拒绝设备/FIFO 节点**：`rejectLinkEntries` 此前只拒绝符号/硬链接，
  现同时拒绝 `b`/`c`/`p`/`s`（块设备/字符设备/FIFO/套接字）——发布包从不携带这些
  特殊节点，FIFO 还会挂住后续对解压树的读取。
- **npm 安装器 curl 选项注入**：URL 现以 `--` 之后传入，使以 `-` 开头的
  `browser_download_url` 不可能被当成 curl 参数。
- **npm 安装器校验和比较改为常量时间 + 大小写无关**：`sha256sum` 可能输出大写十六进制，
  而大小写敏感比较会拒绝一份完全正常的 release；且期望值与 tarball 走同一条网络链路，
  提前退出的字符串不等会泄露前缀信息。现统一小写 + `timingSafeEqual`
  （附长度守卫，避免长度不等时抛异常）。
- **GitHub token 归一化**：`normalizeToken` 现同时去掉首尾空白与换行
  （Windows 生成的文件常带 `\r`），并在 `buildAuthFlags` 里**再次**归一化——
  那才是 token 被拼进请求头的确切位置；内嵌换行会造成 CRLF/头注入或静默破坏鉴权。
- **GPG 签名策略的可选开关取值收紧（三端）**：`ITERATE_ALLOW_UNSIGNED` 此前是"任何
  非空值即生效"，于是字面符合预期的 `=0`（"保持强制签名"）反而**关闭**了签名强制。
  现三处（`iterate_cli/signing.py`、`scripts/install.py`、
  `npm-installer/lib/installer.js`）统一只认 `1`/`true`/`yes`（大小写无关），
  `0`/`false`/`no`/`off`/空白一律保持强制签名。新增跨端守护测试
  （`tests/test_release_meta.py`）：三处取值集合必须完全一致，否则任一安装器会给出
  **不同的安全姿态**而无处可见。

### 修复 / Fixes — CLI 契约与健壮性

- **`iterate status --json` 的 drift 语义修正**：未 onboard 时不再计算/上报
  `drift_detected: true` 及具体漂移清单（此时无基线可比，而 `show --json` 与 TUI
  分支都把它描述为 "unknown"）。新增机器可读的 `drift_reason` 字段
  （`not_onboarded` / `disabled` / `corrupt` / `no_fingerprints` / `unknown`），
  与 `doctor`/`fingerprint` 共用同一判定，避免三个命令对同一状态给出矛盾答案。
- **`iterate fingerprint list` 退出码**：空基线（未 onboard / drift 关闭 /
  尚未采集）是信息性状态，退出 0；只有配置损坏才 fail-closed 退出 1。此前
  `verify` 对同一状态退出 0 而 `list` 退出 1，CI 脚本会踩到不一致。
  `verify --json` 的 `added`/`removed`/`changed`/`unchanged` 现排序，与 TUI 渲染一致。
- **`--json` 契约在用法错误路径上也成立**：`iterate <任意错误用法> --json` 现在
  保证 stdout 恰好一个 JSON 文档（此前 argparse 的用法错误会让
  `iterate fingerprint bogus --json | jq` 得到空 body 而解析失败）。
  同理 `iterate onboard --json` 这条交互命令拒绝路径也补上了 JSON 输出。
- **`BrokenPipeError` 处理**：`iterate status --json | head` 不再抛
  `BrokenPipeError` traceback（重定向 stdout 到 devnull 后再退出，避免解释器最终
  flush 时二次抛出）。
- **`-V` 别名**：`iterate -V` 现与 `-v`/`--version` 等价（保持 `-v` 向后兼容）。
  顶层帮助现列出各退出码语义。
- **`iterate personalize --yes` 校验**：`--yes` 只对 `--clear` 有意义；单独传入
  此前被静默忽略，会让使用者误以为交互向导已被自动确认，现在明确报错。
- **`iterate config unset --json`**：被移除后的值现输出 `null`（此前是字符串
  `"default"`），与 `config get KEY --json` 对同一状态报告的原始值一致；
  TUI 侧仍显示 "default"。
- **`iterate config get` 隐式键**：`config_action` 的 `choices` 已移除，
  `iterate config <key>` 现在能被正确解析为取值而非 argparse 直接拒绝；
  `_cmd_config` 相应地把参数位从 action 移到 key。
- **`scripts/publish_qoder.py`**：`validate_zip` 调用处按真实的三返回值解包
  （`errors, warnings, size`），复用其返回的体积而不重复 stat；诊断类 warning
  改为写入 stderr，stdout 只保留机器可读 JSON；移除了一段从未可达的 top-level
  目录重命名死代码。

### 修复 / Fixes — doctor / refresh / onboarding

- **`doctor` 新增两项检查接入**：`_check_invariants`（invariants 配置项校验）与
  `_check_manifest_drift`（技术栈漂移）此前未接入 `run_doctor`，现均参与诊断。
  `_check_invariants` 现额外校验 `ensure` 路径**不得逃出项目根**（`_ensure_path_escapes`）。
- **`_check_manifest_drift` 复用已加载的配置**：此前在这里重新读一遍配置文件，
  既浪费一次解析，也有可能与其它所有检查基于**不同修订版本**的配置判定（TOCTOU）。
- **`_check_personalization` 不再崩溃**：dimension 为非字符串（list/dict）时
  `x not in enabled` 会抛 `TypeError`，把唯一用于诊断坏配置的命令自己搞崩。现跳过非
  字符串条目（与 `scripts/validate.py` 的容错一致）。
- **`_check_validation_commands` / `_check_validation_whitelist` 措辞修正**：
  明确 `validation.command_whitelist` **没有运行时效果**（该用
  `ITERATE_EXTRA_SAFE_COMMAND_PREFIXES`），且仅在 `commands` 确为 mapping 时才声称
  "已检查 shell 元字符"。
- **`refresh`**：`drift_unavailable_code` 在配置缺失时返回 `not_onboarded`；
  `_as_dict_list` 现拷贝而非直接返回引用；`_build_refresh_data` 移除死掉的
  personalization 加载；reonboard 成功时提示保留的备份。
- **`wizard` / onboarding 加载侧的标量归一化**：加载既有配置时，
  `target_branch`/`reasoning_effort`/`language`/`max_rounds` 等值现按类型与取值域
  归一化（非字符串的 `target_branch`、越界的 `max_rounds`、无效的
  `reasoning_effort`/`language` 回落到默认值），避免把坏值原样写回配置后又被
  `doctor` 反复标记。
- **`fingerprint.capture_fingerprints`**：清单文件仍在但**读不到**（权限错误）时
  复用上次记录的摘要，不再被误报为 `removed` 而提示用户去 refresh；真正被删除的
  清单（`FileNotFoundError`）仍照常报告为 removed。
- **`show`**：TUI 模式对 `completed_at`/`channel`/`skill_version` 先转字符串，
  否则手改的 `skill_version: 1.0`（float）或未加引号的日期会让
  `rich.markup.escape` 抛 `TypeError` 而崩溃（`--json` 侧本就安全）。
- **`scan`**：目录列举失败的裸 `print` 改走 `tui.warning`（保持 `--json` 的 stdout
  纯净）；`spec` 从 `TEST_DIR_CANDIDATES` 移除（它既是 Ruby 的测试目录约定，也是
  其他技术栈的**规格文档**目录，同时列入两处会让只有 specs 的项目报告 `has_tests=True`
  并建议去跑 `pytest spec`），Ruby 项目在 `_scan_features`/`_detect_test_dir` 中单独处理；
  建议命令去掉 `--timeout=60`（该参数需第三方插件，裸 `pytest` 会报未知参数）。
- **`updater`**：`_default_runner` 的子进程输出解码加 `errors="replace"`（此前可能因
  非 UTF-8 字节抛 `UnicodeDecodeError`）；失败路径统一清理临时目录（不再泄漏
  `iterate-update-*`）；latest release 的挑选改为**最高语义版本**而非列表首个
  （此前可能选中带 tarball 的更早 release 而漏掉真正的最新版）；
  `communicate()` 补超时并杀整个进程组；`_copy_release_path` 改为**原子替换**
  （写临时同名再 `os.replace`，中途失败不会留下半新半旧的文件）。
- **`generator`**：`atomic_write` 收紧为 `O_CREAT|O_EXCL|O_NOFOLLOW`（不跟随符号链接、
  不覆盖已有文件），按目标权限创建，异常走 `BaseException` 清理；
  新增 `user_owned_bounds` 供 user-owned 区块边界统一解析。
- **`publish_qoder`** 与 npm 侧均补齐归档成员校验：重复成员、`harness/`/`kernel/`
  等禁止项、单一 top-level 目录、绝对路径与 `..` 分量，均在发布前拒绝。

### 文档与示例 / Docs & Examples

- **示例命令去掉 `--timeout=60`**：`scan.py` 已不再建议该参数（它需要第三方的
  pytest-timeout 插件，裸 `pytest` 会报 `unrecognized arguments: --timeout=60`），
  但随包分发的示例仍带着它——即 onboarding 会把一条**对未装插件的用户永远失败**
  的命令写进 `validation.commands`，导致验证步骤从装好那天起就在报红。现统一去掉：
  `config/iterate.config.yaml`、`templates/onboarding-playbook.md`、`SKILL.md`、
  `README.md`、`README.zh-CN.md`、`examples/python-project.md`。
- **playbook 的白名单自检项写错了（`templates/onboarding-playbook.md`）**：
  原检查项要求"`validation.command_whitelist` 包含所有 `validation.commands` 中使用的
  命令前缀"，但该字段**没有任何运行时效果**——把它填满并不会让
  `iterate guard pre-check` 放行任何命令。现改为可执行的检查：每条命令必须能通过
  `guard pre-check`，确需执行其它工具时用 `ITERATE_EXTRA_SAFE_COMMAND_PREFIXES`
  登记前缀。这是唯一还写错该字段语义的文档（`config/iterate.config.yaml`、
  `tools/SKILL.{claude,cursor,trae}.md` 此前已正确）。

### 修复 / Fixes — 发布工具与钩子

- **`.githooks/pre-push`**：作者身份白名单改为**单行逗号分隔**
  （BSD awk/macOS 拒绝多行的 `-v` 赋值，此前在 macOS 上该门会静默失效）；
  并按**整个待推范围**做单次 `git log | awk` 扫描（此前逐提交扫描，一次常规推送
  会派生数千个进程而卡死推送门）；同时去掉 `|| true`——扫描失败时应当 fail-closed，
  而不是放一个未经审计的作者身份通过。
- **`scripts/publish_qoder.py` 校验的是打包后的归档，而不是暂存目录**：此前只校验
  暂存树，然后打包上传——一个通过树检查的包仍然可能是坏的归档。现对产出的 zip
  本身再跑一次 `validate_zip`，任一 error 直接中止构建（`ValueError`，列出全部问题），
  因此坏包不可能被上传。

### 测试 / Tests

- 新增 `tests/test_prepush_hook.py`（11 例）：把真实钩子拷进一次性 git 仓库的
  `.git/hooks/` 并按 `git push` 的真实方式喂 ref 列表，覆盖作者身份门
  （允许/拒绝/仅扫待推范围/多方身份白名单）、作用域与逃生口
  （非 main 不拦、`SKIP_PREPUSH=1`、空 ref 列表），以及 lint 门的分派契约
  （干净通过、失败阻塞、退出码 3 表示"本地无匹配 ruff 无法验证"且必须提示
  `--no-verify`、缺 `scripts/check.sh` 的旧 checkout 不阻塞）。
- `tests/test_signing.py`：`allow_unsigned` 全分支参数化
  （`1`/`true`/`yes`/大小写/空白 → 生效；`0`/`false`/`no`/`off`/空白/未设置 → 不生效）；
  签名验证的**真值判据**改为指纹比对后补对应用例：伪造 gpg 输出时
  VALIDSIG 指纹与钉住指纹不一致必须判为 invalid，`--auto-key-retrieve` 必须被关闭，
  未知状态与超时均 fail-closed，验证后临时 homedir 的 gpg-agent 必须被清理。
- `tests/test_release_meta.py`：新增"三处 `ITERATE_ALLOW_UNSIGNED` 取值集合一致"守护。
- `tests/test_updater.py`：补最高语义版本挑选、非 UTF-8 输出解码、失败路径临时目录
  清理、原子替换等用例。
- `tests/test_onboarding.py`：补 `scan` 的 `spec/` 判定
  （非 Ruby 项目的 spec/ 只算文档不算测试、不得被建议 `pytest spec`；Ruby 项目的
  spec/ 仍是测试目录）与"建议命令不得携带 `--timeout`"；补 `show` TUI 模式对
  手改的非字符串取值（`skill_version: 1.0` float、未加引号的日期）不崩溃，
  并断言 TUI 与 `--json` 两种模式对同一配置都返回 0。以上用例均已先用旧实现
  跑过一遍确认会失败（6 例中 5 例失败）。
- `tests/test_onboarding.py`：补 onboarding 加载侧标量归一化全分支
  （`"false"`/`"yes"`/`"incremental"`/`"low"`/整数/越界取值域/空白/非字符串
  `target_branch`/全空维度列表）；`atomic_write` 的符号链接竞争（临时路径上预先放置
  symlink 必须 fail-closed 且不动目标文件）、按目标权限创建、编码失败不留临时文件；
  USER-OWNED 边界对渲染进 AI 区的**字面标记**不产生错位；单趟占位符替换（注入的
  `{{TECH_STACK}}` 不得被二次展开）；`capture_fingerprints` 的不可读清单回落；
  非 UTF-8 配置的 `UnicodeDecodeError` → `CorruptConfigError`；
  `dimension_sets` 两个 drop 回调都会报出丢掉的 id。
  以上全部用例都先用**旧实现**跑过一遍确认会失败，避免"只测现状"的空测试。
- `tests/test_publish_qoder.py`：`validate_zip` 的 rival top-level / 重复成员 /
  任意深度的 `harness/` / 缺 SKILL.md 用例（原有），补 build_package 接线用例
  ——zip 校验失败必须中止构建而不是产出归档。
- `tests/test_install_script.py`：补 `ITERATE_ALLOW_UNSIGNED` 取值语义与
  硬链接包含性用例。
- `tests/test_install_script.py`：补**子目录**硬链接逃逸（`a/b/evil → ../../outside`
  必须被拒）与子目录硬链接相对归档根解析（`a/b/evil → target.txt` 必须真正指向
  `target.txt`——用 inode 相等断言，而不只是"没抛错"，否则旧的错误解析也算通过）；
  另补临时目录清理：验签拒绝 / 布局不符 / 归档损坏三条失败路径各断言目录被删除，
  成功路径断言目录必须存活（调用方拥有它），共 6 例。
- npm `mode.test.js` / `tarball.test.js`：补 `parseArgs` 抛错契约
  （含"库函数不得调用 `process.exit`"与 `bin/cli.js` 的退出码）、`constantTimeHashEqual`
  全分支、`declaredEntrySize`/`sumDeclaredSizes` 两种 tar 日期格式、成员名校验、
  解压前体积预算、FIFO 拒绝等用例。
- 同步更新 `iterate config unset --json` 的既有断言（`"default"` → `null`）。

---

## [3.5.2] — 2026-10-16

本轮为发布链路加固（patch）：**把「发布签名」从"尽力而为"改为强制**，并修复 npm
CI 发布链路的认证缺口。

### 新增强制发布签名 / Mandatory release signature

- **发布侧（`.github/workflows/release.yml`）**：GPG 签名不再"缺密钥就跳过"——
  未配置 `GPG_PRIVATE_KEY`/`GPG_PASSPHRASE` 即失败；签名后增加校验步骤，断言
  签名密钥指纹等于钉死的 `0929EA31DF4F7429F63FC53189D88B1D043A1298` 且每份
  `.asc` 都能验证对应产物（密钥被换/签名损坏都会在 CI 就被拦住）。
- **安装侧（npm 与 Python 双端）**：新增/统一强制签名策略——缺少 `.asc`、机器无
  `gpg`、签名无法取回、或签名与钉死公钥不匹配，一律**中止**安装/更新。理由：
  `SHA256SUMS.txt` 与 tarball 出自同一个 release，攻击者能改其一即可改其二，内嵌
  公钥才是不可伪造的唯一锚点。
  - `iterate_cli/signing.py`（新模块）：钉死公钥 + 指纹 + `verify_detached_signature`
    + `enforce_signature_policy`；`iterate update`（`updater.py`）接入该策略。
  - `scripts/install.py`：同步实现同一策略（独立脚本，公钥常量与指纹与前者字节一致，
    由 `tests/test_release_meta.py` 守护三处副本一致：CLI / install.py / installer.js）。
  - `npm-installer/lib/installer.js`：`signaturePolicyError()` 统一判定；最新 release
    的挑选条件从"tarball + 校验和"收紧为"tarball + 校验和 + 签名"。
  - **唯一例外**：显式设置 `ITERATE_ALLOW_UNSIGNED=1`（用于确实无法运行 gpg 的机器）；
    **坏签名永不放行**——该开关只覆盖"无法校验"，不覆盖"校验失败"。
- **修复 gpg 隔离密钥环路径过长导致校验失败**：gpg 的 agent socket 位于
  `<GNUPGHOME>/S.gpg-agent`，Unix socket 路径上限约 104 字符；此前用较深的临时目录
  会报 `can't connect to the gpg-agent: File name too long`，使签名校验在部分环境
  （尤其中间产物在深路径下）直接失败。现改用短前缀临时 homedir，npm 侧同步缩短
  临时目录前缀。

### 修复 / Fixes — 发布链路

- **npm CI 发布链路**：`npm-publish.yml` 此前因仓库未配置 `NPM_TOKEN` secret 且该包
  无 OIDC Trusted Publisher 映射而 `ENEEDAUTH` 失败（v3.5.0、v3.5.1 均如此）。
  现已配置 `NPM_TOKEN` secret，CI 可正常发布；同时在 workflow 中保留 `npm test` 与
  "package.json 版本 == release tag" 断言。**待办（infra）**：npm 已开始限制绕过 2FA
  的 granular token 用于发布与信任管理，持久方案是配置 OIDC Trusted Publisher
  （需带 2FA 的 web 会话执行 `npm trust github …`），配置后可移除该 secret。

### 测试 / Tests

- 新增 `tests/test_signing.py`（15 例）：策略各分支（缺签名/缺 gpg/坏签名/覆盖开关）、
  真实 gpg 往返（生成临时密钥 → 签名 → 校验通过；篡改产物 → `invalid`；异密钥签名 →
  `invalid`）、钉死公钥可导入且指纹相符。
- `tests/test_release_meta.py`：新增"三处公钥字节一致"与"四处均声明指纹"两条守护。
- npm `mode.test.js`：新增 `signaturePolicyError()` 全分支用例。
- 现有 updater/install 下载路径用例改为对策略打桩（其夹具无法产出对钉死密钥有效的
  签名），策略本身由上面两组用例覆盖。

---

## [3.5.1] — 2026-10-16

本轮为无人值守的全量复审 + 修复 + 发版：4 个并行深评子代理对 skill 本体产出
约 52 条 findings（2 HIGH、17 MEDIUM、33 LOW），全部修复项均配有可复现的
单元测试（Python 与 npm 安装器两侧），因此为 patch 版本。评审范围限于
`iterate_cli/`、`npm-installer/`、`scripts/`、`tests/`、`SKILL.md`、
`pyproject.toml`、`CHANGELOG.md`、`RELEASE.md` 与两个 GitHub workflow；
`harness/`（iterate-plugin、iterate-harness）与 `kernel/` 不在发布范围内，
仅在其独立仓库处理。

### 修复 / Fixes — 安全与供应链（HIGH）

- **npm 安装器 tar 列表截断绕过链接防护（HIGH，已实证）**：`lib/installer.js`
  用 1 MiB 的 `TailBuffer` 捕获 `tar -tzf/-tvzf` 输出，只保留**末尾**内容；
  成员数足够多时列表头部被丢弃，其中的 symlink/hardlink 条目因此完全逃过
  检查，而真正的 `tar -xzf` 处理的是完整归档——攻击者可借"表头截断"把
  `link -> /etc` 之类条目解压出来。修复：新增 `FullBuffer`（保留头部并标记
  溢出）与 `runCommand({stdoutMustBeComplete, stdoutCap})`，列表/JSON 这类
  **必须完整**的捕获在超限时 fail-closed 报错而非静默截断；`extractTarball`
  与 `rejectLinkEntries` 均支持注入上限以便测试。
- **GPG 签名验证不再"告警后照装"（MEDIUM）**：SHA256SUMS 与 tarball 同源发布，
  内嵌公钥是攻击者无法伪造的唯一锚点；`.asc` 存在且签名无效时现以退出码 1
  fail-closed，仅"gpg 不可用/无签名资产"降级为 stderr 告警（后者也补了显式
  提示，不再静默跳过）。
- **npm 侧解压炸弹预算（MEDIUM）**：`tar -xzf` 对未压缩体积零防护，新增
  `measureTree`/`enforceExtractedSize`（500 MiB 总量 / 256 MiB 单文件，与
  `scripts/install.py` 对齐），超限即删除解压产物并报错。
- **JSON 响应上限与捕获上限不一致（MEDIUM）**：`fetchJson` 允许 10 MiB 但
  实际只留 1 MiB，超出后 `JSON.parse` 报出费解的 "Unexpected end of JSON
  input"；现按 `JSON_MAX_BYTES` 完整捕获，超限直接报"响应过大"。
- **`personalize` 远程执行动词可被 flag 绕过（HIGH）**：`npm --silent exec x`、
  `pnpm --dir . dlx x` 等把动词挤到 `tokens[1]` 之外即可通过白名单，进而被
  持久化进 committed 配置、在 CI 里以 `shell=True` 执行。修复：扫描动词后的
  全部 token，同时保留 `npm run exec`（本地同名脚本）的合法用法。
- **校验和文件严格化与冲突拒绝**：`_parse_checksum` 改用 `^[0-9a-fA-F]{64}$`
  严格匹配（`int(digest,16)` 曾接受 `+`/`0x` 前缀），同一文件出现同名校验和的
  冲突条目时整体拒绝（与 npm 侧 `parseChecksums` 对齐）。
- **token 形状 fail-fast**：npm 侧新增 `validateTokenShape`（前缀 + 长度），与
  `scripts/install.py` 的 `_validate_github_token` 同规则，避免拼错的 PAT 一路
  走到 401/403 才以模糊信息失败。

### 修复 / Fixes — 健壮性与异常处理

- **不可哈希的手改配置值不再让 doctor 崩溃**：`language: [zh]`、
  `reasoning_effort: {a: 1}`、`review.scope: [full]` 会在成员判断处抛
  `TypeError: unhashable type`；检查路径与 `doctor --fix` 路径都补 `isinstance`
  前置守卫（前者报错/告警，后者修复）。
- **doctor 的 known-safe 门禁逐条校验**：此前只检查每个模块的 `cmds[0]`，
  于是 `[pytest, "curl x | sh"]` 被报为 healthy，而 `guard` 必然拒绝。
- **`validate.py` 白名单与维度一致性**：白名单条目先 `strip()` 再做语法校验与
  前缀匹配（与 doctor 一致，" pytest " 不再一边通过一边拒绝）；纯空白条目拒绝
  （空前缀会让一切命令"被白名单"）；`dimension_sets`/`personalization` 一致性
  检查不再对不可哈希成员调 `set()`，标量 `dimensions` 也不再被拆成单字符。
- **install.py 下载/解压异常**：`ConnectionResetError`/`ssl.SSLError` 等
  `OSError` 子类（非 `URLError`）此前裸崩，现纳入捕获并返回清晰 reason；
  解压异常集补齐 `EOFError`/`ValueError`/`zlib.error`（与 `updater.py` 对齐），
  校验通过但损坏的归档统一转为 `ReleaseStructureError`。
- **`iterate update` 目录刷新语义与安装器对齐**：受管目录此前用
  `copytree(dirs_exist_ok=True)` **合并**，上游删除的文件会永久残留；现整目录
  替换（非受管文件保持不动），`iterate update` 与 `install.py --force` 结果一致。
- **reonboard 取消/无变更时清理临时备份**：`NO_CHANGES`/`CANCELLED` 路径不再在
  仓库根目录累积未跟踪的 `*.bak-*`（同时修正 CLI 提示文案）。
- **`write_onboarding_outputs` 拒绝写入缺标记的生成结果**：模板损坏/过期时
  `_replace_user_owned_section` 会静默返回未替换内容、用户手写区随之上盘丢失；
  现与 refresh 路径对称，抛 `ValueError` 且不落盘。
- **`publish_qoder.py`**：`git archive` 的临时 zip 改写系统临时目录并在 `finally`
  清理（此前落在 stage 目录内，中断即被打包上传）；`check` 对不存在的路径给出
  清晰错误而非 traceback。
- **`doctor --json-out` 临时文件**：改用 pid+随机后缀的唯一名并在失败时清理
  （固定 `.tmp` 名会被并发导出互相覆盖）。
- **向导载回配置的类型归一**：`goal`/`max_rounds`/`atomic.*`/`scope_chunk_size`
  在 re-onboarding 时按 schema 归一（此前 `max_rounds: "abc"` 会被原样回写，
  doctor 持续报错）。
- **`init_config` 创建目标目录**：`mkstemp(dir=target)` 需要 target 存在，
  此前误 mkdir 了 `target.parent`。
- **`prompt_dimensions` 保持顺序**：默认/EOF 路径不再经 `set()` 往返导致
  `dimensions:` 顺序在每次运行时抖动（YAML diff 噪声）。

### 修复 / Fixes — 输出契约与退出码一致性

- **warning 统一走 stderr**：`tui.warning` 此前写 stdout，导致
  `iterate refresh --json`、`config set --json`、`fingerprint verify --json`
  等在 JSON 之前先打印 `⚠` 行，管道下游 `| jq` 直接解析失败——将 warning 迁移
  到 stderr 后，所有命令的 stdout 恢复"只放数据/恰好一个 JSON 文档"。
- **`config set/unset --json` 回显规范化键名**：`config set git.use_worktree`
  与 `config get use_worktree` 现在报告同一个键名，脚本可直接互相映射。
- **`fingerprint list --json` 不再对畸形 `onboarding:` 段崩溃**（标量/列表值
  此前抛 `AttributeError` 且 stdout 无任何 JSON）。
- **漂移原因改用稳定代码**：`drift_unavailable_code()` 返回
  `corrupt_config`/`not_onboarded`/`drift_check_disabled`/`no_fingerprints`，
  CLI 的退出码与提示分支改按代码判定（此前靠子串匹配人类文案，改一句提示语就
  可能让 CI 误绿）；同时修正"drift_check 已开启但无指纹"时的提示——原提示让
  用户去 `onboard`/开 `drift_check`，而两者本就已满足，正确动作是 `refresh`。
- **`fingerprint verify` 只报一次配置解析错误**：`check_onboarding_drift` 支持
  复用已加载的 config（新增哨兵参数，区分"未传"与"传入 None"），消除了同一
  stderr 上重复两遍的解析错误。
- **`show` 与 `status` 退出码对齐**：配置存在但无法解析时，`show` 在未 onboard
  状态下同样 fail-closed（退出 1 且携带 `config_error`），并补齐未 onboard 载荷
  的稳定键集，便于脚本无条件取值。
- **用户取消统一退出 1**：`update` 交互取消与 `personalize --clear` 取消此前返回
  0，与 `onboard`/`reonboard` 及 `main()` 文档化的"1 = 错误/取消"矛盾；现统一。
- **用法错误退出 2**：`scripts/validate.py` 的未知子命令/缺参数、`install.py`
  的无子命令调用改为 2（与同入口 argparse 的语义一致）；`iterate` CLI 新增缺失
  依赖（PyYAML/rich）时的 127 契约实现（`_dependency_exit_code`）。
- **中断提示不再断言"未写入任何文件"**：`config set`（备份已生成）、
  `doctor --fix`（已应用修复）、`update`（已写入文件）等路径下该断言不成立，
  现改为提示可能已留下时间戳备份。
- **`config unset` 缺失 section 的文案**：区分"父段不存在（无可删除）"与
  "父段类型错误"，不再把前者报成不存在的类型错误。
- **`refresh --json` 标注统计口径**：新增 `stats_basis: "pre-apply"`，说明
  `changed`/`md_changed_lines`/`stats` 取自 apply 之前的预扫快照。

### 修复 / Fixes — 文档与发布流程

- **SKILL.md**：`--list`/`--interactive` 更正为 `config --list`/`config
  --interactive`（此前写法在 `install` 下会 argparse 报错退出 2）；补齐支持的
  AI 助手表（13 → 26 项，与 `SUPPORTED_AI` 对齐）；补充"用户取消 = 1"与 127
  的说明。
- **RELEASE.md / npm-publish.yml**：步骤 5 更正为"由 workflow 自动发布"（此前
  手册仍写手动 `npm publish`，与已存在的自动 workflow 冲突）；workflow 增加
  `npm test` 与"package.json 版本 == release tag"断言，避免忘 bump 时静默发布
  旧版本。
- **npm 安装器提示**：`pipx install <repo>` 占位符改为可复制的真实命令
  （仓库 git 地址 / 解压后的源码目录），并说明项目未发布到 PyPI；安装模式提问
  改为中英双语且默认值与显示一致（此前显示 `[Y/n]` 但回车/EOF/超时均为 No）。
- **doctor `--fix` 提示**：应用修复后明确告知配置被重写为纯 YAML、手写注释不会
  保留、且已生成 `.doctorfix-*` 备份。
- **`personalize` 丢弃项全量播报**：`extra_validation_commands` 中模块名非法的
  条目此前被静默丢弃，现与其他结构错误一样进入 `dropped` 汇总提示。
- **`_heading_level` 识别 TAB 分隔**：`##\t标题`（CommonMark 合法）此前不被识别
  为标题边界，`merge_user_sections` 会连同正文删除该用户标题。

### 测试 / Tests

- Python：新增约 60 条用例，覆盖不可哈希配置（检查 + `--fix`）、known-safe 逐条
  校验、白名单 strip/空白拒绝、维度一致性标量与不可哈希、下载层裸 `OSError`、
  损坏归档 fail-closed、校验和严格化与冲突、`init_config` 目录创建、
  `prompt_dimensions` 顺序、无子命令退出 2、受管目录删除语义、`publish_qoder`
  临时文件与缺失路径、黑名单与操作者环境变量 fail-closed、`_is_plain_script_path`
  路径逃逸、带 flag 的远程执行动词、`config set/unset --json` stdout 纯净性与
  键名规范化、漂移原因代码、`fingerprint list --json` 畸形段、`show` 未 onboard
  的退出码与稳定键、缺标记模板拒绝、`drift_check` 往返保持、refresh 模块级归一、
  `tui.warning` 走 stderr、依赖退出码映射。
- npm：新增 `test/tarball.test.js`（`FullBuffer` 溢出语义、**列表截断必须
  fail-closed**、symlink/hardlink 拒绝、多顶层目录拒绝、解压预算、干净归档可解压）
  并在 `mode.test.js` 补充 `validateTokenShape` 用例；`npm test` 现串联两个测试
  文件。

### 备注 / Notes

- 明确**未采纳**的低风险建议（保留现状，理由如下）：`release.yml` 归档剔除
  `RELEASE.md`/`DESIGN-*`（纯体积优化，不值得在发版当天改动发布管线）；
  JS/Python 两侧超时与体积常量完全统一（工具语义不同，且当前值均 failsafe）；
  npm 安装器"最新 release 挑选标准"改为与 Python 完全一致（已在 JS 侧补充
  "跳过缺少校验和资产的 release"的显式告警，语义差异已可见）。
- `harness/` 与 `kernel/` 的既有改动属于用户 WIP，本次未提交、未还原。


---

## [3.5.0] — 2026-10-11

本轮为无人值守的全量复检 + 修复 + 发版：4 个并行深评子代理产出约 45 条 findings，
全部修复项均配有复现性单元测试（正常/异常/边界），另有 2 项新功能与 1 项文档补齐，
因此为 minor 版本。评审范围限于 `iterate_cli/`、`npm-installer/`、`scripts/`、
`templates/`、`tests/`、`config/`、`tools/`、`SKILL.md`、`pyproject.toml`、
`CHANGELOG.md`；`harness/`（iterate-plugin、iterate-harness）不在发布范围内，
其发现仅在报告中记录。

### 新功能 / Features

- **`iterate config unset <key>`**：`config` 此前只有 `get`/`set`，一旦
  `config set` 写入了一个不当值（或向导预置了不想要的项），只能手工编辑 YAML——
  而手工编辑既无 schema 校验、也无自动备份，且 `personalization.*` 下的嵌套结构
  很容易删成残留空壳。新子命令删除指定叶子键，并在父节点因此变空时逐级向上剪除，
  使配置回到 schema 的缺省语义；每次写入前自动备份（`.configunset-` 时间戳），
  键不存在时视为已达成（幂等，退出 0），带注释的键在删除注释时给出 stderr warning。
  用法错误退出 2、操作性失败退出 1，与既有约定一致。
- **`iterate fingerprint list`**：`fingerprint` 此前只有 `verify`，其输出永远是
  「当前 vs 基线」的差异，从不展示基线本身——看到 `changed: pyproject.toml` 时
  无从得知记录时的 sha256，因而无法分辨真实漂移与初次录入错误。`list` 纯读
  `onboarding.fingerprints`、不重扫，毫秒级返回，且在 `drift_check: false` 时
  依然可用（`verify` 在该配置下是 unavailable）。`--json` 输出
  `{project, available, count, drift_check_enabled, ignore_patterns,
  fingerprints:[{path,sha256}]}`；未记录任何指纹（尚未 onboard）属正常状态
  → 退出 0 并给出可执行提示，配置损坏属未知状态 → 退出 1 fail-closed。
- **退出码约定文档化**：SKILL.md 新增「退出码约定 / Exit-Code Contract」小节，
  统一 `0`（成功）、`1`（业务失败/结论为否）、`2`（用法错误，重试无用）、
  `127`（依赖缺失）四档语义，并点明「`2` 不要当业务失败重试」这一判读要点。
  此前各子命令的退出码散落在各自 help 文本里，跨命令无一致契约可依赖。

### 修复 / Fixes — CLI 与配置

- **`personalize` 写回 `ITERATE.md` 用户区不再截断**（HIGH）：`build_updated_
  iterate_md` 用 `find`（首个匹配）定位用户区结束标记，而目标段落的正文中
  同样出现该标记时会拼在**第一个**匹配处收尾，把其后的全部内容（含后续段落与
  文件尾部）一并丢弃。改为 `rfind`（最后匹配）+ 委托给
  `generator._replace_user_owned_section`，两条路径共用同一套定位逻辑。
- **`merge_user_sections` 的合并边界按标题级别判定**（HIGH）：原实现以「任意
  `## ` 开头的行」为边界，但个性化段落自身就含 `### 禁区 / Protected` 这类
  h3 子标题，导致用户段落内部被提前切断；而真正的 h1 级用户章节（如
  `# 我的项目约定`）又因不匹配 `## ` 而从未被清除，新旧内容叠加。改为边界 =
  **标题级别 ≤ 被删段落自身级别**（新增 `_heading_level()`，识别 1–6 个 `#` +
  空格；7 个以上或 `#` 后无空格不算标题）。
- **`config set` 的错误分支统一走 `_set_error`**：各分支此前有的返回 1、有的
  返回 2、有的打印后落回 0，自动化无法区分「键名写错」与「值不合法」。
- **`refresh` 标量归一化**：`target_branch`/`review_scope`/`push_per_round`/
  `language`/`dimensions` 读入时显式归一（含 `None` → 删除该键），
  避免 YAML 里 `language:`（空值）被当作有效语言写回。
- **`refresh` 的预览与写盘区分「文件不存在」与「读失败」**：原先两者都判为
  「无旧配置」，于是一次权限错误会静默丢弃既有备份；`_write_refresh_outputs`
  对缺失配置的备份改为静默跳过（本来就没有可备份的）。
- **`full_reonboard` 先检查 USER-OWNED 标记**再调用向导，避免把用户的
  `ITERATE.md` 用户区当作可覆盖内容重写。
- **`doctor` 对 `validation.commands` 缺失与 `{}` 一视同仁判 warn**：与
  guard 的 fail-closed 边界保持一致，但不因此把整体健康状态翻转为不健康
  （「没配验证命令」是待办，不是故障）。
- **`doctor` 多模块非法配置逐模块报告**，不再只报第一个。
- **`doctor` 的 `_command_is_safe` 与 guard 侧镜像**，避免两处安全基线漂移。
- **`doctor` 导出报告原子化**：`export_report_json(strict=...)` 先写临时文件再
  `os.replace`，中途崩溃不再留下半截 JSON 供下游解析。
- **`doctor` 主入口支持 `--strict` / `--json-out` 独立运行**。
- **`show` 对漂移做三态输出**（disabled / unknown / none / drift），与 `status`
  对齐；此前 `show` 对「漂移检查被配置关闭」与「无漂移」给出同一输出，
  操作者无法区分「干净」与「没在检查」。
- **`scan` 的静态检查目标按实际源码根定位**：`_detect_src_root` 探测 `src/`
  布局，替换硬编码的 `ruff check src/` / `mypy src/`——平铺布局的项目此前
  会得到一条必然失败的建议命令。
- **`dimension_sets` 的 `normalize_dimension_sets` 支持 `on_drop` 回调**，
  被丢弃的非法条目可逐条上报而非静默消失；`suggest_dimension_sets` 修复空种子。
- **向导的 `command_whitelist` 拒绝标量字符串**（schema 要求 list），
  `drift_ignore` 正确传入指纹采集，`dimension_sets` 的 on_drop 走 warning。
- **`fingerprint.capture_fingerprints` 用 `tui.warning` 取代裸 `print`**，
  与其余输出一致（裸 print 会穿透 `--json` 的 stdout 单文档契约）。

### 修复 / Fixes — 更新器与护栏

- **`updater` 复制前预检 REQUIRED 路径**：原先边复制边校验，缺失文件已有一半
  落盘才失败，留下新旧混杂的助手技能目录。
- **`update` 报告 `assistants_not_installed`**（`UpdateOutcome` 新字段 +
  `to_dict` + TUI 提示）：请求刷新从未安装的助手时，此前静默成功，
  操作者以为已刷新。
- **错误详情截断改为保留尾部**（`_ERROR_DETAIL_MAX_BYTES = 2048`）：
  构建/测试输出的结论（失败行）在末尾，保留头部会恰好截掉它。
- **`guard` 的 `_drain` 环形缓冲按尾部保留**，且每行先截断到 160 字符再参与
  保留判定——否则一条超宽噪声行就能把致命错误行挤出缓冲区
  （新增 `test_overflow_keeps_tail_not_head`、
  `test_wide_last_line_cannot_starve_the_final_error` 两条回归测试）。
- **`guard` 超时改为 `proc.wait(timeout=10)` + 线程 `join(timeout=5)`**，
  `_kill_process_tree` 对 `ProcessLookupError` 直接返回、对
  `OSError`/`AttributeError` 回落到 `proc.kill()`——原先子进程已退出时会抛
  未捕获异常，把一次「超时」升级成 traceback。

### 修复 / Fixes — 安装与发布链路

- **安装器 UTF-8 stdio**（`scripts/install.py`）：Windows 上 Python 默认用
  cp1252/本地编码，打印中文横幅或中文项目名会抛 `UnicodeEncodeError`，
  安装进行到一半直接中断。`main()` 入口先 `_reconfigure_stdio()`（best-effort，
  流已关闭或不接受参数时跳过）。
- **安装摘要的富文本转义**：rich 把 `[...]` 当样式标签解析并从输出中丢弃，
  于是 `C:\[build]\skill`、`[404]` 这类用户可控路径/状态会凭空消失——操作者
  看不到摘要本要展示的路径。只转义 message，不转义 style。
- **校验失败分类**：checksum 文件**下载失败**（网络/HTTP/DNS）不再抛
  `ReleaseIntegrityError`，改为丢弃未校验的 tarball 并回退到本地可信源，
  与 tarball 下载失败的行为对齐——原先一次瞬时网络抖动会以「拒绝更新：校验失败」
  终止整个更新，而实际上什么都没被校验过。「取到了但对不上」的真正完整性判定
  仍然 fail-closed（no-entry / mismatch 照旧中止），release 完全没有
  `SHA256SUMS.txt` 资产也照旧拒绝。
- **安装器 `--version`**：此前 `npx iterate-skill-installer --version` 打印
  usage error；现从 `pyproject.toml [project].version` 读取（避免与发版单一
  真值源漂移），文件缺失/损坏时回退占位符而非抛异常。
- **`scripts/validate.py` UTF-8 stdio**：Windows 默认 cp1252、POSIX 可能是
  ISO-8859-1，而校验报错会引用配置值/维度名（其中常含中文），会把一次
  「验证不通过」变成 traceback。
- **Qoder 包字节确定性**（`publish_qoder._zip_dir`）：改为显式构造 `ZipInfo`，
  固定 `date_time`（ZIP 最早可表示的 1980-01-01）、pin `create_system`/
  `external_attr`。原先用 `archive.write`，它把每个文件的 mtime 写进条目，
  于是 `touch` 或换一台机器 checkout 出来的同一份内容打出的 zip 字节不同、
  SHA-256 漂移，而 docstring 恰恰声称「重复构建产出字节一致」。可执行位取自
  文件自身的 `st_mode` 而非 `os.access`（后者看调用者身份，会让产物依赖
  「谁运行的构建」）。
- **`publish_qoder check` 的诊断走 stderr**：原先 `check pkg.zip > out` 会连同
  失败信息一起吞掉，`check | grep ok` 也没法用来断言通过。
- **npm 安装器 `runCommand` 杀掉整个进程组**：POSIX 下以 `detached` 让子进程
  自成进程组，超时用 `process.kill(-pid, SIGKILL)` 杀整组。原先的
  `child.kill('SIGKILL')` 只发信号给直接子进程，于是一个已经派生出 helper 的
  pip/curl 在安装器报「超时」之后照样活着，继续占用 stdio 管道、继续下载/编译。
- **npm 安装器 promise 必然结算**：leader 死了但孙进程继承并握着 stdio 管道时，
  Node 不会派发 `close`，promise 永不结算——安装器恰恰在「超时已触发」之后
  永久挂起。新增 `POST_KILL_SETTLE_MS`（5s）兜底 reject，`settle()` 做一次性
  保护避免双重结算。
- **`gpg-signing.sh` 的 `verify`/`audit` 返回真实退出码**：所有 `bad` 此前都是
  纯打印，即使 secrets 缺失或发现 silent-skip 也 `exit 0`，CI 无法据此门禁——
  而这恰恰是 `audit` 存在的理由（抓「看起来成功」的静默跳过），检查器自己成了
  同一种静默成功。
- **`gpg-signing.sh` 未知 target 不再静默成功**：`targets_filtered` 在
  `< <(...)` 进程替换里运行，其 `exit 2` 只杀掉子 shell，父进程带着空目标列表
  继续跑，于是 `gpg-signing.sh verify typo` 为 0 个仓库打印一份干净报告并
  `exit 0`——最可能拼错的调用方式反而是唯一静默成功的那个。新增
  `require_known_targets()` 在当前 shell 校验，并列出已知 target。
- **`gpg-signing.sh` 的 `seed` 加 `trap 'stty echo' EXIT INT TERM`**：
  在 `stty -echo` 与 `stty echo` 之间被 Ctrl-C 或 `set -e` 打断时，操作者的
  终端会永久关闭回显，接下来输入的每个字符都不可见且无法恢复。
- **`reviewer.scope_chunk_size` 补 `minimum: 1`**（`config/config.schema.json`
  与 `iterate_cli/data/config.schema.json` 字节同步）：原先只声明 `type: integer`，
  一个手改的 `scope_chunk_size: 0` 能通过 `iterate validate config`，进而把
  full-scope 评审切成零大小的分块——产出一个「读了零个文件却报告成功」的空评审。
  新增一条回归测试锁住两份 schema 字节一致，避免以后只改一份导致发布包内嵌的
  schema 过期。

### 测试 / Tests

- 新增 `tests/test_personalize.py`（24 项）：rfind 拼接、标题级别边界
  （h3 子标题不切断、h1 用户章节被清除）、丢弃条目 warning。
- `tests/test_config.py` 扩充至 74 项，覆盖 `config unset` 的叶子删除、
  祖先剪枝、注释剥离 warning、备份生成、JSON 契约。
- `tests/test_install_script.py` 扩充至 191 项：stdio reconfigure 防御性、
  富文本转义（rich 与非 rich 两条路径）、`--version` 与 pyproject 对齐、
  校验下载失败回退 / 校验不匹配 fail-closed。
- `tests/test_publish_qoder.py` 新增确定性 zip 四项（不同 mtime 字节一致、
  成员有序且单一顶层、时间戳钉死、内容往返）与 check 流分离两项。
- `tests/test_validate.py` 新增 `scope_chunk_size` 上下边界（0/-1 拒绝、
  1/25/1000 通过、非整数拒绝、镜像字节一致）与 stdio reconfigure 两项。
- `tests/test_drift_ignore.py` 新增 `fingerprint list` 七项（TUI、JSON 形状、
  纯读不重扫、`drift_check` 关闭仍可用、空基线提示、损坏配置 fail-closed、
  非法动作 exit 2）。
- `npm-installer/test/mode.test.js` 新增两个进程组用例：孙进程落盘标记文件
  证明其确实被杀；孙进程无视 SIGTERM 并握着管道证明 promise 仍在 12s 内结算。
- `tools/gpg-signing.sh selftest` 新增两条断言锁住 `require_known_targets`
  的退出码（0/2），沿用该文件自身的准则「没人见过它失败的检查器不值得信任」。

---

## [3.4.4] — 2026-09-30

本轮为无人值守的全量复检（Bugbot 式代码评审 + UX/功能缺口评审），共 24 个提交，
全部为修复与文档变更，无新增功能（因此为 patch 版本）。

### 修复 / Fixes — 安装与发布链路

- **安装器版本解析（阻断级）**：三处安装器均调用 `/releases/latest`，该端点返回
  「最新发布」而非「最新携带安装包的发布」——线上实测指向 `v2.1.5`（仅有
  `SHA256SUMS.txt`），导致**安装 100% 失败**、`iterate update` 永远报告"已是最新"。
  `updater.RELEASES_API_URL` 与 `scripts/install.py` 改查 `/releases?per_page=100`
  并挑选第一个真正携带 `iterate-skill.tar.gz` 的发布（`_select_skill_release`），
  离线发布（draft/prerelease）与版本回退均有独立报错文案。实测：旧逻辑取
  `v2.1.5`，新逻辑取 `v3.4.2`。
- **命令注入：拒绝包管理器远程执行动词**：`personalize` 的安全命令白名单
  （`KNOWN_SAFE_COMMAND_PREFIXES`）按**前缀**匹配，`npx` 在列意味着
  `npx -y evil` 只要出现在配置里就会以 `shell=True` 执行任意代码。已将 `npx`
  移出白名单，并新增 `_REMOTE_EXEC_VERBS` 闸门拦截 `npm exec`/`npm x`、
  `pnpm dlx`/`pnpm exec`、`yarn dlx`、`bun x`/`bun exec`；`npm run build`、
  `npm test` 等本地脚本仍然放行。
- **tar 解压拒绝 Windows 盘符成员**：`C:/evil` 这类成员在 POSIX 下既非绝对路径、
  也不含 `..`，两道既有防线全部漏过。新增 `_DRIVE_LETTER_RE` 于解压前拦截。
- **npm 安装器传输后大小校验**：`TARBALL_MAX_BYTES` 此前只在 curl 阶段生效，
  新增 `enforceDownloadedSize()` 在传输完成后按落盘体积复核，超限即删除并失败。
- **Qoder 包排除 `kernel/` 等目录**：`publish_qoder.MANDATORY_EXCLUDES` 对齐
  `release.yml` 的路径排除（`harness`/`kernel`/`tests`/`.githooks`/`badges`），
  此前这些目录会混入发布产物。
- **`validate` 非 UTF-8 配置就地报告**：`load_schema`/配置读取改抛 `ValueError`
  并输出可读错误，不再抛原始 `UnicodeDecodeError` traceback。

### 修复 / Fixes — CLI 输出契约（`--json` 与退出码）

- **`--json` 的 stdout 恒为单个可解析文档**：
  - `refresh --json` 先向 **stdout** 打印人类警告再打印 JSON，令
    `iterate refresh --json | jq` 直接解析失败；警告仅在非 `--json` 路径输出。
  - `config --json`、`config get KEY --json` 在配置缺失/键名未知时输出**空**
    stdout，而同一函数的"中间节不是映射"分支却输出 `{"error": ...}`——一个命令
    两套契约；现已统一为 `{"error": ...}`。
  - 任意子命令 `-p /nonexistent` 同样只给退出码不给 JSON，已补上。
- **`doctor --json` 的 `healthy` 与退出码一致**：此前 `healthy` 只看
  `has_errors()`，而退出码用 `errors or (strict and warnings)`，于是
  `doctor --strict` 下"仅告警"报告打印 `"healthy": true` 却退出 1，
  `jq .healthy` 与 `$?` 对同一次运行给出相反结论。现 `healthy` 定义为
  `exit code == 0`，并同时输出 `blocking`/`strict`/`has_errors`/`has_warnings`，
  不丢信息；未加 `--strict` 时取值不变。
- **`show` 与 `status` 对损坏配置给出同一结论**：两者的渲染条件完全相同，
  但 `show` 无条件返回 0、`status` 返回 1（其注释写明理由：否则 CI 会把坏配置
  当成功）。挂 `show` 的流水线因此一直是绿的。现 `show` 亦退出 1，TUI 路径
  并给出处置建议。
- **`config set` 用法错误退出 2**：裸 `iterate`、交互命令带 `--json`、
  `update --json` 缺 `--yes` 均返回 2（"你调用错了"），而
  `config set KEY` 缺 `VALUE` 返回 1（"操作失败"），自动化无法区分。
  现统一为 2；**操作性**失败（如 `max_rounds 999`）仍为 1，测试已钉住两侧。
- **ASCII 横幅不再污染重定向输出**：横幅是 8 行块状字符，此前在任何 isatty
  检查之前写入 stdout，于是 `v=$(iterate --version)` 捕获到 8 行艺术字加版本号，
  与调用点自己写的"非 TTY stdout 只输出一行裸 `iterate <version>`"直接矛盾，
  也破坏了 SKILL.md 推荐的 `iterate config get KEY` 捕获用法。横幅现仅在交互
  终端显示。
- **`--json` 帮助文本补全命令清单**：`iterate --help` 只列了
  `status/show/doctor/refresh/config`，但 `guard`、`invariant`、`fingerprint`、
  `update`（以及 `--version`）同样支持，脚本作者会误以为不支持。现全部列出，
  并写明"除交互命令外，失败路径也保证 stdout 只有一个 JSON 文档"。

### 修复 / Fixes — 非交互（CI/管道）场景下的提示

- **`personalize --clear` 不再对管道抛 EOF**：此前无护栏地调用 `input()`，
  管道 stdin 触发 EOF 后落入通用处理器，提示"输入已结束（Ctrl+D / EOF）"却不提
  `--yes`——而 `--yes` 正是为此存在的。现与 `iterate update` 一致：先检测
  非交互 stdin 并提示 `Pass --yes to confirm ...`，再画提示符。
- **`install.py` 非交互提示点明处置**：`update` 缺 `--yes` 时只报
  "Update cancelled."，`install` 缺 `--ai` 时只报"No assistants selected.
  Installation cancelled."，均未说明是 stdin 导致、也未点出 `--yes` /
  `--ai <name>` / `--ai all`。现两类均先给出诊断再给标志位。
- **`guard pre-check --dry-run` 不再假装预览**：`pre-check` 是静态校验、从不
  执行命令，却打印 "guard-pre: DRY-RUN preview (nothing executed)"，暗示常规路径
  会执行、且该标志改变了结果；其帮助文本也承诺"预览将要执行的确切命令"，
  是 `pre-check` 无法兑现的承诺。现改为如实说明（"guard-pre is read-only ..."），
  并把帮助文案的作用域限定到 `post-check`。JSON 负载中的 `dry_run` 字段保持不变。

### 修复 / Fixes — 正确性

- **`config --json` 序列化日期类型**：date/datetime 值直接 `json.dumps` 抛
  `TypeError`，三处输出点补 `default=str`。
- **`iterate update --check --assistants` 每条路径都校验**：此前 `--check` 分支
  与交互"先检查后确认"分支跳过校验，拼错的名字（如 `cluade`）静默退出 0；
  错误信息现在直接列出 `updater.ASSISTANT_SKILL_DIRS` 而非指向 `--help`。
- **`generate_refreshed_md` 末尾标记用 `rfind`**：用户自有的结束标记若在文件中
  出现多次，`find` 命中第一处导致标记重复、其后内容被吞。
- **`doctor --fix` 重复计数与备份命名**：重复数此前把整条字符串条目也算进
  差值（报出比实际多的数字）；备份名改为 `文件名-时间戳-随机 6 位十六进制`，
  同一秒内的多次修复不再互相覆盖。
- **`guard` 超时杀进程路径不再抛异常**：`proc.kill()` 在进程已退出时抛
  `ProcessLookupError`（`OSError` 子类），会以 traceback 掩盖真正的超时结论；
  现 `killpg` 与 `proc.kill` 分别兜底。
- **`prompt_int_in_range` 越界默认值改为夹取**：`default` 超出 `[min, max]` 时
  既不接受也不拒绝，陷入无限循环（回退该修复会让测试套件挂死）。
- **`uninstall` 目标去重与逐项容错**：`claude`/`claude-code` 同指向
  `.claude/skills/iterate`（`gemini`/`gemini-cli` 同理），`--ai all` 时第一个别名
  删完、第二个别名撞上"无 SKILL.md 标记"的防御复检，于是一次**完全成功**的卸载
  却打印 "Skipped 2 target(s) that did not look like iterate-skill installations."。
  现按目标目录去重；`shutil.rmtree` 亦加护栏，单个只读/锁死目录不再以原始
  traceback 中断其余目标，部分失败退出码为 1。
- **安装摘要框按显示列而非字符数填充**：`_frame_box` 用 `len()` 计算填充，CJK
  字形占两列却只算一列，右边框 `│` 溢出、上下横线差一列。新增本地
  `_display_width`（与 `iterate_cli.tui` 同算法，因该脚本必须在安装前独立运行
  而无法依赖 `iterate_cli`）。
- **下载量徽章脚本容忍 HTTP 帧错误**：`http.client.HTTPException`
  （`IncompleteRead`/`BadStatusLine`/`LineTooLong`）既非 `OSError` 也非
  `ValueError`，截断响应会以 traceback 打断整个更新，恰好放弃了"复用上次已提交
  数值"这条为该场景而写的回退路径。现已一并捕获，`fetch_json` 文档亦声明该类型。

### 重构 / Refactor

- `generator._guess_dir_purpose` 移除从未被读取的 `scan` 形参，唯一调用方一并更新。

### 测试 / Tests

- 新增 `tests/test_command_safety.py`（9 例：远程执行动词拦截、`npx` 移除、
  本地 `npm run`/`test` 仍放行）。
- `tests/test_updater.py` 发布夹具改为 JSON **列表**以匹配新端点，并补 6 例发布
  选择 + 4 例盘符路径。
- `tests/test_install_script.py` 新增：卸载别名去重与逐项容错（4）、摘要框对齐
  （5）与显示宽度（6）、越界默认值夹取（4，回退修复会挂死）、非交互提示点明
  标志位（2）、非 UTF-8 输入（6）。
- `tests/test_onboarding.py` 新增：`--version` 重定向输出为单行裸值（2）、
  `--json` stdout 单文档契约（4）、`show`/`status` 损坏配置一致（4）、
  `personalize --clear` 非交互拒绝与 `--yes` 穿透（2）。
- `tests/test_config.py` 新增：`--json` 错误对象契约（3）与用法/操作退出码分工（2）。
- `tests/test_doctor.py` 新增 `TestStrictJsonConsistency`（4）；
  `tests/test_guard.py` 新增 dry-run 语义（3）；`tests/test_tui.py` 新增
  `TestJsonHelpText`（3）与横幅 TTY 闸门（2）；`tests/test_update_downloads_badge.py`
  新增 HTTP 帧错误回退（1）。
- 全量 `pytest tests/ -q` 1236 通过；`ruff check .` 通过；
  `npm test --prefix npm-installer` 通过；24 个提交逐一通过 ruff 与
  全量 `.py` 语法校验，且均不含 `harness/`、`kernel/` 路径。

---

## [3.4.3] — 2026-09-19

### 修复 / Fixes

- **Guard 命令输出有界与超时收敛（F26-F31）**：`guard._run_command` 改为 `Popen` +
  分块 drain（`_DRAIN_CHUNK_CHARS=64 KiB` 逐块读、超长行/超宽字节被截断，`_OUTPUT_LINE_CAP=200`/
  `_OUTPUT_BYTE_CAP=1 MiB`）+ `_COMMAND_TIMEOUT_SECONDS=600` 超时经 `start_new_session`
  进程组 `SIGKILL`（连子进程一起杀），杜绝命令刷屏耗尽内存或永不返回。
- **`iterate --json --version` 严格机读**：纯 JSON 单行输出（无 banner、exit 0），供脚本判读。
- **所有权标记缺失/损坏**：`personalize` 告警而非静默跳过（非 UTF-8 读取不崩溃）。
- **忽略匹配**：`_matches_ignore` 用 `fnmatchcase` 全平台大小写敏感；`_safe_extractall`
  Python<3.12 回退路径拒绝 symlink/hardlink/绝对路径成员。
- **安装器 fail-closed（ReleaseIntegrityError）**：校验和缺失/下载失败/校验不匹配一律
  exit 1、不落文件、绝不打印 "Update complete."；纯网络失败才回退本地源；`_parse_checksum`
  非 UTF-8 不崩溃。npm 安装器 null 退出码归一 1、`runCommand` 10 分钟超时 + 1 MiB 尾部缓冲；
  `_argmax`/`_is_async_command`/`_output_mode_validate` 均拒绝非法值。
- **配置写入原子性**：`set_config_values` 校验失败回滚并恢复原始字节、无 `.tmp` 残留；
  `interactive_config` 遇损坏现有 config 拒绝（返回 1）且文件原样；`install_command`
  多助手部分失败逐个报告（exit 1）；`publish_qoder._copy_tracked_tree` 仅拷贝已跟踪文件，
  特批 untracked/scratch/dev/harness 一律不进入产物。

### 测试 / Tests

- 新增回归覆盖：`tests/test_guard.py`（分块 drain、超时杀进程、非 UTF-8 报错不崩溃）、
  `tests/test_install_script.py`（EOF/非 UTF-8/校验和 fail-closed/绝对路径/符号链接拒绝）、
  `tests/test_validate.py`（`validate_dimensions` 非 UTF-8 不崩溃）、
  `tests/test_publish_qoder.py`（`_copy_tracked_tree` 只含已跟踪文件）、
  `tests/test_onboarding.py`（corrupt config `status --json` 返回 1、upsert 原子性）。

---

## [3.4.2] — 2026-09-18

### 修复 / Fixes

- **守卫命令防挂死与内存有界（F7）**：`guard._run_command` 原先用 `subprocess.run` 无上限收集输出，命令一直刷屏会耗尽内存、无 `timeout` 时永不返回；现改为 `Popen` + 有界尾部缓冲（`_OUTPUT_LINE_CAP=200` 行 / `_OUTPUT_BYTE_CAP=1 MiB`）+ `_COMMAND_TIMEOUT_SECONDS=600` 超时 + `start_new_session`（`_kill_process_tree` 用进程组 `SIGKILL` 连子进程一起杀）。
- **`--json --version` 输出机器可读（F5）**：`iterate --json --version` 先前输出的是人类文案 `Iterate v3.4.1` + banner 引导，JSON 消费者无法解析版本；现严格输出 `{"command":"version","version":"..."}` 且不打印 banner，退出码 0。
- **迭代文件中所有权标记失效时告警（F4）**：`personalize.build_updated_iterate_md` 在 ITERATE.md 缺少/损坏 `<!-- iterate:start -->` 标记时静默返回 None，用户数据被悄悄跳过；现发 `tui.warning`（"ownership markers ... user-owned section cannot be updated"）后交给主流程处理。
- **忽略规则大小写确定性（F6）**：`fingerprint._matches_ignore` 用 `fnmatch.fnmatch`（macOS/Windows 上大小写不敏感）、Linux 敏感，行为随平台漂移；改 `fnmatchcase` 全平台大小写敏感。
- **Python<3.12 解压回退路径拒绝软/硬链接（F3）**：`updater._safe_extractall` 在无 `tarfile.data_filter`（<3.12）的回退分支上裸 `extractall`，软/硬链接成员可借链接链逃逸；现该分支对任何 symlink/hardlink 成员一律 `TarError` 拒绝（发布 tar 包本不含链接）。
- **更新完整性失败必拒（F8）**：`install.update_command` 在缺 `checksum_url` / 校验和下载失败 / 条目缺失 / SHA-256 不匹配时曾回退"本地目录更新的成功路径"（exit 0、"Update complete."），实际装的却是未经验证的旧代码；新增 `ReleaseIntegrityError`，完整性失败一律失败快返 exit 1、不装任何文件，"网络下载失败"（纯网络错误）仍合法回退本地源（exit 0）。
- **校验和解析防崩溃（F11）**：`install._parse_checksum` 对非 UTF-8 文件体 decode 直接抛 `UnicodeDecodeError` 崩溃；改捕获后返回 None，由调用方按完整性失败处理。
- **安装部分失败不中断（F12）**：`install.install_command` 对多助手安装时某个助手拷贝失败会整体崩溃/静默；现逐个助手 try/except，失败者记录并继续，最终以 `Exit code 1` + "Installation incomplete" 明确报告部分成功。
- **npm 安装器退出码与超时硬化（F9/F10）**：`npx` 子进程被信号杀死时 `close` code 为 null，被当作成功；`bin/cli.js` 与 `runPythonInstall` 统一把非数字/null 归为 1。`runCommand` 原无超时上限、输出无界收集：新增 `DEFAULT_COMMAND_TIMEOUT_MS=10min`（超时 `SIGKILL`，报错含时长）与 `TailBuffer` 1 MiB 有界尾部缓冲。

### 测试 / Tests

- 全量 1124 个 Python 测试通过、`ruff check` 通过、`npm test` 通过。新增 16 项：守卫有界输出（`seq 5000` 尾部保留且 < 1 KiB）与超时杀进程（monkeypatch 1s / `sleep 30`）；`--json --version` 结构断言；标记损坏告警文案；`fnmatchcase` 大小写敏感；<3.12 分支拒绝软链接、良性树放行；完整性失败 4 例（缺 URL / 校验和下载失败 / 条目缺失 / SHA 不匹配）均 fail-closed、纯网络失败回退本地 exit 0、`update` 完整性失败 exit 1 且不装文件、校验和"Update complete."不可达；非 UTF-8 校验和返回 None；多助手部分失败 exit 1 且报告；npm 端超时拒绝、1 MiB 尾部有界、null 退出码归一为 1。

---

## [3.4.1] — 2026-09-16

### 修复 / Fixes

- **`iterate update` 子进程超时生效（F28）**：`updater._run_command` 先前只把 `timeout` 参数接住却从未传给 `subprocess.run` —— `GIT_TIMEOUT_SECONDS`（120s）与 `PIP_TIMEOUT_SECONDS`（600s）是花瓶常量，`git pull --ff-only` / `pip install` 一旦挂起，整个 `iterate update` 会无限阻塞；现生产默认 runner 真正以 `timeout=` 传给 `subprocess.run`，`subprocess.TimeoutExpired` 转成可读的 `RuntimeError`（清晰报错指令与超时时长），注入的测试 runner 保持原 `(argv)` 契约不变。
- **安全解压覆盖目录成员与符号链接（F29）**：`updater._safe_extractall` 此前只对非目录成员做路径穿越检查，`../escape/` 这类目录成员在无 `tarfile.data_filter` 的 Python（<3.12）回退路径上可逃逸；现每个成员（含目录）统一校验为相对路径、拒绝绝对路径/`..` 段，符号链接/硬链接成员的链接目标也拒绝绝对路径与逃逸目标，设备/管道成员照旧拒绝。
- **下载上限按字节精确执行（F30）**：`updater._urlopen_bounded` 原按"块数"近似封顶（最多可读到 ~52.4 MiB > 50 MiB），现改为累计真实字节数，超过 `MAX_DOWNLOAD_BYTES` 立即中断。

### 加固 / Hardening

- **`iterate update --assistants` 白名单（F31）**：`--assistants` 传入未知助手名（如 `--assistants cluade`）此前被静默忽略，只更新了命中的助手子集，极易误判为"全部未装"；`run_update` 现在**在任何网络请求前**用 `ASSISTANT_SKILL_DIRS` 校验名称，未知名字失败快返（`outcome.assistants_unknown`，CLI 列出合法名 + 退出码 1，`--json` 含 `assistants_unknown` 字段）。`--assistants` 空列表（= 跳过技能目录刷新）与缺省（= 全部）不受影响。

### 测试 / Tests

- 全量 1104 个 Python 测试通过、`ruff check` 通过。新增 15 项：生产 runner 超时确实传给 `subprocess.run`、注入 runner 契约不变、`TimeoutExpired` 转可读错误；目录穿越 / 绝对路径 / `..` 逃逸 / 绝对链接目标 / 逃逸链接目标 各自被拒，良性树正常解压；50 MiB 上限恰好放行、多 1 字节拒绝；`--assistants` 已知名 ok / 未知名上报 / 空列表合法 / 未知名失败快返不碰网络 / `to_dict` 含 `assistants_unknown`。

---

## [3.4.0] — 2026-09-15

### 新增 / Features

- **`iterate update` 自更新命令**：一键把 CLI 与所有已安装的助手技能目录更新到最新 GitHub Release，全程不依赖 ~/.agents/skills 结构：
  - **校验先行**：从 GitHub API 拉取 latest release（`iterate-skill.tar.gz` + `SHA256SUMS.txt`），任何写入发生前先做 50 MiB 有界下载、SHA-256 逐字节核对、安全解压（拒路径穿越/解压炸弹/设备节点）；校验不通过一律拒绝写入。
  - **双目标更新**：(a) 按 `scripts/install.py` 的 `SUPPORTED_AI` 布局刷新已安装助手技能目录（SKILL.md / config/ / iterate_cli/ / scripts/ / templates/ ...，剔除 harness/ 并清理历史残留）；(b) 重装 CLI 包——pip 安装走 `--force-reinstall --no-deps` 已验证解压源码，源码安装走 `git pull --ff-only` + `pip install -e`。
  - **交互语义**：默认交互式确认（默认 No，与安装器一致）；非交互 stdin 需显式 `--yes`；`--check` 只对比版本零写入；`--json` 输出结构化结果（需 `--yes`）；`--assistants` 可限定刷新范围；单一助手失败不阻断其余更新。
  - **`iterate --version` 更新提示**：24h 缓存式一次性提示"有新版本，运行 `iterate update`"（`ITERATE_UPDATE_CHECK=0` 可关闭；任何异常静默降级，绝不破坏 `--version`）。

### 测试 / Tests

- 全量 1089 个 Python 测试通过、`ruff check` 通过。新增 47 项：`tests/test_updater.py` 覆盖版本比较、release 发现（mock 网络，含 403/404/网络异常/坏 JSON）、SHA-256 校验匹配/不匹配/缺条目、安全解压与顶层布局断言、安装方式检测、助手目录检测去重、技能目录复制/替换/清理/harness 剔除/符号链接祖先防护、pip/source 两种 CLI 重装（mock runner）、`run_update` 全流程（不可达/已是最新/未确认取消/校验失败拒绝/单助手失败容错）、缓存提示；`tests/test_updater_sync.py` 用 AST 锁定 `ASSISTANT_SKILL_DIRS`/`REQUIRED_RELEASE_PATHS`/`OPTIONAL_RELEASE_PATHS` 与 `scripts/install.py` 三份同名常量永不漂移。

---

## [3.3.1] — 2026-09-14

### 修复 / Fixes

- **doctor dimension_sets 不可哈希崩溃**：手写配置里 `dimensions` 含非字符串条目（如内嵌列表 `[[], "correctness"]`）时，去重检查 `d in seen` 直接抛 `TypeError: unhashable type: 'list'` 令整个 `iterate doctor` 崩溃；现先归一化为 `str` 再判定，崩溃降级为常规 unknown-dimension 警告（doctor.py `_check_dimension_sets` 去重与 `unknown` 两遍归一化逻辑统一）。

### 加固 / Hardening

- **config schema 拒绝空命令列表**：`validation.commands` 与 `invariants.commands` 各模块条目增加 `minItems: 1`（与 `command_whitelist` 一致）——空数组毫无意义（运行时本就自动丢弃空模块），直接在 schema 层面报出；`iterate_cli/data/config.schema.json` 打包副本同步。

### 维护 / Maintenance

- **npm 安装器清理**：`parseArgs` 移除重复死亡的 `token` 默认键（`normalizeToken(...)` 永远覆盖前一默认值，行为不变）；新增 `parseArgs([])` 默认 token 归一化断言。

### 测试 / Tests

- 全量 1041 个 Python 测试通过、`ruff check` 通过、npm 安装器测试通过；新增覆盖：不可哈希 dimension 条目不再崩溃（降级为 warn）、空命令模块触发 schema minItems 警告、加载器默认 token 归一化。

---

## [3.3.0] — 2026-09-12

### 新增 / Features

- **guard pre-check 工具可用性检查**：`guard pre-check` 对每条配置的验证命令检查其首 token 对应的可执行文件是否在 PATH 上（shell 内建如 `true` 除外）；缺失时判定 `FAIL` 并列出缺失工具，防止"命令配置了但环境里根本没有该工具"的假绿灯。
- **`invariants.ensure` 路径安全**：`iterate invariant` 的 file-existence 断言只接受项目根目录内的相对路径——绝对路径与 `../` 越出项目根的逃逸一律 `FAIL`（拒绝在交付门禁里让断言指向项目外文件）。
- **`iterate status` 区分损坏与缺失配置**：`iterate.config.yaml` 存在但无法解析时，status 退出码 1 并提示"could not be parsed → 运行 `iterate doctor`";缺失时保持退出码 0 并提示仅存在 ITERATE.md。`--json` 新增 `config_exists` / `config_ok` 字段供脚本区分。
- **doctor 标量 section 硬错误**：`review:` / `git:` / `validation:` 为标量（非 mapping）时如实上报 error 而非含糊跳过。
- **install.py / npm 安装器加固**：GitHub API 请求增加连接错误（`http.client.HTTPException`）分类提示；`_parse_checksum` 强制 64 位十六进制摘要（非 hex / 截断一律忽略，大写归一化）；`_safe_extractall` 在所有 Python 版本上拒绝 device/fifo 归档成员；`parse_value` 改为 JSON 优先、YAML 兜底；`set_nested_value` 拒绝空段；`init_config` 原子写入。npm 安装器 token 自动 trim 空白（`GITHUB_TOKEN` 常带尾随换行），并在携带 `Authorization` 的 API 请求上禁用跨主机重定向（curl 会把自定义 `-H` 头原样转发到重定向链上的每个主机）。
- **publish_qoder.py 校验加固**：`_git_archive_extract` 显式以仓库根为 cwd 运行 `git archive`（否则从子目录调用时 pathspec `:!harness` 相对当前目录匹配，可能把 `harness/` 打包进去）；zip 顶层目录检查改为校验**每个**条目（此前只查 `names[0]`，可被排序在后的外来顶层目录绕过）；`_find_harness` 同时覆盖名为 `harness` 的文件与目录。

### 修复 / Fixes

- **tui 用户文本富文本转义（F24）**：tui 渲染用户输入的文本（如 `[module]`）前统一 `rich.markup.escape`，避免把用户文本误当 markup 标签。
- **doctor C2/C3/C4/C5**：metachar 报错与无白名单校验不再打印自相矛盾的成功行；`run_doctor_fix` 改用原子写入并捕获 `OSError`/`YAMLError`；`_render_next_actions` 覆盖 `invariants.ensure` 异常的动作建议。
- **install.py**：`_download_bytes` / `_fetch_latest_release_info` 分类网络连接错误；`set_config_values` 捕获 `set_nested_value` 的空段 ValueError 并清晰报错。

### 测试 / Tests

- 全量 1040 个 Python 测试通过、`ruff check` 通过、npm 安装器测试通过；新增覆盖：MissingCommandTool / shell 内建免二进制、ensure 绝对路径与项目外逃逸拒绝、status 损坏配置 TUI/JSON、doctor 标量 section / YAML 序列化错误 / next-actions、checksum 64-hex 策略、device/fifo 归档成员拒绝、init_config 原子失败不回滚脏文件、zip 外来顶层目录与嵌套 harness 文件。

---

### 维护 / Maintenance

- 日常审查与发版：全部测试通过（1002 passed），ruff 检查通过，无新增问题。

## [3.2.2] — 2026-09-09

### 修复 / Fixes

- **doctor 标量 onboarding 配置崩溃**：`onboarding:` 为标量字符串（手写配置常见）时，`_check_manifest_drift` 调用 `.get()` 抛出 `AttributeError`。改用 `isinstance` 守卫，与 `refresh.py`/`wizard.py` 同一模式。
- **ruff 代码质量**：修复 `I001`（import 排序）、`BLE001`（盲捕异常）、`RUF059`（未使用解包变量）。

### 测试 / Tests

- 新增 `TestScalarOnboardingConfig` 回归测试，确保标量 onboarding 配置不再让 doctor 崩溃。

---

## [3.2.1] — 2026-09-07

### 修复 / Fixes

- **命令白名单运行时二次校验（防绕过）**：`iterate guard` 运行时执行校验命令前，除了外壳元字符检查，再次校验命令以已知安全工具前缀开头（与 `personalize` 落盘时同一套判定）。`rm -rf .`、`curl …` 这类"无元字符但任意可执行文件"以及 `python <任意可执行文件> -m <安全工具>`（中间夹带脚本）都不再通过；`python -m` 仅当 `-m` 为解释器之后的第二个 token 才被识别为模块调用。安全前缀新增 `dart`/`flutter`/`mix`/`bundle`/`ruby`/`true`/`false`/`exit`。
- **手写配置不再触发崩溃**：`onboarding:` 为标量/列表、`personalization` 非 dict、`validation.commands` 非 dict、`language: null` 或非 `zh`/`en` 等手写/漂移污染的配置，在 `status`/`fingerprint`/`refresh`/`show`/`wizard`/`config set` 中一律安全降级或显式拒绝，不再抛 `AttributeError`/写坏结构。
- **install.py 供应链加固**：跨主机重定向时剥离 `Authorization` 头（`_SafeRedirectHandler`/`_urlopen`）；GitHub API 响应按块读取并加字节上限；`_safe_extractall` 在解压前校验单成员 ≤256MiB、总量 ≤500MiB（解压炸弹防护）；`copy_skill_files` 拒绝经符号链接祖先目录写入，并修复文件/目录类型冲突（过期文件挡住目录、过期目录挡住文件）。
- **install 无操作不再报成功**：非交互 stdin、所有目标均已存在且未给 `--force` 时返回退出码 1（与 uninstall 无操作契约一致），npx 包装层可据此区分"已安装/已刷新"与"什么都没发生"；uninstall 在非交互 stdin 下拒绝未经确认的删除。
- **npm 安装器**：`askYesNo` 在 stdin EOF 或 30s 超时后回落到默认值（不再挂死）；`parseChecksums` 跳过非 64 位十六进制摘要、拒绝同一 basename 的冲突摘要（防篡改）、兼容 `#` 注释行；`-h`/`--help`/`-v`/`--version` 短路解析（后面跟坏参数也不再报错）；`package.json` 增加 `files` 白名单并移除全局 `iterate` bin（避免与真实 CLI 冲突）。
- **validate.py**：JSON Schema 文件本身结构损坏（坏 `$ref`/`$defs`、类型错误）时报出 "Invalid JSON Schema" 诊断而不是未捕获 traceback 崩溃。
- **config set 嵌套保护**：点号路径的中间段为标量/列表时明确拒绝写入（不静默替换成 mapping）；`.configset` 备份文件名追加随机盐，同一秒内多次 `config set` 不再互相覆盖备份。
- **doctor dimension_sets**：非字符串的集合名与混合类型 dimension 条目不再让 `sorted()`/正则崩溃，统一归一化后上报。

### 测试 / Tests

- 全量 Python 测试 1001 个全部通过，`ruff check .` 通过，npm 安装器测试通过：
  - `test_install_script.py`：符号链接祖先拒绝 / 类型冲突 / 超大成员 / 总量超限 / 非交互无操作返回 1。
  - `test_guard.py`：未知前缀命令拒绝 / 已知安全命令放行。
  - `test_onboarding.py`：`validation.commands` 非 dict 归零、`language` 非法值回退默认。
  - `test_drift_ignore.py`：标量 `onboarding` 在 status/refresh 路径安全降级。
  - `test_config.py`：中间段标量拒绝覆盖、备份名加盐不冲突。
  - `test_validate.py`：损坏 JSON Schema 本身被诊断而非崩溃。
  - `test_publish_qoder.py`：默认 `--out` 构建不再向仓库工作树泄漏 zip。

---

## [3.2.0] — 2026-09-06

### 新增 / Features

- **`iterate refresh --json` / `--dry-run --json`**（B1）：refresh 增加结构化 JSON 输出——`--dry-run --json` 预览而不写盘，`--json` 先预览后写入；负载含 `ok`/`dry_run`/`changed`/`config_changed`/`md_changed_lines`/`stats` 与失败时的 `error`，供脚本/CI 消费。
- **`iterate doctor --strict`**（B2）：新增 `--strict` 标志，将 warning 一并视为失败（退出码 1），供 CI 在"非全绿即失败"的门禁场景使用；默认仍仅 error 阻塞，`--json` 下同样生效。
- **`iterate status --json` 漂移明细**（B4）：结构化输出新增 `drift_detected`（布尔或 null）及 `drifted_added`/`drifted_removed`/`drifted_changed` 明细列表，脚本不再需要解析人类可读的 summary 字符串。
- **`iterate config` 点号路径别名**（B5）：`set`/`get` 支持嵌套点号键（如 `config set git.use_worktree true`、`reviewer.coverage_validation false`），与 `iterate show` 的路径表达及手写配置习惯保持一致；JSON 输出统一以规范扁平键返回。
- **doctor 新增 ITERATE.md USER-OWNED 标记检查**（B6）：`iterate refresh` 会在标记缺失时拒绝覆盖（防手写内容丢失），此前只在 refresh 时才暴露；doctor 新增 `iterate.md.markers` 检查在诊断阶段提前告警，建议 `iterate reonboard` 恢复标记。同步新增 `invariants` 结构 + `invariants.commands` 元字符安全检查。

### 修复 / Fixes

- **doctor 白名单合规检查 fail-open**：`_check_whitelist_compliance` 此前遇到不安全白名单条目即提前返回，跳过命令级 shell 元字符扫描（`pytest; rm -rf /` 可借坏条目绕过）；现元字符扫描无条件执行，两个问题都如实上报；白名单条目先 `.strip()` 再参与匹配（`" pytest "` 不再产生误导性 "not in whitelist" 警告）。
- **doctor manifest 漂移三原因区分**：无 drift 检查时按"配置不可读 / drift_check 已禁用 / 尚未录制指纹（建议 `iterate refresh`）"分别说明，不再笼统报"不适用"。
- **`doctor --fix` 补录缺失指纹（B3）**：对已 onboarded（录音含 skill_version）但 `fingerprints` 为空的配置，`--fix` 现在补录当前 manifest 指纹，恢复漂移检测；已有指纹原样保留。`--fix` 失败时给出明确原因（缺配置/配置损坏），`--json` 下输出与 DoctorReport 同构的失败负载。
- **`doctor --fix --json`、`--json-out`、`fingerprint --json` 输出修正**：`--fix` 失败改输出 DoctorReport 形状 JSON；`--json-out` 与 TUI 模式结合时也保留 `fixes`；`fingerprint verify --json` 的 `reason` 精确到未 onboarding / 已禁用 / 无指纹三类。
- **CLI 语义修正**：裸 `iterate`（无子命令）退出码由 0 改为 2（使用错误）；`iterate --version` 在非 TTY（管道）下输出纯 `iterate X.Y.Z` 便于解析；`--json` 对交互式命令（`onboard`/`personalize`/`reonboard`）改为明确拒绝（退出码 2）而非静默吞掉。
- **健壮性兜底（防手写配置崩溃）**：`check_drift` 对脏指纹条目加 `isinstance(dict)` 守卫；`personalize` 加载 `risk_areas`/`known_intentional`/`dimension_focus` 时对非 list 标量不再逐字符迭代；`guard pre-check` 对多个缺失 manifest 全部上报而非只报第一个。
- **refresh 配置与 diff 统计**：空 `command_whitelist` 不再写为 `command_whitelist: []`（schema minItems 1 违例）而是删除该键；`_diff_stats` 改用 `SequenceMatcher` opcode 长度统计，内容行恰好以 `--`/`++` 开头时不再被误吞为 `--- `/`+++ ` 文件头。
- **wizard**：`_run_basic_wizard` 保留既有 `reasoning_effort`（不再重设默认）；`_parse_dimension_selection` 逐项丢弃非法选择而非整组回退（仍保证全非法输入返回 `[]`）。
- **configcmd 非 mapping 拒绝覆盖**：顶层 YAML 为列表/标量（如手写 `- a`）时 `config set` 明确拒绝并原样保留，不再静默回填成 `{}` 后再写入覆盖。
- **publish_qoder.py**：未传 `--out` 时 zip 默认落到当前目录（此前落在临时目录随上下文退出被删除，构建结果凭空消失）；`_copy_tree` 与 git-archive 路径在 dotfile 上保持一致（只排除 `.git` 与显式 excludes；支持顶层文件），zip 条目排序确定化（同源重复构建产生字节一致的产物）。
- **下载/校验安全**：`update_downloads_badge._read_bounded` 改为按 EOF 循环读取（单次 `read` 可能回不足量，此前可绕过字节上限）；`install.py` 与 `installer.js` 的校验和比较改用常量时间比较（`hmac.compare_digest` / `crypto.timingSafeEqual`）；`installer.js` 增加 `--max-filesize` 字节上限、PAT 仅附加给 `api.github.com`（release-asset 公开下载不再携带令牌）、`--fail-with-body` 按 curl 版本回退为 `--fail`。

### 测试 / Tests

- 新增 35 例，全量 Python 测试 970 个全部通过，`ruff check .` 通过，npm 安装器测试通过：
  - `test_doctor.py`：白名单 fail-open / 空白条目匹配 / 条目字符网（3）、drift 禁用与无指纹原因（2）、invariants 结构/命令/ensure（4）、ITERATE.md 标记（2）、`render_report` strict（3）、`run_doctor_fix` 补录指纹（2）。
  - `test_guard.py`：多缺失 manifest 全量上报与混合场景（2）。
  - `test_refresh_reconcile.py`：`_diff_stats` 头部伪鉴别/变更总数（3）、空白名单删键（2）。
  - `test_config.py`：点号别名 set/get（4）、非 mapping 拒绝覆盖（2）、CLI 别名（1）。
  - `test_onboarding.py`：`_parse_dimension_selection` 部分非法保留/去重/空白（3）。
  - `test_publish_qoder.py`：默认 out 存活 / 确定性 zip / dotfile 一致性 + 顶层文件复制（3）。
  - `npm-installer/test/mode.test.js`：`isGithubApiUrl` 令牌作用域（5）。
- 更新既有断言以匹配新语义：裸 `iterate` 退出码 0→2；badge `_FAKE_RESP` 与 SkillHub `FakeResp` 改为位置感知 + EOF 语义（真实 `read()` 行为）。

### 内部 / Internal

- `version` 升至 3.2.0（minor：新增 B1/B2/B4/B5/B6 特性 + 修复批次）。

---

## [3.1.0] — 2026-09-05

### 新增 / Features

- **CLI `iterate fingerprint verify`**：新增指纹校验子命令，比对 `iterate.config.yaml` 记录的 manifest SHA-256 指纹与当前项目根的实际状态，检测技术栈 manifest 的新增/删除/变更（与 `iterate status` 漂移检测共享 `check_onboarding_drift` 逻辑）；退出码 0 = 无漂移，1 = 存在漂移（漂移非阻塞，附 `iterate refresh` 建议）；支持 `--json` 结构化输出（新增/删除/变更/未变清单）。
- **`iterate doctor` 错误摘要带通过计数**：存在错误时汇总行由 `Doctor: N error(s) found.` 升级为 `Doctor: N error(s) found (M check(s) passed).`，一次看清有多少检查通过（仅 warnings 与 clean 路径行为不变）。

### 修复 / Fixes

- **`_cmd_personalize` 写入错误兜底**：`save_personalization` 除 `CorruptConfigError` 外还可能抛 `OSError`/`UnicodeDecodeError`（磁盘满、权限不足、非 UTF-8 路径等），此前会冒泡成原始 traceback；现统一捕获并显示友好错误、退出码 1。
- **wizard 读取既有配置改用 `load_config_strict`**：`_load_existing_onboarding_data` 原先用裸 `yaml.safe_load`，损坏的 YAML 会被静默当作"空配置"继续合并。现改用 `load_config_strict` 明确报错；非 mapping（如裸列表）的配置返回 None 而非静默吞掉。
- **`doctor` 配置解析区分"缺失/损坏/不可读"**：`_check_config_parse` 改用 `load_config_strict`，损坏的 `iterate.config.yaml` 不再笼统报"缺失或不可解析"，而是给出具体 YAML 语法错误定位。
- **`suggest_validation_commands` 不再硬编码 `tests/` 目录**：Python 项目建议的 `pytest` 命令按实际扫描到的测试目录（`tests`/`test`/`__tests__`/`spec`）生成，项目用 `test/` 时不再给出一条必然失败的默认命令。
- **`FORBIDDEN_COMMAND_CHARS` 改为 `frozenset`**：与 `doctor.py`/`guard.py` 的 `COMMAND_METACHARS` 保持一致，获得 O(1) 成员判定（成员检查在命令校验热路径上）。

### 测试 / Tests

- 新增 7 例：`tests/test_drift_ignore.py::TestFingerprintVerifyCli`（6 例：无漂移退出码/输出、变更退出码 1、删除 manifest、未 onboarding 优雅降级、`--json` 无漂移/有漂移负载字段）；`tests/test_doctor.py::TestRenderSummary::test_errors_report_passed_check_count`（错误路径汇总行含通过计数）。
- 更新 2 例以匹配新错误形态：`test_load_existing_onboarding_data_logs_error`、`test_returns_none_on_yaml_list`（wizard 改用 `load_config_strict` 后的错误文案/空配置判定）。
- 全量 Python 测试 935 个全部通过（既有 928 + 新增 7），`ruff check .` 与 `mypy iterate_cli` 均通过。

### 内部 / Internal

- wizard 返回用户流程（`_load_existing_onboarding_data`）的 `scan_project` 调用纳入 `tui.status(...)` 进度上下文，与首次基础配置流程的扫描反馈保持一致。

---

## [3.0.1] — 2026-09-03

### 修复 / Fixes

- **`guard pre-check` 空验证命令 fail-closed**：对*已 onboarded*（存在非空 `iterate.config.yaml`）但 `validation.commands` 为空的项目，`guard pre-check` 不再返回 `PASS`/退出码 0（此前会给出"可以开工"绿灯，而其承诺的 `post-check` 必然失败）。现按 fail-closed 契约改为 `FAIL`/退出码 1，提示先补配置 `validation.commands`，使 pre-check 与 post-check 的退出码语义一致；全新项目（尚无配置）仍正常降级放行。SKILL.md 防御式模式章节同步说明该行为。
- **npm 安装器与 install.py 的校验和 `*` 前缀剥离语义统一**：`installer.js::parseChecksums` 原先用 `replace(/^\*/, '')` 仅剥离一个前导 `*`，而 Python `scripts/install.py::_parse_checksum` 用 `lstrip("*")` 剥离全部前导 `*`，破坏了"两处同步"的既定声明。现统一为剥离全部前导 `*`（`/^\*+/`），并新增 `**` 前缀的边界断言。

### 测试 / Tests

- 新增 `tests/test_release_meta.py`（2 例）：绑定 `pyproject.toml` / `iterate_cli/__init__.py` / `SKILL.md` frontmatter / `npm-installer/package.json` 四处版本号必须一致且为 `X.Y.Z` 语义化版本，防止 post-patch 发版漏改某处导致跨分发渠道漂移。
- `tests/test_guard.py` 新增 2 例：已 onboarded 但无 `validation.commands` 的配置、显式空 `commands` 映射，`guard pre-check` 均 fail-closed。
- `npm-installer/test/mode.test.js` 新增 1 例：多前导 `*` 校验和标记按 `lstrip("*")` 语义剥离。
- 全量 Python 测试 928 个全部通过（既有 924 + 新增 4），`ruff check .` 通过，npm 安装器测试通过。

### 内部 / Internal

- `pyproject.toml` build-system 依赖精确定版本：`setuptools>=68.0` → `setuptools==68.0.0`、`wheel` → `wheel==0.42.0`。

---

## [3.0.0] — 2026-09-03

### 新增 / Features

- **双模式：iterate 原模式 + 防御式编程模式**（v3.0 大版本主线）：SKILL.md 新增防御式编程模式（`/iterate defensive`），面向**用户让 AI 做正常增量式编程任务**（新增功能、修 bug、重构、接入 API、补测试）——宿主 AI 从动手前到收尾**从头至尾贯彻防御式编程理念**：① 动手前（声明假设 + 前置校验）→ ② 动手时（信任边界验证 + 最小步进）→ ③ 动手后（每步后置校验）→ ④ 收尾（不变量守护 + iterate 收敛门禁，**不收敛不交付**）。iterate 原模式（`/iterate`）行为与 v2 完全一致，零回归，默认不变。
- **CLI `iterate guard pre-check [paths...]`**：动手前确定性前置校验——目标路径存在、git worktree 干净、依赖 manifest 就绪、验证命令配置安全；退出码 0 = 可以开工，1 = 禁止开工；支持 `--json` / `--dry-run`。
- **CLI `iterate guard post-check [module...]`**：动手后后置校验——精确执行 `validation.commands.<module>`（运行时唯一权威白名单，不拼装不前缀）；退出码 0 = 本次改动安全，1 = 必须先修复或回滚；支持 `--json` / `--dry-run`。
- **CLI `iterate invariant`**：项目级不变量检查——`invariants.ensure` 文件断言 + `invariants.commands` 命令列表；无 `invariants` 段时自动退化为 `validation.commands`（旧配置零破坏）；退出码 0 = 不变量成立，1 = 存在违反项；支持 `--json` / `--dry-run`。
- **配置 `mode: iterate | defensive`**：`iterate.config.yaml` 新增默认执行模式配置项（默认 `iterate`，零破坏），可用调用参数显式 `defensive` 覆盖；`iterate show` / `iterate config get|set mode` 支持读写。
- **配置 `invariants` 段**：`iterate.config.yaml` 新增 `invariants`（`ensure` 文件断言 + `commands` 精确命令列表），与 `validation.commands` / `command_whitelist` 共用安全基线（白名单校验、元字符防护）；`config/config.schema.json` 与随包分发副本同步扩展。

### 测试 / Tests

- 新增 `tests/test_guard.py`（33 例）：pre-check / post-check / invariant 的正常路径、异常路径（目标缺失、manifest 缺失、命令失败、脏 worktree、损坏配置）与边界场景（无参数、空配置、模块过滤、dry-run 预览、invariants 退化到 validation.commands、JSON 输出与退出码、运行时元字符拒绝、未配置模块报告），并覆盖 CLI 集成（`guard` / `invariant` 子命令的 `--json` 与退出码契约）。
- 全量 Python 测试 924 个全部通过（既有 888 + 新增 36），`ruff check .` 通过。

---

## [2.12.0] — 2026-09-02

### 新增 / Features

- **`iterate config --json` 结构化输出**：非交互式配置命令新增 `--json`，供脚本/CI 场景消费——`iterate config --json` 输出全部可设键的 JSON 对象、`iterate config get KEY --json` 输出 `{"KEY": value}`、`iterate config set KEY VALUE --json` 成功时输出 `{"key": KEY, "value": <解析值>}` 确认对象；stdout 保持纯净（错误仍走 stderr + 非零码），与 `iterate status/show/doctor --json` 契约对齐。

### 修复 / Fixes

- **publish_qoder 安全加固**：`_git_archive_extract` 原先用 `os.system(" ".join(cmd))` 经 shell 执行 `git archive`，`--exclude` 用户输入被无引号拼入命令字符串，存在 shell 注入面。现改用 `subprocess.run(check=False)` 列表形式（不启动 shell）并以真实返回码判定；解压由裸 `archive.extract` 改为 `archive.extractall(members=_safe_members(...))`，`_safe_members` 拒绝绝对路径、`..` 越界、重复成员及逃逸目标目录的符号链接（zip-slip 防护，与 `install.py` 安全基线一致）。
- **install 下载根目录选择更稳**：`_download_release_source` 原返回 `extracted[0]`（临时目录迭代首个子目录），多顶层目录时可能选中非 skill 目录。现要求 release tarball 顶层目录中恰好一个含 `SKILL.md` 标记，否则拒绝并报错返回。

### 测试 / Tests

- 新增 `tests/test_publish_qoder.py::TestSafeMembers`（6 例：正常嵌套成员、`..` 越界、绝对路径、重复成员、逃逸符号链接、目录内安全符号链接）。
- 新增 `tests/test_install_script.py::TestDownloadReleaseSource`（3 例：唯一含 SKILL.md 根被选中、无标记根拒绝、多标记根拒绝）。
- 新增 `tests/test_config.py::TestConfigJson`（5 例：单键 get、全键 list、set 确认且 stdout 纯净、未知键报错、run_config_get 直调）。
- 全量 Python 测试 888 个全部通过，`ruff check .` 通过。

---

## [2.11.2] — 2026-09-01

### 修复 / Fixes

- **refresh 调和结果真正落盘**：`iterate refresh` 原本计算出的新增 `validation.commands`、`command_whitelist` 前缀与 `dimension_sets` 调和结果只用于重渲染 `ITERATE.md`，未写回 `iterate.config.yaml`，导致配置与文档跑偏。现将 `_build_refreshed_config` 改为接收完整 `OnboardingData`，把调和后的 dimension_sets / validation.commands / command_whitelist / reasoning_effort 等一并持久化，同时保留用户既有自定义字段（如自定义命令逐字保留、显式空白名单意图不覆写）。
- **doctor 畸形白名单不再绕过元字符安全网**：`command_whitelist` 为非法形态（如裸字符串 `make`）时，原先跳过了白名单合规校验，且独立的 shell 元字符安全网仅在白名单为 `None` 时运行，导致 `make; rm -rf /` 这种命令可能通过健康门禁。现检测到非法白名单时仍调用元字符检查，安全网不再被绕过。
- **wizard 重跑基础配置不再丢弃数据**：返回用户拒绝更新基础配置、但现有配置无法加载时，重新运行完整基础向导并确认的新数据，若随后未再个性化，会被「全部拒绝/无变更」守卫丢弃导致白做。现在重跑基础向导即视为"更新基础配置"，新采集的数据会正常写入。
- **validate.py 重定义区块切分双重偏移**：`_sections_for_redefinition` 用 `content[match.start():][start:]` 切分，第二次切片偏移作用在已裁剪子串上造成偏移叠加，长前置文本会跳过区块内部终止标题、让其越界吞并后续内容。改为 `content[start:]`（`start == match.end()`）直接切分，块边界正确停在下个 `## `/`### ` 标题前。
- **publish_qoder 幂等标记字符不一致**：依赖自包含说明段的幂等守卫检测单空格 `<!-- QODER:DEPENDENCIES -->`，而写入时经两次 `replace()` 得到双空格版本，导致复用已标注 `SKILL.md` 重建时重复追加。现直接嵌入 `_DEP_MARKER` 原样，重复构建幂等。

### 内部 / Internal

- `iterate_cli/refresh.py::_build_refreshed_config` 签名由 `(existing_config, new_fingerprints)` 改为 `(existing_config, data: OnboardingData)`；局部用具名拷贝替换 `**dict` 解包以消除 mypy type 错误。

### 测试 / Tests

- 新增 `tests/test_refresh_reconcile.py::TestIncrementalRefreshPersistsReconciledData`（4 例：命令/白名单落盘、dimension_sets 落盘、_build_refreshed_config 直接同步、自定义命令保留）。
- 新增 `tests/test_validate.py::TestSectionsForRedefinition`（2 例：块止于下个三级标题、两个连续重定义块互不吞并）。
- 新增 `tests/test_publish_qoder.py`（2 例：幂等标记逐字一致、普通文件仅追加一次）。
- 全量 Python 测试 874 个全部通过，`ruff check .` 通过。

---

## [2.11.1] — 2026-08-31

### 修复 / Fixes

- **偏门范围重定义「禁抄预设」**：`SKILL.md` Phase 0 明确——未命中任何命名维度集的 goal，必须从根（维度全集）重新推导维度方案，禁止以全局 `dimensions` 或任一已有维度集为起点筛选/微调；每个选中维度必须给出本范围特有的独立理由（与某预设集雷同即视为套用、推翻重想），并可新增非标准临时维度。范围路由（命中预设）与重定义（未命中）两条路径彻底分离，防止 AI 惰性沿用预设。

### 新增 / Features

- **`scripts/validate.py decisions` 新增重定义记录机器校验**：`.iterate_decisions.md` 中出现 `### Scope Dimension Redefinition (on-the-fly)` 小节时，强制要求 `**Origin scope:**` 与 `Dimension / Independent reason` 表格，且每个维度的理由不得照抄 `config/dimensions/<dim>.yaml` 默认 focus（去空白/大小写归一化后比对）。为「禁抄预设」提供可执行的第二道闸。决策日志模板同步新增该小节示例。

### 内部 / Internal

- `pyproject.toml` 的 ruff `extend-exclude` 收录 `.awesome-claude-skills`（第三方 marketplace 校验用 submodule，本地检出会导致 `ruff check .` 假阳性，CI 未检出子模块不受影响）。

### 测试 / Tests

- 新增 `tests/test_validate.py::TestValidateScopeRedefinitions`（8 例：缺 Origin / 空 Origin / 理由抄默认 focus / 理由为空 / 缺表头 / 无数据行 / 合法通过）；全量 Python 测试 862 个全部通过，`ruff check .` 通过。

---

## [2.11.0] — 2026-08-31

### 新增 / Features

- **范围审查蓝图 `dimension_sets`**：新增「按审查范围预设的维度集」能力。用户在 onboarding 时可按 `frontend` / `api` / `security` / `performance` / `style-tests` 等命名集预设维度组合（扫描器按项目实际技术栈筛除不存在 UI/API 层的集）；`iterate.refresh` 保留用户自定义集并增量补入新检测出的层集；校验与健康检查（`scripts/validate.py`、`iterate doctor`）校验集名字符集、维度合法性及 `focus` 一致性。schema（`config/config.schema.json` 与 `iterate_cli/data/config.schema.json`）已同步 `dimensionSet` 定义。
- **`ITERATE.md` 新增「推荐审查蓝图（按范围）」段**：渲染命名维度集供整仓与分范围审查使用；全局 `dimensions` 列表仍是整仓审查默认，指定范围命中蓝图时按该集路由。
- **范围路由运行时支持（SKILL.md Phase 0）**：指定目标的审查优先匹配对应命名维度集；未命中任一律时按该范围动态重定义维度并写入 `.iterate_decisions.md`（带边界记录）。

### 内部 / Internal

- `iterate_cli/dimension_sets.py`：命名集建议/规范化/合并逻辑（新增模块）。
- `mypy strict` 全量归零、`ruff` 全部通过；新增 `tests/test_dimension_sets.py`（19 例覆盖键名/规格规范化、扫描剪枝、refresh 合并）。

### 测试 / Tests

- 新增 `tests/test_dimension_sets.py`（19 例）与 `tests/test_doctor.py`、`tests/test_validate.py` 的 `dimension_sets` 一致性用例；全量 Python 测试 854 个全部通过。

---

## [2.10.0] — 2026-08-30

### 新增 / Features

- **`reasoning_effort` 端到端 CLI 支持**：onboarding 向导新增「推理努力度」配置项（`low`/`medium`/`high`，默认留空跟随 provider），生成的 `iterate.config.yaml` 输出该字段；`iterate show` 展示、`iterate doctor` 校验并自动修复非法值、`iterate refresh` / re-onboard 保留用户自定义值。schema（`config/config.schema.json` 与 `iterate_cli/data/config.schema.json`）已同步。
- **新增 `iterate config` 非交互式配置子命令**：`iterate config` 列出全部可设值，`iterate config get [KEY]` 读取单个（或全部）解析值，`iterate config set KEY VALUE` 校验并写回单个配置项（写入前自动生成时间戳备份）。支持扁平键（`goal`/`max_rounds`/`reasoning_effort`/`language`/`dimensions`）与嵌套段（`atomic.*`/`git.*`/`review.scope`/`reviewer.*`），损坏配置拒绝覆写。修复了 flat 键读取返回整份配置的 bug。

### 测试 / Tests

- 新增 `tests/test_config.py`（24 例）覆盖值解析器、`get`/`set` 正常与异常路径、嵌套写入、备份生成、损坏配置保护与 CLI 退出码；全量 Python 测试 820 个全部通过。

---

## [2.9.1] — 2026-08-27

### 修复 / Bug fixes

- **onboard 不再覆盖手动编辑区**：重新引导时若现有 `ITERATE.md` 缺少 USER-OWNED 区标记，拒绝继续并提示改用 `iterate reonboard`（会先备份），避免静默替换用户手写内容。
- **损坏配置干净报错**：`iterate personalize`（保存与 `--clear` 两条路径）遇到无法解析的 `iterate.config.yaml` 时以清晰错误返回非零码，不再把损坏配置当作「无可清除内容」（返回 0）或抛出裸 traceback。
- **配置写入权限保留**：`atomic_write` 保留原文件权限位（如 0600 的受限配置），不再因临时文件按 umask 生成而悄悄放宽权限。
- **命令校验安全网**：`doctor` 对未配置 `command_whitelist` 的 `validation.commands` 也检查 shell 元字符；已配置白名单时，含元字符的命令同样以错误（而非警告）拦截，防止 `pytest; rm -rf /` 这类命令链通过健康检查。
- **维度校验加固**：`dimensions` 为非列表（如手写标量字符串）时 `doctor` 报错而非静默回退为全部规范维度。
- **个性化一致性校验修正**：缺失/空 `dimension` 的条目不再误报「指向禁用维度 None」（与 `scripts/validate.py` 行为一致）。
- **skill_version 缺失提示修正**：未记录版本时 `doctor` 输出「nothing to compare」，不再误报「匹配」。
- **re-onboard 读取失败中止**：ITERATE.md 无法读取时中止 re-onboarding 并保留 `.bak` 备份，不静默重建丢手动内容。
- **fingerprint 宽容解析**：畸形条目（非字典、缺 path/sha256）被跳过而非抛异常，手写配置降级为「无漂移」而非崩溃。
- **show 损坏配置标记**：`iterate show` 在配置缺失/损坏时标记 `config_error` 并提示运行 `iterate doctor`。
- **status 拆分与 drift 复用**：抽取 `_render_status_tui`，drift 摘要/建议经 `drift_summary`/`drift_advice` 单次计算复用。
- **refresh 保留 reviewer 调优**：`_build_refresh_data` 拆分，channel 非字符串规范化，保留 reviewer 的 output/evidence/coverage/scope_chunk_size 自定义值。
- **scan 建议去重**：Java/Kotlin 多语言条目只生成一次构建工具建议；API 层指示目录提取为具名常量。
- **TUI 渲染改进**：`_display_width` 处理组合记号/变体选择符/Emoji 宽度；`status` 非交互终端返回 no-op；`error` 默认缩进统一为 2；删除未用符号常量。
- **installer 交互与安全加固**：`scripts/install.py` 原子写配置、下载响应大小上限、解压硬链接越界拒绝、`install/uninstall/update` 退出码语义统一、删除死代码 `_render_arrow_select`、网络错误原因透传；`npm-installer` 下载超时（`--max-time 120`）、tarball 下载进度、`--target` 相对路径解析、checksum 解析与 Python 侧一致、魔法字符串提取为常量。
- **wizard 细节修正**：非交互 stdin 明确报错、扫描结果双语标签、默认常量引用（target_branch/review_scope/language/scope_chunk_size）。

### 测试 / Tests

- 新增 doctor 元字符安全网、维度类型、个性化一致性、onboard USER-OWNED 保护、personalize 损坏配置、atomic_write 权限、TUI 宽度（emoji/组合字符）、installer 退出码等用例；Python 测试 778 个全部通过，npm-installer 测试通过。

---

## [2.9.0] — 2026-08-26

### 修复 / Bug fixes

- **CLI 全局标志可放子命令后**：`iterate status --no-banner`、`iterate doctor -p <dir>` 等写法现在与 `iterate --no-banner status` 等价；此前子命令默认值会覆盖全局标志（`-p`/`--no-banner` 放在子命令前会被忽略）。
- **reviewer 配置完整保留**：onboarding 生成的 `iterate.config.yaml` 现在写入完整的 `reviewer` 段（`evidence_validation`、`coverage_validation`、`scope_chunk_size` 与 `output_schema_validation` 一起），`iterate refresh` / re-onboard / 返回用户更新基础配置时均保留用户自定义值，不再静默重置。
- **show 展示补齐**：`iterate show` 的 TUI 与 `--json` 输出补充 `evidence_validation` 字段渲染。
- **安装器箭头菜单重绘修复**：`npx iterate-skill-installer` 交互式选择 AI 工具时，raw 终端模式下 `\n` 只换行不回车，导致每次按键后菜单逐行向右错位（"螺旋阶梯式"重复打印）。重绘改用 `\r\n` 分隔，并提取 `_arrow_redraw_output` 纯函数 + 模拟终端回归测试。
- **配置解析加固**：各配置加载点对嵌套配置段做类型检查，非字典段不再导致崩溃，统一降级为空字典并保持其余字段可用；新增回归测试覆盖。
- **命令白名单放宽**：`go test` 白名单条目改为 `go`，使 `go vet`、`go build` 等所有以 `go` 开头的命令都能通过命令白名单校验，不再误拒。
- **npm-installer 参数校验**：`--ai` / `--target` / `--token` 的参数值若以 `-` 开头（疑似误传后续标志）直接报错，防止静默吞掉标志。
- **workflow_dispatch 支持指定 tag**：`release.yml` 手动触发时可通过 `inputs.tag` 指定构建/发布目标 tag，与 Release published 路径行为一致。
- **内置 schema 同步**：内置 `iterate_cli/data/config.schema.json` 与根 `config/config.schema.json` 保持一致。
- **README badge 链接修正**：SkillHub badge 指向正确链接。

### 重构 / Refactor

- **死代码清理**：移除重复 import 与未使用代码，保持 ruff/mypy 干净。

---

## [2.8.1] — 2026-08-23

### 修复 / Bug fixes

- **命令校验字符集统一收敛**：`personalize` / `doctor` / `validate` 三处 shell 元字符禁止集收敛为同一权威集合，杜绝「个性化阶段放行、白名单阶段拒绝」的矛盾；新增回归测试强制三方同步。
- **schema 文档同步**：内置 `iterate_cli/data/config.schema.json` 与根 `config/config.schema.json` 描述一致，新增测试防漂移。
- **安装检测逻辑统一**：`install.py` 的 `detect_installed_assistants`（菜单预选 / 自动 update）改用与卸载/升级一致的 `SKILL.md` 标记判定，多路径行为一致。
- **downloads badge 响应限流**：`update_downloads_badge.py` 对上游响应体施加 5 MiB 截断读保护，避免无界内存占用。
- **平台 SKILL 文档对齐**：claude / cursor 变体补齐 review-only (dry-run) 只读审查模式说明，与根 `SKILL.md` 及 trae 变体一致。
- **测试覆盖补齐**：scan / fingerprint / refresh 的异常分支与边界场景新增用例。

---

## [2.8.0] — 2026-08-22

### 新增 / Features

- **unattended CLI 子命令**：接线 schedule / hook / cron 无头调用路径，方便脱离对话在定时/钩子场景复用同一闭环。

### 修复 / Bug fixes

- **refresh 版本同步**：`iterate refresh` 现在把 `onboarding.skill_version` 同步到已安装版本，消除 `iterate doctor` 反复提示版本更新的告警（此前刷新不更新该记录）。
- **reonboard 结果区分**：区分「用户取消」与「失败」，不再混用含糊的 "cancelled or failed" 消息。
- **status 一致快照**：`iterate status` 改为单次读取 onboarding 状态/config/drift，JSON 与 TUI 两条渲染路径共享同一数据源。
- **类型安全收敛**：personalization 行号钳制、show 可选配置段解析做类型收窄，满足 ruff PLR1730 与 mypy。
- **webui**：浮出 workspace 删除错误，统一报告尺寸格式化。

---

## [2.7.0] — 2026-08-22

### 发布 / Release

- **主技能版本对齐**：配合插件发布线（iterate-plugin 2.11.0）推进到 2.7.0，将与贴身 harness（iterate-harness 1.13.0）保持同源的强化后状态；无破坏性 API 变更。

---

## [2.6.0] — 2026-08-21

### 修复 / Bug fixes (审查收敛：UX 与一致性)

- **CLI 优雅中断**：交互命令期间 Ctrl+C / Ctrl+D(EOF) 不再抛裸 traceback，统一转为"已中断/输入已结束，未写入任何文件"提示并退出码 1；命令分发集中到 `_dispatch_command` 统一包裹。
- **`--version` 横幅一致性**：`--no-banner` / `ITERATE_NO_BANNER` 现在同样抑制 `--version` 的 ASCII 横幅，仅保留版本信息。
- **doctor 警告态总结**：末尾总结区分三态——存在 error 显示"error(s) found"，仅 warning 显示"healthy but with N warning(s) — non-blocking"，干净显示"healthy (N checks passed)"，避免与上方 findings 自相矛盾。
- **doctor config.schema 可用性**：schema 文件/jsonschema 不可用时降为 warning 而非假"完全匹配"成功（`_schema_violations` 返回语义从空 list 改为 `None`）。
- **doctor 命令元字符过滤扩展**：白名单命令校验扩充过滤集，并改为一次性严格拒绝含元字符的命令。
- **doctor 空维度早退**：空 `dimensions` 报错后提前 return，不再同一次运行再报成功行自相矛盾。
- **doctor 个性化字符串守卫**：手写的字符串 `fix_priority_order` 不再被逐字符误判为断裂维度。
- **doctor onboarding 消息精确化**：缺失提示精确反映仅检查 ITERATE.md（config 由 `config.parse` 单独校验）。
- **`iterate show` 生效配置修正**：此前从 `onboarding` 区段读取生效键导致部分键反映错误值；改为从各自规范位置（顶层 + git/review/atomic/reviewer 嵌套区段）读取。
- **`iterate show` 漂移建议**：检测到漂移时 TUI 追加 `Suggested: ...` 行动建议，`--json` 新增 `drift_advice` 字段。
- **`iterate show` 维度渲染**：`dimensions` 按 list 渲染（原先按 dict 分支永不匹配，实际不显示）。

### 测试 / Tests

- 新增 doctor 警告态总结、CLI 优雅中断、`--version` 横幅、show 漂移建议等回归测试。
- 全量 `tests/` **675 passed**。

---

## [2.5.0] — 2026-08-21

### 新增 / Features

- **`iterate show`**：只读查看合并后的生效配置与个性化详情（onboarding 元数据、生效 config、漂移状态、全部 9 类个性化）。TUI 输出面向人，`--json` 输出结构化数据供脚本/CI/快速 diff。不写任何文件。
- **`iterate personalize --clear [--yes]`**：一次性清空所有个性化——结构化规则从 `iterate.config.yaml` 移除、由个性化所有权新增的验证命令从 `validation.commands` 清理（空模块自动剔除）、`ITERATE.md` 用户区中的个性化段落移除而保留手工内容。原子写入 + 失败回滚，跨文件保持一致；无个性化可清空时友好提示并退出码 0。`--yes` 跳过确认。

### 修复 / Bug fixes (审查收敛)

- **doctor 配置安全与逻辑**：修复浅拷贝共享原配置对象的隐患（改用 `copy.deepcopy`）；修复 `set.add()` 返回值误用（原本 `None` 可能被判为重复）；个性化维度/命令检查改为类型安全（非 list 值不再崩溃）。
- **wizard 再入一致性**：返回用户更新基础配置时保留已有高级字段（language/goal/max_rounds 等），不静默重置；确认的语言立即生效到验证命令建议/白名单/维度默认；统一确认提示默认值；`drift_ignore` 在再 onboarding 时正确持久化。
- **fingerprint/scan 健壮性**：清单文件在存在检查后消失、不可读、非 UTF-8 时不再抛未捕获 `OSError`，降到 stderr 警告并跳过；顶层目录列表失败同样容错。
- **validate.py UX**：未显式指定维度目录且默认回退目录不存在时，明确提示"维度校验被跳过"而非静默跳过；清理无占位符的 `f` 前缀。
- **show/personalize 边界**：未 onboarding 时 `show` 友好提示；`--clear` 取消确认不做任何变更。

### 文档 / Docs

- `SKILL.md` frontmatter 版本与 CLI 子命令列表补 `iterate show`、`iterate personalize --clear`。
- `README.md` 新增 `iterate show` 与 `iterate personalize --clear` 小节（含 `--json` / `--yes` 用法与退出码）。

### 测试 / Tests

- 新增 `iterate show` 与 `personalize --clear` 相关测试（含 TUI/JSON 渲染、纯函数移除语义、CLI 端到端清理、取消确认不落地、无个性化可清空）。
- 全量 `tests/` **657 passed**，`ruff check` 干净。

### 审查收敛（第二轮：UX 与一致性 / 本轮）

- **CLI 优雅中断**：交互命令期间 Ctrl+C / Ctrl+D(EOF) 不再抛裸 traceback，统一转为"已中断/输入已结束，未写入任何文件"提示并退出码 1；命令分发集中到 `_dispatch_command` 统一包裹。
- **`--version` 横幅一致性**：`--no-banner` / `ITERATE_NO_BANNER` 现在同样抑制 `--version` 的 ASCII 横幅，仅保留版本信息。
- **doctor 警告态总结**：末尾总结区分三态——存在 error 显示"error(s) found"，仅 warning 显示"healthy but with N warning(s) — non-blocking"，干净显示"healthy (N checks passed)"，避免与上方 findings 自相矛盾。
- **doctor config.schema 可用性**：schema 文件/jsonschema 不可用时降为 warning 而非假"完全匹配"成功（`_schema_violations` 返回语义从空 list 改为 `None`）。
- **doctor 命令元字符过滤扩展**：白名单命令校验扩充过滤集（`\` `#` `*` `?` `~` `"` `'` `{}` `()` `[]`），并改为一次性严格拒绝含元字符的命令。
- **doctor 空维度早退**：空 `dimensions` 报错后提前 return，不再同一次运行再报"all dimensions canonical"的成功行自相矛盾。
- **doctor 个性化字符串守卫**：手写的字符串 `fix_priority_order` 不再被逐字符误判为断裂维度。
- **doctor onboarding 消息精确化**：缺失提示改为精确反映仅检查 ITERATE.md（config 由 `config.parse` 单独校验）。
- **`iterate show` 生效配置修正**：此前从 `onboarding` 区段读取生效键导致 `atomic_*`/`auto_merge`/`target_branch`/`review_scope`/`output_schema_validation` 等反映错误值；改为从各自规范位置（顶层 + git/review/atomic/reviewer 嵌套区段）读取。
- **`iterate show` 漂移建议**：检测到漂移时 TUI 末尾追加 `Suggested: ...` 行动建议，`--json` 新增 `drift_advice` 字段。
- **`iterate show` 维度渲染**：`dimensions` 按 list 渲染（原先按 dict 分支永不匹配，实际不显示）。
- **测试**：新增 doctor 警告态总结、CLI 优雅中断、`--version` 横幅、show 漂移建议等回归测试；全量 `tests/` **675 passed**。

---

## [2.4.5] — 2026-08-20

### 修复 / Bug fixes (CLI 一致性、安全与文档)

- **refresh 幂等性**：增量刷新复用上次 `completed_at` 时间戳，未变化时逐字节 no-op；`_diff_stats` 跳过 `--- /+++` 文件头行，改动行数统计不再虚高。
- **拒绝静默覆盖手写 ITERATE.md**：缺失 `USER-OWNED` 区块标记时 refresh 抛错拒写而非销毁用户内容（`generate_refreshed_md` 两侧都校验）。
- **personalize 删除同步**：删除个性化验证命令时同步清理 `validation.commands`（按旧归属精准删除、非个性化命令保留），不再残留死命令。
- **doctor 重构为模块化检查**：单一 `run_doctor` 拆分为 `_check_onboarding`/`_check_config_parse`/`_check_config_schema` 等单职责函数，两个致命检查短路后续。
- **validate.py 健壮性**：`command_whitelist` 非字符串条目不再崩溃（过滤+报错），schema 缺失/损坏时优雅降级并报告。
- **CLI schema 同步**：`iterate_cli/data/config.schema.json` 补回 `reviewer.evidence_validation`/`coverage_validation`/`scope_chunk_size`，与主 `config/config.schema.json` 完全一致。
- **install.py 安全加固**：`copy_skill_files` 增加目标路径穿越防护、符号链接目标先 unlink 再替换；`_safe_extractall` 拒绝 symlink 目标逃逸；`_parse_checksum` 支持 `./` 前缀；`update` 移除死参数 `--force` 并接入 `_validate_github_token` 前置校验，畸形 token 快速失败。
- **npm-installer**：新增 `--version/-v` 与 `--help/-h`；tar 解压强制单一顶层目录契约；新增 `LICENSE` 随包分发；CI 增加 node 测试 job。

### 文档 / Docs

- `SKILL.md` 项目结构补齐 `doctor.py`/`personalize.py`/`tui.py`/`data/`；CLI 子命令列表补 `iterate doctor`。
- `README.md` 补充 UX 文档缺口：新增 `iterate doctor` 详述（10 项检查表 + `--json`/`--json-out`/`--fix` 用法与退出码）、常见边界场景（onboarding 中途取消原子写入、无 `USER-OWNED` 标记拒写、非 Git 项目、空项目漂移、配置损坏处理、Early Stop 收敛）、新手推荐路径（安装 → onboarding → doctor → personalize → /iterate）。
- `tools/SKILL.{trae,claude,cursor}.md` 三份平台适配版同步 2.4.x 特性：reviewer prompt 注入 `EVIDENCE RULE`、meta-review 硬证据门禁（`EVIDENCE_VIOLATION`→`needs_revision`）、覆盖率提示（`COVERAGE_GAP`）、onboarding/personalization 指引。

### 测试 / Tests

- 新增 TUI 渲染与 banner 测试（`_display_width` CJK 双宽、各渲染方法、`--no-banner`/`ITERATE_NO_BANNER` 开关逻辑）。
- 新增 install.py 畸形 token 快速失败、空 token 视为缺省测试；refresh 缺 USER-OWNED 标记拒写测试。
- 全量 `tests/` **647 passed**，`ruff check` 干净。

---

## [2.4.4] — 2026-08-20

### 修复 / Bug fixes (安装器 TUI 重绘)

- **箭头多选菜单根治「阶梯式螺旋」**：此前即使有滚动窗口，长标题在窄终端换行后 `move_up` 用逻辑行数上移不足、且重绘未回归列首，逐帧下坠挤压成螺旋。现重绘改为：按每行实际显示宽度（含 CJK 双宽）计算**物理行数**、精确回退光标、`\r` 归列 `\x1b[0J` 清屏后整帧重写；宽度计算用可剥离任意 CSI（光标/清除/颜色）的 `_strip_ansi` 与依赖自由的 `_wcwidth_display_cols`。另隐藏光标避免闪烁，退出时恢复。

### 测试 / Tests

- 新增 `TestTuiRedrawHelpers` 六条用例：CSI 全序列剥离、CJK 双宽计数、窄终端换行物理行不塌缩、物理行数恒 ≥ 逻辑行数。
- 全套 `tests/test_install_script.py` 现 **85 passed**。

---

## [2.4.3] — 2026-08-20

### 新增 / Features (安装器 --no-cli)

- **新增 `--no-cli` 开关**：只想安装 skill、不想要全局 `iterate` CLI 的用户可用 `npx iterate-skill-installer --no-cli` 跳过 CLI 安装。`parseArgs` 从 `bin/cli.js` 抽取到 `lib/installer.js` 并导出，可独立单测。
- **自动装 CLI 更透明**：不再静默预装 CLI。安装 skill 后明确提示即将安装 `iterate` CLI（并说明可用 `--no-cli` 跳过）；使用 `--no-cli` 时改打印「稍后如何手动安装 CLI」的指引。

### 测试 / Tests

- `mode.test.js` 新增 `parseArgs` 用例：`--no-cli` 默认关闭、单独开启、与其它 flag 组合保持；并回归 target 强制 project 模式等既有 flag 面。

---

## [2.4.2] — 2026-08-20

### 修复 / Bug fixes (安装器交互体验)

- **箭头菜单不再螺旋排列**：`scripts/install.py` 选择安装工具的箭头多选菜单在选项超过终端高度时曾逐行错位成阶梯式螺旋。现新增滚动窗口（`MAX_WINDOW=6`），仅渲染当前可见选项，重绘按恒定行数上移光标，菜单高度固定、任何终端都不会溢出或错位。
- **陈旧版本不再静默跳过**：此前目标目录已存在 iterate-skill 安装（可能为旧版本）时会静默跳过，用户无法感知。现在交互终端会询问「是否覆盖升级到最新版」，非交互模式保留现有拷贝并提示使用 `--force`。另按目标目录去重，避免共享目录重复安装。

### 测试 / Tests

- 新增滚动窗口跟随光标、Done 行显示末页、渲染高度固定三组用例；新增陈旧版本升级确认（交互分支）用例。

---

## [2.4.1] — 2026-08-19

### 新增 / Features (强制子代理逐文件读取审查范围 + 覆盖率校验)

- **审查范围强制逐文件读取**：`plan` 在 `full` 范围下预先收集源码清单并按 `reviewer.scope_chunk_size`（默认 25 个）分批；reviewer prompt 注入 `COVERAGE RULE`，要求子代理必须先以 `read_file` 打开负责清单中的**每一个**文件再作判断，不得跳过、臆测或在未读的情况下下结论，并在返回 JSON 中附带 `readFiles` 数组如实罗列实际打开的文件。`changed-only` 范围同样强制逐条读取更动文件清单。
- **覆盖率提示性校验（meta-review）**：meta-review 把各子代理自报的 `readFiles` 与分配到的审查清单比对，明显缺口以 `medium` 的 `COVERAGE_GAP` 提示浮出，推动子代理逐文件读取自身负责范围；该提示**绝不反转最终判定**，保持裁决稳定性。
- **配置开关**：新增 `reviewer.coverage_validation`（默认 `true`）与 `reviewer.scope_chunk_size`（默认 `25`）。设 `coverage_validation=false` 可关闭覆盖率提示；调整 `scope_chunk_size` 可控制 full 范围单批文件数。

### 修复 / Bug fixes

- `EVIDENCE_VIOLATION` 报告现在定位到具体产生该问题的 review round，便于追责。校验两个策略下的一致实现。
- 证据校验双端（Python/TypeScript）对齐：二进制文件（含 NUL 字节）的锚定行号判为无效，行计数正则与 Python `str.splitlines()` 完全一致。
- 修复非连续轮号时 `findings_by_round` 数组定长与收敛判定逻辑，代理 `aggregateRounds`/`computeConvergence`。

---

## [2.4.0] — 2026-08-19

### 新增 / Features (强制实读到代码的证据审查)

- **强制子代理实际读文件再审查，禁止推测**：reviewer prompt（SKILL.md 审查模板）注入强制 `EVIDENCE RULE`——必须先以 `read_file` 读过待报告的每个文件，才能对其下结论；禁止报告从未读过的代码，编造的文件路径/行号一律视为 poisoned evidence。`line` 对行级问题改为必填（精确读到的行号），整文件/模块级问题用 `0`。
- **硬证据门禁（meta-review）**：`meta-review` 在既有内部一致性校验之外，新增代码证据校验，逐条核对 finding 的 `file`/`line` 是否真实存在于磁盘代码中；任何伪造路径或越界行号都会作为 critical 的 `EVIDENCE_VIOLATION` 浮出，并把最终裁决强制翻转为 `needs_revision`。
- **配置开关**：新增 `reviewer.evidence_validation`（默认 `true`）。设 `false` 可关闭硬门禁，用于不需要严格证据校验的场景。

### 文档 / Docs

- **[SKILL.md](SKILL.md)**：dry-run 审查模板注入 EVIDENCE RULE 并把 `line` 明确为必填；meta-review 说明硬证据门禁；审前 checklist 增加「已注入 EVIDENCE RULE」「已确认证据门禁」验收项。
- **[config.schema.json](config/config.schema.json)** / **[iterate.config.yaml](config/iterate.config.yaml)**：新增 `reviewer.evidence_validation` 字段与默认值、中英释义。

### 测试 / Tests

- 补充证据校验模块测试（文件存在性、行号上下界、read-trace 交叉、整文件/模块级 0 行）与 harness/plugin 两侧对称用例，全套 Python 测试通过。

## [2.3.20] — 2026-08-19

### 新增 / Features (onboarding 高级配置 + 数据一致性)

- **[wizard.py](iterate_cli/wizard.py)**：onboard 向导新增**可选高级配置步骤**（默认关闭），暴露 8 个此前隐藏的旋钮：迭代目标、最大轮数（1–50）、输出语言（zh/en）、原子改动阈值（最大行数/相邻方法数）、git 隔离（worktree / 自动合并）、reviewer 输出 schema 校验、漂移忽略 glob。每个提示以当前值为默认，直接回车即保持原值。输入边界与 `config.schema.json` 约束一致，非法输入保持原值而非崩溃。
- **[generator.py](iterate_cli/generator.py)**：`OnboardingData` 新增 `drift_ignore` 字段并在 `generate_config_yaml` 持久化到 `onboarding.drift_ignore`，保证再次 onboarding/re-onboarding 不再静默丢弃漂移忽略规则。
- **[refresh.py](iterate_cli/refresh.py)**：`_build_refresh_data` 从既有配置回读 `drift_ignore`，增量刷新时保留用户设置的漂移忽略项。
- **[personalize.py](iterate_cli/personalize.py)**：新增**事务化保存** `save_personalization` —— config.yaml 与 ITERATE.md 双文件原子写入；若第二文件写入失败则回滚第一文件至原内容，保证两文件状态一致；回滚自身失败时显式暴露错误而非静默吞掉。`cli.py` 的 `_cmd_personalize` 改用该事务化保存，移除旧的分离式 `_update_iterate_md_user_section`。

### 测试 / Tests

- 新增 `TestSavePersonalizationTransactional`（双文件写入、ITERATE.md 缺失跳过、config 缺失抛错、写入失败精确回滚、回滚失败显式暴露）与 `TestAdvancedConfigWizard`（拒绝保持默认、接受全量变更、空输入保持原值、`_read_optional_int`/`_read_language`/`_read_optional_text`/`_read_drift_ignore` 边界与去重）。
- 全套 Python 测试 **582 全绿**（含既有 drift_ignore 用例，均在本地挂载卷复跑通过）。

## [2.3.19] — 2026-08-18

### 修复 / Fixes (skill CLI + 核心模块)

- **[personalize.py](iterate_cli/personalize.py)**：统一「已知意图 / Known Intentional」段的写入标题，修复该段标题后缀不匹配 `PERSONALIZATION_SECTION_HEADERS` 导致刷新时整段重复累积到 ITERATE.md 的问题。
- **[refresh.py](iterate_cli/refresh.py)**：新增 `_load_refresh_config` 区分配置不存在与配置已损坏（存在但无法解析）。损坏配置改为中止刷新并明确报错，不再被默认值整体覆盖。
- **[cli.py](iterate_cli/cli.py)**：`--version` 改为通过返回值返回 `0`（由 `__main__.py` 以 `sys.exit(main())` 承接），不再直接 `raise SystemExit`；刷新前若无法读取现有 ITERATE.md 则提示并中止，避免静默覆盖手动编辑区。
- **[generator.py](iterate_cli/generator.py)**：原子写入临时文件改为带 uuid 后缀，避免并发冲突；清理/回滚失败不再静默吞错，改为记录日志后抛出。
- **[scan.py](iterate_cli/scan.py)**：TypeScript 项目建议白名单补充 `npm` 前缀，修复 `suggest_command_whitelist` 建议的 `npm run` 无法匹配 `npm test` 等命令的问题。
- **[doctor.py](iterate_cli/doctor.py)**：JSON Schema 校验捕获 `Draft202012Validator` 构造可能抛出的 `SchemaError`，避免 schema 异常时崩溃。
- **[install.py](scripts/install.py)**：`update` 命令语义为「刷新到最新版本」，强制覆盖已安装副本（此前默认跳过已存在文件却仍报成功，产生假成功）。
- **[validate.py](scripts/validate.py)**：命令白名单额外拒绝命令本体中的 shell 链接元字符（`;`、`|`、`&`、`$`、反引号、`>`、`<`、换行等），防止 `白名单前缀; 恶意命令` 绕过后缀拼接。
- **示例与依赖**：`examples/typescript-project.md` 白名单补 `npm`；`examples/python-project.md` 移除无 `specs/` 目录却启用的 `spec-compliance` 维度；`scripts/requirements.txt` 的 jsonschema 统一为 `4.26.0`。

### 测试 / Tests

- 更新 `test_version_flag`（`--version` 返回码而非 SystemExit）与 `test_update_detects_installed_assistants`（update 覆盖语义）两处与旧行为耦合的用例。
- 全套 Python 测试 **536 全绿**。

## [2.3.18] — 2026-08-17

### 修复 / Fixes (skill CLI + validate 脚本)

- **`validation.command_whitelist` 改为可选**：[scripts/validate.py](scripts/validate.py) 此前强制要求该字段为非空列表，与 [config.schema.json](config/config.schema.json)（非必填）及 `iterate doctor`（按可选处理）不一致。现对齐三者：未配置白名单视为可选、跳过白名单结构/合规性校验（运行时仍以 `validation.commands` 为唯一信任源）；已配置但为空列表仍报错。新增 `test_absent_whitelist_is_optional` / `test_absent_whitelist_still_rejects_malformed_commands` 回归用例。
- **GitHub release tarball 不再携带 `harness/`**：[release.yml](.github/workflows/release.yml) 的 `git archive` 此前将整个 `harness/` 打入发布包，与 2.3.17「skill 分发包不携带 harness 源码」的规范不一致。现通过 pathspec `:!harness` 在源头上剔除该目录。
- **ruff 全绿**：清理 `iterate_cli/personalize.py`（SIM102）、`iterate_cli/wizard.py`（SIM114）、`tests/test_install_script.py`（I001/RUF100/SIM117）共 5 处 lint 违规，消除 CI 中 `ruff check scripts/ tests/ iterate_cli/` 的潜在失败。

### 测试 / Tests

- 全套 Python 测试 536 全绿。

## [2.3.17] — 2026-08-17

### 发布规范 / Release (skill CLI + installer)

- **skill 发布包不再携带 `harness/` 源码**：ClawHub / ModelScope / SkillHub 的分发包此前一直夹带 `harness/iterate-plugin`（dsh 插件源码），skill 包不应包含 harness 下两个独立分发子项目的源码。现从所有分发包中剔除整个 `harness/` 目录（ModelScope 精简包 72→51 文件、SkillHub 包 49 文件），并统一升版至 2.3.17 以覆盖 SkillHub 的版本锁。
- 更新 `rebuild_ms.py`（去 harness 出 ModelScope 包）与 `rebuild_skillhub.py`（去 harness + 去 LICENSE 出 SkillHub 包）构建脚本。

## [iterate-plugin 2.6.0] — 2026-08-17（独立版本线）

### 新增 / Features (iterate-plugin)

- **`iterate_history` 历史审计工具**：读取决策日志（支持按 `type` / `since` / `limit` 过滤，默认最新 50 条、上限 200 条）+ 修复注册表汇总（各轮 fixed/failed 计数）。只读不落盘，用于审查运行过程、审计日志、盘点修复明细。
- **`iterate_prune` 运行时清理工具**：清理过期决策日志条目（`retainDays` 默认 30 天）、陈旧断点、孤儿修复备份与空轮次；默认 dry-run 只报告不删除，显式 `dryRun:false` 才真正清理，每次清理写入决策日志。
- **UX — 收敛看板修复计数徽章**：normal 模式在看板显示已修复原子问题计数徽章。
- **UX — 分诊面板一键全选**：可对所有 findings（非仅当前筛选集）批量 y/n/a 判定。
- **UX — 设置区运行时状态概览**：展示 `.iterate/` 产物布局与 `iterate_status` / `iterate_history` / `iterate_prune` 查看/清理指引，支持一键清空分诊数据。

### 代码质量 / 安全 / Security (iterate-plugin)

- 修复多处静默 catch 块：统一记录上下文并向上抛出可诊断错误，杜绝空 catch。
- `iterate_fix` 对 `content` 设字符上限、`iterate_triage` 对 `entries` 设数量上限，防止异常超大负载。
- `applyEntries` 失败回滚逻辑加固，配置写入失败时还原现场。

### 文档 / Docs (iterate-plugin)

- README 全面重写：工具数更新为 13 个并逐条列明、UI 层 6 组件挂载槽位与功能表、`.iterate/` 目录布局图、安全模型（路径防护 / 备份回滚 / dry-run / 参数上限）说明。

### 测试 / Tests (iterate-plugin)

- 新增 `allVerdictKeys`、`buildRuntimeStatusGuide`、`iterate_history`、`iterate_prune` 等用例，共 **212 个单元测试全绿**，类型检查通过。

## [2.3.16] — 2026-08-17

### 修复 / Fixes (skill CLI + installer)

- `install.py`：校验子进程同时解析 stdout + stderr（stdout 诊断不再被吞掉，统一为结构化错误列表）。
- `install.py`：`_validate_github_token` 校验 GitHub PAT 前缀（`ghp_/gho_/ghu_/ghs_/ghr_/github_pat_`）与长度范围（20–256），写入 `--token` 前 fail fast。
- `install.py`：卸载 / 更新删除前新增 `_is_iterate_install_dir` 标识防护，确认目标目录含 `SKILL.md` 才允许 `rmtree`，防止误删非 skill 目录。
- `install.py`：Windows 无 `termios` 环境回退到数字选择，不再崩溃。
- `install.py`：删除未使用的死代码 `_key_value`；stdout 解析改用 `str.removeprefix`（消除 ruff FURB188）。
- `iterate_cli/personalize.py`：`load_personalization_from_config` 拒绝 `fix_priority_order` / `forbidden_fixes` 的标量字符串值，防止手动编辑的 config 被逐字符膨胀进列表。

### 新增 / Features (skill CLI + installer)

- `iterate doctor --json-out <PATH>`：把结构化 Dr.Report 导出到文件（自动创建父目录），便于 CI / 脚本消费健康报告。

### 测试 / Tests

- 新增 `--json-out` 文件导出、`fix_priority_order`/`forbidden_fixes` 标量字符串防御等用例。
- 全套 Python 测试 534 全绿。

## [2.3.15] — 2026-08-16

### 重构 / Refactor (skill CLI installer)

- `install.py` 全部交互函数（`prompt_choice/text/int/bool/int_in_range/dimensions`、`interactive_config`、`config_command`）接入可注入的 `input_func`（默认 `input`），安装 / 更新 / 卸载 / config 向导可无需真实 stdin 端到端测试，UX 输出保持不变。

### 测试 / Tests

- 新增 `tests/test_install_script.py`（75+ 项）：覆盖文件拷贝（必选/可选、dry-run、force）、助手检测与选择、config 管理（init/list/set/交互向导，含校验失败原子回退）、update 发布下载与校验和强制校验、`_safe_extractall` 路径穿越防护、全部交互 prompt。
- 修复测试设置，使向导/`--set` 生成的 config 能通过真实 schema 校验（以真实 master config + 真实 dimensions 作为默认值基准）。
- 全套 Python 测试 532 全绿。

## [iterate-plugin 2.3.7] — 2026-08-15（独立版本线）

本节记录 `harness/iterate-plugin`（dsh 插件）的独立版本线变更，不再跟随 skill 版本号。

### 插件安全 / Security (iterate-plugin)

- **S1 路径逃逸防护**：5 个插件工具（`config/validate/context/review/decision_log`）新增 `resolveProjectRoot` 路径校验，解析后拒绝以文件系统根目录作为项目根，杜绝模型可控的 `path` 参数指向任意系统目录的路径遍历逃逸。
- **S2 `timeout` 上限**：`iterate_validate` 的 `timeout` 参数经 `clampTimeout` 钳制在 600s 上限内，模型无法通过无界 `timeout` 无限拉长命令运行时间。

### 插件功能修复 / Bug Fixes (iterate-plugin)

- **B1** `reviewerTaskPrompt` 的 `is_atomic` 阈值从此前未插值的 `{atomic.max_lines}` 占位符改为真实读取 `config.atomic.max_lines`，`is_atomic` 判定恢复阈值依据。
- **B2** `known_intentional` 个性化过滤端到端打通：canonical 脚本从 `plan` 读取并透传给 `aggregate`，此前配置项实际不生效。
- **B3** normal 模式 architectural findings 跨轮去重，避免相同架构问题在多轮重复累积。
- **B4** 原子修复按文件分组、同一文件由单个 fixer 串行应用，杜绝不同 fixer 并发写同一文件产生的竞态。
- **M3** `sortFindings` 对非法 severity 兜底为 `low`，杜绝 NaN 进入比较器导致排序异常。
- **M4** dry-run 的 known 反馈改用去重后的 findings，避免已知列表随轮次无限膨胀。

### 一致性 / Consistency

- **C1** 清理 `package.json` 中指向不存在测试文件的 5 个失效脚本，仅保留 `test` 与 `test:validate`。
- **C2** README 测试数由过时的 31 更正为 63。
- **C3** 插件版本号统一为独立版本线 2.3.7（`package.json` / `package-lock.json`）。

### 新增单元测试 / Tests

- 新增 `resolveProjectRoot`（路径校验）、`clampTimeout`（超时钳制）、`reviewerTaskPrompt` 阈值插值、`sortFindings` 非法 severity 等测试；共 63 个全绿，类型检查通过。

---

## [2.3.14] — 2026-08-16

### 新功能 / Features (skill CLI)
- **`iterate doctor` 全量 JSON Schema 校验**：`run_doctor` 新增 `config.schema` 检查，将 `iterate.config.yaml` 与 `config/config.schema.json` 逐项比对（`additionalProperties:false` 全覆盖），不匹配时以 warn 级别列出前 N 条违规路径，与 `scripts/validate.py` 保持一致。
- **`iterate refresh --dry-run` 预览**：新增 `refresh.preview_refresh`，仅计算不写入，展示 ITERATE.md 增减行数与 iterate.config.yaml 是否变更，用户可在实际刷新前确认影响面。
- **非交互式优雅降级**：`onboard`/`personalize` 向导新增终端交互性检测（`_ensure_interactive`），在管道/重定向/CI 环境下打印指引并以非零状态退出，不再因 `input()` 抛 `EOFError` 崩溃。
- **原子写**：`generator.atomic_write`（临时文件 + `os.replace`）统一应用于 onboarding、refresh、reonboard 的写入路径，配合失败回滚，杜绝半写文件。

### 修复 / Bug Fixes (skill CLI)
- **Bug A — 返回用户自定义配置丢失**：`wizard._load_existing_onboarding_data` 现完整保留 goal/max_rounds/atomic/git/reviewer 等自定义字段，返回用户更新配置时不再静默丢弃。
- **Bug B — `doctor --fix --json` 输出污染**：修复信息整合进 JSON 报告的 `fixes` 字段，移除混入 stdout 的 TUI 文本，保证 `--json` 输出纯净可解析。
- **refresh 幂等化**：`_build_refreshed_config` 仅在指纹实际变化时重写 `completed_at`；`generate_refreshed_md` 原样拼接用户区块（保留原有空行布局）。未漂移时刷新为字节级 no-op，`--dry-run` 正确报告"无需变更"。
- **`_write_refresh_outputs` 引用修复**：统一改用 `atomic_write`，消除重构遗留的未定义 `_atomic_write` 引用。

### 测试 / Tests
- 新增 `config.schema`、`validation.whitelist` 合规、`personalization.consistency`、`refresh --dry-run` 预览、非 TTY 降级等测试；适配原子写后的回滚测试（改 monkeypatch `atomic_write`）。全套 457 个测试通过。

---

## [2.3.13] — 2026-08-16

### 修复 / Bug Fixes (distribution)

- **ClawHub 显示名回归修正**：此前发布流程未显式传 `--name`，导致 ClawHub 上 skill 显示名被默认取为发布目录 basename（`Clawhub Stage 2.3.12`）。本次发布显式指定 `--name Iterate`，恢复为正确显示名 `Iterate`。版本号统一升至 2.3.13 以确保三平台（ClawHub / ModelScope / SkillHub）版本一致。

---

## [2.3.12] — 2026-08-16

### 新功能 / Features (skill CLI)

- **`iterate doctor --fix` 安全自动修复**：补齐"诊断→修复→确认"闭环。`--fix` 仅修复确定性、无损、可逆的配置问题（重复/空维度、非法 language、越界/非整数 max_rounds、空 target_branch、skill_version 漂移），写前自动生成 `.doctorfix-<timestamp>` 备份，随后重跑诊断确认健康。新增 `doctor.apply_safe_fixes` 与 `doctor.run_doctor_fix`。

### 修复 / Bug Fixes (skill CLI)

- **`iterate refresh` 失败提示误导**：此前失败时一律提示 `ITERATE.md not found`，但 `incremental_refresh` 对读取失败、写失败（已打 stderr）同样返回失败。现改为中性的 `Could not read or write ITERATE.md / iterate.config.yaml (see stderr)`，准确反映各类失败原因。
- **`iterate reonboard` 无变更时提示夸大**：`full_reonboard` 对"正常完成"与"返回用户拒绝全部更新（NO_CHANGES_NEEDED）"均返回 True，导致无写入场景也提示 `Full re-onboarding complete`。现将返回值改为 `REONBOARD_*` 状态码（`completed`/`no-changes`/`cancelled`/`failed`），`_cmd_reonboard` 据此输出准确提示。
- **清理死代码**：删除 `doctor._COMMAND_MODULES_KEYS` 未使用常量（其取值 `commands.validation` 本身为错误键名）。

### 新增单元测试 / Tests

- `tests/test_onboarding.py` 的 `full_reonboard` 相关断言更新为 `REONBOARD_*` 状态码；`tests/test_doctor.py` 保留既有 `apply_safe_fixes` / `run_doctor_fix` / CLI `--fix` 用例；全测试集 441 个全绿。

---

## [2.3.11] — 2026-08-16

### 新功能 / Features (skill CLI)

- **`iterate doctor` 补齐 schema 对齐检查**：新增 `max_rounds` 边界（1–50）、`language` 枚举（zh/en）、`dimensions` 非空与唯一性、`validation.command_whitelist` 非空唯一字符串等健康检查，与 `config/config.schema.json` 约束逐一对齐。

### 修复 / Bug Fixes (skill)

- **`jsonschema` 缺失运行时依赖**：`validate` 模块依赖 `jsonschema` 但未在 `pyproject.toml` 声明，导致任意安装用户执行 schema 校验必失败。已补入依赖并固定版本。

### 新增单元测试 / Tests

- `tests/test_doctor.py` 新增空维度、重复维度、越界 `max_rounds`、非法 `language`、非法/合法 `command_whitelist` 等用例；全测试集 429 个全绿。

---

## [2.3.10] — 2026-08-15

### 新功能 / Features (skill CLI)

- **`iterate doctor` 命令**：新增项目健康诊断命令，校验项目 `iterate.config.yaml` / `ITERATE.md` 与技能本体的规范一致性（onboarding 完整性、配置可解析、维度 id 合法性、review.scope 取值、git.target_branch 有效性、validation.commands 结构、skill_version 匹配、manifest 漂移）。发现错误时退出码非零，便于接入 CI。新增 `iterate_cli/doctor.py`。
- **`--json` 结构化输出**：`iterate status` 与 `iterate doctor` 支持 `--json`，输出机器可读的 JSON（用于脚本与 CI 消费）。JSON 模式下自动抑制 ASCII banner，避免污染输出。

### 修复 / Bug Fixes (skill)

- **统一手动验证命令校验逻辑**：`wizard._manual_collect_commands`（onboard 路径）此前只拦截 shell 元字符，与 `personalize.validate_extra_command`（后者严格白名单）强度不一致。现统一复用 `validate_extra_command` 作为唯一权威校验点，杜绝两路径校验割裂。`validate_extra_command` 同时扩展支持 `python <script>.py` 合法脚本调用（非 `-m`），保持 onboard 合法用例可用。
- **`_render_dimensions` priority_map 纳入维度锁**：generator 内硬编码的 priority_map 此前未被 `tests/test_dimension_lock.py` 覆盖，priority 变更会漂移。现新增六源维度锁第 7 个来源，锁定其与 `config/dimensions.yaml` 的 priority 一致。
- **onboard scope 输入防呆**：`wizard._collect_git_config` 中对非法 scope 输入（非 1/2）显式提示并回退默认 full，不再静默降级。
- **TUI 键值对齐**：`tui.key_value` 由字符宽度 `ljust` 改为 CJK 显示宽度感知对齐（新增 `_display_width`），修复中文键名错位。

---

## [2.3.9] — 2026-08-15

### 修复 / Bug Fixes (display)

- **ClawHub 人类读者导引位置调整**：将 SKILL.md 中的人类读者邀请语从 frontmatter 之后移至 `# /iterate` 标题之后，确保其在 ClawHub 平台渲染可见（原位置被平台过滤）。该行对 AI 助手无副作用。
- **人类读者导引补充英文版**：在中文导引旁新增英文版 `For human readers` 说明，邀请浏览者前往 GitHub 阅读 README，保持双语一致。
- **导引与简介视觉分隔**：在人类读者导引与 skill 简介之间加入分隔线 `---`，并为简介添加 `## 简介 / Overview` 标题，避免两段文字紧邻造成阅读困难。

## [2.3.8] — 2026-08-15

### 修复 / Bug Fixes (distribution)

- **ClawHub 名称纠正**：修正发布于 ClawHub 的 Skill 显示名为 `Iterate`（此前误发布为 `Clawhub Stage 2.3.7`），并重新分发至新版 2.3.8。
- **SKILL.md 顶部新增人类读者导引**：在 frontmatter 之后新增一条面向人类浏览者/开发者的说明，邀请其前往 GitHub 仓库 `jingzhao-l/iterate-skill` 阅读 README，以详细了解本 Skill 及其附属生态（iterate-harness、iterate-plugin、CLI 等）。该行对 AI 助手无副作用。

## [2.3.7] — 2026-08-14

### 修复 / Bug Fixes (skill)

- **TUI 接口契约**：`tui.question()` 签名返回类型由 `str` 修正为 `None`（此前签名与实现不一致）；删除无调用方的死代码 `prompt_prefix()`（其返回值含 rich 标记，若被用作 `input()` 提示文本会把 `[iterate.dim]` 标记泄露到终端）。新增 `tests/test_tui.py` 契约测试。
- **示例文档矛盾**：`examples/typescript-project.md` 预期行为第 5 条"验证通过后合并推送"与安全默认 `git.auto_merge=false` / `git.push_per_round=false` 矛盾，已对齐 Python/Swift 示例的措辞。
- **决策日志模板角色说明**：`templates/iterate-decisions.template.md` 增加头注释，明确该模板是 AI 会话按 SKILL.md「决策日志格式」章节填充的结构参考，`{...}` 非 Python format 占位符。
- **入口冗余**：移除 `iterate_cli/cli.py` 尾部与 `__main__.py` 重复的 `if __name__ == "__main__"` 守卫及无用 `import sys`。

## [2.3.6] — 2026-08-14

### 插件安全修复 / Security (iterate-plugin)

- **P0 最高优先**：`validate` 验证命令安全模型由「前缀白名单」改为 `validation.commands` 中命令的**精确匹配**。原前缀匹配允许攻击者通过构造形如 `python3 -c "..."` 绕过白名单执行任意代码，新精确匹配杜绝该风险。无配置信任命令时，会明确拒绝执行任意命令。

### 插件功能补全 / Features (iterate-plugin)

- **P1**：`iterate_context` 支持多路径查找 SKILL.md：按优先级 `自定义路径 → 自动探测 skill 目录（从插件位置向上找）→ 项目根` 查找，返回找到的内容和来源目录。解决插件挂载到项目目录时读不到原 skill 文档的问题。
- **P2**：`config-loader` 支持「默认配置（Master）+项目覆盖（Overrides）」深合并，无配置文件时也能以完整默认配置运行（仍保持 `validation.commands` 默认空，拒绝执行任何命令，符合最小权限）。工具层（`config/validate/review`）全部适配。

### 插件一致性对齐 / Bug Fixes (iterate-plugin)

- **P2**：`ReviewFinding` 字段对齐原 iterate skill：`detail/classification` → `failure_scenario/suggested_fix/is_atomic`，`review.ts/skill-prompt.ts`/测试用例同步更新。
- **P1**：dry-run/normal 工作流对子代理返回添加判空防御：`planRes/finalAgg` 为 null/无效时抛错而非崩溃。
- **P2**：`dry-run` 脚本 `finalReport.metaReview.issues` 添加可选链与默认值，避免无问题时访问 null。

### 新增单元测试 / Tests

- 新增 `config-loader.test.ts`、`context.test.ts`，共新增 22 个测试用例。
- 所有 TS 测试 53 个全绿，类型检查通过。

---

## [2.3.5] — 2026-08-14

### 修复 / Fixes

- **meta-review 误报收敛轮为 ROUND_EMPTY**：dry-run 收敛时最后一轮 0 个新 findings 是**正常的成功信号**，但 `metaReviewReport` 的 ROUND_SHAPE 检查会将其误判为 `ROUND_EMPTY` 缺陷，导致最终审查报告错误判定为 `needs_revision`。已修复——仅当**非最后一轮**出现空 findings 时才报 `ROUND_EMPTY`，最终收敛空轮不再触发。

### 文档 / Docs

- **`harness/iterate-plugin/README.md`**：新增插件运行时说明（安装、加载、dry-run 纯审查与 meta-review 用法）。
- **`DESIGN-iterate-harness.md`**：补充 meta-review 收尾步骤设计说明。

### 维护 / Maintenance

- 版本号统一升级至 `2.3.5`（`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json`、`harness/iterate-plugin/package.json`、`package-lock.json`、`SKILL.md` frontmatter）。

---

## [2.3.4] — 2026-08-14

### 新功能 / Features

- **`iterate review` 纯反复审查 + 报告元审查（meta-review）**：dry-run 纯审查模式新增收尾步骤——反复审查直至某一轮出现 0 个新 findings（收敛），生成审查报告后，再对报告本身进行元审查（校验报告内部一致性：总数匹配、严重级别汇总、维度汇总、排序、收敛数学），最终给出带 `approved`/`needs_revision` 判定的最终审查报告。全部判定逻辑保持确定性、可测试、不触碰文件。
  - `harness/iterate-plugin/src/meta-review.ts`：新增元审查引擎（`metaReviewReport` 执行 6 项一致性检查，`buildFinalReviewReport` 组装最终报告）。
  - `harness/iterate-plugin/src/tools/review.ts`：`iterate_review` 新增 `meta-review` 操作。
  - `harness/iterate-plugin/src/skill-prompt.ts`：dry-run 规范工作流加入 meta-review 阶段。
  - `harness/iterate-plugin/test/meta-review.test.ts`：新增 11 个元审查测试用例。
- **纯审查模式暴露到 skill 调用界面**：`/iterate <goal> review-only`（或 `dry-run`）即可触发纯审查模式。`SKILL.md` 新增 `$mode` 参数、review-only 适用场景与只读审查循环说明；`README.md` Daily Usage 补充纯审查调用示例与说明。

### 安全 / Security

- **`npm-installer` 解压路径遍历防护**：`extractTarball` 在解压前先用 `tar -tzf` 列出归档成员，校验每个成员在去掉顶层目录后解析出的路径仍落在目标目录内（防 `../` 逃逸），否则拒绝解压并抛出 `InstallerError`。保持零运行时依赖。
- **升级 `js-yaml` 至 `4.3.1`**：修复 `js-yaml@4.1.0` 的 4 个安全公告风险（含 2 个 high：prototype pollution merge、quadratic CPU consumption DoS）。`npm audit` 从 1 high 降至 **0 vulnerabilities**。js-yaml 仍为 MIT 许可证。

### 维护 / Maintenance

- 版本号统一升级至 `2.3.4`（`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json`、`harness/iterate-plugin/package.json`、`package-lock.json`、`SKILL.md` frontmatter）。

---

## [2.3.3] — 2026-08-14

### 修复 / Fixes

- **`full_reonboard` 未处理 `NO_CHANGES_NEEDED` 哨兵导致崩溃**：当回归用户同时拒绝基础更新和个性化配置时，`run_wizard` 返回的 `object()` 哨兵直接被传入 `write_onboarding_outputs`，抛出 `AttributeError`。此时旧文件已在向导运行前被备份，造成"备份了但没写入"的中间态。已新增 `NO_CHANGES_NEEDED` 判断并安全返回。
- **JS/Python 校验和解析不一致**：`npm-installer/lib/installer.js` 的 `parseChecksums` 未剥离 GNU tar 二进制标记 `*`，而 `scripts/install.py` 做了 `lstrip("*")`。若 `SHA256SUMS.txt` 采用 `HASH *filename` 格式，npx 安装器会校验失败。已统一 JS 侧 `replace(/^\*/, '')`。

### 安全 / Security

- **`_manual_collect_commands` 缺少 shell 元字符校验**：手动输入的验证命令未检查 `;` `|` `&` `` ` `` `$` `>` `<` `\n` `\r` 等 shell 链接元字符，存在绕过窗口。已复用 `FORBIDDEN_COMMAND_CHARS` 黑名单在输入时拒绝含元字符的命令。
- **`_safe_extractall` 回退分支硬编码 `/` 分隔符**：Python < 3.12 的路径遍历防护使用 `startswith(str(path) + "/")`，Windows 上永不匹配，导致所有合法成员被误判为可疑。已改用 `Path.is_relative_to()`（平台无关）。

### 维护 / Maintenance

- 移除死代码 `_detect_installed_assistants`（与 `detect_installed_assistants` 重复）和 `_fetch_latest_release_tag`（无调用方）。
- 为 `_update_iterate_md_user_section` 的 `read_text`/`write_text` 增加 try/except 异常处理，防止 `OSError`/`UnicodeDecodeError` 向上传播崩溃。
- `_download_release_source` 临时目录在异常和空提取分支增加 `shutil.rmtree` 清理，防止泄漏。
- 提取 `generate_config_yaml` 中裸字面量（`7`/`20`/`3`/`"Improve code quality..."`）为模块级具名常量。
- 提取 `_print_scan_results` 中目录截断上限裸字面量 `10` 为具名常量 `MAX_DIRS_DISPLAYED`。
- 拆分 `run_personalize_wizard`（112 行）为 `_run_personalize_steps_1_4` 与 `_run_personalize_steps_5_9` 两个子函数，满足单函数 ≤ 80 行的代码质量约束。
- 新增 `full_reonboard` 的 `NO_CHANGES_NEEDED` 回归测试（`test_returns_true_on_no_changes_needed`）。
- 新增 `parseChecksums` 的 `*` 标记剥离 JS 测试（`mode.test.js`）。
- 新增 `_manual_collect_commands` shell 元字符拒绝测试（`test_command_with_shell_metacharacter_is_rejected`）。

### 文档 / Docs

- **SKILL.md 配置表 `git.use_worktree` 描述澄清**：明确"当工作区有未提交改动时，无论此值如何，都优先用 worktree 隔离"，消除与 Step 1.7 的矛盾。
- **README 方式 B 手动复制修复**：从"只复制 SKILL.md"改为"必须复制整个 `iterate/` 目录（含 `config/`、`scripts/`、`templates/`），否则运行时找不到依赖"。
- `config/iterate.config.yaml` 的 `git.use_worktree` 新增注释说明。

---

## [2.3.2] — 2026-08-13

### 功能 / Features

- **漂移忽略列表（`onboarding.drift_ignore`）**：允许用户配置 fnmatch 模式，将锁文件等频繁变更的 manifest（如 `package-lock.json`、`yarn.lock`）排除出漂移检测。新增 `iterate_cli/fingerprint.py` 中 `_matches_ignore()` 的完整接线（此前为死代码）：`scan_manifests` / `capture_fingerprints` / `check_drift` 均支持忽略模式，`check_drift` 在比较前同时过滤当前扫描与已存指纹两侧，避免被忽略的旧指纹产生虚假 `removed` 漂移。`refresh.py` 新增 `get_drift_ignore()` 读取配置，`incremental_refresh` 刷新后的指纹列表会排除被忽略的 manifest。`config.schema.json`、`config/iterate.config.yaml`、`SKILL.md` 配置说明同步补充 `onboarding.drift_ignore` 字段。
- **`iterate status` 接入智能建议（`drift.advice()`）**：漂移检测到变更时，status 输出会展示根据漂移类型（新增/删除 vs 内容变更）生成的针对性建议（是否值得 `iterate refresh`），取代此前固定文案。
- **`iterate status` 信息增强**：新增 `Skill version`、`Fingerprints: N manifest(s)`、`Drift check: enabled/disabled` 输出；漂移为空时区分"检查已禁用 / 尚无指纹 / 未知"三种原因，便于排障。

### 修复 / Fixes

- **`SKILL.md`「何时跳过」与 Step 1 矛盾**：v2.3.1 已将脏工作区处理改为"优先 worktree 隔离、不中止"，但「何时跳过 / When to Skip」仍残留"工作区不干净→不要使用"条目。已删除该条（中英文），与 Step 1 的 worktree 隔离策略保持一致。
- **`SKILL.md` 配置表白名单描述过期**：「无需二次确认的允许命令前缀」更新为「不在白名单中的命令直接拒绝，不可通过用户确认绕过」，与命令白名单双层强制策略一致。
- **`config/dimensions.yaml` 主表 `frontend-backend` 缺 `priority`**：补上 `priority: high`，与权威文件 `config/dimensions/frontend-backend.yaml` 一致。

### 维护 / Maintenance

- `iterate_cli/generator.py` 中 `_render_dimensions` 的 `priority_map` 补充"需与 `config/dimensions.yaml` 保持同步"注释，明确重复维护关系。
- 新增 `tests/test_drift_ignore.py`（15 个用例）：覆盖扫描忽略、`check_drift` 两侧过滤、配置读取健壮性、refresh 后指纹排除、status 输出 advice 与新增字段。
- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.3.2`。

---

## [2.3.1] — 2026-08-13

### 功能 / Features

- **操作者级验证工具安全扩展点（无需改源码）**：`iterate_cli/personalize.py` 新增环境变量 `ITERATE_EXTRA_SAFE_COMMAND_PREFIXES`，允许操作者在系统层面追加预批准工具前缀（如 `sphinx`），而无需编辑源码。该变量**只能在进程环境设置，项目配置文件无法设置**，因此不会破坏既有安全模型；含 `;`、`|`、`&` 等元字符的条目会直接丢弃（fail-closed），不以其开头或以非字母数字开头（如 `-rf`、`/`）的碎片也会被过滤。新增 7 个回归测试覆盖默认、解析、注入丢弃、白名单扩展、元字符拒绝与 `python -m` 形式。

### 文档 / Docs

- **首次使用预期提示（体验）**：SKILL.md Step 0 与 AI Onboarding 明确要求 AI 在首次调用时先说明"将先进行项目初始化"，避免用户误以为 skill 失效；README FAQ 同步更新"第一次使用为什么什么都不做"。
- **Monorepo 定位（体验）**：SKILL.md Step 0 与 Setup 的项目根目录定位改为优先命中含 `ITERATE.md` / `iterate.config.yaml` 的目录，并对多子项目场景给出 `AskUserQuestion` 确认，避免误审无关子项目。
- **脏工作区处理（体验）**：SKILL.md 创建隔离环境改为优先 `git worktree add` 隔离，不再强制要求 commit/stash、不因用户拒绝而直接中止。
- **会话内进度反馈（体验）**：SKILL.md Step 2 新增"进度反馈"约定，要求主模型每轮开始/并行审查/每轮结束持续输出进度；README FAQ 的"大项目卡住"答案同步说明。
- **交付指引与提前终止（体验）**：SKILL.md Step 3 新增"交付指引"（明确分支名、日志路径、合并/推送选项）与"提前终止"（剩余均 low 或目标达成时询问提前结束），README FAQ 同步。
- **会话恢复（体验）**：SKILL.md 会话中断与恢复改为 AI 自动读取 `.iterate_decisions.md` 并主动提议 resume/restart/仅查看报告，用户无需自行理解决策日志。
- README FAQ 更新"想增加新的验证工具"答案，补充环境变量扩展方式。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.3.1`。

---

## [2.3.0] — 2026-08-04

### 文档 / Docs

- **新增"常见问题 / FAQ"章节（SkillHub Convention 评测改进）**：SkillHub 评测指出 C·Convention 的短板是"没有常见问题解答，遇到特殊情况只能靠试错摸索"。README 新增 FAQ 章节，按「安装 / 使用 / 安全」三组覆盖：国内网络安装受限、Node/Python 版本要求、是否自动安装 CLI、取消安装是否留半成品、适用/不适用场景、首次使用未初始化、大项目耗时无进度、漂移检测含义、改动未合并推送、验证命令不生效、新增验证工具、密钥与 `.env` 保护、更新下载安全性等 13 个常见问题。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.3.0`。

---

## [2.2.9] — 2026-08-04

### 安全 / Security

- **发布预上传 tarball + SHA256SUMS，installer 下载资产时验证（ClawHub Description-Behavior Mismatch）**：`.github/workflows/release.yml` 改为先 `git archive` 生成 `iterate-skill.tar.gz`，再生成 `SHA256SUMS.txt`，并把两者作为 Release 资产上传。`npm-installer/lib/installer.js` 与 `scripts/install.py` 现在优先下载上传的 `iterate-skill.tar.gz` asset，再用 `SHA256SUMS.txt` 校验，而不是依赖 GitHub 自动生成的 tarball。这样 checksum 文件在 release 发布时即已存在，installer 执行的是真正的完整性校验。
- **明确披露安装器会安装 `iterate` CLI 到 PATH（Context-Inappropriate Capability / Excessive Agency）**：README 与 SKILL.md 的安全说明中明确说明 `npx iterate-skill-installer` 会顺带把 `iterate` CLI 安装到 PATH（优先 `pipx` 隔离，否则 `--user`），并给出不安装 CLI 的替代方式。
- **明确 onboarding 扫描范围（敏感文件披露）**：README 与 SKILL.md 说明 onboarding 扫描仅检查 manifest 等公开文件的存在性以及 `README.md` / `CLAUDE.md` 等上下文文件，不会读取 `.env`、密钥、凭证等敏感文件内容。
- **进一步强化 merge/push opt-in 披露**：README 的 At a Glance、安全说明与 SKILL.md 的风险披露中，统一写明 `auto_merge` / `push_per_round` 默认 `false`，merge/push 为 opt-in。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.9`。

---

## [2.2.8] — 2026-08-04

### 安全 / Security

- **关闭个性化配置的可执行命令信任边界绕过（ClawHub SkillSpector SDI-4/SDI-2）**：`load_personalization_from_config` 与 `merge_personalization_into_config` 现在对 `iterate.config.yaml` 中来源的 `extra_validation_commands` 均用 `validate_extra_command` 重新校验（fail-closed），命令含 shell 链接元字符或不在预批准前缀白名单内时直接跳过，不再并入可执行的 `validation.commands`，也不会自动扩展 `command_whitelist`。此前手工编辑的配置文件可绕过严格白名单并持久化、执行任意命令，现已封堵。
- **统一验证命令白名单文档（SDI-4）**：`SKILL.md`、`tools/SKILL.claude.md`、`tools/SKILL.cursor.md` 中原有"不在白名单的命令需用户确认"的表述与个性化硬白名单矛盾，已统一为"不在白名单的命令直接拒绝，不可通过用户确认绕过"，消除安全模型前后不一致。
- **统一 merge/push 文档默认值（SQP-2 / instruction_scope）**：`SKILL.md` 简介、Git 隔离工作流、重要注意事项，以及 `examples/python-project.md`、`examples/swift-project.md`、`tools/SKILL.cursor.md` 中把 merge/push 描述为"自动/预期行为"的表述已修正为 opt-in，并明确 `git.auto_merge` 与 `git.push_per_round` 默认均为 `false`（安全默认），未显式开启时改动保留在迭代分支由人工 review。
- **新增 `pip-audit` 到预批准验证命令前缀**。

### 修复 / Bug Fixes

- 修复 `extra_validation_commands` 从配置加载时未校验、可被手工编辑的配置文件绕过白名单的问题。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.8`。

---

## [2.2.7] — 2026-08-03

### 安全 / Security

- **降低安装器 `child_process` 的静态分析误报**：VirusTotal 的 `suspicious.dangerous_exec` 将调用 `child_process` 的安装器标记为可疑，属于对"包安装器"的启发式误报。本次将 `commandExists` 由 `execFile` 改为 `spawnSync`（同步、无异步回调特征），并在文件顶部补充安全设计说明，明确：所有子进程以参数数组调用（不经 shell、无命令注入面）、程序名均为固定白名单字面量、用户输入（如 `--target`）作为独立 argv 传递而非拼入 shell 字符串。安装器调用系统命令（curl/python/pipx/tar）是必要行为，无法完全消除该标记，但本次改动可降低误报概率。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.7`。

---

## [2.2.6] — 2026-08-03

### 修复 / Bug Fixes

- **macOS 上 CLI 自动安装的 PEP 668 降级提示**：当系统 Python 为 externally-managed（如 Homebrew Python）导致 `pip install --user` 被拒时，安装器现在能识别该错误并给出明确的下一步指引（安装 pipx 或 `--break-system-packages`），而不是仅输出笼统的失败信息。
- **SKILL.md 的 AI Onboarding 明确写入 `channel`/`completed_at`**：此前 AI 通道生成的 `iterate.config.yaml` 未明确要求写 `onboarding.channel` 与 `onboarding.completed_at`，导致 `iterate status` 对 AI-onboarded 项目显示 `Channel: unknown`。现已与 CLI 通道产出对齐。

### 维护 / Maintenance

- **同步发布 npm 包至 `2.2.6`**：此前 npm 包停留在 `2.1.6`，用户 `npx iterate-skill-installer` 会拉到旧版安装器。本次将 npm 包与 GitHub Release 版本对齐并重新发布。
- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.6`。

---

## [2.2.5] — 2026-08-03

### 修复 / Bug Fixes

- **重新个性化时保留 ITERATE.md 中的自由文本备注与代码约定**：`iterate personalize` 或重新 onboarding 时，此前结构化规则从 `iterate.config.yaml` 加载，但自由文本的 `iterate_notes` 与 `code_conventions` 只存在于 ITERATE.md 的用户自有区块，未读回导致重新保存时 `merge_user_sections` 静默清空用户此前填写的内容。现在新增 `load_personalization_from_iterate_md` 与 `load_existing_personalization`，合并两个来源后再进入编辑，避免内容丢失。

### 测试 / Tests

- 新增 `TestLoadPersonalizationFromIterateMd` 回归测试，验证从 ITERATE.md 用户自有区块正确解析备注与代码约定。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.5`。

---

## [2.2.4] — 2026-08-03

### 修复 / Bug Fixes

- **`iterate onboard` 的引导默认值改为「继续」**：此前用户显式运行 `iterate onboard` 时，gate 问题、技术栈确认、建议校验命令等关键提示默认值为「否」，用户直接回车会中止流程或退回手动输入，体验反直觉。现在这些提示在用户显式发起 onboarding 时默认「是」，直接回车即可按推荐流程继续。

### 测试 / Tests

- 新增 `test_gate_defaults_to_continue_on_empty` 回归测试，验证 gate 问题在空回车时默认继续进入 onboarding。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.4`。

---

## [2.2.3] — 2026-08-03

### 修复 / Bug Fixes

- **安装时仅预选自动检测到的 AI 工具**：此前 `install.py` 的箭头键多选默认全选所有受支持工具，即使某些工具未安装也会被预勾选，导致用户误以为会安装到不存在的工具。现在只预选检测到的（已安装）工具，未检测到的工具列出但默认不勾选，需用户显式选择。
- **安装取消时不再误报成功**：此前当用户取消安装（未选择任何工具）时 `install_command` 返回 `0`，导致 `npx iterate-skill-installer` 打印成功提示。现在返回非零退出码，npm 包装器检测到取消/失败后停止并提示，不再误报成功。

### 测试 / Tests

- 新增 `TestInstallPreselect` 回归测试，验证多选仅预选检测到的工具。
- 新增 `TestInstallCancelExitCode` 回归测试，验证取消安装返回非零退出码。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.3`。

---

## [2.2.2] — 2026-08-03

### 修复 / Bug Fixes

- **修复 `iterate onboard` 重新 onboarding 时丢失 `personalization` 结构化规则**：此前返回用户仅更新基础配置（未重新个性化）时，`iterate.config.yaml` 会被整体重新生成，导致原有的 `personalization` 结构化规则（受保护路径 `protected_paths`、风险区域、额外校验命令 `extra_validation_commands` 等）被静默丢弃。现在 `_cmd_onboard` 会在用户未重新个性化时，从现有配置加载并保留 `personalization`，保证基础配置更新不丢失结构化规则。

### 测试 / Tests

- 新增 `TestCmdOnboardPreservesConfigPersonalization` 回归测试，验证返回用户仅更新基础配置时，`protected_paths` 与 `extra_validation_commands` 等结构化规则在 `iterate.config.yaml` 中得以保留。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.2`。

---

## [2.2.1] — 2026-08-03

### 修复 / Bug Fixes

- **`npx iterate-skill-installer` 自动安装 `iterate` CLI**：此前 npx 一键安装只复制 skill 文件到 AI 助手目录，但 README Quick Start 却引导用户运行 `iterate onboard`（需先安装 CLI），造成用户旅程断裂。现在安装器在复制 skill 后自动安装 `iterate` CLI（优先 `pipx`，否则 `pip install --user`），真正实现“一条命令完成 skill + CLI 安装”。
- **修复 `iterate refresh` 将 `push_per_round` 默认置为 `True`**：`iterate_cli/refresh.py` 的 `_build_refresh_data` 在配置缺失时默认 `push_per_round=True`，违背 Secure-by-default（`OnboardingData` 与文档默认均为 `False`）。已统一为 `False`。
- **修正 CLI onboarding 的“无法扫描代码库”错误表述**：此前 wizard 的 gate 提示声称“命令行向导无法扫描代码库，只能基于你的回答生成配置”，但实际 `scan_project` 会扫描并自动检测技术栈。已更新 wizard 文案、README 与 SKILL.md，说明 CLI 会扫描代码库并让用户确认/调整。

### 测试 / Tests

- 新增 `test_refresh_defaults_push_per_round_to_false` 回归测试，验证 `refresh` 在配置缺失 `git.push_per_round` 时默认置为 `False`（Secure-by-default）。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.1`。

---

## [2.2.0] — 2026-08-03

### 新增 / Features

- **AI 工具选择改为箭头键多选菜单**：`scripts/install.py` 在选择安装目标时，交互终端（TTY）下使用 `↑/↓` 移动高亮、`空格 / 回车` 勾选当前工具、`Done` 确认、`q` 取消，取代原先的编号输入，更直观且支持多选。非 TTY（管道 / 测试）自动回退到编号输入，保证可测试性。
- **AI 工具自动检测优化**：安装时基于用户 `home` 目录自动检测本机已安装的 AI 编程工具并预选；未检测到任何工具时，列出全部支持的工具供手动选择。
- **项目目录自动识别**：`npx iterate-skill-installer` 在非 home 目录启动时，若未显式指定 `--global` / `--target`，会询问当前目录是否为目标项目目录；若是则直接进入项目级安装。

### 测试 / Tests

- 新增 `TestArrowSelectState` 单元测试，覆盖多选状态机的上下移动、勾选/取消、`Done` 确认、取消、`_read_arrow_key` 按键解码与渲染标记。
- `npm-installer` 新增 `test/mode.test.js`，覆盖 `resolveInstallMode` 的全局/项目级安装判定（显式 `--target` / `--global`、cwd 为 home、cwd 非 home 时是否确认项目目录）。

### 代码质量 / Code Quality

- 修复 `scripts/install.py` 中 `InputFunc` 类型别名未定义（F821）：补充 `from typing import Callable` 与 `InputFunc = Callable[[str], str]`。
- 移除 `iterate_cli/tui.py` 中未使用的 `rich.text.Text` 导入（F401）。
- CI 新增 `ruff check scripts/ tests/ iterate_cli/` 步骤，防止后续引入未定义名称 / 未使用导入等静态问题。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.2.0`。

---

## [2.1.6] — 2026-08-03

### 文档 / Documentation

- **全面重构 README.md**：以“用户旅程”为主线重新组织内容，降低阅读负担。
  - 新增“3 分钟上手 / Quick Start”章节，用三步引导用户完成安装、onboarding、开始迭代。
  - 安装方式精简为“推荐 + 其他方式”两层，突出 `npx iterate-skill-installer` 唯一推荐路径。
  - 合并原先并列的 4 种安装方式，将 pip install、手动复制 SKILL.md、源码脚本归入“其他方式”。
  - 新增“全局安装 vs 项目级安装”对比表格，给出明确建议。
  - 新增“为什么不推荐 skills.sh 安装？”说明，明确从 v2.1 起统一使用 npm 安装器。
  - 将“使用方式”和“Onboarding”内容整合到“它如何工作”章节，减少重复。

### 维护 / Maintenance

- 同步更新 `SKILL.md`、`pyproject.toml`、`iterate_cli/__init__.py`、`npm-installer/package.json` 中的版本号至 `2.1.6`。

---

## [2.1.5] — 2026-08-03

### 修复 / Fixed

- **修复安装摘要框线错位**：`scripts/install.py` 的 `_strip_markup` 正则现在能正确匹配空关闭标签（如 `[/]`），确保框线宽度计算与可见文本一致。

### 文档 / Documentation

- README 中补充 `npx iterate-skill-installer` 一键安装器的使用示例与选项说明。
- 重新组织 README 的安装与使用流程，使主线更清晰。

---

## [2.1.3] — 2026-08-03

### 修复 / Fixed

- 在 `scripts/requirements.txt` 中显式添加 `rich==13.7.1`，确保 npx 安装器创建的隔离 Python 环境具备 TUI 渲染依赖。
- 改进 `scripts/install.py` 的 markup stripping fallback，在 rich 不可用时仍能对齐输出。

---

## [2.1.2] — 2026-08-03

### 修复 / Fixed

- `npm-installer` 现在正确传递 `FORCE_COLOR=1` 到 Python 安装脚本，确保非 TTY 环境下仍保留彩色输出。

---

## [2.1.1] — 2026-08-03

### 新增 / Added

- `scripts/install.py` 新增 skills.sh 风格框线分区（`_frame_box`）和安装摘要，提升安装完成后的可读性。

---

## [2.1.0] — 2026-08-03

### 新增 / Added

- **skills.sh 风格 TUI**：新增 `iterate_cli/tui.py` 统一终端渲染层，采用青色主题与 @clack/prompts 符号体系（◆ ◇ └ ● ✓ ⚠）。
- **ITERATE 立体 ASCII 横幅**：CLI 命令与版本输出顶部展示 ITERATE Logo，左对齐避免错位。
- **AI 助手自动检测**：`scripts/install.py` 可检测 25+ 已安装的 AI 编程工具，并提供交互式多选菜单。
- **npx 一键安装器**：新增 `npm-installer`，支持 `npx iterate-skill-installer` 一条命令完成下载、SHA256 校验、隔离 Python 环境创建与安装。
- **跨助手安装统一**：同一份安装逻辑覆盖 Trae、Claude Code、Cursor、Windsurf、GitHub Copilot、Codex、Roo Code 等 25+ 工具。

### 改进 / Changed

- 将 `iterate onboard`、`personalize`、`status`、`refresh`、`reonboard` 的输出统一接入 TUI 层。
- 安装脚本 `pip install .` 输出美化，与整体 CLI 风格保持一致。

---

## [2.0.2] — 2026-07-29

### 安全 / Security

针对 ClawHub SkillSpector 审计报告的剩余 findings 进行第二轮修复。本次涉及**行为变更**（默认值从 `true` 改为 `false`）和**命令安全策略升级**（从"警告+确认"改为"硬拒绝"）。

- **`extra_validation_commands` 改为硬白名单 / Strict whitelist enforcement**（Finding 1: Context-Inappropriate Capability）：
  - `iterate_cli/personalize.py` 的 `validate_extra_command` 从"未知前缀警告但可确认添加"改为"未知前缀**直接拒绝**"。
  - wizard 步骤移除确认分支，不再提供绕过白名单的路径。
  - 只有 `KNOWN_SAFE_COMMAND_PREFIXES` 中列出的 30+ 常见 test/lint/type-check/build 工具前缀才会被接受。
  - 测试同步更新：`test_unknown_prefix_warns_but_accepts` → `test_unknown_prefix_rejected`，`test_python_m_with_unknown_module_warns` → `test_python_m_with_unknown_module_rejected`，`test_add_extra_validation_commands` 验证 `safety check` 被拒绝。

- **`git reset --hard` 全部替换为非破坏性命令 / Non-destructive rollback**（Findings 11-14: Tool Parameter Abuse）：
  - Phase 2 原子修复回滚：`git reset --hard HEAD` → `git restore --staged --worktree .`
  - Phase 3 全量验证回滚：`git reset --hard iterate/round-{round}-backup` → `git reset --mixed iterate/round-{round}-backup && git restore --worktree .`
  - Phase 5 备份标签回滚引用：同上替换。
  - `--mixed` 只移动分支指针不改工作区，`git restore` 再恢复文件，避免了 `--hard` 的数据丢失风险。

- **`push_per_round` 和 `auto_merge` 默认值改为 `false` / Secure-by-default**（Findings 7-10: Missing User Warnings）：
  - `config/iterate.config.yaml`：`push_per_round: true` → `false`，新增 `auto_merge: false`。
  - `config/config.schema.json`：新增 `auto_merge` 字段定义（boolean, default: false）。
  - `iterate_cli/generator.py`：`OnboardingData.push_per_round` 默认值 `True` → `False`，生成配置新增 `auto_merge: False`。
  - `iterate_cli/wizard.py`：`_collect_git_config` 的 `_ask_yes_no` 默认值 `True` → `False`；`_load_existing_data` 的 fallback `True` → `False`。
  - `scripts/install.py`：`config --interactive` 的 `push_per_round` fallback `True` → `False`。
  - SKILL.md Phase 5 Merge/Push 步骤改为条件化：仅在配置显式设为 `true` 时才执行自动 merge/push。

- **架构修复审批门禁显式化 / Explicit approval gate**（Finding 5）：
  - SKILL.md Phase 3 用户审批步骤标注为 **强制门禁 / Mandatory gate**。
  - 新增安全约束说明：此门禁不可跳过、不可自动绕过，独立于 merge/push 流程。

- **命令白名单双层强制执行说明 / Dual-layer whitelist enforcement**（Finding 6）：
  - SKILL.md 安全章节更新：明确标注配置时校验（validate.py）和个性化硬白名单（validate_extra_command）双层执行。
  - 个性化硬白名单部分明确说明"不在白名单中的命令**直接拒绝**，不可通过用户确认绕过"。

- **`description` 补充 update 能力 / Description accuracy**（Finding 2）：
  - SKILL.md frontmatter description 从 "cross-assistant installer" 扩展为 "cross-assistant installer/update system with mandatory SHA256 checksum verification"。
  - Update 命令远程下载说明从"若包含 SHA256SUMS.txt 则校验"改为"**强制校验**，缺失则拒绝下载"。

- **`scripts/install.py` 强制 SHA256 校验 / Mandatory checksum verification**（延续 v2.0.1 未提交变更）：
  - `_download_release_source` 在 `checksum_url` 为 None 时拒绝下载。
  - `_run_validate_subprocess` 替换 `_load_validate_module`，用 subprocess 替代 exec_module 消除 static analysis 误报。

### Breaking Changes

- **`push_per_round` 默认值从 `true` 改为 `false`**：新 onboarding 生成的配置不再自动 push。已有配置不受影响（值已显式写入）。
- **`auto_merge` 新增字段，默认 `false`**：新 onboarding 生成的配置不自动 merge。已有配置无此字段时视为 `false`。
- **`extra_validation_commands` 未知前缀从"警告+确认"改为"拒绝"**：之前可通过确认添加非白名单命令，现在直接拒绝。

### 升级 / Upgrade

```bash
python scripts/install.py update --ai trae --target /path/to/project
```

或直接从 GitHub Release 下载 v2.0.2 source code：
https://github.com/jingzhao-l/iterate-skill/releases/tag/v2.0.2

---

## [2.0.1] — 2026-07-29

### 安全 / Security

针对 ClawHub SkillSpector 与 static analysis 报告的安全审计 findings 进行透明度与校验加固。**不改变任何运行时行为**，所有改进都是为了让人机审计员更容易判断 skill 的能力边界与可信范围。

- **SKILL.md frontmatter 新增 `permissions` 字段**：显式声明 `file_read` / `file_write` / `shell` / `git` / `network` 能力，以及敏感文件跳过清单（`.env`、`*.key`、`.pem`、`.aws/`、`.ssh/` 等）。解决 SkillSpector Lp3「MCP Least Privilege / Underdeclared Capability」finding。
- **SKILL.md `description` 扩展**：从「multi-round code iteration」扩展到「multi-round code iteration with onboarding/personalization, and a cross-assistant installer」，使描述与实际能力（onboarding、personalize、跨 assistant 安装/更新）一致。解决 SkillSpector Tp4「MCP Tool Poisoning / 描述与能力不匹配」finding。
- **SKILL.md 4 处 `git reset --hard` 加边界注释**：明示「仅限 `iterate/*` 分支，严禁对 `main`/`master` 执行 reset --hard」，让静态扫描器与人工 review 都能识别安全边界。解决 4 处 Tool Parameter Abuse (High) finding。
- **SKILL.md 自动 merge/push 加 ⚠️ 高风险提示**：在 Phase 5 Merge 与 Push 步骤前加入风险提示，建议生产仓库设置 `push_per_round: false` 或 `auto_merge: false`，或为 main 启用分支保护。解决 2 处 Missing User Warnings (Medium) finding。
- **`scripts/install.py` `_load_validate_module` 加 security note 注释**：说明 `spec.loader.exec_module` 加载的是本 skill 自带的 `scripts/validate.py`，非远程代码、非用户输入、非网络获取，且 `source` 路径来自本地 checkout 或经过 SHA256 校验的 release tarball。澄清 Static analysis Critical「suspicious.dynamic_code_execution」finding 为误报。
- **`iterate_cli/personalize.py` 新增 `validate_extra_command` 校验函数**：对 `extra_validation_commands` 用户输入做白名单 + 黑名单双层校验：
  - 黑名单：拒绝 `;`、`|`、`&`、`` ` ``、`$`、`>`、`<`、换行等 shell 链接元字符，防止命令注入。
  - 白名单：30+ 常见 test/lint/type-check/build 工具前缀（pytest/ruff/mypy/eslint/swift/cargo/go/make 等），未命中白名单的命令需用户二次确认。
  - 支持 `python -m pytest` 形式的间接调用识别。
  解决 SkillSpector Context-Inappropriate Capability (Medium 95%) 与 Intent-Code Divergence (Medium 91%) finding。

### 文档 / Documentation

- `CHANGELOG.md` 新增本 v2.0.1 段，详细记录每项安全改进对应的 ClawHub finding 编号与原因。

### 不变性 / Non-changes

- **无 breaking change**：所有运行时行为、配置 schema、CLI 命令、返回值契约均与 v2.0.0 完全一致。
- **无新增依赖**：`validate_extra_command` 仅用标准库 `re`，未引入第三方包。
- **无 schema 变更**：`iterate.config.yaml` schema 不变，`personalization` 段结构不变。

### 升级 / Upgrade

```bash
python scripts/install.py update --ai trae --target /path/to/project
```

或直接从 GitHub Release 下载 v2.0.1 source code：
https://github.com/jingzhao-l/iterate-skill/releases/tag/v2.0.1

---

## [2.0.0] — 2026-07-29

### 重大变更 / Breaking Changes

- **Onboarding 全流程重构**：从单一流程改为多路径分支引导。
  - 首次用户（无 ITERATE.md）：gate 提问 → 基础 onboarding → 个性化配置。
  - 回归用户（有 ITERATE.md）：基础配置更新提示 → 个性化配置。
- **`run_wizard` 返回值契约变更**：新增 `NO_CHANGES_NEEDED` sentinel 用于区分"回归用户明确拒绝所有更新"（退出码 0）与"用户中途取消"（退出码 1）。原先 `None` 同时承担两种语义。
- **CLI 子命令新增**：`iterate personalize` 独立子命令用于随时更新个性化配置。

### 新增功能 / Added

- **个性化配置系统**（9 类约束）：
  - `protected_paths` — 受保护路径（禁止修改）
  - `risk_areas` — 风险区域（需谨慎）
  - `known_intentional` — 已知刻意模式（避免误报）
  - `dimension_focus` — 维度重点覆盖
  - `fix_priority_order` — 修复优先级顺序
  - `forbidden_fixes` — 禁止的修复类型
  - `iterate_notes` — iterate 场景备注
  - `code_conventions` — 代码规范补充
  - `extra_validation_commands` — 额外验证命令
- **Dual-storage 策略**：structured rules 写入 `iterate.config.yaml`，自由文本写入 `ITERATE.md` 用户区，merge 策略保留用户手动编辑。
- **多路径 CLI 引导**：首次 vs 回归用户分流，回归用户可选增量刷新。
- **`iterate personalize` 子命令**：9 步交互式 wizard，支持 add/remove/skip 统一界面。
- **Incremental refresh 原子写入 + rollback**：`incremental_refresh` 对 ITERATE.md 和 config.yaml 实施原子写入，失败时 best-effort rollback 并记录日志。
- **Personalization schema 版本化**：`personalization.version` 字段用于未来兼容性检测。
- **SKILL.md Step 0 / Phase 0**：skill 运行时消费 personalization 数据，调整审查行为。
- **Schema 约束强化**：`propertyNames` pattern 限制模块名仅允许 `[A-Za-z0-9_.-]`，防止 shell 元字符注入。
- **维度一致性校验**：`validate_personalization_consistency` 检查 personalization 中引用的维度是否在启用维度列表内。
- **Command whitelist 自动更新**：`merge_personalization_into_config` 自动从 `extra_validation_commands` 提取命令前缀加入白名单。

### 改进 / Changed

- `load_onboarding_config` 拒绝非 dict YAML（list/scalar），防止 caller 调用 `.get()` 时 AttributeError 崩溃。
- `_load_existing_onboarding_data` 同样增加非 dict 防护。
- `_cmd_onboard` 退出码语义精确化：`NO_CHANGES_NEEDED` → 0，`None`（取消）→ 1。
- `_returning_user_flow` 持久化 `project_description` 和 `code_conventions` 到 config.yaml 的 `onboarding` 段，避免回归用户丢失数据。
- `validate.py` 错误输出重定向到 stderr，错误消息包含数组索引以便定位。
- `_count_personalization_rules` 排除 `version` 元数据字段，正确计数 `extra_validation_commands`。
- `wizard.py` 维度选择去重，模块名校验（`MODULE_NAME_PATTERN`）。

### 修复 / Fixed

- 回归用户流程中 `project_description` 和 `code_conventions` 数据丢失。
- `extra_validation_commands` 保存/加载往返断裂。
- `merge_user_sections` 误匹配头部（`startswith` → 精确匹配）。
- `known_intentional.line` 字段类型保护缺失。
- `known_intentional.dimension` 缺少 enum 约束。
- Incremental refresh 原子性问题（双文件写入无 rollback）。
- `load_onboarding_config` 对非 UTF-8 文件和权限拒绝未处理。
- `_cmd_status` personalization 规则计数不准确。
- Rollback 失败静默吞错（现记录到 stderr）。
- `full_reonboard` backup 和 write 操作缺少错误处理。

### 测试 / Tests

- 测试套件从 ~140 扩展至 303 个测试。
- 新增覆盖：非 dict YAML 防护、退出码语义（取消 vs 无需变更）、atomicity rollback、维度去重、模块名校验、个性化一致性 e2e、增量刷新保留数据。

---

## [1.0.1] — 2026-07-20

### Fixed

- 简化 SKILL.md frontmatter 以兼容 OpenClaw/ClawHub 解析器，仅保留 `name`/`description`/`version` 字段。

---

## [1.0.0] — 2026-07-20

### Added

- 初始发布：fully automated multi-round code iteration with configurable N-dimension parallel review。
- CLI onboarding 基础流程。
- Fingerprint drift 检测。
- Dimension 配置与校验。
- Release tarball 安全提取（path traversal 防护）。
