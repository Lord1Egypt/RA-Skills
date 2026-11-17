# Changelog

## 2.4.2 — 2026-11-18 00:55

RetroArch 存档迁出内部存储到 TF 卡（实机已闭环），并按 Ponytail / 技能架构师 / 瘦身师三方审查做结构性整理。

- **✅ 新增 PLAYBOOK §21「存档位置与迁移」**：内部存储只剩 5.8G，RA 即时存档占 681M + `.srm` 19M。迁移到 TF 卡应用私有目录 `.../6AF3-384F/Android/data/com.retroarch.aarch64/files/{states,saves}`，内部存储 5.8G → **6.5G**，TF 卡 101 个 state / 95 个 save 完整。
- **🔴 新增硬性禁令 60**（共 60 条）：存档迁移三坑 —— ①设备上有**两份** `retroarch.cfg`，生效的是 `/storage/emulated/0/RetroArch/retroarch.cfg`（属主 `u0_a92`，应用退出回写），`Android/data/...` 那份是遗留副本，改错等于没改；②RA **无** `MANAGE_EXTERNAL_STORAGE`，读 TF 卡靠 SAF 授权 Roms，存档**不能**放 TF 卡根目录，只能放应用私有目录；③该版本 `log_to_file="true"` **不产生任何日志**，验证只能比文件数与 mtime（内部份 mtime 不动 + TF 份冒新文件 = 写通路通；「读取存档状态」列表非空 = 读通路通）。
- **✅ 新增 `references/SCRIPTS.md`**：22 个脚本的完整索引（用途 / 是否写设备 / 常用参数 / 回滚方式）。`SKILL.md` 只常驻 4 个高频入口，其余按需查。
- **✅ 结构瘦身（三方审查结论落地）**：`SKILL.md` 8817 → 8106 字符，7 步表移入 `INSTALL.md` §3 并**补上「关键判定」列**（原先判据只存在于 SKILL 表里，外移会断链）；专项脚本表移入 `SCRIPTS.md`；前置条件/清理回滚/版本与来源压缩为指针。`按需读取` 路由表扩容到 10 行，新增主题、存档、脚本索引三个入口（避免外移后「知识还在但找不到」）。
- **🔴 修正文档与脚本不一致**：`INSTALL.md` §3 原称 step2 装 kpa-shelf，实际 `step2_theme.sh` 装的是 **prosperoOS**；kpa-shelf 是手工部署的自建主题。三处表述已分开，避免用户跑完一键脚本找不到承诺的主题。
- **✅ 口径统一**：禁令条数 59 → 60（SKILL/README/INSTALL/HARD_RULES/OPTIMIZATION_JOURNEY 全部同步）；`SKILL.md` 正文版本号由 v2.4.0 对齐到 frontmatter。
- **审查中未采纳的建议**（记录理由，便于回溯）：①把常驻区 15 条禁令压到 5 条 —— 这 15 条是「读完再动手就已经造成不可逆损坏」的拦停闸，指针化必然失效；②删 `assets/desc/zh_desc.json`、`assets/meta_latest/` 34 份 —— 属 Cold 层不进上下文，删了会让离线校验与中文简介回填失去默认源，收益低风险高；③删 `assets/themes/kpa-shelf/` —— 该主题是用户实机在用的主力主题，且本轮刚修好 `isPrevPage`；④`description` 压到 45 字 —— 会丢触发词召回。
- **设备侧清理（同轮完成）**：删 2 个已无 ROM 的孤儿存档、27M 旧存档回滚备份、5 份过期配置备份、重复 ROM `二之国：漆黑的魔导士.nds`（124.5MB，md5 与《忍者龙剑传：龙剑》完全一致，天马条目同步移除并清 `dataCache.json`）、`RPG_RT.exe.old`。
- **🔴 顺手抓到一个幽灵条目**：天马报 3729 条但元数据只有 3728 条，差额来自 `/storage/6AF3-384F/Roms/ngage/ngage2.nga` —— 11-16 留下的 0 字节测试占位文件，未被 metadata 引用，但该集合声明了 `extensions: nga`，天马按扩展名把目录里未声明的文件也算成游戏，货架上就多出一个叫 `ngage2` 的条目。删除后清缓存重启，`3728 games found` 与元数据对齐。**教训**：`Roms/<平台>/` 里任何匹配 `extensions` 的零字节占位都会被当成游戏，测试文件用完必须删（禁令 14 的延伸）。
- **基线更新**：文档中的当前态由 3729 改为 **3728**（SKILL / README / VERIFICATION 11-18 基线块），11-16 的 3729 作为带日期的历史快照保留。

## 2.4.1 — 2026-11-17 23:15

修复天马 L1 不切平台（KPA 实机 2026-11-17 验证）。

- **🔴 根因**：kpa-shelf 主题把「L1 上一平台」写成 `api.keys.isPreviousPage(ev)`，Pegasus 官方方法名是 **`isPrevPage`**（`src/backend/model/keys/Keys.h`：`KEYVEC_PROP(PREV_PAGE, prevPage, isPrevPage)`）。方法不存在 → `kIs` 静默退化到 `ev.key === Qt.Key_PageUp` → 手柄 L1 的键值 **1048580** 永远不相等 → L1 完全无反应，而 R1 走对的 `isNextPage` 一直正常，表现为「只有 R1 管用」。
- **✅ 修复**：`assets/themes/kpa-shelf/theme.qml` 改为 `isPrevPage`，并加注释说明拼写陷阱；已同步到掌机（md5 一致）并重启天马验证，L1/R1 双向切平台正常。
- **✅ 新增硬性禁令 59**（共 59 条）：主题调 `api.keys` 必须用官方方法名，附全量方法名清单与 `GamepadKeyId` 键值表（A=1048576…L1=1048580、R1=1048583）。同时记录 `kIs` 的 try/catch 兜底会掩盖拼写错误、Qt 不热重载 theme.qml 必须重启天马、覆盖设备文件用 `cat >` 保留 `u0_a92:media_rw` 权限。
- **✅ 口径统一**：禁令条数 58 → 59（SKILL/README/INSTALL/OPTIMIZATION_JOURNEY 全部同步）。
- **排查留痕**：`getevent` 证明 BTN_TL DOWN/UP 干净、天马 `[KEY] 1048580` 照常打印 —— 硬件与键值都对，问题纯在 QML 层。别再把这类现象当硬件故障。

## 2.4.0 — 2026-11-16 23:05

新增 EKA2L1 / N-Gage 1.0+2.0 支持（KPA 实机 2026-11-16 验证）。

- **✅ 新增 `references/EKA2L1_NGAGE.md`**：官方 EKA2L1 v0.1.0 部署、三设备 devices.yml、`config device` 唯一设备开关（intent 的 `appDeviceCode` 实测完全无效，`device:0` 通用 1.0/2.0）、1.0 原生 app 装 E 盘流程、2.0 无法手工预装（adler32 bug，只能整体恢复数据盘）、天马 NGAGE 入口+官方封面+dataCache 重建、ScaleType 满高语义、FUSE tar `--no-same-owner`、首次启动设置页点「开始」等完整成功流程与踩坑。
- **✅ 实机成果**：新增贪食蛇 Snakes（0x101FD3F7）/ 文明 Civilization（0x101FD42A）两个 1.0 游戏，配官方封面；天马 NGAGE 19→21 入口，端到端从天马点击直达游戏验证通过。
- **✅ 新增硬性禁令 58**（共 58 条）：设备只由 config device 决定、appDeviceCode 无效，2.0 手工预装/intent 直进均不可行。
- **✅ SKILL.md**：版本号 2.4.0、description/trigger 补 EKA2L1 关键词、按需读取表与关键技术事实各加一条速查。
- **✅ 发布前审查优化（Ponytail + skill-architect + agent-slim 三角色）**：
  - `SKILL.md` 常驻正文 **21358 → 8921 字符（-58.2%）**，估算常驻 token 约 12815 → 5353。外移原则：保留身份、核心判断尺（禁令前 15 条）、路由表、一键安装、7 步流程；`版本与来源`里堆积的 12 版完整变更日志改为指向本文件，`关键技术事实`由 18 条压到 6 条最高频（其余 PLAYBOOK 已有全文），健康基线移入 `VERIFICATION.md`。
  - `description` 里 60+ 个堆砌触发词收敛为 15 个核心场景词（KPA / 天马 / RetroArch / PPSSPP / EKA2L1 / N-Gage / 竖版方向 / 核心装不上 / 封面简介缺失 / 退出不回原位 / 缓存清理 / 一键安装等），具体故障句移入 `trigger` 列表。
  - 删除 `references/PROCESS_REVIEW.md`（45K）：与 `OPTIMIZATION_JOURNEY.md` 为同源两代复盘，其独有内容「用户三次纠正」的完整溯源已浓缩并入 `OPTIMIZATION_JOURNEY.md` **§5.1**，其余被 PLAYBOOK 覆盖。全包引用点已同步改指。
- **🔴 修正长期失真的事实口径（发布硬伤）**：
  - **禁令条数**：`HARD_RULES.md` 正文实为 58 条（编号 1–58 连续），但标题写「44 条」，SKILL.md 写「57 条」和「43 条」，README/INSTALL 写「57/55 条」——同一件事五种口径。现全部统一为 **58 条**，并在标题补编号-主题对照说明。
  - **游戏/平台数**：SKILL.md 内有 3706 / 3736 / 3769 三个值，README 写 3,706。**2026-11-16 设备逐平台实测为 36 平台 / 3729 条**，已据此统一当前态表述；`VERIFICATION.md` 顶部新增 11-16 基线块，并注明 3706/3708/3769/3,736/3,773 均为带日期的历史快照、不得当作验收线。
  - 新增本条 `OPTIMIZATION_JOURNEY.md` §5.1，把三次用户纠正从「散落的复盘」变成「可引用的禁令溯源」。
- **🔒 发布脱敏**：移除 `EKA2L1_NGAGE.md` 里的本机绝对路径与设备序列号；本机标准目录改用 `$HOME` 中性表示；`adb input` 类技术词与占位符改为「目录 + 节点」等价表述。`check_release.py --skillhub` 预检 **problems=0**。

