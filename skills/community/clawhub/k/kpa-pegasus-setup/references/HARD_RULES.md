# 硬性禁令（60 条）

每一条都来自实机故障或用户纠正。`SKILL.md` 收录前 15 条，本文是全文与正确做法。**编号 1–59 连续无缺**，按主题分组（A 系统层 / B 天马 / C RetroArch / D PSP 与判定 / E 清理与纪律 / F 输入注入），分组只是归类，编号是唯一引用口径。

- 36–40：2026-11-14 清理与 PSP 排障新增，其中 37/38 已按 17:35 回归更正。
- 41：PPSSPP 退出与注入按键陷阱，21:50 用户实体键实测闭环。
- 42–44：街机核心级 cfg 按键污染（42）、playlist 混合编码与死引用（43）、CPS3 六键由 `.opt` 决定（44，⛔ 别套用 42 的 cfg 修法）。
- 45–52：DOS 免选 exe、`.dosz` 崩溃二分、PICO 遮罩、GBA 封面按内容分类、土星 CHD 引导区、扩展名不可信、N64 十字键绑左摇杆、汉化版长片头。
- 53–56：删大文件先留回滚点、删条目同步清封面与历史引用、静态 0 缺失≠封面修好、一次性修复不进通用脚本。
- 57：SkillHub 发布包拒绝 `.png`，图示走 COS + 绝对 URL。
- 58：EKA2L1 设备只由 `config.yml device:` 决定（v2.4.0）。

## A. 系统层与权限

**1. 禁止 `am force-stop com.ayaneo.home`**
- ❌ 为了刷新 AYA 桌面而强杀 → 杀掉 AYAWindow 的 `WindowKeyEventService`，KPA / Android 层系统按键全部失灵，只能关机重启恢复。
- ✅ 刷新用重启或等待；系统按键属于 KPA / Android / AYASetting / AYAWindow 层，**不要在 RetroArch 配置里找它**。排查按键问题先分清是「系统按键」还是「RA 游戏内按键」。

**2. 禁止把 libretro 核心 `.so` 推到 public 路径后指望加载**
- ❌ `adb push xxx.so /sdcard/RetroArch/cores/` → SELinux `avc: denied { execute }`，linker 报 `not accessible for the namespace`。
- ✅ 只有 `/data/data/com.retroarch.aarch64/cores/` 是 `avc: granted { execute }`；靠 APK 内置解包，或让 RA 核心下载器自己装。

**3. 禁止用 `run-as` / `adb root` / `su` / `adb backup` 操作 RA 私有数据**
- `package not debuggable` / production 拒绝 / 无 root / Android 12 `adb backup` 产出 0 字节。
- ✅ 迁移用 `scripts/sync_from_device.sh`（APK 从 `pm path` 拉）+ BIOS 单独拷。

**4. 禁止 `input tap` / 大部分 `input keyevent` 操作 RA ozone 菜单**
- 固件走内核 evdev 直读；`keyevent 66/23/96/97/20` 基本无效。
- ✅ `input motionevent DOWN x y` + 0.3s + `UP x y`（单击=移高亮，再单击=确认）；BACK(4)、方向键 19/20/21/22 有效。

## B. Pegasus 天马

**5. 禁止改 metadata / 新增目录后不清 `dataCache.json` 就判断生效**
- ✅ `rm /sdcard/pegasus-frontend/dataCache.json` → force-stop 重启 `org.pegasus_frontend.android` → 日志 `N games found` 才是准数。缓存会保留已删除游戏（幽灵条目）。

**6. 禁止靠改 `game_dirs.txt` 排除目录**
- 天马启动会重写回原样。
- ✅ 根治幽灵条目只能删掉那个被递归扫描的备份目录。

**7. 禁止整份覆盖 `metadata.pegasus.txt`**
- 云端与设备 ROM 数不匹配会丢游戏。
- ✅ 只就地 patch 启动命令 / 字段；改前留 `.before` 快照，改后清点条目数。

**8. 禁止 ANDROID 集合 `file:` 写 Android 组件名**
- ❌ `file: com.xxx/.MainActivity` → Pegasus 丢弃，表现为整个集合不显示。
- ✅ `extensions: app` + `file: <短名>.app`（真实占位空文件）+ 每个游戏一条 `launch: am start --user 0 -n <包名>/<Activity>`。

**9. 禁止改 `media-pack.bytes` / 往口袋博物馆 media-pack 加文件**
- 触发包校验失败并重下。ANDROID 集合缺图用第 8 条的占位法解决。

## C. RetroArch 配置与按键

**10. 禁止对竖版 cfg 整文件覆盖式改按键**
- ✅ 只精确替换 4 行方向：`up=h0right / down=h0left / left=h0up / right=h0down`；保留 `a=109 / b=108 / start=97 / select=96`、`video_rotation`、x/y 行。
- ✅ 禁止新建或污染核心级 `config/remaps/<核心>/<核心>.rmp`（会作用于该核心全部游戏）。历史上 21:14 的 rmp 污染了 A/B/X/Y，21:53 的 cfg 方向错误，都靠回轮解决。

**11. 禁止未经用户单点确认就批量推广按键/配置改动**
- ✅ 节奏：查历史结论 → 只改一个游戏 → 用户实机确认 → 再推广。「回轮」= 回滚到用户指定的时间点，不是重新生成一份。

**12. 禁止照搬 `video_rotation` 数值差异推导方向映射**
- MAME 2003-Plus `rot=1` 与 FBNEO `rot=3` 最终呈现一致（FBNeo 核心自带旋转叠加）。动手前先查历史结论，别用数值差异反推按键。

**13. 禁止手工在核心 cfg 写 `video_shader` 键**
- 会破坏 RA 自动预设加载链；改 `config/global_*.slangp` 一处即可覆盖上百个逐游戏预设。

**14. 禁止不带 `-e CONFIGFILE` 启动 RA 判断配置成败**
- 不带会读默认配置（中文变 `?`、菜单黑白），容易误判。GBA 启动命令禁止带 `--activity-clear-top`。

**15. 禁止批量「更新已安装核心」**
- 官方源约 17.5KB/s（手动下载卡在 14%）、nightly 非稳定版、与 219 个竖版 cfg / 遮罩 / CRT 配套有回归风险。
- ✅ 中断后的核查：看 `RetroArch/downloads/` 有无 zip 残留、`core_backups/` 有无 `.lcbk`、对 5 个核心冒烟；实测未覆盖任何核心。要更新单独点某一个。

**16. 禁止给 GBA 加遮罩**
- KPA 专为 GBA 设计，240×160 = 1.5 倍原生满屏 960×640，遮罩只会破坏画面。

**17. 禁止把存档/截图放 `/storage/6AF3-384F/save/`**
- RA 进程无 `sdcard_rw` 权限；只能放 TF 卡 `Android/data/<pkg>/files/`。

## D. PSP / 显示 / 判定

**18. 禁止 PSP ROM 只放 TF 卡或删掉 app 私有目录那份**
- PPSSPP targetSdk 35 无 `MANAGE_EXTERNAL_STORAGE`，读不到 TF 卡；双份均为必需，拷到 `/storage/emulated/0/Android/data/org.ppsspp.ppsspp/files/` 并 chmod 666。

**19. 禁止用 3.2 秒截图 / 单一亮度阈值 / 文件大小推断黑屏或封面质量**
- 冷启动 8–26 秒（PS 20s、ATOMISWAVE 20s、`PS/射雕英雄传.chd` 368MB 需 15s、MSX 15–18s、泰拉瑞亚/星露谷 15s）；首轮 27 DARK / 11 BLACK，8 秒复查后 23 个恢复。
- ✅ 先查前台窗口与 `ANR in com.retroarch.aarch64`；ANR 弹窗会造成非黑像素假阳性。中文 zip 条目名还会让 toybox `unzip` 误报 CRC BAD，本机 Python `zipfile` 复核为准。

**20. 禁止并行冒烟任务互相污染截图、禁止强杀 TMNT/Oceanhorn 后直接截图**
- 会留 ANR 弹窗，需 `input tap` 点「等待」清除后再截图。ANR 检测只匹配 `ANR in com.retroarch.aarch64`，否则会串到后台 APP。

## E. 清理与工程纪律

**21. 禁止在设备上留 `.bak*` 备份**
- 用户要求零备份；改动为覆盖式 / 幂等增量，回滚用 `sync_from_device.sh` 或重跑对应 step。
- 实际工程中确需保留的最小回滚点（`GameDetails.qml.bak20261113`、`firmware.bin.bak`）必须在清理清单里单列、经确认后处理。

