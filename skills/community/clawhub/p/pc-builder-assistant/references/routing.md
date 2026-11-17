# 需求路由

先识别用途，再分配预算。用户有明确偏好时优先；否则按默认路由。

软件名不是触发条件本身。ComfyUI、SD、PS、PR、AE、Blender、UE、CAD、本地 agent 等词，只有和配电脑、装机、DIY、升级、预算、配置、硬件需求、性能瓶颈、卡顿或跑不动同时出现时，才进入硬件路线；纯安装、教程、插件、命令、报错、工作流或软件使用问题不使用本 skill。

## 口语化需求理解

用户常用装机圈表达 → 路由参数映射：

| 用户说 | 含义 | 路由参数 |
|--------|------|---------|
| 黑色海景房 | 黑色 + 展示型机箱(玻璃侧透) + 审美向水冷权重 + 读取风扇位 | color=black, case_type=showcase, cooler_preference=liquid_when_aesthetic, read_fan_mounts=true |
| 白色海景房 | 白色 + 展示型机箱 + 白色配件 + 审美向水冷/RGB 权重 + 读取风扇位 | color=white, case_type=showcase, cooler_preference=liquid_when_aesthetic, read_fan_mounts=true |
| 无光 / 不要灯 | 不花预算在RGB/灯效上 | rgb=false |
| 纯性能不要颜值 | 性能优先，压外观预算 | aesthetics=false |
| 水冷 / 360水冷 | 用水冷散热 | cooler_type=liquid, radiator=360 |
| 小机箱 / 紧凑机箱 | 默认优先紧凑 M-ATX；只有用户明确说 ITX、Mini-ITX、SFF 或给出严格体积/尺寸时才进入 ITX 全链路 | form_factor=MATX_compact |
| ITX / Mini-ITX / SFF | 主板、机箱、电源、显卡和散热全部按 ITX 空间约束收窄 | form_factor=ITX, require_full_itx_chain=true |
| 散热限高 / 下压散热 / 低矮散热 | 按机箱给出的 CPU 散热限高查询已知高度的风冷，不用旧平台开关绕过 | query_cooler=--max-cooler-height N |
| 低U高显 | CPU够用，显卡拉满 | routing=low_cpu_high_gpu |
| 无独显 / 不配显卡 / 核显装机 / APU / 先用核显以后加卡 | 不采购独显，CPU 必须确认带核显，主板必须有已核实视频输出 | gpu=none, require_cpu_igpu=true, query_cpu=--integrated-graphics yes, query_mb=--display-output any |
| 2K / 4K | 分辨率目标，影响显卡档位 | resolution=2K/4K |
| 能跑多少帧 / 跑满 240Hz、360Hz、500Hz / 1K 500帧 | 游戏帧率参考需求 | read=game-performance.md, run=query_game_fps.py |
| 多开 / 挂机 | CPU核心+内存容量优先 | routing=multitask |
| Intel 还是 AMD / 办公选什么 / 内存要多大 / 风冷能不能压 / 电源要多大 | 硬件选择或原理问答 | routing=hardware_qa, mode=reference |
| 三角洲 / 吃鸡 / CS2 / GO / 瓦 | 热门 FPS / 电竞网游，高帧和 1% low 优先 | routing=fps, cpu_priority=x3d |
| 直播 / 推流 / OBS / 录制 | 需要硬件编码和稳定后台 | routing=streaming, cpu_priority=intel_igpu |
| 内置采集卡 / PCIe 声卡网卡 / 扩展卡 | 独显之外还需物理扩展槽，并复核显卡厚度、槽间距和通道共享 | query_mb=--min-pcie-slots 2, check=--require-extra-pcie-slot |
| 必须有 USB4 / 雷电口 | 只接受精确型号已核实的后置端口；USB-C 或雷电针脚不能替代 | query_mb=--require-usb4/--require-thunderbolt |
| 为本地 AI 编程/终端 agent 工作流配电脑 / 给 Codex、Claude Code、opencode、OpenClaw、Hermes 配电脑 / 多 agent 并发主机 | 本地终端/IDE agent、项目索引、缓存、测试工具链和可能的本地模型带来的硬件负载 | routing=local_agent, priority=ram_ssd_cpu |
| 16G/24G/32G/96G 显存能跑多大模型 / 30B、32B、70B 要什么显卡 | 双向估算本地文本模型、显存和系统内存容量；区分最低可试与稳妥推荐 | read=local-model-fit.md, run=query_model_fit.py |
| ComfyUI / SD / Stable Diffusion / 文生图 / 文生视频 | 本地生成式 AI，吃 NVIDIA CUDA、显存、SSD 和内存 | routing=local_ai_image_video, gpu_priority=nvidia_vram |
| PS / Photoshop / Lightroom / 修图 / 摄影后期 | 图片后期，CPU/内存/SSD 优先，中端显卡足够 | routing=photo_editing |
| PR / Premiere / 剪辑 / 视频剪辑 / 达芬奇 / DaVinci | 视频剪辑/调色，按分辨率、编码、特效和显存分流 | routing=video_editing |
| AE / After Effects / 动效 / 合成 | 动效合成，CPU/内存/缓存 SSD 优先，3D 再提高 GPU | routing=motion_graphics |
| Blender / C4D / 3D建模 / 渲染 | 建模、动画、GPU/CPU 渲染分流 | routing=3d_workstation |
| UE / Unreal / Unity / 游戏开发 | 引擎开发，CPU 编译、GPU 视口、内存和 SSD 均衡 | routing=game_dev |
| CAD / AutoCAD / SolidWorks / 建模绘图 | 按 2D/3D/装配规模分流 | routing=cad, ask_software=true |

