# 曲风库与演唱描述规范（music-style）

写"曲风卡"前的必读参考。目标：让一个没听过这首歌的人，读完曲风卡就能在脑内"预演"整首歌。

---

## 一、新民谣子流派选型表

| 子流派 | 气质 | 参考艺人 | 适用母题 |
|--------|------|----------|----------|
| 城市叙事民谣 | 烟火气、白描、市井 | 赵雷、毛不易、宋冬野 | 乡愁、时代浮沉 |
| 校园/清新民谣 | 干净、轻盈、少年感 | 好妹妹乐队、房东的猫、谢春花 | 青春、怀人 |
| 山野古风新编 | 意象浓、戏感、灵动 | 谢春花《盗将行》、花粥、陈鸿宇 | 江湖退隐、失意自渡 |
| 悲怆大民谣 | 沉郁、史诗、长线条 | 马頔《南山南》、低苦艾、万能青年旅店(跨界) | 爱别离、时代浮沉 |
| 禅意/文人民谣 | 留白、气声、器乐克制 | 周云蓬、万能青年旅店、程璧 | 禅意放下、怀人 |
| 民谣摇滚 | 递进爆发、鼓组驱动 | 朴树、许巍、痛仰 | 失意自渡、时代批判 |

选型逻辑：按诗词**情感内核**选流派，按**演唱形式**微调——对唱优先校园/古风新编，独白优先禅意/悲怆，组诗专辑建议混搭 2–3 个流派形成版图。

---

## 二、曲风卡五要素写法

### 1. 风格定位
一句话格式：`新民谣（子流派）× 情绪关键词，参考风格：艺人A / 艺人B`。
例："新民谣 / 古风新编，唯美而略带忧伤，参考风格：谢春花 / 花粥"。

### 2. BPM 与律动
- 慢板抒情 62–76（如悼亡、禅意）；中板叙事 78–92（默认，如《梦压星河》BPM 88）；民谣摇滚 96–120。
- 必须补一句律动描述："舒缓摇摆，适合木吉他扫弦配大提琴""三拍子摇曳，似舟行水上"。

### 3. 配器清单（分层写）
- **根基层**：木吉他（分解和弦/扫弦，写明何时转换）
- **古意层**（至少 2 件）：竹笛、箫、古筝、二胡、琵琶、木鱼、编钟、寺钟
- **氛围层**：雨声、水声、木桨划水、风声、市井叫卖、人声嘈杂采样
- **点缀层**：铃铛、铃铎、大提琴、口琴、手鼓
- **动态提示**：写明各段进出——"前奏纯木吉他，间奏加入手鼓与古筝对答，尾声只剩一把木吉他+一声水滴回响"

### 4. 演唱指令（声部×段落矩阵）
- **音色**：男声（清冷克制 / 沙哑沧桑 / 温厚叙事）；女声（空灵如烟 / 清亮干净 / 慵懒气声）
- **段落处理**：主歌叙事低吟（近麦、气声多）→ 预副歌渐强 → 副歌开阔深情（真声推开）→ 桥段收回来（半白半唱）→ 终段副歌升 Key（半音或全音）→ 尾声气声渐弱
- **对唱和声**：何处齐唱、何处三度和声、何处轮唱交叠，逐一标注

### 5. 情绪曲线（一句话）
"从落第失意 → 江畔守候 → 钟声点化 → 归于心安"——四个坐标点对应四个结构段，必须与歌词情感递进吻合。

---

## 三、AI 音乐工具 Prompt 写法（Suno 类）

### Style Prompt（英文，一段式，≤200 词）
模板：
```
[Subgenre] folk ballad, [tempo] BPM, [key if known], male/female/duet vocals,
acoustic guitar [strumming/fingerpicking], [Chinese instruments: bamboo flute, guzheng, erhu, temple bell],
[ambience: rain, water, market sounds], [mood adjectives], verse intimate low-register,
chorus soaring emotional, bridge stripped-back spoken-word feel, final chorus key change up,
outro fading with [sound effect]
```
示例：
```
Chinese folk ballad, 82 BPM, duet male & female vocals, fingerpicked acoustic guitar,
bamboo flute and temple bell, subtle river water ambience, melancholic yet serene,
intimate storytelling verses, soaring unison chorus, bridge spoken dialogue over single guitar,
final chorus modulated up with stacked harmonies, outro fades with a single water drop echo
```

### 歌词文本格式（带 meta 标签）
```lyrics
[Intro]
(配器/氛围可写进 Style，此处留白或写音效提示)

[Verse 1]
歌词逐行…

[Pre-Chorus]
…

[Chorus]
…

[Interlude]

[Verse 2]
…

[Bridge]
(spkoken/duet 标注)

[Final Chorus] (higher key)

[Outro]
(whispered) 尾句…
```
注意：中文歌词直接填入；演唱角色用 `(male:)` `(female:)` `(both:)` 行内标注；升调用 `[Final Chorus - higher key]`。

---

## 四、编曲小抄（诗词→配器直觉映射）

| 诗词意象 | 配器直觉 |
|----------|----------|
| 江/湖/舟/渡口 | 水声采样、木桨声、箫、三拍子律动 |
| 寺/钟/僧/禅 | 木鱼、寺钟、铃铎、留白式编曲 |
| 雪/霜/秋/雁 | 弦乐长音、二胡、慢板 |
| 酒/宴/灯市 | 手鼓、古筝轮指、市井采样 |
| 剑/马/边塞 | 民谣摇滚、鼓组、琵琶轮扫 |
| 月/夜/相思 | 指弹木吉他、口琴、气声唱法 |

---

## 五、曲风卡交付模板

```
【曲风卡】
风格定位：新民谣 / 古风新编 —— 唯美而略带忧伤（参考：谢春花 / 花粥）
BPM 律动：82，舒缓摇摆，似舟行水上
配器清单：
  根基层 – 木吉他（前奏分解和弦，副歌转扫弦）
  古意层 – 竹笛（前奏主旋律）、寺钟（间奏一声）、古筝（间奏对答）
  氛围层 – 轻微水声与木桨声贯穿
  点缀层 – 大提琴长音（终段副歌垫底）
演唱指令：男声清冷克制（落第书生）；女声空灵如烟（江水化身）；
  主歌低吟近麦，副歌合唱推开，Bridge 半白半唱交叠，终段升全音，
  尾声气声各一句+合声收束
情绪曲线：失意 → 相遇 → 点化 → 心安
AI Prompt：（附英文 style prompt + 带标签歌词文本）
```
