# -*- coding: utf-8 -*-
"""
把结构化题库 JSON 构建成可离线运行的题库网站。

用法：
    python build_bank.py <bank.json> <site-dir> [--check-only]

参数：
    bank.json    结构化题库。两种形态都接受：
                 1) 完整包：{"meta": {...}, "subjects": [...], "questions": [...]}
                 2) 裸数组：[ {题目}, {题目}, ... ]        —— meta/subjects 自动补全
    site-dir     目标站点目录（已由 SKILL 流程从 assets/app-template 拷贝而来）
    --check-only 只校验不写文件，用于生成题目后的预检

行为：
    1. 严格校验题库（题型、答案与选项匹配、填空空位数、出处等）
    2. 自动推导 subjects（若未显式提供）
    3. 写出 <site-dir>/questions.json（人类可读，便于用户手改）
    4. 写出 <site-dir>/assets/js/data.js（内嵌题库，保证 file:// 双击可用）

设计要点：
    data.js 是 file:// 场景的关键——浏览器在 file:// 下会拦截 fetch/XHR 读取
    同目录 JSON，所以必须把题库内嵌成 JS 变量。questions.json 同时保留，
    用于用户手工编辑和 http:// 场景。两者由本脚本保持一致。
"""
import json
import os
import sys
from collections import Counter, OrderedDict

VALID_TYPES = {"single", "multiple", "judge", "blank", "short"}

TYPE_LABEL = {
    "single": "单选题", "multiple": "多选题", "judge": "判断题",
    "blank": "填空题", "short": "简答题",
}
DIFF_LABEL = {"1": "基础", "2": "进阶", "3": "挑战"}

# 与 app-template/assets/js/app.js 中 ICONS 保持同步
VALID_ICONS = {
    "book", "pill", "leaf", "sprout", "flask", "brain", "code", "sigma",
    "scale", "globe", "language", "atom", "heart", "chart", "scroll",
    "cpu", "palette", "music", "briefcase", "compass",
}


def validate(questions):
    """返回错误列表；空列表代表通过。"""
    errors = []

    if not questions:
        return ["题库为空，至少需要 1 道题"]

    ids = Counter(q.get("id", "<无ID>") for q in questions)
    for qid, n in ids.items():
        if n > 1:
            errors.append(f"重复 ID：{qid}（出现 {n} 次）")

    for q in questions:
        qid = q.get("id", "<无ID>")

        if not q.get("id"):
            errors.append("存在没有 id 的题目")

        t = q.get("type")
        if t not in VALID_TYPES:
            errors.append(f"{qid}: 题型非法 {t!r}，必须是 {sorted(VALID_TYPES)} 之一")

        for field in ("subject", "chapter", "stem", "analysis", "difficulty"):
            if not q.get(field):
                errors.append(f"{qid}: 缺少必填字段 {field}")

        diff = q.get("difficulty")
        if diff not in (1, 2, 3):
            errors.append(f"{qid}: difficulty 必须是 1/2/3，当前 {diff!r}")

        # 出处：file 必填，locator 必填，page 允许为 null 或整数
        src = q.get("source") or {}
        if not src.get("file") or not src.get("locator"):
            errors.append(f"{qid}: source 需要同时含 file 与 locator")
        page = src.get("page")
        if page is not None and not isinstance(page, int):
            errors.append(f"{qid}: source.page 必须是整数或 null（无可靠页码时填 null，不要编造）")

        if t in ("single", "multiple"):
            opts = q.get("options") or []
            keys = [o.get("key") for o in opts if isinstance(o, dict)]
            if len(keys) < 3:
                errors.append(f"{qid}: 选项少于 3 个")
            if len(set(keys)) != len(keys):
                errors.append(f"{qid}: 选项 key 重复")
            for o in opts:
                if not isinstance(o, dict) or not o.get("key") or not o.get("text"):
                    errors.append(f"{qid}: 选项需同时含 key 与 text")
            ans = q.get("answer")
            ans = [ans] if isinstance(ans, str) else (ans or [])
            if not ans:
                errors.append(f"{qid}: 缺少答案")
            for a in ans:
                if a not in keys:
                    errors.append(f"{qid}: 答案 {a!r} 不在选项 key 中")
            if t == "single" and len(ans) != 1:
                errors.append(f"{qid}: 单选题答案必须恰好 1 项，当前 {len(ans)} 项")
            if t == "multiple" and len(ans) < 2:
                errors.append(f"{qid}: 多选题答案至少 2 项，当前 {len(ans)} 项")

        elif t == "judge":
            if q.get("answer") not in ("T", "F"):
                errors.append(f"{qid}: 判断题答案必须是 'T' 或 'F'，当前 {q.get('answer')!r}")

        elif t == "blank":
            ans = q.get("answer")
            if not isinstance(ans, list) or not ans:
                errors.append(f"{qid}: 填空题 answer 必须是非空数组")
            else:
                for i, b in enumerate(ans):
                    if not isinstance(b, dict) or not b.get("accept"):
                        errors.append(f"{qid}: 第 {i + 1} 个空缺少 accept 数组")
                    elif not isinstance(b["accept"], list):
                        errors.append(f"{qid}: 第 {i + 1} 个空的 accept 必须是数组")
            n_blank = q.get("stem", "").count("____")
            if n_blank == 0:
                errors.append(f"{qid}: 填空题题干必须用连续 4 个下划线 ____ 标记空位")
            elif n_blank != len(ans or []):
                errors.append(f"{qid}: 题干空位数 {n_blank} 与答案数 {len(ans or [])} 不一致")

        elif t == "short":
            if not q.get("answer"):
                errors.append(f"{qid}: 简答题缺少参考答案")
            kw = q.get("keywords") or []
            if not isinstance(kw, list) or not (2 <= len(kw) <= 12):
                errors.append(f"{qid}: 简答题 keywords 需为 2-12 个，当前 {len(kw) if isinstance(kw, list) else '非数组'}")

        icon = q.get("icon")
        if icon and icon not in VALID_ICONS:
            errors.append(f"{qid}: 图标 {icon!r} 不在图标库中")

    return errors


