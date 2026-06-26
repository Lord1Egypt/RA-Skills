---
name: novel-character-graph
description: "Professional long-form novel analysis and character relationship mapping + theme song generation. Automatically handles GBK/UTF-8 encoding, multi-GB file chunking, chapter-by-chapter incremental parsing, supports TXT/EPUB/PDF/DOCX novel formats. Outputs complete character system, relationship maps, worldviews, weapon/item systems, interactive visualization HTML, and AI-generated theme songs (Suno). Use when users ask for: novel analysis, character mapping, relationship graphs, worldview architecture, story timeline organization, manga/comic adaptation settings, novel theme song, ending song, OST."
tags: [novel, analysis, character, relationship, graph, xianxia, wuxia, fantasy, song, music]
triggers:
  - 小说分析
  - 人物图谱
  - 人物关系
  - 关系图谱
  - 世界观
  - 小说人物
  - 角色设定
  - 主题曲
  - 片头曲
  - 片尾曲
  - OST
  - 小说配乐
required_commands:
  - iconv
  - ebook-convert
  - pdftotext
  - pandoc
usage_hint: >
  当用户提到「小说分析」「人物图谱」「关系图」「世界观」「角色设定」时使用本skill。
  当用户提到「主题曲」「片头曲」「片尾曲」「OST」「配乐」时也使用本skill（可独立使用，
  不需要先做完整人物分析，直接基于用户描述的小说类型/情绪生成即可）。
---

# 小说人物图谱专业分析Skill + 主题曲生成

## 核心能力

本Skill专业处理百万字级长篇小说深度分析，解决大文件无法一次性解析的问题，并能为小说生成专属主题曲。

---

## 第一步：文件预处理流程

### 1.1 文件格式检测与编码修复

```bash
# 1. 检测文件基本信息
file -i <小说文件>
wc -l <小说文件>
ls -lh <小说文件>

# 2. 编码自动修复（中文小说90%为GBK编码）
cat <小说文件> | iconv -f GBK -t UTF-8 2>/dev/null > decoded.tmp && mv decoded.tmp <小说文件>_utf8.txt

# 3. 编码失败备选方案
iconv -f GB18030 -t UTF-8 <小说文件> 2>/dev/null
iconv -f BIG5 -t UTF-8 <小说文件> 2>/dev/null
```

### 1.2 支持的主流小说格式

| 格式 | 处理方法 | 依赖命令 |
|------|---------|---------|
| ✅ `.txt` | 直接分段读取 | - |
| ✅ `.epub` | `ebook-convert file.epub file.txt` | `calibre-bin` |
| ✅ `.pdf` | `pdftotext -layout file.pdf output.txt` | `poppler-utils` |
| ✅ `.docx` | `pandoc -s file.docx -o output.txt` | `pandoc` |
| ✅ `.mobi` | `ebook-convert file.mobi file.txt` | `calibre-bin` |

> 安装依赖：`sudo apt install calibre-bin poppler-utils pandoc`

---

## 第二步：大文件智能分段解析

### 2.1 分段策略（>10万行强制分段）

```
文件大小 < 500KB  → 一次性读取
500KB - 2MB → 分2-4段
2MB - 10MB → 每500行一段增量解析
> 10MB → 每1000行一段增量解析
```

### 2.2 分段读取Shell模板

```bash
# 分段读取命令模板
cat <小说文件> | head -n +500          # 第1段
cat <小说文件> | tail -n +501 | head -n 500  # 第2段
cat <小说文件> | tail -n +1001 | head -n 500 # 第3段
# ... 以此类推
```

### 2.3 每段解析核心提取项

每段必须提取并增量更新：
- ✅ 新出场人物全名 + 别名 + 外号
- ✅ 人物关系变化（敌对/盟友/情侣/师徒/血缘）
- ✅ 关键剧情节点 + 时间线推进
- ✅ 武功/功法/神器/丹药系统更新
- ✅ 势力阵营/宗门/国家变化
- ✅ 重要伏笔 + 世界观补全

---

## 第三步：人物体系标准化建模

### 3.1 人物层级分类体系

| 层级 | 定义标准 | 详细程度 |
|------|---------|---------|
| S级核心人物 | 主角团 + 最终BOSS + 关键导师 | 深度解析：性格/成长线/经典场景/漫画设定 |
| A级重要人物 | 主要反派 + 主要盟友 + 主要女主 | 完整人物卡 |
| B级次要人物 | 重要配角 + 各门派掌门 | 基础信息 + 立场 |
| C级NPC | 路人甲 + 一次性炮灰 | 只计数不展开 |

### 3.2 标准人物卡模板

```markdown
### 🎭 人物名称
- **身份**：详细身份定位
- **修为/境界**：
- **性格特质**：3-5个核心关键词
- **核心能力/功法**：
- **人物关系网**：
  - ❤️ 恋人：xxx
  - 👨‍🏫 师父：xxx
  - ⚔️ 死敌：xxx
  - 👬 兄弟：xxx
- **经典分镜/漫画设定**：
```

---

## 第四步：关系图谱构建规范

