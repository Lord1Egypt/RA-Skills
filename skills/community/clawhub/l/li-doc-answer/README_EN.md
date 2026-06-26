# Li_doc_answer - User Guide

## Overview

**Li_doc_answer** is a **universal Word document processing tool** with AI-powered answer generation. It supports batch processing, conversion, and automatic answer generation for any doc/docx format documents.

> ⚠️ **Note:** This skill is not limited to specific topics or subjects - it can process any Word document (educational question banks, office documents, reports, etc.)

## 🎯 v3.0 Core Feature: AI Answer Generation

**Input:** Any doc/docx document (with questions)  
**Process:** Auto-detect all questions + AI generate reference answers  
**Output:** Document with complete answers

### Usage Example

```bash
# AI automatic answer generation
python3 scripts/ai_generate_answers.py questions.doc

# Output: questions_AI_Answers.docx
# Contains: All questions + Reference answers for each
```

### Supported Question Types

| Type | Auto-Detect | Answer Template |
|------|-------------|-----------------|
| True/False | ✅ | Correct/Incorrect + Reason |
| Single Choice | ✅ | Correct Option + Analysis |
| Multiple Choice | ✅ | Correct Options + Analysis |
| Short Answer | ✅ | Key Points 1/2/3 + Details |
| Essay | ✅ | Introduction + Body + Conclusion |
| Case Analysis | ✅ | Problem + Theory + Solution + Summary |
| Fill-in-Blank | ✅ | Correct Answer |
| Term Explanation | ✅ | Definition + Features + Significance |

## Use Cases

- 📚 Educational/training question bank processing (any subject)
- 📄 Enterprise office document batch conversion
- 📝 Document content organization and archiving
- 🔄 doc ↔ docx format unification
- 📋 Document answer/note batch addition

## Quick Start

### 1. Install Dependencies

```bash
pip3 install python-docx mammoth
```

### 2. Install Skill

```bash
clawhub install li-doc-answer
```

### 3. Usage Examples

#### AI Answer Generation (v3.0 Core)

```bash
python3 scripts/ai_generate_answers.py /path/to/questions.doc
```

#### Process Single Document

```bash
python3 scripts/generate_answers.py /path/to/document.doc
```

#### Batch Process Directory

```bash
# Place files to process in data/ directory
python3 scripts/generate_all_answers.py
```

#### Format Conversion

```bash
python3 scripts/convert_md_to_docx.py input.md output.docx
```

#### Document Validation

```bash
python3 scripts/check_answers.py document.docx
```

## Supported Document Types

| Type | Support | Description |
|------|---------|-------------|
| .doc | ✅ | Legacy Word documents (requires antiword) |
| .docx | ✅ | Modern Word documents |
| .md | ✅ | Markdown to Word conversion |

## Supported Content Types

This skill **does not limit document content topics**, it can process:

- ✅ Any subject question banks (Math, English, Physics, Chemistry, History, etc.)
- ✅ Single choice questions
- ✅ True/False questions
- ✅ Short answer questions
- ✅ Case analysis questions
- ✅ Essay questions
- ✅ Any office documents

## Command Line Arguments

### ai_generate_answers.py (AI Core Feature)

```bash
python3 scripts/ai_generate_answers.py <input_file> [output_file]
```

- `input_file` - Required, path to doc/docx file to process
- `output_file` - Optional, defaults to `input_file_AI_Answers.docx`

### generate_answers.py

```bash
python3 scripts/generate_answers.py <input_file> [output_file]
```

- `input_file` - Required, path to doc/docx file to process
- `output_file` - Optional, defaults to `input_file_processed.docx`

### generate_all_answers.py

```bash
python3 scripts/generate_all_answers.py [directory_path]
```

- `directory_path` - Optional, defaults to `data/` directory

## Output Description

Processed documents will:

1. Retain all original document content
2. Auto-detect all questions
3. Generate reference answers for each question
4. Apply unified formatting
5. Save as .docx format

## FAQ

**Q: Can it only process specific subject documents?**  
A: No! v3.0+ is a universal document processing tool that can handle any subject, any topic.

**Q: Does it support Mac/Windows?**  
A: Yes, uses relative paths for cross-platform deployment.

**Q: Will my document content be leaked?**  
A: No, all operations are performed locally with no network requests.

**Q: Are AI-generated answers accurate?**  
A: AI-generated answers are for reference only. Please refer to textbooks and instructor explanations.

## Author

**Beijing Lao Li** (北京老李)

## Version

3.0.4 (March 2026)

## License

MIT

## Other Languages

- [中文](README.md) - 中文版本

---

## ⚠️ Important Notice

**AI-generated answers are for reference only.** Please refer to textbooks and instructor explanations for authoritative answers.

**Answer Source:** Generated based on general knowledge base. Please supplement with relevant textbooks.
