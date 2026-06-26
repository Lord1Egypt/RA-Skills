### 3.3 视频字幕提取（B站/抖音等）

视频中的口语是还原真实说话风格的**最佳素材**——书面体（微博/推文）和口语体（播客/访谈）差别巨大。

**为什么口语数据很重要？**

| 维度 | 书面体（微博） | 口语体（视频字幕） |
|------|--------------|------------------|
| 句长 | 50-200字长段 | 平均9字短句 |
| 口头禅 | 几乎不出现 | 高频出现（"这个""就是""然后"） |
| 语气 | 犀利、绝对 | 更温和、有余地（"其实""可能"） |
| 填充词 | 无 | 大量（"呃""嗯""那个"） |
| 句子完整度 | 完整 | 经常不完整就跳下一句 |

**采集优先级**：访谈/播客 > 直播回放 > 短视频独白 > Vlog

#### B站字幕提取（标准流程）

B站大部分视频有 AI 自动生成的中文字幕（`ai-zh`），通过 API 可直接获取文本。

**Step 1: 获取视频BV号列表**

如果知道UP主 mid：
```bash
# 用B站搜索API获取视频列表（不需要签名/cookie）
# duration=4 过滤60分钟以上长视频
curl -s "https://api.bilibili.com/x/web-interface/search/type?\
keyword={UP主名}+{关键词}&search_type=video&order=click&page=1&duration=4" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/"
```

从结果中筛选 `mid == 目标UP主mid` 的视频，提取 `bvid`。

> ⚠️ 空间视频列表API（`/x/space/wbi/arc/search`）需要 wbi 签名，即使 ManoBrowser `fetch_api` 也会返回 -403，不推荐。

**Step 2: 获取 aid/cid**

```bash
# view API（不需要cookie）
curl -s "https://api.bilibili.com/x/web-interface/view?bvid={BV号}" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/"
```

返回 `data.aid`、`data.cid`、`data.title`。

**Step 3: 获取字幕URL（需要cookie）**

```bash
# 通过 ManoBrowser fetch_api 调用（自动注入B站cookie）
fetch_api("https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}", "GET")
```

返回 `data.subtitle.subtitles[0].subtitle_url`（去掉 `//` 开头，加上 `https:`）。

> ⚠️ 不登录时 `subtitle.list` 为空数组！必须用 ManoBrowser `fetch_api` 带cookie请求。

> ⚠️ `fetch_api` 返回的是 OSS 链接，需要二次 `curl` 下载。

**Step 4: 下载字幕JSON**

```bash
curl -sL "https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/..." | \
  python3 -c "import json,sys; d=json.load(sys.stdin); \
  print('\n'.join(item['content'] for item in d['body']))"
```

字幕JSON结构：`{ "body": [{ "from": 秒, "to": 秒, "content": "文字" }, ...] }`

**批量提取脚本模式**：

```python
for bvid in bvids:
    # 1. curl view API → aid, cid
    # 2. fetch_api player/v2 → subtitle_url (OSS link → curl download)
    # 3. curl subtitle_url → parse body[].content
    # 4. 保存 /tmp/{target}_subs/{bvid}.txt
    time.sleep(1)  # 避免限流
```

**已知限制**：
- 部分视频无AI字幕（返回 `subtitles: []`），跳过即可
- 多P视频只获取第一P的字幕（cid对应第一P）
- 对话类视频无法区分发言人（AI字幕不标注说话人）
- `fetch_api` 返回的OSS链接偶尔为空，重试一次通常可解决

#### 抖音视频文字提取（Whisper 语音识别）

抖音**没有字幕API**（xgplayer 字幕按钮只有"不开启"选项，正片和切片都没有）。唯一可行路径：**下载视频 → 提取音频 → Whisper 本地语音转文字**。

**前置依赖**：
```bash
brew install ffmpeg
python3.12 -m pip install --break-system-packages openai-whisper
```

**Step 1: 获取视频列表**

用 ManoBrowser 打开创作者主页，从交互元素中提取视频ID：
```python
# 搜索用户
chrome_navigate("https://www.douyin.com/search/{用户名}?type=user")
# 从结果中找到目标用户的 sec_uid
# 打开主页
chrome_navigate("https://www.douyin.com/user/{sec_uid}")
# 获取视频ID
chrome_get_interactive_elements(tabId)
# 从 href 中提取 /video/{id} 的 id
```

**Step 2: 获取视频播放直链**

```python
# 打开视频页面
chrome_navigate(f"https://www.douyin.com/video/{video_id}")
# 等待5秒加载
time.sleep(5)
# 从 <video> 标签获取播放URL
chrome_execute_script(tabId, "MAIN",
    "() => { const v = document.querySelector('video'); return v ? (v.currentSrc || v.src || '') : ''; }")
# 返回类似: https://v26-web.douyinvod.com/...
```

> ⚠️ 播放URL有时效性（约2小时），获取后尽快下载。

