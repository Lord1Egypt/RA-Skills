#!/usr/bin/env python3
"""
parse_docx.py v2.0 - Extract document structure from Word files for ISO 20000-1 gap analysis
Improvements:
1. Better error handling and logging
2. Support for .doc files (using antiword)
3. Improved structure extraction
4. Command-line argument validation
5. Detailed logging
"""

import json
import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parse_docx.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def parse_docx(file_path):
    """
    Parse Word document (.docx) and extract structure.
    For .doc files, use antiword or LibreOffice to convert first.
    """
    logger.info(f"Starting to parse file: {file_path}")
    
    # Validate file path
    if not file_path:
        error_msg = "File path is empty"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}
    
    if not os.path.exists(file_path):
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}
    
    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        error_msg = f"File is empty: {file_path}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}
    
    logger.info(f"File size: {file_size} bytes")
    
    # Process different file formats
    if file_path.endswith('.txt'):
        logger.info("Processing .txt file")
        return parse_txt(file_path)
    
    elif file_path.endswith('.docx'):
        logger.info("Processing .docx file")
        return parse_docx_file(file_path)
    
    elif file_path.endswith('.doc'):
        logger.warning("(.doc file detected, attempting to convert with antiword")
        return parse_doc_with_antiword(file_path)
    
    else:
        error_msg = f"Unsupported file format: {file_path}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "status": "failed",
            "suggestion": "Please convert to .docx or .txt format"
        }

def parse_txt(file_path):
    """Parse text file"""
    try:
        # Try different encodings
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                logger.info(f"Successfully read file with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            error_msg = "Failed to decode file with any supported encoding"
            logger.error(error_msg)
            return {"error": error_msg, "status": "failed"}
        
        return extract_structure(content, file_path)
    
    except Exception as e:
        error_msg = f"Failed to parse .txt file: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}

def parse_docx_file(file_path):
    """Parse .docx file using python-docx"""
    try:
        from docx import Document
        
        logger.info("Loading .docx file with python-docx")
        doc = Document(file_path)
        
        # Extract text from paragraphs
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        content = '\n'.join(paragraphs)
        
        logger.info(f"Extracted {len(paragraphs)} paragraphs")
        return extract_structure(content, file_path)
    
    except ImportError:
        error_msg = "python-docx not installed. Install with: pip install python-docx"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}
    
    except Exception as e:
        error_msg = f"Failed to parse .docx: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}

