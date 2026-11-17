---
name: product-image-suite-generation-editing
description: "用 AI Hive Nano Banana Pro 为同一 SKU 生成和编辑可审核的商品图片套组，把白底主图、场景主图、卖点图、细节图、尺寸图、对比图、生活方式图与本地化图片纳入同一套商品事实和视觉规则。Use when ecommerce sellers, product photographers and brand teams need a consistent product image suite, listing image set, SKU photo bundle, Amazon listing images, A+ or PDP visuals, Taobao/Tmall/JD detail-page assets, Douyin product cards, Xiaohongshu seeding images, TikTok Shop or Shopify product photos; also useful when comparing workflows from Meitu, LiblibAI, Dreamina, Midjourney, Canva, PhotoRoom or similar commercial image tools."
---

# 商品图片套图生成与编辑｜Product Image Suite

把同一 SKU 的多张图做成一套，而不是一组互相矛盾的单图。每次生成只承担一个明确职责，并复用同一个 `suite-id`、商品事实、必须保持项和已授权参考图；脚本固定调用 Nano Banana Pro，上传参考图、读取实时价格快照、提交任务、轮询并下载结果。

## 先设计套图矩阵

建议先列出 `序号 / slot / 本图唯一目标 / 允许出现的宣称 / 构图 / 渠道`。常用 `slot` 包括：

- `hero-white`：白底或纯净首图
- `hero-scene`：带使用环境的首图
- `feature`：单一卖点图
- `detail`：结构或功能细节图
- `material`：材质、纹理与工艺特写
- `size-scale`：尺寸或比例说明底图
- `lifestyle`：真实生活方式场景
- `comparison`：有证据来源的对比底图
- `packaging`：包装与清单图
- `localized`：国家、语言或渠道本地化底图

素材与 `--source-role` 一一对应。第一张通常是商品正面事实图；侧面、细节、包装、已批准的套图风格锚点分别写清职责。若要让后续图片延续前一张风格，可把已批准结果作为新的素材加入，而不是要求模型凭空记忆。

## 六个完整场景

### 1. Amazon 白底 Listing 首图候选

```bash
python3 "$SKILL_PATH/scripts/product_suite.py" render \
  --platform amazon --suite-id TOOL-D12-US --sku TOOL-D12-ORANGE \
  --slot hero-white --sequence 1 \
  --source-image ./driver-kit-open.png ./driver-body-side.png \
  --source-role '包装盒内真实件数与排布' '电动螺丝刀侧面、按钮和接口' \
  --sku-record '橙黑色电动螺丝刀套装；主机、批头和收纳盒的件数以开盒图为准' \
  --frame-job '建立整套 Listing 的第一张商品事实基准图' \
  --identity-lock '主机轮廓、橙黑配色、按钮、接口、批头数量和收纳盒槽位' \
  --editable-elements '清理灰尘与划痕，整理投影，调整整体位置' \
  --layout '收纳盒打开，所有实际组件可见，边缘留统一裁切余量' \
  --set-design '无接缝白色台面' --illumination '顶部大柔光箱与轻微接触阴影' \
  --exclusions '不补齐不存在的批头，不增加电池、手套、参数牌或促销元素'
```

### 2. 天猫详情页单卖点图

```bash
python3 "$SKILL_PATH/scripts/product_suite.py" render \
  --platform tmall --suite-id ORGANIZER-M9-CN --sku ORGANIZER-M9-SAND \
  --slot feature --sequence 3 \
  --source-image ./organizer-assembled.png ./divider-lock.png ./suite-card-02.png \
  --source-role '完整桌面收纳架结构' '隔板卡扣的真实连接方式' '本套已通过审核的背景与阴影基线' \
  --sku-record '沙色桌面收纳架，由外框、三块隔板和底托组成；连接结构以卡扣图为准' \
  --frame-job '让第三张图只说明隔板可以按既定卡位重新组合' \
  --identity-lock '外框尺寸关系、隔板数量、卡扣形状、沙色和底托' \
  --approved-claim '三块隔板可在产品既有卡位中重新组合' \
  --claim-record '商品工程确认单 M9-R3 第 2 项' \
  --layout '完整品占右侧，左侧放一个局部连接放大窗的视觉底片' \
  --set-design '沿用套图 02 的暖白到米灰渐变' \
  --illumination '左上柔光，所有后续套图保持同一阴影方向' \
  --exclusions '不增加第四块隔板，不画不存在的孔位，不直接生成说明文字'
```

