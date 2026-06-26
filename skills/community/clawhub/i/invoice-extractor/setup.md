# Invoice Extractor Setup Guide

## Prerequisites

- Python 3.8 or higher
- Internet connection (for Baidu OCR API)
- Baidu Cloud account

## Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- requests (for API calls)
- pandas (for data handling)
- openpyxl (for Excel export)
- PyMuPDF (for PDF processing)
- Pillow (for image processing)

### Step 2: Get Baidu OCR Credentials

1. Visit https://cloud.baidu.com/product/ocr
2. Register/login with your phone number
3. Complete real-name verification (upload ID card, instant approval)
4. Create application and select "VAT Invoice Recognition"
5. Copy your **API Key** and **Secret Key**

### Step 3: Configure

Run the setup wizard:
```bash
python src/main_baidu.py --setup
```

Or manually create `config.txt`:
```
BAIDU_API_KEY=your_api_key_here
BAIDU_SECRET_KEY=your_secret_key_here
```

### Step 4: Test

```bash
# Preview files
python src/main_baidu.py -i ./fp --list

# Process invoices
python src/main_baidu.py -i ./fp
```

---

## Detailed Setup Instructions

### Step 1: Install Dependencies

#### Option A: Using pip

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using conda

```bash
# Create conda environment
conda create -n invoice-extractor python=3.10

# Activate environment
conda activate invoice-extractor

# Install dependencies
pip install -r requirements.txt
```

#### Option C: Using poetry

```bash
# Install poetry first: https://python-poetry.org/docs/#installation

# Install dependencies
poetry install

# Run with poetry
poetry run python src/main_baidu.py
```

### Step 2: Get Baidu OCR Credentials

#### 2.1 Register Baidu Cloud Account

1. Visit https://cloud.baidu.com/
2. Click "Register" or "Login"
3. Complete registration with phone number
4. Verify email (optional but recommended)

#### 2.2 Real-name Verification

**Required for free tier access**

1. Go to console after login
2. Click "Account" → "Real-name Verification"
3. Choose "Personal Verification"
4. Upload ID card photos (front and back)
5. Wait for automatic approval (usually instant)

**Note:** Enterprise verification is also available for business accounts.

#### 2.3 Create OCR Application

1. Go to https://cloud.baidu.com/product/ocr
2. Click "Get Started" or "Console"
3. Select "Create Application"
4. Fill in application details:
   - **Application Name**: Invoice Extractor (or any name)
   - **Application Description**: Invoice recognition tool
   - **Interface Selection**: Check "VAT Invoice Recognition"
5. Click "Create"

#### 2.4 Get API Keys

After creating the application, you'll see:
- **AppID**: Application ID
- **API Key**: For API authentication
- **Secret Key**: For API authentication

**Important:** Copy the **API Key** and **Secret Key** immediately. You'll need them for configuration.

### Step 3: Configure the Tool

#### Option A: Configuration Wizard (Recommended)

```bash
cd src
python main_baidu.py --setup
```

Follow the prompts:
```
Invoice Extractor - Setup Wizard
================================
Configure Baidu OCR now? (y/n): y
Enter Baidu API Key: [paste your API key]
Enter Baidu Secret Key: [paste your secret key]
[OK] Configuration saved to: config.txt
```

#### Option B: Manual Configuration

Create `config.txt` in project root:

```
# Invoice Extractor Configuration
# Get your API credentials from https://cloud.baidu.com/product/ocr

BAIDU_API_KEY=3yrSX2UuhRpzgdiLBD3D1GDr
BAIDU_SECRET_KEY=ZP6MY4DF6RR6GQhD66p5xrifSWXk2TZl
OCR_ENGINE=baidu
```

**Security Tips:**
- Never commit `config.txt` to version control
- Add `config.txt` to `.gitignore`
- Use environment variables for CI/CD

#### Option C: Environment Variables

```bash
# Windows (Command Prompt)
set BAIDU_API_KEY=your_api_key
set BAIDU_SECRET_KEY=your_secret_key

# Windows (PowerShell)
$env:BAIDU_API_KEY="your_api_key"
$env:BAIDU_SECRET_KEY="your_secret_key"

# macOS/Linux
export BAIDU_API_KEY="your_api_key"
export BAIDU_SECRET_KEY="your_secret_key"
```

### Step 4: Test Installation

#### 4.1 Verify Configuration

