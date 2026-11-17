# 分项实操手册

## 1. Pegasus metadata 规范

文件位置 `<TF>/Roms/<平台>/metadata.pegasus.txt`（UTF-8）。头部与游戏块：

```txt
collection: CPS1
shortname: cps1
extensions: zip
launch: am start --user 0 -n com.retroarch.aarch64/com.retroarch.browser.retroactivity.RetroActivityFuture -e ROM "{file.path}" -e LIBRETRO /data/data/com.retroarch.aarch64/cores/fbalpha2012_cps1_libretro_android.so -e CONFIGFILE /storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg

game: 1941 反击战
file: 1941.zip
assets.box_front: Imgs/1941 反击战.png
description: 《1941 反击战》，CPS1 平台街机射击游戏。
  第二行起缩进两空格可续写长简介。
publisher: CAPCOM
release: 1990
genre: 射击
players: 1-2
```

要点：
- `description:` 支持多行，后续行缩进两空格；留空则主题显示 `No description available`。
- `publisher / developer / release / genre / players` 影响 prosperoOS 详情页「More by 厂商」区块；16 个平台原本缺这些字段。
- per-game `launch:` 覆盖集合级 `launch:`，用于换核心（例：`mercsj / samuraia / sonicwi` 换 `fbneo_libretro_android.so`）或独立 APP（PSP 用 PPSSPP intent）。
- **改完必做**：`rm /sdcard/pegasus-frontend/dataCache.json` → 重启天马。

### ANDROID 移植游戏（关键）

`file:` 必须是真实文件，组件名会被丢弃：

```txt
collection: ANDROID
shortname: android
extensions: app

game: 忍者神龟：施莱德的复仇
file: tmnt.app
launch: am start --user 0 -n com.netflix.NGP.TMNTShreddersRevenge/crc64ce797c93931d6e91.MainActivity
assets.box_front: Imgs/忍者神龟：施莱德的复仇.png
```

用 `scripts/kpa_android_apps.sh` 创建占位文件并推送。已整合 7 个：忍者神龟 / 星露谷物语 / 泰拉瑞亚 / 像素足球19 / 小丑牌 / 海之号角 / 口袋博物馆。封面用 `adb exec-out screencap` 截启动画面生成。

## 2. RetroArch 配置分层（优先级从低到高）

| 层 | 路径 | 说明 |
|---|---|---|
| 全局 | `/storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg` | 黑黄 ozone / vulkan / CRT / 96ms / 存档迁 TF / 官方核心源；**设备上存在两份，改要一起改** |
| 核心级 | `/sdcard/RetroArch/config/<核心名>/<核心名>.cfg` | 该核心全部游戏生效 |
| 全局着色器 | `/sdcard/RetroArch/config/global_*.slangp` | 改这一处可覆盖上百个逐游戏预设 |
| per-game | `/sdcard/RetroArch/config/<核心名>/<ROM名>.cfg` | 竖版旋转 / 方向映射写这里 |
| remaps | `/sdcard/RetroArch/config/remaps/<核心>/<核心>.rmp` | **厂商基线，禁止污染**（会作用于该核心全部游戏） |

`libretro_directory` 指向 `/data/user/0/com.retroarch.aarch64/cores/`，RA 从不读 public `RetroArch/cores/`。显示核查基线：`video_filter=""`（滤镜关）、`video_shader_enable=true` 命中 crt-easymode、厂商 `overlays/*_B.cfg` 边框正常、竖版 cfg 统一 `input_overlay_enable=false`。

## 3. 竖版游戏（219 个 cfg）

**最终统一值**（用户实机「1941 测试正常」）：

```ini
video_rotation = "3"          # 2026-11-14 实测：219 个文件全部 "3"，arkanoid 方向正确
aspect_ratio_index = "0"
video_scale_integer = "false"
input_overlay_enable = "false"
input_player1_up_btn = "h0right"
input_player1_down_btn = "h0left"
input_player1_left_btn = "h0up"
input_player1_right_btn = "h0down"
input_player1_a_btn = "109"   # 机身 SELECT 键 → RetroPad A（MAME Button3）
input_player1_b_btn = "108"   # 机身 START 键  → RetroPad B（MAME Button1 = 射击）
input_player1_start_btn = "97"   # 机身 B 键   → 1P START
input_player1_select_btn = "96"  # 机身 A 键   → 投币
# 不写 x/y 两行：沿用全局 x=99 / y=100
```

- **按键这 4 行是用户 2026-11-12 实机验收的「A/B/START/SELECT 互换」规则，任何时候不要改成全局值 96/97/108/109。** 已有两次整文件覆盖把它改错的记录（11-12 21:46、11-14 03:20）。
- `video_rotation` 的取值随核心/RA 版本会不同（历史记录里 MAME 曾为 "1" 且"呈现一致"）。**唯一判据是画面**：arkanoid demo 砖块在屏幕**右侧**、挡板在**左下** = 对；砖块在左侧 = rotation 差 180°。

- 厂商原版基线是反的：`up=h0left / down=h0right / left=h0down / right=h0up`（69 个 FBNEO cfg 字节级一致，md5 `44950e1a…`）。**翻转时只精确替换 4 行方向**，其余原样。
- 分布（2026-11-14 04:00 复核）：`MAME 2003-Plus` **139**、`FinalBurn Neo` **73**、CPS1 3 / CPS2 2 / NEOGEO 2，合计 **219**，rotation/mapping/keys 三项全 0 异常。
- 修已有 cfg 用 `bash scripts/kpa_vertical.sh --keys`（默认 dry-run，`--apply` 才写）。

### 3.1 怎么确定「一个游戏是不是竖版」——只能用实机探针

**⛔ 盒面图不能判方向**：metadata 的 `assets.box_front: Imgs/x.png` 是**海报/宣传画**（`airass`、`suratk`、`arcadian` 都是竖版海报但游戏是横版/竖版不一），长宽比与帧缓冲无关。曾据此误判 6 个。

**唯一可靠判据**（2026-11-14 实机验证）：让 RA 写运行日志，读核心自己上报的两个字段。

```bash
# 1) 造一份开日志的配置（log_to_file / log_verbosity 置 true），推成 /sdcard/ra_probe.cfg
# 2) 逐个启动，读 /sdcard/RetroArch/logs/retroarch__*.log
adb shell "am force-stop com.retroarch.aarch64; am start -n com.retroarch.aarch64/com.retroarch.browser.retroactivity.RetroActivityFuture \
  -e ROM <rom.zip> -e LIBRETRO <core.so> -e CONFIGFILE /sdcard/ra_probe.cfg"
adb shell 'F=$(ls -t /sdcard/RetroArch/logs/*.log|head -1); grep -E "SET_ROTATION|\] Geometry" "$F"'
```

- **`Aspect: 0.750` = 竖版**（帧缓冲 320×240 已被核心对调）；`Aspect: 1.333` = 横版。
- `Geometry: 800x600` + 无 `SET_ROTATION` = **ROM 没加载成功**（典型是 `Romset is unknown`），不是方向问题。
- ⚠️ **FBNeo 会调 `SET_ROTATION`（竖版给 "1"，个别 "3"），但它只改几何不改画面**：实测把 `batsugun.cfg` 移走后，画面变成「竖版压扁、左右被裁」。所以**竖版仍然必须有 per-game cfg 的 `video_rotation="3"`**，不能指望核心。
- `video_rotation="3"` 在 MAME 与 FBNeo 上输出方向**完全一致**（把截图顺时针转 90° 两张都倒置），所以 219 个统一用 "3" 是对的。
- 已验证结果存 `assets/data/fbneo_orient_probe.json`（41 条：vertical 8 / horizontal 20 / broken 13），DB 缺的 FBNeo 专属 rom 从这份查，别再猜。
- 本轮据此纠正：**新增 7 个竖版 cfg**（`airass arcadian explbrkr samesame2 saturnzi slapfighb1 unclepoo`）；**删除 2 个误配**（`tengaij` 天外、`schmeisr` 实际都是横版 1.333，此前被 `mame_orient.json` 缺失误补进竖版）；**删除 5 个失效 cfg**（`galaga mercsj p47mus samuraia sonicwi`，ROM/metadata 均已不存在）。

### 3.2 「中文名 zip 打不开」的救援法（2026-11-14 实测）

现象：进游戏只显示 `Romset is unknown. THIS IS NOT A BUG!`，日志 `[Core] Geometry: 800x600`。

原因：FBNeo 用 **zip 文件名** 当 romset 名去查驱动表。这批中文名包（`三国战纪-*.zip`、`西游释厄传*.zip`）内部是 **MAME 命名风格**（`a0600.rom`、`a0100.u5`），文件名又不是驱动名 → 查表失败。

两条可行路线（都验证过）：

1. **改名（保原版内容）**：把 zip 复制成 `<驱动名>.zip` 再启动。FBNeo 会按 **CRC** 认 rom，日志出现 `[FBNeo] Using ROM with known crc 0x… from archive …` 即成功。实测 `三国战纪-一统中原.zip → kovytzy.zip` 可直接跑。
   ⚠️ 只适用于目标驱动名**没被占用**的情况。
2. **改指向（本次采用）**：驱动名都已被标准包占用时，直接把 metadata 的 `file:` 改成能跑的 `<驱动名>.zip`，`game:` id 保持不变（收藏/排序不受影响）。原中文 zip 留作存档。

中文名 → FBNeo 驱动名对照（按 rom 特征确认：asic / v1xx / ytzy / a05xx 家族）：

| 货架条目 | 正确驱动包 | 判据 |
|---|---|---|
| 三国战纪-一统中原 | `kovytzy.zip` | `ytzy_v201cn.rom` |
| 三国战纪-乱世枭雄 | `kovshp.zip` | `p0600h_101.rom` |
| 三国战纪-正宗PLUS | `kovplus.zip` | `v119.u2…u6` |
| 三国战纪-风云再起 | `kovsh.zip` | `kovsh_v100_china.asic` |
| 三国战纪2 | `kov2.zip` | `kov2_v100_hongkong.asic` |
| 三国战纪2-群雄争霸 | `kov2p.zip` | `kov2p_igs027a_china.bin` |
| 西游释厄传 | `orlegend.zip` | `a0100.u5` 家族 |
| 西游释厄传SUPER | `olds.zip` | `a0500` + `sp_v101` |
| 西游释厄传2-群魔乱舞 | `oldsplus.zip` | `a05301` 家族 |
| r2dx（雷电DX） | `raiden2dx.zip` | `raidendx_eeprom-r2dx` |
| snowbros3 | `snowbro3.zip` | 条目集完全相同 |
| kov4p / kovsh4p | `kov.zip` / `kovsh.zip` | 4P hack，FBNeo 无该驱动 |

⚠️ `raiden2dx` 是**竖版**（Aspect 0.750），已有 per-game cfg；`r2dx` 条目改指向它后会自动继承该配置，无需另建。

### 3.3 货架去重：重复条目 / 版本变体 / 孤立 zip（2026-11-14 实测）

**症状**：同一款游戏在货架上出现 2～4 条（`三国战纪2` 与 `kov2`；`风云再起` 与 `kovsh` / `kovsh101` / `kovsh102` / `kovsh103`），且大量条目名是裸 rom 文件名。

**去重判据（按可靠度排序）**

1. **`file:` 引用完全相同** → 100% 重复，删 ASCII 条目、留中文条目（`game:` id 不变，收藏与排序不受影响）。
2. **同驱动不同版本号**（`kov115`、`kovsh101~103`、`kov2100/2106`、`kov2p202/204`、`olds100a/103t`、`orlegend111c/orlegendc`）→ 同游戏的不同 revision，普通玩家无差别，条目一并收掉；zip 文件可保留（条目删了就不显示）。
3. ⛔ 不要按名字相似度猜，必须落到 `file:` 或 zip 内 rom 名。