## 默认路由

本节只做场景识别和轻量映射；具体取舍规则读取 `scenarios.md`。

| 用途 | scenario_id | 备注 |
|------|-------------|------|
| 硬件选择问答 | hardware_qa | 按场景直接解释 CPU/内存/散热/电源/主板等取舍，不强行输出整机 |
| 3A / 单机大作 | gaming_3a | 低U高显路线 |
| 网游 / 日常游戏 | online_gaming | CPU、显卡、内存均衡 |
| 三角洲 / PUBG / CS2 / 无畏契约 / P社策略 | fps_esports | 高帧、1% low、X3D 路线 |
| 直播 / 推流 / 录制 | streaming | Intel 核显、NVENC、编码路线 |
| 本地 agent 硬件配置 | local_agent | 只在用户明确为本地 AI 编程/终端 agent 配电脑时触发 |
| ComfyUI / SD / 文生视频 / 本地模型 | local_ai_image_video | NVIDIA/CUDA、显存、SSD、内存优先 |
| PS / Lightroom | photo_editing | 图片后期 |
| PR / 达芬奇 / 视频剪辑 | video_editing | 编解码、显存、I/O、缓存盘 |
| AE | motion_graphics | CPU、内存、缓存盘 |
| Blender / 3D / 渲染 | 3d_workstation | GPU/CPU 渲染分流 |
| UE / Unity / 游戏开发 | game_dev | 编译、Shader、视口、SSD |
| CAD / 建模绘图 | cad | 先区分 2D、3D、装配和认证需求 |

用户问具体帧率或跑满刷新率时，读取 `game-performance.md` 并运行 `query_game_fps.py`；未收录游戏或硬件组合不要编 FPS。

## 核显/无独显直达路由

用户明确要求无独显、不配显卡、核显装机、APU、办公机或先用核显以后加卡时，直接进入核显整机，不先尝试独显方案，也不要求用户再次确认。

