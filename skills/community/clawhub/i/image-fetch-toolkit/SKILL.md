---
name: image-fetch-toolkit
description: Search and fetch images from the internet for any purpose - paper figures, news photos, stock images, product photos, scientific illustrations, social media images, and more. Use this skill whenever the user needs to find, retrieve, or curate images from online sources, whether for academic papers, blog posts, presentations, marketing materials, or content creation. Also covers academic figure composition (multi-panel abc labeling), scientific illustration generation, and image search API integration.
---

# Image Fetch Toolkit

A comprehensive guide for AI agents to search, retrieve, and curate images from various online sources. Covers free stock photos, academic figures, news images, product photos, scientific illustrations, and more.

## Quick Start

Before fetching images, check which tools/APIs are available in the current environment:

1. **Tavily** - Web search + URL extraction (recommended, often pre-configured)
2. **Unsplash API** - 3M+ free high-quality photos
3. **Pexels API** - Free stock photos + videos
4. **Pixabay API** - 2M+ free images, illustrations, vectors
5. **Flickr API** - Photographer community images
6. **Google Custom Search API** - General image search
7. **Bing Image Search API** - Microsoft's image search

---

## 1. Free Stock Photo APIs

### Unsplash API
- **Base URL**: `https://api.unsplash.com`
- **Auth**: Bearer token in header `Authorization: Bearer <ACCESS_KEY>`
- **Get key**: https://unsplash.com/developers
- **Rate limit**: 50 requests/hour (free tier)

```bash
# Search photos
curl -H "Authorization: Bearer $UNSPLASH_ACCESS_KEY" \
  "https://api.unsplash.com/search/photos?query=renewable+energy&per_page=10&orientation=landscape"

# Get a random photo
curl -H "Authorization: Bearer $UNSPLASH_ACCESS_KEY" \
  "https://api.unsplash.com/photos/random?query=technology&orientation=squarish"

# Download tracked photo (respects photographer attribution)
curl -H "Authorization: Bearer $UNSPLASH_ACCESS_KEY" \
  -L "https://api.unsplash.com/photos/<PHOTO_ID>/download"
```

**Response fields**: `results[].urls.raw`, `results[].urls.full`, `results[].urls.regular`, `results[].urls.small`, `results[].user.name`, `results[].links.html`

### Pexels API
- **Base URL**: `https://api.pexels.com/v1`
- **Auth**: Header `Authorization: <API_KEY>`
- **Get key**: https://www.pexels.com/api/
- **Rate limit**: 200 requests/hour

```bash
# Search photos
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=nature&per_page=10&orientation=landscape"

# Curated photos
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/curated?per_page=15"

# Get photo by ID
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/photos/<PHOTO_ID>"
```

### Pixabay API
- **Base URL**: `https://pixabay.com/api`
- **Auth**: Query param `key=<API_KEY>`
- **Get key**: https://pixabay.com/api/docs/
- **Rate limit**: 100 requests/min

```bash
# Search images
curl "https://pixabay.com/api/?key=$PIXABAY_API_KEY&q=mountain+landscape&image_type=photo&per_page=10&safesearch=true"

# Search vectors/illustrations
curl "https://pixabay.com/api/?key=$PIXABAY_API_KEY&q=robot&image_type=vector&per_page=10"

# Search videos
curl "https://pixabay.com/api/videos/?key=$PIXABAY_API_KEY&q=ocean&per_page=5"
```

**Categories**: `backgrounds`, `fashion`, `nature`, `science`, `education`, `feelings`, `health`, `people`, `religion`, `places`, `animals`, `industry`, `computer`, `food`, `sports`, `transportation`, `travel`, `buildings`, `business`, `music`

### Flickr API
- **Base URL**: `https://api.flickr.com/services/rest`
- **Auth**: API key query param
- **Get key**: https://www.flickr.com/services/apps/
- **Note**: Check license! Use `license=1,2,4,5,9` for CC-compatible

```bash
# Search photos (CC license only)
curl "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=$FLICKR_API_KEY&text=sunset&license=1,2,4,5,9&per_page=10&format=json&nojsoncallback=1"

# Get photo URL: https://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg
```

---

