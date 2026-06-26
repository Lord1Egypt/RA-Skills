# PPT Translation Tool - Technical Reference

## Architecture Overview

The translation pipeline consists of four main stages using an OpenAI-compatible LLM API:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  1. Extraction  │───▶│  2. Batching    │───▶│  3. Translation │───▶│  4. Application │
│                 │    │                 │    │                 │    │                 │
│ - Parse PPTX    │    │ - Collect text  │    │ - OpenAI API    │    │ - Replace text  │
│ - Recurse shapes│    │ - Filter CJK    │    │ - Retry logic   │    │ - Adjust fonts  │
│ - Extract runs  │    │ - Batch by size │    │ - Map responses │    │ - Resize boxes  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

The tool uses the standard OpenAI-compatible `/v1/chat/completions` API endpoint, enabling compatibility with:
- **Qoderwork** built-in models
- **Ollama** (via its OpenAI-compatible endpoint at `/v1`)
- **OpenAI** API
- **DeepSeek** and other cloud providers
- Any other OpenAI-compatible LLM service

## Text Extraction

### Shape Hierarchy Traversal

The PPTX structure follows a hierarchical model:

```
Presentation
└── Slides[]
    ├── Slide
    │   ├── Shapes[]
    │   │   ├── Shape (with text_frame)
    │   │   ├── GroupShape
    │   │   │   └── Shapes[] (recursive)
    │   │   ├── Table
    │   │   │   └── Rows[]
    │   │   │       └── Cells[]
    │   │   │           └── TextFrame
    │   │   └── Picture/Chart/Media (skip)
    │   └── NotesSlide (optional)
    │       └── NotesTextFrame
```

### Extraction Algorithm

```python
def extract_texts(shape, path=""):
    texts = []
    
    if shape.has_text_frame:
        for para_idx, para in enumerate(shape.text_frame.paragraphs):
            for run_idx, run in enumerate(para.runs):
                texts.append({
                    "text": run.text,
                    "path": path,
                    "para_idx": para_idx,
                    "run_idx": run_idx,
                    "font": run.font
                })
    
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        for child_idx, child in enumerate(shape.shapes):
            texts.extend(extract_texts(child, f"{path}/group[{child_idx}]"))
    
    if shape.has_table:
        for row_idx, row in enumerate(shape.table.rows):
            for col_idx, cell in enumerate(row.cells):
                texts.extend(extract_texts(
                    cell, 
                    f"{path}/table[{row_idx},{col_idx}]"
                ))
    
    return texts
```

## Grouped Shapes and Tables

### Grouped Shapes (GroupShape)

GroupShapes contain nested shapes that must be processed recursively:

- Access via `shape.shapes` iterator
- Each child shape maintains its own coordinate system relative to the group
- Text frames within grouped shapes are processed identically to top-level shapes
- Groups can be nested (groups within groups)

### Tables

Tables require cell-by-cell processing:

```python
for row in table.rows:
    for cell in row.cells:
        # Each cell has a text_frame
        process_text_frame(cell.text_frame)
        # Enable word wrap for English text
        cell.text_frame.word_wrap = True
```

- Table structure (rows/columns) is preserved
- Cell formatting (borders, fill) is preserved
- Only text content within cells is translated

## Translation Batching Strategy

### Text Collection Phase

1. Traverse all slides and shapes
2. Collect text segments with metadata:
   - Original text
   - Slide index
   - Shape path (for reconstruction)
   - Paragraph and run indices
   - Font properties

3. Filter segments:
   - Skip empty strings
   - Skip pure ASCII/alphanumeric (no Chinese)
   - Use CJK Unicode range detection:
     - U+4E00-U+9FFF (CJK Unified Ideographs)
     - U+3400-U+4DBF (CJK Extension A)
     - U+F900-U+FAFF (CJK Compatibility Ideographs)

### Batch Translation

```python
# Group segments into batches
def create_batches(segments, batch_size=20):
    for i in range(0, len(segments), batch_size):
        yield segments[i:i + batch_size]

# Translate batch using OpenAI-compatible API
def translate_batch(batch, model, api_base, api_key=None):
    texts = [s["text"] for s in batch]
    numbered_texts = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))

    url = f"{api_base}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Translate the following {len(texts)} Chinese text segments to English. Return ONLY the translations, one per line:\n\n{numbered_texts}"}
        ],
        "temperature": 0.3,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(url, json=payload, headers=headers, timeout=120)
    response.raise_for_status()
    result = response.json()
    translated_text = result["choices"][0]["message"]["content"]

    # Parse numbered response
    translations = parse_numbered_response(translated_text, len(batch))
    return translations
```

