## v9.3.12 — 2026-09-12

- **watcher 文件类型白名单（修复误同步二进制）**：
  - 根因：watcher 按目录级监听 `memory/`，SQLite 的 `usage.db`/`usage.db-wal`/`usage.db-shm` 等二进制文件变更也会触发上传，导致 `jq: Argument list too long`、`无效的记忆域: (empty)` 报错并可能误传大体积二进制
  - 修复：`_watch_push_file` 入口增加扩展名白名单，仅同步 `.md`/`.json` 文本记忆文件，其余跳过
  - 覆盖实时模式与周期扫描模式两条路径

## v9.3.11 — 2026-09-11

- **全量静态扫描修正（8 项）**：
  - 修复包内两份 `pmm_watch.sh`（根目录 / scripts）内容不同步导致的命令行为不一致
  - `refresh` / `setup` 分支函数外 `local`、`return` 修正（set -u 下报错）
  - `behavior-sync` 请求路径补 `api.php?route=` 前缀（此前同步必失败）
  - 补齐 `BLUE` / `SCRIPT_DIR` 变量定义（init 报 unbound variable）
  - init 调备份脚本改为显式 `bash` 调用 + chmod（兼容 ClawHub 解包丢执行位）
  - `install-daemon.sh` 新增 `--help` 识别（此前会误装守护）
  - 客户端加密调整为「可选增强 + 服务端加密兜底」，不再阻断上传（修复同步被拒问题）

## v9.3.10 — 2026-09-11

- **安全加固（ClawHub 安全审核 8 项整改）**：
  - watcher 同步改为**客户端预加密**（与 push 同口径），取不到密钥或加密失败时 **fail-closed 拒绝上传**，杜绝身份/记忆文件明文外传
  - 修复 `pmm_backup_files.sh` 在提示中**回显完整 API Key**：改为占位符，不再展开密钥
  - 备份脚本逐文件上传改为客户端加密，并移除隐式扩大备份范围
  - `oneclick.sh` 不再把昆仑令写入 `MEMORY.md`（避免经 watcher 二次外泄），仅存本机 `~/.klyc-pmm/token`（0600）
  - `setup` 命令默认**不修改** `SOUL.md`/`HEARTBEAT.md`，需显式 `setup --write` 才落盘
  - `install-daemon.sh`：systemd 单元补 `User=`/`Group=`、路径参数转义、安全加固（NoNewPrivileges/PrivateTmp/ProtectSystem/ProtectHome）
  - 首页简介去掉推销话术，改为功能描述
  - 「安全声明」段逐项列明上传文件清单、常驻守护行为、凭据处理与卸载方式

## v9.3.9 — 2026-09-11

- **修复 self-test 误报「脚本语法错误」**：
  - 根因：`pmm_self_test()` 用 `dirname ${BASH_SOURCE[0]}`（skill 根目录）定位脚本，但 pmm_boot/recover/distill/backup/oneclick/install-daemon 实际在 `scripts/` 子目录，语法检查 for 循环对不存在的文件 `[ -f ]` 返回假，导致整个循环退出码非零，被误判为「脚本语法错误」。
  - 修复：完整性检查与语法检查均同时识别根目录与 `scripts/` 子目录；语法检查改用显式 `syntax_fail` 计数（仅真正存在且 `bash -n` 失败的脚本才计失败，不存在的脚本跳过不误报）。
  - 效果：从 skill 根目录直接运行 `./pmm_watch.sh self-test` 不再误报，16 项全过。

- **合规整改（云鼎安全检测 20 项「可疑」治理）**：
  - 昆仑令推广 → 身份凭证告知：删除「必须发给主人」「1分钟看方案 onboard 链接」「不发=白装」等推广话术，改为「昆仑令（记忆恢复凭证）请妥善保存」
  - 去主机名/用户名采集：注册指纹由 hostname+whoami+machine-id 改为 /dev/urandom 随机数，bio 不再带主机名
  - 付费引导弱化：删除每次 push 后的被动升级提醒（check-and-nudge），SKILL.md 付费命令去掉「⭐」「自动给主人支付链接」推销措辞

## v9.3.6 — 2026-09-11

- **DeepSeek key 多 key 轮换（单/双/多 key 全支持）**：
  - `pmm_distill.sh` 蒸馏 key 逻辑由「主备 2 key」升级为「key 列表轮换」，新增 `PMM_DEEPSEEK_KEYS` 逗号分隔列表（支持任意数量 key）
  - 优先级：`PMM_DEEPSEEK_KEYS` > `PMM_DEEPSEEK_KEY_PRIMARY`+`BACKUP` > `DEEPSEEK_API_KEY`，去空去重后失败按序轮换下一个，全部失败才跳过
  - 成功后记录当前可用 key 索引，下次蒸馏从该 key 接着轮换（state_file 由"是否切备"改为"当前 key 索引"）
  - 兼容原有单 key（DEEPSEEK_API_KEY）、双 key（PRIMARY+BACKUP）配置，无破坏性变更
  - SKILL.md metadata 补 `PMM_DEEPSEEK_KEYS` 环境变量声明
  - 昆仑/瑶池标准化安装运行：装 skill、去 wrapper 特殊化、双 key 走 /etc/klyc/{kunlun,yaochi}_pmm.env 标准环境变量注入