## 2. Search Engine Image APIs

### Google Custom Search API (Image Search)
- **Base URL**: `https://www.googleapis.com/customsearch/v1`
- **Auth**: API key + CX (search engine ID)
- **Get key**: https://developers.google.com/custom-search
- **Note**: Enable "Image Search" in your Custom Search Engine settings

```bash
# Search images
curl "https://www.googleapis.com/customsearch/v1?key=$GOOGLE_API_KEY&cx=$GOOGLE_CX&searchType=image&q=AI+conference+2024&num=10&imgSize=large"
```

### Bing Image Search API
- **Base URL**: `https://api.bing.microsoft.com/v7.0/images/search`
- **Auth**: Header `Ocp-Apim-Subscription-Key: <KEY>`
- **Get key**: https://www.microsoft.com/en-us/bing/apis/bing-image-search-api
- **Rate limit**: 1000 transactions/month (free)

```bash
curl -H "Ocp-Apim-Subscription-Key: $BING_API_KEY" \
  "https://api.bing.microsoft.com/v7.0/images/search?q=cute+cats&count=10&imageType=Photo&size=Large"
```

### Tavily Extract (for webpage images)
```bash
# Extract content + images from a URL
node ~/.openclaw/workspace/skills/tavily-search/scripts/extract.mjs "https://example.com/article" --include-images true
```

---

## 3. Academic & Scientific Image Sources

### Paper Search MCP (MCP Server)
- **Repo**: https://github.com/openags/paper-search-mcp
- **Features**: Search Semantic Scholar, arXiv, CORE, Zenodo, Google Scholar, IEEE, ACM
- **Install**:
```bash
npx skills add openags/paper-search-mcp
# or with uv:
uv tool install paper-search-mcp
```
- **Usage**: Search papers → extract figure URLs from paper pages

```bash
# Search papers
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=protein+folding&limit=10&fields=title,url,openAccessPdf"
```

### Semantic Scholar API (Free)
```bash
# Search papers with figure references
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=transformer+architecture&limit=5&fields=title,url,openAccessPdf,figures"
```

### arXiv API (Free, no key needed)
```bash
# Search papers
curl "http://export.arxiv.org/api/query?search_query=all:electron+microscopy&start=0&max_results=5"
```

### PubMed Central (Free, no key needed)
```bash
# Search PMC for figures
curl "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC1234567"  # get full text XML with figures
```

### Scientific Illustration Tools
- **FigureLabs**: https://www.figurelabs.ai - AI-powered scientific figure generation
- **BioRender**: https://biorender.com - Professional biological diagrams
- **Illustrae**: AI scientific illustration generation
- **Mind the Graph**: https://mindthegraph.com - Scientific infographic maker

---

## 4. Academic Figure Composition (Multi-Panel abc Labels)

For combining multiple images into a single figure with (a), (b), (c) labels - standard in academic papers.

### Python (matplotlib + PIL)

