# OCAX Passport Tool

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from skill import handle_command

def run(input_text: str) -> str:
    """运行 OCAX Passport 技能"""
    # 解析命令
    parts = input_text.strip().split()
    
    if not parts:
        command = "passport"
        args = ""
    else:
        command = parts[0]
        args = " ".join(parts[1:])
    
    return handle_command(command, args)


if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    print(run(text))