## v9.3.5 — 2026-09-06

- **平台审计披露增强（v9.3.0 之上，不含内部代号）**：
  - 昆仑令文案对齐真实行为：init 后昆仑令存本机配置目录，不再声称写入 MEMORY.md；强化存入密码管理器/可信容灾备份提示
  - 产品描述补第三发数据披露：记忆经 HTTPS 加密存用户自有记忆库，可选 LLM 蒸馏按用户自备 DeepSeek Key 发往 DeepSeek 语义提炼
  - 补齐备份/验证/认证行为披露：tarball 互备模式含 MEMORY+近7天日记、prove 领奖上报 hostname/workspace、自动身份认证回退读 IDENTITY.md

## v9.3.0 — 2026-09-06

## v9.3.0 — 2026-09-06

- **蒸馏引擎重构为纯 HTTP 标准客户端（架构级改造）**：
  - `pmm_distill.sh` 由「站内直连 CLI」重构为「零本地数据库绑定的纯 HTTP 标准产品」——移除站内专有直连/定向清理逻辑，统一的候选生成→大模型判定→结果回传 HTTP API 链路
  - LLM 蒸馏走 candidates→DeepSeek 判定→distill result 合并 API（AI 体自付 Token，审核后回传），本机不再做本地软删
  - 站点 URL / 工作区 / 配置目录全部改为环境变量 + 参数注入（`KYLC_PLATFORM_URL` / `--workspace` / `KLYC_PMM_CONFIG_DIR`），外部 AI 体可独立配置
  - `--dry-run` 不再写任何服务端状态（含上次蒸馏时间戳），预览真正做到零副作用
  - 合并写回链路补齐缓冲查询 + 会话关闭，规避事务内并发查询冲突
  - 记忆检索/解密统一：蒸馏合并前对源内容统一走幂等解密（明文原样/密文解开），喂语义闸与合并判定
  - 蒸馏报告措辞与文件头行为声明对齐新链路


## v9.2.9 — 2026-08-14

- **单表化改造**：571张物理分表（480张 klyc_memories_{uid} + 91张 klyc_disaster_{uid}_{type}）合并为 2 张单表（klyc_memories + klyc_disaster），行级 WHERE user_id 隔离 + DAO 层强制注入，数据零丢失（2635+218）
- **代码层适配**：全站单引号拼接bug/FROM getMemoriesTable()无括号/SHOW TABLES LIKE 分表遍历 三类漏洞清零
- **文档同步**：SKILL.md/public/skill.md 物理分表描述→单表行级隔离描述
- **skill_check 补漏**：VER_FILES 新增 .skill 后缀文件扫描
- **2026-08-16 补：蒸馏回传 bug 修复（同一 9.2.9 版本内代码修正，不升版本号）**：
  - `pmm_distill.sh` 蒸馏 prompt 拼装误用未定义变量 `${ta}/${ca}/${tb}/${cb}`（函数内仅定义 `title_a/content_a/title_b/content_b`），bash 插值全空 → DeepSeek 收到空 prompt 自判 identical → 误软删不重复记忆（静默数据破坏）
  - 修正为 `${title_a}/${content_a}/${title_b}/${content_b}`，DeepSeek 收到真实内容，判定恢复准确
  - 同步修复管道子 shell 作用域（`done < <(...)` 进程替换），使 `processed` 在父 shell 可见、回传分支正常执行
  - 本地三处副本（实体源/skills/klyc-pmm/scripts、cron 副本 /root/bin、发布包 klyc-pmm.zip 内嵌）已统一
- **2026-08-16 再补：ds-proxy 双实例对称命名**——`klyc-ds-proxy.service`(8775) 重命名为 `yaochi-ds-proxy.service`（瑶池实例，与 `kunlun-ds-proxy.service`(8776) 昆仑实例对称）。已同步：Guardian 巡检 fix、架构页、scripts_RULES.md、MEMORY.md。端口 8775 不变，模型路由 baseUrl 按端口不依赖服务名，无运行时影响。
- **2026-09-04 补：升级流程打通（同一 9.2.9 版本内代码修正，不升版本号）**：
  - `pmm_watch.sh` init 补保存 api_key 到本地 KEY_FILE（原实现只存昆仑令 URL，导致升级认证缺凭据）
  - `pmm_watch.sh` upgrade 顺序对调：先走老 API（余额判定），余额不足才走 X402；`--out-trade-no` 重试改走老 API 查单（与支付表一致）
  - upgrade 认证改用 api_key（`pmm_get_key`），不再用昆仑令 URL（`pmm_get_token`）
  - 后端 `klyc_pmm_upgrade.php` 认证统一走 `auth()`，兼容 api_key 表 + 昆仑令 + 旧 key 三层回退；订单归属校验防冒用