def derive_subjects(questions, declared):
    """按题目出现顺序推导科目；已声明的科目补全 chapters / count。"""
    declared_map = {s.get("id") or s.get("name"): s for s in (declared or [])}
    order = list(OrderedDict((q["subject"], None) for q in questions).keys())

    subjects = []
    for name in order:
        qs = [q for q in questions if q["subject"] == name]
        chapters = list(OrderedDict((q["chapter"], None) for q in qs).keys())
        d = declared_map.get(name, {})
        icon = d.get("icon", "book")
        if icon not in VALID_ICONS:
            icon = "book"
        subjects.append({
            "id": name,
            "name": d.get("name", name),
            "desc": d.get("desc", ""),
            "icon": icon,
            "chapters": chapters,
            "count": len(qs),
        })
    return subjects


def normalize(raw):
    """把裸数组或完整包统一成完整包。"""
    if isinstance(raw, list):
        questions, meta, declared = raw, {}, []
    elif isinstance(raw, dict):
        questions = raw.get("questions") or []
        meta = raw.get("meta") or {}
        declared = raw.get("subjects") or []
    else:
        raise SystemExit("题库 JSON 顶层必须是数组或对象")

    subjects = derive_subjects(questions, declared)

    full_meta = {
        "title": meta.get("title") or "智能复习题库",
        "brandName": meta.get("brandName") or meta.get("title") or "题库",
        "brandIcon": meta.get("brandIcon") if meta.get("brandIcon") in VALID_ICONS else "book",
        "version": meta.get("version") or "1.0.0",
        "generatedFrom": meta.get("generatedFrom") or [],
        "note": meta.get("note") or "",
        "typeLabels": TYPE_LABEL,
        "difficultyLabels": DIFF_LABEL,
    }
    return {"meta": full_meta, "subjects": subjects, "questions": questions}


def report(bank):
    qs = bank["questions"]
    by_type = Counter(q.get("type") for q in qs)
    by_subject = Counter(q.get("subject") for q in qs)
    by_diff = Counter(q.get("difficulty") for q in qs)
    print(f"题目总数：{len(qs)}")
    print("题型分布：", {TYPE_LABEL.get(k, k): v for k, v in by_type.items()})
    print("科目分布：", dict(by_subject))
    print("难度分布：", {DIFF_LABEL.get(str(k), k): v for k, v in by_diff.items()})


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2

    bank_path = argv[0]
    site_dir = argv[1]
    check_only = "--check-only" in argv

    with open(bank_path, encoding="utf-8") as f:
        raw = json.load(f)

    bank = normalize(raw)
    errors = validate(bank["questions"])

    if errors:
        print(f"校验未通过，共 {len(errors)} 处问题：")
        for e in errors[:50]:
            print("  -", e)
        if len(errors) > 50:
            print(f"  ...另有 {len(errors) - 50} 处")
        return 1

    print("校验通过。")
    report(bank)

    if check_only:
        print("（--check-only：未写出任何文件）")
        return 0

    js_dir = os.path.join(site_dir, "assets", "js")
    os.makedirs(js_dir, exist_ok=True)

    qjson = os.path.join(site_dir, "questions.json")
    with open(qjson, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)

    data_js = os.path.join(js_dir, "data.js")
    payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":"))
    with open(data_js, "w", encoding="utf-8") as f:
        f.write("/* 自动生成，请勿手动修改。\n")
        f.write("   题库源文件为站点根目录的 questions.json，\n")
        f.write("   修改后重新运行 build_bank.py 即可同步本文件。*/\n")
        f.write("window.__EMBEDDED_BANK__ = ")
        f.write(payload)
        f.write(";\n")

    print("已写出：", qjson)
    print("已写出：", data_js)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