## 2.3.0 — 2026-11-15 08:30

「总结优化流程 → 一键安装 → 蓝标系列图示 → 上传」。本轮不改动掌机，产物全部可复现、可审计。

- **✅ 一键安装通道**：新增 `scripts/kpa_oneclick.sh`（只读前置体检 → 设备/本机双回滚点 → `step1~step7` 幂等 → 自动清 `dataCache.json` 重启天马 → `kpa_health_check.sh` 静态校验 → `report.md` 含人手验收清单），支持 `--dry-run`（设备离线也能预览）、`--verify-only`、`--steps 3,4`；`bash -n` 与 dry-run 均已实测通过。
- **✅ 新增 `INSTALL.md`**：从零到可验收的最短路径、7 步职责表、成功判据、必须人手确认 5 项、最易踩的 10 条禁令、六阶段优化流程总结、回滚命令。明确区分「通用安装」与「特定机器数据修复」。
- **✅ 蓝标（Blueprint Badge）系列图示**：核对 `@user_43faedd6` 账号 15 个 SkillHub 图标（本机 `icon.png` 与线上像素 diff=0.00），采样色板 `#0A1F3C` 网格底 / `#49D0FF` 亮青线稿；新增 `scripts/blueprint_icons.py` 生成器，产出根目录 `icon.png`（512×512）+ `assets/blueprints/` 4 张同风格图示（7 步流程 / 配置分层 / 验收边界 / 排障决策树）+ 256 副本，`--check` 校验 6/6 通过。**实测 SkillHub 发布包拒绝 png**：6 张图改走 `/api/v1/skills/<slug>/comments/images` 上传 COS，文档用绝对 URL 引用并留 `URLS.md` 清单；主图标 `iconUrl` 在 publish payload 里携带，发布后回查确认。
- **✅ 新增硬性禁令 56–57**（共 57 条）：禁止把特定机器的一次性修复塞进通用安装；记录 SkillHub 二进制文件限制、COS 上传链路与蓝标规范。
- **✅ 文档同步**：`PLAYBOOK` §20（一键安装 SOP + 不进脚本的特例清单）、`OPTIMIZATION_JOURNEY` §16（沉淀阶段）、`VERIFICATION` 顶部自检说明、README/SKILL.md 触发词与入口。
- 当前设备基线未变：**35 平台 / 3706 条**，ROM 与封面缺失 0；设备在本轮开始时已离线，本轮未做实机改动。
- **发布状态（2026-11-15 08:35）**：`POST /api/v1/community/skills/publish` 返回 `201`、`fileCount=90`、`contentAuditStatus=pending`，账号列表版本已显示 2.3.0、`stats.versions` 由 3 变 4；但详情 `latestVersion` 仍为 2.0.2、`iconUrl` 仍 `None`（审核队列中，见 `HARD_RULES` 57）。服务端按扩展名拒绝 `.png/.opt/.orig/.verified`，发布时把 10 个受限文本文件追加 `.txt` 并留 `assets/PATH_MAPPING.md` 映射表，6 张 PNG 走 COS 绝对 URL（`assets/blueprints/URLS.md`）。

## 2.2.6 — 2026-11-15 01:40

用户二次反馈 5 项：PS 月下打不开 / GBA 封面还是不对 / N64 方向键还是不行 /《钟表骑士》删除 / VARCADE 弹窗确认消失。工作目录 `work/fix13-20261114/round2/`。

- **🔴 更正 2.2.5 的重大误判（禁令 48）**：上轮把 213 张 `500×315` GBA 封面按尺寸一律判为占位图并换成文字卡，实际其中 **54 张是真实日版盒绘**，被误删正是用户「还是不对」的原因。改用粗色桶数 / 高频细节量按内容分类，真盒绘原样恢复。
- **✅ GBA 封面重做**：拉取 libretro-thumbnails GBA 5961 个盒绘清单，中文名→精确英/日文标题映射 178/213，下载校验 141 张；按「原备份真盒绘 54 → libretro 137 → 精修卡 22」统一生成 480×640 封面卡，实机货架截图确认全部为真盒绘、中文名清晰、无空白格。
- **✅ N64 方向键根因（禁令 51）**：`input_player1_analog_dpad_mode` 是 analog→dpad，上轮改 `=1` 无效；改为 `=0` 并把 `h0*` 绑到 `input_player1_l_x/l_y_*_btn`，让十字键驱动 N64 读取的左摇杆。
- **✅ PS 月下定性（禁令 52）**：60s 汉化片头 → 75s「音乐欣赏模式」，用户只等 54s；零崩溃。已在该游戏 description 写明等待提示。
- **✅ 删除土星两作（禁令 53/54）**：CHD / 封面 / metadata / 历史引用同步清理，本机与设备双备份，回归验证《守护英雄》正常。
- **✅ VARCADE 弹窗用户确认消失**，闭环。
- 新增硬性禁令 51–55（共 55 条）、`PLAYBOOK` §19、`OPTIMIZATION_JOURNEY` §15；`VERIFICATION` / `README` 基线更正为 **35 平台 / 3706 条 / 332 条热门置顶**。

## 2.2.5 — 2026-11-15 01:00

用户一次给出 **13 项体验问题清单**（VARCADE 启动弹窗 / DOS 要选 exe 且大唐英雄传进不去 / 每平台热门 10 款置顶 / MSX 无遮罩 / ATOMISWAVE 动物篮子竖版按键 / 删除 VB / PS·PSP 按键 / GBA 无封面 / 土星钟表骑士 / PICO 无遮罩 / N64 按键与封面 / MD 光明力量 1·2 / FC 兵蜂封面）。按「只读盘点 → 分组修复 → 单点验证 → 批量推广 → 全库复核」执行，工作目录 `work/fix13-20261114/`。

- **✅ DOS 免选 `.exe`（最大突破，推翻此前「只能人手 Set Auto Start」的结论）**：`DOSBox-pure.opt` 的 `dosbox_pure_conf` 合法值 `false|inside|outside`；设 **`outside`** 后在 `Roms/DOS/` 放同名 `.conf`，`[autoexec]` 执行包内 `PLAY.BAT` 即可直接进游戏。只读解出 15 个 `.dosz` 的 ZIP central-directory 与 `PLAY.BAT` 内容（尾部 tail + raw deflate，不用 pull 488MB），单点验证《毁灭战士2》9s 直接出 id Software 标题画面后批量推 15 份；抽样 8 款全部直进、无崩溃。
- **✅ 《大唐英雄传》SIGSEGV 救援**：崩溃在 `core_load_game+156`（载入阶段，与启动脚本无关）。本地校验 1010 条目全合法 → 用「只打包前 N 条」二分 10 轮定位 **`GAME.IMG`（307200 = 崩溃寄存器 `x19`）** 被核心误判为软盘镜像后末尾越界读；**尾部补 1 个 `\0`** 重建完整包即不崩。再定制 conf 修正原 `PLAY.BAT` 的两处 DOSBox-Pure 不兼容（`-T ISO` 大写 + 末尾 `MOUNT -U D`）：`IMGMOUNT D CDROM.ISO -t iso` → `midi sb220` → `nlb`，实机出「大唐英雄傳」标题画面。原件备份 `/sdcard/backup/fix13-dos-auto/`。
- **✅ 遮罩**：MSX 病因是 `blueMSX/` 只有 `.opt` 没有 cfg → 补 `MSX_B.cfg`/`MSX_B_frame.png` + 核心级/per-game cfg；PICO 病因是核心级与 per-game cfg **全不生效** → 新建 `retroarch_pico.cfg` 并改 PICO `launch` 的 `-e CONFIGFILE`。两者实机截图均确认生效（红细线 + 竖排 `MSX` / `PICO-8`）。PICO-8 原生 128×128 正方形，「有竖版游戏」不成立。
- **✅ VARCADE**：蓝底旋转 `DIP SWITCH SETTING` 是游戏自检画面（22s 已到 TAITO 片头），非 OSD；`MAME 2003-Plus.cfg` 关闭 `savestate_auto_save` / `rewind_enable` / `video_font_enable` 消除存档失败类文字提示。
- **✅ MD《光明力量 1/2》**：`.md` 文件头 `PK\x03\x04` 实为 ZIP 伪装，解出内层真 ROM 替换，两作实机均进游戏。
- **✅ 封面**：GBA 静态缺失为 0 但用户仍报「很多没封面」→ 真因是 213 张 `500×315` 纯文字横条占位图，按尺寸精确识别后换 480×640 竖版卡；《兵蜂》（原为电路图）、《动物之森》（原为鹿照片）换 libretro-thumbnails 真盒绘（GitHub raw 超时改 `cdn.jsdelivr.net/gh/...`）。
- **✅ 热门置顶 / 删除 VB / 按键配置**：`sort-by: 01 … 10` 写入 35 份 metadata 共 **334 条**，覆盖 35/35 平台；`Roms/VB` 已删（本机 `VB-backup/` 57 文件 44M，⚠️ 设备侧备份失败，仅此一份回滚点）；`动物篮子.cfg` 竖版映射、PPSSPP `controls.ini`（D-pad 同时驱动摇杆 + Y=方块/X=三角/A=圆圈/B=叉）、`胜利十一人2002.rmp`、N64 `input_player1_analog_dpad_mode="1"` 均已落地。⚠️ **实体键手感仍待用户实机确认**。
- **❌ 未解决：土星《钟表骑士》/《钟表骑士 2》**。四个土星核心全黑屏、四个 CHD 头部同为合法 v5；Beetle Saturn 关卡+锁日区能进 BIOS 的 CD 播放器界面但显示 `TRACK 00` → **镜像无有效 Saturn 引导区**，属坏 dump，需换 CHD 或删条目。实验改动已恢复并回归验证《守护英雄》正常。
- **✅ 全库静态复核（删 VB 后新基线）**：**35 平台 / 3708 条**；`file:` 与 `assets.box_front:` 各 3708、缺失均为 **0**；334 条热门 `sort-by` 覆盖 35 平台；设备文件 25481；`dataCache.json` 已清并重建。
- 新增 `HARD_RULES` 第 **45–50** 条（共 **50** 条）、`PLAYBOOK` **§18**（13 项 SOP / 二分定位 / 全库复核口径）、`OPTIMIZATION_JOURNEY` §14、`VERIFICATION` 基线更正；`SKILL.md` 版本、描述、触发词与平台数字同步。
- ⚠️ 踩坑记录：重建 ZIP 时把 `ZipInfo` 直接传 `writestr` 会原地改写 `header_offset`，导致下一轮误报 `Overlapped entries (possible zip bomb)`（假警报，须 `copy.copy`）；`apply.sh` 曾把 PPSSPP 私有目录误写成 RA `$SYS`，已手工修正并 md5 回读。

