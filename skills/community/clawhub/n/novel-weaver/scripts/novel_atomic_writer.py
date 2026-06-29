#!/usr/bin/env python3
"""
Atomic Writer — 原子写入器（v4，系统组装版）

流程变更（v4）：
  LLM 只输出纯正文 → write-sub 自动组装标题行+别名+末行标记
  atomic_writer 只做正文校验和写入，不再校验标题/标记格式（系统生成）。

格式规范（写入磁盘的最终文件）：
  第1行: L## · S##《标题》（系统生成）
  第2..N-2行: 正文（纯叙事，不得含子结构标记行）
  第N-1行: 【别名】声明（系统从正文提取后剥离）
  末行: L##S##（系统追加）
"""
import sys, os, re, subprocess
from pathlib import Path

TITLE_PATTERN = re.compile(r'^L\d+ · S\d+《.+》$')
MARKER_PATTERN = re.compile(r'^L\d+S\d+$')
ALIAS_PATTERN = re.compile(r'^【别名】\s*(.+?)\s*=\s*(.+)$')
ALIAS_NONE_PATTERN = re.compile(r'^【别名】\s*无\s*$')
SCRIPTS_DIR = Path(__file__).parent

# 署名/代名检测模式
SIGNATURE_PATTERNS = [
    r'由\s*\w*\s*(撰写|创作|生成|编写|完成)',
    r'本文\s*(由|为)\s*\w*\s*(撰写|创作|生成|编写)',
    r'WorkBuddy\s*(创作|生成|编写|撰写)',
    r'(撰写|创作|生成)于\s*\w*\s*(助手|AI|WorkBuddy)',
    r'在\s*\w*\s*(指导|帮助|协助)下\s*(撰写|创作|生成)',
    r'本文由\s*\w+\s*创作',
]