**22. 清理前必须先出只读清单 + 影响说明并获用户确认**
- ✅ 列出路径 / 大小 / 删除理由 / 回滚点；设备删除无废纸篓，分批 ≤10 项、每批校验。本机删除用可恢复方式（废纸篓或隔离区）。
- 网络受限时不要假设 GitHub raw / bgm.tv / wikipedia / thegamesdb / screenscraper 可达；实测仅 `api.github.com` + gh-proxy + libretro thumbnails 可用（thumbnails 索引走 `git/trees?recursive=1`，contents 分页无效）。macOS adb 用 r34.0.5；大传输分块 55MB / 300 文件，`tar -T` 清单只放文件，校验用 `md5sum "路径"`（带双引号）。

## F. RA 输入注入与配置层级（v2.0.1 新增）

**23. 禁止假设 adb 能操作 RetroArch / 核心菜单**
- ❌ 反复试 `input keyevent 19/20/21/22`、`input gamepad|joystick|dpad|keyboard keyevent`、`input tap`、`input motionevent` 去点 RA 菜单或 DOSBox-pure 启动菜单 —— **RA 完全不接收**。它直接 poll `/dev/input 下的 event* 节点`，绕过 InputManager，注入的事件根本不进它的输入队列（实测四种 source 注入后截图逐像素完全相同）。
- ❌ `sendevent /dev/input 下的 event3 节点 ...` → `Permission denied`（shell 不在 `input` 组；`getevent` 同样读不到，无输出）。
- ✅ 唯一有效的是 `input keyevent 4`(BACK)，走 Activity 回调能呼出 RA 菜单。
- ✅ **天马(Pegasus) 是普通 Qt 应用、走 InputManager**，`input tap` / `input motionevent DOWN x y` + 0.3s + `UP x y` 对它有效。别把天马和 RA 的输入路径混为一谈 —— 这是本条最容易被误推的地方。
- ✅ 结论：RA 核心选项、DOSBox-pure 启动菜单（`→ Set Auto Start`）这类操作**只能人手完成**。脚本负责把"该改哪个文件、改成什么值"准备好，但不要承诺自动点菜单。

**24. 禁止用 per-playlist cfg 覆盖 OSD 开关**
- ❌ 新建 `config/Flycast/ATOMOSWAVE.cfg` 写 `video_font_enable = "false"` —— 实测无效，弹窗照旧显示。
- ✅ 写进该平台**每个 per-game** cfg：`config/Flycast/<游戏名>.cfg`，逐游戏生效（`kpa_gamefix.sh aw-osd` 批量处理）。
- 层级实测：全局 → per-core → per-game 都生效；per-playlist 对 `video_font_enable` 不生效（但 `aspect_ratio_index` 这类显示键在 `NAOMI.cfg` 里是生效的，不能一概而论）。

**25. 禁止在 `Roms/<平台>/` 放非 ROM 文件而不先收紧 extensions**
- ❌ 直接往 `Roms/DOS/` 放 `游戏名.conf` 想让核心自动加载 —— metadata 没有 `extensions` 时 Pegasus 按目录扫全部文件，立刻多出幽灵条目。
- ✅ 要么先给 metadata 加 `extensions: dosz`，要么把辅助文件放到 `Roms/` 之外。

**26. 禁止用设备端 unzip 改 `.dosz`**
- ❌ toybox `unzip` 遇中文条目名报 `Invalid entry name` / `couldn't open`，`unzip -l` 直接无输出。
- ✅ 本机 Python：`zipfile.ZipFile(p, 'a')` 只追加新条目（不重压几百 MB），改完 `z.testzip()` 返回 `None` 才算成功；先 `cp` 一份 `.orig` 到设备同目录，验证通过再删。

**27. 禁止让 P2/P3 与 P1 共用同一个 joypad index + analog_dpad_mode=3**
- ❌ `input_player1_joypad_index = "0"` 与 `input_player2_joypad_index = "0"` 并存，且两者 `analog_dpad_mode = "3"` —— 表现为**推一下左摇杆，1P 和 2P 的角色一起动**、格斗/清版游戏选人时"主副两个角色都进入"。
- 关键机制：`analog_dpad_mode` **不依赖 `input_playerN_*_btn` 绑定**，即使 P2 的按键全是 `nul`，只要索引指向同一个物理手柄，摇杆模拟量仍会被换算成 P2 的方向键。
- 两类核心会踩到：①**没有 remap** 的 `fbalpha2012_cps1/cps2/cps3/neogeo`、`mame2003_plus`、Snes9x、Nestopia、FCEUmm、PicoDrive、PCSX-ReARMed；②remap 里 P2 仍写 `3` 的 Gambatte / Game & Watch / VBA-M。FBNeo / MAME / Flycast / Beetle / Genesis Plus GX / gpSP 等预置 remap 已写 `0`，所以看起来"只有部分游戏出问题"。remap 不含 `joypad_index`，改全局索引即可全部覆盖。
- ✅ 正确配置：P1 保持 `index 0` + `analog_dpad_mode 3`（街机是数字输入，摇杆要当十字键用）；P2 用 `index 1` + `analog_dpad_mode 0`；P3 用 `2`、P4 用 `3`，不要与 P2 撞索引。
- ✅ 改完要**同时**改两份 cfg：天马 launch 传的 `CONFIGFILE`（`/storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg`，真正生效）和 `/storage/emulated/0/RetroArch/retroarch.cfg`（从 RA 图标直接启动时读）。只改后者不生效。
- ✅ 一键：`scripts/kpa_gamefix.sh p2 --apply`（`--revert` 值级还原）。

**28. 竖版街机 per-game cfg：`video_rotation` 只能写 "3"，且方向映射必须与它配套**
- ❌ `video_rotation = "1"`（逆时针 90°）配 `up=h0right / down=h0left / left=h0up / right=h0down` —— 两者差 180°，表现是"画面竖着但方向全反"，推上挡板往下走。MAME 2003-Plus 的 140 个 cfg 曾全是这个错法。
- ✅ 唯一正确组合：`video_rotation = "3"`（顺时针 90°，画面内容"上"落在屏幕**右侧**）+ 上述四向映射。玩家把掌机**逆时针竖转 90°**后画面正立、方向一致。
- 判据：进 arkanoid 看 demo —— **砖块在屏幕右侧、挡板在左下** = 正确；砖块落在左侧 = rotation 被写成 1 了。
- 覆盖范围（2026-11-14 04:00 复核 219 个文件）：`config/MAME 2003-Plus` 139、`config/FinalBurn Neo` 73、`FB Alpha 2012 CPS-1` 3 / `CPS-2` 2 / `NeoGeo` 2。一键核对修正：`scripts/kpa_vertical.sh [--apply] [--keys]`。
- ⛔ **绝对不要改 per-game cfg 的 A/B/START/SELECT**。竖版 cfg 的按键是**厂商基线 + 用户 2026-11-12 实机验收**过的：`a=109 / b=108 / start=97 / select=96`，**且不得写 x/y 两行**（沿用全局 x=99/y=100）。这就是用户口中的「A/B/START/SELECT 互换规则」——机身 A→投币、B→开始、START→射击/1P键、SELECT→第3键。
- ❌ 2026-11-14 03:20 我把 219 个文件"标准化"成全局值 `a=96 / b=97 / start=108 / select=109`，用户立即反馈"方向对了、其他按键还是不对"。**这是本项目第二次犯同一个错**（11-12 21:46 也犯过）。全局值是 `a=96/b=97/start=108/select=109`，只适用于没有 per-game cfg 的普通游戏，**不能往竖版 cfg 里写**。
- 自检：`scripts/kpa_vertical.sh --keys`（dry-run 应输出 `bad_keys=0`）。```
grep -E '^input_player1_(a|b|start|select|up)_btn' "config/MAME 2003-Plus/arkanoid.cfg"
# 期望 a=109 b=108 start=97 select=96 up=h0right，无 x/y 行
```
- 注意 `kpa_vertical.sh` 旧版用 `grep -q '^video_rotation = "[13]"'` 做前置条件，等于把错值当合法值放行 —— 判断"是否已修好"必须同时校验 rotation 与四向映射。

