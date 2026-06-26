import json
import pathlib
import re


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
SOURCE_JSONL = BASE_DIR.parent / "ijingyi_export" / "docs_clean.jsonl"
OUT_DIR = BASE_DIR / "data"
OUT_FILE = OUT_DIR / "command_index.jsonl"

SUPPLEMENT_SUMMARIES = {
    810: ".子程序 时间_取月末, 日期时间型, , 源码由论坛用户【ds9660】雕哥提供。",
    1109: ".子程序 文本_取随机汉字, 文本型, , 取常用的随机汉字",
    6255: ".子程序 选择字体, 字体, , 打开选择字体对话框，成功返回字体相关信息。",
}


def strip_html_summary(text: str) -> str:
    text = re.sub(r"复制命令（简易）|复制命令（带参数说明）|复制声明代码", " ", text)
    text = re.sub(r"子程序名|返回值类型|公开|备\s*注|参数名|类\s*型|参考|可空|数组", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 160:
        text = text[:160].rstrip() + "..."
    return text


def split_keywords(text: str):
    parts = re.split(r"[\s_/\-，。；、（）()\[\]【】]+", text)
    return [p for p in parts if p]


def make_summary(item: dict) -> str:
    if item.get("id") in SUPPLEMENT_SUMMARIES:
        return SUPPLEMENT_SUMMARIES[item["id"]]
    text = item.get("content_text", "") or ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    preferred = []
    for line in lines:
        if line.startswith(".子程序") or line.startswith(".类") or line.startswith(".DLL命令") or line.startswith(".参数"):
            preferred.append(line)
        if len(preferred) >= 3:
            break
    if preferred:
        return strip_html_summary(" ".join(preferred))
    return strip_html_summary(" ".join(lines[:3]))


def short_name(name: str) -> str:
    if "_" in name:
        return name.split("_", 1)[1]
    return name


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    with SOURCE_JSONL.open("r", encoding="utf-8") as src, OUT_FILE.open("w", encoding="utf-8") as out:
        for line in src:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            record = {
                "id": item.get("id"),
                "pid": item.get("pid"),
                "name": item.get("canonical_name") or item.get("name") or "",
                "short_name": short_name(item.get("canonical_name") or item.get("name") or ""),
                "canonical_path": item.get("canonical_path") or item.get("tree_path") or "",
                "cmdtype": item.get("cmdtype"),
                "is_dir": item.get("is_dir"),
                "summary": make_summary(item),
                "keywords": sorted(
                    set(
                        split_keywords(item.get("canonical_name") or "")
                        + split_keywords(item.get("canonical_path") or "")
                    )
                ),
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    print(json.dumps({"written": count, "file": str(OUT_FILE)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
