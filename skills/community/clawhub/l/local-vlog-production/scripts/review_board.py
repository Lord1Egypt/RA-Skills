"""Build a local selection page and its script from the same reviewed material."""
import argparse
import hashlib
import json
import math
import os
import re
import stat
import tempfile
from html import escape
from pathlib import Path
from urllib.parse import quote


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def nonempty(record, key):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"缺少文字字段 {key}")
    return value


def index_by_id(records, name):
    if not isinstance(records, list):
        raise ValueError(f"{name} 必须为列表")
    indexed = {}
    for record in records:
        identifier = nonempty(record, "id")
        if identifier in indexed:
            raise ValueError(f"{name} 编号重复 {identifier}")
        indexed[identifier] = record
    return indexed


def number(record, key, default=None):
    value = record.get(key, default)
    if type(value) not in (float, int) or not math.isfinite(value):
        raise ValueError(f"{record['id']} 的 {key} 需要有限数值")
    return value


def clip_seconds(clip):
    if clip["kind"] == "photo":
        return number(clip, "duration")
    start = number(clip, "source_in")
    end = number(clip, "source_out")
    speed = number(clip, "speed", 1)
    if start < 0 or end <= start or speed <= 0:
        raise ValueError(f"{clip['id']} 的原片区间或速度无效")
    return (end - start) / speed


def check_selections(beats, clips):
    used = set()
    for beat in beats:
        chosen = beat.get("selected")
        if not isinstance(chosen, list):
            raise ValueError(f"{beat['id']} 需要已选列表，留空用 []")
        for key in chosen:
            if not isinstance(key, str) or key not in clips or key in used:
                raise ValueError(f"{beat['id']} 的候选编号无效或重复 {key}")
            used.add(key)


def reviewed_media(path, clip_id):
    path = Path(os.path.abspath(path))
    # Review only named files. Keep links inside the workspace source tree opaque.
    inside_sources = False
    for component in (*reversed(path.parents), path):
        inside_sources = inside_sources or component.name == "素材"
        if inside_sources:
            info = component.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError(f"{clip_id} 的素材路径经过链接，请引用审阅过的原件 {component}")
    if not path.is_file():
        raise ValueError(f"{clip_id} 缺少本地材料 {path}")
    return path


def load_plan(path):
    plan = read_json(path)
    for key in ("project", "edition", "version"):
        nonempty(plan, key)
    beats = index_by_id(plan["beats"], "段落")
    clips = index_by_id(plan["candidates"], "候选")
    if not beats:
        raise ValueError("至少需要一个脚本段落")
    for beat in beats.values():
        for key in ("chapter", "title"):
            nonempty(beat, key)
        for key in ("narration", "sound", "edit"):
            if not isinstance(beat.get(key, ""), str):
                raise ValueError(f"{beat['id']} 的 {key} 需要文字")
    for clip in clips.values():
        for key in ("home", "asset_id", "visual", "source"):
            nonempty(clip, key)
        if clip["home"] not in beats or clip.get("kind") not in ("video", "photo"):
            raise ValueError(f"{clip['id']} 的所属段落或媒体类型无效")
        if clip_seconds(clip) <= 0:
            raise ValueError(f"{clip['id']} 的时长需要大于零")
        for key in ("source", "preview", "thumb"):
            if clip.get(key):
                clip[key] = str(reviewed_media(path.parent / clip[key], clip["id"]))
    check_selections(beats.values(), clips)
    return plan