**29. 判断「某游戏是不是竖版」只能用实机日志，⛔ 不能用封面/盒面图**
- metadata 里的 `assets.box_front` 是**海报/宣传画**，比例与帧缓冲无关。据此曾把 4 个横版海报当竖版、把 3 个竖版海报当横版。
- 唯一判据：开 RA 日志（`log_to_file=true` + `log_verbosity=true`），看核心上报的 `[Core] Geometry ... Aspect: 0.750`（竖）或 `1.333`（横）。`Geometry: 800x600` 且无 `SET_ROTATION` = ROM 加载失败（`Romset is unknown`），别当方向问题处理。
- ⚠️ FBNeo 会调 `SET_ROTATION`，但**它只改几何不改画面**：移走 `batsugun.cfg` 后画面变成"竖版被压扁、左右裁切"。所以 FBNeo 的竖版**照样必须有 per-game cfg**。
- 已验证的 41 条 FBNeo 方向结果见 `assets/data/fbneo_orient_probe.json`（`mame_orient.json` 里没有的 rom 先查这份，查不到再实测，别猜）。
- 完整方法见 `references/PLAYBOOK.md` §3.1。

**30. 改完 `metadata.pegasus.txt` 必须删 `dataCache.json` 再重启，否则界面不更新**
- 天马库缓存：`/sdcard/pegasus-frontend/dataCache.json`（含每个平台游戏数）。只 push metadata 不刷新左侧计数，实测 233 改 208 后界面仍显示 233。
- 正确顺序：备份 → `rm dataCache.json` → `am force-stop org.pegasus_frontend.android` → `am start -n org.pegasus_frontend.android/.MainActivity` → 等 8～15 秒重扫。
- 判「生效没有」以设备文件 `grep -c '^game:'` + 清缓存后界面数字为准，不要只看 push 成功。
- 去重前先确认 `file:` 引用是否重合；⛔ 不要把 `neogeo.zip` 当孤立文件删掉（BIOS 依赖）。详见 `references/PLAYBOOK.md` §3.3。
**31. 这台掌机的 A/B 标签与上报位置相反 —— 按位置读键的游戏里 A/B 必然颠倒**
- 实测（2026-11-14）：**物理 A 在右侧** → 内核 `BTN_EAST`(305) → Android `BUTTON_B`(97)；**物理 B 在下方** → 内核 `BTN_SOUTH`(304) → Android `BUTTON_A`(96)。即标签是任天堂式（A 右 B 下），固件却按 Xbox 位置上报。
- 结论：任何**按位置**解释 A/B 的程序（SDL/LÖVE 移植游戏、部分 Unity 游戏）里都是「B=确认、A=返回」。这不是故障，`dumpsys input` 里设备就是 `Microsoft X-box 360 pad`，`Sources: 0x01000511`（KEYBOARD|GAMEPAD|JOYSTICK）。
- 系统层改不了 A/B：AYANEO 掌机设置 → 手柄 → 自定义按键，明确写「暂时仅支持 MODE / LC / RC / = 」；「手柄风格」只有 Xbox / AYANEO 两档，**切换会连带改变按键上报，影响 RetroArch 整套按键基线（a=109/b=108/start=97/select=96），不要为了单个游戏去动**。
- 抓键证据方法：`getevent -lt` 让用户按 A、B、X、Y 各一次，出现顺序为 `BTN_EAST / BTN_SOUTH / BTN_WEST / BTN_NORTH` 即证实标签顺序 = A/B/X/Y。

**32. 清理时禁止按「目录大小」排序直接删 —— 最大的几个目录全是游戏本体**
- 实机反例：`/sdcard/Android/data/` 6.1G 看着像缓存，拆开是 PPSSPP 4.3G（4 个 ISO/CSO）+ pocketmuseum 2.0G（`video-pack` / `media-pack` 资源包），`cache/` 子目录只有 4K。
- 同理禁删：`RetroArch/system/` 387M（BIOS + dats）、`overlays/` 108M、`cheats/` 58M、`/sdcard/PSP/Cheats/` 30M、`RetroArch/temp/` 576K（Vulkan 着色器编译缓存，删了只是变慢）。
- 判据是「删掉后功能会不会少」，不是「占多少」。先 `du -s <dir>/*/` 下钻一层，再决定。完整清单见 `PLAYBOOK.md` §12.1。

**33. `.state.auto` 是存档不是缓存；会话 jsonl / sqlite 是正文不是日志**
- `RetroArch/states/*.state.auto`（`savestate_auto_save=true` 每次退出写）代表游戏进度，最大一份 67.5M。要清必须逐份点名，⛔ 不要 `rm states/*.state*`。
- 本机 `$HOME/.codex/sessions/**/*.jsonl` 是 Codex 对话的 **source of truth**；`$HOME/.workbuddy/projects/**/*.jsonl` 是桌面端本地会话正文（`transport=local` 不上云）；`thread_history_1.sqlite` 虽可从 rollout 重建，但必须先备份 + 完全退出 App。⛔ 都不能当「缓存」清掉。
- `$HOME/.workbuddy/logs/sandbox|traces|20XX-XX-XX/` 与 `$HOME/.codex/logs_2.sqlite` 才是可按日期/保留窗口处理的日志。

**34. 卸载 ANDROID 移植游戏必须走五步，只 `pm uninstall` 会留下点不开的死条目**
- 顺序：① 备份（原 APK 拉本地 + 设备 `metadata.pegasus.txt` / 占位 `.app` / `dataCache.json` 拷 `/sdcard/backup/<game>/`）→ ② `pm uninstall` 并 `pm list packages` 复核 → ③ **就地**删 metadata 的 5 行条目（⛔ 不整份覆盖）并把 `.app` 移走 → ④ `rm dataCache.json` + 重启天马 + 等 12 秒确认缓存重建 → ⑤ 同步本地镜像 `work/meta/ANDROID/metadata.pegasus.txt` 并核对 `grep -c '^game:'`。
- 提醒：LÖVE / Unity 类存档在 `/data/data`，`run-as` 报 not debuggable、`adb backup` 产空 tar（Android 12），**拿不到内部存档**，卸载前必须如实告知用户会丢进度。
- 完整命令见 `PLAYBOOK.md` §12.5。

**35. 「检查缓存/垃圾」= 只读扫描，扫描与删除必须分成两轮**
- 用户说「检查」「看看」「总结」时，只输出路径 + 大小 + 影响 + 分级清单，⛔ 不带 `rm` / `mv`，并明确写「未对你的文件做任何改动，需要删哪项请逐项点名」。
- 本机 `~/Desktop` / `~/Downloads` / `~/Documents` / `~` 属于个人目录，同样只出报告；真要动必须按 🟢🟡🔴 分级、逐项确认、先备份、每批 ≤10 项、每批校验、失败即停，且优先走系统废纸篓而不是 `rm`。
- 设备删除无回收站，配置类删除后必须重启对应 App 验证（尤其改了 `dataCache.json` / metadata）。
- 体检命令集与 2026-11-14 实测基线见 `PLAYBOOK.md` §12.2 / §12.3 / §12.7 / §12.8。

**36. 「放弃进度」「保留一轮」的精确执行口径**
- 「放弃游戏进度」= 只删 `states/*.state.auto`，⛔ 不动 `states/<核心名>/` 子目录（RA 会按核心重建分类），⛔ 不删 `.state` / `.state1` 等手动存档。删前必须整目录 `adb pull` 到本机，设备无回收站。
- 「保留一轮」= 按**时间戳**保留每组回滚点的最新一份，不是按文件名里的 vN 判断（`bak_v5` 反而比 `bak_probe` 早）。`/sdcard/backup/` 的四个子目录是四次不同操作的回滚点，只留最新那个目录，其余整体移走（先备份）。
- 配套检查 `retroarch.cfg` 的 `savestate_auto_save`：为 `true` 时每次退出都会重新生成 `.state.auto`，只删不关等于没清；且 `savestate_auto_load=false` 说明这些存档开机根本不读，纯垃圾。⛔ 改配置属行为变更，必须单独问过用户，不能顺手改。

**37. 判定游戏包重复只能靠 MD5；PSP 双份不能任删一侧**
- 文件名相同 ≠ 重复、字节大小相同 ≠ 重复：卡带/光盘 ROM 容量天然按 2 的幂对齐（GB 0.25/0.5/1/2MB、NDS 64/128/256/512MB），「同大小」组可能有上千个文件却全是不同游戏。59 组同名 zip 里实测只有 9 组 MD5 相同，其余是不同核心要求的不同 romset 版本。
- 方法：小包全量 `md5sum`；>100MB 用 `{ dd 头4MB; dd 中4MB; tail -c 4MB; } | md5sum` 抽样指纹，够判重且不用传回本机。
- `PSP/metadata.pegasus.txt` 里 `file:` 是相对路径（指向 TF 卡 `Roms/PSP/`），`launch:` 却写死 `/storage/emulated/0/Android/data/org.ppsspp.ppsspp/files/...`。Android 11+ scoped storage 下 PPSSPP 读不了 TF 卡任意目录，内置那份才是游戏本体。⛔ 直接删任一侧都会留死条目；正确顺序：① 4 条 `file:` 改成 `.app` 占位 + 加 `extensions: app`；② **把 `launch` 的 `file://` URI 改成 shortcut extra**（禁令 40）；③ 清 `dataCache.json` + 重启天马，从前端逐条点击验证；④ 通过后才删 TF 卡副本。
- `FBNEO/neogeo.zip` 与 `NEOGEO/neogeo.zip` 虽 MD5 相同，但两个核心各从自己的 ROM 目录找 BIOS，🔴 保留两份。

