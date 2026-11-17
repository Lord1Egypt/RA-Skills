# -*- coding: utf-8 -*-
"""提示压缩器：按 关键词密度+位置 给句子打分，按目标比例删低分句。零依赖。"""
import argparse, pathlib, re, sys

KEYWORDS = ["必须", "禁止", "默认", "重要", "关键", "不能", "务必", "require", "must", "never",
            "always", "default", "important", "key", "约束", "规则", "步骤", "注意"]
CONSTRAINT = re.compile(r"(必须|禁止|不能|务必|require|must|never|always|约束|规则)", re.I)
# 含关键数字的句子（指标/阈值/限额）强制保留
NUMERIC = re.compile(r"\d+(?:\.\d+)?\s*(?:%|％|万|亿|元|次|天|小时|分钟|ms|s\b)|\d{3,}")

def split_sentences(txt):
    # 中英文句子切分（保留句号/问号/叹号/换行）
    parts = re.split(r"(?<=[。！？!?\n])", txt)
    return [p.strip() for p in parts if p.strip()]

def stash_blocks(txt):
    """代码块摘出整体保留，原位留占位符。返回(替换后文本, blocks列表)。"""
    blocks = []
    def _stash(m):
        blocks.append(m.group(0))
        return f"\x00BLOCK{len(blocks) - 1}\x00"
    return re.sub(r"```.*?```", _stash, txt, flags=re.S), blocks

def restore_blocks(txt, blocks):
    for i, b in enumerate(blocks):
        txt = txt.replace(f"\x00BLOCK{i}\x00", b)
    return txt

def score(sent, idx, total):
    kw = sum(1 for k in KEYWORDS if k.lower() in sent.lower())
    length = len(sent)
    # 适中长度得分（<=120字最佳）
    length_ok = 1.0 if length <= 120 else max(0.2, 120 / length)
    # 位置权重：首尾更高
    pos = 1.0
    if idx == 0 or idx == total - 1:
        pos = 1.4
    elif idx < total * 0.2 or idx > total * 0.8:
        pos = 1.15
    return kw * 2.0 + length_ok + pos

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--ratio", type=float, default=0.5, help="保留比例 0-1")
    a = ap.parse_args()

    txt = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8-sig")
    txt2, blocks = stash_blocks(txt)
    sents = split_sentences(txt2)
    if not sents:
        print(restore_blocks(txt, blocks))
        return
    total = len(sents)
    scored = [(i, s, score(s, i, total)) for i, s in enumerate(sents)]
    # 强制保留：约束句 + 数字句 + 代码块句
    must_keep = {i for i, s, _ in scored
                 if CONSTRAINT.search(s) or NUMERIC.search(s) or "\x00BLOCK" in s}
    n_constraint = sum(1 for i, s, _ in scored if CONSTRAINT.search(s))
    n_numeric = sum(1 for i, s, _ in scored if NUMERIC.search(s) and not CONSTRAINT.search(s))
    n_block = sum(1 for i, s, _ in scored if "\x00BLOCK" in s)
    # 其余按分排序补足到目标比例
    rest = sorted([x for x in scored if x[0] not in must_keep], key=lambda x: x[2])
    target_keep = max(len(must_keep), int(total * a.ratio))
    keep = set(must_keep)
    need = target_keep - len(keep)
    for i, s, sc in rest:
        if need <= 0:
            break
        keep.add(i)
        need -= 1
    keep = sorted(keep)
    out = restore_blocks("\n".join(sents[i] for i in keep), blocks)
    print(f"# 压缩 {total}→{len(keep)} 句 (ratio={a.ratio})\n")
    print(out)
    # 第 3 步校验：约束句/数字句/代码块必须全部保留
    kept_constraints = sum(1 for i in keep if CONSTRAINT.search(sents[i]))
    kept_numeric = sum(1 for i in keep if NUMERIC.search(sents[i]) and not CONSTRAINT.search(sents[i]))
    kept_blocks = sum(1 for i in keep if "\x00BLOCK" in sents[i])
    print(f"\n# 校验：约束句 {kept_constraints}/{n_constraint} 保留  数字句 {kept_numeric}/{n_numeric} 保留  代码块 {kept_blocks}/{n_block} 完整")
    ok = (kept_constraints == n_constraint and kept_numeric == n_numeric and kept_blocks == n_block)
    print(f"# 校验结果：{'✅ 通过（关键内容零丢失）' if ok else '⛔ 失败（关键内容被删，请人工复核）'}")

if __name__ == "__main__":
    main()
