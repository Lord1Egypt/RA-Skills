#!/usr/bin/env python3
"""
生成 DOCX 編輯的 Unified Diff 報告
用法：
  python generate_diff.py old.docx new.docx output.diff.md
"""

import sys
from pathlib import Path
import subprocess


def docx_to_text(docx_path):
    """使用 mammoth 轉換 DOCX 為純文字"""
    try:
        result = subprocess.run(
            ["uvx", "mammoth", "--output-format=markdown", str(docx_path)],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"錯誤：轉換失敗 {e}")
        return ""


def generate_unified_diff(old_text, new_text, old_name, new_name):
    """生成 Unified Diff 格式"""
    import difflib
    
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=old_name,
        tofile=new_name,
        lineterm='\n'
    )
    
    return ''.join(diff)


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    
    old_docx = Path(sys.argv[1])
    new_docx = Path(sys.argv[2])
    output_diff = Path(sys.argv[3])
    
    if not old_docx.exists():
        print(f"錯誤：文件不存在 {old_docx}")
        sys.exit(1)
    
    if not new_docx.exists():
        print(f"錯誤：文件不存在 {new_docx}")
        sys.exit(1)
    
    print(f"📄 轉換舊版本：{old_docx}")
    old_text = docx_to_text(old_docx)
    
    print(f"📄 轉換新版本：{new_docx}")
    new_text = docx_to_text(new_docx)
    
    print(f"📊 生成 Unified Diff...")
    diff_text = generate_unified_diff(old_text, new_text, str(old_docx), str(new_docx))
    
    # 寫出 diff 文件
    with open(output_diff, 'w', encoding='utf-8') as f:
        f.write("# DOCX 編輯差異報告\n\n")
        f.write(f"**舊版本:** {old_docx}\n\n")
        f.write(f"**新版本:** {new_docx}\n\n")
        f.write("```diff\n")
        f.write(diff_text)
        f.write("```\n")
    
    print(f"✅ 差異報告已保存：{output_diff}")
    
    # 同時輸出到 stdout
    print("\n" + "="*60)
    print(diff_text)


if __name__ == "__main__":
    main()