**改完必须做的三项自检**（缺一项就可能出现空条目或两条目抢同一文件）

```python
import re, collections
s = open('/tmp/fb_new.txt', encoding='utf-8', errors='replace').read()
b = re.split(r'(?m)^game:\s*', s)[1:]
ids = [x.split('\n', 1)[0].strip() for x in b]
files = [re.search(r'(?m)^file:\s*(.+)$', x).group(1).strip() for x in b]
print('条目', len(ids), '唯一', len(set(ids)))
print('共用同一 zip:', [k for k, v in collections.Counter(files).items() if v > 1])
```

**⚠️ 关键坑：改 metadata 后界面不刷新 = 天马有库缓存**

天马把整库（含各平台游戏数）缓存在 **`/sdcard/pegasus-frontend/dataCache.json`**（实测 5.7MB）。只 push metadata 再重启，左侧仍显示旧数字（233），必须：

```bash
adb shell 'cp /sdcard/pegasus-frontend/dataCache.json /sdcard/backup/x.bak'
adb shell 'rm -f /sdcard/pegasus-frontend/dataCache.json'
adb shell 'am force-stop org.pegasus_frontend.android'
adb shell 'am start -n org.pegasus_frontend.android/.MainActivity'
```

重扫 3768 条约 8～15 秒，之后平台计数与列表才更新。

**给裸文件名条目补中文名**：不改 `game:` id，只在 `file:` 前插一行 `title: 中文名`（Pegasus 优先显示 title）。本次给 `kov → 三国战纪（初版）`、`r2dx → 雷电DX`、`snowbros3 → 雪人兄弟3`。

**孤立 zip 判定**：拿 metadata 的 `file:` 集合与目录 `*.zip` 求差集。⚠️ `neogeo.zip` 永远是孤立的（BIOS 依赖包），**绝不能删**。

**本次结果**：FBNeo 233 → 208 条（删 25 个重复/变体条目），删掉 13 个孤立 zip 共 252MB（9 个中文包 + `kov4p` / `kovsh4p` / `r2dx` / `snowbros3`）。
⚠️ 实测 `kovsh4p.zip` 报 `Romset is unknown`——FBNeo **没有 kovsh4p 驱动**，而 `三国战纪-风云再起.zip` 与它 md5 完全相同（即 4P hack 版）。所以「改指向标准驱动包」不是偷懒，是这台核心上唯一能跑的路线。

## 4. MSX blueMSX 核心（本地镜像法）

APK 未内置 bluemsx/fmsx；官方源约 17.5KB/s，手动下载会卡在 14%。步骤：

1. 拿到 `bluemsx_libretro_android.so`（可从已安装设备的私有目录或 RA 官方 zip 解出）。
2. 建最小核心源目录：`zip -j bluemsx_libretro_android.so.zip <.so>`，并造 `.index-extended`（**不是 `.index`**）：
   ```txt
   2026-11-10 3f68b86d bluemsx_libretro_android.so.zip
   ```
   格式每行 `日期 哈希 文件名`。只有 `.index` 时 RA 列表显示「没有可显示的条目」。
3. Mac 起 `python3 -m http.server 8765 --bind 0.0.0.0`（目录即核心源目录）。
4. 临时把**两份** `retroarch.cfg` 的 `core_updater_buildbot_cores_url` 改成 `http://<Mac 局域网 IP>:8765/`。
5. RA 菜单：在线更新 → 核心下载 → BlueMSX —— **必须人手在掌机上点**。实测 adb 注入的 `input` 事件 RA 完全收不到（`sendevent` 亦无权限），详见 HARD_RULES 第 23 条。RA 自己下载并解压到私有 cores 目录。
6. 验证 logcat `avc: granted { execute } .../cores/bluemsx_libretro_android.so`；**装完把两份 cfg 改回官方源 `http://buildbot.libretro.com/nightly/android/latest/arm64-v8a/` 并关掉 HTTP 服务**。
7. MSX metadata 加 launch 行指向该核心；BIOS 在 `/storage/emulated/0/RetroArch/system/`（MSX.rom / MSX2.rom + Machines / Databases）。

MSX 冷启动约 15–18 秒出日文字符界面，不是黑屏。脚本见 `scripts/kpa_msx_core.sh`。

## 5. `.nomedia`（图库隐藏）

加 4 个目录，不删文件、不影响天马按路径读封面：

```txt
/storage/6AF3-384F/Roms/
/storage/emulated/0/RetroArch/
/storage/emulated/0/pegasus-frontend/
/storage/emulated/0/Android/data/com.pocketmuseum.app/
```

重扫：`content call --uri content://media --method scan_volume --arg external_primary`。内部存储立即生效（RetroArch 1105→1、pocketmuseum 20002→1），TF 卡卷 `public:179,129` 重扫不生效，**需重启一次**。脚本见 `scripts/kpa_nomedia.sh`。

## 6. 详情页 `GameDetails.qml` 增强

视觉根因：`gamedetails` 是 mainList 第 2 页（需按 ↓），未选中 `opacity: selected ? 1 : 0.5`、标题 `vpx(24)`、简介 `vpx(18)`、`elide: Text.ElideRight` 截断长文、无背景卡片。

增强版 `assets/golden/GameDetails.improved.qml.txt`：opacity 0.5→0.85、加半透明卡片 + 橙色强调条、标题 24→30、简介 18→25、去掉 elide、`lineHeight: 1.3`、左右 margin。固定色写法（不要用 `theme.highlight || ...`，该主题未定义会回退失败）。

原版回滚点 `assets/golden/GameDetails.before.qml.txt`（设备侧 `.bak20261113`）。推送后清 `dataCache.json` 重启，检查 logcat 无 QML/QQml 报错。**RA 完全不接收 adb 注入的输入**（见 HARD_RULES 23），所以详情页观感只能在掌机上目视确认。脚本见 `scripts/kpa_gamedetails.sh`。

内容侧：3772 条 description 平均 46.3 字，约 30%（1142 条）是「《X》，X 平台。」空壳句；用 `scripts/bangumi_desc.py` 升级为真简介并回填 16 个平台的 publisher/genre/release。

## 7. 封面修复链路

坏封面三来源：黑屏图（抓图失败）、小图（<8KB）、缺图。按顺序：

1. zip 内部文件名（汉化 ROM 的原版英文名）→ `https://thumbnails.libretro.com/<系统>/Named_Boxarts/<名>.png` 匹配；系统名形如 `MAME`、`SNK - Neo Geo`、`Bandai - WonderSwan`、`Sega - Game Gear`、`Nintendo - Game Boy Color`。
2. 匹配不到 → RA 实机截图：`am start` 带核心参数 → 等 15–40s → `screencap` → PIL 裁掉 RA 边框缩放 480×320。
3. 三核心全黑 → 标题文字占位图。
4. EASYRPG 特例：从游戏目录 `.xyz` 标题画面按 `xyzpal_first / xyzpal_last` 调色板解码，重做 13 张真封面（Mogeko城堡 / 威伦诺尔 / 寂静岭 / 废都物语 / 怪异症候群1-2 / 恐怖美术馆 / 梦幻重装机兵 / 灰色庭院 / 野比大雄系列 4 作），部署到 `Roms/EASYRPG/Imgs/` 并 md5 校验。

## 8. 冷启动等待基准（冒烟判定）

| 平台 / 游戏 | 出画面时间 |
|---|---|
| PS / SATURN / N64 / MD / SFC / NDS | 8–20s |
| `PS/射雕英雄传.chd`（368MB） | 15s |
| ATOMISWAVE | 20–30s（首屏 NOTICE 版权屏，不是不兼容） |
| MSX | 15–18s |
| 泰拉瑞亚 / 星露谷物语 | 15s |

3.2 秒截图会得出大量假黑屏。判定顺序：前台窗口 → `ANR in com.retroarch.aarch64` → 非黑像素 + 外接矩形 → 再下结论。

## 9. 网络与传输实测

- 可用：`api.github.com`、gh-proxy 镜像、libretro thumbnails。thumbnails 目录索引走 `git/trees?recursive=1`，`contents` 分页无效。
- 不可假设可达：GitHub raw、bgm.tv、wikipedia、thegamesdb、screenscraper。
- macOS adb r34.0.5；大传输分块 55MB / 300 文件；`tar -T` 清单只放文件；校验用 `md5sum "路径"`（中文路径必须带双引号）。

## 10. 实机体验类修复（v2.0.1）

用户实测反馈的六类问题，全部已定位根因并修复。脚本：`scripts/kpa_gamefix.sh`（配置类）+ `scripts/kpa_theme_tweak.py`（主题类），都幂等、支持 `--revert`。

| 现象 | 根因 | 修法 |
|---|---|---|
| DOS 左下角反复刷 `Save State Error` | 全局 `rewind_enable=true` + `savestate_auto_save=true`，而 DOSBox-pure 进来先停在 START MENU、游戏尚未运行 | 只在 `DOSBox-pure.cfg` 关这两项（不影响其它平台倒带） |
| NDS 双屏被纵向拉长、画面被裁 | `melonds_screen_layout="Left/Right"` + `aspect_ratio_index="23"`，两屏并排后又被拉满屏 | 改 `Top/Bottom` + index **21** |
| Atomiswave 背景满屏雪花噪点 | flycast 多线程渲染在 Atomiswave 下有 bug | `reicast_threaded_rendering="disabled"` |
| Atomiswave 左下角 `Please upgrade to MAME romsets` | 核心对旧格式 romset 发 `SET_MESSAGE`，RA 以 OSD 显示数秒 | 每个 **per-game** cfg 写 `video_font_enable="false"` |
| 顶部平台名太小、看不出当前平台 | 字号 24 且选中/未选同色 | delegate 字号 36、选中 `#ffffff` / 未选 `#6affffff` |
| 退出游戏回到平台第一个而非刚才那个 | 2.96GB RAM 下天马被 LMK 回收，重启后只记 `Last Collection` | 记 `Last Game` + `restoreLastGame()` + 电池白名单 |

### 10.1 主题平台条为什么"一直存在却看不见"

`theme.qml` 里 `collectionNav` 写的是 `visible: false`，但它被 `OpacityMask` 的 `ShaderEffectSource` 当作纹理源渲染 —— **平台条其实一直在显示**，只是 `font.pixelSize: vpx(24)` 且所有项同为 `white`（选中项只换字体族，差别极小）。

所以正确改法是只动 delegate 的 `font.pixelSize` 与 `color`（外加 `opacity: gameBar.active ? 1 : 0` → `1` 让它常显）。

⚠️ **不要新造一个"平台名大标题"控件** —— 实测会与遮罩渲染出的那层重叠，出现双层错位文字。

### 10.2 NDS 双屏比例怎么客观定

不要靠肉眼。用截图数"亮像素外接矩形宽度"：

```python
# 960×640 截图，隔点采样后取非黑区域的 x/y 范围
```

实测同一标题画面：`aspect_ratio_index` 为 **21 / 22** 时亮像素宽约 **408px**（核心原始比例，左右留黑边，文字不变形）；为 **23 / 24** 时拉到 **918px**（满屏，纵向变形）。`Hybrid` 布局该核心不支持 —— 设了与 `Top/Bottom` 截图逐像素相同。

### 10.3 一条走不通的路：DOS 自动跳过启动菜单

想省掉每次进 DOS 都要在 `DOSBOX PURE START MENU` 里选程序，试过全部常规路线，**均无效**：