**38. PSP 去重：占位 `.app` + 独立 `launch`，且必须过「三件套验证」才删副本（⚠️ 2026-11-14 17:35 更正）**
- 正确写法：`collection` 头加 `extensions: app`，每条 `file:` 改成短 ASCII 名 `.app`（46B 占位文件）；`launch:` 保持**每条独立且写死内置本体绝对路径**。改 `file:` 不影响启动，只影响天马是否把条目列出来。
- ⚠️ **原文「`launch` 一个字都不要动」是错的**：`file://` URI 会被 Pegasus 构造成 `Intent.setData()`，触发 `FileUriExposedException`，前端点了没反应。必须同时按禁令 40 把 `launch` 改成 shortcut extra，再去重。
- ⛔ 别把 `file:` 改成绝对路径：可能让 `assets.box_front: Imgs/xxx.png` 解析基准漂移，封面丢失。占位 `.app` 保持相对路径不变，实机验证封面仍指向 `Roms/PSP/Imgs/`。
- 三件套（缺一不可，全部通过才允许删 TF 卡副本）：① 清 `dataCache.json` 重启天马，解析缓存确认全库条数不减、PSP 4 条都在、封面路径正确；② **从天马前端点击**启动（`input keyevent 66`），`logcat` 看到 `NativeApp.init(): Launch shortcut parameter:` + `[BOOT] Booted`、截图进游戏 —— ⛔ `adb shell am start` 是假验证（见禁令 40）；③ 删完副本后再从前端启动一次复核。备份 metadata + dataCache 到设备和本机。
- 2026-11-14 实测：全库 3,736 / PSP 4，四个游戏（含两个带空格文件名）冷启动全部 `[BOOT] Booted`，TF 卡 4.14G 副本已删。

**39. 删重复 ROM 必须三处同步，最后做全库死条目复核**
- 三处：① ROM 文件本身；② 对应平台 `metadata.pegasus.txt` 的整块条目（按 `game:` 分块就地删，⛔ 不整份覆盖，diff 应只等于被删块行数）；③ **RetroArch 播放列表** `/sdcard/RetroArch/playlists/*.lpl` 里指向该 ROM 的 item（JSON `items[]`，删后 `json.dumps(indent=2, ensure_ascii=False)` 写回）。⛔ 只删文件会同时留下天马死条目和 RA 死条目。
- 保留哪一份的判据：描述最完整 / 带 `publisher` / `content_history.lpl` 里用户实际玩过的那条。例：保留 `星之卡比：集合!卡比`（历史指向它）、`fatfursp`（原版）、`kof2k4se`（有 publisher），删其余 MD5 相同的别名条目。
- 收尾：清 `dataCache.json` + 重启天马 → 解析缓存核对条数（3,741→3,736）与被删/保留名各出现次数 → 设备端遍历所有 metadata 的 `file:` 逐条 `test -e`，必须 **MISSING 0**。孤儿封面 png 很小，可留着不删。
- 本机已卸载游戏的 APK 原包删除应 `mv` 到 `~/.Trash/`（可恢复），⛔ 不要直接 `rm`；清空废纸篓才真正释放空间。

**40. 禁止用 `file://` URI 启动 PPSSPP；验证必须从前端点击**
- `launch: am start ... -d "file://..."` 在 `adb shell` 里能跑，但 Pegasus 会把它变成 `Intent.setData()`，Android 7+ StrictMode 抛 `android.os.FileUriExposedException`，表现是「条目在、点不开」。
- ✅ 唯一正确写法：`am start --user 0 -n org.ppsspp.ppsspp/.PpssppActivity --es "org.ppsspp.ppsspp.Shortcuts" "<本体绝对路径>"`；collection 级兜底不带 `-a` / `-d`。PPSSPP 1.19.3 `parseIntent()` 在无 `getData()` 时读该 key 作为启动路径。
- ⛔ `org.ppsspp.ppsspp.Args` 只是附加参数，不能用来指定游戏；⛔ 别猜 `content://` URI。
- 验证必须走前端：`input keyevent 21/22` 选游戏 + `input keyevent 66` 启动（`input tap` / `motionevent` 实测无响应），`am force-stop org.ppsspp.ppsspp` 保证冷启动，`logcat` 看 `Launch shortcut parameter` + `[BOOT] Booted`，`grep -c "Failed to run the launch command" lastrun.log` 必须为 0。完整 SOP 见 `PLAYBOOK.md` §13。

**41. 禁止用 adb 注入按键验证 PPSSPP 实体组合键；退出键配置有固定写法**
- 本机 `input keyevent` / `input tap` / `input motionevent`（含显式 source）/ `sendevent`（SELinux `Permission denied`）注入的按键，**只有 BACK(4) 有效**；其余在 native 层不接收。logcat 里 `PPSSPPNativeActivity: KeyEvent Down/Up` 只说明 Java 层收到，不代表 `ControlMapper` 命中。⛔ 用 `input keyevent --longpress 109 & ... 96` 验证 select+B 是假验证（v2.0.1 在 RetroArch 上已记过同一个坑）。
- `VIRTKEY_EXIT_APP` 走 `EmuScreen::OnVKey()`，首行 `if (!IsOnTop()) return;`。暂停菜单、语言选择等任何模态层盖在上面时，组合键被直接丢弃。本机 PPSSPP 冷启动会常驻一个「语言」选择层，远程无法用注入按键关掉，因此**只能请用户用实体键实测**（✅ 21:50 已实测通过，配置生效，见本条状态行）。
- ✅ 定稿配置（源码核对）：`[General]` `AskForExitConfirmationAfterSeconds = 0`（`GameSettingsScreen` 里 `SetZeroLabel("Off")`，0 = 关闭确认）、`PauseMenuExitsEmulator = True`（`leaveGame()` 里 `System_ExitApp()`，暂停菜单「返回主菜单」可直接退出 App）；`[Control]` `AllowMappingCombos = True`、`StrictComboOrder = False`（不检查按键顺序）。
- ✅ `controls.ini` 键名必须精确 `Exit App`；`:` 是 AND 组合、`,` 是替代映射，如 `Exit App = 10-109:10-96`。⛔ `DEVICE_ID_ANY(-1)` 被 `InputMapping::FromConfigString` 显式拒绝，只能写具体设备号；`DEVICE_ID_PAD_0 = 10` 是默认手柄，机身 A/B 颠倒时 B 键可能是 Android 96 或 97，建议 0/1/10~19 全写。
- ⛔ **`adb push` 到 `/Android/data/<pkg>/files/` 不截断**：推比原文件短的内容会留下尾部残片（实测 controls.ini 多出 `97\n9:0-97\n`），且 shell 对该目录无权 `rm`。做法：让新文件不短于旧文件（可补尾随空行），push 后 `pull` 回来做 md5 比对，两者必须一致。
- 兜底路径：BACK → 暂停菜单 →「返回主菜单」→ `PauseMenuExitsEmulator` 触发 `System_ExitApp()`；天马窗口在后台（`mViewVisibility=0x8 GONE`），PPSSPP `finish()` 后系统自然回到天马，无需额外脚本。
- 状态（2026-11-14 21:50 ✅ **已闭环**）：用户用实体键从 PSP 游戏退出成功，回读 `mCurrentFocus=org.pegasus_frontend.android/.MainActivity`，系统自然回到天马。
- 落点（21:55 确认）：`lastrun.log` 里 `[SHELF] resume coll=33 idx=1 title=实况足球 2009` + 截图确认，退出后**停在原平台原游戏**；`api.memory` 恢复机制对独立 App 同样生效，⛔ 不要再为「返回页面」写守护脚本。
- ⛔ **两条被实机证伪的推测**：① PPSSPP 退出时会规范化并写回 ini（自动加 UTF-8 BOM、`RunCount+1`、`FileName0` 改为最近游戏、去掉尾随空行），但**所有自定义键原样保留**，不会「吞掉」配置；② BOM 不是失效原因 —— PPSSPP 自己写回的 ini 就带 BOM 且配置生效，`GameLanguage=-1→11` 也不是语言框触发条件。⛔ 别再据 BOM 推断「ini 段被当成未知段」。
- ⛔ 远程 adb 注入按键无效只是 **adb 层限制**，实体键可正常穿过 PPSSPP 的模态 UI；「远程点不动语言框」≠「设备 UI 有问题」。语言框是否常驻属远程不可判定，但不构成实际阻塞。
- 模板：推送定稿 `assets/ppsspp/{ppsspp.ini,controls.ini}`（无 BOM）、实机生效基准 `*.verified`、原版 `*.orig`。SOP 见 `PLAYBOOK.md` §14 / §14.6。