### Response Mapping

Translations are mapped back using the stored metadata:

```python
for segment, translation in zip(batch, translations):
    slide = prs.slides[segment["slide_idx"]]
    shape = locate_shape(slide, segment["path"])
    run = shape.text_frame.paragraphs[segment["para_idx"]].runs[segment["run_idx"]]
    run.text = translation
```

## Font Replacement Logic

### CJK Font Detection

```python
CJK_FONTS = {
    'SimSun', '宋体',
    'SimHei', '黑体',
    'Microsoft YaHei', '微软雅黑',
    'KaiTi', '楷体',
    'FangSong', '仿宋',
    'STSong', 'STHeiti', 'STKaiti', 'STFangsong',
    'NSimSun', '新宋体',
    'PMingLiU', 'MingLiU',
    'DengXian', '等线',
    'Source Han Sans', 'Noto Sans CJK',
}

def is_cjk_font(font_name):
    if not font_name:
        return True  # Default to replacing unset fonts
    return font_name in CJK_FONTS or any(
        cjk in font_name.lower() 
        for cjk in ['song', 'hei', 'kai', 'fang', 'ming', 'gothic', 'yuan']
    )
```

### Font Replacement Rules

1. **Title Detection:**
   Shapes are detected as titles using the placeholder type:
   ```python
   from pptx.enum.shapes import PP_PLACEHOLDER
   
   def is_title_shape(shape) -> bool:
       ph = getattr(shape, "placeholder_format", None)
       if ph is None:
           return False
       try:
           return ph.type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE, PP_PLACEHOLDER.SUBTITLE)
       except Exception:
           return False
   ```

2. **Replacement:**
   ```python
   if is_cjk_font(run.font.name):
       run.font.name = target_font  # Calibri
       if segment.is_bold or is_title:
           run.font.bold = True
   
   # Title placeholders always get bold Calibri
   if is_title:
       run.font.name = target_font
       run.font.bold = True
   ```

3. **Preservation:**
   - Font size (unless auto-resize needed)
   - Color (RGB, theme color)
   - Bold/italic/underline/strikethrough (for non-title text)
   - Hyperlink URL

## Text Box Auto-Resize Algorithm

### Overflow Detection

English text is typically 1.3-1.8x longer than Chinese. The auto-resize is triggered when:

```python
len(translated_text) > len(original_text) * 1.5
```

### Resize Strategies

The `adjust_text_box_size` function is called from `apply_translation` after setting the translated text. It applies the following strategies:

1. **Word Wrap (always enabled):**
   ```python
   text_frame.word_wrap = True
   ```

2. **Auto-fit (when text is significantly longer):**
   ```python
   from pptx.enum.text import MSO_AUTO_SIZE
   if len(translated_text) > len(original_text) * 1.5:
       try:
           text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
       except:
           pass
   ```

3. **Width Expansion (freestanding shapes only):**
   ```python
   # Only for shapes not in groups or tables
   if not is_grouped and not is_in_table:
       current_width = shape.width
       max_width = 9144000  # ~10 inches in EMU
       new_width = min(int(current_width * 1.2), max_width)
       if new_width > current_width:
           try:
               shape.width = new_width
           except:
               pass
   ```

4. **Font Size Reduction (last resort, non-title text only):**
   ```python
   if not is_title:
       for para in text_frame.paragraphs:
           for run in para.runs:
               if run.font.size and run.font.size > Pt(10):
                   try:
                       new_size = max(Pt(10), run.font.size - Pt(1))
                       run.font.size = new_size
                   except:
                       pass
   ```

### Invocation

The function is called once per shape from `apply_translation`:

```python
# In apply_translation, after setting run.text:
if not segment.shape_path.startswith("notes") and "table[" not in segment.shape_path:
    adjust_text_box_size(target, segment.text, segment.translated, is_title)
```

Note: Text box adjustment is skipped for notes and table cells to avoid layout issues.

## API Configuration

### OpenAI-Compatible API Setup

The tool uses the standard OpenAI `/v1/chat/completions` API format via the `requests` library:

```python
import requests

def translate_batch(segments, model, api_base, api_key=None, verbose=False):
    url = f"{api_base}/chat/completions"

    texts = [seg.text for seg in segments]
    numbered_texts = "\n".join(f"{i+1}. {text}" for i, text in enumerate(texts))

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Translate the following {len(texts)} Chinese text segments to English. Return ONLY the translations, one per line:\n\n{numbered_texts}"}
        ],
        "temperature": 0.3,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(url, json=payload, headers=headers, timeout=120)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
```

### Supported Providers

The following providers are compatible with this tool:

| Provider | API Base URL | Authentication |
|----------|--------------|----------------|
| Qoderwork | (provided by client) | As needed |
| Ollama | `http://localhost:11434/v1` | None required |
| OpenAI | `https://api.openai.com/v1` | API key required |
| DeepSeek | `https://api.deepseek.com/v1` | API key required |
| Other | Varies | Varies |

### System Prompt

```
You are a professional translator specializing in business and technical content. 
Translate Chinese text to English following these rules:
1. Maintain original meaning, tone, and intent
2. Use professional business English for formal content
3. Preserve formatting markers (bullet points, numbering) in the translation
4. Do not translate proper nouns unless they have standard English equivalents
5. For mixed Chinese/English text, only translate the Chinese portions
6. Return ONLY the translations, one per line, corresponding to each input line
7. Do not add numbering, explanations, or any other text

Input format: Numbered list of text segments
Output format: Same numbered list with English translations only
```

### Model Selection

Translation quality varies significantly between models. Recommended models:

| Model | Size | Quality | Best For |
|-------|------|---------|----------|
| `qwen2.5:14b` | ~9GB | ★★★★★ | Chinese-to-English business content |
| `qwen2.5:7b` | ~4.7GB | ★★★★ | Good balance of quality and speed |
| `llama3.1:8b` | ~4.7GB | ★★★ | General purpose |
| `qwen2.5:3b` | ~2GB | ★★ | Quick tests, basic translations |

For best results with Chinese-to-English business content, **Qwen2.5 14B is strongly recommended** as it has excellent Chinese language understanding.

### Retry Logic

The `translate_batch` function implements inline retry with exponential backoff:

```python
def translate_batch(segments, model, api_base, api_key=None, verbose=False):
    texts = [seg.text for seg in segments]
    numbered_texts = "\n".join(f"{i+1}. {text}" for i, text in enumerate(texts))

    url = f"{api_base}/chat/completions"
    payload = {...}  # See above
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for attempt in range(MAX_RETRIES):  # MAX_RETRIES = 3
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            response.raise_for_status()
            result = response.json()
            return parse_numbered_response(result["choices"][0]["message"]["content"], len(segments))
        except requests.ConnectionError:
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                sleep(wait_time)
            else:
                return [seg.text for seg in segments]  # Fallback to original
        except requests.Timeout:
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                sleep(wait_time)
            else:
                return [seg.text for seg in segments]  # Fallback to original
        except requests.HTTPError:
            if attempt < MAX_RETRIES - 1:
                sleep(1)
            else:
                return [seg.text for seg in segments]  # Fallback to original
        except Exception:
            return [seg.text for seg in segments]  # Fallback to original
```

On failure after all retries, the function falls back to returning the original (untranslated) text to ensure the presentation remains usable.

## Error Handling

### Error Categories

| Error Type | Handling Strategy |
|------------|-------------------|
| API not reachable | Soft check on startup, warning only, proceed with translation attempt |
| Model not found | Log error, suggest checking model name or pulling for Ollama |
| Invalid PPTX | Try-catch on `Presentation()` load, suggest re-saving |
| API Timeout | Retry with backoff, skip batch on final failure |
| Partial Translation | Log warning, keep original text for failed segments |
| Font Not Found | Silently skip, use default font |

### Progress Logging

```python
print(f"Translating slide {slide_idx + 1}/{total_slides}...")
if verbose:
    print(f"  - Extracted {len(segments)} text segments")
    print(f"  - Batched into {len(batches)} API calls")
```

## Performance Considerations

- **Batch Size:** 20 segments balances API efficiency vs. token limits
- **Memory:** Stream process large presentations (process slide-by-slide)
- **Rate Limiting:** Add delays between batches for large files
- **Caching:** Consider caching translations for repeated segments