1. `dosbox_pure_conf` 改 `"true"` / `"1"` / `"2"` / 完整 label 四种值 —— 都仍停在菜单；
2. 在 `.dosz` 旁放同名 `.conf`（`[autoexec]` + `PLAY.BAT`） —— 无效；
3. 用 Python 往 `.dosz` 内追加 `DOSBOX.CONF`（CRC 自检通过） —— 无效；
4. 用 `input keyevent` 在菜单里按「→ Set Auto Start」 —— RA 收不到事件（HARD_RULES 23）；
5. `sendevent` 直写 evdev —— `Permission denied`。

**结论：这一步只能人手做。** 操作路径：进游戏 → 菜单出现 → 用 ↓ 移到 `PLAY.BAT` → 按 **→**（`Set Auto Start`）→ 该项出现标记，下次跳过菜单。想恢复菜单：在核心菜单选 Restart 时按住 L2/R2。

15 个 DOS 包的启动项（已逐个解包确认，全部含 `PLAY.BAT`）：

| 游戏 | 启动项 | 实际执行 |
|---|---|---|
| 仙剑奇侠传 | PLAY.BAT | PAL |
| 轩辕剑外传-枫之舞 | PLAY.BAT | SWDA |
| 高校魔影 | PLAY.BAT | g_map |
| 大唐英雄传 / 明星志愿 / 毁灭战士2 | PLAY.BAT | — |
| 炎龙骑士团 / 炎龙骑士团2 | PLAY.BAT | FD / FD2 |
| 英雄传说3-白发魔女 | PLAY.BAT | ED3 |
| 金庸群侠传 | play.bat | — |
| 魔影哈雷 / 魔神战纪2 / 魔胎 / 鹿鼎记 / 龙骑士4 | PLAY.BAT | — |

---

### 10.4 一个手柄同时控制两个角色（P2 串控 1P）

**症状**：某些街机游戏一开局就是"主角色 + 副角色"两个都在场上，且推一下左摇杆两个角色一起动；格斗/清版游戏选人界面两个光标同步移动。有的游戏又完全正常。

**为什么"只有一部分"**：不是按键重复绑定。查 `retroarch.cfg` 会发现 P2 的 `input_playerN_*_btn` 全是 `nul`，看着没问题。真正的原因是：

| 键 | 本机原值 | 后果 |
|---|---|---|
| `input_player1_joypad_index` | `0` | P1 用物理手柄 0（唯一的那个） |
| `input_player2_joypad_index` | `0` | **P2 也用同一个物理手柄** |
| `input_player2_analog_dpad_mode` | `3` | 把该手柄左摇杆**自动换算成 P2 的方向键** |

`analog_dpad_mode` 是独立于按键绑定的旁路：只要索引指向同一只手柄，摇杆模拟量就会喂给 P2 的十字键。所以"P2 按键全是 nul"并不能阻止串控。

**哪些核心会中招**：取决于 `config/remaps/<核心>/<核心>.rmp` 里有没有把 P2 的 `analog_dpad_mode` 写成 `0`（实测值，2026-11-14）：

| P2 analog_dpad_mode | 核心 | 表现 |
|---|---|---|
| `0`（正常） | FinalBurn Neo、MAME、Flycast、Beetle NeoPop/PCE/Saturn/WonderSwan、Genesis Plus GX、gpSP、Handy、NeoCD、Opera、Yabause、DOSBox-pure | 不串控 |
| `3`（仍会串控） | **Gambatte、Game & Watch、VBA-M** | GB/GBA/G&W 都是单人机种，平时看不出来 |
| 无 remap（吃全局 `3`） | **`fbalpha2012_cps1/cps2/cps3/neogeo`（CPS1/CPS2/CPS3/NEOGEO 平台）、`mame2003_plus`（MAME/VARCADE 平台）**、Snes9x、Nestopia、FCEUmm、PicoDrive、PCSX-ReARMed 等 | 街机最明显 |

remap 文件**不含 `joypad_index`**，所以只要把全局的 `input_player2_joypad_index` 改成 `1`，上面三类都一起静默（P2 指不到任何物理手柄）。只改 `analog_dpad_mode` 而索引仍是 `0` 是不够彻底的。

**修法**（`scripts/kpa_gamefix.sh p2 --apply`）：

```ini
input_player1_joypad_index = "0"     # P1 不动
input_player1_analog_dpad_mode = "3" # 街机是数字输入，摇杆要能当十字键

input_player2_joypad_index = "1"     # 指向不存在的第二只手柄 => 2P 彻底静默
input_player2_analog_dpad_mode = "0" # 断掉摇杆直通 2P 的旁路

input_player3_joypad_index = "2"     # 顺移，避免以后插第二只手柄时 P2/P3 抢同一索引
```

两份 cfg 必须同步改，否则会出现"改完没效果"：
- `/storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg` ← 天马 `launch:` 里 `-e CONFIGFILE` 传的就是它，**真正生效**
- `/storage/emulated/0/RetroArch/retroarch.cfg` ← 从 RA 图标直接启动时读

改完 `am force-stop com.retroarch.aarch64` 再启动游戏。想要 2P 时接第二只手柄即可（index 1 正好给它）。

## 11. 天马主题：自建 kpa-shelf（平台分类 + 游戏介绍）

### 11.1 为什么不用现成主题

| 主题 | 实测问题 |
|---|---|
| prosperoOS（厂商原版） | 平台条是横向细字，36 个平台只能露出 6~7 个；字号 24 时几乎看不出当前平台 |
| Reprise | 现代主机风、有三页签，但首页不显示平台，Library 里平台只是筛选胶囊；介绍页不含 description |
| NPE | Xbox 360 风格，按 16:9 设计，3:2 屏上半部大片空白 |
| Library | Steam Deck 风格，首页无平台入口，字偏细 |

共同问题：都不展示 `description`，即使用元数据里已有简介也不显示。

### 11.2 布局与尺寸（960×640 真实像素）

```
┌──────────────────────────────────────────────────────┐
│ 顶栏 58：KPA 游戏库(27px) · 36平台/3769游戏    当前平台+n/m │
├────────┬─────────────────────────────────────────────┤
│ 平台栏  │        封面墙 4 列 × 全宽 722                │
│ 238px  │        cell 177×268 / 封面 167×222           │
│ 两行 52│                                             │
├────────┴─────────────────────────────────────────────┤
│ 信息条 166：缩略图 96×128 │ 标题25 │ 元信息14 │ 简介15×3行 │ 键位 │
└──────────────────────────────────────────────────────┘
```

- 顶栏 58；平台行高 52（短名 21px 粗 + 中文名 15px + 游戏数 14px），分组标题 30px。
- 封面墙 cell 177×268，封面 167×222（`width-10` × 222），名字 15px 最多两行；上下各 16/26px 渐隐。
- 底部信息条 166：缩略图 96×128（`PreserveAspectCrop`）+ 标题 25px + 元信息 14px 红 + 简介 15px/固定行高 23/最多 3 行 + 右上「已玩 N 次」+ 右下键位列。
- **关键**：所有尺寸用 `px(v)`（`kScale=1.0`），**不要用 `vpx()`** —— 本机 `vpx(v) = v×0.75`，用它排版整体缩水 25%，这正是"字和封面偏小"的根因。

### 11.3 三条必须知道的机制

1. **主题会被重载**：游戏启动后 Pegasus 会 minimize 并重新加载主题，返回时 `Component.onCompleted` 重跑。位置恢复只能靠 `api.memory`，不能靠界面残留。
2. **列表定位要延迟**：`ListView/GridView` 在 `onCompleted` 里设 `currentIndex` 会被模型初始化覆盖 → 用 30ms 与 400ms 两次 `positionViewAtIndex()`。
3. **改 metadata 要删缓存**：`/sdcard/pegasus-frontend/dataCache.json`，删掉重启后约 30–40 秒重建。

### 11.4 简介回填

```bash
# dry-run 看会改哪些
scripts/kpa_desc_fill.sh --json assets/desc/zh_desc.json --meta-dir /path/to/Roms
# 真写（自动 .bak）
scripts/kpa_desc_fill.sh --json assets/desc/zh_desc.json --meta-dir /path/to/Roms --apply
```
设备侧可直接：`adb pull` 单平台 metadata → 回填 → `adb push` → 删 `dataCache.json` → 重启天马。

已有 199 条（PS 4 / DOS 15 / SFC 26 / MD 13 / N64 15 / PSP 4 / SATURN 4 / ANDROID 7 / EASYRPG 13 / DREAMCAST 5 / NDS 93）。其余平台仍是模板句，但模板里已含厂商/年份/类型，可反解进 `publisher` / `release` / `genre` 字段。

## 12. 缓存 / 垃圾体检与优化（2026-11-14 实机基线）

### 12.0 铁律：先只读，再分级，最后才删

体检命令**一律不含 `rm` / `mv`**。用户说「检查」「看看」时只交清单，并明确写一句「未对你的文件做任何改动，需要删哪项请逐项点名」。设备删除没有废纸篓；本机 `~/Desktop`、`~/Downloads`、`~/Documents`、`~` 下的个人文件同样只出报告。扫描输出与删除动作必须分成两轮对话。

### 12.1 三色分级（判错一次就丢游戏）

| 级别 | 判据 | 处理 |
|---|---|---|
| 🟢 可清 | 一次性产物：安装残留 APK、解包副本、临时截图、`.bak` 副本、7 天前日志、空的回收站目录 | 备份后分批删 |
| 🟡 需确认 | 还能代表用户进度或可回滚能力：`.state.auto` 即时存档、旧主题 `.qml.bak`、多份 `dataCache.json` 备份、卸载游戏的原 APK 备份 | 逐项问 |
| 🔴 禁删 | 功能数据 / 会话正文：ROM/ISO/CSO、BIOS、遮罩、金手指库、着色器编译缓存、`sessions/*.jsonl`、`projects/*.jsonl`、`thread_history_1.sqlite`（损坏可重建但**必须**先备份 + 退出 App） | 一律不动 |

⚠️ **大 ≠ 垃圾**。本机实测最大的两个目录全是游戏本体：`/sdcard/Android/data/org.ppsspp.ppsspp/files/` 4.3G 是 4 个 ISO/CSO，`com.pocketmuseum.app/files/` 2.0G 是 `video-pack` + `media-pack` 资源包。按 `du | sort -nr` 排完直接删，等于把游戏删了。同理 RA 的 `system/` 387M（BIOS/dats）、`overlays/` 108M、`cheats/` 58M、`PSP/Cheats/` 30M 都是功能数据；`RetroArch/temp/` 576K 是 Vulkan 着色器编译缓存，删了只会让下次启动变慢。

### 12.2 设备侧只读扫描（可整段复制，全程不写设备）

```bash
export ADB=~/WorkBuddy/*/tools/platform-tools/adb       # 或 source scripts/kpa_env.sh
$ADB shell "df -h /sdcard /storage/6AF3-384F /data"                    # 1. 容量基线
$ADB shell "for d in /sdcard/*/; do du -sh \"\$d\"; done"               # 2. 一级目录
$ADB shell "du -s /sdcard/Android/data/*/ | sort -n -r | head -25"     # 3. 应用数据（toybox sort 不支持 -h，用 -n）
$ADB shell "dumpsys diskstats" > /tmp/diskstats.txt                    # 4. 应用缓存/数据/APK 四组数组
$ADB shell "ls -la /data/local/tmp/; du -sh /data/local/tmp/*/"        # 5. 排障临时文件高发区
$ADB shell "ls -la /sdcard/RetroArch/states/ | head -30"               # 6. 自动即时存档
$ADB shell "find /sdcard/RetroArch/config -name '*.bak*' | wc -l"      # 7. 配置备份堆积
$ADB shell "find /storage/6AF3-384F/Roms -name '*.bak*' | wc -l"       # 8. metadata 备份堆积
$ADB shell "du -sh /storage/6AF3-384F/.Trashes/; ls -la /storage/6AF3-384F/.Trashes/501/"  # 9. 回收站
$ADB shell "grep -E '^log_to_file|^log_verbosity|^savestate_auto_save' /sdcard/RetroArch/retroarch.cfg"  # 10. 产垃圾开关
$ADB shell "grep -n 'console.log' /sdcard/pegasus-frontend/themes/kpa-shelf/theme.qml"                  # 11. 主题调试日志
```