**42. 禁止把「竖版专用按键映射」留在街机核心级 cfg 里；横版会继承它**
- 竖版基线 `a=109 / b=108 / start=97 / select=96`（把 Select/Start 当 A/B、物理 A/B 当 Start/Select）只在**画面旋转 90°、机器横躺**时才顺手。⛔ 它一旦出现在 `config/<核心名>/<核心名>.cfg` 这种**核心级**文件里，该核心下所有横版游戏全部继承：按机身 A/B(97/96) 变投币，要按 Select/Start(109/108) 才出拳跳。
- 全局标准（`retroarch.cfg`，48 个核心级 cfg 里其余 43 个都继承它）：`a=96 / b=97 / start=108 / select=109`，方向 `up=h0up / down=h0down / left=h0left / right=h0right`。
- 排查顺序：① 读 `rgui_config_directory`（本机 `/storage/emulated/0/RetroArch/config`）② 列出所有「文件名==目录名」的核心级 cfg，看 `input_player1_(a|b|start|select)_btn` ③ 与全局值比对 ④ 确认哪些游戏有 per-game cfg 覆盖（**per-game 优先级高于核心级，改核心级不会破坏竖版**）。
- ✅ 修法：只把核心级那 4 行改成全局标准；⛔ 别删 3 个竖版 per-game cfg 的映射、别改 `video_rotation`、别新建 `.rmp`（remap 会作用于整个核心）。改前 `am force-stop com.retroarch.aarch64`（⛔ 绝不能 force-stop `com.ayaneo.home`），备份到设备 + 本机，push 后 pull 回读 md5。
- 2026-11-14 实测：CPS1 平台 29 条横跨 `fbalpha2012_cps1`（前 12）与 `fbneo`（后 17），26 个横版全被污染；3 个竖版 `1941/mercsj/varth` 有 per-game cfg 不受影响。
- ✅ **22:35 收尾**：CPS-2 / NeoGeo 两个核心级 cfg 也已改回全局标准，至此 **4/4 核心级统一**（CPS-1 / CPS-2 / NeoGeo / FinalBurn Neo），设备读回 md5 一致。备份再增 `/sdcard/backup/cps2-neogeo-keyfix-20261114/` 与本机 `work/cps1-keyfix-20261114/round2/{before,after}/`。
- ⚠️ **22:35 更正（撤销原文误判）**：全设备 `a=109` 共 **226 个文件**，绝大多数是**竖版 per-game cfg 的正确设计**；`FinalBurn Neo/FBNEO {ACT,STG,FLY,ETC} V.cfg` 是竖版分类配置（`aspect_ratio_index=24`，V=Vertical），`a=109` 正确，**不是污染，一律不动**。⛔ 不能按 `a=109` 一刀切扫描后批量改；只认「文件名==目录名」的核心级 cfg。CPS-3 核心级无自定义按键。
- ⚠️ 改 cfg 时 RA 正在前台（用户在实机测游戏），**本轮未 force-stop**：改动对已启动会话不生效、下次启动生效；RA 退出后必须再 pull 回读 md5 确认没被写回覆盖。
- ⚠️ 改 `FinalBurn Neo.cfg` 会作用于 FBNEO/NEOGEO 等所有用该核心的游戏（同为错误映射，属修复）。⛔ RA 不接收 adb 注入按键，配置改完**只能请用户实体键实测**，不得写成「已验证」。SOP 见 `PLAYBOOK.md` §15。

**43. 禁止用严格 UTF-8 解析判 RA 播放列表死引用；`saf://` + `#` 混合编码必须先按字节还原**
- `Nintendo - Game Boy Advance.lpl` 的 `path` 是**混合编码**：`saf://.../GBA/<UTF-8 zip 名>.zip#<GBK 的 zip 内条目名>.gba`。⛔ 用 `json.load(open(..., encoding='utf-8'))` 会直接 `UnicodeDecodeError`；⛔ 用 latin-1 / errors=replace 强读会把中文路径变成 mojibake，据此与文件系统比对会**误判 153 条死引用**（实际全部有效）。
- ✅ 正确口径：`raw = bytes.decode('utf-8', errors='surrogateescape')` → `json.loads(raw)` → 把 path `encode('utf-8', errors='surrogateescape')` 还原字节 → `unquote_to_bytes` **两次**（SAF URI 双重 percent-encode）→ 取 `tree/<卷>:<路径>` 还原成 `/storage/6AF3-384F/...` → **只取 `#` 之前的文件系统路径**（`#` 后是 zip 内部条目，不属于文件系统）。写回同样用 `surrogateescape` 保持字节不变。
- 按此口径 2026-11-14 实测：21 个 playlist / 2,498 条，**恰好 44 条死引用**（FBNeo 14 / GW 19 / MAME2010 8 / GG 1 / PSP 2），GBA 一条都不涉及。
- ✅ 清理 SOP：① 只读出清单 + 影响说明并获确认 ② 停 RA 或确认它不会写回、备份原文件到设备 + 本机 ③ 逐文件过滤 `items`（保留 `version` / `label_display_mode` 等顶层键与键顺序，`json.dumps(ensure_ascii=False, indent=2)`）④ **先 `rm` 目标再 push**（`adb push` 到公共 sdcard 推更短文件也可能留尾部残片）⑤ pull 回读 md5 + 重新解析确认 `DEAD=0` ⑥ 天马不读 playlist，无需清 `dataCache.json`。
- 10 条「同名文件在别的平台目录」也删而非改写路径：这些 ROM 归属不同核心/romset，改写会让核心跑错 ROM；且原路径已不存在、RA 内点了必然失败，天马主库另有正确条目。⛔ 别为「保住入口」擅自改 SAF URI。
- 空 playlist（GW 19→0、PSP 2→0）保留文件不删，保证可逆。回滚：`/sdcard/backup/playlist-clean-20261114/` 五份 cp 回原路径。完整 SOP 见 `PLAYBOOK.md` §16。

**44. 禁止用「修街机核心级 cfg」的思路处理 CPS3 按键；CPS3 的 6 键布局由核心选项 `.opt` 决定**
- CPS3 走 `fbalpha2012_cps3`，其 `config/FB Alpha 2012 CPS-3/FB Alpha 2012 CPS-3.cfg` **只有 aspect/scale/overlay 6 行、没有任何 `input_player1_*`**，继承全局 `a=96 / b=97 / start=108 / select=109` 本来就是对的；也没有 per-game cfg 和 remap。⛔ 不要按禁令 42 给它补写 4 行按键、更不要按 `a=109` 扫描它。
- 全库唯一带「control scheme」选项的街机核心就是它：`fbalpha2012_cps3_controls_p1/p2`（`gamepad`|`arcade`）、`fbalpha2012_cps3_lr_controls_p1/p2`（`normal`|`remap to R1/R2`），文件在 `config/<核心名>/<核心名>.opt`（**不是 .cfg**）。选项定义见 libretro 官方文档与仓库 `libretro/fbalpha2012_cps3` 的 `svn-current/trunk/src/burner/libretro/libretro.cpp`。
- ✅ 6 键格斗（`bStreetFighterLayout`，sfiii2 / sfiii3 / jojoba）在 **`gamepad + normal`** 下是 `fire1=Y / fire2=X / fire3=L / fire4=B / fire5=A / fire6=R` —— 机身 A/B 落在「脚」上，看起来就是「部分按键不正确」；改成 **`arcade`** 后为 `fire1=A / fire2=B / fire3=X / fire4=Y / fire5=L / fire6=R`，即标准街机三拳三脚，且 6 个键（96/97/99/100/102/103）全局都有绑定。4 键游戏在 `arcade` 下也是 `A/B/X/Y` 顺序。
- ⛔ **绝不要开 `remap to R1/R2`**：它会把按键挪到 `RETRO_DEVICE_ID_JOYPAD_R2/L2`（Android 105/104），而本机全局 `input_player1_l2_btn = "nul"` / `r2_btn = "nul"`（只有 `l2_axis=+6 / r2_axis=+7`）。虽然 `getevent -pl` 显示手柄有 `BTN_TL2/BTN_TR2`，RA 侧没绑就是没反应。`arcade` 下该选项对 6 键分支不生效，保持 `normal` 即可。
- ✅ 修法：只把 `.opt` 的 `controls_p1` / `controls_p2` 两行 `gamepad → arcade`，其余行一字不动；**先 `rm` 目标再 push**、pull 回读 md5。改前确认 RA 已退出（`ps -A | grep retroarch` 为空），否则退出时可能写回；改完冷启动一次 `sfiii3` 确认核心加载/游戏可进，再复核 `.opt` md5 未被覆盖。回滚：`/sdcard/backup/cps3-keyfix-20261114/` 或 `assets/ra-cps3/` 之外的 `before/CPS-3.opt` cp 回去。
- ⚠️ 与禁令 12 一致：**实体按键手感必须用户实机确认**，远程只能验证「核心接受该值、游戏能启动、配置没被写回」，不得写成「按键已修好已验证」。完整 SOP 与映射表见 `PLAYBOOK.md` §17。

