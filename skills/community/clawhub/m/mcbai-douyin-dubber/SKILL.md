---
name: douyin-dubber
description: >
  Auto-dub Douyin/TikTok videos into any language using a fully local pipeline:
  download with Playwright Chromium + Douyin cookie → transcribe with Whisper → translate subtitles with the AI agent →
  generate TTS (gTTS / Edge TTS / ElevenLabs) → timing stretch with FFmpeg atempo →
  mix original audio at 10% + new TTS voice → burn ASS subtitle overlay (positioned over original sub area).
  Use when: (1) dubbing/translating a Douyin or TikTok video, (2) replacing original voice with
  translated TTS, (3) any "tải video douyin rồi dịch/lồng tiếng" request.
metadata:
  openclaw:
    credentials:
      - id: douyin_cookie
        label: Douyin Session Cookie
        kind: file
        path: skills/douyin-dubber/douyin_cookies.txt
        env: DOUYIN_COOKIE_FILE
        required: true
        sensitive: true
        description: >
          Exported Douyin session cookie (header string format). Required for downloading videos.
          Never share this file — it grants access to your Douyin account.
          Recommend using a throwaway/test account. Rotate cookies after use.
      - id: elevenlabs_api_key
        label: ElevenLabs API Key
        kind: secret
        env: ELEVENLABS_API_KEY
        required: false
        sensitive: true
        description: >
          Optional. Only needed if you choose ElevenLabs TTS (highest quality).
          Free tier: 10,000 chars/month. Create a scoped key at https://elevenlabs.io.
    requires:
      bins:
        - ffmpeg
        - python
      python_packages:
        - playwright
        - openai-whisper
      optional_packages:
        - gtts
        - edge-tts
---