## 2.2.4 — 2026-11-14 22:50

- **新故障「CPS3 也有部分按键不正确」：根因与 CPS1 完全不同，在核心选项 `.opt` 而不是 cfg**。CPS3 走 `fbalpha2012_cps3` 核心，其核心级 `FB Alpha 2012 CPS-3.cfg` **没有任何 `input_player1_*` 行**（继承全局标准，本来就是对的），也没有 per-game cfg / remap；所以 2.2.2/2.2.3 那套「核心级竖版映射污染」修复对它无效，⛔ 不要给它补写那 4 行按键。
- **真正根因**：`config/FB Alpha 2012 CPS-3/FB Alpha 2012 CPS-3.opt` 里 `fbalpha2012_cps3_controls_p1 = "gamepad"`（核心默认值）。FB Alpha 2012 CPS-3 是唯一带「P1/P2 control scheme; gamepad|arcade」与「L/R gamepad scheme; normal|remap to R1/R2」选项的街机核心；`gamepad` 把 6 键格斗打散成手柄三角布局，与用户按街机面板/CPS1 习惯的「三拳三脚」不一致。
- **源码级映射（libretro/fbalpha2012_cps3 `svn-current/trunk/src/burner/libretro/libretro.cpp` 1387–1469 行，`bStreetFighterLayout` 分支）**：`gamepad + normal` → fire1=Y / fire2=X / fire3=L / fire4=B / fire5=A / fire6=R（机身 A/B 出的是**脚**）；`arcade` → fire1=A / fire2=B / fire3=X / fire4=Y / fire5=L / fire6=R（轻中重拳 + 轻中重脚，标准街机 6 键）。`arcade` 下 `lr_controls` 对 6 键不生效；⛔ 若开 `remap to R1/R2` 会把按键挪到 `R2/L2`（Android 105/104），而全局 `input_player1_l2_btn/r2_btn = "nul"`，会直接没反应。
- **已改（仅 2 行）**：`controls_p1` / `controls_p2` `gamepad → arcade`；`lr_controls_p1/p2 = "normal"` 及其余 11 行一字未动。备份设备 `/sdcard/backup/cps3-keyfix-20261114/`、本机 `work/cps3-keyfix-20261114/{before,after,verify}/`；先 `rm` 再 push、pull 回读 md5 一致。定稿存 `assets/ra-cps3/CPS-3.opt`。
- **验证边界**：`am force-stop` 后冷启动 `sfiii3.zip`（60fps、正常进区域警告画面），证明 `arcade` 是合法值、核心加载与游戏启动无异常；`am force-stop + am kill` 后进程为空、焦点回天马、`.opt` 再 pull md5 一致**未被写回覆盖**。⚠️ **实体按键仍需用户实机确认**（adb 注入按键 RA 全不接收）。
- 新增 `HARD_RULES` 第 **44** 条（共 **44** 条）、`PLAYBOOK` §17（含 6 键映射对照表与 SOP）、`OPTIMIZATION_JOURNEY` 遗留项补记；`SKILL.md` 版本/描述/触发词/街机条目同步。⛔ 设备其他配置、天马 dataCache、playlist 均未动。

## 2.2.3 — 2026-11-14 22:35

- **✅ 44 条 RA 播放列表孤儿死引用已清理**：按正确口径复核后精确锁定 5 个 playlist（FBNeo 14 / Handheld Electronic Game(GW) 19 / MAME2010 8 / Game Gear 1 / PSP 2），条目 2,498→**2,454**，设备侧复查 **DEAD=0**。逐文件 `rm` 后 push、pull 回读 md5 全一致；备份在设备 `/sdcard/backup/playlist-clean-20261114/` 与本机 `work/playlist-clean-20261114/{before,after}/`。天马 3,736 条、启动失败 0、PSP `file://` 0 均未变（天马不读 playlist）。GW 的 19 条对应整个已移除平台（TF 卡 `.mgw` 文件 0 个）；PSP 2 条是去重时删掉的 TF 卡 ISO；`Handheld Electronic Game.lpl` 与 `Sony - PlayStation Portable.lpl` 现为空列表但保留文件（可逆）。10 条「同名文件在别的平台目录」也一并删除而非改写路径：core_path 与 romset 归属不同，改写反而可能让核心跑错 ROM（禁令：不同核心 romset 不能乱合并），且这些路径本身已不存在、RA 内点了必然失败。
- **⚠️ 重大口径更正：GBA playlist 的 153 条不是死引用**。`Nintendo - Game Boy Advance.lpl` 是**混合编码**：`path` 里 `#` 之前是 UTF-8 的 zip 路径、`#` 之后是 GBK 的 zip 内条目名，严格按 UTF-8 解析会 `UnicodeDecodeError`，用 latin-1 强读会把中文路径变成 mojibake，从而误判 153 条死引用。正确做法：`decode('utf-8', errors='surrogateescape')` 保字节 + SAF URI 双重 percent-decode + **只取 `#` 之前的文件系统路径**再比对。按此口径全库恰好 44 条，GBA 一条都不涉及。⛔ 绝不能因编码问题批量删 playlist 条目。
- **街机核心级 cfg 污染：精确核定 + 推广收尾**。全设备 `a=109` 的文件有 **226 个**，但绝大多数是**竖版 per-game cfg（设计如此）**；真正「文件名==目录名」的核心级污染只有 **4 个**：`FB Alpha 2012 CPS-1`、`FB Alpha 2012 CPS-2`、`FB Alpha 2012 NeoGeo`、`FinalBurn Neo`。本轮把 CPS-2 / NeoGeo 两个也改成全局标准，至此 4/4 统一为 `a=96 / b=97 / start=108 / select=109`，设备读回一致。
- **⚠️ 撤销 2.2.2 的一处误判**：`FinalBurn Neo/FBNEO {ACT,STG,FLY,ETC} V.cfg` 是**竖版分类配置**（`aspect_ratio_index=24`、V=Vertical），其 `a=109` 是竖版正确设计，**不是污染，一律不动**；CPS-3 核心级 cfg 无自定义按键。48 个核心级 cfg 中其余 43 个都继承全局、无自定义映射。
- **依据与状态**：用户 22:16/22:23 试 CPS1 `captcomm`（修前）、22:25 试 CPS2 `armwar`、22:29/22:31 试 CPS3，随后要求「继续」，据此按同源结构推广到 CPS-2/NeoGeo。⚠️ **仍需用户实体键确认** 4 个街机平台的 A/B/Start/Select；本机 adb 注入按键 RA 全不接收（禁令 12）。改 cfg 时 RA 正在前台运行，**未 force-stop**（不打断用户），改动对已启动的游戏不生效、下次启动生效；✅ 22:37 RA 退出回到天马后已复核：4 个核心级 cfg 仍为 `a=96`、5 个 playlist md5 全一致，**均未被写回覆盖**。
- 新增 `HARD_RULES` 第 43 条、更正第 42 条（共 **43** 条）；`PLAYBOOK` 新增 §16 播放列表清理 SOP、更新 §15；`OPTIMIZATION_JOURNEY` 新增 §12 并更新 §11；`VERIFICATION` 顶部标注同步。
- **未动项**：4 个核心级 cfg 的 `input_overlay_enable="true"` + `ARCADE_B.cfg`（横版仍盖虚拟按键遮罩，竖版 per-game 已 false），是否关闭仍待用户定夺。

## 2.2.2 — 2026-11-14 22:25（⚠️ 部分结论已由 2.2.3 更正：FBNEO V 分类 cfg 不是污染；CPS-2/NeoGeo 已于 22:35 一并修复）

- **新故障「CPS1 横版游戏的按键不对」**：根因不是竖版 cfg，而是 **5 个街机核心级 cfg 里写着竖版专用的 A/B/Start/Select 重映射**（`a=109 / b=108 / start=97 / select=96`），横版游戏继承后全部错位 —— 按机身 A/B(97/96) 变成 Start/Select，要按 Select/Start(109/108) 才出拳跳。全局主配置是 `a=96 / b=97 / start=108 / select=109`，其余 43 个核心级 cfg 都继承它、没有自定义按键。
- **实机分布**：48 个核心级 cfg 中仅 **5 个**带这套映射 —— `FB Alpha 2012 CPS-1` / `FB Alpha 2012 CPS-2` / `FB Alpha 2012 NeoGeo` / `FinalBurn Neo`（+ `FBNEO ACT/STG/FLY/ETC V` 分类 cfg 同源）；CPS-3 无。CPS1 平台 29 条横跨两个核心：前 12 条用 `fbalpha2012_cps1`、后 17 条用 `fbneo`，**26 个横版全被污染**，3 个竖版（1941/mercsj/varth）有 per-game cfg 显式覆盖、不受影响。
- **已改（仅 2 个核心级 cfg 的 4 行按键，值改为全局标准）**：`config/FB Alpha 2012 CPS-1/FB Alpha 2012 CPS-1.cfg`、`config/FinalBurn Neo/FinalBurn Neo.cfg`；3 个竖版 per-game cfg md5 未变。备份在设备 `/sdcard/backup/cps1-keyfix-20261114/` 与本机 `work/cps1-keyfix-20261114/{before,after}/`，push 后 pull 回读 md5 一致。
- **⚠️ 影响面与未闭环**：改 `FinalBurn Neo.cfg` 会同时作用于 FBNEO/NEOGEO 等所有用该核心的横版游戏（同为错误映射，属修复非破坏），但**未经用户实机确认**；CPS2 / NeoGeo 两个核心级 cfg 的同类问题**尚未改**，等确认后推广。⛔ 本机 adb 注入按键 RA 全不接收（禁令 12），无法远程验证，只能请用户用实体键试 `dino`（CPS-1 核心）和 `sf2`（FBNeo 核心）。
- 未动项：`FB Alpha 2012 CPS-1.cfg` 里 `input_overlay_enable="true"` + `ARCADE_B.cfg`（横版仍显示虚拟按键遮罩，竖版 per-game 已设 false）—— 是否一并关闭待用户定夺。
- 新增 `HARD_RULES` 第 42 条、`PLAYBOOK` §15；共 **42 条**硬性禁令。回滚：把 `before/` 两份 cp 回原路径即可。