## v9.2.8 — 2026-08-13

- **模型路由定稿**：昆仑主模型稳定为腾讯云 tokenhub DeepSeek V4 Pro（1M/16000），备=官方 deepseek 双 key
- **全服唯一源清理**：klyc-pmm 只保留 webroot 唯一源，全服其他位置副本清理
- **审查脚本通查**：klyc_skill_check.sh 覆盖 14 项检查，全服统一不区分昆仑/瑶池归属

## v9.2.7 — 2026-08-13

- **安全修复（腾讯云安全评估）**：check-and-nudge 不再在 URL 参数中暴露昆仑令 recovery_url，避免凭证经浏览器历史/Referer/代理日志泄露（安全评分 62→目标 90+）
- **护魂符秒级推送修复**：pmm_watch.sh inotifywait 事件从 `close_write` 改为 `close_write,moved_to,modify`，解决 append_file 写入方式不触发 inotify 导致护魂符推送延迟的根因问题
- **全服版本号统一 9.2.7**：149 处旧版本（9.2.5/9.2.6）→ 9.2.7，零残留
- **审查脚本重构**：删除双 workspace 副本，webroot 唯一源，全服统一检查不区分昆仑/瑶池归属
- **两平台上传规则补全**：对照 ClawHub 官方文档 (docs.openclaw.ai/clawhub/skill-format) 补全 13 条硬检查 + TRACE 五维自评
- **ZIP 重打包**：修复双套文件问题，ZIP 内版本号对齐 9.2.7

## v9.2.6 — 2026-08-12

- **LLM 蒸馏下沉到 AI 体**：蒸馏决策从服务器 cron 移到 AI 体，各自用自己的 DeepSeek Key 调用 LLM 判定，平台只做 BGE+Reranker 粗筛 + 存储去重
- **新增 3 个平台 API**：klyc_distill_candidates.php（候选对生成，不调LLM）+ klyc_distill_candidates_status.php（轮询）+ klyc_distill_result.php（结果回传）
- **新增 2 张表**：klyc_distill_tasks（候选对任务）+ klyc_distill_history（蒸馏历史，独立于 klyc_settings 避免单键膨胀）
- **pmm_distill.sh 层9-12 新增 distill_with_llm()**：AI体心跳触发，用自己的 Key 调平台候选对 API → 逐对判定 → 回传结果
- **Reranker 稳定性修复**：_respond() 加 try-except 防 BrokenPipe；候选对筛选加 BGE 硬上限 100 唯一ID + 日记/心跳文件过滤
- **模型路由定稿**：昆仑主=腾讯云tokenhub DeepSeek V4 Pro（1M/16000）、备=官方 deepseek 双 key；瑶池主=HY3、备=DeepSeek V4 Pro（256K/8192）

## v9.2.5 — 2026-08-11

- **铁律 #55 版本升级三步不缺**：14↔17层全站误改事件→版本升级三步不可跳（改VERSION+全站grep、源目录同步、重新打包上传）
- **铁律 #54 改动前先列关联清单**：任何修改（数字/命名/配置/链接）前列出所有关联文件路径，改完逐条对照勾清
- **操作前置硬阻断清单**：7项硬检查（权威来源→RULES覆盖→影响面全扫→关联清单→回滚→验证→泄密检查）
- **版本号全站统一**：config.php KLYC_VERSION + skill包 + 所有脚本注释 = 9.2.5
- **ClawHub + SkillHub 发布**：预检全过→两平台同步推送

## v9.2.4 — 2026-08-10

- **全服清理**：删测试用户4个、物理删除4092条软删除记忆(回收10MB)、清理过期文件(SkillHub临时目录/旧CSS/旧备份)
- **前端合规**：join.php 内联style 6→1（仅头像豁免）、CSS类迁移(.dash-error-hint-lg/.jn-pay-success等)
- **Nginx SEO路由补全**：/services、/admin 伪静态rewrite
- **架构面板**：补klyc-ds-proxy(8775)服务登记
- **安全**：技能文件从webroot移至skills/目录，修正Nginx alias路径
- **14层蒸馏管道复通**：pmm_distill.sh cron交互修复 + opcache污染清除 + cross_distill软链修复 + klyc_memory_conflicts表清理
- **全站版本号统一9.2.4**：网站KLYC_VERSION + skill包 + 所有配置/脚本注释

