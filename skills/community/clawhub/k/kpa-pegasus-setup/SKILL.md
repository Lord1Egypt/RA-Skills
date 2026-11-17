---
name: kpa-pegasus-setup
slug: kpa-pegasus-setup
displayName: "KPA掌机天马安装与优化助手"
version: 2.4.2
platforms: [macos, linux, windows]
author: lis
description: KONKR Pocket ADVANCE（KPA，Android 12 / 960×640）掌机装天马 Pegasus + RetroArch/PPSSPP/EKA2L1（N-Gage）：竖版方向、libretro 核心、BIOS/遮罩、封面与中文简介、主题与双屏、全库校验与可逆清理、按键修正、存档迁移。路径/按键码/旋转值均实机验证，脚本幂等。触发词：KPA、天马、Pegasus、RetroArch、PPSSPP、EKA2L1、N-Gage、掌机优化、方向键反了、核心装不上、封面或简介缺失、存档丢了、缓存清理、一键安装。
trigger:
  - KPA 掌机安装 / 优化
  - 天马不显示游戏 / 封面不对 / 简介不显示
  - 竖版游戏方向键反了
  - RetroArch 核心装不上 / MSX 黑屏
  - EKA2L1 / N-Gage 装不上 / 天马 NGAGE 没入口
  - KPA 体检与清理
locale: zh-CN
---

# KPA掌机天马安装与优化助手

面向 **KONKR Pocket ADVANCE**（KPA，AYANEO 旗下，Android 12 / arm64-v8a / 960×640），把新机或半配置机整理成：天马(Pegasus) 前端 **36 平台 3728 游戏**（2026-11-18 设备实测基线，ROM/封面引用缺失 0）、RetroArch 27 个可用核心、PPSSPP 直启、EKA2L1 双 N-Gage 环境、竖版方向正确、封面与简介完整、图库不被素材刷屏、主题与双屏观感可用。

本包是**实机工程沉淀**，不是通用模拟器教程。脚本幂等，可重复运行修复。

> **不携带版权与大文件**：APK / BIOS / 遮罩 PNG / ROM 均不随包分发。SkillHub / ClawHub 只收文本类文件，因此 **prosperoOS 主题包与背景图放在 GitHub 仓库 `assets-heavy/`**（`step2_theme.sh` 检测到缺失会打印获取指引并跳过，不影响其余步骤）；`assets/golden/` 只放配置文本与 QML 修改。离线完整版可克隆 GitHub 仓库，或用 `scripts/sync_from_device.sh` 从已配置好的机器拉取（仅供个人使用，勿再发布）。

## 必须遵守：硬性禁令

违反以下任一条都曾导致实机故障。**完整 60 条见 `references/HARD_RULES.md`**（编号连续，按主题分组）。