1. CPU 查询必须加 `--integrated-graphics yes`；Intel F/KF、AMD F 和核显状态未知型号不得进入方案。显卡不查询、不计价，报价表显卡行写“无独显，使用 CPU 核显，¥0”。
2. 核显路线默认面向办公、网页、视频、轻修图、轻剪辑、家庭影音和过渡使用。用户同时要求 3A、CUDA、本地 AI、重度 3D 或高画质高帧时，先说明核显不能满足该目标，再给独显预算方向。
3. 主板查询加 `--display-output any`，优先选择已有 `display_outputs` 证据的候选；用户明确显示器接口时可改用 `--display-output HDMI/DisplayPort/VGA`。字段缺失会被完整度门禁拦住，不能只凭 CPU 有核显就承诺显示链路已确认。
4. 用户给出未来目标显卡或性能档位时，按目标卡的功耗、供电接口和长度预留电源与机箱；目标未定时只说明可后续加卡，不承诺任意显卡均可兼容。
5. 最终兼容检查仍用 `--strict --require-complete`，传 CPU、主板、内存、硬盘、散热、电源和机箱，不传 `--gpu`。

## 性能档位与预算取舍

不要用固定金额表代替本次查询；硬件价格会变化，同一预算所需配件也可能变化。先按用途确定性能底线，再用本次查询的 14 天内价格组单。

| 用途档位 | 典型性能路线 | 主要取舍 |
|------|---------|------|
| 办公、影音、核显过渡 | 已确认带核显的 CPU + 有已核实视频输出的主板 | 优先内存、SSD、安静和小体积；GPU 行计 ¥0，不能承诺未指定的未来显卡 |
| 1080p 入门游戏 | 入门独显与对应的成熟低功耗 CPU 平台 | 显卡优先于外观；容量和平台代际按当前整机价取舍，只说明 1080p 入门定位 |
| 2K 主流游戏 | 中端独显，CPU 按高刷与模拟类游戏需求升级 | 比较 8GB/16GB 显存版，不因后缀或显存容量单独判为同档 |
| 2K 高刷、4K 入门 | 高端独显与均衡 CPU，电源、散热和机箱一起核算 | 显卡、电源、内存、SSD 不可用旧低价闭合；按用户优先级调整非核心件 |
| 4K 高画质 | 更高一档独显，CPU 按游戏或生产力分流 | 不默认为纯游戏加购过多 CPU 内核；先做整机总价和散热风道核算 |
| 旗舰、本地大模型、工作站 | 当前库内旗舰显卡或经验证的工作站卡 | 只有用途和本次报价都支持时启用；显存容量、系统内存、SSD、电源和机箱不能删减成纸面方案 |

预算低到无法用当前有效价格覆盖用途底线时，直接说明预算缺口。可给出核显过渡或旧机升级方案；用户需要完整新主机时，也可并列最接近的完整方案及超支项目，但不能省略显卡、电源或机箱后把未完成清单写成完整配置。

## 预算闭合决策流程（有限状态机）

整机报价按状态推进，禁止在同一筛选条件内重复重组。查询次数和调整轮次是控制无效枚举的内部提示，不能压过必要的兼容核验；触顶前应保留已核实结果并报告未闭合项。

1. S1 正常选件：用用户预算和用途查询候选并组单。用户明确说“最多/不超过/不能超”时，把该金额当作硬上限；没有硬上限时，92%-102% 只作为软目标。任何缺价、过期价或不同币种都不能用来凑闭合。
2. S2 定向调整：
   - 第 1 轮：压缩主板、机箱、散热、风扇、电源等非核心溢价，不动容量/供电/显卡档位。
   - 第 2 轮：显卡降一档（如 RTX5060 → RTX5050/Arc B580/RX9060XT 8GB），并同步适配 CPU/主板/电源，不跨平台硬凑。
   - 只有用途允许时，才把内存或硬盘容量降级为临时取舍，并写明后续升级顺序。
3. S3 终端态：停止无目的的重新筛选，输出最接近当前约束的可行方案、明确超支额和导致超支的项目；若硬上限内没有符合用途的完整方案，给核显过渡或旧机升级备选。用户可以据此决定是否调整要求。
4. 终端态不得假装刚好卡进预算，不得用缺价、过期、二手或范围外老平台凑数。