## 2.2.1 — 2026-11-14 22:20

- **全库验收审计（只读，回答用户三问：各平台能否完美运行 / 历史要求是否达成 / 多余数据是否清完）**：36 平台 3,736 条，ROM 与封面缺失 0、简介 3,736 条且模板句 0、launch 36/36、启动失败 0、竖版 219/219、BIOS 370 个齐全、`.state.auto` 0、本机废纸篓 0 项。结论：**配置与启动链路全绿，但不等于逐条试玩过 3,736 个游戏**；库内仍有 1 个确认坏 ROM `WS/恐怖传说.zip`。
- **新发现 44 条 RA 播放列表孤儿死引用**（GW 19 / FBNeo 14 / MAME2010 8 / PSP 2 / GG 1），天马不显示但 RA 内点会失败。已出清单，当时未删；**✅ 22:35 已清理完毕，见 2.2.3**。
- **口径校准**：实测简介模板句 0、废纸篓已空，据此更正 `VERIFICATION.md`、`OPTIMIZATION_JOURNEY.md` §9、`SKILL.md` 健康基线里「3,570 / 1,142 条空壳简介」「废纸篓待清」等过时结论；新增 `OPTIMIZATION_JOURNEY.md` §11 审计快照。
- 仅清理本会话自建的两个临时探针 `/data/local/tmp/{check.sh,tf-paths.txt}`（12K→0），设备其余配置零改动。禁条数仍 41。

## 2.2.0 — 2026-11-14 22:05

- **新增 `references/OPTIMIZATION_JOURNEY.md`**（用户要求「总结修改优化的过程，加入到 skill」）：六阶段全过程时间线（11-12 基础落成 → 11-13 体验修复 → 11-14 上午全库整理 → 下午清理去重 → 傍晚回归修复 → 晚交互闭环）、量化成果对照表、9 条可复用方法论、**10 条失败与更正清单**（含两次假验证、BOM 与写回推测被证伪）、遗留项索引。
- **新增只读机能体检基线（21:59 采集，未改设备）**：MT6785V/CD + Mali-G76 MC4、2.82GB RAM（zram 1.55GB 已用 520MB）、960×640@60Hz、内置剩 7.9G / TF 剩 30G、36 平台 3,736 条、RA+PPSSPP 均 Vulkan、492 进程 / 56 服务、`top` 707% idle、`/proc/loadavg` 22.69 系 Android 冻结进程计入不可当过载。
- **判断：没有把机能发挥到极致，但属合理保守**。库组织 / 元数据 / 稳定性 / 启动退出闭环 / 后端选择已接近做满；最大余量是 PPSSPP `InternalResolution = 1`（480×272，屏幕 960×640），其次是 3GB RAM 的内存与后台压力。硬拉 3×/MSAA/超频会撞内存与散热上限，不建议。
- **§8 分级优化候选全部仅为建议、未执行**：🟢 PSP 2× / 主配置 rewind+auto save 关 / 重启 / 废纸篓清理；🟡 关闭拉伸改 16:9 / `TextureBackoffCache` / swapchain 2 / `audio_latency` 64 / 后台治理（⛔ 不动 `com.ayaneo.home`）；🔴 3× / MSAA / 超频 / 批量更核心 / 合并 56 组同名。
- 配套：修正 `SKILL.md` 与 `README.md` 里残留的「40 条 / 27 条禁令」口径为 41 条，登记新文档索引；今日工作日志追加。禁条数仍 41，脚本与设备配置零改动。

## 2.1.9 — 2026-11-14 21:50

- **✅ 闭环：PSP 游戏已可退出回天马**（用户实体键实测反馈「可以退出到天马了」）。2.1.8 下发的 `assets/ppsspp/` 配置生效；退出后回读设备 `mCurrentFocus=org.pegasus_frontend.android/.MainActivity`，证明天马窗口在后台、PPSSPP `finish()` 后系统自然回前台，无需守护脚本。
- **实机配置回读（source of truth）**：PPSSPP 退出时把内存配置规范化写回，两份 ini 都自动加了 UTF-8 BOM；`ppsspp.ini` 更新 `RunCount 10→11`、`FileName0` 改为最近游玩的 `实况足球 2009.cso`、去掉为覆盖残片补的尾随空行；**所有自定义键原样保留**（`AskForExitConfirmationAfterSeconds=0`、`PauseMenuExitsEmulator=True`、`AllowMappingCombos=True`、`StrictComboOrder=False`、`GameLanguage=11`），`controls.ini` 仅多 BOM、`Exit App` 24 组完整。定论：PPSSPP 会规范化 ini 但**不会吞掉自定义键**，18:55「退出时写回覆盖导致配置失效」的担忧不成立。
- **⚠️ 证伪 18:55 的 BOM 推测**：PPSSPP 自己写回的配置就带 BOM 且配置生效，所以「BOM 让 ini 段被当成未知段、导致语言向导常驻」是错的；`GameLanguage=-1 → 11` 也不是语言框触发条件。真正原因只是**远程 adb 注入按键在这台设备上仅 BACK(4) 有效**，实体键可以正常穿过模态层。⛔ 别再把「远程点不动 UI」推断成「设备 UI 有问题」或「配置没读到」。
- **未区分项**：用户反馈只确认「能退出回天马」，未说明是 `Exit App` 组合键直接命中，还是 `PauseMenuExitsEmulator` 兜底（BACK → 暂停菜单 → 返回主菜单）生效；两条路径均已配置可用，不影响交付。
- 资产：推送定稿 `assets/ppsspp/{ppsspp.ini,controls.ini}`（无 BOM）、实机生效基准 `*.verified`（PPSSPP 回写版）、原版备份 `*.orig`，同步 `work/meta/PPSSPP/`。`HARD_RULES` 41 条状态行、`PLAYBOOK` §14 标题与新增 §14.6 已标注闭环；禁条数仍 41。

- **退出落点已确认（21:55 追加）**：21:49 从天马启动「实况足球 2009」（`coll 33 / idx 1`），退出后 `lastrun.log` 出现 `qml: [SHELF] resume coll=33 idx=1 title=实况足球 2009`；截图 `shots/after-exit-landing.png` 显示左侧选中「索尼 PSP」(4)、红框停在实况足球 2009（2/4）、底部信息条是该游戏详情（已玩 14 次）。即**主题 `api.memory` 的 Shelf Collection + Shelf Game 恢复机制对 PPSSPP 独立 App 同样生效**：游戏启动后主题整体重载，返回时精确回到原平台原游戏，无需守护脚本或额外定位逻辑。

## 2.1.8 — 2026-11-14 18:55（✅ 退出配置已于 21:50 实机确认，见 2.1.9）

- **媒体库重扫（已完成）**：`content call --uri content://media --method scan_volume --arg external_primary` 与 `--arg 6af3-384f`（卷名必须小写）。两个卷 `REASON_DEMAND` 扫描成功；TF 卡 25,842 条索引逐路径比对**死索引 0**（已删 PSP ISO/CSO 的旧记录早被首次扫描清掉），`DocumentsProvider: Missing file` 归零；`.nomedia` 齐全，全库仍 3,736 条。
- **PPSSPP select+B 退出（配置已下发；✅ 21:50 用户实体键确认可退出回天马，见 2.1.9）**：新增 `assets/ppsspp/{ppsspp.ini,controls.ini}` 定稿与 `.orig` 原版备份，同步 `work/meta/PPSSPP/`。配置依据 PPSSPP 1.19.3 源码：`AskForExitConfirmationAfterSeconds = 0`（UI 里 0 = Off）、`AllowMappingCombos = True`、`StrictComboOrder = False`、`PauseMenuExitsEmulator = True`；`Exit App = <dev>-109:<dev>-96,...` 覆盖 deviceId 0/1/10~19 与 B 键 96/97。
- **远程验证受限（历史记录，✅ 已由 21:50 实体键实测闭环，见 2.1.9）**：本机 `adb` 注入按键（含 `input keyevent` / `tap` / `motionevent` / `sendevent`）只有 BACK(4) 有效，无法模拟实体 select+B；且 PPSSPP 冷启动有常驻模态「语言」层，`EmuScreen::OnVKey()` 的 `IsOnTop()` 判定会丢弃虚拟键。因此当时**只能请用户用实体键实测** —— 结果通过。上轮 2.1.7 的「实机验证」教训继续适用：远程注入 ≠ 实体键。
- **新坑**：`adb push` 到 `/Android/data/<pkg>/files/` 不截断，推更短文件会留下旧文件尾部残片（实测 controls.ini 残留 `97\n9:0-97\n`），且 shell 无权 `rm`；必须让新文件不短于旧文件并 `pull` 回来做 md5 比对。
- 新增 `HARD_RULES` 第 41 条、`PLAYBOOK` §14；共 41 条硬性禁令。

## 2.1.7 — 2026-11-14 17:35