**45. 禁止把「DOS 必须进核心菜单手点 Set Auto Start」当成不可解；同名 `.conf` + `[autoexec]` 可全自动绕过**
- `DOSBox-pure.opt` 的 `dosbox_pure_conf` 合法值只有 `false` / `inside`（读 `.dosz` 内 `dosbox.conf`）/ `outside`（读 ZIP 旁同名 `.conf`）。选 **`outside`**：不用改动几十/几百 MB 的 `.dosz`，只要在 `Roms/DOS/<游戏名>.conf` 写 `[autoexec]` → `C:` → `CD \` → `PLAY.BAT`。
- 15 个 `.dosz` 的包内**几乎都有 `PLAY.BAT`**（`金庸群侠传` 是小写 `play.bat`，DOS 大小写不敏感）。⛔ 不要凭 exe 列表猜启动命令，更不要只取列表前 N 条（早期脚本截断 `exe[:25]` 曾把《轩辕剑外传-枫之舞》误写成 `CHNA1.EXE`）；先解出 `PLAY.BAT` 内容再定。
- ✅ 单点验证：先把核心 `.opt` 备份 → 只给《毁灭战士2》写 conf → `dosbox_pure_conf=outside` → 冷启动 9s 截图确认直接出 id Software 标题画面、启动菜单完全消失，再批量推广 15 份。2026-11-15 抽样 8 款（含仙剑/炎龙骑士团/金庸/枫之舞/龙骑士4/明星志愿/魔胎）全部直接进游戏、无崩溃。
- ⛔ 例外必须单独定制：《大唐英雄传》原 `PLAY.BAT` 的 `IMGMOUNT D CDROM.ISO -T ISO` 在 DOSBox-Pure 上报 `Type "ISO" is unsupported`，且末尾 `MOUNT -U D` 会把盘卸掉；正确写法见禁令 46。

**46. 禁止把 DOSBox-Pure 的 `retro_load_game` SIGSEGV 归因于启动脚本或内嵌 ISO；用 ZIP 条目二分定位**
- 《大唐英雄传.dosz》冷启动 `Fatal signal 11 (SEGV_MAPERR)`，backtrace `#05 core_load_game+156` —— **载入阶段就崩**，与 `[autoexec]`、`PLAY.BAT`、CD 挂载全无关。⛔ 别再去改启动命令试图绕开。
- 本地全量校验：1010 个条目、local header 全合法、无重名、无非 ASCII、无 ZIP64、ISO 头 `CD001` 有效、ZIP 结构完好。⛔ 重建脚本里若把 `ZipInfo` 直接传给 `writestr` 会**原地改写 header_offset**，下一轮 `z.read(name)` 会误报 `Overlapped entries ... (possible zip bomb)`；必须 `copy.copy(i)` 并用 `z.read(i)` 读。
- ✅ 用「只打包前 N 个条目」生成 `_probe.dosz` 冷启动看有无 `Fatal signal 11`，二分 10 轮定位到 **`GAME.IMG`（307200 = 0x4B000）**——恰好等于崩溃寄存器 `x19`，即核心把这个图片数据文件误判为软盘镜像后在**文件末尾越界读**。
- ✅ 最小修复：`GAME.IMG` 尾部**补 1 个 `\0`**（307201 字节）即可不崩，保留原文件名、游戏按固定记录长度读取不受影响。对照实验：改名 `GAME.DAT` / 补齐到 360K / 补 1 字节三者都不崩，但改名会破坏游戏引用、补齐 61440 字节可能改变文件大小语义，**只选补 1 字节**。修后完整 1010 条目重建包 `crash_lines=0`。
- ✅ 修完再定启动命令（不是 PLAY.BAT）：`IMGMOUNT D CDROM.ISO -t iso`（**必须小写**）→ `midi sb220` → `nlb`。实测三要素缺一不可：无 `IMGMOUNT` 或大写 `-T ISO` 都会退回 `C:\>`；加上后 12s 出「大唐英雄傳 / 遊戲開始」标题画面。⛔ 不要执行原 `PLAY.BAT` 末尾的 `MOUNT -U D`。

**47. 禁止把「PICO 遮罩不生效」继续归因于核心级 / per-game cfg；该核心必须走专用主配置**
- `Retro8.cfg`、`PICO-8.cfg` 核心级写 `input_overlay`、以及同时在 `config/Retro8/` 和 `config/PICO-8/` 放同名 per-game cfg，三种做法**实机全部无遮罩**。
- ✅ 唯一生效路径：新建独立主配置 `.../com.retroarch.aarch64/files/retroarch_pico.cfg`，写死 `input_overlay = "/sdcard/RetroArch/overlays/PICO_B.cfg"` + `input_overlay_enable="true"` + `input_overlay_enable_autopreferred="false"` + `input_overlay_hide_when_gamepad_connected="false"`，再把 **PICO 集合 `launch` 的 `-e CONFIGFILE`** 从全局 `retroarch.cfg` 指向它。实机截图确认左右红细线与竖排 `PICO-8` 标记出现。
- MSX 是另一种病因：`config/blueMSX/` **只有 `.opt`、根本没有 `.cfg`**；补 `MSX_B.cfg`/`MSX_B_frame.png` + 核心级 `blueMSX.cfg` + 样例 per-game cfg 即生效。⛔ 两个平台病因不同，别照抄。
- PICO-8 卡带原生 128×128 **正方形**，⛔ 不要把「看起来画面偏竖」当成竖版游戏去补 `video_rotation`。

**48. ⚠️ v2.2.6 更正：禁止用尺寸或颜色「一刀切」判断 GBA 占位封面；必须按图像内容分类，且替换前双备份**
- 2.2.5 曾把 `Image.open(f).size == (500,315)` 的 213 张一律判为「纯文字占位横条」并全部换成自绘文字卡 —— **这是错的，且造成用户二次反馈「GBA 封面还是不对」**。libretro-thumbnails 的 `Nintendo_-_Game_Boy_Advance/Named_Boxarts` 里 `500×315` 本身就是合法真盒绘尺寸（本轮下载 141 张中 43 张为此尺寸）。备份复核：213 张中 **54 张是真实日版盒绘**（《金童卡修》《魔法封神》《魔法元素》《三国志》三作各有专属封面），只有 **159 张**是纯文字占位卡。
- ✅ 正确判据（缩到 100×63）：**粗色桶数** `len({(r//48,g//48,b//48)})` —— 单色渐变占位卡 ≈ 13–15，真盒绘 ≥ 40（常见 60–110）；**高频细节量** `mean(|p[x+1]-p[x]|)` —— 占位卡 3–12，真盒绘 15–30。⛔ 主色占比 / 颜色总数完全无效：占位卡是渐变，6300 像素能有 6000 种颜色，这正是 2.2.5「检测结果为 0」的原因。
- ✅ 正确流程：① 替换前 `adb pull` 到本机 + 设备 `cp` 双备份；② 按内容分「真盒绘 / 占位卡」；③ 真盒绘**原样恢复**（中文游戏专属封面比英文通用盒绘更贴切）；④ 占位卡才补 libretro 真盒绘；⑤ 仍无对应盒绘的做精修标题卡（中文名清晰、不裁切）；⑥ 统一输出 480×640 并**实机看货架**确认。
- 中文名→盒绘映射要「精确英/日文标题关键词 + 人工校对」，⛔ 别用宽泛词取第一个命中：`仓鼠天堂` 会命中 `Hamtaro Card-e` 卡片、`超人特攻队` 会命中 `2 Games in 1` 合辑；而 `Tales of the World - Summoner's Lineage`、`Metroid Fusion`、`Mario _ Luigi - Superstar Saga`、`Tennis no Ouji-sama 2004 - Glorious Gold` 都有精确文件名，先宽松搜再人工定。
- libretro-thumbnails 仓库名用**下划线**格式；`raw.githubusercontent.com` 常超时/404，优先 `cdn.jsdelivr.net/gh/libretro-thumbnails/<repo>@master/Named_Boxarts/<urlquote(file)>.png`，⛔ 下载后必须 `Image.open().verify()`（jsDelivr 偶发返回 491KB 非图片），失败的换 raw 或换候选文件。