def validate_and_write_body(body_text, filepath, chapter, sub_key, title,
                              signature=None, state_path=None):
    """
    校验纯正文 → 组装全文 → 原子写入。
    body_text: LLM 输出的纯正文（可能末尾含 【别名】行）
    title: 子结构标题（不含 L##·S## 前缀）
    """
    fp = Path(filepath)
    fp.parent.mkdir(parents=True, exist_ok=True)

    title_line = f"{chapter} · {sub_key}\u300a{title}\u300b"
    sub_marker = f"{chapter}{sub_key}"
    lines = body_text.split("\n")

    # ── 钩子5: 别名声明拦截（从正文末尾提取）──
    alias_line = None
    alias_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if ALIAS_PATTERN.match(stripped):
            alias_line = stripped
            alias_idx = i
            break
        if ALIAS_NONE_PATTERN.match(stripped):
            alias_line = stripped
            alias_idx = i
            break

    if alias_line is None:
        # 系统自动补【别名】无（新流程：LLM 不强制输出别名行）
        print(f"  [别名] 系统自动补: 【别名】无")
        alias_line = "【别名】无"
    elif alias_line.startswith("【别名】无"):
        # 声明无别名，剥离即可
        lines.pop(alias_idx)
        print(f"  [别名] 声明: 无别名")
    else:
        # 解析别名声明并注册
        m = ALIAS_PATTERN.match(alias_line)
        if m:
            char_name = m.group(1).strip()
            alias = m.group(2).strip()
            lines.pop(alias_idx)
            print(f"  [别名] 声明: {char_name} ← 「{alias}」")
            if state_path:
                sm_path = SCRIPTS_DIR / "novel_state_manager.py"
                r = subprocess.run(
                    [sys.executable, str(sm_path), "register-alias", state_path, char_name, alias],
                    capture_output=True, text=True, encoding="utf-8"
                )
                if r.returncode == 0:
                    for out_line in r.stdout.strip().split("\n"):
                        if out_line.strip():
                            print(f"    {out_line.strip()}")
                else:
                    print(f"    [WARN] 别名注册失败: {r.stderr.strip()}")

    # ── 重新构建干净的正文（别名行已剥离）──
    clean_body = "\n".join(lines).strip()

    # ── 钩子6: 正文非空检测（阻断）──
    if not clean_body:
        print(f"[HOOK-BLOCK] 正文为空，拒绝写入")
        return False

    # ── 钩子7: 正文标记行检测（阻断）──
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if MARKER_PATTERN.match(stripped):
            print(f"[HOOK-BLOCK] 正文第{i}行含非法子结构标记: {line.strip()}")
            print(f"  正文中禁止出现 L#S# 标记，该标记由系统自动追加")
            return False

    # ── 钩子8: 标点缺失校验（软性，不阻断）──
    PUNCTUATION = set("，。；：？！、,.;:?!")
    MAX_SEGMENT = 80
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        segments = []
        current = ""
        for ch in stripped:
            if ch in PUNCTUATION:
                if current.strip():
                    segments.append(current.strip())
                current = ""
            else:
                current += ch
        if current.strip():
            segments.append(current.strip())
        longest = max((len(s) for s in segments), default=0)
        if longest > MAX_SEGMENT:
            print(f"  [PUNCT] 正文第{i}行含超长无标点片段（{longest}字），建议补充断句标点")

    # ── 元注释污染检测（阻断）──
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if re.match(r'^\*\*(S\d+|L\d+)\s*(完成|全章完成)', stripped):
            print(f"[HOOK-BLOCK] 正文第{i}行含元注释污染: {line.strip()}")
            return False

    # ── 钩子4: 署名/代名检测（代码级硬阻断） ──
    if signature is None:
        pass
    elif not signature.get("enabled", False):
        for i, line in enumerate(lines, 1):
            for pat in SIGNATURE_PATTERNS:
                if re.search(pat, line):
                    print(f"[HOOK-BLOCK] 正文第{i}行含禁止的署名/代名: {line.strip()}")
                    print(f"  匹配模式: {pat}")
                    return False
    else:
        sig_text = signature.get("text", "")
        for i, line in enumerate(lines, 1):
            for pat in SIGNATURE_PATTERNS:
                m = re.search(pat, line)
                if m:
                    if not sig_text:
                        print(f"[HOOK-BLOCK] 正文第{i}行含署名内容，但 signature.text 为空: {line.strip()}")
                        return False
                    if sig_text not in line:
                        print(f"[HOOK-BLOCK] 正文第{i}行署名与配置值不匹配: {line.strip()}")
                        return False

    # ── 组装最终内容（系统生成标题行+别名行+标记行）──
    final_lines = [title_line, "", clean_body, alias_line]
    final_content = "\n".join(final_lines)

    # ── 原子写入（不含末行标记，由最后一步追加）──
    with open(fp, "w", encoding="utf-8") as f:
        f.write(final_content)
        f.flush()
        os.fsync(f.fileno())

    # ── 追加子结构编号标记 ──
    with open(fp, "a", encoding="utf-8") as f:
        f.write(f"\n{sub_marker}\n")
        f.flush()
        os.fsync(f.fileno())

    print(f"[WRITE-OK] {filepath}")
    print(f"  标题: {title_line}")
    print(f"  正文: {len(lines)} 行")
    print(f"  标记: {sub_marker}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法: python novel_atomic_writer.py <body_file|-> <filepath> <chapter> <sub_key> [title]")
        print("  - 表示从 stdin 读取正文内容")
        print("  title: 子结构标题（可选，默认从 filepath 推导）")
        sys.exit(1)

    body_src = sys.argv[1]
    filepath = sys.argv[2]
    chapter = sys.argv[3]
    sub_key = sys.argv[4]
    title = sys.argv[5] if len(sys.argv) > 5 else f"{chapter}·{sub_key}"

    if body_src == "-":
        body_text = sys.stdin.read()
    else:
        body_text = Path(body_src).read_text(encoding="utf-8-sig")

    success = validate_and_write_body(body_text, filepath, chapter, sub_key, title)
    if not success:
        sys.exit(1)
