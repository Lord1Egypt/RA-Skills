---
name: paperview
description: PaperView API — generate ECharts visualizations, AI scientific diagrams, and word clouds from data, text, or PDF papers. Use when the user wants to create charts, scientific figures, flowcharts, architecture diagrams, or extract keywords from documents.
author: yyccR
homepage: https://www.ipaperview.com
repository: https://github.com/yyccR/paper-view-skill
license: MIT
env:
  PAPERVIEW_API_TOKEN:
    description: API token obtained from www.ipaperview.com (Profile → API Token). Format: pv_live_<hex_string>
    required: true
---

# PaperView API

PaperView provides three AI-powered visualization APIs:
1. **ECharts Visualization** — generate interactive charts from CSV/JSON/text data
2. **AI Scientific Diagram** — generate publication-quality figures from text or arxiv PDF
3. **Word Cloud** — extract keyword frequencies from PDF documents (supports CJK)

## Authentication

All requests require an API Token:

```
Authorization: Bearer pv_live_<your_token>
```

Obtain your token from the www.ipaperview.com website (Profile → API Token). Each account can create one token. Set via environment variable `PAPERVIEW_API_TOKEN` or ask the user for their token.

## Base URL

```
https://api.ipaperview.com
```

## API Quota

Daily API call limits by plan:

| Plan | Daily Limit |
|------|-------------|
| Free | 3 calls/day |
| Monthly ($4.99/mo) | 30 calls/day |
| Yearly ($29.99/yr) | 100 calls/day |

Each API call consumes 1 quota.

---

## 1. ECharts Visualization