- **修复「PSP 没法玩了」回归（用户实机反馈）**：去重后从天马点 PSP 游戏无反应。根因不是 ROM 丢失、也不是 `.app` 占位 —— 而是 `launch` 里的 `-d "file://..."` 被 Pegasus 构造成 `Intent.setData()`，Android 7+ StrictMode 抛 `android.os.FileUriExposedException`，PPSSPP 根本没被启动；`lastrun.log` 里 17:14 两次点击都有该异常。
- **⚠️ 作废 2.1.6 的 PSP 验证结论**：上一轮用 `adb shell am start` 直启做「实机验证」是假验证（shell 不受 App 级 VmPolicy 约束），只证明命令本身能跑，没证明从前端能点开。「每条独立 `launch` 一个字都不要动」的说法错误 —— 恰恰必须改。
- **修法**：4 条 per-game `launch` 改为 PPSSPP 快捷方式 extra：`am start --user 0 -n org.ppsspp.ppsspp/.PpssppActivity --es "org.ppsspp.ppsspp.Shortcuts" "<绝对路径>"`；collection 级兜底去掉 `-d` / `-a`，只留 `-n`。依据 PPSSPP 1.19.3 `PpssppActivity.parseIntent()`：无 `getData()` 时读 `SHORTCUT_EXTRA_KEY = "org.ppsspp.ppsspp.Shortcuts"` 当启动路径。
- **四条全部冷启动实机验证**：山脊赛车（前端点击 → Ridge Racer 开场）、战神（Ready at Dawn Logo）、侠盗猎车（含空格）、实况足球（含空格）均出现 `NativeApp.init(): Launch shortcut parameter:` + `[BOOT] Booted`；`FileUriExposedException` 0、`Failed to run the launch command` 0、全库仍 3,736 条。
- 同步修正 `assets/meta_latest/PSP.txt`、`scripts/step5_ppsspp.sh`（新增幂等修复路径，旧 `file://` launch 自动转 extra）、本机镜像 `work/meta/PSP/metadata.pegasus.txt`；`HARD_RULES.md` 更正 37/38、新增第 40 条（共 40 条）；`PLAYBOOK.md` 新增 §13；`SKILL.md` 版本 / 描述 / 触发词同步到 2.1.7。
- 副产物：`work/psp-debug/`（设备 metadata 三个版本 + PPSSPP base.apk 41M）、`shots/psp-*.png`（故障与四次验证截图），仅本机留档。

## 2.1.6 — 2026-11-14 17:10（⚠️ PSP 启动验证结论已被 2.1.7 更正）

- **用户三项确认全部执行并实机验证**：① 两个本机 APK 移入 macOS 废纸篓（`~/.Trash/pcs19-orig-20261114-1701.apk` 589M、`balatro-base-20261114-1701.apk` 59.8M，可恢复），`work/pcs` 589M→28K、`work/balatro` 64M→4.4M；② PSP 去重；③ D2/D3/D4 去重。
- **PSP 占位方案实机验证通过（可直接复用）**：`Roms/PSP/metadata.pegasus.txt` 加 `extensions: app`，4 条 `file:` 改 `*.app` 46B 占位，每条独立 `launch:` **一字不动**（写死 `file:///storage/emulated/0/Android/data/org.ppsspp.ppsspp/files/...`）。因启动命令与 `file:` 无关，游戏照常运行。验证三件套：清 `dataCache` 重启天马 → 缓存里全库 3,741 条 / PSP 4 条 / 4 个封面路径仍指向 `Roms/PSP/Imgs/`（占位不破坏相对资源解析）；实机 `am start` 山脊赛车 → PPSSPP 出现 Ridge Racer 载入小游戏；删完 TF 卡副本后再启动一次仍正常。**通过后才删** TF 卡 4 个 ISO/CSO（4.14G），内置 4 份完好。
- **D2/D3/D4 三处同步清理**：删 5 个 ROM（NDS `集合!卡比.nds` 65.8M、NEOGEO `fatfur5sp/6sp/spsp.zip` 32.3M、`kof2k4extra.zip` 39.2M），保留 `星之卡比：集合!卡比`（`content_history.lpl` 指向它）、`fatfursp`（原版带 publisher）、`kof2k4se`（带 publisher）。同步就地删 metadata 块（NDS 93→92、NEOGEO 168→164，diff 仅 4/16 行）和 **RA playlist** 里 4 条失效 item（`FBNeo - Arcade Games.lpl` 227→223，4 条 label 全是同一个 `Fatal Fury Special`）。清缓存重启后全库 **3,736 条**，设备端逐条校验 3,736 个 `file:` 全部存在，**死条目 0**。
- TF 卡 58G 用 33G(57%)→29G(50%)，可用 25G→30G。5 个孤儿封面 png 保留（小、无害）。
- `PLAYBOOK.md` §12.8 追加执行状态；`HARD_RULES.md` 新增 38～39 条（PSP 占位三件套验证、删 ROM 必须三处同步 + 死条目复核），共 39 条。

## 2.1.5 — 2026-11-14 16:55

- **16:50 按用户三项确认执行第二轮清理**：① 「放弃游戏进度」→ 分 2 批删 `RetroArch/states/*.state.auto` 16 份 156M（states/ 156M→44K，保留 10 个按核心分类的空目录）；② 「保留一轮」→ 删 `/sdcard/backup/` 的 pcs19 / fbneo-shelf-clean / ra-vertical-fix 三个旧目录 + `theme.qml.bak_v3|bak_v5`，只留 `balatro/` 与 `bak_probe`；③ 全部先备份到本机 `work/cleanup/pruned-backup-20261114/`（33 文件 / 167M）。内置可用 7.7G→7.9G(63%)；🔴 项与前端缓存、ANDROID 5 条复核完好。遗留 `savestate_auto_save=true` 未改（会再生垃圾，且 `auto_load=false` 说明这些存档开机根本不读）。
- **全量游戏包重复体检（只读，未删任何游戏包）**：本机 2 个 APK（像素足球19 589M、小丑牌 59.8M，均为已卸载游戏的原包备份，互不重复）、设备散落 APK 0、9 个第三方包各一份。TF 卡 25,528 文件 / 30.69G，主包 3,720 个 / 29.13G，36 平台 3,741 条 metadata。**内容真重复 6 组共 4.28G**：PSP ISO/CSO 双份 4.14G（4 对 MD5 抽样指纹全同、inode 不同）、NDS 星之卡比 65.8M、NEOGEO 饿狼 hack ×4 32.3M、KOF2004 39.2M、neogeo BIOS 1.6M、MAME/VARCADE 4 组 0.4M。货架层：跨平台同名 144 组（56 组在街机集合间，多为不同 romset 版本而非垃圾），同平台重名 0、死条目 0。报告 `work/cleanup/kpa-duplicate-audit-20261114.txt`。
- **判定法固化（新禁令 36/37）**：同名 ≠ 重复、同字节大小 ≠ 重复（卡带 ROM 天然是 2 的幂，`GB 0.25/0.5/1/2MB`、`NDS 64/128/256/512MB`）；一律 MD5，>100MB 用「头/中/尾各 4MB」抽样指纹。`PSP/metadata.pegasus.txt` 的 `launch` 指向 `/Android/data/org.ppsspp.ppsspp/files/`（scoped storage 只能读这里），`file:` 却指向 TF 卡副本 —— 直接删任一侧都会留死条目，必须先改 `file:`、清缓存重启验证。
- `PLAYBOOK.md` 新增 §12.8（重复包体检命令集与 6 组重复清单）、`HARD_RULES.md` 新增 36～37 条，`SKILL.md` 版本/描述/触发词同步。

## 2.1.4 — 2026-11-14 13:20

- **16:40 按 §12.6 流程执行 🟢 设备侧清理**（用户「首先清理可以清理的」）：分 4 批（2/3/9/1 项）每批校验，清掉 `/data/local/tmp/pcs/` 417M、`terraria.apk` 172M（md5 与已装 base.apk 相同）、3 个临时文件 6.4M、`/sdcard` 7 张 png + `._RetroArch` 2.5M、`dataCache.json.bak20261114` 5.7M、TF 卡空 `.Trashes/501/`。小文件先备份到本机 `work/cleanup/device-backup-20261114/`（12 个 / 14M），两个大文件靠等价来源可再生成。结果：`/data/local/tmp` 606M→12K，内置 7.1G(67%)→7.7G(64%)，`Data-Free` +约 700M。🔴 功能数据与 🟡 存档/备份复核全部完好。**未动** 43 个 `.bak`（<1M 且是回滚点）、应用缓存 88.5M（`pm trim-caches` 实测 `App Cache Size` 不变，只能走系统设置）、本机个人目录项（需单独确认）。
- **卸载小丑牌并按五步流程清干净**：`pm uninstall com.playstack.balatro.android`，删除 ANDROID metadata 的 5 行条目（6→5 条）、把 `balatro.app` 移入备份、删 `dataCache.json` 后重启天马，缓存重建 5,676,952 字节；本地镜像 `work/meta/ANDROID/metadata.pegasus.txt` 同步。备份在 `work/balatro/base.apk`(62MB) 与 `/sdcard/backup/balatro/`。此前像素足球已用同一流程删除（7→6 条）。流程写进 `PLAYBOOK.md` §12.5、`HARD_RULES.md` 第 34 条。
- **补完小丑牌方向键结论**：系统 `Vendor_045e_Product_028e.kl` 里 `HAT_X/HAT_Y` 与四向 `DPAD_*` 全齐，硬件没问题；是游戏自带 `gamecontrollerdb.txt` 把该 GUID 的 Android 条目写成 `dpup:b11 / dpleft:b13 / dpright:b14 / dpdown:b12`（按钮），而十字键走 HAT 轴，故方向不全。零改动解法是推左摇杆（所有 Android 条目都有 `leftx:a0,lefty:a1`，`controller.lua` 会把 >0.5 的轴转成 dpad）。候选修正行留档 `work/balatro/gamecontrollerdb-fix-candidate.txt`（`dpup:h0.1 / dpright:h0.2 / dpdown:h0.4 / dpleft:h0.8`），需重签才生效，本轮未改设备。
- **新增缓存 / 垃圾体检章节**：`PLAYBOOK.md` §12（只读命令集、🟢🟡🔴 三色分级、三个「持续产垃圾」开关、卸载五步、分批删除流程、2026-11-14 实测基线）；`HARD_RULES.md` 新增 32～35 条（大目录≠垃圾、`.state.auto`/会话 jsonl 不是缓存、卸载五步、扫描与删除必须分两轮且只出报告）。
- **体检只读结论（本轮未删任何体检对象）**：设备最大可清项是 `/data/local/tmp/pcs/` 417M（像素足球资源解包）与 `terraria.apk` 179M；`RetroArch/states/*.state.auto` 16 份 156M 属需确认项；应用缓存合计 88.5M。本机工作区 1.0G、`$HOME/.workbuddy` 7.0G（logs 788M / workspace-sessions 2.63G / binaries 2.06G）、`$HOME/.codex` 1.6G，磁盘仍剩 347G，不建议为腾空间冒险。
- **踩坑固化**：`dumpsys diskstats` 是四组等长数组（包名 / APK / 数据 / 缓存），按 `ast.literal_eval` 配对才能定位缓存大户；toybox `sort` 不支持 `-h`，用 `du -s ... | sort -n -r`；`du -sh` 输出给 `sort -nr` 排序会错（780K 排到 592M 前），要按 KB 排。