`dumpsys diskstats` 的 `Package Names / App Sizes / App Data Sizes / Cache Sizes` 是四组等长的 Python 风格数组，用 `ast.literal_eval` 按下标配对即可得出「哪个包缓存最大」，比逐个 `du /data/data`（无权限）可靠。注意它列出的是**全量包**（含已卸载包的历史统计），别据此判断安装状态，用 `pm list packages`。

### 12.3 本机侧只读扫描

```bash
df -h /
du -sh ~/WorkBuddy/*/work ~/WorkBuddy/*/shots ~/WorkBuddy/*/backup
for d in ~/.Trash ~/Library/Caches ~/Library/Logs ~/Downloads $HOME/.workbuddy $HOME/.codex; do
  [ -e "$d" ] && printf "%8s  %s\n" "$(du -sh "$d" | awk '{print $1}')" "$d"
done
du -sk $HOME/.workbuddy/* | sort -nr | head -15
du -sk $HOME/.codex/*      | sort -nr | head -15
find $HOME/.workbuddy/logs -type f -mtime +7 | wc -l        # 7 天前日志数
```

`$HOME/.workbuddy/logs/sandbox/` 与 `traces/` 是日志大户，按日期分目录，适合「保留最近 7 天」策略；`$HOME/.workbuddy/workspace/sessions/<sessionId>/` 是会话工作区副本，与 `projects/*.jsonl` 的性质不同但也**不要**随手删 —— 先确认该 session 是否还在用。

### 12.4 会「持续制造垃圾」的三个开关

1. `RetroArch/retroarch.cfg` 的 `savestate_auto_save = "true"`：每次退出游戏写一份 `states/<游戏>.state.auto`。实测 16 份共 156M，单份最大 67.5M（动物篮子 / Flycast）。想止血就关掉它，或明确「只删排障期那几份」。
2. 主题 `theme.qml` 里的 `console.log("[KEY] " + event.key)`：**每按一次键**写一条到 `pegasus-frontend/lastrun.log`。排障结束后应移除该行（其余 `[SHELF]` 日志只在关键动作触发，可留）。
3. 排障期间开的 `log_to_file=true` / `log_verbosity=true`：用完必须改回 `false`。2026-11-14 复查已是 `false`，`logs/` 空 —— 这是正确状态，写进体检的期望值。

### 12.5 卸载一个 ANDROID 移植游戏的标准五步（小丑牌实例）

```bash
P=com.playstack.balatro.android; M=/storage/6AF3-384F/Roms/ANDROID/metadata.pegasus.txt
# 1 备份：原 APK 拉本地；设备侧 metadata / 占位 .app / dataCache 拷到 /sdcard/backup/<game>/
$ADB pull $($ADB shell pm path $P | sed 's/package://') work/<game>/base.apk
$ADB shell "mkdir -p /sdcard/backup/balatro; cp $M /sdcard/backup/balatro/; mv /storage/6AF3-384F/Roms/ANDROID/balatro.app /sdcard/backup/balatro/; cp /sdcard/pegasus-frontend/dataCache.json /sdcard/backup/balatro/"
# 2 卸载并复核（LÖVE/Unity 类存档多在 /data/data，run-as 非 debuggable、adb backup 空 tar，拿不到，只能提前说明）
$ADB shell pm uninstall $P; $ADB shell pm list packages | grep -i balatro || echo 已无该包
# 3 就地删 metadata 的 5 行条目（game/file/launch/assets.box_front/description），不要整份覆盖
$ADB pull $M work/<game>/ANDROID-metadata.txt   # 本地 Edit 后 push
# 4 清缓存重启（见 §11.3 / HARD_RULES 30）
$ADB shell "rm -f /sdcard/pegasus-frontend/dataCache.json"
$ADB shell am force-stop org.pegasus_frontend.android
$ADB shell monkey -p org.pegasus_frontend.android -c android.intent.category.LAUNCHER 1
sleep 12; $ADB shell "ls -la /sdcard/pegasus-frontend/dataCache.json"   # 重建才算完成
# 5 同步本地镜像 + 复核
cp work/<game>/ANDROID-metadata.txt work/meta/ANDROID/metadata.pegasus.txt
$ADB shell "grep -c '^game:' $M"     # 6 -> 5
```

封面 `Imgs/<游戏>.png` 可以留着（无害、不进库），但占位 `.app` 必须移走，否则天马仍会按扩展名扫出一个点不开的条目。缓存文件大小变化也能当旁证：本次 5,678,215 → 5,676,952 字节。

### 12.6 真要删时的分批流程

① 明确列出**每一个**待删路径 + 大小 + 影响 → ② 用户逐项确认 → ③ 先 `cp -r` 到备份目录并确认成功 → ④ 每批 ≤10 项 → ⑤ 每批 `ls`/`du` 校验 → ⑥ 涉及配置的，删完重启对应 App 验证 → ⑦ 任一批失败立即停。设备无回收站，本机个人文件走系统废纸篓而不是 `rm`。

### 12.7 2026-11-14 实测基线（下次体检可对照）

| 位置 | 数值 | 级别 |
|---|---|---|
| 内置存储 / TF 卡 | 21G 用 14G（67%）/ 58G 用 33G（57%） | 不紧张 |
| `/data/local/tmp/pcs/` 像素足球资源解包 | 417M | 🟢 最大可清项 |
| `/data/local/tmp/terraria.apk` | 179M | 🟢 安装残留 |
| `/data/local/tmp/` 其余 `catalog.sqlite` 4.6M / `_probe.so` 1.7M / `t.cfg` 117K | 6.4M | 🟢 |
| `RetroArch/states/*.state.auto` 16 份 | 156M | 🟡 先问进度 |
| 应用缓存合计（`diskstats`） | 88.5M；pocketmuseum 47.4M / photosgo 12.3M / ayaneo.home 11.2M / Chrome 6.1M | 🟢 走系统设置清 |
| `/sdcard/backup/` 4 份 `dataCache.json` 副本 | 16M | 🟡 至少留一份 |
| `pegasus-frontend/dataCache.json.bak20261114` | 5.7M | 🟢 |
| `themes/kpa-shelf/theme.qml.bak_*` 3 份 | 72K | 🟡 回滚用 |
| `/sdcard` 根 7 个临时 png + `._RetroArch` | 2.5M | 🟢 |
| TF 卡 13 个 `metadata.*.bak*` + RA config 30 个 `.bak*` | <1M | 🟢 保留最近一轮 |
| `.Trashes/501/` | 空目录 256K | 🟢 |
| PPSSPP ISO/CSO 4.3G、pocketmuseum 2.0G、RA system/overlays/cheats 553M | — | 🔴 禁删 |
| 本机工作区 / `$HOME/.workbuddy` / `$HOME/.codex` / `~/Library/Caches` / `~/.Trash` | 1.0G / 7.0G / 1.6G / 316M / 1.3M(22 项) | 分级见 12.3 |
| 本机 `$HOME/.workbuddy/logs` 788M（sandbox 515M、435 个文件、>7 天 155 个） | — | 🟢 按日期清 |
| 本机 460G 盘剩 347G | — | 无需为腾空间冒险 |

> **2026-11-14 16:40 执行状态更新**：设备侧 🟢 主项已按 §12.6 分批清理（4 批，每批 ≤10 项并逐批校验），`/data/local/tmp` 606M → 12K，内置 7.1G(67%) → 7.7G(64%)，`Data-Free` 7,448,064K → 8,164,392K。仍未动：43 个 `.bak`（<1M 且是配置回滚点，收益远小于风险）、应用缓存 88.5M、全部 🟡/🔴、本机个人目录项。执行明细见工作区 `work/cleanup/kpa-cleanup-audit-20261114.txt`。
>
> **两条执行经验**：① 大文件先找等价来源再决定要不要复制备份 —— `terraria.apk` 与 `pm path` 指向的已装 `base.apk` md5 完全相同，`pcs/` 是本机 `pcs19-orig.apk` 的解包副本，两者都不必再花 600M 备份；② `pm trim-caches 10737418240` 在本机执行后 `App Cache Size` 仍是 92,758,016 不变，**回收应用缓存只能走系统设置 → 应用 → 清缓存**，adb 普通权限写不了 `/data/data/*/cache`。

> **2026-11-14 16:50 第二轮执行状态**：用户答「①放弃游戏进度 ②保留一轮 ③查游戏包重复」。分 3 批（8/8/5 项）删 16 份 `.state.auto` 156M + 5 个旧回滚点；全部先备份到本机 `work/cleanup/pruned-backup-20261114/`（33 文件 / 167M）。`states/` 156M→44K（保留 10 个核心分类空目录），`/sdcard/backup/` 16M→5.4M（只留 `balatro/`），主题只留 `theme.qml` + `bak_probe`。内置可用 7.7G→7.9G(63%)。`savestate_auto_save` 仍为 `true` 未改，需单独确认。

### 12.8 游戏包 / ROM 重复体检（只读）

```bash
# ① 一次遍历拿到精确字节数 + 路径（toybox find 支持 -printf，比 du -a 干净）
adb shell "find /storage/6AF3-384F/Roms -type f -printf '%s %p\n'" > rom-list.txt
# ② 本地按 (basename,size) / (size) 分组找候选，注意同大小组绝大多数是假阳性
# ③ 候选逐个 md5；>100MB 用抽样指纹，避免把文件传回本机
adb shell "{ dd if='FILE' bs=1048576 count=4 2>/dev/null; \
            dd if='FILE' bs=1048576 skip=<size/1M/2> count=4 2>/dev/null; \
            tail -c 4194304 'FILE'; } | md5sum"
# ④ 货架层：拉全部 metadata.pegasus.txt，解析 game:/file:，查跨平台同名、
#    同平台重名、多条共用一个 file、file 指向的实际文件是否存在（死条目）
# ⑤ 已安装与散落 APK：pm list packages -f -3、find ... -iname '*.apk'
# ⑥ PSP 双份必查：stat -c '%d:%i' 两侧 inode；cat PSP/metadata.pegasus.txt 看 launch 与 file
```

**2026-11-14 实测结论**（完整清单见工作区 `work/cleanup/kpa-duplicate-audit-20261114.txt`，本轮未删任何游戏包）：

| 层级 | 结果 |
|---|---|
| APK | 本机 2 个（像素足球19 589M、小丑牌 59.8M，已卸载游戏的原包备份）、设备散落 0、第三方包 9 个各一份 → **无重复** |
| 文件层 | 25,528 文件 / 30.69G，主包 3,720 个 / 29.13G；内容真重复 6 组 **共 4.28G** |
| 货架层 | 3,741 条 / 36 平台；跨平台同名 144 组（56 组在街机集合间）、同平台重名 0、共用 file 1 组（EASYRPG 公共 RPG_RT.ldb）、**死条目 0** |