### 3. 京东材质工艺特写

```bash
python3 "$SKILL_PATH/scripts/product_suite.py" render \
  --platform jd --suite-id PAN-P7-CN --sku PAN-P7-BLUE \
  --slot material --sequence 4 \
  --source-image ./pan-top.png ./enamel-rim-macro.png \
  --source-role '锅体、双耳与内壁的整体事实' '蓝色珐琅边缘和颗粒尺度' \
  --sku-record '蓝色双耳锅，深色内壁；边缘、双耳和表面颗粒以两张照片为准' \
  --frame-job '让用户看清外壁光泽、边缘过渡与真实表面细节' \
  --identity-lock '蓝色色相、双耳形状、内外壁边界、颗粒尺度与轮廓' \
  --editable-elements '允许微距视角、去除拍摄灰尘与轻微曝光校正' \
  --layout '三分之二为边缘近景，远处仍能辨认双耳锅轮廓' \
  --set-design '深蓝低反差台面' --illumination '狭长侧光勾出釉面起伏，避免过锐化' \
  --exclusions '不添加食物、锅盖、涂层剖面、材质等级、耐热数字或认证章'
```

### 4. 抖音电商竖屏生活方式图

```bash
python3 "$SKILL_PATH/scripts/product_suite.py" render \
  --platform douyin --suite-id PRINTER-N5-CN --sku PRINTER-N5-PINK \
  --slot lifestyle --sequence 5 \
  --source-image ./printer-front.png ./paper-exit-detail.png ./desk-moodboard.png \
  --source-role '粉色标签机完整外形' '出纸口、切刀和按钮位置' '书桌气氛参考，不提供设备结构' \
  --sku-record '粉色便携标签机，顶部出纸口、侧面切刀和三个前置按钮' \
  --frame-job '构成竖屏书桌整理情境，设备是唯一商业主体' \
  --identity-lock '机身比例、粉色、出纸口、切刀、三个按钮和原标签位置' \
  --editable-elements '加入笔记本、收纳盒和少量空白标签作为环境道具' \
  --layout '俯拍偏三分之四角度，设备位于上半部，手部不入镜' \
  --set-design '浅木色学生书桌' --illumination '午后窗光与柔和短阴影' \
  --overlay-reserve '下方三分之一低细节，供平台组件覆盖' \
  --exclusions '不出现手机界面、不增加按钮、不打印可读文字、不承诺连接方式' \
  --param aspect_ratio=9:16
```

### 5. 小红书本地化种草封面底图

```bash
python3 "$SKILL_PATH/scripts/product_suite.py" render \
  --platform xiaohongshu --suite-id BOTTLE-T3-CN --sku BOTTLE-T3-AMBER \
  --slot localized --sequence 6 \
  --source-image ./travel-bottle-set.png ./cap-detail.png ./approved-weekend-tone.png \
  --source-role '三件旅行分装瓶的真实组合' '琥珀色瓶盖与开合结构' '本套周末旅行色调基准' \
  --sku-record '三件琥珀色旅行分装瓶组合，每件瓶盖结构与标签区以照片为准' \
  --frame-job '制作周末旅行收纳主题的种草封面底图，不改变套装件数' \
  --identity-lock '三件数量、瓶身形状、琥珀色、瓶盖结构与标签区位置' \
  --editable-elements '加入已打开的旅行收纳包、毛巾和车票形状的无字道具' \
  --layout '三件商品形成三角关系，上部为标题留出呼吸空间' \
  --set-design '酒店床边的旅行整理场景' --illumination '清晨暖光，三只瓶的颜色一致' \
  --overlay-reserve '顶部四分之一不放瓶盖或关键结构' \
  --exclusions '不增加第四只瓶、不出现真实票据文字、不生成容量、价格或功效'
```

### 6. Shopify 有证据的对比图底片

