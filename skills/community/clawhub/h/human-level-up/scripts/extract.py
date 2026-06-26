import sys
import json
import re
from pathlib import Path

def extract_key_points(text: str, max_points: int = 5) -> dict:
    """
    从文本中提取认知重点
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    key_points = []

    for i, line in enumerate(lines[:max_points * 2]):
        if len(line) > 20 and len(line) < 200:
            key_points.append({
                "id": len(key_points) + 1,
                "title": f"要点 {len(key_points) + 1}",
                "content": line[:150] + "..." if len(line) > 150 else line
            })
        if len(key_points) >= max_points:
            break

    return {
        "status": "success",
        "count": len(key_points),
        "key_points": key_points
    }

def extract_atomic_units(text: str) -> list:
    """
    从文本中提取认知原子（更细粒度）
    """
    sentences = re.split(r'[。!?\n]', text)
    atoms = []

    for sent in sentences:
        sent = sent.strip()
        if len(sent) > 30 and len(sent) < 300:
            atoms.append(sent)

    return atoms[:10]

def process_file(file_path: str) -> dict:
    """
    处理文件并提取重点
    """
    path = Path(file_path)
    if not path.exists():
        return {"status": "error", "message": f"File not found: {file_path}"}

    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding='gbk')
        except:
            return {"status": "error", "message": f"Encoding error: {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return extract_key_points(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = process_file(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"status": "error", "message": "Usage: extract.py <file_path>"}))