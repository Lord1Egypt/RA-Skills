# 脚本索引（22 个）

`SKILL.md` 只常驻 4 个高频入口，其余在这里查。所有脚本都在 `scripts/` 下，**默认只读或 dry-run**，写设备必须显式 `--apply`（个别安装步骤脚本本身即执行体，见「写设备」列）。

约定：`KPA_ADB` / `KPA_TF` 由 `kpa_env.sh` 统一解析，单独调用脚本时也会自动 source。

## 一、编排与安装

| 脚本 | 做什么 | 写设备 | 常用参数 |
|---|---|---|---|
| `kpa_oneclick.sh` | 全流程编排：前置体检 → 备份 → step1~7 → 清缓存 → 静态校验 → `report.md` | 是（含） | `--dry-run` 只出计划，设备没连也能跑 |
| `run_all.sh` | 只跑 step1~step7，不做体检与报告 | 是（含） | 无 |
| `kpa_env.sh` | 公共环境：定位 adb、检查设备、TF 挂载点。被其余脚本 source | 否 | 无 |
| `step1_apps.sh` | 装 RetroArch / 天马 / PPSSPP 上架版；已装则跳过；APK 从官方渠道下载，直连失败走镜像 | 是 | 无 |
| `step2_theme.sh` | 装 **prosperoOS** 主题（放大封面 + 戴夫背景 + 平台 Logo）并切到该主题 | 是 | 缺 `assets/golden/prosperoOS-kpa.zip` 时只提示并 SKIP |
| `step3_ra.sh` | 部署 RA 主配置 `retroarch.cfg` + 生成竖版 per-rom cfg | 是 | 无 |
| `step4_metadata.sh` | 各平台 metadata 写 `launch` 行 + 按方向库生成 per-game cfg（只 patch） | 是 | 无 |
| `step5_ppsspp.sh` | PSP ROM 拷入应用可读目录 + `ppsspp.ini` + PSP `launch` 行 | 是 | 无 |
| `step6_cleanup.sh` | 清 AppleDouble `._*` / `.DS_Store` / 测试截图 / 应用缓存 | 是 | 失效旧路径只报告不删 |
| `step7_verify.sh` | 借天马拉起核心、重启天马、截图、检查 `lastrun.log` 资源缺失 | 是 | 无 |

## 二、专项修复（按症状找）

| 脚本 | 症状 / 用途 | 写设备 | 常用参数 |
|---|---|---|---|
| `kpa_health_check.sh` | 全库静态校验（ROM / 封面 / launch / 简介 / 竖版 cfg）+ 清理盘点 | 否 | `--local` 用本地 `assets/meta_latest/` 离线校验 |
| `kpa_gamefix.sh` | 五类实机修复：DOS 存档弹窗 / NDS 双屏变形 / Flycast 雪花 / Atomiswave OSD / 2P 串控 1P | 是 | `dos\|nds\|flycast\|aw-osd\|p2\|all`，`--apply` / `--revert` |
| `kpa_vertical.sh` | 竖版 cfg 4 行方向修正为实机正确版 | 是 | `--apply` 才写 |
| `kpa_msx_core.sh` | MSX blueMSX 装不上：搭本地最小核心源让 RA 自己下载进私有目录 | 是 | 无 |
| `kpa_android_apps.sh` | ANDROID 移植游戏不显示：`.app` 占位 + per-game `launch` + 推 metadata | 是 | 无 |
| `kpa_nomedia.sh` | 图库被封面刷屏：4 个 `.nomedia` + MediaStore 重扫 | 是 | 需重启一次生效 |
| `kpa_gamedetails.sh` | 详情页观感：推送增强版 `GameDetails.qml`（字号 / 卡片 / 去截断）+ 清缓存 | 是 | 原版自动留回滚点 |
| `kpa_theme_tweak.py` | 主题增强：平台名字号 24→36 并高亮、平台条常显、退出后回原位 | 是 | `--apply` 才写 |
| `kpa_desc_fill.sh` | 批量回填 `description:`（中文简介库） | 是 | `--json <库>`、`--apply`、自动 `.bak` |
| `bangumi_desc.py` | 空壳简介升级为真简介并回填 publisher/genre | 是 | 需 bgm.tv 可达 |

## 三、工具与自用

| 脚本 | 用途 | 写设备 |
|---|---|---|
| `blueprint_icons.py` | 生成 / 校验蓝标图示（`--check`） | 否 |
| `sync_from_device.sh` | 从已配置好的机器拉回重资产（APK / RA config+overlays / BIOS），个人离线装机用，**不上架** | 否（只读设备） |

## 四、调用纪律

1. 先 `--dry-run` 或只读脚本，再 `--apply`；`kpa_gamefix.sh`、`kpa_vertical.sh`、`kpa_theme_tweak.py` 三者都支持回滚（`--revert` 或自带 `.bak`）。
2. 改 metadata 的脚本都会自动清 `dataCache.json`；**手动改 metadata 后不清缓存等于没改**（禁令 3）。
3. `kpa_health_check.sh` 是唯一「不写设备」的全库校验入口，排查问题一律先跑它。
4. 主题有两套，别混：**prosperoOS** 由 `step2_theme.sh` 一键装；**kpa-shelf** 是自建主题，手工部署，源码在 `assets/themes/kpa-shelf/`，改法与布局见 `PLAYBOOK.md` §11。
