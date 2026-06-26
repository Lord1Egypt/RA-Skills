# OCR Tool Usage Examples

## Basic Usage

### 1. Extract Text from Image

```bash
# Basic OCR (English)
tesseract image.png output.txt

# Chinese OCR
tesseract image.png stdout -l chi_sim

# Chinese + English OCR
tesseract image.png stdout -l chi_sim+eng
```

### 2. Using the Python Script

```python
# Import and use in Python
from scripts.ocr_extract import analyze_image

result = analyze_image("announcement.png", lang="chi_sim+eng", detailed=True)
print(f"Found {len(result['info']['companies'])} companies")
```

### 3. Using the Batch Script (Windows)

```batch
:: Basic extraction
ocr.bat announcement.png

:: With detailed analysis
ocr.bat announcement.png --detailed

:: Extract only to file
ocr.bat announcement.png --output analysis.txt --extract-only
```

### 4. Using the Shell Script (Unix/Linux/macOS)

```bash
# Basic extraction
./ocr.sh announcement.png

# With detailed analysis
./ocr.sh announcement.png --detailed

# Extract only to file
./ocr.sh announcement.png --output analysis.txt --extract-only
```

## Real-World Examples

### Example 1: Financial Announcement Analysis

```bash
# Analyze a financial announcement image
./ocr.sh "公告全知道20260331.png" --detailed

# Output will include:
# - Company names (extracted from hashtags and text)
# - Stock codes
# - Financial metrics
# - Keywords
```

### Example 2: Batch Processing Multiple Images

```bash
# Process all PNG images in a directory
for img in *.png; do
    echo "Processing: $img"
    ./ocr.sh "$img" --output "analysis_${img%.png}.txt"
done
```

### Example 3: Integration with OpenClaw

```python
# In an OpenClaw skill or agent
import subprocess
import json

def process_telegram_image(image_path):
    """Process image received via Telegram"""
    
    # Extract text using OCR
    result = subprocess.run(
        ['tesseract', image_path, 'stdout', '-l', 'chi_sim+eng'],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    text = result.stdout
    
    # Analyze for financial information
    companies = []
    if '#红相股份' in text:
        companies.append('红相股份')
    if '#海亮股份' in text:
        companies.append('海亮股份')
    if '#国电南自' in text:
        companies.append('国电南自')
    
    # Extract other company mentions
    import re
    all_companies = re.findall(r'#([^\s#]+)', text)
    
    return {
        'text': text[:500] + '...' if len(text) > 500 else text,
        'companies': companies,
        'all_mentions': all_companies,
        'has_financial_data': any(keyword in text for keyword in ['利润', '增长', '合同', '中标'])
    }
```

### Example 4: Telegram Message Processing Workflow

```python
# Typical workflow for processing Telegram financial images
def process_financial_image_message(image_path, message_text):
    """
    Process financial image messages like "公告全知道"
    
    Args:
        image_path: Path to downloaded image
        message_text: Original message text (for context)
    """
    
    # Step 1: Extract text from image
    ocr_text = extract_text_with_ocr(image_path)
    
    # Step 2: Parse message text for context
    hashtags = extract_hashtags(message_text)
    
    # Step 3: Analyze combined information
    analysis = analyze_financial_content(ocr_text, hashtags)
    
    # Step 4: Generate concise summary
    summary = generate_summary(analysis)
    
    return summary

def extract_text_with_ocr(image_path):
    """Extract text using Tesseract"""
    try:
        result = subprocess.run(
            ['tesseract', image_path, 'stdout', '-l', 'chi_sim+eng'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"OCR Error: {e.stderr}"
    except FileNotFoundError:
        return "Error: Tesseract not installed"

def extract_hashtags(text):
    """Extract hashtags from message text"""
    import re
    return re.findall(r'#(\S+)', text)

def analyze_financial_content(ocr_text, hashtags):
    """Analyze financial content"""
    analysis = {
        'mentioned_companies': hashtags,
        'ocr_companies': [],
        'financial_metrics': [],
        'key_themes': []
    }
    
    # Extract companies from OCR text
    import re
    ocr_companies = re.findall(r'#([^\s#]+)', ocr_text)
    analysis['ocr_companies'] = list(set(ocr_companies))
    
    # Extract financial metrics
    metrics = re.findall(r'同比增长\s*([0-9.]+%)|利润\s*([0-9.]+亿元)', ocr_text)
    analysis['financial_metrics'] = [m for m in metrics if m]
    
    # Identify key themes
    themes = ['商业航天', '智能电网', '机器人', '绿色电力', '电气设备']
    analysis['key_themes'] = [theme for theme in themes if theme in ocr_text]
    
    return analysis

def generate_summary(analysis):
    """Generate concise summary"""
    summary = []
    
    if analysis['mentioned_companies']:
        summary.append(f"提及公司: {', '.join(analysis['mentioned_companies'])}")
    
    if analysis['key_themes']:
        summary.append(f"主题: {', '.join(analysis['key_themes'])}")
    
    if analysis['financial_metrics']:
        summary.append(f"财务指标: {len(analysis['financial_metrics'])}项")
    
    return " | ".join(summary)
```

