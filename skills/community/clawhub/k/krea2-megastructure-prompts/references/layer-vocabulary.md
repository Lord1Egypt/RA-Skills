# 七层词库与尺度锚定技法

## 尺度锚定：本 skill 的核心技术

模型读到 "colossal" 只会稍微放大物体；读到 "a lone figure at its base is the size of a fingernail" 才会真正重算比例关系。**永远优先用参照物，其次用可测量数字，最后才用尺寸形容词。**

### 四种锚定手段

**1. 参照物（最有效）**
按场景挑一个，写在提示词后半段（光之后、镜头之前）：

| 场景 | 参照物写法 |
|---|---|
| 陆地 | `a lone figure at the base is no taller than a fingernail` · `a caravan of six camels crossing below, ant-sized` · `a single vehicle on the access road is a speck` |
| 海面 | `a fishing trawler is a white speck against the hull` · `a kayak at the base, impossibly small` |
| 天空 | `flocks of birds swirl around the summit like gnats` · `clouds drift at mid-height and swallow the lower third` |
| 城市 | `a city skyline is visible at the base of the landing leg` · `a single window opening is large enough to swallow a city block` |
| 内部 | `workers on the catwalks are specks` · `a village of dozens of houses sits between two ribs` |

**2. 可测量数字**
`rises over four kilometers` · `eleven kilometers bow to stern` · `thirty stories tall` · `the wall stretches to the horizon, over two hundred meters high` · `a single tread is the height of a five-story building`

**3. 局部特写反推**
不拍全身，只拍**一段表面**：一道墙、一片甲、一块岩层、一只脚。靠"这显然只是巨大整体的一小块"来制造尺度。关键要素：表面纹理极细、附着生态（苔藓、藤壶、鸟巢、积尘）、景深极浅、不出现地平线。

**4. 大气分层（必加）**
大尺度物体的物理特征是：**越远越被大气冲淡**。不写这条，画面立刻变平、变小。
三段式模板：
> `the foreground <surface> is razor sharp; the middle section is veiled in <mist/haze/dust>; the <top/far end> dissolves entirely into <cloud/atmosphere>`

### 结构可读性

巨构最怕糊成一团。至少写 2 个可辨认的重复单元：
`rows of identical arched windows` · `rib-like buttresses at regular intervals` · `visible seams between prefabricated blocks` · `stepped terraces` · `lattice of exposed trusses` · `plating divided into panels` · `staircases switchbacking up the facade` · `suspended cables in a regular fan`

### 重量感

写"它凭什么不倒"：
`massive buttressed base` 巨大的扶壁基座 · `cantilevered counterweighted by a stone spur` 悬挑由石翼配重 · `anchored by tension cables driven into bedrock` 张索锚入基岩 · `roots gripping the cliff like a hand` 根如手抓岩 · `sagging under its own weight, cracks spreading` 自重下垂、裂缝蔓延

---

## L1 · CORE 主体与结构语法

**句式**：`<结构语法> <材质> <主体名词>, <重复单元>, <支撑方式>`

**主体名词**：sky fortress · arcology tower · hollow colossus · terraced ziggurat · orbital ring · leviathan · megalithic gate · inverted mountain · world tree · stranded hulk · glacier face · crystal geode · planetary engine

**结构语法**：见 `scene-playbooks.md` 各剧本。

**动词/状态**（加一点更好）：`rising out of` · `clinging to` · `striding across` · `half-sunk into` · `overgrown by` · `weathered into` · `collapsing slowly into` · `drifting above`

---

## L2 · SCALE 尺度锚定

见上文。通常 1 句，最多 2 句。

---

## L3 · MATERIAL 材质与表面

**模板**：`<主材>, <风化/侵蚀>, <附着物>, <表面状态>`

**主材**：weathered board-formed concrete · oxidized copper · banded sandstone · rusted corten steel · pitted hull steel · glacial blue ice · wet basalt · petrified hide · chitinous plating · mossy bone · polished obsidian · mirror chrome · veined marble · glazed ceramic tile

**风化**：eroded to rounded edges · pitted and scarred · scorched and blackened · bleached by sun · cracked and spalled · polished smooth by wind · stained with rust streaks · salt-crusted

**附着物**：lichen and moss · clinging vines and stunted trees · barnacles and coral · nesting birds · accumulated dust in every crevice · kelp and dried algae · rusted ladders and prayer flags · settlements built onto it