### 4.1 四大核心关系类型

使用标准Emoji统一标记：
| 关系类型 | Emoji标记 |
|---------|-----------|
| 爱情/道侣 | ❤️ 💕 |
| 师徒/传承 | 👨‍🏫 👩‍🏫 |
| 兄弟/战友 | 👬 🤝 |
| 血缘/家族 | 👨‍👩‍👧 |
| 敌对/死仇 | ⚔️ 💀 |
| 上下级/从属 | 👑 🛡️ |

### 4.2 ASCII关系总图规范

```
                    【核心主角】⭐
           ┌───────────┼───────────┐
        【女主1】💕  【兄弟】👬  【师父】👨‍🏫
           │           │           │
        家族线      战队线      功法线
```

---

## 第五步：输出交付标准

### 5.1 必须交付的三个文件

| 交付物 | 文件名 | 内容 |
|-------|--------|------|
| 1 | `《书名》_人物完整谱系.md` | 完整人物体系 + 势力架构 + 功法系统 + 时间线 |
| 2 | `《书名》_核心人物关系.md` | S级+A级人物深度解析 + 漫画分镜设定 |
| 3 | `index.html` | TailwindCSS + SVG交互式动态图谱网页 |

### 5.2 交互式网页标准组件

HTML页面必须包含4个标签页：
1. 🕸️ **关系图谱页** - SVG动态连线图
2. 👤 **人物介绍页** - 毛玻璃人物卡片
3. 🌍 **势力格局页** - 阵营分布 + 战力对比
4. 🎨 **漫画设定页** - 每人画风+色彩+经典分镜

---

## 第六步：质量检查清单

交付前必须验证：

✅ **编码正确** - 无乱码、无问号、无GBK残留
✅ **人物数量** - 长篇小说≥100人，中篇≥50人，短篇≥20人
✅ **无遗漏** - 女主/反派/导师/兄弟四大类完整
✅ **关系清晰** - 爱情/敌对/师徒/阵营四类关系无歧义
✅ **世界观** - 功法/境界/神器/丹药系统完整

---

## 第七步：主题曲生成（可选增值服务）

> 当用户要求生成主题曲、片头曲、片尾曲、OST、配乐时执行本节
> **注意**：主题曲功能可独立使用，不需要先做完整人物分析。
> 用户可以直接描述小说类型和想要的风格，跳过第一步到第六步直接到本节。

### 7.1 推荐主题供用户挑选

分析小说后，根据**类型/题材/情绪氛围**，从以下预设主题中推荐3-5个：

| 主题风格 | 适用场景 | 情绪关键词 |
|---------|---------|-----------|
| 🔥 **热血燃战** | 主角爆发、决战、逆袭 | 燃、热血、激昂、不屈 |
| 🌙 **古风柔情** | 爱情线、离别、思念 | 婉约、忧伤、唯美、深情 |
| ⚔️ **江湖侠气** | 武侠小说、门派争斗 | 豪迈、洒脱、义气、快意 |
| 🌌 **史诗宏大** | 世界观展示、神魔大战 | 庄严、壮阔、神秘、命运 |
| ❄️ **冰冽虐心** | 悲剧结局、失去、死亡 | 压抑、悲怆、孤独、破碎 |
| ☀️ **希望曙光** | 主角成长、胜利、重生 | 希望、温暖、崛起、救赎 |
| 🔮 **宿命轮回** | 穿越、系统、转生 | 轮回、命运、混沌、超脱 |
| 🌸 **青春校园** | 现代言情、校园恋爱 | 清新、甜蜜、悸动、纯真 |

**用户也可以自己指定主题风格**，直接进入7.2节。

### 7.2 Suno AI主题曲创作

根据小说内容构建Suno提示词：

#### Style字段公式

```
Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics
```

#### 小说主题曲Style参考模板

**🔥 热血燃战型**
```
Epic xianxia battle anthem, intense heroic atmosphere, ancient Chinese fantasy,
drums and erhu lead, male vocalist with powerful belting, orchestral percussion,
minor key with triumphant modulations, building from ominous intro to explosive chorus,
90BPM D minor
```

**🌙 古风柔情型**
```
Ancient Chinese romantic ballad, melancholic and ethereal, guqin and bamboo flute,
female vocalist with soulful nasally tone, sparse arrangement with gradual orchestral layers,
情感爆发点在副歌, Bb major 65BPM
```

**⚔️ 江湖侠气型**
```
Wuxia martial arts world soundtrack, bold and free-spirited, traditional Chinese instruments
pipa and dizi, male vocalist with raw gritty tone, rhythmic drums with folk elements,
outro fades to peaceful resolution, G minor 85BPM
```

**🌌 史诗宏大型**
```
Epic dark fantasy orchestral, divine and mysterious atmosphere, full symphonic orchestra
with choir, operatic male vocals with reverb, Gregorian chant elements,
命运感强烈, E minor 120BPM
```

#### Lyrics结构标签（写在歌词中）

```
[Intro] [Verse] [Pre-Chorus] [Chorus]
[Post-Chorus] [Bridge] [Interlude]
[Instrumental] [Outro]
```