## Advanced Examples

### Example 5: Image Preprocessing for Better OCR

```bash
# Preprocess image before OCR (using ImageMagick)
# Convert to grayscale
convert input.png -grayscale Rec709Luma grayscale.png
tesseract grayscale.png stdout -l chi_sim+eng

# Increase contrast
convert input.png -contrast -contrast enhanced.png
tesseract enhanced.png stdout -l chi_sim+eng

# Remove noise
convert input.png -despeckle denoised.png
tesseract denoised.png stdout -l chi_sim+eng
```

### Example 6: Custom Configuration for Financial Charts

```bash
# Use specific PSM mode for financial charts
# PSM 6: Assume a single uniform block of text
tesseract chart.png stdout -l chi_sim+eng --psm 6

# PSM 11: Sparse text (good for charts with scattered text)
tesseract chart.png stdout -l chi_sim+eng --psm 11

# PSM 12: Sparse text with OSD
tesseract chart.png stdout -l chi_sim+eng --psm 12
```

### Example 7: Multi-language Support

```bash
# Chinese Simplified
tesseract image.png stdout -l chi_sim

# Chinese Traditional
tesseract image.png stdout -l chi_tra

# Japanese
tesseract image.png stdout -l jpn

# Korean
tesseract image.png stdout -l kor

# Multiple languages
tesseract image.png stdout -l chi_sim+eng+jpn
```

## Troubleshooting Examples

### Example 8: Handling Common Issues

```bash
# Issue: Poor OCR accuracy
# Solution: Preprocess image
convert input.png -resize 200% -grayscale Rec709Luma -contrast preprocessed.png
tesseract preprocessed.png stdout -l chi_sim+eng --psm 6

# Issue: Missing Chinese characters
# Solution: Verify language data and use appropriate PSM
tesseract input.png stdout -l chi_sim --psm 3 --oem 1

# Issue: Tesseract not found
# Solution: Install Tesseract
# Windows: choco install tesseract
# macOS: brew install tesseract
# Ubuntu: sudo apt install tesseract-ocr
```

## Integration with Other Tools

### Example 9: OCR + Text Analysis Pipeline

```python
def ocr_analysis_pipeline(image_path):
    """Complete OCR analysis pipeline"""
    
    # Step 1: OCR extraction
    text = extract_text_with_ocr(image_path)
    
    # Step 2: Text cleaning
    cleaned_text = clean_text(text)
    
    # Step 3: Information extraction
    entities = extract_entities(cleaned_text)
    
    # Step 4: Sentiment/trend analysis
    analysis = analyze_sentiment(cleaned_text)
    
    # Step 5: Report generation
    report = generate_report(entities, analysis)
    
    return report

def clean_text(text):
    """Clean OCR text"""
    import re
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Fix common OCR errors
    corrections = {
        'O': '0',  # OCR often confuses zero with letter O
        'l': '1',  # Letter l with number 1
        # Add more corrections as needed
    }
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    return text.strip()

def extract_entities(text):
    """Extract entities from text"""
    import re
    entities = {
        'companies': re.findall(r'([\u4e00-\u9fa5]{2,}股份|[\u4e00-\u9fa5]{2,}科技)', text),
        'dates': re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', text),
        'amounts': re.findall(r'[0-9,.]+亿元|[0-9,.]+万元|[0-9,.]+%', text),
    }
    return entities

def analyze_sentiment(text):
    """Simple sentiment analysis"""
    positive_words = ['增长', '利好', '上涨', '突破', '创新高']
    negative_words = ['下跌', '利空', '风险', '亏损', '下滑']
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

def generate_report(entities, sentiment):
    """Generate analysis report"""
    report = {
        'summary': f"Found {len(entities['companies'])} companies, sentiment: {sentiment}",
        'companies': entities['companies'],
        'dates': entities['dates'],
        'amounts': entities['amounts'],
        'sentiment': sentiment
    }
    return report
```

## Best Practices

1. **Always verify OCR results** - Especially for financial data
2. **Preprocess images** - Improve accuracy with grayscale, contrast adjustment
3. **Use appropriate language packs** - Install chi_sim for Chinese text
4. **Test different PSM modes** - Different images work better with different modes
5. **Cache results** - Avoid re-processing the same images
6. **Handle errors gracefully** - Tesseract may fail on poor quality images
7. **Combine with context** - Use message text to supplement OCR results