**表面状态**：wet and reflective · slick with rain · frosted with cryogenic ice · matte and chalky · dusted with ash · slick with oil

---

## L4 · ENVIRONMENT 环境与占据

**大气/天气**：sea of cloud · dust haze · driving monsoon rain · volumetric fog · falling ash · salt spray · aurora · storm front · mist layered between strata · heat shimmer

**谁住在上面**：terraced rice fields · a shantytown of tin roofs · monk cells carved into the ledges · markets strung between buttresses · cables and walkways · beacons and signal fires

**时间痕迹**：half-buried in dune sand · reclaimed by jungle · frozen mid-collapse · long abandoned · still under construction, scaffolding everywhere

---

## L5 · LIGHT 光与大气

**光源方向**：`low sun raking across from the left` · `backlit by a blazing sun` · `single shaft of dawn light` · `lit from below by sodium dock lights` · `god rays piercing the haze` · `overcast diffused light` · `moonlit with cool blue fill`

**时间**：`blue hour` · `golden hour` · `dawn` · `pre-dawn cold light` · `high noon harsh light` · `dusk` · `storm light`

**体积光**：`volumetric shafts through the mist` · `god rays` · `light shaft falling through the opening` · `dusty beams`

**对比/色温**：`warm amber against cold blue shadow` · `high contrast, deep crushed blacks` · `soft even light` · `rim light separating subject from background` · `specular highlights along wet edges`

**大气透视**（必写）：`atmospheric perspective with the far section faded to pale blue` · `the distant legs dissolve into golden dust`

---

## L6 · CAMERA 镜头与构图

**焦距**（Krea 2 理解摄影参数，写具体值很有效）
- `14mm` / `16mm` ultra-wide — 极端仰视、畸变强化高度
- `24mm` wide — 环境与主体并重的标准广角
- `35mm` — 远景全身、人景关系
- `50mm` — 平实、纪念碑式
- `85mm` / `135mm` — 长焦压缩，把远处的巨物压到眼前
- `100mm macro` — 表面特写
- `tilt-shift` — 微缩/模型感（**慎用**，会削弱宏大感；除非要刻意做"这是一座模型"的效果）

**角度**：`extreme low angle looking up` · `high aerial view looking down` · `eye level from a neighbouring ridge` · `from inside looking out` · `worm's-eye view` · `three-quarter view`

**构图**：`the subject fills the frame and extends beyond the top edge` · `vertical composition, subject in the right third` · `horizon placed low, vast negative space above` · `symmetrical centered composition` · `framed through an archway in the foreground` · `dwarfed by the scale, tiny figure in the lower third`

**曝光/质感**：`1/2000s frozen detail` · `long exposure smoothing the water` · `shallow depth of field` · `deep focus front to back` · `anamorphic flare` · `film grain`

---

## L7 · STYLE 风格与渲染

一句话即可，但**必须写出媒介**。风格预设见 `references/style-presets.md`。

**常用媒介词**：cinematic matte painting · photorealistic photograph · oil painting · 3D render (Octane / Redshift) · architectural visualization · ink wash painting · gouache illustration · concept art for film · charcoal and graphite study · vintage lithograph poster

---

## 组装模板（可直接填空）

```
<L1 结构语法 + 材质 + 主体>, <重复单元>, <支撑方式>, <附着生态>.
<L4 环境/占据>.
<L2 尺度锚定：参照物 + 数字>.
<L3 材质细节 + 表面状态>.
<L5 光：时间 + 方向 + 体积光 + 大气透视分层>.
<L6 镜头：焦距 + 角度 + 构图 + 画幅关系>.
<L7 风格媒介 + 调色 + 质感>.
```

**注意**：不用每层都写成独立一句。熟练后把它们自然揉成 3–5 个长句更接近 Krea 2 偏好的自然语言风格；分层只是保证不漏项。

## 反模式清单（写了就扣分）

- ❌ 三个以上尺寸形容词堆在一起：`huge giant massive enormous colossal`
- ❌ 元语言：`This image shows a very large building...`
- ❌ 抽象无物：`epic, awesome, masterpiece, best quality, 8k, ultra detailed`（这类 tag 对 Krea 2 基本无效，用具体描写替代）
- ❌ 尺度矛盾：既说"极高"又让整个物体完整入画且清晰 —— 要么让顶部出框，要么让它被大气吃掉
- ❌ 主体占比过小还写 `extreme close-up`
- ❌ 光源超过一个主光且没说明强弱关系