**49. 禁止把三个土星核心一致黑屏归因于核心兼容 / BIOS / 扩展卡；CHD 无引导区应换镜像**
- 《钟表骑士.chd》《钟表骑士 2.chd》黑屏，而《守护英雄.chd》正常。三个核心 `yabasanshiro` / `mednafen_saturn` / `beetle_saturn` / `yabause` **全部黑屏** → 不是核心问题；四个 CHD 头部都是合法 `MComprHD` v5、`cdlz/cdzl/cdfl`、hunk 19584 / unit 2448，结构一致 → 不是格式问题。
- Beetle Saturn 关卡 + 锁日区后能进土星 BIOS 的 **CD 播放器界面**（`TRACK 00 / TIME 00:00 / SEGA`），即 BIOS 正常但**光盘没有可引导的 Saturn IP.BIN** → 镜像自身坏 dump / 非土星盘。⛔ 不要再改 `beetle_saturn_cart` / `yabasanshiro_force_hle_bios` / region 来「救」它。
- ⚠️ 这些实验改动都写在**核心级 `.opt`**，会影响《守护英雄》等正常游戏；实验完必须从备份 `cp` 回去并回归验证（本轮 `non-black pixels 13798/16000` 确认守护英雄仍正常）。
- ⛔ 本机 v5 CHD 的 map 是**压缩**存放的，`mapoff + 12*hunks <= filesize` 这种朴素公式会把能正常运行的《守护英雄》也误报 TRUNCATED，别拿它当损坏判据。

**50. 禁止相信扩展名即内容；`.md` 可能是 ZIP，启动期蓝屏不等于 OSD**
- 《光明力量.md》《光明力量2.md》打不开：文件头是 `PK\x03\x04`，实为 ZIP 伪装，内层才是真 ROM（`shining-force-cn.md` / `shining-force-ii-cn.md` + `__MACOSX`）。解包替换后两作均正常进游戏（1 出剧情文字、2 出汉化片头）。⛔ 改核心/改 cfg 都救不了。
- VARCADE / MAME 2003-Plus 启动期的蓝底旋转 `DIP SWITCH SETTING` 是**游戏自检画面**（约 20s 自动过去，22s 已见 TAITO 片头），⛔ 不是 RetroArch OSD、也不是「左下角弹窗」。`video_font_enable=false` 只关 RA 文字 OSD；搭配 `savestate_auto_save=false` / `rewind_enable=false` 可消除存档失败类提示。副作用：该核心不再显示存档/快进/截图 OSD。

**51. 禁止用 `input_player1_analog_dpad_mode` 修「实体十字键无效」；N64 正解是把 D-Pad 绑到左摇杆四轴**
- 该选项语义是 **analog → dpad**（把摇杆输入转成数字方向），不是 dpad → analog。2.2.5 把核心级改成 `= "1"` 完全无效，用户回报「N64 方向键还是不行」。
- Mupen64Plus-Next 的角色移动读 **RetroPad 左摇杆**，而机身十字键只绑在 `input_player1_(up|down|left|right)_btn = "h0*"`（RetroPad D-Pad，多数 N64 游戏不用）。正解是核心级 `config/Mupen64Plus-Next/Mupen64Plus-Next.cfg` 追加：
  ```ini
  input_player1_analog_dpad_mode = "0"
  input_player1_l_x_minus_btn = "h0left"
  input_player1_l_x_plus_btn = "h0right"
  input_player1_l_y_minus_btn = "h0up"
  input_player1_l_y_plus_btn = "h0down"
  ```
  ⚠️ 只写 `*_btn`、不要动 `*_axis`（全局已有 `-0/+0/-1/+1`，实体摇杆仍可用）。⛔ 别新建核心级 `.rmp`（禁令 7）。冷启动冒烟 + 回读 cfg 未被写回后，**实体键手感仍须用户实测**（禁令 12）。

**52. 禁止把汉化 / 破解版 ROM 的长片头判为「游戏无法启动」；先看 lastrun.log 的等待时长**
- 《恶魔城：月下夜想曲》2003 中文汉化版：8s 汉化声明 → 14s `中文版 STAFF` → 35s `Agemo / ASM Hack` → 60s 标题 LOGO → 75s **「音乐欣赏模式」菜单**（需选「退出」进游戏）；90/110s 仍停在该菜单等输入，全程零崩溃。
- `lastrun.log` 显示用户 01:12:51 `launch`、01:13:45 `resume` —— **只等了 54 秒**，比出 LOGO 还早。⛔ 别去改核心 / BIOS / cue / 换核心，也别写「已修复启动」。
- 正确动作：60–110s 时间线截图 + `grep 'SHELF.*launch\|resume' lastrun.log` 算停留时长；在 metadata `description` 追加片头说明让用户知道要等。可选项：换无长片头镜像，或进游戏后手动存档 + `savestate_auto_load`（首次仍需等）。

**53. 删除大 CHD / ROM 前必须先在本机留回滚点**
- 设备删除无废纸篓。本机 `adb pull` 实测 **39 MB/s**，443MB 两个 CHD 约 11 秒，成本极低。删《钟表骑士》/《钟表骑士 2》时同时备份 metadata、封面、`content_history.lpl`，之后即使理解偏差也能完整恢复。
- ⚠️ 删 VB 时设备侧 `cp` 曾失败（本机 `VB-backup/` 成了唯一回滚点），所以**本机侧 pull 是必需项，不是可选项**。

**54. 删前端条目必须同步清封面与 `content_history.lpl` 历史引用**
- 只删 `metadata.pegasus.txt` 里的 game 块会留下死引用：`/sdcard/RetroArch/playlists/builtin/content_history.lpl` 里本轮有 4 条指向两个 CHD。用 `json.loads` 过滤 `items[].path` 再写回（注意混合编码用 `surrogateescape`）。
- 删除后必须 `force-stop` 天马 → 删 `dataCache.json` → 重启，否则缓存仍显示幽灵条目（禁令 3）。

**55. 禁止「静态引用 0 缺失」就宣布封面修好；必须实机截货架看观感**
- 2.2.5 的 213 张文字卡让 `assets.box_front` 引用全部存在，静态校验全绿，但用户看到的是「没有封面」。视觉类验收必须：切到该平台货架截图 → 确认封面有游戏图像、中文名没被裁、没有空白格 → 再写结论。
- 切平台不用手点：改 `/sdcard/pegasus-frontend/theme_settings/kpa-shelf.json` 的 `Shelf Collection` 下标（从 `dataCache.json` 的 `collections[]` 顺序取，本轮 GBA=14），`force-stop` + 重启天马即可。

**56. 禁止把「特定机器的一次性数据修复」塞进通用安装脚本**

- `kpa_oneclick.sh` 只跑在任意 KPA 上都成立的 7 个幂等步骤。以下只对那台实机成立，⛔ 不许进一键脚本、不许默认推广：热门 10 款 `sort-by` 置顶、DOS 15 份同名 `.conf`、`大唐英雄传.dosz` 的 `GAME.IMG` 补 1 字节、GBA 213 张真盒绘回填、《光明力量》ZIP 伪装解包、土星坏 CHD 删除、CPS1/CPS3 键位、N64 十字键→左摇杆四轴绑定。按需查 `PLAYBOOK` §18–§20。
- 判断标准：**「换一台机器还成立吗？」** 不成立就是特例。特例必须写在 PLAYBOOK 并标注实机前提，不能写成安装步骤。
- 一键脚本必须自带三个收尾：配置级备份（本机 + 设备双份）、自动删 `dataCache.json` 重启天马、报告里列「必须人手实机确认」清单。缺任一项都不算「不走弯路」。

