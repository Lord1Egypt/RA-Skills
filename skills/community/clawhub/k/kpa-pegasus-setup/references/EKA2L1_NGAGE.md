# EKA2L1 + N-Gage 1.0/2.0 + 天马 NGAGE 入口（KPA 实机 2026-11-16 验证）

本文沉淀 KPA 掌机上用**官方 EKA2L1 v0.1.0**（`com.github.eka2l1`）运行 N-Gage 1.0（QD / RH-29）与 2.0（5800 / RM-356）游戏、并在天马建立独立入口与官方封面的完整成功流程。全部路径、UID、命令均来自实机验证。⛔ 只用官方包，不用汉化/fork。

## 0. 核心设备/环境事实

| 项 | 值 |
|---|---|
| adb | 本机 `platform-tools/adb`（路径随机器而定，必要时设 `KPA_ADB`）；设备序列号以 `adb devices` 实测为准 |
| EKA2L1 数据根 | `/storage/emulated/0/Android/data/com.github.eka2l1/files/` |
| config | `<根>/config.yml` —— **设备只由这里决定** |
| TF 卡 | `/storage/6AF3-384F`；NGAGE 入口在 `Roms/ngage/` |
| 天马缓存 | `/sdcard/pegasus-frontend/dataCache.json` |
| 设备索引（会变，必须现查） | `RH-29`(QD)=1.0，`RM-356`(5800)=2.0，`RM-409`(5320) |

**三设备 devices.yml 关键字段**（`<根>/data/devices.yml`，isolated-drives 必须按此）：

```yaml
RH-29:  { platver: epoc6,     manufacturer: (c)NMP, firmcode: RH-29, model: N-Gage QD,          machine-uid: 270512817, isolated-drives: false }
RM-356: { platver: epoc94,    manufacturer: Nokia, firmcode: RM-356, model: 5800 XpressMusic,   machine-uid: 536926806, isolated-drives: true  }
RM-409: { platver: epoc93fp2, manufacturer: (c)Nokia, firmcode: RM-409, model: N-Gage 5320,     machine-uid: 536926810, isolated-drives: false }
```

## 1. 致命易错点（先看，能省几小时）

1. **🔴 `config.yml` 的 `device:` 是唯一设备开关，intent 的 `--es appDeviceCode` 完全无效。** 实测：设 `device:1` 时，即使 intent 带 `appDeviceCode RH-29`，FIFA 仍黑屏；日志 `Device being used:` 显示实际设备。设 `device:0` 后 **1.0 和 2.0 都能跑**（2.0 游戏数据是共享盘，QD 设备下也能加载 Games 平台）。**结论：`device: 0` 固定即可，两套通用，无需动态切换。**
2. **🔴 N-Gage 2.0 游戏无法手工预装。** 官方 EKA2L1 0.1.0 的 SIS 安装器有 **adler32 bug**，装 Nokia 打包的 SISX 报 `Inflate data error`；手工写 `sisregistry`/DBMS/注册 rsc 全部实测失败。能玩的 18 个 2.0 游戏来自**整体恢复已装好的完整数据盘**（`~/Downloads/EKA2L1模拟器/eka_data.tar`，961M），就地 `tar xf` 覆盖（不含今天的 1.0 共享盘与 RH-29 ROM，故不冲突）。要加新的 2.0 游戏 = 需拿到含它的完整环境包整体恢复，没有捷径。
3. **🔴 FUSE 目录直推会静默损坏/漏文件**（EKA2L1 私有目录）。正确法：本机 `COPYFILE_DISABLE=1 tar -cf` → `adb push` 到 `/sdcard/Download/` → `adb shell "tar -xf ... -C $D --no-same-owner"`。**必须加 `--no-same-owner`**，否则 FUSE 对 `settime` 报 `Operation not permitted` 中断解包。TF 卡（`/storage/6AF3-384F`）下 push 图片/文本 md5 正常。
4. **macOS `._*` AppleDouble** 会让 applist SIGSEGV —— 打包前 `COPYFILE_DISABLE=1`，解包后 `find $F -name '._*' -delete`。
5. **`dataCache.json` 别清空重扫**（会导致「没有找到游戏」）。正确法：`adb pull` → Python 深拷贝已有有效条目改造 → `adb push` 回临时文件 → `cp` 覆盖（force-stop 天马后操作）。改 metadata 后**不要删缓存**，直接编辑 JSON 的 NGAGE 部分。
6. **首次用 intent 启动某 UID 会先显示 per-game「游戏设置」页**，必须点右上角「开始」才进游戏。坐标按**原图 960×640** 算（开始按钮约 `x=870 y=58`）；用缩放后的坐标会点不中。

## 2. 设备索引 / control API（现查，别硬编码）

```bash
$ADB shell "am force-stop com.github.eka2l1"; sleep 2
$ADB shell "am start --user 0 -n com.github.eka2l1/.MainActivity --ei debug_control_port 9000" >/dev/null 2>&1
sleep 10; $ADB forward tcp:9000 tcp:9000
curl -s http://127.0.0.1:9000/v1/devices            # 查索引
curl -s -X POST http://127.0.0.1:9000/v1/devices/0/boot
curl -s 'http://127.0.0.1:9000/v1/apps?system=1'    # 应用列表（验证新游戏被识别）
curl -s -X POST 'http://127.0.0.1:9000/v1/apps/0x101FD3F7/launch'
```

## 3. 安装 N-Gage 1.0 游戏（QD / RH-29，✅ 稳定可复用）

游戏包是 QD 原生 app：`system/apps/<appdir>/`（.app/.aif/.rsc/.mbm），可能带 `system/Libs` 和 `xxx_1` 资源目录。