6 组真重复：PSP ISO/CSO 双份 **4.14G**（4 对 MD5 抽样指纹全同、inode 不同，`launch` 用内置那份、`file:` 却指 TF 卡副本，删前必须先改 `file:`）；NDS 星之卡比两个中文名 65.8M；NEOGEO `fatfur*sp.zip` 四份同内容 32.3M；`kof2k4extra/kof2k4se` 39.2M；`neogeo.zip` BIOS 1.6M（🔴 两核心各要一份）；MAME/VARCADE 4 组 0.4M（收益可忽略）。

⛔ 判定铁律：同名 ≠ 重复、同大小 ≠ 重复。59 组同名 zip 只有 9 组 MD5 相同，其余 50 组是不同核心的不同 romset 版本（例：`sengoku3` FBNEO 42.73MB vs NEOGEO 51.03MB），属于「双平台收录」而非垃圾，要合并必须逐个验证核心兼容性。

> **2026-11-14 17:10 去重执行状态**：用户「①先删两个包 ②能跑就改 PSP ③删 D2/D3/D4」全部完成。
> ① 两个本机 APK `mv` 到 `~/.Trash/*-20261114-1701.apk`（649M，可恢复），`work/pcs` 589M→28K、`work/balatro` 64M→4.4M。
> ② PSP 用**占位 `.app` 方案**（`extensions: app` + 4 个 46B 占位 + 独立 `launch` 不动），过三件套验证：缓存 3,741 条 / PSP 4 条 / 封面路径正确；`am start` 山脊赛车两次都正常加载 Ridge Racer；**验证通过后才删** TF 卡 4 个 ISO/CSO 4.14G，内置 4 份完好。`Roms/PSP/` 现仅 1.8M。
> ③ 删 5 个 ROM（137M）+ 5 条 metadata 块 + 4 条 RA playlist item；NDS 93→92、NEOGEO 168→164、FBNeo lpl 227→223；清缓存重启后全库 **3,736** 条，设备端遍历 3,736 个 `file:` → **MISSING 0**。5 个孤儿封面 png 保留。
> 空间：TF 卡 58G 用 33G(57%)→29G(50%)，可用 25G→30G。备份在 `/sdcard/backup/{psp-dedup,d234-dedup}-20261114/` 与本机 `work/cleanup/` 同名目录。完整细节见 `work/cleanup/kpa-duplicate-audit-20261114.txt` 第六节。
> ⚠️ **该轮第 ② 项「独立 launch 一个字都不动」的结论已被 17:35 的回归推翻，正确做法见 §13**。当时用 `adb shell am start` 验证属假验证，前端根本点不开。

## 13. PSP 条目在前端点不开：`FileUriExposedException`（2026-11-14 实测）

**症状**：天马里 PSP 封面、简介、4 条条目全在，点「开始游戏」却毫无反应；ROM 文件完好，`adb shell am start` 同一条命令能进游戏。

**根因**：Pegasus 在 Android 上把 `launch` 里的 `am start -d "file://..."` 解析成 `Intent.setData()`。Android 7+ 的 StrictMode 禁止跨 App 暴露 `file://` URI，天马 `lastrun.log` 报：

```
[w] Failed to run the launch command: android.os.FileUriExposedException:
file:///storage/emulated/0/Android/data/org.ppsspp.ppsspp/files/xxx.iso exposed beyond app through Intent.getData()
```

`adb shell am start` 由 shell 进程发起，不受该 App 级 VmPolicy 约束，所以能成功 —— **用它做验证会漏掉前端路径，是假验证**。此坑与 ROM 是否双份、是否 `.app` 占位无关。

**修法**：不传 URI，改用 PPSSPP 的快捷方式字符串 extra。`PpssppActivity.parseIntent()` 在 `getData()` 为空时读 `SHORTCUT_EXTRA_KEY = "org.ppsspp.ppsspp.Shortcuts"`，把值当启动路径：

```text
launch: am start --user 0 -n org.ppsspp.ppsspp/.PpssppActivity --es "org.ppsspp.ppsspp.Shortcuts" "/storage/emulated/0/Android/data/org.ppsspp.ppsspp/files/山脊赛车.cso"
```

- ⛔ 不要 `-a android.intent.action.VIEW -d "file://..."`，⛔ 不要猜 `content://` URI。
- collection 级兜底只写 `am start --user 0 -n org.ppsspp.ppsspp/.PpssppActivity`（不带 `-a` / `-d`），避免 `{file.path}` 又变成 file URI。
- 路径含中文 / 空格没问题：Pegasus 把 `--es` 的值作为单个 argv，`logcat` 里路径完整。
- `file:` 仍可用 `.app` 占位（见 §12.8 / 禁令 38），与启动路径互不影响。
- PPSSPP 1.19.3 另有 `org.ppsspp.ppsspp.Args`，但它是**附加参数**、与 `getData()` 共存时排在路径后面，不能用来指定游戏。

**验证 SOP（必须从前端点击，逐条）**：

1. 改完 `rm /sdcard/pegasus-frontend/dataCache.json` → `am force-stop org.pegasus_frontend.android` → 重启，等 `N games found`。
2. `am force-stop org.ppsspp.ppsspp` 保证冷启动。天马是 Qt 应用：`input keyevent 21/22` 选游戏、`input keyevent 66`（ENTER）启动有效；**`input tap` / `motionevent` 实测无响应**。
3. `logcat -d -t 1200 | grep -iE 'Shortcut Parameter|Launch shortcut|\[BOOT\] Booted|FileUriExposed'`：冷启动应出现 `NativeApp.init(): Launch shortcut parameter:` + `[BOOT] Booted <iso>`；热切换应出现 `Posting a 'shortcutParam' message`。
4. 截图确认画面；`grep -c "Failed to run the launch command" lastrun.log` 必须为 0。
5. **带空格的文件名必须单独验**（`侠盗猎车 - 罪恶都市传奇.iso`、`实况足球 2009.cso`），确认参数没被拆断。

2026-11-14 17:35 四条全部冷启动通过：山脊赛车（Ridge Racer 开场）、战神（Ready at Dawn Logo）、侠盗猎车、实况足球；全库仍 3,736 条。配置模板 `assets/meta_latest/PSP.txt`，幂等修复在 `scripts/step5_ppsspp.sh`。

## 14. PPSSPP 退出回天马：配置写法与「假验证」陷阱（2026-11-14 18:55，✅ 21:50 实机确认闭环）

用户诉求：RA 里 select+B 能退出回天马，PSP 里不行。PPSSPP 是独立 App、不吃 RA 的 `input_enable_hotkey_btn` / `input_exit_emulator_btn` 热键，必须用它自己的 `VIRTKEY_EXIT_APP`。

### 14.1 定稿配置
`assets/ppsspp/` 有可直接推的成品与 `.orig` 原版备份，路径：
`/storage/emulated/0/Android/data/org.ppsspp.ppsspp/files/PSP/SYSTEM/{ppsspp.ini,controls.ini}`（⛔ 不是 `/sdcard/PSP/SYSTEM/`，本机无此目录）。

```ini
# ppsspp.ini
[General]
AskForExitConfirmationAfterSeconds = 0   # 0 = Off，见 GameSettingsScreen::SetZeroLabel("Off")
PauseMenuExitsEmulator = True            # leaveGame() -> System_ExitApp()，兜底路径
[Control]
AllowMappingCombos = True
StrictComboOrder = False                 # 组合键不要求按下顺序

# controls.ini（节选，完整 24 组见模板）
[ControlMapping]
Exit App = 10-109:10-96,10-109:10-97,11-109:11-96,...,19-109:19-97
```

- `:` = 同时按住（AND），`,` = 可替代映射（OR）；键名精确为 `Exit App`，另有 `Pause` / `Pause (no menu)` 不可混用。
- `109` = Android `BUTTON_SELECT`；机身 B 键因 A/B 颠倒可能是 `96`(`BUTTON_A`) 或 `97`(`BUTTON_B`)，两个都写。
- ⛔ 不能写 `-1-109`（`DEVICE_ID_ANY` 被 `FromConfigString` 拒绝）；默认手柄是 `DEVICE_ID_PAD_0=10`，覆盖 `0/1/10~19` 最稳。

### 14.2 为什么不能「远程验证通过」
1. 本机 adb 注入按键只有 BACK(4) 有效（`input keyevent/tap/motionevent` 全无效、`sendevent` 被 SELinux 拒）。v2.0.1 在 RA 上已记过同一坑。
2. `EmuScreen::OnVKey()` 开头 `if (!IsOnTop()) return;`。本机 PPSSPP 冷启动后一直盖着一个「语言」模态层，注入按键关不掉，虚拟键送不到游戏层。
3. 所以 `[BOOT] Booted` + 截图有语言框 ≠ 游戏可交互；`KeyEvent Down/Up` 日志 ≠ 映射命中。**这一层只能由用户用实体键确认** —— ✅ 2026-11-14 21:50 用户反馈「可以退出到天马了」，已闭环。⛔ 远程点不动 UI ≠ 设备 UI 有问题：实体键能正常穿过模态层。

### 14.3 推送 SOP（含残片坑）
```sh
# 1) 先停进程，避免 PPSSPP 退出时把内存配置写回覆盖
am force-stop org.ppsspp.ppsspp; sleep 3
# 2) push 前确认新文件不短于设备上旧文件；adb push 不截断，短文件会留尾残片，且 shell 无权 rm
# 3) push 后 pull 回来 md5 比对，必须完全一致
adb pull <device>/controls.ini /tmp/check.ini && md5 /tmp/check.ini <local>/controls.ini
```
实测残留样例：`Exit App = ...0-109:0-97
97
9:0-97
`（后两行是上一次更长文件的尾巴）。

### 14.4 兜底退出路径
BACK → PPSSPP 暂停菜单 →「返回主菜单」→ `PauseMenuExitsEmulator = True` 使 `leaveGame()` 调 `System_ExitApp()`。天马窗口在后台 `GONE`，PPSSPP `finish()` 后系统自然回天马，无需守护脚本。

### 14.5 媒体库重扫（本次已完成）
```sh
content call --uri content://media --method scan_volume --arg external_primary
content call --uri content://media --method scan_volume --arg 6af3-384f   # 卷名必须小写
```
两个卷 `REASON_DEMAND` 成功；TF 卡 25,842 条索引死索引 0，`Missing file` 警告归零，全库 3,736 条不变。卷名大写会静默失败。

### 14.6 实机确认与配置回读（2026-11-14 21:50，✅ 闭环）

用户用实体键从 PSP 游戏退出成功。回读设备：`mCurrentFocus=org.pegasus_frontend.android/.MainActivity` —— 天马窗口在后台，PPSSPP `finish()` 后系统自然回前台，无需守护脚本。

PPSSPP 退出时会规范化并写回 ini：两份文件都自动加 UTF-8 BOM；`ppsspp.ini` 更新 `RunCount 10→11`、`FileName0` 为最近游玩的 `实况足球 2009.cso`、移除为覆盖残片补的尾随空行；`controls.ini` 仅多 BOM。**所有自定义键原样保留**（4 个 General/Control 开关 + `Exit App` 24 组）。结论：

- ⛔ 别再推断「退出写回吞掉自定义键」；18:55 关于「BOM 让 ini 段失效、导致语言向导常驻」的推测也被证伪 —— PPSSPP 自己写的 ini 就带 BOM 且配置生效，`GameLanguage=-1→11` 同样不是触发条件。
- 语言框是否常驻属远程不可判定，但实体键操作不受影响，不构成实际阻塞。
- ⛔ 「远程 adb 注入按键只有 BACK 有效」是 adb 层限制，不是设备/PPSSPP 输入链故障。