## 2.1.3 — 2026-11-14 10:35

- **定位「移植游戏实体键不对」的硬件根因**：本机面键标签是任天堂式（A 在右、B 在下），但固件按 Xbox 位置上报 —— 物理 A = `BTN_EAST`(305) = Android `BUTTON_B`(97)，物理 B = `BTN_SOUTH`(304) = `BUTTON_A`(96)。所以 SDL/LÖVE 系移植游戏里必然是「B=确认、A=返回」。写进 `HARD_RULES.md` 第 31 条。
- 查明系统层无解：AYANEO 掌机设置 → 手柄 → 自定义按键仅支持 MODE/LC/RC/=；手柄风格只有 Xbox/AYANEO 两档，切换会动到 RetroArch 的按键基线，不建议为单游戏切换。
- 小丑牌（com.playstack.balatro.android，LÖVE 移植）输入路径实测：只处理 `love.gamepadpressed`；`_RELEASE_MODE=true` 时键盘路径仅剩调试逻辑（`key_press_update` 内几乎全是 debug 分支），所以键盘映射方案无效；自带 `assets/resources/gamecontrollerdb.txt` 1503 条**无一条 platform:Android**；LÖVE 存档目录不会覆盖包内资源（放同名目录实测游戏照常启动）。
## 2.1.3 — 2026-11-14 10:20

- **货架去重**：FBNeo 233 → 208 条。按 `file:` 引用重合判定重复，删掉 25 个条目（13 个与中文条目共用同一 zip 的裸驱动条目 + 12 个同驱动版本变体 `kov115 / kovsh101~103 / kov2100,2106 / kov2p202,204 / olds100a,103t / orlegend111c,orlegendc`）。
- **补中文名**：给 `kov` / `r2dx` / `snowbros3` 加 `title:`（三国战纪（初版）、雷电DX、雪人兄弟3），不改 `game:` id。
- **删 13 个孤立 zip 共 252MB**（9 个中文包 + `kov4p` / `kovsh4p` / `r2dx` / `snowbros3`）。
- **重大踩坑记录**：天马把整库缓存在 `/sdcard/pegasus-frontend/dataCache.json`，只 push metadata 不刷新界面（233 改 208 后仍显示 233）。必须备份并删除该缓存再重启，等 8～15 秒重扫。写进 `PLAYBOOK.md` §3.3 与 `HARD_RULES.md` 第 30 条。
- **新事实**：`kovsh4p.zip` 报 `Romset is unknown`（FBNeo 无 kovsh4p 驱动），且 `三国战纪-风云再起.zip` 与其 md5 完全相同 —— 说明该中文包本身就是 4P hack 版，只能改指向标准 `kovsh.zip` 才能跑。
- 校验：208 条 id 全唯一、无缺 `file:`、无两条目共用同一 zip、208 个引用文件全部存在；竖版 219 个配置复检仍 `bad_rotation=0 bad_mapping=0 bad_keys=0`。
- 保留但不进库：12 个版本变体 zip 仍在 SD 卡（共约 39MB），`neogeo.zip`（BIOS）必须保留。

## 2.1.2 — 2026-11-14 09:45

- **救活 13 个「`Romset is unknown`」的 FBNeo 条目**。根因：中文名 zip 内部是 MAME 命名风格（`a0600.rom`），FBNeo 按 zip 文件名查驱动表 → 查不到。
  - 实测确认 FBNeo **按 CRC 认 rom**（日志 `Using ROM with known crc …`），所以改名成驱动名即可保留原版内容；但目标驱动名均已被标准包占用，故本次采用**改 metadata `file:` 指向**，`game:` id 不变。
  - 三张对照表见 `PLAYBOOK.md` §3.2（一统中原→kovytzy、乱世枭雄→kovshp、正宗PLUS→kovplus、风云再起→kovsh、三国战纪2→kov2、群雄争霸→kov2p、西游释厄传→orlegend、SUPER→olds、群魔乱舞→oldsplus、r2dx→raiden2dx、snowbros3→snowbro3、kov4p/kovsh4p→kov/kovsh）。
  - 12 个目标包全部实测能进游戏（Geometry 448x224 / 256x224，无 800x600）。
- 复核 `raiden2dx`（雷电DX）：它本来就是竖版（Aspect 0.750），**已有** per-game cfg，本轮仅确认内容正确（rotation=3 + 四向映射 + 按键基线），竖版总数仍 219。`r2dx` 条目改指向 `raiden2dx.zip` 后自动继承该 cfg，实机截图确认 TATE 正常。
- 遗留 12 个孤立中文 zip（约 230MB）仍在 SD 卡，未删除。

## 2.1.1 — 2026-11-14 04:00

- **竖版街机方向/按键全量复核为 0 异常**（219 个 per-game cfg：rotation=3、四向映射、按键基线三项全过）。
- **新增判方向的方法（实机日志，替代封面猜测）**：开 `log_to_file` + `log_verbosity`，读核心上报的 `[Core] Geometry ... Aspect`——`0.750` 是竖版、`1.333` 是横版；`800x600` 且无 `SET_ROTATION` 是 ROM 没加载（`Romset is unknown`）。写进 `PLAYBOOK.md` §3.1 与 `HARD_RULES.md` 第 29 条。
- 结论要点：FBNeo 核心虽然会发 `SET_ROTATION`，但**不转画面**（移走 cfg 后画面被压扁），竖版仍必须靠 `video_rotation="3"`；MAME 与 FBNeo 在 "3" 下输出方向完全一致。
- **纠错**：此前把 `mame_orient.json` 缺失的 `tengaij`（天外）和 `schmeisr` 当竖版补了 cfg，实测两者都是横版（Aspect 1.333），**已删除这两个误配 cfg**；`p47mus` 的残留 cfg 一并清掉。
- **补漏 7 个真竖版**：`airass / arcadian / explbrkr / samesame2 / saturnzi / slapfighb1 / unclepoo`（实机日志均 Aspect 0.750）。删 5 个失效 cfg（`galaga / mercsj / p47mus / samuraia / sonicwi`，ROM 与 metadata 都不存在）。
- 计数变化：MAME 2003-Plus 140→139、FinalBurn Neo 72→73，总数仍 219。
- 新增 `assets/data/fbneo_orient_probe.json`（41 条实机方向：vertical 8 / horizontal 20 / broken 13）。
- 发现 13 个 FBNeo ROM 报 `Romset is unknown` 打不开（9 个中文改版 三国战纪/西游释厄传 + `kov4p / kovsh4p / r2dx / snowbros3`），与方向无关，待用户决定是否删除或改名。

## 2.1.0 — 2026-11-14 03:45

- **简介全库补完，两种模板句式双向校验为 0**：本轮补 650 条（GBA 286 / PICO 80 / GBC 44 / NGP 40 / GG 36 / MSX 30 / WS 22 / PCE 19 / A2600 16 / NAOMI 15 / FBNEO 13 / ATOMISWAVE 10 / GB 10 / VB 10 / SMS 9 / NEOGEO 4 / MAME 2 / MDCD 2 / PCECD 2）。全库 3768 个游戏 description 均为真实中文介绍。
  - 关键：之前只校验 `由 .*出品`，漏了 `《X》，Y 平台。` 这一种（650 条）。**校验脚本必须同时跑两条正则**。
  - 词库 `assets/desc/zh_desc.json` 3058 → 3708 条。
- 删除坏 ROM `FBNEO/p47mus`（zip/cfg/封面/metadata 条目，备份于项目 `backup/bad-rom-20261114/`），平台 234→233、全库 3769→3768。
- 已知待处理坏档：`FBNEO/truxton`（报缺 `b65_09.21`）、`MAME/raiden`（启动即 ANR）。
- 待确认：非竖版街机（MAME 137 个、FBNeo 156 个没有 per-game cfg 的游戏）仍走全局映射 `a=96/b=97/start=108/select=109`，机身 A 键在这些游戏里不是"射击"。若要统一成「互换规则」，需在核心级 cfg 加 4 行（会影响该核心全部游戏），**未经用户确认不要做**。

## 2.0.9 — 2026-11-14 03:40

- **回滚我造成的按键二次破坏**：2.0.8 里我以「与全局一致」为名，把 219 个竖版 cfg 的 `a/b/start/select` 从厂商基线 `109/108/97/96` 改成了全局 `96/97/108/109`，并对 MAME 140 个文件补写了 `x_btn/y_btn`。用户实测反馈「方向对了、其他按键还是不对」。
  - 已按 2026-11-12 用户验收的厂商基线恢复：`a=109 / b=108 / start=97 / select=96`，并**删除**我多加的 `x_btn/y_btn`（回落全局 99/100）。
  - 同时还原核心级 `MAME 2003-Plus.cfg`（备份里只有 4 行，我误加了 a/b/x/y，会覆盖该核心**全部**游戏）。
  - 覆盖 5 个目录共 227 个 per-game cfg：MAME 2003-Plus 140、FinalBurn Neo 77、CPS-1 4、CPS-2 3、NeoGeo 3。`kpa_vertical.sh --keys` 复核：`total=219 bad_rotation=0 bad_mapping=0 bad_keys=0`。