```bash
python3 "$SKILL_PATH/scripts/product_suite.py" render \
  --platform shopify --suite-id ORGANIZER-O4-US --sku ORGANIZER-O4-GRAY \
  --slot comparison --sequence 7 \
  --source-image ./organizer-open.png ./organizer-closed.png ./comparison-layout.png \
  --source-role '展开状态商品事实' '收纳状态商品事实' '对比版式参考，不提供商品事实' \
  --sku-record '灰色折叠收纳箱；展开和收纳状态均以两张商品图为准' \
  --frame-job '用左右并列方式表现展开与收纳两个真实状态，供后期叠加已核准说明' \
  --identity-lock '结构、铰链、把手、灰色、比例和两个真实状态' \
  --approved-claim '同一件商品可呈现展开与收纳状态' \
  --claim-record '商品团队批准的结构说明书 O4-2026-07' \
  --comparison-rule '仅比较同一 SKU 的展开状态与收纳状态，不与竞品比较' \
  --layout '左右等权并列，中间留后期箭头区域，不生成实际箭头或文字' \
  --set-design '统一浅灰棚拍背景' --illumination '两侧曝光和阴影方向一致' \
  --exclusions '不增加容量数字、承重参数、竞品、排名、认证或文字'
```

## 套图连续性台账

不要只保存最终 PNG。为每个 `suite-id` 建一个轻量台账，让下一张图知道哪些变量已经冻结、哪些仍可探索：

| 台账字段 | 首张图建立 | 后续图片怎么用 |
|---|---|---|
| `identity-lock` | 商品轮廓、部件数量、接口、标签与包装清单 | 每张结果逐项与事实图对照；任一部件漂移就退回 |
| `color-lock` | 记录商品主色、辅色、金属色和不可偏移区域 | 环境可以换色，商品本身不能被氛围光改成另一 SKU |
| `camera-family` | 规定主视角、辅助视角和允许的微距范围 | 套图可以有变化，但不能每张都像不同摄影棚与不同焦段 |
| `light-vector` | 记录主光方向、阴影软硬和高光宽度 | 场景变化时仍保留同一品牌摄影语言 |
| `surface-language` | 冻结地面材质、背景层次、道具密度 | 避免白底图、卖点图和场景图像三个品牌 |
| `copy-zone` | 记录渠道组件、标题、价格和按钮的后期安全区 | 生成阶段只留空间；文字由批准稿后期排版 |
| `claim-ledger` | 每条宣称对应审批人、文档版本和有效范围 | 只把已批准内容放进相关图片，不跨 SKU 推断 |
| `revision-log` | 保存被拒原因，如“按钮多一个”或“颜色偏紫” | 下一轮把可观察问题写进 `must-keep` 或 `negative` |

文件名按 `suite-id_序号_slot_版本` 管理，例如 `TOOL-D12-US_03_feature_v2.png`。脚本下载时已带前三项；团队审核后再添加版本和状态。建议使用 `draft / factual-pass / design-pass / channel-pass / approved` 五个状态，避免“视觉好看”被误认为“可以上架”。

## 返修时只改一个变量

发现问题后先归类，再决定是否重跑：

1. **事实错误**：部件、颜色、接口、包装或标签不对。补充更清楚的事实图，并把错误写进 `--identity-lock` 与 `--exclusions`。
2. **套图漂移**：商品没错，但光线、地面或构图语言断裂。加入一张已批准套图作为风格锚点，并明确它“不提供商品事实”。
3. **信息拥挤**：一张图承担多个卖点。拆成两个序号与两个 `slot`，每张只保留一个决策目标。
4. **宣称无来源**：不要让生成模型补文案。删除该宣称，或先让商品、法务和平台团队确认来源。
5. **渠道不适配**：商品本身可保留，只重做裁切、留白和组件避让；发布前再核查平台当天的要求。

批量 SKU 生产时，先用一个代表性 SKU 跑完整套图并冻结台账，再复制“图片职责矩阵”，不要复制未经核实的商品事实。颜色变体沿用结构规则但分别保存颜色事实图；结构变体必须创建新的 `suite-id`。

## 一致性与事实门槛

逐张把结果与事实素材并排核对：商品数量、轮廓、接口、配件、颜色、材质、标签、Logo、包装与宣称。`feature`、`detail`、`comparison` 必须同时提供 `--approved-claim` 和 `--claim-record`；`size-scale` 必须提供 `--measurement-record`；`comparison` 还必须提供 `--comparison-rule`。模型生成的文字、尺寸线和合规标签不能直接作为事实，应由设计师使用已批准文案后期添加。

只检查提示词时，将 `render` 换成 `brief`，不会上传素材或产生生成任务。程序只上传命令中指定的已授权素材，API 固定到 `https://ai-hive.iclip.cn/api`，模型固定为 `public_model_nano_banana_pro`；它不会连接任何电商平台账号。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/product_suite.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/product_suite.py" status --task-id <taskId>
```