**Step 3: 下载视频 + 提取音频**

```bash
# 下载视频（必须带 Referer）
curl -sL "{video_url}" -o video.mp4 \
  -H "Referer: https://www.douyin.com/" -H "User-Agent: Mozilla/5.0"

# ffmpeg 提取音频
ffmpeg -i video.mp4 -vn -acodec libmp3lame -q:a 4 audio.mp3 -y

# 删除视频节省空间
rm video.mp4
```

**Step 4: Whisper 语音转文字**

```python
import whisper

model = whisper.load_model("base")  # base够用，medium更准
result = model.transcribe("audio.mp3", language="zh")
text = result['text']  # 纯文字，无标点分段
```

**批量处理脚本模式**：

```python
model = whisper.load_model("base")  # 只加载一次

for video_id in video_ids:
    # 1. ManoBrowser 打开视频页 → 获取 currentSrc
    # 2. curl 下载 MP4
    # 3. ffmpeg 提取 MP3
    # 4. model.transcribe(mp3, language="zh")
    # 5. 保存文字到 /tmp/{target}_subs/{video_id}.txt
    # 6. 关闭 ManoBrowser tab
    time.sleep(1)
```

**性能参考（Apple Silicon M系列芯片）**：
| 模型 | 加载时间 | 1分钟音频 | 准确度 |
|------|---------|---------|-------|
| base | 0.5s（已缓存） | ~2s | ⭐⭐⭐ 口语内容准确，部分同音字错误 |
| medium | ~5s | ~8s | ⭐⭐⭐⭐ 专有名词更准 |
| large | ~15s | ~25s | ⭐⭐⭐⭐⭐ 最准但慢 |

**已知限制**：
- Whisper `base` 模型会产生同音字错误（如"影视飓风"→"影视剧方"、"刘谦"→"刘强"）
- 无标点、无分段——输出是连续文字流
- 对话类视频无法区分说话人
- 正片视频（3-4小时）下载超时，建议只处理切片视频
- 偶尔出现繁体字混入
- 首次运行需下载模型（base ~140MB）

**建议**：切片短视频用 Whisper，正片/长视频优先用 B站字幕API（更快更准）。

#### YouTube 字幕提取

YouTube 搬运视频通常有自动字幕，但获取有门槛：

**方案A：youtube-transcript-api（推荐，需代理）**
```bash
pip install youtube-transcript-api
```
```python
from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
transcript = ytt.fetch(video_id, languages=['zh-Hans', 'zh'])
text = ' '.join(s.text for s in transcript.snippets)
```
> ⚠️ YouTube 会封禁云服务器IP，本地运行+代理才行。

**方案B：yt-dlp + cookie**
```bash
yt-dlp --cookies-from-browser chrome --proxy http://127.0.0.1:7897 \
  --write-auto-subs --sub-langs "zh.*" --skip-download -o "%(id)s" "{URL}"
```
> ⚠️ macOS Chrome cookie 加密，`--cookies-from-browser` 可能读不到。

**方案C：ManoBrowser fetch_api + innertube API**

通过 ManoBrowser 的 `fetch_api` 调用 YouTube innertube player API 获取字幕track URL，但需要有效的登录session。目前不稳定，不推荐。

**方案D：Whisper 兜底**

如果以上都失败，用与抖音相同的 Whisper 路径：yt-dlp 下载音频 → Whisper 转文字。

#### 口语风格分析方法

字幕提取完成后，合并所有文本进行统计分析：

```python
import re
from collections import Counter

# 高频词/口头禅统计
patterns = {
    '就是': r'就是', '然后': r'然后', '这个': r'这个',
    '那个': r'那个', '其实': r'其实', '对': r'对',
    '嗯': r'嗯', '呃': r'呃', '特别': r'特别',
    '可能': r'可能', '反正': r'反正', '确实': r'确实',
    '我觉得': r'我觉得', '怎么说呢': r'怎么说呢',
}
for word, pat in sorted(patterns.items(), key=lambda x: -len(re.findall(x[1], text))):
    count = len(re.findall(pat, text))
    per_1k = count / (len(text)/1000)
    print(f"{word}: {count}次 ({per_1k:.1f}/千字)")

# 句式分析
lines = [l.strip() for l in text.split('\n') if l.strip()]
avg_len = sum(len(l) for l in lines) / len(lines)
short_pct = sum(1 for l in lines if len(l) <= 5) / len(lines)
```

**分析维度**：
- 口头禅频率排行（次/千字）
- 平均句长（区分口语碎片化程度）
- 短句(≤5字)/中句(6-20字)/长句(>20字) 比例
- 语气词使用偏好
- 疑问/反问句比例
- 有特色的表达片段（作为 MENTOR.md 示例）

**将分析结果写入 MENTOR.md**：
- 口头禅频率 TOP 5 作为说话风格规则
- 平均句长指导输出长度
- 典型片段作为示例对话
- 书面 vs 口语差异作为风格切换指导