> 🚀 Developed by **[MCB AI](https://www.mcbai.vn)** · [YouTube](https://www.youtube.com/@mcbaivn) · [OpenClaw 101](https://openclaw.mcbai.vn/openclaw101)

# MCBAI Douyin Dubber

Full pipeline: Playwright download → Whisper transcribe → AI translate → TTS → FFmpeg ASS subtitle mix.

---

## ⚠️ Bảo Mật & Cookie

**Skill này chạy hoàn toàn local** — không upload video hay dữ liệu lên server nào ngoài các TTS provider bạn chọn.

### Credentials cần thiết

| Credential | Bắt buộc | Mô tả |
|-----------|----------|-------|
| `douyin_cookies.txt` | ✅ Có | Cookie Douyin để tải video |
| ElevenLabs API key | ❌ Không | Chỉ cần nếu chọn ElevenLabs TTS |

### Cookie Douyin — Lưu ý quan trọng

> ⚠️ **Cookie session = quyền truy cập tài khoản Douyin.** Không chia sẻ file này với ai.

**Khuyến nghị:**
- 🔐 Dùng **tài khoản throwaway/test** — không dùng tài khoản chính
- 📁 Lưu cookie vào `skills/douyin-dubber/douyin_cookies.txt` (local only, không commit lên git)
- ♻️ **Rotate cookie** sau khi dùng xong
- 🚫 Không paste cookie vào bất kỳ tool/website nào khác

**Override đường dẫn cookie bằng env var:**
```bash
# macOS / Linux
export DOUYIN_COOKIE_FILE=/path/to/your/cookies.txt

# Windows
$env:DOUYIN_COOKIE_FILE = "C:\your\path\cookies.txt"
```

---

## ⚙️ Cài Đặt (chỉ làm 1 lần)

### 1 — Python 3.11+

```bash
python --version   # Python 3.11.x hoặc cao hơn
```

> 💡 Tải tại https://www.python.org/downloads/ — tick **"Add Python to PATH"** khi cài

### 2 — Playwright Chromium

```bash
pip install playwright
python -m playwright install chromium
```

### 3 — Whisper

```bash
pip install openai-whisper
```

> ⚠️ Cần FFmpeg trên PATH — tải tại https://ffmpeg.org/download.html

### 4 — TTS Providers (cài theo nhu cầu)

#### Option 1: gTTS — Mặc định ✅
```bash
pip install gtts
```
- Miễn phí, không cần API key

#### Option 2: Edge TTS — Tự nhiên hơn, miễn phí
```bash
pip install edge-tts
```
- Giọng Microsoft Neural, tự nhiên hơn gTTS
- Giọng Việt: `vi-VN-HoaiMyNeural` (Nữ) / `vi-VN-NamMinhNeural` (Nam)

#### Option 3: ElevenLabs — Chất lượng cao nhất
- Không cần cài thêm package
- Cần API key từ https://elevenlabs.io (free: 10,000 ký tự/tháng)

### 5 — Cookie Douyin

Export cookies từ Chrome/Edge khi đang **đăng nhập Douyin**:

**Cách 1 — Extension EditThisCookie:**
1. Cài [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie) trên Chrome
2. Vào **www.douyin.com** → đăng nhập
3. Click icon extension → **Export** → chọn format **"Header String"**
4. Lưu vào file `douyin_cookies.txt` trong thư mục skill

**Cách 2 — DevTools (không cần extension):**
1. Vào **www.douyin.com** → đăng nhập → F12
2. Tab **Application** → **Cookies** → `www.douyin.com`
3. Copy: `sessionid`, `sid_tt`, `ttwid`, `uid_tt`, `odin_tt`
4. Ghép thành 1 dòng: `sessionid=xxx; sid_tt=yyy; ttwid=zzz; ...`
5. Lưu vào `douyin_cookies.txt`

> ⚠️ Cookie hết hạn sau ~60 ngày → export lại khi bị lỗi download

---

## 🚀 Chạy Pipeline

**Windows (PowerShell):**
```powershell
$env:PYTHONIOENCODING = "utf-8"
python skills/douyin-dubber/scripts/dubber.py `
  "https://www.douyin.com/video/XXXXX" `
  --lang Vietnamese `
  --outdir "./dubbed_output"
```

**macOS / Linux:**
```bash
PYTHONIOENCODING=utf-8 python skills/douyin-dubber/scripts/dubber.py \
  "https://www.douyin.com/video/XXXXX" \
  --lang Vietnamese \
  --outdir "./dubbed_output"
```

Script sẽ hỏi chọn TTS provider:

```
═══════════════════════════════════════════════════════
  🔊 CHỌN GIỌNG ĐỌC (TTS PROVIDER)
═══════════════════════════════════════════════════════

  1️⃣   gTTS  (Google TTS)          ← Mặc định
  2️⃣   ElevenLabs                  ← Chất lượng cao nhất
  3️⃣   Edge TTS (Microsoft Neural) ← Tự nhiên, miễn phí

  👉 Nhập 1, 2 hoặc 3 (mặc định = 1):
```

---

## 🔊 Chi Tiết TTS Providers

### Option 1: gTTS

| | |
|--|--|
| Chi phí | Miễn phí |
| Chất lượng | ⭐⭐ |
| API key | Không cần |

```bash
echo 1 | python dubber.py "URL" --lang Vietnamese --outdir "./output"
```

---

### Option 2: Edge TTS (Microsoft Neural)

| | |
|--|--|
| Chi phí | Miễn phí |
| Chất lượng | ⭐⭐⭐⭐ |
| API key | Không cần |

```bash
# Giọng nữ HoaiMy
echo "3\n1" | python dubber.py "URL" --lang Vietnamese --outdir "./output"

# Giọng nam NamMinh
echo "3\n2" | python dubber.py "URL" --lang Vietnamese --outdir "./output"
```

**Danh sách giọng Việt:**

| Voice ID | Giới tính | Phong cách |
|----------|-----------|------------|
| `vi-VN-HoaiMyNeural` | Nữ | Giọng Bắc, tự nhiên |
| `vi-VN-NamMinhNeural` | Nam | Giọng Bắc, trầm |

---

### Option 3: ElevenLabs

| | |
|--|--|
| Chi phí | 10k chars free/tháng |
| Chất lượng | ⭐⭐⭐⭐⭐ |
| API key | Bắt buộc |

**Giọng có sẵn:**

| # | Tên | Giới tính |
|---|-----|-----------|
| 1 | Rachel | Nữ |
| 2 | Bella | Nữ |
| 3 | Antoni | Nam |
| 4 | Josh | Nam |
| 5 | Arnold | Nam |
| 6 | Elli | Nữ |
| 7 | Custom | Nhập Voice ID |

**Lấy API key:**
1. Đăng ký tại https://elevenlabs.io
2. Vào **Profile → API Keys → Create API Key**
3. Tick permission **"Text to Speech"** ✅

---

## ⚡ Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `url` | required | Douyin/TikTok URL |
| `--lang` | Vietnamese | Target language |
| `--whisper-model` | medium | tiny/base/small/medium/large |
| `--outdir` | `.` | Output directory |
| `--original-vol` | 0.10 | Volume audio gốc (0–1) |
| `--skip-download` | — | Dùng video có sẵn |
| `--skip-transcribe` | — | Dùng SRT có sẵn |
| `--translated-srt` | — | Dùng SRT đã dịch |

---

## ⏭️ Skip Flags (Resume khi bị ngắt)

```bash
# Bỏ qua download
python dubber.py URL --skip-download ./work/original.mp4

# Bỏ qua transcribe
python dubber.py URL --skip-download video.mp4 --skip-transcribe original.srt

# Chỉ chạy TTS + mix
python dubber.py URL --skip-download video.mp4 --translated-srt translated.srt
```

---

## 📁 Output Structure

```
dubbed_output/
├── dubbed_original.mp4          ← Video output cuối cùng
└── dubber_work/
    ├── original.mp4             ← Video gốc
    ├── original.srt             ← Transcript (Whisper)
    ├── translated.srt           ← SRT đã dịch
    ├── subtitle.ass             ← ASS subtitle file
    ├── tts_track.mp3            ← TTS track hoàn chỉnh
    └── silence.mp3              ← Base silence track
```

---

## 🐛 Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|-----|-------------|-----|
| `UnicodeEncodeError` | Terminal không encode UTF-8 | Set `PYTHONIOENCODING=utf-8` |
| `No video URL found` | Cookie hết hạn | Export lại cookie từ browser |
| `401 Unauthorized` ElevenLabs | API key sai hoặc thiếu permission | Tạo key mới với permission TTS |
| `402 Payment Required` ElevenLabs | Hết credits | Nạp thêm hoặc dùng account khác |
| Edge TTS retry nhiều lần | Rate limit | Bình thường, script tự retry |
| ASS subtitle không hiển thị | Font path sai | Cần Arial font tại `/System/Library/Fonts` hoặc `C:/Windows/Fonts` |

---

## 📊 So Sánh TTS Providers

| | gTTS | Edge TTS | ElevenLabs |
|--|------|----------|------------|
| **Chi phí** | Miễn phí | Miễn phí | 10k chars free/tháng |
| **Chất lượng** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Tốc độ** | Nhanh | Chậm (rate limit) | Nhanh |
| **API key** | Không | Không | Có |
| **Tiếng Việt** | Tốt | Rất tốt | Xuất sắc |
| **Khuyến nghị** | Test nhanh | Dùng thường xuyên | Video quan trọng |

---

<p align="center">Made with ❤️ by <a href="https://www.mcbai.vn">MCB AI</a> &nbsp;·&nbsp; <a href="https://www.youtube.com/@mcbaivn">YouTube</a> &nbsp;·&nbsp; <a href="https://openclaw.mcbai.vn/openclaw101">OpenClaw 101</a></p>