1. **禁止 `am force-stop com.ayaneo.home`** —— 会杀掉 AYAWindow 的 `WindowKeyEventService`，KPA / Android 层系统按键全部失灵，只能关机重启恢复。**系统按键属于 KPA / Android / AYASetting / AYAWindow 层，不是 RetroArch 按键**，不要在 RA 配置里找它。
2. **禁止把 libretro 核心 `.so` 推到 public 路径**（`/sdcard`、`Android/data`、`/data/local/tmp`）后指望加载 —— SELinux `avc: denied { execute }`；只有 `/data/data/com.retroarch.aarch64/cores/` 可用。`run-as` / `adb root` / `su` / `adb backup` 全部无效（Android 12 备份产出 0 字节）。
3. **禁止改 metadata / 新增目录后不清 `dataCache.json` 就判断生效** —— 必须 `rm /sdcard/pegasus-frontend/dataCache.json` 再重启天马；缓存会保留已删除游戏。
4. **禁止靠改 `game_dirs.txt` 排除目录** —— 天马启动会重写回原样；幽灵条目只能删备份目录根治。
5. **禁止整份覆盖 `metadata.pegasus.txt`** —— 只就地 patch 启动命令/字段，云端与设备 ROM 数不匹配会丢游戏。
6. **禁止未经单点确认就批量推广按键/配置改动**。用户说「回轮」= 回滚到指定时间点。正确节奏：查历史结论 → 只改一个 → 实机确认 → 再推广。
7. **禁止对竖版 cfg 整文件覆盖式改按键** —— 只精确替换 4 行方向，保留 a/b/start/select/rotation；禁止新建或污染核心级 `config/remaps/*.rmp`（会作用于该核心全部游戏）。
8. **禁止照搬 `video_rotation` 数值差异推导方向映射**（MAME `rot=1` 与 FBNEO `rot=3` 最终呈现一致）；动手前先查历史。
9. **禁止用 3.2 秒截图或单一亮度阈值判黑屏 / 坏封面** —— 冷启动 8–26 秒；先查前台窗口与 `ANR in com.retroarch.aarch64`（ANR 弹窗造成非黑像素假阳性）。
10. **禁止批量「更新已安装核心」** —— 官方源约 17.5KB/s、nightly 非稳定版，且与 216 个竖版 cfg / 遮罩 / CRT 配套有回归风险；要更新单独点某一个。
11. **清理前必须先出只读清单 + 影响说明并获确认**；设备删除无废纸篓，分批 ≤10 项、每批校验。
12. **禁止假设 adb 能操作 RetroArch / 核心菜单** —— `input keyevent`（含 `gamepad` / `keyboard` 源）、`input tap` 对 RA **全部无效**（RA 直接 poll evdev 设备节点），`sendevent` 报 `Permission denied`（shell 不在 input 组）。只有 BACK(4) 能呼出 RA 菜单（走 Activity 回调）。**核心选项、DOSBox-pure 启动菜单的 auto start 这类操作只能由人手完成**，不要反复试注入。
13. **禁止用 per-playlist cfg 覆盖 `video_font_enable`** —— 必须写进该平台**每个 per-game** cfg（`config/<核心>/<游戏名>.cfg`）；`config/Flycast/ATOMOSWAVE.cfg` 实测不生效。
14. **禁止在 `Roms/<平台>/` 放非 ROM 文件而不先收紧 `extensions`** —— metadata 无 `extensions` 时 Pegasus 按目录扫全部文件，多一个 `.conf` 就立刻多一个幽灵条目。
15. **禁止用设备端 `unzip` 改 `.dosz`** —— 含中文条目名会报 `Invalid entry name`；改包一律在本机用 Python `zipfile` 以 append 模式追加（只写新条目，不重压几百 MB）。

## 按需读取

| 想做什么 | 读哪个 |
|---|---|
| **新机一键安装 / 最短路径 / 不走弯路 10 条** | `INSTALL.md` |
| **优化全过程复盘 / 机能体检 / 失败与更正清单 / 三次用户纠正溯源** | `references/OPTIMIZATION_JOURNEY.md`（仅复盘时读） |
| 60 条禁令全文与正确做法 | `references/HARD_RULES.md` |
| 分项实操手册（metadata / RA 分层 / 竖版 / MSX / 封面 / 详情页 / 街机按键 / DOS / .nomedia） | `references/PLAYBOOK.md` |
| **主题：字太小 / 封面太小 / 返回后回不到原位 / 改 QML 按键** | `references/PLAYBOOK.md` §11 |
| **RetroArch 存档位置 / 存档写到哪 / 换卡或重装后存档消失** | `references/PLAYBOOK.md` §21 |
| 健康校验 SOP、达标基线、已知遗留、清理清单 | `references/VERIFICATION.md` |
| **EKA2L1 / N-Gage 1.0+2.0 / 天马 NGAGE 入口与官方封面** | `references/EKA2L1_NGAGE.md` |
| 查某个脚本干什么 / 全部 22 个脚本与参数 | `references/SCRIPTS.md` |
| 直接执行（推荐） | `scripts/kpa_oneclick.sh`；只跑 7 步用 `scripts/run_all.sh` |

## 一键安装（推荐入口）

> 新机 / 半配置机统一走这里，完整最短路径见 `INSTALL.md`。

