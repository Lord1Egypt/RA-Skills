import argparse
import json
import pathlib
import sys

import requests


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "data" / "command_index.jsonl"
API_URL = "https://ec.ijingyi.com/plugin.php?id=plugin1&"

SUPPLEMENTS = {
    810: {
        "id": 810,
        "name": "时间_取月末",
        "content_text": ".版本 2\n\n.子程序 时间_取月末, 日期时间型, , 源码由论坛用户【ds9660】雕哥提供。\n.参数 参_指定时间, 日期时间型, 可空 ,",
    },
    1109: {
        "id": 1109,
        "name": "文本_取随机汉字",
        "content_text": ".版本 2\n\n.子程序 文本_取随机汉字, 文本型, , 取常用的随机汉字\n.参数 个数, 整数型, , 要取出多少个汉字！\n.参数 汉字或全拼, 整数型, 可空 , 0为汉字，否则为全拼音！",
    },
    6255: {
        "id": 6255,
        "name": "选择字体",
        "content_text": ".版本 2\n\n.类 类_通用对话框, , 公开 ,\n\n.子程序 选择字体, 字体, , 打开选择字体对话框，成功返回字体相关信息，调用格式如； 编辑框.字体=选择字体()\n.参数 字体名称, 文本型, 可空 ,\n.参数 字体大小, 整数型, 可空 ,\n.参数 字体颜色, 整数型, 可空 ,\n.参数 加粗, 逻辑型, 可空 ,\n.参数 倾斜, 逻辑型, 可空 ,\n.参数 删除线, 逻辑型, 可空 ,\n.参数 下划线, 逻辑型, 可空 ,\n.参数 lRes, 逻辑型, 参考 可空 , 如果用户单击对话框的OK按钮，则返回值为真。",
    },
}


def load_index():
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"index file not found: {INDEX_FILE}")
    data = []
    with INDEX_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(json.loads(line))
    return data


def find_by_name(name: str):
    for item in load_index():
        if item.get("name") == name or item.get("short_name") == name:
            return item
    return None


def fetch_by_id(doc_id: int):
    response = requests.post(
        API_URL,
        data={"mod": "sub", "ac": "getdata", "num": str(doc_id)},
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://ec.ijingyi.com/sub.htm",
        },
    )
    response.raise_for_status()
    if not response.text.strip():
        if doc_id in SUPPLEMENTS:
            return {
                "result": 1,
                "data": {
                    "id": doc_id,
                    "name": SUPPLEMENTS[doc_id]["name"],
                    "content_text": SUPPLEMENTS[doc_id]["content_text"],
                    "supplemented": True,
                },
            }
        raise RuntimeError("official API returned empty body")
    data = response.json()
    if not data.get("result"):
        raise RuntimeError(data.get("error") or "API returned failure")
    return data


def main():
    parser = argparse.ArgumentParser(description="Fetch 精易模块 command docs")
    parser.add_argument("--id", type=int, help="fetch by command id")
    parser.add_argument("--name", help="fetch by command name")
    args = parser.parse_args()

    doc_id = args.id
    if doc_id is None:
        if not args.name:
            print("must provide --id or --name", file=sys.stderr)
            sys.exit(1)
        try:
            item = find_by_name(args.name)
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)
        if not item:
            print("command name not found", file=sys.stderr)
            sys.exit(1)
        doc_id = int(item["id"])

    try:
        data = fetch_by_id(doc_id)
    except Exception as exc:
        print(json.dumps({"error": str(exc), "id": doc_id}, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
