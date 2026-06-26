# 音乐周报 — 完整工作流

> 所有路径均从 `~/.config/music-weekly/config.json` 读取。「配置」指代该 JSON 文件中的字段。

---

## 0. 初始化

**目标：** 加载历史记录，为查重做准备。

```python
# 读取历史 log
with open(CONFIG["history_log"]) as f:
    history = f.read()

# 提取所有「艺术家 - 专辑名」组合
# log 文件格式：
# 2026年第X周 X期 | 艺术家 - 专辑名 | 发行日期 | Apple Music ID | 推荐日期
import re
seen = set()
for line in history.split("\n"):
    m = re.match(r'\d{4}年第\w+周.*?\|\s*(.+?)\s*\|', line)
    if m:
        seen.add(m.group(1).strip())
# seen = {"NMIXX - Heavy Serenade", "Broken Social Scene - Remember The Humans", ...}
```

---

## 1. 搜索候选专辑

### 英语圈（2-3张候选）

| 来源 | 搜索方式 | 特点 |
|------|----------|------|
| **Pitchfork** | `site:pitchfork.com reviews album` | 有评分（BNM = 高分），编辑精选 |
| **Resident Advisor** | `site:ra.co reviews album` | 电子/舞曲为主 |
| **The Guardian** | `site:theguardian.com music album review` | 涵盖面广 |
| **NME** | `site:nme.com reviews album` | 摇滚/独立为主 |
| **AllMusic** | `site:allmusic.com album review` | 编辑评分，信息全 |
| **Stereogum** | `site:stereogum.com album review` | 独立/另类 |
| **Apple Music 编辑精选** | `music.apple.com` → 浏览→新专辑 | 主流+独立混合 |

**搜索关键词示例：**
```
new album review 2026 site:pitchfork.com
best new albums this week 2026
album review site:theguardian.com 2026
```

### 华语（最多1张候选）

| 来源 | 说明 |
|------|------|
| **落日广播 Sunset** | 微信公众号/Newsletter，华语独立音乐编辑推荐 |
| **11pond** | 影响乐评，华语专辑深度评论 |
| **街头噪声 StreetVoice** | 编辑策展频道，华语 Indie |
| **豆瓣音乐** | 编辑推荐板块 |
| **微博** | 关注 @呆若鹤、@眠座谈 等靠谱乐评人 |

**搜索关键词示例：**
```
2026年 专辑 乐评 site:douban.com
华语独立 专辑 推荐 2026
Chinese indie album review 2026
```

### 日韩（最多1张候选）

| 来源 | 说明 |
|------|------|
| **Real Sound** | 日本音乐新闻与评论 |
| **Natalie Japan** | 日本音乐艺能新闻 |
| **Billboard Japan** | 编辑推荐 |
| **Soompi / Allkpop** | K-Pop 编辑文章 |
| **Pitchfork Korea** | K-Pop 专业乐评 |

**搜索关键词示例：**
```
新譜 アルバム レビュー 2026
K-pop album review 2026 site:pitchfork.com
J-pop album 2026 review
```

### 拉丁/南美（0-1张候选）

| 来源 | 说明 |
|------|------|
| **Remezcla** | Latin 音乐编辑评论 |
| **Rolling Stone Latin** | 编辑推荐文章 |
| **NPR Music Latin** | NPR 旗下 Latin 音乐编辑策展 |

**搜索关键词示例：**
```
Latin album review 2026 site:remezcla.com
reggaeton album 2026 review
```

---

## 2. 筛选标准

每张候选专辑必须同时满足以下条件才能进入候选池：

| 条件 | 标准 | 检查方法 |
|------|------|----------|
| 发行时间 | 近1周内，最长不超过1个月 | 确认发行日期 |
| 评分 | **≥7.5**（优先 ≥8.0） | 查 Pitchfork / RYM / Metacritic / Apple Music / QQ音乐 / 网易云 |
| 评分真实性 | 必须来自真实平台，不得虚构 | 确认分数确实来自上述平台 |
| 地区符合 | 不违反地区比例规则 | 参考表格 |

### 多平台评分获取指南

