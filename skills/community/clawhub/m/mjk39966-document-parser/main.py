import docx
import pdfplumber
from pathlib import Path

def parse_document(file_path):
    file_path = Path(file_path)
    text = ""
    
    if file_path.suffix in [".docx", ".doc"]:
        # 解析 Word 文档
        doc = docx.Document(str(file_path))
        text = "\n".join([para.text for para in doc.paragraphs])
        
    elif file_path.suffix == ".pdf":
        # 解析 PDF 文档
        with pdfplumber.open(str(file_path)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    
    return {"text": text, "status": "success"}

# 如果是直接运行此脚本（测试用）
if __name__ "__main__":
    import sys
    result = parse_document(sys.argv[1])
    print(result["text"])
