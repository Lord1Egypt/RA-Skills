# 一键安装 · 从零到可验收

> 这份文档只讲**验证成功、可复用**的最短路径。整轮踩坑复盘见 `references/OPTIMIZATION_JOURNEY.md`，
> 完整 60 条禁令见 `references/HARD_RULES.md`，分项实操见 `references/PLAYBOOK.md`。

![KPA 一键安装 7 步流程](https://skillhub-1388575217.cos.accelerate.myqcloud.com/skill-comments/uploads/634669/4224e8230a6941eaa2aa7eb8bd955926.png)

## 一句话

装好 skill → 连上掌机 → `bash scripts/kpa_oneclick.sh`。脚本会先做只读体检、留回滚点，再跑 7 个幂等步骤、清缓存、出静态校验报告；**实体键手感与封面观感仍需你在掌机上过一遍**。

## 1. 前置条件

| 项 | 要求 | 不满足时 |
|---|---|---|
| 设备 | KONKR Pocket ADVANCE（Android 12 / 960×640），USB 调试已授权 | `adb devices` 无 `device` 时脚本会拒绝执行 |
| adb | platform-tools（macOS 实测 r34.0.5） | 设 `KPA_ADB=/path/to/adb` |
| TF 卡 | 默认 `/storage/6AF3-384F` | 挂载点不同设 `KPA_TF=/storage/XXXX-XXXX` |
| 本机 | Python 3 + Pillow（仅生成蓝标图示时需要） | 安装流程本身不依赖 Python |
| 磁盘 | 本机 ≥200MB 空闲（放配置级回滚点） | 体检会告警 |

> APK / BIOS / ROM / 遮罩 PNG / 主题二进制包**不随包分发**。step1 会从官方渠道下载 APK（直连失败自动走镜像），
> step2 检测到主题包缺失会打印获取指引并 SKIP，不影响其余 6 步。

## 2. 三条命令

```bash
# ① 安装 skill（SkillHub 会多套一层 @handle/ 目录，手动装要移到 <skills>/<slug>/SKILL.md 这一层）
skillhub install "@user_43faedd6/kpa-pegasus-setup"

# ② 先体检 + 看计划（只读，不写设备；设备没连也能预览）
bash ~/.workbuddy/skills/kpa-pegasus-setup/scripts/kpa_oneclick.sh --dry-run

# ③ 正式执行（幂等，失败后可原样重跑）
bash ~/.workbuddy/skills/kpa-pegasus-setup/scripts/kpa_oneclick.sh
```

其它模式：`--verify-only`（只出校验报告）、`--steps 3,4`（只跑指定步骤）、`--no-backup`（不建议）。
运行时产物统一写在 `~/WorkBuddy/kpa-oneclick/<时间戳>/`：`oneclick.log` / `backup/` / `health.txt` / `report.md`。

## 3. 这 7 步分别做什么

| 步 | 脚本 | 落地内容 | 关键判定 |
|---|---|---|---|
| 1 | `step1_apps.sh` | RetroArch / 天马 / PPSSPP 上架版；已装则跳过；APK 从官方渠道下载，直连失败走镜像 | `pm list packages -3` |
| 2 | `step2_theme.sh` | **prosperoOS** 主题（放大封面 + 戴夫背景 + 平台 Logo）并切换；文本版缺 `assets/golden/prosperoOS-kpa.zip` 会 SKIP | `lastrun.log` 中 `Cannot open` = 0 |
| 3 | `step3_ra.sh` | RA 主配置 `retroarch.cfg` + 竖版 per-game cfg 生成 | 单独开 RA 呈黑黄 ozone |
| 4 | `step4_metadata.sh` | 各平台 `launch` 行 + 按方向库生成 per-game cfg（只 patch 不整覆盖） | 219 个竖版 cfg、方向统一 |
| 5 | `step5_ppsspp.sh` | PSP 可读目录 + `ppsspp.ini`（满屏拉伸、关虚拟键）+ PSP 直启 | **前端点击**后 logcat `Booted` |
| 6 | `step6_cleanup.sh` | AppleDouble / `.DS_Store` / 测试截图清理（失效旧路径只报告不自动删） | 用户确认后分批 |
| 7 | `step7_verify.sh` | 重启天马、截图、检查 `lastrun.log` 资源缺失 | `N games found`、零 ANR |

> `step2_theme.sh` 装的是 **prosperoOS**。另一套 **kpa-shelf** 是自建主题（左栏分类 + 4 列封面墙 + 底部介绍），**手工部署**，源码在 `assets/themes/kpa-shelf/`，改法与布局见 `PLAYBOOK.md` §11；两套不要混为一谈。

阶段 3 会**自动** `am force-stop 天马` → 删 `dataCache.json` → 重启，这是禁令 3 的强制收尾；
阶段 4 跑 `kpa_health_check.sh` 做全库静态校验（ROM / 封面引用缺失数）；阶段 5 出 `report.md`。

## 4. 安装完成后怎么算验收

![验收边界](https://skillhub-1388575217.cos.accelerate.myqcloud.com/skill-comments/uploads/634669/a536feba554b4264898b021461331233.png)

**脚本能自动证明的**：核心能加载、冷启动不崩、配置没被写回、ROM / 封面引用缺失数、metadata 条目与排序、playlist 死引用、缓存已重建。

**必须你亲手确认的 5 件事**（adb 注入按键对 RetroArch 完全无效）：

1. 实体按键手感：街机 CPS1 / CPS3、ATOMISWAVE 竖版、PPSSPP / PS ABXY、N64 方向键；
2. 每个平台各冷启动 1 款游戏（**8–26 秒**才算黑屏；汉化破解版可能有 60 秒以上片头）；
3. 切到该平台货架截图，确认封面有游戏图像、中文名没被裁、没有空白格；
4. 从游戏按 `select+B` 能否退回天马对应平台页面；
5. DOSBox-Pure 核心菜单内的操作（本包用同名 `.conf` 的 `[autoexec]` 已绕开「选 exe」）。

> ⚠️ 报告里的「35 平台 / 3706 条、缺失 0」是**那台实机的基线数字，不是新机的通过标准**，请以本次 `health.txt` 的实际结果为准。

## 5. 配置分层速查（改动落点）

![配置分层](https://skillhub-1388575217.cos.accelerate.myqcloud.com/skill-comments/uploads/634669/5a5fc17907ea4b8ca9fa08c2e1f41b7d.png)

越往下优先级越高。最常见的事故是「在错误的层改了，结果被上层覆盖」或「把竖版方向映射污染到核心级 cfg，导致所有横版游戏按键错位」。
**竖版 cfg 只精确替换 4 行方向，保留 `a/b/start/select/rotation`**；不要新建核心级 `.rmp`。

## 6. 出问题先看这张图

![排障决策树](https://skillhub-1388575217.cos.accelerate.myqcloud.com/skill-comments/uploads/634669/845099395d2544649e341b69b5746b98.png)

## 7. 不走弯路：最容易踩的 10 条

这 10 条来自真实故障，其余 45 条见 `references/HARD_RULES.md`。

1. **改 metadata / 新增目录后必须删 `dataCache.json` 并重启天马**，否则前端一直显示旧缓存（脚本阶段 3 已自动做）。
2. **禁止 `am force-stop com.ayaneo.home`** —— 会杀掉系统按键服务，只能关机重启恢复。
3. **禁止把核心 `.so` 推到 public 路径**（SELinux `avc: denied { execute }`）；只能用 `/data/data/com.retroarch.aarch64/cores/`。
4. **禁止整份覆盖 `metadata.pegasus.txt`**，云端与设备 ROM 数不匹配会直接丢游戏；只就地 patch。
5. **禁止靠 `game_dirs.txt` 排除目录**，天马启动会重写回原样；幽灵条目要删源目录。
6. **禁止假设 adb 能操作 RetroArch 菜单**：`input keyevent` / `input tap` 全部无效，只有 `BACK(4)` 能呼出 RA 菜单。
7. **禁止用 3.2 秒截图或单一亮度阈值判黑屏**；先看前台窗口与 `ANR in com.retroarch.aarch64`。
8. **禁止按尺寸 / 颜色一刀切判「占位封面」**：libretro 的 GBA 真盒绘本身就有 `500×315`；按图像内容（粗色桶数 <20 才是占位卡）分类，替换前双备份。
9. **禁止静态引用 0 缺失就宣布封面修好**，视觉类必须实机截货架。
10. **删除 ROM / CHD 前先在本机留回滚点**（实测 39MB/s，443MB 约 11 秒）；设备删除无废纸篓。

## 8. 优化流程总结（本包是怎么来的）

整轮工程按「先通用、后特例；先只读、后写入；先单点、后推广」推进，六个阶段：

| 阶段 | 做了什么 | 沉淀位置 |
|---|---|---|
| ① 基线搭建 | 36 平台 metadata / 27 核心 / 主题 / 双屏 / 遮罩 / 竖版方向库 | `scripts/step1~7`、`references/OPTIMIZATION_JOURNEY.md` §5.1 |
| ② 数据治理 | 简介回填、封面补齐、`.nomedia`、重复 ROM 与冗余包分级清理、playlist 死引用 | `references/PLAYBOOK.md` §1–§12 |
| ③ 体验优化 | 热门 10 款置顶、MSX / PICO 遮罩、PSP 退出组合、CPS1 / CPS3 键位 | `references/PLAYBOOK.md` §13–§17 |
| ④ 疑难攻坚 | DOS 免选 exe 直启、`.dosz` 崩溃二分定位、ZIP 伪装 ROM 解包、土星 CHD 引导区判定 | `references/PLAYBOOK.md` §18 |
| ⑤ 二次反馈 | 更正「按尺寸判占位封面」误判、N64 十字键绑定层、汉化版长片头定性、坏 CHD 删除 | `references/PLAYBOOK.md` §19、`OPTIMIZATION_JOURNEY.md` §15 |
| ⑥ 沉淀 | 60 条禁令 + 一键安装通道 + 蓝标系列图示 + 本机 / 设备双回滚点 | 本文件、`scripts/kpa_oneclick.sh`、`assets/blueprints/` |

**贯穿全程的三条方法论**：

- **静态校验全绿 ≠ 用户看得见**。视觉与手感必须实机验收，这是本包最大的一次自我更正来源。
- **二分定位优于猜测**。`大唐英雄传.dosz` 冷启动 `SIGSEGV`，用「只打包 ZIP 前 N 个条目」二分 10 轮定位到 `GAME.IMG` 越界读，尾部补 1 字节救回。
- **区分「通用安装」与「特定数据修复」**。热门置顶、DOS 同名 conf、GBA 真盒绘回填、坏 CHD 删除都只对那台机器成立，**不在一键脚本里**；按需照 `PLAYBOOK` §18–§19 单独处理，避免新机误跑。

## 9. 回滚

```bash
RUN=~/WorkBuddy/kpa-oneclick/<时间戳>
adb push "$RUN/backup/meta/<平台>.txt" /storage/6AF3-384F/Roms/<平台>/metadata.pegasus.txt
adb shell 'am force-stop org.pegasus_frontend.android; rm -f /sdcard/pegasus-frontend/dataCache.json'
```

设备侧还有一份同步副本 `/sdcard/backup/kpa-oneclick-<时间戳>/`。
**值级还原优先**：整份覆盖 metadata 会引入新问题；`.bak` 可能已被后续改动覆盖成改版，回滚前先确认内容。

## 10. 图示

本包图标与 4 张图示属于 `@user_43faedd6` 账号统一的**蓝标（Blueprint Badge）系列**：深藏青 `#0A1F3C` 网格蓝图底、亮青蓝 `#49D0FF` 圆角线稿、白色辅助线、无渐变无阴影。SkillHub 发布包不接受 png，图示存于 COS，地址清单见 `assets/blueprints/URLS.md`；本地可用生成器重建。
可用 `python3 scripts/blueprint_icons.py` 重新生成，`--check` 校验产物。

> 图示由 `scripts/blueprint_icons.py` 生成，源文件在 `assets/blueprints/`（根目录 `icon.png`）；因 SkillHub 发布包不接受 png，文档用 COS 绝对地址引用，清单见 `assets/blueprints/URLS.md`。