def fingerprint(plan):
    data = json.dumps(plan, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def apply_choices(plan, choices):
    if choices.get("schema") != "vlog-review/1" or choices.get("base") != fingerprint(plan):
        raise ValueError("选择文件来自另一份分镜。请在对应底版合并，再按段落编号带入当前稿。")
    edits = index_by_id(choices["beats"], "选材反馈")
    base = index_by_id(plan["beats"], "段落")
    if edits.keys() != base.keys():
        raise ValueError("选择文件中的段落与底稿不一致")
    check_selections(edits.values(), index_by_id(plan["candidates"], "候选"))
    for key, beat in base.items():
        note = edits[key].get("narration")
        if not isinstance(note, str):
            raise ValueError(f"{key} 的旁白需要文字")
        beat.update(selected=edits[key]["selected"], narration=note)


def relative_media(path, output):
    try:
        return Path(os.path.relpath(path, output)).as_posix()
    except ValueError:  # Windows sources on a different volume.
        return Path(path).as_posix()


def media_url(value):
    path = Path(value)
    return path.as_uri() if path.is_absolute() else quote(value, safe="/")


def timecode(seconds):
    tenths = math.floor(seconds * 10 + 0.5)
    return f"{tenths // 600}:{tenths % 600 // 10:02}.{tenths % 10}"


def source_label(clip):
    if clip["kind"] == "photo":
        return f"照片 {clip['duration']:g} 秒"
    speed = clip.get("speed", 1)
    rate = f"，{speed:g} 倍速" if speed != 1 else ""
    return f"原片 {timecode(clip['source_in'])}–{timecode(clip['source_out'])}{rate}"


def script_text(plan):
    clips = index_by_id(plan["candidates"], "候选")
    rows = [f"# {plan['project']} · {plan['edition']} · {plan['version']}", "",
            "[打开选材与片段预览](index.html)", ""]
    previous = None
    cursor = 0
    for beat in plan["beats"]:
        if beat["chapter"] != previous:
            rows.extend([f"## {beat['chapter']}", ""])
            previous = beat["chapter"]
        chosen = [clips[key] for key in beat["selected"]]
        end = cursor + sum(clip_seconds(clip) for clip in chosen)
        rows.extend([f"### {beat['id']}　{beat['title']}", "",
                     f"选材串联 {timecode(cursor)}–{timecode(end)}", ""])
        for clip in chosen:
            rows.append(f"- {clip['visual']}（{clip['id']} / {clip['asset_id']}，{source_label(clip)}）")
        if not chosen:
            rows.append("本段待选画面。")
        for key, label in (("narration", "旁白"), ("sound", "声音"), ("edit", "剪辑")):
            if beat.get(key):
                rows.extend(["", f"**{label}**　{beat[key]}"])
        rows.append("")
        cursor = end
    return "\n".join(rows) + "\n"


def write_bundle(plan, output):
    base = fingerprint(plan)
    clips = []
    for clip in plan["candidates"]:
        for field in ("source", "preview", "thumb"):
            if clip.get(field):
                clip[field] = relative_media(clip[field], output)
        start = clip.get("source_in", 0) if not clip.get("preview") else 0
        seconds = clip_seconds(clip)
        clips.append({"id": clip["id"], "home": clip["home"], "asset_id": clip["asset_id"],
                      "kind": clip["kind"], "visual": clip["visual"], "sourceLabel": source_label(clip),
                      "src": media_url(clip.get("preview") or clip["source"]),
                      "thumb": media_url(clip["thumb"]) if clip.get("thumb") else "",
                      "start": start, "duration": seconds, "speed": clip.get("speed", 1)})
    data = {key: plan[key] for key in ("project", "edition", "version", "beats")}
    data.update(base=base, clips=clips)
    data_json = json.dumps(data, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c")
    template = Path(__file__).resolve().parents[1] / "assets" / "selection-review.html"
    title = " · ".join([plan["project"], plan["edition"], plan["version"]])
    fields = {"{{TITLE}}": escape(title), "{{PLAN}}": data_json}
    html = re.sub(r"{{(?:TITLE|PLAN)}}", lambda match: fields[match[0]], template.read_text(encoding="utf-8"))
    if output.exists():
        raise ValueError(f"版本目录已有内容，请选用新目录 {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix=".vlog-review-") as temporary:
        stage = Path(temporary) / "bundle"
        stage.mkdir()
        (stage / "index.html").write_text(html, encoding="utf-8")
        (stage / "分镜脚本.md").write_text(script_text(plan), encoding="utf-8")
        (stage / "分镜选材.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        stage.rename(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="审阅后的分镜选材 JSON")
    parser.add_argument("output", type=Path, help="新的成对交付目录")
    parser.add_argument("--choices", type=Path, help="从对应底版 HTML 导出的选择")
    parser.add_argument("--version", help="新版本标识")
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan.resolve())
        if args.choices:
            if not args.version or args.version == plan["version"]:
                raise ValueError("合并选材时请给本次修订设置新版本")
            apply_choices(plan, read_json(args.choices))
        if args.version:
            plan["version"] = args.version
        write_bundle(plan, args.output.resolve())
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"{exc}\n")
    print(args.output.resolve() / "index.html")


if __name__ == "__main__":
    main()