**POST /api/v1/viz/generate/**

AI analyzes your data sample, selects the best chart type, and returns a ready-to-render ECharts option. The full data processing happens server-side — AI only sees a sample to generate a transform script, then the backend executes it with Node.js on the full dataset.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `data` | string | Yes | Raw data in CSV, JSON, or plain text |
| `toolset` | string | No | Chart category: `bar`, `line`, `scatter`, `pie`, `heatmap`, `violin`, `manhattan`, `volcano`, `forest`, `survival`, `roc`, `venn`, `upset`, etc. If omitted, AI auto-selects |
| `template` | string | No | Specific template within the toolset. If omitted, AI auto-selects |
| `context` | string | No | Natural language instructions, e.g. "show GDP trend by country", "use blue color scheme" |

**Available chart types:**
- **Basic:** line, bar, scatter, pie, radar, funnel, boxplot
- **Advanced:** heatmap, treemap, sankey, tree, sunburst, map, structure
- **3D:** gl3d (bar3D, scatter3D)
- **Scientific:** violin, manhattan, volcano, forest, survival, roc, venn, upset, enrichment, circos, waterfall

```bash
curl -X POST \
  -H "Authorization: Bearer $PAPERVIEW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "Year,China,USA,Japan\n2018,13608,20544,4971\n2019,14280,21373,5082\n2020,14723,20894,5040\n2021,17734,23315,4941\n2022,17963,25463,4231",
    "context": "Show GDP trends as a line chart"
  }' \
  https://api.ipaperview.com/api/v1/viz/generate/
```

**Response:**

```json
{
  "success": true,
  "toolset": "line",
  "template": "confidence_band",
  "echarts_option": {
    "title": { "text": "GDP by Country (2018-2022)" },
    "xAxis": { "type": "category", "data": ["2018", "2019", "2020", "2021", "2022"] },
    "yAxis": { "type": "value" },
    "series": [
      { "name": "China", "type": "line", "data": [13608, 14280, 14723, 17734, 17963] },
      { "name": "USA", "type": "line", "data": [20544, 21373, 20894, 23315, 25463] },
      { "name": "Japan", "type": "line", "data": [4971, 5082, 5040, 4941, 4231] }
    ],
    "legend": { "data": ["China", "USA", "Japan"] }
  },
  "reason": "Time series data with multiple countries — line chart shows trends clearly"
}
```

The `echarts_option` can be rendered directly with `echarts.setOption(echarts_option)` in any ECharts-compatible environment.

---

## 2. AI Scientific Diagram

**POST /api/diagram/ai-generate/**

Generate publication-quality scientific diagrams, flowcharts, and research illustrations. Supports arxiv paper URLs directly. Returns a Server-Sent Events stream — use `curl -N` to receive events.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `template_type` | string | Yes | `custom_text_only` (from text) or `custom` (with reference image) |
| `custom_prompt` | string | Yes | Description of what to draw. Can include style instructions (colors, themes, specific elements) |
| `pdf_url` | string | No | URL to a PDF paper (supports arxiv abs/pdf URLs like `http://arxiv.org/abs/2510.13809v1`) |
| `selected_text` | string | No | Text excerpt to visualize |
| `reference_image_url` | string | No | Reference image URL to guide the style |
| `language` | string | No | `auto`, `en`, `zh` (default: `auto`) |
| `aspect_ratio` | string | No | e.g. `16:9`, `1:1`, `4:3` |

**Example — from text description:**

```bash
curl -N -X POST \
  -H "Authorization: Bearer $PAPERVIEW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "template_type": "custom_text_only",
    "custom_prompt": "A flowchart: Data Collection -> Preprocessing -> Training -> Evaluation"
  }' \
  https://api.ipaperview.com/api/diagram/ai-generate/
```

**Example — from arxiv paper with custom style:**

```bash
curl -N -X POST \
  -H "Authorization: Bearer $PAPERVIEW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "template_type": "custom_text_only",
    "pdf_url": "http://arxiv.org/abs/2510.13809v1",
    "custom_prompt": "Generate an architecture diagram with pink color scheme, include Doraemon as a mascot element"
  }' \
  https://api.ipaperview.com/api/diagram/ai-generate/
```

**SSE Events (in order):**

```
data: {"type": "step", "step": "extracting", "message": "Extracting document content..."}
data: {"type": "step", "step": "generating_prompt", "message": "Generating image prompt..."}
data: {"type": "prompt_generated", "prompt": "...", "enhanced_prompt": "..."}
data: {"type": "step", "step": "generating_image", "message": "Generating image..."}
data: {"type": "complete", "success": true, "image_url": "https://...", "model": "gemini-2.0-flash-preview-image-generation"}
```

The final `complete` event contains `image_url` — a CDN URL to the generated image.

---

## 3. Word Cloud

**POST /api/wordcloud/extract/**

Extract keyword frequencies from PDF documents with automatic CJK (Chinese/Japanese/Korean) segmentation and semantic clustering.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pdf_url` | string | Yes | URL to a PDF document (supports arxiv URLs) |
| `max_words` | integer | No | Max keywords to return (default: 100) |

```bash
curl -X POST \
  -H "Authorization: Bearer $PAPERVIEW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_url": "https://arxiv.org/pdf/2301.00001.pdf",
    "max_words": 50
  }' \
  https://api.ipaperview.com/api/wordcloud/extract/
```

**Response:**

```json
{
  "success": true,
  "data": [
    { "word": "neural", "frequency": 45, "cluster": 0 },
    { "word": "network", "frequency": 38, "cluster": 0 },
    { "word": "attention", "frequency": 32, "cluster": 1 }
  ]
}
```

The `cluster` field (0-4) groups words by frequency — useful for color coding in word cloud rendering. CJK documents are automatically segmented using jieba.

---

## Error Responses

```json
{ "success": false, "error": "Error description" }
```

| HTTP Code | Meaning |
|-----------|---------|
| 400 | Bad request (missing or invalid parameters) |
| 401 | Invalid or missing API token |
| 402 | Quota exceeded (daily API call limit reached) |
| 500 | Server error |

## Rendering Results

After calling the API, you MUST render the results visually. No extra dependencies needed — use CDN-loaded HTML files.

### Render ECharts Visualization

When you receive `echarts_option` from `/api/v1/viz/generate/`, create a self-contained HTML file and open it in the browser:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PaperView Chart</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>body{margin:0;background:#fff}#chart{width:100vw;height:100vh}</style>
</head>
<body>
  <div id="chart"></div>
  <script>
    var chart = echarts.init(document.getElementById('chart'));
    var option = {{ECHARTS_OPTION_JSON}};
    chart.setOption(option);
    window.addEventListener('resize', function() { chart.resize(); });
  </script>
</body>
</html>
```

Replace `{{ECHARTS_OPTION_JSON}}` with the `echarts_option` value from the API response (the JSON object, not stringified). Save as a `.html` file and open:

```bash
# macOS
open /tmp/paperview_chart.html
# Linux
xdg-open /tmp/paperview_chart.html
```

For 3D charts (gl3d toolset), add this additional script tag before the main script:
```html
<script src="https://cdn.jsdelivr.net/npm/echarts-gl@2/dist/echarts-gl.min.js"></script>
```

### Render Word Cloud

When you receive word frequency data from `/api/wordcloud/extract/`, create an HTML file using echarts-wordcloud:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PaperView Word Cloud</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/echarts-wordcloud@2/dist/echarts-wordcloud.min.js"></script>
  <style>body{margin:0;background:#fff}#chart{width:100vw;height:100vh}</style>
</head>
<body>
  <div id="chart"></div>
  <script>
    var chart = echarts.init(document.getElementById('chart'));
    var words = {{WORDCLOUD_DATA_JSON}};
    var clusterColors = ['#5470c6','#91cc75','#fac858','#ee6666','#73c0de'];
    chart.setOption({
      series: [{
        type: 'wordCloud',
        sizeRange: [14, 80],
        rotationRange: [-45, 45],
        gridSize: 8,
        shape: 'circle',
        textStyle: {
          fontFamily: 'sans-serif',
          color: function(params) {
            return clusterColors[params.data.cluster || 0];
          }
        },
        data: words.map(function(w) {
          return { name: w.word, value: w.frequency, cluster: w.cluster };
        })
      }]
    });
  </script>
</body>
</html>
```

Replace `{{WORDCLOUD_DATA_JSON}}` with the `data` array from the API response.

### Render AI Diagram

The AI diagram endpoint already returns an `image_url` (CDN link). Simply download it or open in browser:

```bash
# Open in browser
open "https://cdn.example.com/generated/image.jpg"
# Or download
curl -o /tmp/paperview_diagram.png "https://cdn.example.com/generated/image.jpg"
```

## Privacy & Data Handling

**What data is sent to api.ipaperview.com:**
- **ECharts API**: The raw text data (CSV/JSON/text string) you provide in the `data` field is sent to the server. No local files are uploaded — you must pass the data content as a string in the request body.
- **AI Diagram API**: Only the `pdf_url` (a public URL) is sent. The server fetches the PDF from that URL. No local files are uploaded from your machine.
- **Word Cloud API**: Only the `pdf_url` (a public URL) is sent. The server fetches the PDF from that URL. No local files are uploaded from your machine.

**Data retention:**
- Submitted text data (CSV/JSON) is processed in memory and **not stored** after the response is returned.
- Generated AI diagram images are uploaded to Upyun CDN and retained for **30 days**, after which they are automatically deleted.
- No user data is sold or shared with third parties.

**Authentication:**
- This skill requires a `PAPERVIEW_API_TOKEN` environment variable (format: `pv_live_<hex_string>`).
- Obtain your token from [www.ipaperview.com](https://www.ipaperview.com) → Profile → API Token.
- Each API call is authenticated and rate-limited per your subscription plan.

## Usage Tips

1. **Auto-selection**: For ECharts, omit `toolset` and `template` to let AI pick the best chart type for your data
2. **Large datasets**: Safe to send large CSV files — AI only sees a sample, full data is processed server-side
3. **SSE parsing**: AI diagram endpoint uses Server-Sent Events. Parse each `data:` line as JSON and wait for the `type: "complete"` event
4. **Arxiv URLs**: Both `http://arxiv.org/abs/...` and `https://arxiv.org/pdf/...` formats are supported for pdf_url
5. **Custom styles**: Use the `custom_prompt` and `context` fields to request specific colors, themes, or visual elements
6. **Always render**: After receiving API results, always render them visually using the HTML templates above so the user can see the chart/wordcloud
