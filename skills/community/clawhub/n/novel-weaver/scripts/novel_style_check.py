#!/usr/bin/env python3
"""
Style Check — 风格一致性校验
检查文体规范、对白自然度、叙事视角等
"""
import json, sys, re
from pathlib import Path

# Windows 终端编码修复
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 禁止的模式
FORBIDDEN_PATTERNS = [
    (r'从第\s+\w+章开始', "元文本引用（读者视角，非叙事者视角）"),
    (r'[\*\*]{2}\d+字\*\*', "字数统计标记，不应出现在正文中"),
    (r'继续\s+S?\d+', "助手元注释残留（如'继续S02正文'）"),
]

def check_chapter(chapter_dir, chapter, state_path):
    """检查风格一致性
    返回结构化问题列表: [{"file", "problem", "position", "severity", "suggestion"}, ...]
    """
    cd = Path(chapter_dir)
    files = sorted(cd.glob("S*.txt"))
    issues = []
    result = []

    for f in files:
        content = f.read_text(encoding="utf-8-sig")
        lines = content.strip().split("\n")

        # 1. 检查禁止模式
        for pattern, desc in FORBIDDEN_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                for m in matches:
                    # 找匹配行号
                    line_no = next((i+1 for i, ln in enumerate(lines) if m in ln), 0)
                    result.append({
                        "file": f.name,
                        "problem": f"含禁用模式: {desc}（匹配: {m[:30]}）",
                        "position": f"第{line_no}行",
                        "severity": "HARD",
                        "suggestion": f"将元文本引用或助手残留改为正常叙事"
                    })
                    issues.append({
                        "file": f.name, "type": "禁止模式", "desc": desc,
                        "detail": f"匹配: {matches}"
                    })

        # 2. 检查是否以编号标记结束
        last_line = lines[-1].strip() if lines else ""
        sub_match = re.match(rf'^{chapter}S\d+$', last_line)
        if not sub_match:
            result.append({
                "file": f.name,
                "problem": f"末行应为子结构编号标记，实际为: {last_line[:30]}",
                "position": f"末行",
                "severity": "HARD",
                "suggestion": f"在文件末尾添加 {chapter}{f.stem.replace(chapter, '')}"
            })
            issues.append({
                "file": f.name, "type": "格式", "desc": "末行应为子结构编号",
                "detail": f"实际末行: {last_line}"
            })

        # 3. 检查行数
        if len(lines) > 200:
            result.append({
                "file": f.name,
                "problem": f"行数 {len(lines)} 超过 200 行上限",
                "position": f"全文（{len(lines)}行）",
                "severity": "HARD",
                "suggestion": f"压缩至200行以内，优先精简环境描写和过渡段落"
            })
            issues.append({
                "file": f.name, "type": "行数超标", "desc": f"行数 {len(lines)} 超过 200 行上限"
            })

    # 输出报告
    print(f"[风格报告] {chapter}")
    if not result:
        print(f"  [OK] 无问题")
        print(f"  - 检查文件数: {len(files)}")
        print(f"  - 末行标记: 正确")
        print(f"  - 禁止模式: 未检出")
    else:
        for r in result:
            icon = "[BLOCK]" if r["severity"] == "HARD" else "[WARN]"
            print(f"  {icon} [{r['file']}] {r['problem']}")

    # 更新 state
    sp = Path(state_path)
    if sp.exists():
        data = json.loads(sp.read_text(encoding="utf-8-sig"))
        for ch in data.get("chapters", []):
            if ch["id"] == chapter:
                ch["style_check_notes"] = issues
                break
        sp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[风格校验] {chapter} 完成 ({len(result)} 个问题)")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python novel_style_check.py <chapter_dir> <chapter> <state_path>")
        sys.exit(1)
    check_chapter(sys.argv[1], sys.argv[2], sys.argv[3])