- `kpa_vertical.sh --keys` 语义反转：不再「标准化到全局值」，改为**校验/恢复厂商基线**并删除 x/y 行（旧实现正是错误来源）。
- HARD_RULES 第 28 条改写：明确「⛔ 绝对不要改 per-game 的 A/B/START/SELECT」，并记下这是**第二次**犯同一个错（11-12 21:46 一次、11-14 03:20 一次），两次都是「为求统一而整文件覆盖」。
- 删除已知坏 ROM `FBNEO/p47mus`（zip + cfg + 封面 + metadata 条目，已备份到 `backup/bad-rom-20261114/`）。排查中发现 `FBNEO/truxton` 同样缺文件（报 `Rom with name 'b65_09.21' ... is missing`），`MAME/raiden` 启动即 ANR —— 三个都属 romset 不匹配，不是配置问题。
- 更正一条诊断结论：**adb 注入按键到 RA 是「时灵时不灵」**（同一键有时生效、有时丢），不能用单次注入结果判断映射对错；`96→投币` 可稳定复现，`start` 键注入经常丢失。

## 2.0.8 — 2026-11-14 03:20

- **修复竖版街机方向全反 + 按键错位**（用户反馈：VARCADE 的 arkanoid 竖版方向错、按键可能不对）。
  - 根因：`config/MAME 2003-Plus` 的 140 个 per-game cfg 把 `video_rotation` 写成 **"1"**（逆时针 90°），而方向映射是 `up=h0right / down=h0left / left=h0up / right=h0down`（对应顺时针 90° 的那套），两者差 180° → 画面竖着但推上往下走。
  - 实机取证：`rotation=1` 时 arkanoid demo 的**砖块落在屏幕左侧**；改成 `"3"` 后砖块落到**右侧**、挡板在左下，玩家逆时针竖拿掌机即正立且方向一致。
  - 修正：140 个 cfg 全部 `1 → 3`；FBNeo(72)、CPS1(3)、CPS2(2)、NeoGeo(2) 原本就是 `3`，无需改。现 219 个文件完全一致。
  - **按键错位**：per-game cfg 里 `a=109(SELECT键) / b=108(START键) / start=97(B) / select=96(A)`，与全局（`a=96/b=97/start=108/select=109`）完全错位 → 按 A 不射击、按 B 反而开始。219 个文件已标准化。
  - `scripts/kpa_vertical.sh` 重写：旧版用 `grep -q '^video_rotation = "[13]"'` 把错误值当合法值放行，且只要 `up` 是 `h0right` 就 `continue` —— 等于永久跳过没修的文件。新版强制 `rotation="3"` + 四向映射，新增 `--keys` 一并标准化按键，dry-run 输出分类计数（bad_rotation / bad_mapping / bad_keys）。
  - `scripts/kpa_env.sh`：`set -u` 下 `[ -n "$KPA_ADB" ]` 未定义即报错，改 `${KPA_ADB:-}`。
- 覆盖核对：VARCADE 74 + MAME 277 去重 326 个游戏，竖版 139 个**全部有 cfg**（另多 1 个 galaga，MAME 中标 horizontal 但实为竖版），横版无误配。
- 已知坏档：`FBNEO/p47mus` 是 FBNeo 不支持的 romset，进游戏显示蓝底 `ROM set p47mus is known but not working / Insert is unknown`，与方向无关。

## 2.0.7 — 2026-11-14 03:00

- **修复「进入天马后按键全部失灵」**（这是 kpa-shelf 最严重的一次回归，两个独立成因叠加）：
  1. **RetroArch 进程残留抢走输入焦点**。adb 反复 `am start` 测试后，RA 的 `RetroActivityFuture` 窗口仍持有 `FocusedWindows`，而 `mCurrentFocus` 显示天马 —— 于是画面是天马、按键全被投递到 RA 的死窗口。判据：`dumpsys input | grep -A2 FocusedWindows` 与 `dumpsys activity activities | grep mResumedActivity` 必须都指向 `org.pegasus_frontend.android`。修复：`am force-stop com.retroarch.aarch64` 且确认 `ps -A | grep retroarch` 为空，再启动天马。
  2. **Qt 窗口重新激活后根 FocusScope 不自动拿回焦点**。从天马启动游戏、退出返回时 Qt 窗口 inactive→active，`activeFocus` 变为 false 且不会自己恢复，症状同样是「界面正常但按键全失灵」。修复：主题内加 `focusGuard` Timer（800ms 轮询，`!root.activeFocus && root.visible` 时 `forceActiveFocus()`）。
- **按键处理重构为容错版**：新增 `kIs(name, ev, fallbackKey)`，用 `typeof api.keys[name] === "function"` 保护并 fallback 到 `event.key`；`Keys.onPressed` 整体包 `try/catch` 调 `handleKey(event)`；**方向键判断提到最前**，保证 A/B 或分页 API 异常时移动光标仍然可用。
- **诊断技巧（重要）**：Pegasus 的 `console.log` **不写 logcat，而是写 `/sdcard/pegasus-frontend/lastrun.log`**（格式 `[i] qml: ...`）。这是唯一能远程确认「按键是否到达主题」的手段。
- **adb 注入按键在天马无效**（Qt 直读 evdev，绕过 Android InputManager），所以 `input keyevent 22` 之类不能用来测主题按键，只能靠实体手柄 + lastrun.log 验证。

## 2.0.6 — 2026-11-14 02:50

- **简介全库完成**：3769 条 description 全部为真实中文介绍，模板句残留 0（本次补 1265 条）。词库 `assets/desc/zh_desc.json` 1793 → **3058** 条。
- **左栏 v5（kpa-shelf theme.qml）**：
  - 主名改为**中文机种名 23px 粗**（雅达利 2600 / 任天堂 红白机 / 世嘉 MD），英文短名降为 13px 副行，游戏数 17px 右对齐；
  - 左栏宽度 238 → **252**，行高 56，分组标题 15px 加短横线；
  - 选中态：#1f2a3a 底 + 5px 红条 + 纯白粗体；
  - 新增 **L1/R1 直接切换上/下一个平台**（`stepPlatform(dir)`），不必每次按 ← 回左栏滚动；
  - 底栏键位提示改为四行（A/B/L1R1/方向键）。
- **NDS 双屏改左右并排**：`melonDS.opt` 的 `melonds_screen_layout` 由 `Top/Bottom` 改 **`Left/Right`**。原上下排列在 960×640 上两屏总高 720 会超出屏幕被裁；并排后两屏各 480×360 完整可见、比例正确（`aspect_ratio_index` 仍为 21）。实测《世界树迷宫》标题与菜单画面双屏均完整。
- 修复流程中踩到：`cd work` 后再用相对 `$ADB` 路径会全部 pull 失败（静默），须用绝对路径。

## 2.0.5 — 2026-11-14

修实机新反馈：**部分街机游戏开局"主副两个角色都进入"，且一个手柄同时控制两个角色。**

- 根因：`input_player2_joypad_index` 与 P1 同为 `0`（同一个物理手柄），且 `input_player2_analog_dpad_mode = 3`。该选项不依赖按键绑定，直接把左摇杆换算成 P2 方向键 —— 所以即使 P2 按键全是 `nul` 也会串控。
- 为何"只有一部分"：`fbalpha2012_cps1/cps2/cps3/neogeo`、`mame2003_plus` 等核心没有 `config/remaps/` 覆盖，直接吃全局错误配置；而 FBNeo / MAME / Flycast / Beetle / Genesis Plus GX / gpSP 等预置 remap 已把 P2 该值写死为 0。（Gambatte / Game & Watch / VBA-M 的 remap 仍为 3，只是这些机种单人不外显。remap 不含 `joypad_index`，故全局索引一改即全部覆盖。）
- 修法：P2 → `joypad_index = 1` + `analog_dpad_mode = 0`；P3 → `joypad_index = 2`；P1 不变。两份 cfg（`files/retroarch.cfg` 与 `RetroArch/retroarch.cfg`）同步。
- 新增 `kpa_gamefix.sh p2`（支持 `--apply` / `--revert` 值级还原），并并入 `all`。
- 新增禁令 27；PLAYBOOK 新增 10.4 完整机制说明与"哪些核心会中招"清单。

## 2.0.4 — 2026-11-14

### 修复

- **「字太小、封面太小」的真正根因：`vpx()` 在本机等于 `v × 0.75`**。Pegasus 自带的 `vpx()` 按 853 高标准换算，于是主题里写的 `vpx(58)` 顶栏只有 43px、`vpx(21)` 的平台名只有 15.7px、`vpx(167)` 的封面只有 125px —— 越"按设计值调大"越是被打七五折。现封装 `px(v)`（`kScale = 1.0`）直接用 960×640 真实像素排版。
- **QML 方法名不能大写**：`function S(v)` 会报 `Method names cannot begin with an upper case letter`，表现为整屏「主题载入失败 /(ToT)/~~」。缩放函数改名为小写 `px()`。
- **简介行距失控**：`lineHeight: 1.42` 在这台机器的中文字体度量下实际撑到约 1.7 倍，第三行被屏幕底边切掉。改用 `lineHeightMode: Text.FixedHeight` + `lineHeight: 23` 后完全可控。

### 变更

- **主题布局 v4（重排，整体放大）**：
  - 顶栏 58px：标题 27px 粗 + 副标题 15px，右侧常驻「当前平台 19px + n/m 17px」；
  - 左栏 238px：平台行高 52px，短名 21px 粗 + 中文机种名 15px + 右侧游戏数 14px，分组标题 30px；
  - 中间**全宽 722px / 4 列**（cell 177×268，封面 167×222），去掉原右栏，封面比 v3 大 33%；
  - 底部**整条游戏介绍 166px**：96×128 缩略图 + 25px 标题 + 14px 元信息 + 15px 简介 3 行 + 右侧键位列，横贯整屏不再有大片空白；
  - 封面墙上下各加 16/26px 渐隐，滚动时不出现生硬的切边。
- 布局实测校准：顶栏分隔线 57、左栏竖线 237、信息条上边 474，与设计值 58/238/474 一致，确认是 1:1 渲染。

## 2.0.3 — 2026-11-14

### 新增

- **自建主题 `kpa-shelf`**（`assets/themes/kpa-shelf/`）。三个现成主题都不满足「平台分类 + 游戏介绍」：prosperoOS 平台条是横向细字、点击区域小；Reprise/ NPE / Library 按 16:9 设计，在 3:2 屏上不是留白就是字太小。自建版按 960×640 手排：
  - 左栏 202px：**平台按机种分组**（家用机 → 掌机 → 街机 → 电脑 → 移植），每行两排字（短名 16px 粗 + 中文机种名 12px）+ 游戏数；
  - 中栏 438px：封面墙 3 列（cell 140×222），选中项红框 + 游戏名两行；
  - 右栏 320px：170px 大图（有截图用截图、否则用封面）+ 25px 标题 + 元信息 + 完整简介 + 游玩次数 + 键位提示。