资产：`assets/ppsspp/{ppsspp.ini,controls.ini}` 为无 BOM 推送定稿（推前确认不短于设备旧文件），`*.verified` 为本次实机生效基准，`*.orig` 为改动前原版。

未区分项：用户只确认「能退出回天马」，未说明是 `Exit App` 组合键直接命中，还是 §14.4 的暂停菜单兜底；两条路径均已配置可用。

### 14.7 退出落点（21:55 实机确认）

同样以 `lastrun.log` 为准：21:49:26 从天马启动「实况足球 2009」（`[SHELF] launch: ... @ coll 33`），21:49:36 出现 `[SHELF] resume coll=33 idx=1 title=实况足球 2009`。截图 `shots/after-exit-landing.png` 显示左侧选中「索尼 PSP」(4)、红框停在实况足球 2009（2/4）、底部信息条为该游戏详情。

结论：**`api.memory` 的 `Shelf Collection` + `Shelf Game` 恢复机制对 PPSSPP 独立 App 一样有效**。游戏启动后 Pegasus 会 minimize 并整体重载主题，返回时 QML 是全新实例，靠 `api.memory` 才定位回原平台原游戏 —— 这条路径已在 PSP 上验证，不需要额外脚本。⛔ 别为「退出后回到哪个页面」再写守护逻辑，先查 `lastrun.log` 的 `[SHELF] resume`。

## 15. 街机横版按键错位：核心级 cfg 被竖版映射污染（2026-11-14 22:25；✅ 22:35 四个核心级已统一，⚠️ 仍待实体键确认）

**症状**：CPS1 横版游戏（恐龙快打、街霸 2、惩罚者…）按 A/B 没反应或变成投币，要按 Select/Start 才出招；方向键正常。

**根因**：竖版专用映射被写进了核心级 cfg。`config/<核心名>/<核心名>.cfg` 会作用于该核心下**所有**游戏，包括不旋转画面的横版。

```ini
# 错误（核心级，竖版专用）
input_player1_a_btn = "109"      # SELECT 物理键当 A
input_player1_b_btn = "108"      # START 物理键当 B
input_player1_start_btn = "97"   # 物理 A 当 Start
input_player1_select_btn = "96"  # 物理 B 当 Select

# 正确（全局 retroarch.cfg，其余 43 个核心都继承）
input_player1_a_btn = "96"
input_player1_b_btn = "97"
input_player1_start_btn = "108"
input_player1_select_btn = "109"
```

### 15.1 排查命令

```sh
CFG=/sdcard/RetroArch/config   # = rgui_config_directory
# 列出所有核心级 cfg 的按键，与全局比对
grep -E "^input_player1_(a|b|start|select)_btn" "$CFG"/*/*.cfg | grep -E '"(109|108|97|96)"'
grep -E "^input_player1_(a|b|start|select)_btn" /sdcard/RetroArch/retroarch.cfg
```

本机结果：48 个核心级 cfg 中 **5 个**带污染 —— `FB Alpha 2012 CPS-1`、`FB Alpha 2012 CPS-2`、`FB Alpha 2012 NeoGeo`、`FinalBurn Neo`，以及 `FinalBurn Neo/FBNEO {ACT,STG,FLY,ETC} V.cfg` 分类 cfg；`FB Alpha 2012 CPS-3` 无。

### 15.2 CPS1 平台的特殊性

`CPS1/metadata.pegasus.txt` 里 29 条**横跨两个核心**：前 12 条集合级 launch 用 `fbalpha2012_cps1_libretro_android.so`，从 `msword` 起第二条 launch 用 `fbneo_libretro_android.so`。所以只改一个核心级 cfg 修不全：

| 游戏 | 核心 | 继承的 cfg |
|---|---|---|
| 前 12 条（1941 / dino / ghouls / ffight…） | fbalpha2012_cps1 | `FB Alpha 2012 CPS-1.cfg` |
| 后 17 条（sf2 / punisher / wofj…） | fbneo | `FinalBurn Neo.cfg` |
| 1941 / mercsj / varth（竖版） | fbalpha2012_cps1 | **per-game cfg 显式覆盖，不受影响** |

### 15.3 已执行（可逆）

```sh
am force-stop com.retroarch.aarch64     # 防退出时写回覆盖；⛔ 别碰 com.ayaneo.home
cp <两个核心级 cfg> /sdcard/backup/cps1-keyfix-20261114/
# 只把 4 行按键改成全局标准，其余行（aspect_ratio / overlay / rotation）一字不动
adb push <改后> <原路径> && adb pull <原路径> /tmp/check && md5 比对
```

备份：设备 `/sdcard/backup/cps1-keyfix-20261114/`、本机 `work/cps1-keyfix-20261114/{before,after}/`。3 个竖版 per-game cfg md5 未变（`25fb88a7…`）。

### 15.4 未闭环 / 下一步

- ⚠️ **仍待用户实体键实测**：CPS1 `dino` / CPS2 `armwar` / FBNeo `sf2` 各进一次，按 A/B/Start/Select 确认。本机 adb 注入按键 RA 全不接收（禁令 12），远程无法验证。
- ✅ **22:35 已推广**：用户 22:16/22:23 试 CPS1 `captcomm`、22:25 试 CPS2 `armwar`、22:29/22:31 试 CPS3 后要求「继续」，据此把 `FB Alpha 2012 CPS-2.cfg` 与 `FB Alpha 2012 NeoGeo.cfg` 也改回全局标准。**4/4 核心级现在统一** `a=96 / b=97 / start=108 / select=109`，设备读回 md5 一致；备份 `/sdcard/backup/cps2-neogeo-keyfix-20261114/`、本机 `work/cps1-keyfix-20261114/round2/{before,after}/`。
- ⚠️ **口径更正**：全设备 `a=109` 有 226 个文件，绝大多数是竖版 per-game cfg 的正确设计；`FBNEO {ACT,STG,FLY,ETC} V.cfg`（`aspect_ratio=24`）是竖版分类配置，**不是污染、一律不动**。⛔ 只认「文件名==目录名」的核心级 cfg，别按值一刀切。CPS-3 核心级无自定义按键。
- 改 cfg 时 RA 正在前台（用户实机测试中），**本轮未 force-stop**：改动对已启动会话不生效、下次启动生效；✅ 22:37 RA 退出回天马后已 pull 复核，4 个核心级 cfg 与 5 个 playlist 均未被写回覆盖。
- 未动：4 个核心级 cfg 的 `input_overlay_enable="true"` + `ARCADE_B.cfg`，横版仍显示虚拟按键遮罩（竖版 per-game 已 false）。是否关闭待用户定夺。
- 回滚：把 `before/`、`round2/before/` 四份推回原路径即可。

## 16. RA 播放列表死引用清理（2026-11-14 22:35，✅ 已完成）

**症状**：天马里游戏都在、点得开，但直接在 RetroArch 里点某条播放列表条目会失败——路径指向已删除/迁移的 ROM。天马主库读 `metadata.pegasus.txt`，**完全不依赖 `.lpl`**，所以这类坏记录长期隐藏。

### 16.1 判定口径（⛔ 先看这条，否则会误删 153 条）

`Nintendo - Game Boy Advance.lpl` 是混合编码：`path` 中 `#` 前是 UTF-8 zip 路径、`#` 后是 GBK 的 zip 内条目名。严格 UTF-8 解析会抛 `UnicodeDecodeError`，latin-1 强读会 mojibake。正确做法：

```python
raw = open(f,'rb').read().decode('utf-8', errors='surrogateescape')
d = json.loads(raw)
def to_fs(p):
    b = p.encode('utf-8', errors='surrogateescape')
    if b.startswith(b'saf://'):
        s = urllib.parse.unquote_to_bytes(urllib.parse.unquote_to_bytes(b[6:])).decode('utf-8','replace')
        m = re.search(r'tree/([^/]+)(/.*)$', s)
        if m: s = '/storage/' + m.group(1).replace(':','/') + m.group(2)
    else:
        s = b.decode('utf-8','replace')
    return s.split('#',1)[0]        # zip 内条目不属于文件系统路径
```

拿设备端 `find /storage/6AF3-384F/Roms -type f` 的全量路径做集合比对。按此口径 21 个 playlist / 2,498 条 → **恰好 44 条死引用**；GBA 一条都不涉及。

### 16.2 44 条构成

| playlist | 条数 | 原因 |
|---|---|---|
| `Handheld Electronic Game.lpl` | 19 | GW 平台整个移除，TF 卡 `.mgw` 文件 0 个 |
| `FBNeo - Arcade Games.lpl` | 14 | 8 个 kov/olds 版本变体 ROM 已删；6 个路径已迁到 FBNEO/MAME 目录 |
| `MAME 2010.lpl` | 8 | 4 个中文/版本变体 ROM 已删；4 个路径已迁移 |
| `Sony - PlayStation Portable.lpl` | 2 | PSP 去重时删掉的 TF 卡 ISO |
| `Sega - Game Gear.lpl` | 1 | 已移除的坏 ROM `GG雅士达3.gg` |

10 条「同名文件在别的目录」也删而非改写路径：不同核心/romset 不能乱合并，且原路径已不存在、RA 内点了必然失败，天马主库另有正确条目。

### 16.3 执行 SOP

```sh
am force-stop com.retroarch.aarch64     # 若用户正在玩则不要停，改为退出后复核
cp <5 个 .lpl> /sdcard/backup/playlist-clean-20261114/
# 本机过滤 items，保留顶层键与键顺序，json.dumps(ensure_ascii=False, indent=2)
rm -f <目标 .lpl> && adb push <已删条目的 LPL> <目标>     # ⛔ 先删再推，避免短文件尾部残片
adb pull <目标> /tmp/check && md5 比对
# 再全库复算：21 个 playlist / 2,454 条 / DEAD=0
```

结果：2,498→**2,454**、空 playlist（GW、PSP）保留文件不删、天马 3,736 条与启动失败 0 不变。备份：设备 `/sdcard/backup/playlist-clean-20261114/`、本机 `work/playlist-clean-20261114/{before,after}/`。回滚直接把 5 份 `before` cp 回去。

### 16.4 清理后仍需复核

RA 运行时若用户手动「Save Current Config / 重新扫描目录」可能重写 playlist；下次退出 RA 后再 pull 一次 md5 比对即可。天马侧无需清 `dataCache.json`。

---

## 17. CPS3 六键格斗按键：核心选项 `controls_p1 = arcade`（v2.2.4）

### 17.1 症状与排查顺序

用户报「CPS3 也有部分按键不正确」。**先别按 §15 的核心级 cfg 思路动手** —— CPS3 的根因在另一层：

1. `cat "/sdcard/RetroArch/config/FB Alpha 2012 CPS-3/FB Alpha 2012 CPS-3.cfg"` → 只有 `aspect_ratio_index` / `video_scale_integer` / `input_overlay*` 共 6 行，**没有按键行**；两份主 `retroarch.cfg` 的 P1 绑定完全一致且是全局标准。
2. `find /sdcard/RetroArch/config -iname "jojo*.cfg" -o -iname "sfiii*.cfg" -o -iname "redearth*.cfg"` → 0 个 per-game cfg；remaps 下也无 CPS3。→ 继承链干净。
3. 看**核心选项文件** `config/FB Alpha 2012 CPS-3/FB Alpha 2012 CPS-3.opt`，发现 `controls_p1 = "gamepad"`（默认值）。
4. 拉 RA APK → `assets/cores/fbalpha2012_cps3_libretro_android.so` + `assets/info/*.info` 可 `strings` 取证；映射表以仓库 `libretro/fbalpha2012_cps3` 的 `svn-current/trunk/src/burner/libretro/libretro.cpp` **1387–1469 行**为准（`bStreetFighterLayout` 与 `nFireButtons<=4` 两个分支）。