```bash
bash scripts/kpa_oneclick.sh --dry-run   # 只读体检 + 计划（设备没连也能预览）
bash scripts/kpa_oneclick.sh             # 体检 → 备份 → 7 步幂等 → 清缓存 → 静态校验 → 报告
```

编排脚本只跑**通用安装**：`step1~step7` 幂等步骤 + 配置级备份（本机 + 设备双回滚点）+ 自动清 `dataCache.json` + `kpa_health_check.sh` 静态校验 + `report.md`（含「必须人手实机确认」清单）。

⛔ **针对特定机器数据的一次性修复不进一键脚本**：热门 10 款置顶、DOS 同名 `.conf`、`.dosz` 补字节、GBA 真盒绘回填、《光明力量》ZIP 伪装解包、土星坏 CHD 删除、CPS1/CPS3 键位、N64 摇杆绑定 —— 只对那台实机成立，按需查 `references/PLAYBOOK.md` §18–§20。

图示属于 `@user_43faedd6` 账号统一的**蓝标（Blueprint Badge）系列**（`assets/blueprints/`），可用 `python3 scripts/blueprint_icons.py` 重新生成、`--check` 校验。

## 前置条件

`KPA_ADB`（platform-tools 里的 adb）、`KPA_TF`（默认 `/storage/6AF3-384F`）、`adb devices` 必须显示 `device`、BIOS 自备（清单 `assets/data/bios_list.txt`：PS / DC / SATURN / PCE-CD / MDCD / MSX / NAOMI 必需，卡带与街机不需要）。四项的完整要求与「不满足时的表现」见 `INSTALL.md` §1。

## 执行流程

```bash
bash scripts/run_all.sh     # step1..step7，幂等，可重跑
```

7 步各自做什么、验收判定见 `INSTALL.md` §3。三个最容易误判的点：

- step1 只认 `pm list packages -3`，不看下载是否成功
- step2 装的是 **prosperoOS**；**kpa-shelf 是另一套手工部署的主题**，不在一键流程内
- step7 只认 `lastrun.log` 的 `N games found` 与 `Cannot open` = 0，不看截图

**专项脚本**（默认只读 / dry-run，完整 22 个与参数见 `references/SCRIPTS.md`）：

| 脚本 | 用途 |
|---|---|
| `kpa_health_check.sh` | 全库静态校验 + 清理盘点（排查一律先跑这个，不写设备） |
| `kpa_gamefix.sh` | 五类实机修复：DOS 存档弹窗 / NDS 双屏 / Flycast 雪花 / Atomiswave OSD / 2P 串控 |
| `kpa_vertical.sh` | 竖版 cfg 4 行方向修正（`--apply` 才写） |
| `kpa_theme_tweak.py` | 主题字号 / 平台条常显 / 返回回原位（`--apply` 才写） |

**体检与清理**：只读扫描命令集、🟢🟡🔴 三色分级、三个「持续产垃圾」开关、ANDROID 卸载五步与分批删除流程见 `references/PLAYBOOK.md` §12；清理硬禁令见 `HARD_RULES.md` 32–35。用户说「检查缓存 / 垃圾」时**只出清单，不在同一轮执行删除**。

**仍需人工**：① RA 首启解包内置核心 ② 自备 BIOS ③ MSX 核心需在 RA 菜单点一次下载 ④ 系统桌面壁纸 ⑤ 详情页观感实机确认 ⑥ **RA / 核心菜单内的任何操作**（adb 注入事件 RA 收不到）。

## 关键技术事实（只列最高频 7 条，其余按需查）