## 选件优先级

先满足用途和预算，再看外观。不要把每个品类的最低价候选直接拼成整机。

1. 优先选择数据完整的配件: 有 `price_cny`/`price_status`/`price_date`，并且关键兼容字段不为空。
2. 避开硬件范围外的老平台和老规格: DDR3、120/128GB SATA SSD、Intel 11代及更早、RTX 40/RX 7000 等不作为新装机首选。AM4 只保留 X3D + B550 + DDR4 的低预算 FPS 例外路线，不作为普通新装机默认平台。
3. 整机报价先服从用户明确上限；未给出硬上限时，再把预算的 92%-102% 作为软目标。低于目标不自动代表“更好”，先检查是否漏项或用了过期价。
4. 总价超过软目标时，先回查主板、机箱、散热和风扇等非核心溢价；能在不破坏容量、供电、兼容和场景底线时，压回预算附近。仍无法闭合时按“预算闭合决策流程”进入终端态，不要假装刚好卡进预算。
5. 查询候选时按品类分开跑，通常用 `--limit 50` 起步；高预算或白色/海景房等强约束场景用更大的 limit 后二次筛选。CPU、显卡、内存和 SSD 低于可信行情日低价地板时不作默认方案；显卡、内存、SSD 还可按同规格/同定位分布过滤明显低价。CPU 不按同型号中位数离群算法删除，只按日低价地板、具体型号、代际、盒装/散片口径和同价位性能比较。
6. 中高端装机查询显卡、主板、系统盘/生产力 SSD 和内存候选时用 `--sort tier`: 显卡按芯片等级优先（如 RTX 5070 优先于 RTX 5060Ti），主板按芯片组等级优先（B760/B650 优先于 H610/A620），SSD/内存按公开采用率信号、规格完整度和关键参数优先。CPU 的 tier 是场景候选顺序，不是纯跑分榜；例如剪辑/混合生产力默认可让 Core Ultra 7 270K/同档 U7 先于高价 U9，只有重度多任务、复杂工程或预算明确足够时再提高 U9 权重。SSD 若只要求 1TB/2TB，不要被 4TB 顶级盘首屏带偏；先贴合用户容量，再比较 PCIe 代际、TLC、缓存、保修和价格。
7. 候选收窄按依赖顺序做，不要每类各取最低价后拼单:
   - 选主板时用已选 CPU 的 socket/供电需求过滤；选 CPU 时反向核对已选主板 socket。
   - 选内存时用主板 DDR 代际、可支持频率、槽位和容量上限过滤；用户需要 64GB/96GB/128GB 或进入生产力/本地 AI 路线时用 `--min-capacity ... --max-capacity ... --sort tier` 收窄；输出必须写清容量、频率和时序。
   - 选电源时用已选整机功耗加余量过滤，不只看显卡推荐瓦数。
   - 选机箱时用主板版型、显卡限长、散热限高/冷排位和电源规格过滤；显卡限长建议留 20-30mm 以上余量，前置冷排、厚风扇、转接线或静音机箱留更大余量。
   - 最后再用 `check_compatibility.py --strict --require-complete` 做全单校验。返回待复核状态时不能写成完整通过，应换字段完整候选或列人工复核项。

## 后续读取

- 已确认要输出具体型号、完整配置、升级方案、配置补全或搭配检查时，继续读取 `selection-policy.md`。
- 只做意图路由、纯方向问答或硬件知识解释时，不加载完整选件策略；按需读取 `hardware-faq.md`。
- 具体用途仍读取 `scenarios.md`，价格和兼容字段分别读取 `pricing.md`、`compatibility.md`。
- 用户询问一体式水冷保修、漏液包赔、售后网址或在线安装说明书时，按需读取 `liquid-cooling-support.md`；具体购买或索赔条款还要打开对应官方页面复核。