```bash
W=/tmp/ng1_work; mkdir -p $W/game
# zip / rar 解压（中文条目名用 bsdtar，不用设备端 unzip）
COPYFILE_DISABLE=1 unzip -q -o "xxx.zip" -d $W/game
bsdtar -xf "xxx.rar" -C $W/game
# UID 从 .app / .aif 头部偏移 8 读 u32：
#   python: struct.unpack_from('<I', open(app,'rb').read(), 8)[0]
cd $W/game && COPYFILE_DISABLE=1 tar -cf /tmp/g_e.tar system
$ADB push /tmp/g_e.tar /sdcard/Download/g_e.tar
$ADB shell "tar -xf /sdcard/Download/g_e.tar -C $D --no-same-owner"
$ADB shell "find $D -name '._*' -type f -delete"
```

- 目标盘：`$D=/storage/emulated/0/Android/data/com.github.eka2l1/files/data/drives/e`（**E 盘 = 模拟 MMC**）。
- 放进去后**重启 EKA2L1，applist 自动识别**，无需写 reg/rsc。
- 已验证游戏：
  - FIFA 2004 `6RAV` UID `0x101FD3D2=270521298`
  - 贪食蛇 Snakes `6r45`(+`6r45_1`) UID `0x101FD3F7=270521335`
  - 文明 Civilization `6R69`(+`system/Libs`) UID `0x101FD42A=270521386`

## 4. N-Gage 2.0 环境与游戏（5800 / RM-356）

- 数据盘在 `drives/rm-356/c/Private/<UID>/Arena/`，每个游戏有 `ngi_splash_land.jpg`（可作封面来源）。
- 平台 Games UID `0x20007B39=536902457`。2.0 游戏**不在 applist**，须在 Games 平台内点游戏启动。
- **intent 直进具体 2.0 游戏 UID 会 native crash —— 硬限制，别再试**。天马 2.0 入口统一进 Games 平台，在描述里写清选哪个游戏。
- 已装 18 个 UID / 官方封面编号映射见本机 `/tmp/ngage_games.json`（临时，长期以 metadata 为准）。

## 5. 天马 NGAGE 入口 + 官方封面（✅ 可复用）

**封面来源**：`~/Downloads/N-Gage游戏1.0/N-GAGE/media/<目录>/boxFront.jpg`；1.0 游戏在 `NNN.[中文名].英文/`，2.0 在 `[NG2.0].NN.名/`。

1. 封面放 `<TF>/Roms/ngage/Imgs/<名>.jpg`（文件名与 metadata 引用一致）。
2. 每个入口一个 `.nga` 占位文件（空文件即可），metadata 里 `extensions: nga` 才会扫。
3. `metadata.pegasus.txt` 条目格式：

```
game: 1.0 Snakes 贪食蛇 (QD)
sort-by: 00b Snakes
file: Snakes.nga
assets.box_front: Imgs/Snakes.jpg
launch: am start --user 0 -a emu.launch -n com.github.eka2l1/.emu.EmulatorActivity --el appUid 270521335 --es appName "Snakes" --es appDeviceCode RH-29
description: N-Gage 1.0 / QD。首次进入点右上角开始。
```

4. **intent 模板**：`am start --user 0 -a emu.launch -n com.github.eka2l1/.emu.EmulatorActivity --el appUid <十进制UID> --es appName "<名>" --es appDeviceCode <RH-29|RM-356>`（appDeviceCode 仅为兼容保留，真正生效靠 config device）。
5. 写回 metadata 用 base64 法避免 FUSE 问题：`B64=$(base64 < f | tr -d '\n'); $ADB shell "echo '$B64' | base64 -d > $D/metadata.pegasus.txt"`。
6. 更新 `dataCache.json`：Python 深拷贝 FIFA 条目 → 改 title/sort_by/launch_cmd/description/assets.boxFront/uuid → append 到 `games[]` 和 `path_to_gamefiles[]`（`path` 指向 `.nga`），force-stop 天马后 push 覆盖。
7. ⚠️ FUSE 下 `ls | wc -l` 枚举会少算（如显示 20 实际 21），用逐个 `[ -s file ]` 校验封面覆盖。
8. 验证：重启天马 → 左侧 NGAGE 显示入口数 → 右上角 `n/总数` → 封面非灰图 → 从天马点击端到端进游戏。

## 6. 显示满高 / 无白边

per-game config `<根>/android/configs/<UID大写8位>/config.json`。**ScaleType 语义来自官方 arrays.xml**：`0=As is`、`1=Fit`、`2=Fill`。用 `2`（Fill）铺满；配 `ScreenGravity`、`ScreenBackgroundColor`。实测 2.0 游戏满高无底部白边（左右窄黑边是 4:3 内容在 3:2 屏的正常现象）。

## 7. 无法完成 / 别浪费时间

- ❌ intent 直进具体 2.0 游戏 UID（native crash/tombstone）。
- ❌ 手工预装新 2.0 游戏（adler32 bug + 注册链缺失）。
- ❌ 破解补丁：都市赛车Ⅲ补丁 UID `0x2000afe3` 对应 Asphalt3.n-gage（本体历史上装不上）；救世主One补丁 UID `0x2000afbf` 本地无匹配本体。两个都无处打。
- ❌ 退出键（select+B 回天马）：EKA2L1 Android 层只认 `KEYCODE_BACK`，`KeyMappings` 仅 Android→Symbian 映射，无法生成系统 BACK 直接回天马（用户实机反馈「只能成为选择列表」）。