| 平台 | 搜索方法 | 备注 |
|------|----------|------|
| Apple Music | 点开专辑页面查看 | 编辑评分 + 用户评分 |
| Pitchfork | `site:pitchfork.com "Album Name" review` | BNM 标签=高分 |
| RateYourMusic | `site:rateyourmusic.com "Album Name"` | 社区评分 |
| Metacritic | `site:metacritic.com "Album Name"` | 媒体综合分 |
| AllMusic | `site:allmusic.com "Album Name"` | 星评制（5星换算） |
| QQ音乐 | 直接搜 | 国内评分参考 |
| 网易云音乐 | 直接搜 | 国内评分参考 |

### 地区比例检查表

```
如果是周二（1期）：
  English: 2-3 | 华语: ≤1 | 日韩: ≤1 | 拉丁: ≤1
  华语+日韩 ≠ 同时出现

如果是周五（2期）：
  English: 2-3 | 华语: ≤1 | 日韩: ≤1 | 拉丁: ≤1
  华语+日韩 ≠ 同时出现
```

---

## 3. 查重（强制步骤）

每选一张候选专辑，必须执行：

```python
def is_duplicate(artist, album):
    return f"{artist} - {album}" in seen
```

**流程：**
1. 选一张候选 → 查 `seen` 集合
2. 有重复 → 直接丢弃，换下一个
3. 无重复 → 加入暂定列表
4. **最终5张锁定前，再做一次全量比对**
5. 确认0重复

> 注意：`seen` 集合包含**所有历史周次**的记录。不是只看本周。

---

## 4. 获取详细信息

每张专辑确认入选后，收集以下信息：

### 使用 iTunes API 获取

```python
from scripts.notion_utils import search_itunes, get_artwork_from_apple_link

info = search_itunes("Broken Social Scene", "Remember The Humans")
# 返回：
# {
#   "artist": "Broken Social Scene",
#   "album": "Remember The Humans",
#   "release_date": "2026-05-08",
#   "artwork_url": "https://is1-ssl.mzstatic.com/.../600x600bb.jpg",
#   "apple_music_url": "https://music.apple.com/us/album/remember-the-humans/1871484971?uo=4",
#   "track_count": 12,
#   "copyright": "℗ 2026 Arts & Crafts Productions Inc.",
#   "genre": "Alternative"
# }

# 从track_count判断专辑类型
album_type = "全长" if info["track_count"] >= 10 else "EP" if info["track_count"] >= 4 else "单曲"

# 从copyright提取厂牌
label = info["copyright"].replace("℗ ", "").strip()
```

### 多平台收集评分

```python
# 综合评分 = 各平台加权平均
# 权重建议：Pitchfork 30% + Apple Music 25% + Metacritic 25% + RYM 20%
# 若某平台找不到评分，其余平台等比例调整权重

# 示例：一张评分9.0的专辑
scores = [
    ("Pitchfork", 8.5, 0.30),
    ("Apple Music", 9.2, 0.25),
    ("Metacritic", 88, 0.25),   # 注意 Metacritic 是百分制
    ("RYM", 4.0, 0.20),          # RYM 5分制 → 换算为×2
]

# 换算到10分制
def to_10(name, score):
    if name == "Metacritic":
        return score / 10
    elif name == "RYM":
        return score * 2
    return score

overall = sum(to_10(n, s) * w for n, s, w in scores) / sum(w for _, _, w in scores)
# → 最终评分 ≈ 8.6（四舍五入到一位小数）
```

### 撰写推荐理由

推荐理由要求：
- **≥100字**
- 内容充实，避免模板化
- 每张专辑的描述要有独到见解
- 结构建议：1-2句介绍背景 → 1-2句音乐风格 → 1-2句突出亮点/推荐点

### 确定音乐分布地区标签

从 iTunes API 和专辑背景信息综合判断，使用 emoji+地区名格式：

| 地区 | 标签 |
|------|------|
| 美国 | `🇺🇸 美国` |
| 英国 | `🇬🇧 英国` |
| 加拿大 | `🇨🇦 加拿大` |
| 韩国 | `🇰🇷 韩国` |
| 日本 | `🇯🇵 日本` |
| 澳大利亚 | `🇦🇺 澳大利亚` |
| 中国 | `🇨🇳 中国` |

多地区专辑拆成多个标签（如合作专辑）。

---