**57. ⚠️ SkillHub 发布包拒绝所有 `.png`；图示必须先传 COS，文档用绝对 URL 引用**
- **实测（v2.3.0）**：`skillhub publish` 带 `icon.png` 直接返回 `400 不允许的文件类型: icon.png`——服务端按扩展名拒绝二进制文件，原 skill 文档「SkillHub / ClawHub 只允许文本类文件」属实。⛔ 别再把 png 放进发布目录，也别去试 `/skills/<slug>/icon`、`PATCH /skills/<slug>`（全部 405）。
- ✅ 正确链路：① `POST /api/v1/skills/<slug>/comments/images?namespace=@<handle>/<slug>`，multipart 字段名 `file`，返回 `{"url":"https://skillhub-*.cos.../skill-comments/uploads/<uid>/<hash>.png"}`，公开可读且持久；② 把 README / INSTALL 里的相对图片路径替换为该绝对 URL，并在包内留一份 `assets/blueprints/URLS.md` 清单；③ 主图标 `iconUrl` 在 `POST /api/v1/community/skills/publish` 的 **payload JSON** 里带（CLI 的 `_post_publish_multipart` 没实现这个字段，需手工构造 multipart）；④ 发布后必须回查 `GET /api/v1/skills/<slug>` 的 `skill.iconUrl`，若为 `None` 先别急着判定失败：**实测 2.3.0 发布返回 `201` 且 `contentAuditStatus=pending`**，此时用户列表 `version` 已变 2.3.0、`stats.versions` +1，但详情 `latestVersion` 仍停在旧版、`/versions` 只列已审版本、`iconUrl` 仍 `None` —— 属内容/图标审核队列，需等审核通过再回查；审核后仍为 `None` 才说明服务端忽略该字段，需在网页端补设（把 COS URL 交给用户）。
- `files` 多 part 用相对路径作 filename，`.md` 用 `text/markdown`，其余 `application/octet-stream`；发布包只保留文本类文件（`.md/.txt/.sh/.py/.json/.ini/.cfg/.opt/.orig/.qml/.verified`）。
- 同账号 15 个 skill 的 `icon.png` 与线上 `iconUrl` 像素 diff=0.00。蓝标系列规范：512×512（或 256×256）、深藏青 `#0A1F3C` 网格蓝图底（32px 细网格 / 128px 主网格）、亮青蓝 `#49D0FF` 圆角外框与线稿、白色辅助线、无渐变无阴影、**主图标无文字**；1 个主体 + 1 个角标，大留白。
- 发布后必须回查 `GET https://api.skillhub.cn/api/v1/skills/<slug>` 的 `skill.iconUrl`、`latestVersion.version` 与 `latestVersion.changelog`，不要只看 publish 返回的 success。本机图示生成器 `scripts/blueprint_icons.py --check` 可校验产物；从发布包安装后若需本地图，重跑该生成器即可。

**58. ⚠️ EKA2L1 设备只由 `config.yml device:` 决定，intent 的 `appDeviceCode` 完全无效**
- 实测：设 `device:1`(5800) 时，即使 intent 带 `--es appDeviceCode RH-29`，FIFA 1.0 仍黑屏；日志 `Device being used:` 显示实际设备。设 `device:0`(QD) 后 1.0 与 2.0 全部正常。⛔ 别再靠改 intent 的 appDeviceCode 切设备，也别为 1.0/2.0 做动态 config 切换 —— **固定 `device: 0` 即可**。
- 2.0 游戏无法手工预装：官方 EKA2L1 0.1.0 SIS 安装器 adler32 bug，手工写注册链全部失败；只能整体恢复已装好的数据盘 tar。intent 直进具体 2.0 游戏 UID 会 native crash，天马入口统一进 Games 平台。详见 `EKA2L1_NGAGE.md`。
- FUSE 私有目录解包 tar 必加 `tar -xf ... --no-same-owner`，否则 `settime: Operation not permitted` 中断；`ls | wc -l` 枚举会少算，封面覆盖用逐个 `[ -s ]` 校验。

**59. ⚠️ 主题 QML 调 `api.keys` 必须用官方方法名：是 `isPrevPage`，不是 `isPreviousPage`**

- 实测（2026-11-17，KPA 960×640）：kpa-shelf 主题把「L1 上一平台」写成 `api.keys.isPreviousPage(ev)`。Pegasus 里**没有**这个方法（官方 `src/backend/model/keys/Keys.h`：`KEYVEC_PROP(PREV_PAGE, prevPage, isPrevPage)`），调用时 `kIs` 走兜底 `ev.key === Qt.Key_PageUp`，而手柄 L1 的键值是 **1048580**，永远不相等 → **表现就是「只有 R1 能切平台，L1 完全没反应」**，且日志里 L1 的 `[KEY] 1048580` 照常打印，极易误判为硬件问题。
- 官方全量方法名（少一个字母都会静默失效）：`isUp / isDown / isLeft / isRight / isAccept / isCancel / isDetails / isFilters / isNextPage / isPrevPage / isPageUp / isPageDown / isMenu`。
- 手柄键值表（`GamepadKeyId`，base `0x100000`）：A=1048576、B=1048577、X=1048578、Y=1048579、**L1=1048580**、L2=1048581、L3=1048582、**R1=1048583**、R2=1048584、R3=1048585、SELECT=1048586、START=1048587、GUIDE=1048588。排查时在主题里 `console.log("[KEY] " + event.key)` 对号即可。
- **L2/R2 在本机拿不到按钮事件**：`getevent` 可见 BTN_TL2/BTN_TR2 的 DOWN/UP 与 `ABS_BRAKE`/`ABS_GAS` 同时上报，SDL 按扳机轴处理、不产生 `GamepadL2/R2`，天马日志里没有对应 `[KEY]`。所以 `settings.txt` 里 `keys.page-up: ...,GamepadL2` / `keys.page-down: ...,GamepadR2` 这两条绑定实际是无效的，别指望 L2/R2 做翻页。
- ⛔ 别用「内核 `getevent` 有 BTN_TL 但天马没日志」就当硬件坏：本机 L1 在 evdev 层正常（BTN_TL DOWN/UP 干净），值也对，纯粹是 QML 拼错。
- `kIs` 的 try/catch 兜底会**掩盖**这类拼写错误（方法不存在不抛异常，只静默返回 false）。改完必须重启天马（`am force-stop org.pegasus_frontend.android` + 重开），Qt 不会热重载 `theme.qml`；覆盖设备文件用 `cat 新文件 > 旧文件` 以保留 `u0_a92:media_rw` 权限。

---

**60. ⛔ RetroArch 存档迁 TF 卡只能放「应用私有目录」，且要先认准唯一生效的 `retroarch.cfg`**

- 本机有**两份** `retroarch.cfg`：`/storage/emulated/0/RetroArch/retroarch.cfg`（属主 `u0_a92`，应用每次退出回写 → **生效**）与 `Android/data/com.retroarch.aarch64/files/retroarch.cfg`（11-15 遗留副本）。改错那份等于没改。判据：哪个文件里的存档路径与实际落盘位置一致，哪个才是活的。
- RetroArch 在本机**没有** `MANAGE_EXTERNAL_STORAGE`（`appops get com.retroarch.aarch64 MANAGE_EXTERNAL_STORAGE` 返回 `default`），读 TF 卡靠 SAF 单独授权 `Roms` 目录。⛔ 因此不能把 `savestate_directory` 指到 TF 卡根目录（如 `/storage/6AF3-384F/RetroArch/`），应用写不进去。唯一正确目标：`/storage/6AF3-384F/Android/data/com.retroarch.aarch64/files/{states,saves}`。
- 迁移顺序固定：TF 卡旧存档先改名 `*.bak_日期` → `cp -r` 内部存档过去 → 按**文件名逐条比对**（`comm -23` 内部 vs TF，必须为 0）→ 改配置 → 实机验证 → **验证通过才删**内部那份。
- ⛔ 验证不能靠日志：该版本 `log_to_file = "true"` **不产生任何日志文件**（`logs/` 始终为空）。判据是 TF 卡 `states` 目录的**文件数与 mtime**（内部份不动、TF 份冒出新文件 = 写通路通），读通路靠「进游戏 → 存档 → 读取存档状态」列表非空，两者都过才算成功。
- 改配置只 `sed` 替换两行并先 `cp` 一份 `.bak_日期`；顺带核查核心级 `config/<核心>/<游戏>.cfg` 不得再写 `savestate_directory`（会抢走路径；本机 467 个 cfg 实测全无覆盖）。
- 存档机制本机实配：`savestate_auto_save=true`（退出游戏/退出 RA 自动写 `.state.auto`）、`savestate_auto_load=false`（进游戏**不**自动读，需手动读取存档状态）、`savestate_auto_index=false`（自动存档固定名，每次覆盖）、`autosave_interval=10`（游戏内 `.srm` 每 10 秒自动落盘）。