def parse_doc_with_antiword(file_path):
    """Try to convert .doc file using antiword"""
    try:
        # Try antiword first
        output_file = file_path + '.txt'
        logger.info(f"Attempting to convert .doc to .txt using antiword")
        
        import subprocess
        result = subprocess.run(
            ['antiword', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Save converted text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            logger.info(f"Successfully converted .doc to {output_file}")
            return parse_txt(output_file)
        else:
            error_msg = f"antiword conversion failed: {result.stderr}"
            logger.error(error_msg)
            return {"error": error_msg, "status": "failed"}
    
    except FileNotFoundError:
        error_msg = "antiword not found. Please install antiword or convert .doc to .docx manually"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}
    
    except Exception as e:
        error_msg = f"Failed to convert .doc file: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}

def extract_structure(content, file_path):
    """Extract document structure from text content"""
    logger.info("Extracting document structure")
    
    lines = content.split('\n')
    logger.info(f"Total lines: {len(lines)}")
    
    result = {
        "file_name": os.path.basename(file_path),
        "file_path": file_path,
        "file_size": os.path.getsize(file_path),
        "total_lines": len(lines),
        "headings": [],
        "responsibilities": [],
        "process_steps": [],
        "records": [],
        "clause_mapping": {},
        "high_voltage_lines": {
            "change_grading": False,
            "incident_handling": False,
            "raci_responsibilities": False,
            "supplier_risk": False,
            "sla_reporting": False
        },
        "status": "success",
        "parsed_at": datetime.now().isoformat()
    }
    
    current_heading = ""
    in_responsibility_section = False
    in_process_section = False
    in_record_section = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Skip empty lines
        if not line_stripped:
            continue
        
        # Detect headings (improved heuristic)
        if is_heading(line_stripped):
            current_heading = line_stripped
            result["headings"].append({
                "level": guess_heading_level(line_stripped),
                "text": line_stripped,
                "line_number": i
            })
            logger.debug(f"Found heading: {line_stripped}")
        
        # Detect section transitions
        if '职责' in line_stripped:
            in_responsibility_section = True
            in_process_section = False
            in_record_section = False
        elif '工作程序' in line_stripped or '流程' in line_stripped:
            in_process_section = True
            in_responsibility_section = False
            in_record_section = False
        elif '记录' in line_stripped or '表单' in line_stripped:
            in_record_section = True
            in_responsibility_section = False
            in_process_section = False
        
        # Extract responsibilities
        if in_responsibility_section and is_responsibility_line(line_stripped):
            result["responsibilities"].append(line_stripped)
        
        # Extract process steps
        if in_process_section and is_process_step(line_stripped):
            result["process_steps"].append(line_stripped)
        
        # Extract records
        if in_record_section and is_record_line(line_stripped):
            result["records"].append(line_stripped)
        
        # Detect high-voltage lines (improved detection)
        detect_high_voltage_lines(line_stripped, result["high_voltage_lines"])
    
    # Clause mapping (improved heuristic)
    map_clauses(content, result["clause_mapping"])
    
    logger.info(f"Extraction complete: {len(result['headings'])} headings, "
                f"{len(result['responsibilities'])} responsibilities, "
                f"{len(result['process_steps'])} process steps, "
                f"{len(result['records'])} records")
    
    return result

def is_heading(line):
    """Check if a line is a heading"""
    # Short lines with section keywords
    if len(line) > 0 and len(line) < 50:
        keywords = ['目的', '范围', '职责', '工作程序', '流程', '记录', '术语', 
                   '管理内容', '控制要求', '相关文件', '附录']
        return any(keyword in line for keyword in keywords)
    return False

def guess_heading_level(line):
    """Guess heading level based on content"""
    if '目的' in line or '范围' in line or '职责' in line:
        return 1
    elif '工作程序' in line or '流程' in line:
        return 2
    else:
        return 3

def is_responsibility_line(line):
    """Check if line contains responsibility information"""
    return '负责' in line or '|' in line or '部门' in line

def is_process_step(line):
    """Check if line is a process step"""
    if not line:
        return False
    # Numbered steps
    if line[0] in '123456789' and ('.' in line or '、' in line):
        return True
    # Lines with action verbs
    action_verbs = ['识别', '分析', '制定', '实施', '评审', '确认', '记录']
    return any(verb in line for verb in action_verbs)

def is_record_line(line):
    """Check if line is a record/form"""
    return '《' in line and '》' in line

def detect_high_voltage_lines(line, high_voltage_dict):
    """Detect high-voltage line keywords in a line"""
    if '变更' in line and ('重大' in line or '窗口' in line or '00:00' in line):
        high_voltage_dict["change_grading"] = True
    if '先恢复' in line or '业务恢复' in line or '临时措施' in line:
        high_voltage_dict["incident_handling"] = True
    if '归口' in line or ('负责' in line and '部门' in line):
        high_voltage_dict["raci_responsibilities"] = True
    if '供应商' in line and ('单一' in line or '风险' in line or '备份' in line):
        high_voltage_dict["supplier_risk"] = True
    if '报告' in line and ('SLA' in line or '指标' in line or '完成' in line):
        high_voltage_dict["sla_reporting"] = True

def map_clauses(content, clause_dict):
    """Map content to ISO 20000-1 clauses"""
    content_lower = content.lower()
    
    # Clause mapping based on keywords
    clause_keywords = {
        "8.5.1": ['变更', 'change'],
        "8.4.1": ['事件', 'incident', '故障'],
        "8.4.2": ['问题', 'problem', 'RCA'],
        "8.3.3": ['供应商', 'supplier', '外部提供'],
        "9.4": ['报告', 'report', 'SLA'],
        "9.3": ['服务级别', 'service level', 'SLA'],
        "9.5.3": ['配置', 'configuration', 'CMDB'],
        "7.5": ['文件', 'document', '成文信息'],
        "7.2": ['能力', 'competence', '培训'],
        "9.2": ['内审', 'internal audit', '审核']
    }
    
    for clause, keywords in clause_keywords.items():
        if any(keyword in content for keyword in keywords):
            clause_dict[clause] = True
    
    return clause_dict

def main():
    """Main function with command-line interface"""
    logger.info("=" * 60)
    logger.info("parse_docx.py v2.0 - ISO 20000-1 Document Parser")
    logger.info("=" * 60)
    
    # Validate command-line arguments
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python parse_docx.py <file_path> [output_json_path]")
        print("\nExamples:")
        print("  python parse_docx.py document.txt")
        print("  python parse_docx.py document.docx output.json")
        print("\nSupported formats: .txt, .docx, .doc (requires antiword)")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    logger.info(f"Input file: {file_path}")
    if output_path:
        logger.info(f"Output file: {output_path}")
    
    # Parse the file
    result = parse_docx(file_path)
    
    # Output results
    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"Output written to: {output_path}")
            print(f"\n✅ Output written to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to write output file: {str(e)}")
            print(f"\n❌ Failed to write output file: {str(e)}")
            sys.exit(1)
    else:
        # Print to stdout
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Parsing Summary")
    print("=" * 60)
    print(f"File: {result.get('file_name', 'Unknown')}")
    print(f"Status: {result.get('status', 'unknown')}")
    print(f"Headings found: {len(result.get('headings', []))}")
    print(f"Responsibilities found: {len(result.get('responsibilities', []))}")
    print(f"Process steps found: {len(result.get('process_steps', []))}")
    print(f"Records found: {len(result.get('records', []))}")
    print(f"Clause mapping: {result.get('clause_mapping', {})}")
    print(f"High-voltage lines detected: {result.get('high_voltage_lines', {})}")
    print("=" * 60)
    
    # Exit with appropriate code
    if result.get('status') == 'success':
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