### 17.2 6 键映射对照（P1，`lr_controls_p1 = normal`）

| 街机动作 | `gamepad`（原值，错感来源） | `arcade`（定稿） | Android keycode |
|---|---|---|---|
| fire1 轻拳 | `JOYPAD_Y` (100) | **`JOYPAD_A` (96)** | 96 |
| fire2 中拳 | `JOYPAD_X` (99) | **`JOYPAD_B` (97)** | 97 |
| fire3 重拳 | `JOYPAD_L` (102) | **`JOYPAD_X` (99)** | 99 |
| fire4 轻脚 | `JOYPAD_B` (97) | **`JOYPAD_Y` (100)** | 100 |
| fire5 中脚 | `JOYPAD_A` (96) | **`JOYPAD_L` (102)** | 102 |
| fire6 重脚 | `JOYPAD_R` (103) | **`JOYPAD_R` (103)** | 103 |

`gamepad` 把机身 A/B 落到「脚」上，用户以为是拳 → 表现为「部分按键不正确」（不是全错、也不是没反应）。`arcade` 是标准街机三拳三脚，且与 CPS1/CPS2 横版的 A/B/X/Y/L/R 语义一致。4 键游戏（jojo / redearth）在 `arcade` 下是 `A/B/X/Y`。

⛔ `remap to R1/R2` 会把键挪到 `R2/L2`（105/104），本机全局这两行是 `nul`；`getevent -pl` 虽有 `BTN_TL2/BTN_TR2`，RA 未绑定就是没反应。**保持 `normal`**。

### 17.3 执行 SOP（2026-11-14 22:45 实测）

```sh
ADB=$PWD/tools/platform-tools/adb
D="/sdcard/RetroArch/config/FB Alpha 2012 CPS-3/FB Alpha 2012 CPS-3.opt"
$ADB shell 'ps -A | grep -i retroarch'        # 必须为空，否则退出时会写回
$ADB shell "mkdir -p /sdcard/backup/cps3-keyfix-20261114 && cp '$D' /sdcard/backup/cps3-keyfix-20261114/"
$ADB pull "$D" work/cps3-keyfix-20261114/before/CPS-3.opt
# 只改两行：controls_p1 / controls_p2 : "gamepad" → "arcade"
$ADB shell "rm '$D'" && $ADB push work/cps3-keyfix-20261114/after/CPS-3.opt "$D"
$ADB pull "$D" /tmp/chk && md5 比对                      # 必须一致
# 冷启动验证（不依赖实体按键）
$ADB shell 'am start --user 0 -n com.retroarch.aarch64/com.retroarch.browser.retroactivity.RetroActivityFuture \
  -e ROM "/storage/6AF3-384F/Roms/CPS3/sfiii3.zip" \
  -e LIBRETRO /data/data/com.retroarch.aarch64/cores/fbalpha2012_cps3_libretro_android.so \
  -e CONFIGFILE /storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg'
# screencap 确认进游戏（本机是 Euro 区域 WARNING 画面、60fps）
$ADB shell 'am force-stop com.retroarch.aarch64; am kill com.retroarch.aarch64'
# 复核：ps 为空 / mCurrentFocus 回 pegasus / .opt md5 仍一致
```

产物：`assets/ra-cps3/CPS-3.opt`（定稿）、`shots/cps3-arcade-verify.png`、本机 `work/cps3-keyfix-20261114/{before,after,verify}/`。

### 17.4 边界

`am start` 冷启动只能证明「`arcade` 是合法值 + 核心加载 + 游戏能进 + 配置未被写回」。**实体按键布局是否合手，必须用户从天马进 `sfiii3` 用实体键实测**（禁令 12：RA 不接收 adb 注入按键）。若用户觉得拳脚顺序仍需调整，下一步是核心选项切回 `gamepad` 或用 RA Quick Menu → Controls 做 per-game remap，⛔ 不要改全局 cfg。

## 18. 13 项清单批量修复（2026-11-15，v2.2.5）

用户一次给出 13 条体验问题，按「只读盘点 → 分组修复 → 单点验证 → 批量推广 → 全库复核」执行。工作目录 `work/fix13-20261114/`，下分 `device-meta/`（35+1 份设备 metadata）、`probes/`、`diag/`、`verify/`、`final/`、`cfg-before/`、`VB-backup/`、`covers/`、`covers-new/`、`new-meta/`、`fix-out/`。

### 18.1 只读盘点与探针（不改动设备）

```bash
probe() {  # probe.sh：冷启动只读截图
  name="$1"; rom="$2"; core="$3"; wait="$4"
  $ADB shell 'am force-stop com.retroarch.aarch64' >/dev/null 2>&1
  $ADB shell 'logcat -c' >/dev/null 2>&1
  $ADB shell "am start --user 0 -n com.retroarch.aarch64/com.retroarch.browser.retroactivity.RetroActivityFuture -e ROM \"$rom\" -e LIBRETRO /data/data/com.retroarch.aarch64/cores/$core -e CONFIGFILE $CFG"
  sleep "$wait"; $ADB shell screencap -p /sdcard/f.png; $ADB pull /sdcard/f.png "$W/probes/$name.png"
}
```
`diag.sh` 抓完整 `logcat -d -t 2500` 过滤噪音，专用于定位崩溃（本轮靠它拿到 `F DEBUG / signal 11 / core_load_game+156`）。拼图脚本把 5～8 张截图缩到 480×320 排成 contact sheet，一次目检多平台，效率远高于逐张看。

### 18.2 前端 / 遮罩（第 1/4/10 项）

| 平台 | 病因 | 修法 |
|---|---|---|
| MSX | `config/blueMSX/` 只有 `.opt`，**没有核心级 / per-game cfg** | `overlay_fix.py` 生成 `MSX_B.cfg` + `MSX_B_frame.png`，写 `blueMSX.cfg` 与样例 `勇者斗恶龙一代.cfg` 的 `input_overlay`；实机见红细线与竖排 `MSX` |
| PICO | 核心级 `Retro8.cfg` / `PICO-8.cfg`、两处 per-game cfg **全不生效** | 新建 `retroarch_pico.cfg` 强制四项 overlay 开关，改 PICO metadata `launch` 的 `-e CONFIGFILE` 指向它；实机见 `PICO-8` 竖排标记 |
| VARCADE | 蓝底旋转 `DIP SWITCH SETTING` 是游戏自检画面，非 OSD | `MAME 2003-Plus.cfg` 加 `savestate_auto_save=false` / `rewind_enable=false` / `video_font_enable=false`；22s 截图已到 TAITO 片头 |

⚠️ PICO-8 卡带是 128×128 正方形，「有的游戏可能是竖版」不成立，⛔ 不要补 `video_rotation`。

### 18.3 热门 10 款置顶（第 3 项）

Pegasus 的 `sort-by` 是「排序用替代标题」。集合级原本统一 `sort-by: 10`；`hot10.py` 给每平台选 10 款，在 `game:` 行后写 `sort-by: 01 <标题>` … `10 <标题>`：

```python
idx={t:i+1 for i,t in enumerate(chosen)}
for l in open(p,encoding='utf-8',errors='surrogateescape'):
    out.append(l)
    if l.startswith('game:'):
        t=l[5:].strip()
        if t in idx: out.append('sort-by: %02d %s\n'%(idx[t],t))
```
`EXPLICIT` 给小平台/中文平台精确名单，`SCORE` 给大平台打分，`PENALTY` 降权 hack/改版/汉化/β。产出 35 份 metadata、**334 条** game-level `sort-by`（部分平台不足 10 款），覆盖全部 35 平台。⛔ metadata 只 patch 不整覆盖；改完必须 `am force-stop org.pegasus_frontend.android` → `rm /sdcard/pegasus-frontend/dataCache.json` → 重启天马。

### 18.4 DOS 直启 + 崩溃救援（第 2 项，本轮最大突破）

**免选 exe**：`dosbox_pure_conf = "outside"` + `Roms/DOS/<游戏名>.conf`：

```ini
[autoexec]
@echo off
C:
CD \
PLAY.BAT
```
先用《毁灭战士2》单点验证（9s 直接出 id Software 标题画面）再批量推 15 份。只读解出包内 `PLAY.BAT` 用 ZIP central-directory 尾部解析 + raw deflate，不必把 488MB 全 pull 到本机：

```python
sz,t = tail_of(p)                     # adb exec-out tail -c 393216
i = t.rfind(b'PK\x05\x06')            # EOCD → cd_off / entry count
# 逐条 PK\x01\x02 取 (local_off, csize, usize, method, name)
# dd if=<dosz> bs=1 skip=local_off count=csize+80 → zlib.decompress(dat,-15)
```

**《大唐英雄传》救援**（用户写「隋唐英雄传」）：① `SIGSEGV` 在 `core_load_game`，用「只打包前 N 条」二分 10 轮定位 `GAME.IMG`（0x4B000 == 崩溃 `x19`），核心误判为软盘镜像后末尾越界读；② 尾部补 1 个 `\0` 重建完整包，`crash_lines=0`；③ 定制 conf：`IMGMOUNT D CDROM.ISO -t iso` → `midi sb220` → `nlb`，12s 出标题画面。原件备份 `/sdcard/backup/fix13-dos-auto/`。

### 18.5 其他修复与产物

- **MD《光明力量 1/2》**：`.md` 实为 ZIP（`PK\x03\x04`），解出内层真 ROM 替换；两作实机均进游戏。
- **封面（第 8/11/13 项）**：按 `size == (500,315)` 识别 213 张 GBA 占位横条 → 480×640 竖版卡；《兵蜂》《动物之森》换 libretro-thumbnails 真盒绘（走 `cdn.jsdelivr.net/gh/...`）。
- **删除 VB（第 6 项）**：设备 `Roms/VB` 已删，本机 `VB-backup/` 57 文件 44M；⚠️ 设备侧备份失败，**回滚只有本机这一份**。
- **按键（第 5/7/11 项）**：`Flycast/动物篮子.cfg` 补竖版映射；PPSSPP `controls.ini` 让 D-pad 同时驱动 `An.Up/Down/Left/Right` 并按 `Y=方块(99) / X=三角(100) / A=圆圈(97) / B=叉(96)` 补 `10-/0-/1-` 多设备；`SwanStation/胜利十一人2002.rmp` 单游戏 remap；`Mupen64Plus-Next.cfg` 加 `input_player1_analog_dpad_mode = "1"`。⚠️ 全部**待实体键实测**。
- ⚠️ `apply.sh` 曾把 PPSSPP 私有目录误写成 RA 的 `$SYS`，导致 `cp: bad ... No such file`；正确路径 `/storage/emulated/0/Android/data/org.ppsspp.ppsspp/files/PSP/SYSTEM/controls.ini`，改 `adb push` 直接覆盖（不删再推），回读 md5 一致。

### 18.6 未解决：土星《钟表骑士》（第 9 项）

四个土星核心全黑屏 → 不是核心；四个 CHD 头部同为合法 v5 → 不是格式；Beetle Saturn 关卡+锁日区能进 BIOS 的 CD 播放器（`TRACK 00`）→ **镜像无有效 Saturn 引导区**。《钟表骑士 2》同病。需用户提供可用 CHD 替换，或删除这两条前端条目。⛔ 实验用的 `beetle_saturn_cart=None` / `yabasanshiro_force_hle_bios=enabled` 已 `cp` 回备份并回归验证《守护英雄》正常。

### 18.7 全库复核基线（2026-11-15）