```bash
python -c "
from src.config import Config
Config.load_from_file()
print('API Key:', Config.BAIDU_API_KEY[:10] + '...' if Config.BAIDU_API_KEY else 'Not set')
print('Secret Key:', 'Set' if Config.BAIDU_SECRET_KEY else 'Not set')
"
```

#### 4.2 Test with Sample Invoice

1. Place a test invoice (image or PDF) in `fp/` directory
2. Preview files:
   ```bash
   python src/main_baidu.py -i ./fp --list
   ```
3. Process:
   ```bash
   python src/main_baidu.py -i ./fp
   ```
4. Check `output/` directory for Excel file

---

## Usage Examples

### Basic Usage

```bash
# Process all invoices in fp/ directory
python src/main_baidu.py

# Process specific directory
python src/main_baidu.py -i ./my_invoices

# Process single file
python src/main_baidu.py -f invoice.pdf

# Process multiple files
python src/main_baidu.py -f 1.pdf -f 2.png -f 3.jpg

# Custom output
python src/main_baidu.py -i ./fp -o ./reports -n "March_2024"
```

### Advanced Usage

```bash
# Preview before processing
python src/main_baidu.py -i ./fp --list

# Process with custom credentials
python src/main_baidu.py -i ./fp --api-key "xxx" --secret-key "yyy"

# Batch process with helper script
python scripts/batch_process.py ./invoices -o ./output -n "Q1_2024"

# Verify export quality
python scripts/verify_export.py output/invoice_info.xlsx
```

---

## Troubleshooting

### Authentication Failed

**Symptom**: "Baidu OCR authentication failed"

**Solutions**:
1. Check API Key and Secret Key in `config.txt`
2. Verify no extra spaces or newlines in the values
3. Ensure credentials are from OCR service (not other Baidu services)
4. Check if account has real-name verification
5. Try regenerating keys in Baidu Cloud console

### No Invoice Files Found

**Symptom**: "No invoice files found"

**Solutions**:
1. Check files are in correct directory
2. Verify file extensions (.pdf, .png, .jpg, etc.)
3. Ensure files are not corrupted
4. Use `--list` flag to see what files are detected

### Image Format Error

**Symptom**: "image format error"

**Solutions**:
1. For PDF files: Ensure PDF is not password-protected
2. For images: Check image is not corrupted
3. Try converting file to different format
4. Check if file is actually an image/PDF (not renamed)

### Network Issues

**Symptom**: Connection timeout or API errors

**Solutions**:
1. Check internet connection
2. Verify firewall allows HTTPS to aip.baidubce.com
3. Try again later (Baidu API may have temporary issues)
4. Check if you're behind a corporate proxy

### Module Not Found

**Symptom**: "ModuleNotFoundError: No module named 'xxx'"

**Solutions**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or install specific package
pip install pandas openpyxl requests PyMuPDF Pillow
```

---

## Free Tier Limits

- **Daily quota**: 50,000 requests/day
- **QPS limit**: 2 requests/second (free tier)
- **Sufficient for**: Personal/small business use

**Rate Limiting:**
If you hit the QPS limit, the tool will automatically retry with exponential backoff.

**Upgrading:**
If you need higher limits, upgrade in Baidu Cloud console. Paid tiers offer:
- Higher QPS (10-100+)
- Priority support
- SLA guarantees

---

## Directory Structure

After setup, your project should look like:

```
invoice-extractor/
├── fp/                      # Place invoice files here
├── output/                  # Excel output directory
├── src/
│   ├── main_baidu.py       # Main entry point
│   ├── baidu_ocr_extractor.py
│   ├── invoice_model.py
│   ├── excel_exporter.py
│   └── config.py
├── scripts/
│   ├── batch_process.py    # Batch processing helper
│   └── verify_export.py    # Export verification
├── config.txt              # Your API credentials (gitignored)
├── config.template.txt     # Template for new users
├── requirements.txt        # Dependencies
├── SKILL.md                # Skill documentation
├── setup.md                # This file
└── examples.md             # Usage examples
```

---

## Next Steps

1. Read [SKILL.md](SKILL.md) for detailed usage
2. Check [examples.md](examples.md) for common use cases
3. Explore [scripts/](scripts/) for utility scripts
4. Visit https://cloud.baidu.com/doc/OCR/index.html for API documentation

## Getting Help

- **Issues**: Check troubleshooting section above
- **Baidu OCR**: https://cloud.baidu.com/doc/OCR/index.html
- **Examples**: See [examples.md](examples.md)