```python
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def create_figure_grid(image_paths, labels=None, cols=2, label_font_size=20, 
                       label_position='top-left', padding=20, label_color='white',
                       bg_color='white', dpi=300, output_path='figure.png'):
    """
    Combine multiple images into a single academic figure with (a)(b)(c) labels.
    
    Args:
        image_paths: List of image file paths
        labels: List of label strings (default: a, b, c, ...)
        cols: Number of columns
        label_font_size: Font size for labels
        label_position: 'top-left', 'top-right', 'bottom-left', 'bottom-right'
        padding: Space between images in pixels
        label_color: Color of labels ('white' or 'black')
        bg_color: Background color
        dpi: Output DPI
        output_path: Output file path
    """
    if labels is None:
        labels = [chr(ord('a') + i) for i in range(len(image_paths))]
    
    rows = (len(image_paths) + cols - 1) // cols
    images = [Image.open(p).convert('RGB') for p in image_paths]
    
    # Find max dimensions
    max_w = max(img.width for img in images)
    max_h = max(img.height for img in images)
    
    # Create canvas
    total_w = cols * max_w + (cols + 1) * padding
    total_h = rows * max_h + (rows + 1) * padding
    canvas = Image.new('RGB', (total_w, total_h), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # Try to load a font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", label_font_size)
    except:
        font = ImageFont.load_default()
    
    for idx, (img, label) in enumerate(zip(images, labels)):
        row, col = idx // cols, idx % cols
        x = padding + col * (max_w + padding)
        y = padding + row * (max_h + padding)
        canvas.paste(img, (x, y))
        
        # Draw label
        label_text = f"({label})"
        bbox = draw.textbbox((0, 0), label_text, font=font)
        lw, lh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        margin = 10
        
        if label_position == 'top-left':
            lx, ly = x + margin, y + margin
        elif label_position == 'top-right':
            lx, ly = x + max_w - lw - margin, y + margin
        elif label_position == 'bottom-left':
            lx, ly = x + margin, y + max_h - lh - margin
        else:
            lx, ly = x + max_w - lw - margin, y + max_h - lh - margin
        
        # Draw background rectangle for readability
        draw.rectangle([lx - 4, ly - 2, lx + lw + 4, ly + lh + 2], fill=label_color, outline=label_color)
        text_color = 'black' if label_color == 'white' else 'white'
        draw.text((lx, ly), label_text, fill=text_color, font=font)
    
    canvas.save(output_path, dpi=(dpi, dpi))
    print(f"Figure saved to {output_path}")
    return canvas

# Usage
create_figure_grid(
    image_paths=['fig1.png', 'fig2.png', 'fig3.png', 'fig4.png'],
    labels=['a', 'b', 'c', 'd'],
    cols=2,
    output_path='combined_figure.png'
)
```

### Python (matplotlib subplot)

```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def subplot_figure(image_paths, labels=None, cols=2, figsize=(12, 10), 
                   label_size=16, label_weight='bold', output_path='figure.pdf'):
    """Create academic figure using matplotlib subplots with (a)(b)(c) labels."""
    if labels is None:
        labels = [chr(ord('a') + i) for i in range(len(image_paths))]
    
    rows = (len(image_paths) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
    
    for ax, path, label in zip(axes, image_paths, labels):
        img = mpimg.imread(path)
        ax.imshow(img)
        ax.set_title(f'({label})', fontsize=label_size, fontweight=label_weight, loc='left')
        ax.axis('off')
    
    # Hide empty subplots
    for ax in axes[len(image_paths):]:
        ax.axis('off')
    
    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")

# Usage
subplot_figure(['a.png', 'b.png', 'c.png'], cols=3, output_path='fig1.pdf')
```

### CLI one-liner (ImageMagick)

```bash
# Simple 2x2 grid
montage img1.png img2.png img3.png img4.png -tile 2x2 -geometry +5+5 output.png

# With labels (requires additional steps)
# Better to use the Python script above for labeled figures
```

---

## 5. News Image Sources

### Google News Scraper
- **Repo**: https://github.com/oxylabs/google-news-scraper
- Scrapes Google News articles including thumbnails

### Tavily News Search
```bash
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "AI breakthrough 2024" --topic news --days 7
```

### NewsAPI.org
- **Base URL**: `https://newsapi.org/v2`
- **Auth**: `apiKey` query param or `X-Api-Key` header
- **Get key**: https://newsapi.org
- **Rate limit**: 100 requests/day (free)

```bash
# Search news with images
curl "https://newsapi.org/v2/everything?q=AI+research&apiKey=$NEWSAPI_KEY&pageSize=10"
# Articles include urlToImage field
```

### GNews API
- **Base URL**: `https://gnews.io/api/v4`
- **Auth**: `token` query param or `apikey` header

```bash
curl "https://gnews.io/api/v4/search?q=climate+change&token=$GNEWS_API_KEY&lang=en&max=10"
```

---

## 6. E-Commerce / Product Image Sources

### Amazon Product Advertising API
- **Base URL**: `https://webservices.amazon.com/paapi5`
- **Auth**: Access Key + Secret Key
- **Get key**: https://affiliate-program.amazon.com

```bash
# Search products with images (via PA-API)
curl -X POST "https://webservices.amazon.com/paapi5/searchitems" \
  -H "Content-Type: application/json" \
  -d '{"Keywords":"wireless headphones","SearchIndex":"Electronics","ItemCount":10}'
```