- **EKA2L1 设备只由 `config.yml` 的 `device:` 决定**（intent 的 `appDeviceCode` 完全无效）：**固定 `device: 0` 即可，N-Gage 1.0(QD) 与 2.0(5800) 都正常**。2.0 游戏**无法手工预装**（SISX adler32 bug），只能整体恢复已装好的数据盘；天马入口统一进 Games 平台（直进具体 2.0 游戏 UID 会 native crash）。⛔ 设备端解包 tar 必加 `--no-same-owner`（否则 FUSE `settime: Operation not permitted` 中断）。完整流程见 `references/EKA2L1_NGAGE.md`。
- **`vpx()` 在本机等于 `v × 0.75`** —— 这是"字太小、封面太小"的真正根因（不是设计值不够大）。按真实像素排版要直接用原始数值（kpa-shelf 封装成 `px(v)`，`kScale = 1.0`）。另：QML 方法名不能大写，`function S(v)` 会让整个主题加载失败。
- **改 metadata 后必须清 `dataCache.json`**（`/sdcard/pegasus-frontend/dataCache.json`，约 5.79MB）：`am force-stop` → 删文件 → 重启，重建约 30–40 秒。只 `force-stop` 不够。已有 21 条 NGAGE 等条目时**不要清空重扫**（会出现"没有找到游戏"），应用 Python 改 JSON 的 `games` + `path_to_gamefiles`。
- **Pegasus 每次从游戏返回都会重载主题** —— 位置恢复**只能靠 `api.memory`**（记 `Shelf Game` + `Shelf Collection`），不能指望界面状态残留；且要延迟一拍 + `positionViewAtIndex()` 并补一次 ~400ms 二次定位。
- **PPSSPP 启动禁止 `-d "file://..."`** —— Pegasus 会构造 `Intent.setData()` 触发 `FileUriExposedException`，前端点了没反应。正确写法 `--es "org.ppsspp.ppsspp.Shortcuts" "<本体绝对路径>"`。验证必须**从天马前端点击**并看 logcat `[BOOT] Booted`，⛔ 不能用 `adb shell am start` 代替（假验证）。
- **竖版方向最终值**：`up=h0right / down=h0left / left=h0up / right=h0down`，按键 `a=109 / b=108 / start=97 / select=96`；厂商原版基线是反的，**不要照抄**。竖版判定用 `assets/data/mame_orient.json`（6055 条）。街机核心级 cfg 与 CPS3 `.opt` 的按键坑见 `HARD_RULES` 42 / 44、`PLAYBOOK` §15 / §17。
- **RA 存档已迁到 TF 卡**（`savestate_directory` / `savefile_directory` → `.../6AF3-384F/Android/data/com.retroarch.aarch64/files/`）。三个坑：①本机有**两份** `retroarch.cfg`，生效的是 `/storage/emulated/0/RetroArch/retroarch.cfg`（应用退出回写，属主 u0_a92）；②RA **没有** `MANAGE_EXTERNAL_STORAGE`，存档只能放应用私有目录，放 TF 卡根目录会写不进去；③该版本 `log_to_file` 无效，验证只能比文件数与 mtime。`savestate_auto_save=true` 退出自动存、`auto_load=false` 进游戏不自动读。详见 `PLAYBOOK` §21。

> 其余（metadata 规范、RA 配置分层、MSX 本地镜像、封面修复链路、NDS 双屏、Flycast、DOS、`.nomedia`、kpa-shelf 布局细节）全部在 `references/PLAYBOOK.md`。

## 清理与回滚

设备侧默认零备份，最小回滚点单列在 `references/VERIFICATION.md` §5；回滚也可用 `sync_from_device.sh` 从好机器同步或重跑对应 step。**任何删除前先出清单、说明影响、获确认，分批 ≤10 项逐批校验**（设备无废纸篓）。

## 版本与来源

- 当前 **v2.4.2**（2026-11-18）：RetroArch 存档迁 TF 卡、主题 `isPrevPage` 按键修正、发布前审查瘦身。逐版变更（含 v1.0.0 起全部记录）见 **`CHANGELOG.md`**（唯一版本源）。
- 发布：SkillHub `@user_43faedd6/kpa-pegasus-setup` · ClawHub `kpa-pegasus-setup` · GitHub `lisong2003-lgtm/kpa-pegasus-setup`
- 资源版权归各自所有者；本包只分发配置文本、脚本与自建主题修改，不含 ROM / BIOS / APK。
