---
name: powpowcity-map-editor
description: Create, edit, simulate and share isometric city maps for the PowPow City / IsoCity browser game (https://powpowcity.powpow.online/). Bundles a zero-dependency Node.js CLI (15 commands) that AI agents use to generate cities from real-world OpenStreetMap data (with Baidu Maps geocoding and GCJ-02/BD-09 coordinate correction for China), place buildings, lay roads, zone districts, terraform terrain, run the real game engine headlessly, capture screenshots, and produce share links that players open in a browser. Use when the user asks to build or edit an isometric city, generate a city map from a real-world place, place buildings, build roads, zone districts, make city screenshots, or create playable share links. Triggers - IsoCity, isocity, PowPow City, powpowcity, isometric city, city map, city builder, 城市地图, 等距城市, 放建筑, 铺路, 划区, 城市截图, 分享链接, OSM 地图.
---

# powpowcity Map Editor

编辑 PowPow City 等距城市建造游戏（线上版 https://powpowcity.powpow.online/，引擎 IsoCity）的地图：创建城市、放置建筑、铺路划区、生成截图与分享链接。当用户要求编辑 IsoCity 地图、生成/建造城市、放置建筑、修路、划区、拆建筑、生成城市截图、制作 IsoCity 分享链接、用 OSM 真实地图生成城市时，使用本技能。

触发词：IsoCity、isocity、城市地图、等距城市、放建筑、铺路、划区、bulldoze、simulate、城市截图、分享链接、OSM 地图、powpowcity、isocity CLI。

## 能力边界（重要）

本技能自带完整 CLI（本目录 `cli/`），**不依赖游戏项目文件**，分两档：

- **档位 1 - 纯编辑（任何装了 Node.js ≥18 的机器可用）**：
  `new / map / info / get / buildings / place / bulldoze / zone / terraform / tax / budget / money / share`
  零依赖（lz-string 已 vendor），无需游戏、无需 node_modules、可离线（OSM 生成除外）。
- **档位 2 - 截图与模拟（需要游戏可访问）**：
  `screenshot / simulate` 需要能访问 IsoCity 游戏页面（线上站或本机 dev server）。
  先安装 Playwright：在本技能目录执行
  `npm install playwright && npx playwright install chromium`

## 入口命令

```bash
node <本技能目录>/cli/isocity.mjs <command> [args]
```

`<本技能目录>` 即本 SKILL.md 所在目录（含 `cli/` 子目录）。
生成的城市默认保存在**当前工作目录**的 `cities/` 下。

## 标准工作流

```bash
CLI="node <本技能目录>/cli/isocity.mjs"   # 示例，按实际路径替换

# 1. 创建城市（四选一）
$CLI new --random --grid 60 --name MyCity --seed 7        # 随机地形（湖/海岸/树）
$CLI new --osm --lat 31.2304 --lon 121.4737 --radius 700  # OSM 按坐标
$CLI new --osm --place "Peking University" --ak $BAIDU_MAP_AK   # OSM 按地名（百度地理编码，国内推荐）
$CLI new --osm --lat 39.9962 --lon 116.3174 --coord-sys bd09    # 百度坐标直接用，自动纠偏

# 2. 查看
$CLI map cities/mycity.isocity.json       # ASCII 全图（行=y、列=x，左上角为 0,0）
$CLI info cities/mycity.isocity.json      # 汇总（钱/人口/建筑）
$CLI get cities/mycity.isocity.json 30 20 # 单格详情

# 3. 编辑（选择器: --at x,y | --tiles x,y;x,y | --rect x1,y1,x2,y2 | --line x1,y1,x2,y2）
$CLI place cities/mycity.isocity.json road --line 30,10 30,50
$CLI place cities/mycity.isocity.json power_plant --at 50,50
$CLI zone cities/mycity.isocity.json residential --rect 32,12 40,28
$CLI bulldoze cities/mycity.isocity.json --at 35,20
$CLI terraform cities/mycity.isocity.json land --at 5,5   # 水变陆地

# 4. 交付
$CLI share cities/mycity.isocity.json --short   # 短链（推荐）：上传快照，打印 /city/<code> 短链
# 短链 ≤50 字符，聊天工具不截断、LLM 转述不损坏；玩家打开即玩原版快照
$CLI share cities/mycity.isocity.json --short --gallery   # 短链 + 公开到首页"热门地图"画廊
$CLI share cities/mycity.isocity.json           # 长链（离线兜底）：/c/<城市名>#s=<数据>
# 长链：城市名在路径里，微信聊天分享会解析成卡片（标题=城市名）；数据全在
# #s= 片段，服务器零存储——但长链很长（数千字符），可能被聊天工具截断
# 或把 .isocity.json 文件给玩家（游戏内 Settings > Import from File 导入）

# 5. 截图 / 模拟（档位 2，需先装 Playwright 并有游戏可访问）
$CLI screenshot cities/mycity.isocity.json -o preview.png
$CLI simulate cities/mycity.isocity.json --ticks 600
```

## 规则要点（避免无效操作）

- 水上不能建造 → 先 `terraform land`（$50,000/格，昂贵，规划时避开水域）
- road/rail 只能放 grass/tree/road/rail 上；其他建筑不能压 road/bridge/rail
- 多格建筑（stadium 3x3、airport 4x4 等，`buildings` 命令可查全部）锚点在**左上角**，需整片干净 grass/tree
- `marina_docks_small` / `pier_large` 必须邻水
- 住宅区生长三要素：**道路连通 + 电（power_plant）+ 水（water_tower）**，之后 `simulate`；缺了 population 恒为 0
- 分区建筑免费生长；手工放置按 `buildings` 列表收费；`--free` 跳过扣费
- 每次编辑自动生成 `.bak` 备份，改坏可回滚

## 命令速查

| 命令 | 用途 |
|---|---|
| `new [--random\|--osm] [--grid N] [--seed N] [--name NAME] [--out FILE] [--ak AK] [--coord-sys wgs84\|gcj02\|bd09]` | 创建城市 |
| `map <file> [--no-legend]` / `info <file>` / `get <file> <x> <y>` | 查看 |
| `buildings` | 所有可放建筑 + 尺寸 + 费用 |
| `place <file> <type> <selectors> [--free]` | 放置 |
| `bulldoze <file> <selectors> [--free]` | 拆除（多格建筑整栋拆） |
| `zone <file> <residential\|commercial\|industrial\|none> <selectors>` | 划区（$50/格，清区免费） |
| `terraform <file> <water\|land\|tree> <selectors>` | 地形（water/land $50000/格，tree $15） |
| `tax <file> [0-100]` / `budget <file> [key] [0-100]` / `money <file> <N\|+N\|-N>` | 经济 |
| `share <file> [--url BASE] [--short] [--gallery] [--api-base URL] [--anon-key KEY]` | 分享 URL；`--short` 上传快照并打印 `/city/<code>` 短链（推荐），`--gallery` 同时公开到首页热门地图画廊（env 覆盖：`POWPOWCITY_API_BASE` / `POWPOWCITY_ANON_KEY`） |
| `screenshot <file> [-o out.png] [--zoom-out N] [--url URL]` | 截图（默认拉远看全城） |
| `simulate <file> --ticks N [-o out.json] [--url URL]` | 真实游戏引擎跑 N tick |

## 游戏访问（档位 2 用）

- 线上站 `https://powpowcity.powpow.online` 已部署 `window.__isocity` 桥，screenshot/simulate 可直接 `--url` 指向线上站
- 或本地 dev server：游戏源码 `npm run dev` 启动，默认 `http://localhost:3000`

## 地理数据源（百度地图，国内推荐）

`new --osm --place` 需要地理编码（地名→坐标）。**国内环境用百度地图**：

- 传 `--ak <AK>` 或设环境变量 `BAIDU_MAP_AK`，即走百度地理编码（快、不被墙、坐标自动 BD-09→WGS-84 纠偏）
- AK 获取：[lbsyun.baidu.com](https://lbsyun.baidu.com) → 控制台 → 创建应用，类型选**「服务端」**，IP 白名单**留空**（CLI 会跑在不同机器上）
- 无 AK 时回退 Nominatim——国内网络基本不可达，会提示改用 `--lat --lon`
- 从百度地图复制的坐标是 bd09、高德/腾讯是 gcj02：传给 `--lat/--lon` 时加 `--coord-sys bd09` 或 `--coord-sys gcj02`，自动纠偏到真实 GPS（WGS-84）再查 OSM，否则地图整体偏移 500~1300 米
- 建筑轮廓/道路/水域矢量数据仍来自 OSM Overpass（百度无公开矢量接口）；Overpass 国内可直连，偶发 504 等 60 秒重试
- 自检：`node <本技能目录>/cli/lib/baidu.mjs [--ak AK]` 跑坐标转换与编码测试

## 故障排查

- `playwright is not installed` → 在本技能目录执行 `npm install playwright && npx playwright install chromium`
- Overpass 504 → 服务端限流，等 60 秒重试（内置 3 端点自动切换）
- `Geocoding ... failed` → 没配百度 AK 且 Nominatim 不可达；配 `--ak`/`BAIDU_MAP_AK`，或改用 `--lat --lon --coord-sys bd09`
- 百度报 status 210/211 → AK 类型不是「服务端」或 IP 白名单没留空，检查应用配置
- screenshot/simulate 连接失败 → 游戏没启动或 `--url` 不对，先启动游戏或指向线上站
- 分享 URL 超长（>30000 字符）→ 部分聊天工具会截断，改用 `share --short` 短链或文件交换
- `share --short` 报错（HTTP 404 表不存在 / 网络不可达）→ 服务端 `shared_cities` 表尚未初始化或网络问题；CLI 会报清晰错误并**自动回退打印长链**，长链/文件交换仍可用
- 超大城市短链被拒（快照 >1MB）→ 压缩后仍超上限，改用 `.isocity.json` 文件交换
- 城市改坏 → 用同名 `.bak` 文件恢复

## 验证清单

编辑后建议：`map` 肉眼检查布局 → `screenshot` 视觉确认（档位 2）→ `info` 确认数据 → `share` 产出交付链接。

## 致谢与许可

- 游戏本体：[isometric-city](https://github.com/durenzidu/isometric-city)，线上版 [PowPow City](https://powpowcity.powpow.online/)
- `cli/lib/vendor/lz-string.js`：Pieroxy 的 LZ-String（WTFPL，文件头含授权声明）
- `cli/` 的规则与分享编码移植自游戏源码（`rules.mjs` ← `simulation.ts`，`share.mjs` ← `shareState.ts`），与游戏仓库同源，游戏规则更新时两处需同步