### Scraper Alternatives (GitHub)
- Search GitHub for `amazon scraper`, `taobao scraper`, `ebay scraper`
- Use with caution regarding terms of service

---

## 7. Social Media Image Sources

### X/Twitter
- **xbird-skill MCP**: https://github.com/checkra1neth/xbird-skill - 34 tools for Twitter/X
- **x-search (ClawHub)**: Search tweets with media

### Reddit
- **Reddit API**: `https://oauth.reddit.com/search.json?q=<query>&type=link`
- Multiple subreddits are excellent image sources:
  - r/EarthPorn, r/SpacePorn, r/CityPorn - High-res photography
  - r/dataisbeautiful - Data visualizations
  - r/infographics - Infographics
  - r/scientific - Scientific imagery

### Instagram (via Meta Graph API)
- **Base URL**: `https://graph.instagram.com`
- **Auth**: Access Token
- **Get key**: https://developers.facebook.com/docs/instagram-api

---

## 8. Wikimedia Commons (Free, no key needed)

```bash
# Search images via MediaWiki API
curl "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrsearch=cat+breeds&gsrlimit=10&prop=imageinfo&iiprop=url|extmetadata&format=json"

# Get random featured picture
curl "https://commons.wikimedia.org/w/api.php?action=query&list=random&rnnamespace=6&rnlimit=5&prop=imageinfo&iiprop=url&format=json"
```

---

## 9. AI Image Generation (When You Can't Find What You Need)

### Built-in OpenClaw image generation
Use the `image_generate` tool directly - supports DALL-E, Gemini, and other providers.

### MCP Image Generators
- **mcp-image (Nano Banana)**: AI image generation via Gemini
  - `npx mcp-image` with `GEMINI_API_KEY`
- **fal.ai MCP**: Multi-provider image generation
- **Flux MCP**: Flux model image generation

---

## 10. Image Search Strategy Guide

### By Use Case

| Use Case | Best Sources | Notes |
|----------|-------------|-------|
| Academic papers | Semantic Scholar, arXiv, PubMed | Check open access for figures |
| Blog posts | Unsplash, Pexels, Pixabay | Free commercial use |
| Presentations | Unsplash, Wikimedia Commons | High resolution preferred |
| Social media | Unsplash, Pexels, Pixabay | Square/vertical formats |
| Product images | Platform APIs, scraper | Check ToS |
| News articles | NewsAPI, Tavily news, Google News | urlToImage field |
| Scientific figures | FigureLabs, BioRender, matplotlib | Generate, don't search |
| Data visualizations | Reddit r/dataisbeautiful, Observable | Check licensing |
| Icons/illustrations | Pixabay (vectors), Flaticon, Noun Project | SVG preferred |
| Backgrounds | Unsplash, Pixabay (backgrounds category) | High resolution |

### Best Practices

1. **Always check licensing** - Use CC0/public domain when possible for publications
2. **Attribute creators** - Even when not required, it's good practice
3. **Prefer high resolution** - Download `raw` or `full` size for print/publication
4. **Batch your requests** - Respect API rate limits
5. **Cache results** - Don't re-fetch the same images
6. **Validate URLs** - Image URLs can expire; download promptly
7. **Use `include_images`** - When extracting web content, request images

---

## Environment Variable Reference

Set these in your shell environment or `.env` file:

```bash
# Free Stock Photos
UNSPLASH_ACCESS_KEY=""     # https://unsplash.com/developers
PEXELS_API_KEY=""          # https://www.pexels.com/api/
PIXABAY_API_KEY=""         # https://pixabay.com/api/docs/
FLICKR_API_KEY=""          # https://www.flickr.com/services/apps/

# Search Engines
GOOGLE_API_KEY=""          # https://developers.google.com/custom-search
GOOGLE_CX=""               # Custom Search Engine ID
BING_API_KEY=""            # https://www.microsoft.com/en-us/bing/apis/

# News
NEWSAPI_KEY=""             # https://newsapi.org
GNEWS_API_KEY=""           # https://gnews.io

# AI Generation
GEMINI_API_KEY=""          # https://aistudio.google.com
OPENAI_API_KEY=""          # https://platform.openai.com
```

