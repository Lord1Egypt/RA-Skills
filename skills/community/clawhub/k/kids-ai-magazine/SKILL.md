---
name: kids-ai-magazine
description: "Generate a kids-friendly AI news magazine with text and audio narration. Creates an interactive HTML magazine with stories adapted from real AI news for ages 3-6, featuring parent-child dialogues, TTS audio playback, illustrations, nursery rhymes, and quizzes. Use when asked to: create a kids or children AI magazine or newsletter, make AI news child-friendly or preschool-friendly, generate a parent-child reading experience about technology, produce an audio story about AI or robots for kids, build an educational web page about AI for young children. Triggers: kids magazine, children AI story, 儿童杂志, 学前, 亲子阅读, 给小朋友讲AI, 幼儿科普."
---

# Kids AI Magazine (学前亲子AI电子杂志)

Generate interactive HTML magazines that turn AI news into stories for 3-6 year olds, with TTS audio narration.

## Workflow

### 1. Collect News

Gather 3-5 current AI news items from reliable sources (36氪, 澎湃, TechCrunch, etc.). For each item, extract:
- Core fact (one sentence)
- Why it matters
- Source URL

### 2. Adapt Stories

Transform each news item into a kids story. Each story needs:

- **Title**: Fun, curiosity-driven (e.g., "机器人宝宝学走路啦！")
- **Paragraphs**: 2-3 short paragraphs, use analogies to things kids know (bikes, scissors, building blocks)
- **TTS text**: Pure Chinese narration text, no English words (replace "AI" → "智能技术", "GPU" → "芯片"), add verbal cues ("你知道吗？", "是不是很神奇呀？")
- **Parent-child dialogue**: 2 Q&A pairs (child asks naive question → parent gives educational answer)
- **Parent note**: Brief context for parents + source link
- **Icon**: One emoji per story

### 3. Generate Audio

Prerequisite: `pip3 install edge-tts`

```bash
python3 scripts/generate_audio.py --stories stories.json --voice zh-CN-XiaoxiaoNeural --output-dir ./output
```

Voices: `zh-CN-XiaoxiaoNeural` (女声, recommended), `zh-CN-YunxiNeural` (男声), `zh-CN-XiaoyiNeural` (女童声)

TTS text rules:
- No English words (TTS reads them letter by letter)
- Add pauses with commas and periods
- Use onomatopoeia: "噗通！摔倒啦！"
- Warm narrator tone: "小朋友们好呀～"

### 4. Build HTML

Use `assets/template.html` as the base. The template includes:
- Colorful header with rainbow gradient
- Story cards with embedded audio players
- Parent-child dialogue bubbles
- Activity section, nursery rhyme, quiz
- Mobile-responsive design

For custom builds: `python3 scripts/build_magazine.py --stories stories.json --template assets/template.html --output output/index.html`

### 5. Serve & Share

```bash
# Local preview
python3 -m http.server 8899 -d ./output

# Public sharing (install once: brew install cloudflared)
cloudflared tunnel --url http://localhost:8899
```

## Story JSON Format

See `references/example-stories.json` for a complete 3-story example. Key fields:

```json
{
  "title": "故事标题",
  "icon": "🤖",
  "paragraphs": ["HTML段落1", "段落2"],
  "tts_text": "纯中文朗读文本，无英文",
  "dialogue": [
    {"role": "child", "avatar": "👶", "text": "问题"},
    {"role": "parent", "avatar": "👩", "text": "回答"}
  ],
  "parent_note": "给家长的背景说明",
  "source_name": "来源名",
  "source_url": "https://..."
}
```

## Design Principles

1. **No scary content** — only positive, wonder-inspiring stories
2. **Analogy-first** — explain everything through things kids already know
3. **Emotion boundary** — always clarify: computers are smart but have no feelings
4. **Parent empowerment** — every story gives parents a conversation hook
5. **Audio-first** — assume kids can't read; audio must stand alone
