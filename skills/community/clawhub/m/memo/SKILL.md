---
name: senseaudio-voice-memo-transcriber
description: Transcribe and organize voice memos with automatic categorization and information extraction. Use when users have voice notes, audio memos, or spoken notes to convert to structured text.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Voice Memo Transcriber

Transform voice memos into organized, searchable text with automatic categorization and key information extraction.

## What This Skill Does

- Transcribe voice memos to text with high accuracy
- Convert casual speech to structured written format
- Extract key information (dates, tasks, contacts)
- Organize memos by topic or category
- Generate summaries and action items

## Prerequisites

Install required Python packages:

```bash
pip install requests
```


## Implementation Guide

### Step 1: Transcribe Voice Memo

```python
import requests

def transcribe_voice_memo(audio_file):
    url = "https://api.senseaudio.cn/v1/audio/transcriptions"

    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"file": open(audio_file, "rb")}
    data = {
        "model": "sense-asr",  # Standard model: full features, good for voice memos
        "response_format": "json"
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()["text"]
```

### Step 2: Clean and Structure Text

Convert casual speech to readable text:

```python
import re

def clean_transcription(text):
    # Remove filler words
    fillers = ["um", "uh", "like", "you know", "basically", "actually"]
    for filler in fillers:
        text = re.sub(rf'\b{filler}\b', '', text, flags=re.IGNORECASE)

    # Fix spacing
    text = re.sub(r'\s+', ' ', text).strip()

    # Capitalize sentences
    sentences = text.split('. ')
    text = '. '.join(s.capitalize() for s in sentences)

    return text
```

### Step 3: Extract Key Information

```python
import re
from datetime import datetime

def extract_info(text):
    info = {
        "dates": [],
        "tasks": [],
        "contacts": [],
        "keywords": []
    }

    # Extract dates
    date_patterns = [
        r'\b(?:tomorrow|today|yesterday)\b',
        r'\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b'
    ]
    for pattern in date_patterns:
        info["dates"].extend(re.findall(pattern, text, re.IGNORECASE))

    # Extract tasks (action verbs)
    task_patterns = [
        r'(?:need to|have to|must|should)\s+(\w+(?:\s+\w+){0,5})',
        r'(?:remember to|don\'t forget to)\s+(\w+(?:\s+\w+){0,5})'
    ]
    for pattern in task_patterns:
        info["tasks"].extend(re.findall(pattern, text, re.IGNORECASE))

    # Extract names (capitalized words)
    info["contacts"] = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)

    return info
```

### Step 4: Categorize Memo

```python
def categorize_memo(text):
    categories = {
        "work": ["meeting", "project", "deadline", "client", "email"],
        "personal": ["family", "friend", "home", "weekend"],
        "shopping": ["buy", "purchase", "store", "grocery"],
        "ideas": ["idea", "think", "maybe", "could"],
        "tasks": ["todo", "task", "need to", "must"]
    }

    text_lower = text.lower()
    scores = {}

    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[category] = score

    return max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
```

### Step 5: Generate Structured Output

```python
def process_voice_memo(audio_file):
    # Transcribe
    raw_text = transcribe_voice_memo(audio_file)

    # Clean
    clean_text = clean_transcription(raw_text)

    # Extract info
    info = extract_info(clean_text)

    # Categorize
    category = categorize_memo(clean_text)

    # Create structured memo
    memo = {
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "text": clean_text,
        "raw_text": raw_text,
        "extracted_info": info,
        "summary": generate_summary(clean_text)
    }

    return memo

def generate_summary(text):
    # Use first sentence or first 100 chars
    sentences = text.split('. ')
    return sentences[0] if sentences else text[:100]
```

## Advanced Features

### Batch Processing

Process multiple memos:

```python
def process_memo_batch(audio_files):
    memos = []
    for audio_file in audio_files:
        memo = process_voice_memo(audio_file)
        memos.append(memo)

    # Group by category
    by_category = {}
    for memo in memos:
        category = memo["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(memo)

    return by_category
```

### Search and Filter

```python
def search_memos(memos, query):
    results = []
    query_lower = query.lower()

    for memo in memos:
        if query_lower in memo["text"].lower():
            results.append(memo)

    return results

def filter_by_date(memos, date):
    return [m for m in memos if date in m["extracted_info"]["dates"]]
```

### Export Formats

```python
def export_to_markdown(memos):
    md = "# Voice Memos\n\n"

    for memo in memos:
        md += f"## {memo['timestamp']}\n"
        md += f"**Category**: {memo['category']}\n\n"
        md += f"{memo['text']}\n\n"

        if memo['extracted_info']['tasks']:
            md += "**Tasks**:\n"
            for task in memo['extracted_info']['tasks']:
                md += f"- [ ] {task}\n"
            md += "\n"

    return md
```

## Output Format

- Cleaned transcription text
- Structured memo JSON
- Extracted information (dates, tasks, contacts)
- Category classification
- Summary

## Tips for Best Results

- Speak clearly and at normal pace
- Mention dates and names explicitly
- Use action verbs for tasks
- Keep memos under 5 minutes for best results
- Review and edit extracted information

## Reference

- [SenseAudio ASR API](https://senseaudio.cn/docs/speech_recognition/http_api)
- [SenseAudio Platform](https://senseaudio.cn)
