# 📚 Image Knowledge Converter (图片知识库整理工具)

> Automatically convert phone screenshots into structured Word + Markdown knowledge documents with AI-powered categorization.  
> **First-time users get an interactive setup wizard — no technical background required!**

<p align="center">
  <img src="https://raw.githubusercontent.com/haoyiyong985/image-knowledge-converter/main/demo.gif" alt="Demo" width="480">
</p>

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/haoyiyong985/image-knowledge-converter?style=social)](https://github.com/haoyiyong985/image-knowledge-converter)
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Skill-green)](https://workbuddy.ai)

🌐 [中文](README.md) | [English](README_EN.md)

---

## 🌟 Overview

**Image Knowledge Converter** is an AI-powered knowledge management tool that:

- 📷 **Auto OCR**: Extract text from phone screenshots (Xiaohongshu, WeChat Reading, WeChat, etc.)
- 🏷️ **Smart Categorization**: AI understands content and automatically classifies it into knowledge themes
- 📝 **Generate Documents**: Output structured Word + Markdown dual-format documents
- 🔗 **Auto Archive**: Organize images and documents by category
- 🔄 **Content Deduplication**: Similar topics are automatically merged to avoid duplicates
- ☁️ **Cloud Sync**: One-click sync to IMA personal notes

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| **Multi-Engine OCR** | Tencent Cloud → Baidu Cloud → Local Tesseract (auto fallback) |
| **AI Smart Categorization** | Dynamic category system with free naming and auto category creation |
| **Document Merging** | Same-topic content auto-merged into one document |
| **Dual-Format Output** | Simultaneously generates `.docx` and `.md` files |
| **IMA Sync** | Auto sync to IMA notes (supports incremental updates) |
| **Batch Processing** | Smart batch splitting for large volumes, with resume support |
| **Duplicate Detection** | Hash + topic similarity double-check |
| **Newbie Wizard** | Interactive setup wizard on first run — no tech background needed |

### Technical Highlights

- ✅ **Full LLM Coverage**: Hunyuan Lite / Kimi / Doubao multi-model fallback
- ✅ **Smart Naming**: `{Category}-{Topic}` format, e.g., `History-Qian Qianyi Biography`
- ✅ **Content Cleanup**: Auto-fix OCR errors, structured formatting
- ✅ **Source Extraction**: Auto-identify platform sources (Xiaohongshu, WeChat, etc.)
- ✅ **Newbie Wizard**: Interactive first-run configuration wizard

---

## 🚀 Quick Start (3 Steps)

> **No need to choose an installation method!** No matter which way you install, the first run will **auto-launch the Newbie Wizard** to guide you through setup.

### Step 1: Choose Installation Method (any one)

#### Method A: WorkBuddy Skill (Easiest ⭐)

**For**: WorkBuddy users who want one-click setup

1. Download `image-knowledge-converter_v1.1.0_skill.zip` from Releases
2. Open WorkBuddy → Top-right avatar → **Skills Management**
3. Click "Import Skills" → Select the zip → "Import Now"
4. **Say to WorkBuddy**: `first time` or `initialize`
5. ✅ The wizard auto-starts and guides you through setup (~2 minutes)

#### Method B: Full Package (More Control ⭐)

**For**: Users who want full control, or without WorkBuddy

1. Download `tupianzhengligongju_wanzheng_v1.1.0.zip` from Releases
2. Extract to your desired location (e.g., `D:\MyImageKnowledgeBase`)
3. Open terminal, enter the extracted directory
4. Run: `python setup_wizard.py`
5. ✅ The wizard auto-starts and guides you through setup (~2 minutes)

#### Method C: Git Clone (For Developers)

**For**: Developers familiar with Git and CLI

```bash
git clone https://github.com/haoyiyong985/image-knowledge-converter.git
cd image-knowledge-converter
pip install -r requirements.txt
python setup_wizard.py   # ← Launch wizard
```

---

### Step 2: Newbie Wizard (Auto-Starts)

No matter which method you choose, **you'll see this wizard on first run** (cannot be skipped):

```
==================================================
  Welcome to Image Knowledge Converter!
  I'm your smart assistant. First time? Let me help you set up.
  Just 3 steps, about 2 minutes.

  If you have any questions, just ask me!
==================================================
```

#### Wizard Flow (3 Steps, ~2 Minutes)

**Step 1: Choose Working Folder**
```
  Step 1: Choose Working Folder
  ℹ️ This is where images and generated documents will be stored.

  Suggested: D:\Users\YourUsername\ImageKnowledgeBase

  Use default location? (y/n, press Enter for default):
```

- Press `y` → Auto-creates default folder
- Press `n` → Enter custom path (e.g., `D:\MyImageLibrary`)

**Step 2: Configure OCR Service (pick one)**
```
  Step 2: Configure OCR Recognition Service
  ℹ️ You need at least one OCR service to recognize text in images.

  Please select an OCR service (pick one):
    1. Tencent Cloud OCR (Recommended, 1000 free/month)
      High accuracy, generous free quota
    2. Baidu Cloud OCR (Free, requires real-name)
      Large free quota, suitable for heavy use
    3. Local Tesseract (Completely free)
      No internet needed, but lower accuracy

  Enter option number (1-3):
```

- **Option 1 (Tencent Cloud)** → Wizard shows tutorial → You fill in `config/api_keys_template.txt` → Wizard auto-reads and generates config
- **Option 2 (Baidu Cloud)** → Wizard shows tutorial → You fill in `config/api_keys_template.txt` → Wizard auto-reads and generates config
- **Option 3 (Local)** → Wizard prompts Tesseract installation → Config complete

**Step 3: Create Folder Structure**
```
  Step 3: Create Folder Structure
  ✅ Created folder: Pending Images
  ✅ Created folder: Processed Images
  ✅ Created folder: Processing Results

  ✅ Config saved to config/api_keys.yaml
```

**Step 4 (Optional): Configure IMA Sync**
```
  (Optional) Configure IMA Sync
  ℹ️ IMA is a note service that can automatically sync your generated documents.
  ℹ️ If you don't use IMA, you can skip this.

  Configure IMA sync? (y/n):
```

- Press `y` → Wizard prompts for IMA API Key → You fill in `config/api_keys_template.txt` → Wizard auto-reads and generates config
- Press `n` → Skip, you can re-run wizard anytime to add it

**Done!**
```
==================================================
  🎉 Setup Complete!
==================================================

  Next steps:
  1. Put images to process in the "Pending Images" folder
  2. Run: python auto_process_all_v9_4.py
  3. Wait for processing, results are in "Processing Results" folder
```

---

### Step 3: Drop Images and Process

#### If Using WorkBuddy Skill (Method A)

1. Put images in: `YourWorkingFolder\Pending Images\`
2. Say to WorkBuddy: `process new images`
3. Wait for processing (~3-5 seconds/image)
4. Results in: `YourWorkingFolder\Processing Results\`

#### If Running Locally (Method B or C)

1. Put images in: `YourWorkingFolder\Pending Images\`
2. Run: `python auto_process_all_v9_4.py`
3. Wait for processing (~3-5 seconds/image)
4. Results in: `YourWorkingFolder\Processing Results\`

---

## 📖 User Guide

### Directory Structure

```
ImageKnowledgeBase\
├── auto_process_all_v9_4.py   ← Main processing script (V9.5 logic)
├── setup_wizard.py            ← Newbie wizard script
├── requirements.txt
├── config\
│   └── api_keys.yaml        ← OCR/IMA config (auto-generated by wizard)
├── Pending Images（待处理图片）\                ← Drop images to process here
│   ├── Health\
│   ├── Travel\
│   └── ...
├── Processed Images（已处理图片）\                ← Processed images auto-archived
└── Processing Results（处理结果）\                  ← Generated Word/Markdown docs
    ├── History-Qian Qianyi Biography.docx
    ├── History-Qian Qianyi Biography.md
    └── ...
```

### Daily Usage Flow

#### Step 1: Add New Images

Copy phone screenshots to the `Pending Images` folder (supports subfolder categorization):

```
Pending Images\Health\  ← Health-related images
Pending Images\Travel\  ← Travel-related images
```

#### Step 2: Start Processing

**WorkBuddy Users**:
```
process new images
```

**Local Users**:
```bash
python auto_process_all_v9_4.py
```

#### Step 3: View Results

After processing, open the `Processing Results` folder and you'll see:

```
Processing Results\
├── History-Qian Qianyi Biography.docx    ← Word format (editable)
├── History-Qian Qianyi Biography.md     ← Markdown format (plain text)
├── Health-Anti-Inflammatory Diet.docx
└── Health-Anti-Inflammatory Diet.md
```

---

## ⚙️ Configuration

### Secure API Key Handling (Security Improvement ⭐)

**New users note**: To protect your API keys, **you no longer need to send keys to WorkBuddy**!

We use **local TXT file** for key transfer:
1. The wizard teaches you how to get API keys
2. You fill keys in `config/api_keys_template.txt` (with detailed instructions)
3. Save and press Enter to continue
4. The wizard auto-reads the TXT file and generates encrypted YAML config

**Advantages**:
- ✅ Keys never appear in chat history
- ✅ Keys are not transmitted over the network (except normal API calls)
- ✅ You can edit files locally in a secure environment

TXT template path: `config/api_keys_template.txt` (auto-created by wizard)

---

### API Key Configuration (Auto-completed by wizard)

The wizard will generate the following in `config/api_keys.yaml`:

```yaml
# OCR Services (configure at least one)
ocr:
  tencent:
    secret_id: "Your Tencent Cloud SecretId"
    secret_key: "Your Tencent Cloud SecretKey"

  # OR Baidu Cloud
  baidu:
    api_key: "Your Baidu Cloud API Key"
    secret_key: "Your Baidu Cloud Secret Key"

# IMA Sync (optional, wizard will ask if you want to configure)
ima:
  api_key: "Your IMA API Key"
  base_url: "https://api.ima.tencent.com/v1"
```

### How to Get API Keys (Wizard will guide you step by step)

| Service | Free Quota | Get Started | Wizard Support |
|---------|------------|-------------|----------------|
| Tencent Cloud OCR | 1000/month | https://console.cloud.tencent.com/cam/capi | ✅ Tutorial |
| Baidu Cloud OCR | 50000/day | https://console.bce.baidu.com/ | ✅ Tutorial |
| Local Tesseract | Completely free | https://github.com/UB-Mannheim/tesseract/wiki | ✅ Setup guide |

---

## 📊 Category System

### Preset Categories (Auto-expanding)

| Category | Description | Examples |
|----------|-------------|----------|
| **History & Culture** | History, biographies, cultural knowledge | Qian Qianyi Biography, Southern Song History |
| **Health & Nutrition** | Diet, nutrition, health knowledge | Anti-inflammatory diet, gut health |
| **Lifestyle** | Exercise, sleep, daily advice | Daily diet recommendations |
| **Education & Parenting** | Education methods, parenting knowledge | - |
| **Travel & Guides** | Travel logs, attraction guides | - |

### Dynamic Categories

When content doesn't fit preset categories, AI will:
1. Automatically determine a new topic name
2. Freely name the category
3. Create the new category and archive

**Examples**:
- Image content is about "Photography Tips" → AI auto-creates `Photography` category
- Image content is about "Programming Learning" → AI auto-creates `Programming` category

---

## 💡 Common Commands

### WorkBuddy Users

You can use these in WorkBuddy conversation:

| Command | Effect |
|---------|--------|
| `first time` or `initialize` | Launch newbie wizard (first-time setup) |
| `process new images` | Process all pending images |
| `process pending images/Health` | Only process images in specified folder |
| `view existing documents` | List all documents and chapter lists |
| `reconfigure` | Re-run wizard to update config |

### Local Users

```bash
# Launch newbie wizard (first time)
python setup_wizard.py

# Process images
python auto_process_all_v9_4.py

# Batch processing (large volumes)
python auto_process_all_v9_4.py --batch

# Check progress
python auto_process_all_v9_4.py --progress

# Clear state
python auto_process_all_v9_4.py --clear
```

---

## 📂 Output Examples

### Processing Results Directory

```
Processing Results\
├── History-Qian Qianyi Biography.docx
├── History-Qian Qianyi Biography.md
├── History-Overview of Southern Song History.docx
├── History-Overview of Southern Song History.md
└── ...
```

### Document Content Structure

```markdown
# History-Qian Qianyi Biography

## I. Biography
(OCR extracted content, auto-segmented by AI)

## II. Major Achievements
(Structured organization)

## III. Historical Evaluation
(Auto-classified and archived)
```

---

## 🔧 Advanced Features

### Batch Processing

When processing large volumes, the system auto-splits batches:

| Image Size | Batch Size |
|-----------|-----------|
| < 500KB | 10 images/batch |
| 500KB-2MB | 6 images/batch |
| 2MB-5MB | 4 images/batch |
| > 5MB | 2 images/batch |

### Resume Processing

If processing is interrupted, you can resume:

```bash
python auto_process_all_v9_4.py --batch
```

Check progress:

```bash
python auto_process_all_v9_4.py --progress
```

Clear state:

```bash
python auto_process_all_v9_4.py --clear
```

---

## 🐛 FAQ

### Q1: I'm a complete beginner, can I use this?

**Answer**: Absolutely!  
- First run auto-launches the **Newbie Wizard**, guiding you step by step
- Just 2 minutes, no technical background needed
- After setup, just say "process new images" each time

### Q2: OCR recognition fails?

**Solution**:
1. Check image clarity (recommend resolution ≥ 150 DPI)
2. Confirm Tencent Cloud/Baidu Cloud OCR is configured
3. Install local Tesseract as fallback

### Q3: Document naming not as expected?

**Solution**:
- Document format: `{Category}-{Topic}`
- Auto-generated by AI, aligned with content theme
- To customize, modify naming rules in `auto_process_all_v9_4.py`

### Q4: How to avoid duplicate content?

**Solution**:
- System auto-detects duplicates (Hash + topic similarity)
- Duplicate images are automatically skipped

### Q5: IMA sync fails?

**Solution**:
1. Check `config/api_keys.yaml` IMA config is correct
2. Confirm credentials are not expired
3. Re-run wizard: `python setup_wizard.py`

---

## 📈 Performance Metrics

- **Processing Speed**: ~3-5 seconds/image (depends on OCR engine)
- **Recognition Accuracy**: 90%+ Chinese (Tencent Cloud OCR)
- **Supported Formats**: JPG, PNG, WEBP, BMP
- **Output Formats**: Word (.docx) + Markdown (.md)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **OCR** | Tencent Cloud, Baidu Cloud, Tesseract |
| **AI Analysis** | Hunyuan Lite, Kimi, Doubao |
| **Document Generation** | python-docx |
| **Sync** | IMA OpenAPI |
| **Language** | Python 3.8+ |

---

## 📄 File Guide

### Core Scripts

| File | Description |
|------|-------------|
| `auto_process_all_v9_4.py` | Current latest version (V9.5 logic) |
| `setup_wizard.py` | Newbie wizard script (auto-launches on first run) |
| `ima_sync.py` | IMA sync script |
| `classifier_engine.py` | Classification engine |

### Configuration Files

| File | Description |
|------|-------------|
| `config/api_keys.yaml` | OCR/IMA credentials (auto-generated by wizard) |
| `requirements.txt` | Python dependency list |
| `.env` | Environment variables (not committed to Git) |

---

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Changelog

### v1.1.0 (2026-04-27) 🆕

- ✅ **Built-in Newbie Wizard** (auto-launches on first run)
- ✅ Support for tutorial-based API key acquisition
- ✅ Auto-create folder structure
- ✅ Updated to V9.5 processing logic
- ✅ Removed "General Knowledge" catch-all category
- ✅ Support LLM free naming for categories
- ✅ Added `setup_wizard.py` wizard script

### v1.0.0 (2026-03-17)

- ✅ Initial release
- ✅ OCR support (Tencent Cloud, Baidu Cloud, Tesseract)
- ✅ AI smart categorization and document merging
- ✅ Word + Markdown dual-format output
- ✅ IMA sync feature

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [WorkBuddy](https://workbuddy.ai) - AI assistant platform
- [Tencent Cloud OCR](https://cloud.tencent.com/product/ocr) - OCR service
- [Baidu Cloud OCR](https://ai.baidu.com/tech/ocr) - OCR service
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - Open-source OCR engine

---

## 📧 Contact

- GitHub Issues: [Submit an issue](https://github.com/haoyiyong985/image-knowledge-converter/issues)
- Email: (add your contact)

---

**⭐ If this project helps you, please give it a star!**
