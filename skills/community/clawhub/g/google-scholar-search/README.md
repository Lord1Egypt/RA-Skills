# Google Scholar Search Skill

A specialized skill for searching academic papers using the free Semantic Scholar API. No API key required.

## Features

- ✅ **Free to use** - No API key needed
- ✅ **Search academic papers** - Millions of papers from around the world
- ✅ **Get citation counts** - Understand paper influence
- ✅ **Get abstracts and author info** - Quickly understand paper content
- ✅ **Year filtering** - Find papers from specific time periods
- ✅ **Citation filtering** - Find high-impact papers
- ✅ **PDF download links** - Direct access to open access papers

## Installation

### Method 1: Copy folder to extensions (Recommended)

```bash
cp -r google-scholar-search ~/.openclaw/extensions/
```

### Method 2: Move folder to extensions

```bash
mv google-scholar-search ~/.openclaw/extensions/
```

After installation, restart OpenClaw to use the skill.

## Usage Examples

### Basic Search

```bash
python3 scripts/search_papers.py "machine learning"
```

### Search Papers from Specific Years

```bash
python3 scripts/search_papers.py "deep learning" --year 2020-2024
```

### Search Highly Cited Papers

```bash
python3 scripts/search_papers.py "quantum computing" --min-citations 100
```

### Limit Number of Results

```bash
python3 scripts/search_papers.py "neural networks" --limit 5
```

### Combined Search

```bash
python3 scripts/search_papers.py "artificial intelligence" --limit 10 --year 2022-2024 --min-citations 50
```

### Get JSON Format Output

```bash
python3 scripts/search_papers.py "computer vision" --json --limit 20
```

### Get Paper Details

```bash
python3 scripts/search_papers.py --details 4f2eda8077dc7a69bb2b4e0a1a086cf054adb3f9
```

## Returned Fields

Each paper includes:

- `title` - Paper title
- `authors` - List of authors
- `year` - Publication year
- `venue` - Journal or conference name
- `citationCount` - Number of citations
- `abstract` - Paper abstract
- `url` - Semantic Scholar link
- `openAccessPdf` - Direct PDF link (if available)
- `paperId` - Unique identifier

## Common Use Cases

### Find Latest Research

```bash
python3 scripts/search_papers.py "large language models" --year 2024 --limit 10
```

### Find Classic Papers

```bash
python3 scripts/search_papers.py "neural networks" --min-citations 500 --limit 10
```

### Find Survey Papers

```bash
python3 scripts/search_papers.py "survey review" --year 2020-2024
```

### Find Papers in Specific Field

```bash
python3 scripts/search_papers.py "reinforcement learning robotics" --limit 15
```

## API Limits

- Free tier: 5 requests per second, 100,000 calls per day
- No authentication required
- Higher limits available with API key (optional)

## Troubleshooting

### Getting "429 - Too Many Requests"

Wait a few seconds and retry. The API has rate limits.

### Empty Search Results

- Try more specific keywords
- Check spelling of search terms
- Try related terms

### Can't Get Abstract

Some papers may not have publicly available abstracts. Try visiting the paper URL for more information.

## Technical Details

- **API**: Semantic Scholar Graph API
- **No Authentication**: Free to use, no API key required
- **Data Sources**: Academic publishers worldwide and open access resources
- **Supported Formats**: Text and JSON output

## More Information

- Semantic Scholar: https://www.semanticscholar.org
- API Documentation: https://api.semanticscholar.org

## Example Output

```
Title: EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks
Authors: Mingxing Tan, Quoc V. Le
Year: 2019
Venue: International Conference on Machine Learning
Citations: 22714

Abstract:
Convolutional Neural Networks (ConvNets) are commonly developed at a fixed resource
budget, and then scaled up for better accuracy if more resources are available...

URL: https://www.semanticscholar.org/paper/4f2eda8077dc7a69bb2b4e0a1a086cf054adb3f9
```

---

Enjoy convenient academic searching! 🎓📚