## 5. 写入 Notion

```python
from scripts.notion_utils import create_record

# 准备所有字段
record = create_record({
    "名称": "Remember The Humans",
    "艺术家": "Broken Social Scene",
    "发行日期": "2026-05-08",
    "流派": "Indie Rock",
    "综合评分": 8.6,
    "收听状态": "未听",        # 默认值
    "专辑类型": "全长",
    "厂牌": "Arts & Crafts",
    "评论来源": "Pitchfork / AllMusic",  # 实际搜到的来源
    "推荐短语": "九年回归，从容沉淀的独立摇滚盛宴",
    "推荐理由": "加拿大独立摇滚天团Broken Social Scene时隔九年携第七张专辑回归...（100字以上）",
    "Apple Music链接": "https://music.apple.com/us/album/remember-the-humans/1871484971",
    "音乐分布": ["🇨🇦 加拿大"],
    "周次": "2026年第20周 2期",
    "推送日期": "2026-05-15",
    "封面URL": "https://is1-ssl.mzstatic.com/.../600x600bb.jpg",
})

if record and record.get("object") == "page":
    print(f"✅ 写入成功: Remember The Humans")
else:
    print(f"❌ 写入失败")
```

**写入全部5张后，验证一次：** 确认每个记录都已正确写入，特别是封面URL字段。

---

## 6. 推送消息

### 准备封面图

```python
import shutil

artwork_url = "https://is1-ssl.mzstatic.com/.../600x600bb.jpg"
local_path = f"{CONFIG['covers_dir']}/broken_social_scene_remember_the_humans.jpg"

# 下载封面
import urllib.request
urllib.request.urlretrieve(artwork_url, local_path)

# QQ Bot 需要复制到 media_dir
if CONFIG["delivery_channel"] == "qqbot":
    shutil.copy(local_path, f"{CONFIG['media_dir']}/broken_social_scene.jpg")
```

### 组装消息

```python
week_label = "2026年5月15日（第20周 2期）"
sender = CONFIG.get("sender_name", "🎵 音乐编辑")

intro = (
    f"{sender} | {week_label}\n\n"
    f"━━━━━━━━━━━━━━━━━━\n\n"
)

albums_text = ""
for i, album in enumerate(albums, 1):
    albums_text += (
        f"{i}️⃣ {album['artist']} — {album['album']}\n"
        f"📅 发行日期：{album['release_date']}\n"
        f"🏷️ {album['genre']}\n"
        f"⭐ 综合评分：{album['score']}/10\n"
        f"💬 {album['reason']}\n\n"
        f"Apple Music: {album['apple_link']}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
    )

summary = f"✨ 本周编辑精选 | {editor_pick}"
full_message = intro + albums_text + summary
```

### 发送

根据 `delivery_channel` 不同，发送方式有所不同：

**QQ Bot：**
```markdown
# 封面图用 <qqmedia> 标签嵌入消息体中
🎵 音乐编辑 | 2026年5月15日（第20周 2期）

<qqmedia>/root/.openclaw/media/qqbot/broken_social_scene.jpg</qqmedia>

1️⃣ Broken Social Scene — Remember The Humans
📅 发行日期：2026-05-08
...
```

**Telegram / Discord / Signal 等：**
```python
# 使用 message 工具的 media 参数
await message(
    action="send",
    channel=CONFIG["delivery_channel"],
    target=CONFIG["delivery_target"],
    message=text_only,
    media=local_cover_path,
)
```

**原则：** 封面图和文字必须在同一条消息，不要分开发。如果频道不支持合并发送，文字优先，随后单独发送图片并说明对应关系。

---

## 7. 追加到历史 log

```python
import datetime

entry = (
    f"{week_label} | {artist} - {album} | "
    f"{release_date} | {apple_music_id} | "
    f"{datetime.date.today().isoformat()}"
)

with open(CONFIG["history_log"], "a") as f:
    f.write(entry + "\n")
```

log 文件格式示例：
```
2026年第20周 2期 | Broken Social Scene - Remember The Humans | 2026-05-08 | 1871484971 | 2026-05-15
2026年第20周 2期 | NMIXX - Heavy Serenade - EP | 2026-05-11 | 1892154305 | 2026-05-15
```
