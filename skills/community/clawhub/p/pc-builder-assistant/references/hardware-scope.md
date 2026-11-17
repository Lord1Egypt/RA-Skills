# 硬件范围

## CPU

- Intel: 12/13/14 代 Core 台式机 + Core Ultra 200S 台式机
  - Plus 只作为 250K Plus/250KF Plus/270K Plus 等具体型号后缀
- AMD: Ryzen 5 / Ryzen 7 / Ryzen 9 AM5 台式机优先；AM4 只保留 Ryzen 5/7 X3D + B550 + DDR4 的低预算 FPS 例外路线。明确查询该路线时给 CPU/主板命令加 `--socket AM4 --sort tier`，脚本只放行 AM4 X3D 与 B550；审计其他旧平台才使用 `--include-legacy`
- 默认候选池不推荐旧显卡；但用户明确已有或点名某个旧芯片时，`--gpu-chip` 属于显式查件入口，可直接定位该芯片，不要求再附加 `--include-legacy`。普通浏览旧库仍使用 `--include-legacy`。
- 无独显整机允许当前范围内已确认带核显的 Intel 非 F/KF、AMD APU/AM5 非 F 型号；必须用 `--integrated-graphics yes` 查询，不按型号印象手选核显。
- 不收录: AM4 非 X3D 新装机路线、A520 搭高功耗 X3D 默认方案、Intel 11 代及更早、二手/99新/翻新/矿卡

## GPU

- NVIDIA: RTX 50 系 + 5090D/5090D V2 + 复产 RTX 3060 Ti；RTX PRO 6000 Blackwell Workstation 96GB 仅作为有明确本地大模型/工作站需求和足够整机预算的特例
  - RTX 40 系不再收录
- AMD: RX 9000 系 (9060 XT/9070 GRE/9070/9070 XT)
  - RX 7000 系不再收录
- Intel: Arc B570/B580

## 主板

品牌: ASUS, Gigabyte, MSI, ASRock, Colorful, Maxsun, Biostar

- 无独显整机只使用已由厂商规格核实 `display_outputs` 的主板；用 `--display-output any` 查询，明确接口时按 HDMI/DisplayPort/VGA 过滤。
- 主板扩展能力按精确型号维护 `pcie_slot_layout`、`m2_slot_layout`、USB4/雷电后置端口状态及共享条件。`pcie_slot_layout` 只表示显卡/采集卡等物理扩展槽，`m2_slot_layout` 才表示 SSD 槽位及其 PCIe 代际；两者不能混用。用 `--min-pcie-slots` 只筛已核实的物理扩展槽数；`--require-usb4` 和 `--require-thunderbolt` 对未知字段保守排除。USB-C 不自动等于 USB4，雷电针脚不自动等于雷电口。

## 内存

品牌: Kingston, ADATA/XPG, G.Skill, Crucial, Corsair, Team, Lexar,
Gloway, Asgard, ZhiTai
- DDR4: 3200/3600
- DDR5: 6000/6400/7200

## SSD

品牌: Samsung, WD, Kioxia, Crucial, Kingston, SK hynix, Solidigm,
Lexar, ZhiTai, Fanxiang
- 只按 PCIe 4.0/5.0 + 容量 + M.2 核对
- 不参与色系/RGB/机箱外观匹配

## 电源

品牌: Seasonic, Super Flower, Corsair, Cooler Master, FSP,
Great Wall, Huntkey, MSI, ASUS, Thermaltake, XPG, Antec

## 散热

品牌: Thermalright, DeepCool, Cooler Master, ID-COOLING, Jonsbo,
NZXT, Corsair, Arctic, Noctua, MSI, ASUS

- 普通查询默认保留当前推荐范围；ITX、小钢炮或机箱给出明确风冷限高时，使用 `--max-cooler-height N` 显式查询已知高度的低矮/下压风冷。未知高度条目不因型号印象进入结果。
- 散热结构字段包括 `socket_support`、`air_cooler_layout`（低矮/下压/单塔/双塔）、`heatpipe_count` 和 `radiator_mm`。字段只记录型号一致的明确证据；缺少塔体、热管或冷排尺寸时，高负载 CPU 配置不能完整通过。

## 机箱

品牌: ASUS, Jonsbo, DeepCool, Lian Li, Cooler Master, NZXT,
Fractal Design, Corsair, Montech, Phanteks, Thermaltake, SAMA

## 风扇

- 独立按需品类，仅海景房补风扇、水冷夹汉堡、风道/无光风扇或用户明确要风扇时启用。
- 收录机箱风扇、冷排风扇套装和无风扇水冷框架；CPU 风冷、双塔/单塔/下压式散热器和内存散热器不属于风扇分组。
- 可用字段包括尺寸、正页/反页、颜色、RGB/无光、积木/串联、带屏、240/280/360/420/480 一体式或冷排风扇套装和默认推荐状态；无风扇水冷框架默认不参与机箱风扇推荐，但用户明确指定 `--fan-type aio_frame` 时可查询。
- 风扇转速字段暂不完整；需要控制噪音时优先同系列/同尺寸/同定位风扇，避免混搭明显高转高速型号。

## 显示器

- 独立数据库，仅用户明确要求“带显示器/推荐显示器/屏幕”时启用。
- 按分辨率、尺寸、刷新率和参考价做候选筛选；不参与整机默认总价、兼容性检查或机箱/电源/散热决策。
- 显示器候选只按分辨率、尺寸、刷新率和参考价筛选。