- **199 条真实中文简介**（`assets/desc/zh_desc.json`）：PS / DOS / SFC / MD / N64 / PSP / SATURN / ANDROID / EASYRPG / DREAMCAST / NDS，每条 1–2 句讲清年份、厂商、玩法与地位。原库 3769 条全是「《X》，Y 平台。」模板句。
- **`scripts/kpa_desc_fill.sh`**：用本地 JSON 简介库回填 `description:`，默认 dry-run，`--apply` 时自动 `.bak`，只改 description 行、不动其他字段。

### 修复

- **「退出游戏回不到原来选的游戏」**：真因不是任务栈 —— Pegasus 官方文档写明游戏启动后前端会 minimize 并**把主题整个重新加载**，返回时 QML 是全新实例。改为用 `api.memory` 记 `Shelf Game` + `Shelf Collection`，启动时按平台定位、找不到再全库扫标题兜底，并做 30ms + 400ms 两次 `positionViewAtIndex`。实测启动游戏 → 退出后精确回到同一游戏（`已玩 2 次` 也保留）。
- **右栏简介只显示两行就被省略号截断**：`height: Math.min(contentHeight, ...)` 会因 height 绑定自身而把 `contentHeight` 算短，改用 `implicitHeight`。
- **改完 metadata 界面不更新**：天马缓存 `/sdcard/pegasus-frontend/dataCache.json`（5.79MB），只 `force-stop` 不删缓存无效；必须删文件再启动，重建约 30–40 秒。

## 2.0.2 — 2026-11-13

### 修复

- `scripts/kpa_gamefix.sh` 的 `--revert` 改为**值级还原**，不再依赖 `.bak` 文件。原因：同一份 cfg 会被多轮改动，`.bak` 很容易在某次「改完之后」才被创建，于是变成「已改版」备份 —— `cp` 回去等于没回滚（本轮实测在 Flycast 的 10 个 per-game cfg 上踩到了）。
  现在的还原语义：DOS → `rewind_enable`/`savestate_auto_save` 回 `true`；NDS → 布局回 `Left/Right`、触屏回 `Mouse`、`aspect_ratio_index` 回 `23`；Flycast → `reicast_threaded_rendering` 回 `enabled`；Atomiswave → 删除 `video_font_enable` 行。
- 设备上双向验证通过：回滚后 `video_font_enable` 计数归 0、`rewind_enable=true`；再 `--apply` 恢复 16 处写入，值回到 `false`。

## 2.0.1 — 2026-11-13

按实机反馈修六类体验问题，并推翻一处会误导排查的错误认知。

### 修复

- **DOS 左下角 `Save State Error` 弹窗**：全局 `rewind_enable=true` + `savestate_auto_save=true`，而 DOSBox-pure 进来先停在 `DOSBOX PURE START MENU`、游戏尚未运行 → 存状态必然失败。只在 `DOSBox-pure.cfg` 关这两项，不影响其它平台倒带。
- **NDS 双屏被纵向拉长、画面被裁**：`melonds_screen_layout="Left/Right"` + `aspect_ratio_index="23"`，两屏并排后又被拉满屏 → 改 `Top/Bottom` + index **21**（实测 21/22 才是核心原始比例，亮像素宽约 408px；23/24 拉到 918px）。`Hybrid` 该核心不支持。
- **Atomiswave 背景满屏雪花噪点**：`reicast_threaded_rendering` 改 `disabled`。
- **Atomiswave 的 `Please upgrade to MAME romsets` 提示**：逐游戏 per-game cfg 写 `video_font_enable="false"`（**per-playlist 层实测不生效**）。
- **平台名字太小、切平台看不出当前在哪**：delegate 字号 24→36、选中 `#ffffff` / 未选 `#6affffff`、平台条常显；顶部游戏条 10→16。
- **退出游戏回到平台第一个而非刚才那个**：记 `Last Game` + `restoreLastGame()` 定位回原游戏；天马 / RA 加入电池优化白名单（RAM 仅 2.96GB，天马易被 LMK 回收）。
- **坏 ROM `VR运动会.bin`**：实测 40 秒仍全黑（同平台罪恶装备X 20 秒进画面），移入 `Roms/_quarantine/` 并从 metadata 移除条目，天马 3770→3769。**移走不删，可逆。**

### 新增

- `scripts/kpa_gamefix.sh`：`dos` / `nds` / `flycast` / `aw-osd` / `all`，默认 dry-run，`--apply` 写入、`--revert` 回滚，全部幂等。**回滚用值级还原而非文件恢复** —— 同一份 cfg 可能被多轮改动，`.bak` 很容易在某次"改完之后"被创建而变成"已改版"备份，此时 `cp` 回去等于没回滚（本次实测就踩到了）。
- `scripts/kpa_theme_tweak.py`：主题 6 处增强，锚点失配会明确报告而不是写半成品；`--apply --restart` 一步到位。
- `references/PLAYBOOK.md` 第 10 节：六类问题根因对照表、主题遮罩机制、NDS 比例客观定法、以及「一条走不通的路」（DOS 自动跳过启动菜单，含 15 个包启动项清单）。

### 修正

- **推翻错误认知**：原文写「`input motionevent` 可点 RA 菜单、方向键 19–22 有效」。实测 RA **完全不接收** adb 注入的事件 —— `input keyevent`（keyboard / gamepad / joystick / dpad 四种 source 全试）与 `input tap` 注入后截图**逐像素相同**；`sendevent /dev/input 下的 event3 节点` 报 `Permission denied`（shell 不在 input 组）。只有 **BACK(4)** 走 Activity 回调有效。天马是普通 Qt 应用、走 InputManager，注入对它有校 —— 两者不能混为一谈。
- 新增禁令 12–15：RA 输入注入边界 / per-playlist 覆盖 OSD 开关不生效 / 往 `Roms/<平台>/` 放非 ROM 文件前必须先收紧 `extensions` / 禁止用设备端 `unzip` 改 `.dosz`。

### 基线

- 天马条目 **3770 → 3769**（隔离坏 ROM），`is_missing = 0`。
- 竖版 cfg 实测 **219**（MAME 2003+ 140 / FBNeo 72 / CPS1 3 / CPS2 2 / NEOGEO 2），方向映射 **219/219** 全量校验通过；早期文档写 216 属口径漂移。
- 设备侧 17 项 / 17.40MB 备份已清理完毕，幽灵目录与 555 条缺文件警告归零，平台数 37→36。

## 2.0.0 — 2026-11-13

名称定为「KPA掌机天马安装与优化助手」，slug 统一为 `kpa-pegasus-setup`，发布到 SkillHub / ClawHub / GitHub。

### 修正（会导致实机故障的错误）

- 竖版方向映射：`up=h0left / down=h0right / left=h0down / right=h0up`（厂商基线）→ `up=h0right / down=h0left / left=h0up / right=h0down`（实机验证值）。同步修正 `SKILL.md` 与 `scripts/step4_metadata.sh` 两处。
- ANDROID 集合 `file:` 由 Android 组件名改为 `.app` 占位真实文件 + `extensions: app` + per-game `launch:`；重写 `assets/meta_latest/ANDROID.txt`，并补 `assets/golden/game_dirs.txt` 的 ANDROID 行。
- 机型名由误写的 "AYANEO Pocket Advance" 改为正式名 KONKR Pocket ADVANCE（AYANEO 旗下）。
- MSX 核心安装方式由「下载 .so 到 public 路径」改为「本地 HTTP 最小核心源 + `.index-extended`，让 RA 自己装进私有 cores 目录」。
- `scripts/bangumi_desc.py` 移除硬编码的 adb 绝对路径，改为 `KPA_ADB` / PATH / 自动发现；TF 卡路径支持 `KPA_TF`。
- `scripts/step6_cleanup.sh` 移除两处通配 `rm -rf`，改为只盘点、不自动删。

### 新增

- `scripts/kpa_vertical.sh`：修存量竖版 cfg，默认 dry-run，只精确替换 4 行方向。
- `scripts/kpa_msx_core.sh`：MSX 本地镜像 prepare / restore。
- `scripts/kpa_android_apps.sh`：ANDROID 占位文件与 metadata 部署。
- `scripts/kpa_nomedia.sh`：4 处 `.nomedia` + MediaStore 重扫。
- `scripts/kpa_gamedetails.sh`：详情页 QML 增强与回滚点。
- `scripts/kpa_health_check.sh`：全库静态校验 + 离线自检 `--local`。
- `references/PROCESS_REVIEW.md`：7 阶段完整工程复盘。
- `references/HARD_RULES.md`：22 条硬性禁令与正确做法。
- `references/PLAYBOOK.md`：9 个分项实操手册。
- `references/VERIFICATION.md`：健康校验 SOP、达标基线、遗留项、清理清单、回滚点。
- `assets/golden/GameDetails.improved.qml.txt` 与 `.before20261113`。
- `README.md`、`.gitignore`、本文件；GitHub 仓库 `archive/` 归档工程报告与回滚点（已脱敏）。

### 记录

- 补充「禁止 `am force-stop com.ayaneo.home`」等系统按键层禁令。
- 补充核心批量更新风险评估（3% 中断无影响，不建议更新 nightly）。
- 补充冷启动等待基准（8–26 秒）与 toybox `unzip` 中文条目 CRC 误报说明。
- 明确遗留项：`WS/恐怖传说.zip` 坏 ROM、`_backup_20261112_2347` 幽灵目录、1142 条空壳简介、详情页观感待实机确认、设备侧 17 项待清理。

## 1.0.0 — 2026-11-12

上架版：7 步幂等安装脚本（APP / 主题 / RA 主配置 / metadata + 竖版 cfg / PPSSPP / 清理 / 验证）、`sync_from_device.sh`、`bangumi_desc.py`、36 平台 metadata 与方向库、prosperoOS 主题包。约 3.4MB，不含 ROM / BIOS / APK。