#### 动态标签（描述演唱情绪）

| 标签 | 含义 |
|------|------|
| `[Powerful]` | 爆发力强 |
| `[Whispered]` | 低语诉说 |
| `[Soulful]` | 深情款款 |
| `[Gritty]` | 粗犷沙哑 |
| `[Falsetto]` | 假音飘渺 |
| `[Building Energy]` | 渐强递进 |
| `[Emotional Climax]` | 情感高潮 |

### 7.3 主题曲与视频合成

生成音频后，用ffmpeg合并视频：

```bash
# 方式一：6秒精华版（视频片段 + 歌曲开头）
ffmpeg -y -i <视频文件> -i <音频文件> \
  -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=5.5:d=0.5" \
  -c:v libx264 -c:a aac -shortest \
  <输出文件>

# 方式二：循环版（视频循环 + 歌曲完整版）
ffmpeg -y -stream_loop 9 -i <视频文件> -i <音频文件> \
  -vf "fade=t=in:st=0:d=1,fade=t=out:st=54:d=2" \
  -c:v libx264 -c:a aac -t <时长秒数> \
  <输出文件>
```

---

## 第八步：进阶脚本（可选）

> 以下脚本位于 `scripts/` 目录，执行前先验证环境，无需用户批准即可安装依赖。

`scripts/chapter_split.py` - 按章节智能分割大文件
`scripts/character_extract.py` - NLP辅助提取人名（中文分词）
`scripts/generate_html.py` - 自动生成交互式图谱页面

### 8.1 chapter_split.py（章节分割）

```python
#!/usr/bin/env python3
"""智能章节分割脚本 - 按章节将大文件分成多个小文件"""

import re
import os
import sys

def split_by_chapters(file_path, output_dir=None):
    """检测章节标题并分割文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 常见章节标题正则
    chapter_pattern = re.compile(
        r'^第[一二三四五六七八九十百千\d]+[章节卷部篇]\s*[：:]\s*.+$',
        re.MULTILINE
    )

    chapters = chapter_pattern.split(content)
    if len(chapters) <= 1:
        # 备选：简单按"第X章"分割
        chapter_pattern = re.compile(r'第[一二三四五六七八九十百千\d]+章')
        chapters = chapter_pattern.split(content)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = output_dir or os.path.dirname(file_path)

    for i, chapter_content in enumerate(chapters):
        if chapter_content.strip():
            output_path = os.path.join(output_dir, f"{base_name}_第{i+1}章.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(chapter_content.strip())
            print(f"OK: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chapter_split.py <novel.txt>")
        sys.exit(1)
    split_by_chapters(sys.argv[1])
```

### 8.2 character_extract.py（人名提取）

```python
#!/usr/bin/env python3
"""基于结巴分词的中文人名提取辅助工具"""

import re
import os
import sys

def extract_names(text, top_n=100):
    """提取文本中的中国人名（简单基于姓氏词典）"""
    # 常见姓氏
    surnames = r'[赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄穆萧尹姚邵堪汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯咎管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左右崔吉钮龚程嵇邢滑裴陆荣翁荀羊于惠甄曲面加羊舌微巢关蒯相查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷利段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟]'

    # 简单的人名匹配（姓氏+1-2个汉字）
    pattern = re.compile(rf'{surnames}[\u4e00-\u9fff]{{1,3}}')
    names = pattern.findall(text)

    # 去重并统计频率
    name_freq = {}
    for name in names:
        name_freq[name] = name_freq.get(name, 0) + 1

    sorted_names = sorted(name_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_names[:top_n]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python character_extract.py <novel.txt> [top_n]")
        sys.exit(1)

    file_path = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    names = extract_names(text, top_n)
    print(f"共提取到 {len(names)} 个人名：")
    for name, freq in names:
        print(f"  {name}: {freq}次")
```

### 8.3 generate_html.py（生成交互图谱）

```python
#!/usr/bin/env python3
"""自动生成交互式人物关系图谱HTML"""

import os
import sys

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '../assets/graph_template.html')

def generate_html(title, subtitle, characters, relationships, output_path='index.html'):
    """生成HTML图谱"""

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    # 填充标题
    template = template.replace('{{TITLE}}', title)
    template = template.replace('{{SUBTITLE}}', subtitle)

    # 生成人物卡片HTML
    cards_html = ''
    for char in characters:
        cards_html += f'''
        <div class="character-card bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50">
            <h3 class="text-xl font-bold text-orange-400 mb-2">{char['name']}</h3>
            <p class="text-gray-300 text-sm">{char.get('identity', '')}</p>
            <p class="text-gray-400 text-xs mt-2">修为：{char.get('realm', '未知')}</p>
        </div>
        '''

    # 替换占位符
    template = template.replace('<!-- CHARACTER_CARDS -->', cards_html)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"OK: {output_path}")

if __name__ == "__main__":
    print("Usage: from generate_html import generate_html")
    print("       generate_html('小说名', '副标题', characters_list, relationships_list)")