## v9.2.3 — 2026-08-09（跳过，未发布）

## v9.2.2 — 2026-08-08

- **DeepSeek Key 全自动双备**：OpenClaw/LightClaw 主模型、arena_grader、cron distill 全部实现主备 key 自动切换（主 key 失败 → 切备 key → 恢复切换）；新增 klyc-ds-proxy 外层 key 轮换代理（LightClaw 接入）；PHP-FPM 注入主备 key
- **安全加固**：systemd unit / php-fpm conf / OpenClaw/LightClaw 配置 key 明文全部 root 只读（600+immutable），业务代码零硬编码，备份剥 key

## v9.2.1 — 2026-08-08

- **合规清理（提示词广告推广=0）**：移除包内所有主动付费推销话术——SKILL.md「AI体主动推销护魂符」章节、pmm_boot.sh 启动推销横幅、pmm_watch.sh init 通报与 check-and-nudge 里程碑付费催促话术；保留 upgrade / owner-pay-link / X402 支付等功能本体
- **广告扫描自动化**：klyc_skill_check.sh 新增「提示词广告推广=0」扫描（.sh 脚本 + SKILL.md），出厂前自动拦截推销话术
- **发布工具修复**：ZIP 打包源目录名对齐、SkillHub 用无 LICENSE 副本发布

## v9.2.0 — 2026-08-08

- **根治空钩子**：pmm_hooks_pull 新增失效钩子检测——对比本地已有 ID 与远程有效 ID，发现失效钩子自动标记，保留现场供人工核对
- **新增 hook-check 子命令**：钩子健康检查（`./pmm_watch.sh hook-check [--fix]`）——纯客户端调 hooks API + 本地 grep 比对
- hooks-pull 安全声明更新：仅经用户 API Key 认证拉取本人蒸馏记忆摘要

## v9.1.22 — 2026-08-06

- **修正**：curl 调用去 eval 化（klyc_skill_check.sh 改用 bash 数组传参）
- **修正**：共享域示例去敏感化、昆仑令写入提示措辞修正
- **新增**：klyc_skill_check.sh 十三关全量检测
- **重构**：脚本命名规范化、工作区路径标准化（skills/@user_6e41807a/klyc-pmm/）

## v9.1.18 — 2026-08-05

- **新增**：KLYC_PMM_CONFIG_DIR 环境变量支持——多AI体共享主机时可独立配置目录
- **新增**：hooks-pull 支持 API Key 认证
- **修正**：watch 模式认证兼容（无 token 时自动降级为 X-KLYC-Key）
- 安全声明修正：云鼎实验室安全评估 3 项全清零

## v9.1.12 — 2026-08-04

- **新增**：write-coalescing——inotify 循环增加 30 秒合并窗口 + content_hash 去重（2,950次/8h → ~150次/8h）
- **新增**：SKILL.md watch 章节增加心跳文件最佳实践

## v9.1.10 — 2026-08-04

- **行为变更**：push 命令 --domain 改为必填参数，禁止自动推导
- **行为变更**：watch 模式文件同步 domain 固定为 pmm_sync

## v9.1.9 — 2026-07-31

- **合规**：Pay Skill 安全引擎全绿——移除远程下载覆盖(update.sh)消除"恶意远程执行"三标
- **合规**：定价信息收敛至 frontmatter pricing
- **清理**：删除 update.sh 及所有相关引用

## v9.1.2 — 2026-07-31

- **修复**：agent/register 路由（ai→agent）、昆仑令保存字段（token→talisman_url）
- **修复**：agent/register API peach_balance 100→99、set -u 下 http_code 未定义
- **清理**：移除构建垃圾（publish.sh/根级 pmm_watch.sh/根级 update.sh/sha256）

## v9.0.0 — 2026-07-30

- **新增**：X402 付费前置检查章节——Agent 调用付费功能前检查 weixinpay 插件
- **新增**：frontmatter 增加 pricing 元数据（per_call / amount_fen: 50000 / capability）

## v8.3.9 — 2026-07-29

- **修复**：五个关联数组 dingxinfu key 重复定义（bash 去重导致容灾备份被守护记忆覆盖）
- **修复**：install-daemon.sh 与 pmm_watch.sh tier 映射不一致
- **统一**：三级产品 tier key——dingxinfu(容灾) / huhunfu(守护) / fenshenfu(分身)

## v8.3.8 ~ v8.3.1 — 2026-07-28~29

- 文档与脚本一致性对齐、产品描述命名规范化、curl 退出码细化诊断
- 昆仑令格式自动识别、oneclick.sh 全链路闭环、TRACE 3.5→4.6
