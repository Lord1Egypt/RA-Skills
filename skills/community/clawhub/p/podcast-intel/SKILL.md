---
name: podcast-intel
description: >
  Podcast intelligence engine. Transcribes, segments, summarizes, and scores
  podcast episodes from RSS feeds. Generates "worth your time" recommendations
  with cross-source deduplication and maintains a local consumption diary.
  
  Use this skill when the user asks about podcasts, wants podcast recommendations,
  says "what podcasts should I listen to", "podcast briefing", "what's worth
  listening to", "podcast summary", "summarize this podcast", "podcast diary",
  "what did I listen to", or any request involving podcast content analysis.
  
  Also activates for: "brief me on podcasts", "podcast recap", "new episodes",
  "what's new from [podcast name]", "is this episode worth it".

metadata:
  openclaw:
    emoji: "🎧"
    primaryEnv: "OPENAI_API_KEY"
    requires:
      bins: ["python3", "ffmpeg"]
      env:
        - OPENAI_API_KEY
      optionalEnv:
        - WHISPER_MODEL
        - PODCAST_INTEL_FEEDS
        - PODCAST_INTEL_INTERESTS

tools:
  - name: podcast_briefing
    description: >
      Full intelligence pipeline: fetch new episodes from configured feeds,
      transcribe audio, segment by topic, analyze against user interests,
      and generate ranked "worth your time" recommendations.
      Appends to local consumption diary.
    command: "cd {baseDir} && python3 scripts/main.py"
    args:
      - name: hours
        type: number
        description: "Look back this many hours for new episodes (default: 168 = 7 days)"
        default: 168
      - name: top
        type: number
        description: "Return only the top N ranked recommendations (default: 10)"
        default: 10
      - name: output
        type: string
        description: "Output format: json, markdown, or tts (default: markdown)"
        default: markdown
        options: ["json", "markdown", "tts"]
      - name: dry_run
        type: boolean
        description: "Analyze episodes but don't write to diary"
        default: false
    category: "podcast"
    requiredEnv: ["OPENAI_API_KEY"]

  - name: podcast_analyze
    description: >
      Analyze a specific podcast episode by URL.
      Transcribes, segments, scores relevance and novelty against your interests.
    command: "cd {baseDir} && python3 scripts/main.py"
    args:
      - name: episode_url
        type: string
        description: "Direct URL to podcast audio file or RSS feed entry URL"
        required: true
      - name: show_name
        type: string
        description: "Name of the podcast show (optional, for context)"
      - name: output
        type: string
        description: "Output format: json or markdown"
        default: markdown
        options: ["json", "markdown"]
    category: "podcast"
    requiredEnv: ["OPENAI_API_KEY"]

  - name: podcast_diary
    description: >
      Display your podcast consumption diary — a structured log of episodes
      you've been briefed on, topics covered, and recommendations.
    command: "cd {baseDir} && python3 scripts/diary.py"
    args:
      - name: show
        type: boolean
        description: "Display diary entries"
        default: true
      - name: last
        type: number
        description: "Show entries from the last N days (default: 7)"
        default: 7
      - name: format
        type: string
        description: "Output format: json or markdown"
        default: markdown
        options: ["json", "markdown"]
    category: "podcast"

  - name: podcast_recommend
    description: >
      Quick recommendations from already-transcribed episodes.
      No new transcription — uses cached transcripts and instant scoring.
    command: "cd {baseDir} && python3 scripts/main.py"
    args:
      - name: top
        type: number
        description: "Return only the top N ranked recommendations"
        default: 5
      - name: recommend_only
        type: boolean
        description: "Skip transcription, use cache only"
        default: true
      - name: output
        type: string
        description: "Output format: json or markdown"
        default: markdown
        options: ["json", "markdown"]
    category: "podcast"
    requiredEnv: ["OPENAI_API_KEY"]