```
35 平台 / 3708 条 game；file 引用 3708（缺失 0）；assets.box_front 3708（缺失 0）
334 条热门 sort-by，覆盖 35/35 平台；VB 集合已消失；设备文件总数 25481
dataCache.json 于清缓存重启后重新生成（5.6MB）
```
复核脚本口径：`adb exec-out find <Roms> -type f` 建路径集合，metadata 用 `encoding='utf-8', errors='surrogateescape'` 读，`file:` 取 `#` 之前部分再与集合比对（同禁令 43 的字节还原口径）。

## 19. 二次反馈 5 项（2026-11-15，v2.2.6）

用户回报：① PS 月下夜想曲无法启动 ② GBA 封面还是不对 ③ N64 方向键还是不行 ④《钟表骑士》删除 ⑤ VARCADE 弹窗「没有了」。

**① PS 月下 = 非故障（禁令 52）**：时间线 8/14/35/60/75/90/110s 截图 + `lastrun.log` 的 launch→resume 54s 证明用户没等到片头结束。只在 PS metadata 该游戏 `description` 追加「约 60 秒黑底片头、随后进音乐欣赏模式，选退出开始游戏」。原名《隋唐英雄传》在 DOS 轮已确认实际文件是《大唐英雄传》，本轮无同名 PS 游戏。

**② GBA 封面 = 2.2.5 误删真封面（禁令 48，本轮最大更正）**：
- 从设备 `/sdcard/backup/fix13-20261115/gba-covers-before/`（426 张）与本机 `work/fix13-20261114/covers/GBA/` 抽图复核：`500×315` 中 54 张是真实日版盒绘、159 张才是单色渐变文字卡。
- 判据 `buckets = len({(r//48,g//48,b//48)})`（100×63 缩图）：`<20` 占位卡、`>=40` 真盒绘。
- 用 `api.github.com/repos/libretro-thumbnails/Nintendo_-_Game_Boy_Advance/git/trees/master?recursive=1` 一次取 5961 个 `Named_Boxarts` 文件名；中文名→精确英/日文标题词典 + 人工校对，得到 **178/213** 个可用盒绘；jsDelivr 并发下载 141 个文件（`verify()` 剔掉 1 个假图）。
- 生成优先级：**54 张原备份真盒绘（原样内容）→ 137 张 libretro 真盒绘 → 22 张精修标题卡**，全部统一 480×640（顶部 GBA 条 / 中部盒绘保持比例 / 底部中文名 / 中文改版角标）。`adb push <dir>/. <Roms/GBA/Imgs/>` 一把推 213 张，md5 抽样一致；清缓存后货架实拍全是真盒绘。

**③ N64 = 绑定层错向（禁令 51）**：核心级 cfg 的 `analog_dpad_mode` 改 `0`，新增 4 行把 `h0*` 绑到 `l_x/l_y_*_btn`。备份 `/sdcard/backup/fix13-n64-20261115/` 与本机 `round2/n64/before.cfg`；《冲浪大赛》冷启动 0 崩溃、cfg 未写回。⚠️ 实体键仍需用户实测。

**④ 土星删除（禁令 53/54）**：删两作 CHD（442MB）+ 2 张封面 + metadata 2 个 game 块 + `content_history.lpl` 4 条历史；本机 `round2/saturn_backup/rom/` 留两个 CHD，设备 `/sdcard/backup/fix13-saturn-delete/` 留小文件。SATURN 集合剩 2 条（《守护英雄》《空牙 2001》），回归验证《守护英雄》仍正常。

**⑤ VARCADE**：用户确认弹窗消失，2.2.5 的 `video_font_enable=false` / 关存档与 rewind 闭环，不再改动。

**最终基线**：35 平台 / **3706** 条；`file:` 3706、`assets.box_front:` 3706、缺失均为 0；热门 `sort-by` 332 条；GBA `Imgs/` 426 张（213 张本轮新卡 + 213 张原真封面）；`dataCache.json` 已清并重建。

**待用户实测**：N64 方向键、CPS1/CPS3/ATOMISWAVE/PPSSPP/PS 系列实体键（禁令 12）；VARCADE 之外若还有其它启动弹窗需拍图。

## 20. 一键安装通道与蓝标图示（2026-11-15，v2.3.0）

### 20.1 通用安装 SOP

```bash
bash scripts/kpa_oneclick.sh --dry-run   # ① 只读体检 + 计划（设备离线也能预览）
bash scripts/kpa_oneclick.sh             # ② 备份 → 7 步 → 清缓存 → 静态校验 → 报告
# ③ 打开 ~/WorkBuddy/kpa-oneclick/<时间戳>/report.md，逐条过「必须人手实机确认」
```

阶段顺序不可换：**体检（adb / 设备 / TF 卡 / 资源完整性 / 磁盘）→ 配置级备份（本机 + 设备双份）→ `step1~step7` → `force-stop` 天马 + 删 `dataCache.json` + 重启 → `kpa_health_check.sh` → `report.md`**。
任一步失败即中止，修复后原样重跑（幂等）。`--verify-only` 只出报告、`--steps 3,4` 只跑指定步骤。

### 20.2 明确不进一键脚本的 8 项（禁令 56）

| 特例 | 为什么是特例 | 位置 |
|---|---|---|
| 热门 10 款 `sort-by` 置顶 | 依那台机器的游戏清单 | §18 |
| DOS 15 份同名 `.conf` | 依各 `.dosz` 内 `PLAY.BAT` | §18 |
| `大唐英雄传.dosz` 补字节 | 单个坏包的 `GAME.IMG` 越界读 | §18 |
| GBA 213 张真盒绘回填 | 依那台机器的中文名与备份原图 | §19 |
| 《光明力量》ZIP 伪装解包 | 两个具体 ROM 文件 | §18 |
| 土星坏 CHD 删除 | 用户明确要求删那两个镜像 | §19 |
| CPS1/CPS3 键位、N64 摇杆绑定 | 依该机实体键与核心版本 | §15/§17/§19 |

### 20.3 蓝标图示

`python3 scripts/blueprint_icons.py` 生成，`--check` 校验。色板与规范见 `HARD_RULES` 57。
4 张图示分别用于：`01-oneclick-flow`（安装流程）、`02-config-layers`（改动落点）、`03-verify-boundary`（自动 vs 人手）、`04-troubleshoot`（排障分流），均在 `INSTALL.md` 中引用。

### 20.4 发布

先 `--dry-run` 预检 → ① 用 `/api/v1/skills/<slug>/comments/images` 把 6 张图传 COS 拿绝对 URL → ② 发布目录**排除所有 `.png`**（否则 400 `不允许的文件类型`）→ ③ 手工构造 multipart 调 `POST /api/v1/community/skills/publish`，payload 里带 `iconUrl`（CLI 未实现该字段）→ ④ 回查 `skill.iconUrl` / `latestVersion.version` / `changelog`。详见 `HARD_RULES` 57。

---

## 21. RetroArch 存档位置与迁移（2026-11-18 实机，✅ 已验证）

### 21.1 为什么要把存档搬出内部存储

内部存储只有 21G（系统 + APP 占 15G），而 RA 的即时存档按核心内存大小预分配，108 个存档就吃掉 **681M**，`.srm` 再 19M。TF 卡通常还有 30G 空闲，这是性价比最高的一次腾挪。

### 21.2 唯一正确落点

```
savestate_directory = "/storage/6AF3-384F/Android/data/com.retroarch.aarch64/files/states"
savefile_directory  = "/storage/6AF3-384F/Android/data/com.retroarch.aarch64/files/saves"
```

⛔ **不能**放 `/storage/6AF3-384F/RetroArch/`（TF 卡根目录）——RA 没有 `MANAGE_EXTERNAL_STORAGE`，读 TF 卡靠 SAF 单独授权 `Roms`，写根目录会失败。只能放 TF 卡上的**应用私有目录** `Android/data/com.retroarch.aarch64/files/`，那里它无条件可读写，也不需要软链接（Android 上软链接反而容易出问题）。

### 21.3 先认准哪份配置是活的

设备上存在两份同名配置，最容易改错：

| 路径 | 属主 / 时间 | 是否生效 |
|---|---|---|
| `/storage/emulated/0/RetroArch/retroarch.cfg` | `u0_a92`（应用自己），每次退出回写 | ✅ **生效** |
| `Android/data/com.retroarch.aarch64/files/retroarch.cfg` | `shell`，日期停在旧版本 | ❌ 遗留副本 |

判据：哪份文件里的存档路径与**实际落盘位置**一致，哪份就是活的。改完还要核查核心级 `config/<核心>/<游戏>.cfg` 没有写 `savestate_directory`（会抢走全局路径；本机 467 个 cfg 实测全无覆盖）。

### 21.4 迁移步骤（照做，顺序不能变）

```bash
T=/storage/6AF3-384F/Android/data/com.retroarch.aarch64/files
S=/storage/emulated/0/RetroArch
# 1. TF 卡上已有的旧存档先改名，保证可回滚
$ADB shell "cd $T && [ -d states ] && mv states states.bak_$(date +%Y%m%d)"
# 2. 复制（不要 mv，内部那份留作保险）
$ADB shell "cp -r $S/states $T/ && cp -r $S/saves $T/"
# 3. 逐名比对，内部有而 TF 缺的必须为 0
$ADB shell "cd $S/states && find . -type f" | sort > /tmp/in.txt
$ADB shell "cd $T/states && find . -type f" | sort > /tmp/tf.txt
comm -23 /tmp/in.txt /tmp/tf.txt          # 输出为空才继续
# 4. 改配置（先备份）
$ADB shell "cp $S/retroarch.cfg $S/retroarch.cfg.bak_$(date +%Y%m%d)"
$ADB shell "sed -i 's#^savefile_directory = .*#savefile_directory = \"$T/saves\"#; \
                     s#^savestate_directory = .*#savestate_directory = \"$T/states\"#' $S/retroarch.cfg"
```

### 21.5 怎么验证（日志不可用）

该版本 `log_to_file = "true"` **不产生任何日志文件**，`RetroArch/logs/` 一直是空的，别在这上面浪费时间。只能看文件：

1. **写**：进任意有旧存档的游戏，玩一下退出。比对两处 `states`：
   `内部文件数不变、mtime 仍旧` + `TF 卡文件数 +1 或 mtime 变新` → 写通路通。
2. **读**：游戏内「存档 → 读取存档状态」，列表能列出 TF 卡上那份 `.state` → 读通路通。两项都过才算成功。
3. 通过后再 `rm -rf $S/states $S/saves`，内部存储立省约 700M。

### 21.6 存档机制（本机实际配置）

| 类型 | 写入时机 | 自动？ |
|---|---|---|
| `.state.auto` | 退出游戏 / 退出 RA 时（`savestate_auto_save=true`） | ✅ 自动写，但固定文件名，**每次覆盖** |
| `.state` | 菜单「保存存档状态」 | ❌ 手动 |
| `.srm` / `.sav` | 游戏内存档 + `autosave_interval=10` 每 10 秒落盘 | ✅ 自动 |

`savestate_auto_load=false`：进游戏**不会**自动接上次，必须手动「读取存档状态」。想开机即续可改 `true`，但音游/格斗这类想从头玩的会被打断。

### 21.7 三条后续注意

1. 存档现在跟着 TF 卡走：**换卡或格式化 = 全丢**，建议定期把 `files/states`、`files/saves` 拷到电脑。
2. RA 更新版本或「恢复默认设置」会把路径重置回内部存储，表现为「存档又回到内部了」，升级后复查一次。
3. 存档写入瞬间断电会损坏那一次存档；`.srm` 每 10 秒自动写，风险窗口不大但别在存盘时拔卡。
