#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility linter with advisory style diagnostics.

Novel Core keeps literary taste configurable. This command reports style signals
by default and only emits a blocking error when a project explicitly lists the
rule in ``blocking_rules``. Structural delivery gates live in ``novelforgectl``.
"""

import argparse
import json
import re
import sys
from pathlib import Path


STYLE_PATTERNS = (
    ("cliche", re.compile(r"需要强调的是|总的来说|值得注意的是|综上所述|一言以蔽之")),
    ("mental", re.compile(r"(?:他|她|我|你)(?:们)?(?:想|感到|意识到|回忆起|觉得|认为|明白)")),
    ("modern-unit", re.compile(r"分钟|小时|厘米|毫米|公里|公斤")),
    ("modern-term", re.compile(r"计算机|数据库|网络|信号|系统|订单|客户|KPI")),
    ("pompous-naming", re.compile(
        r"(?:盛世|天鼎|傲世|龙腾|至尊|君临|帝豪|天衍)(?:集团|大厦|国际|酒店|会所|资本|庄园)|"
        r"(?:天机阁|暗影殿|血煞门|修罗殿)"
    )),
    ("ai-trope", re.compile(
        r"(?:踏碎|撕碎|染上|融入).*?(?:月光|夜色|苍穹)|"
        r"(?:火把|旗帜|衣袂).*?猎猎|"
        r"(?:忽然|嘴角|脸上).*?(?:勾起|扬起|浮现|闪过).*?(?:轻笑|冷笑|一抹|弧度|玩味|讥讽)|"
        r"(?:忽然|悄然)?(?:传出|发出)?(?:一?声)?(?:冷笑|轻笑)|"
        r"(?:冷笑|轻笑)(?:了一?声|出声|了声|一声)?|"
        r"(?:倒吸|倒抽).*?(?:一口)?(?:凉气|冷气)|"
        r"(?:深邃|冰冷|漆黑).*?眼眸.*?(?:闪过|寒芒|冷芒)|"
        r"全场.*?(?:死寂|死一般|鸦雀无声|落针可闻)|"
        r"宛如.*?(?:神明|魔神|杀神|主宰)|"
        r"滔天.*?(?:杀意|怒意|威压)"
    )),
)

REPETITIVE_ACTIONS = (
    ("点头", re.compile(r"点(?:了|了下|了个|了点头|头)")),
    ("轻笑/苦笑", re.compile(r"(?:笑(?:了笑|了下|了起来)|苦笑|冷笑|轻笑)")),
    ("叹气", re.compile(r"叹(?:了口|了声|了)气")),
    ("皱眉", re.compile(r"皱(?:了|了下|起了)?眉")),
    ("深呼吸", re.compile(r"深吸(?:了一口|了口)?气")),
)


def _path_safe_identifier(value):
    if not isinstance(value, str) or not value or value in (".", ".."):
        return False
    if any(character in value for character in ("/", "\\", "\x00")):
        return False
    return not any(ord(character) < 32 or ord(character) == 127 for character in value)


def _diagnostic(rule, line_number, line, blocking_rules, problem=None, fix=None):
    item = {
        "rule": rule,
        "line": line_number,
        "content": line[:120],
        "problem": problem or "style signal detected",
        "fix": fix or "review this signal against the project profile and current engine",
        "blocking": rule in blocking_rules,
    }
    return item


def run_lint(file_path, project_root=None, custom_banned_words=None, trigger_flags=None, config=None):
    path = Path(file_path)
    if not path.is_file():
        return {"status": "ERROR", "message": "file does not exist: {}".format(path), "errors": [], "warnings": []}
    if config is None:
        config = load_project_config_for_path(project_root or path)
    config = dict(config or {})
    blocking_rules = set(config.get("blocking_rules", []))
    patterns = list(STYLE_PATTERNS)
    if "style_detectors" in config:
        for item in config.get("style_detectors") or []:
            if isinstance(item, dict) and item.get("pattern"):
                patterns.append((str(item.get("id", "project-style")), re.compile(str(item["pattern"]))))
    policies = config.get("policies") or {}
    blocking_rules.update(policies.get("blocking_rules") or [])
    for word in custom_banned_words or []:
        patterns.append(("custom", re.compile(re.escape(word))))
    if policies.get("style_detector_mode", "warning") == "blocking":
        blocking_rules.update(rule for rule, _pattern in patterns)
        blocking_rules.update(("repetitive-action", "flat-cadence"))
    errors = []
    warnings = []
    full_text = path.read_text(encoding="utf-8", errors="ignore")
    lines_with_numbers = list(enumerate(full_text.splitlines(), start=1))

    for line_number, line in lines_with_numbers:
        for rule, pattern in patterns:
            if pattern.search(line):
                prob = "pompous generic entity name detected (e.g. 盛世集团/天机阁)" if rule == "pompous-naming" else None
                fx = "use naming-methodology.md to ground entity names in real socio-economic registers" if rule == "pompous-naming" else None
                diagnostic = _diagnostic(rule, line_number, line, blocking_rules, problem=prob, fix=fx)
                (errors if diagnostic["blocking"] else warnings).append(diagnostic)

        # Repetitive action check within a single paragraph/line
        for action_name, action_re in REPETITIVE_ACTIONS:
            matches = action_re.findall(line)
            if len(matches) >= 3:
                diagnostic = _diagnostic(
                    "repetitive-action",
                    line_number,
                    line,
                    blocking_rules,
                    problem="repetitive micro-action '{}' detected ({} times in line)".format(action_name, len(matches)),
                    fix="break mechanical symmetry by introducing concrete environment disruption or distinct reactions",
                )
                (errors if diagnostic["blocking"] else warnings).append(diagnostic)

    # Stock chapter ending check
    non_empty_lines = [(ln, l) for ln, l in lines_with_numbers if l.strip()]
    if non_empty_lines:
        last_ln, last_l = non_empty_lines[-1]
        if re.match(r'^\s*["\'“‘][\u4e00-\u9fa5]{1,6}[？?]["\'”’]\s*$', last_l):
            diagnostic = _diagnostic(
                "ai-trope",
                last_ln,
                last_l,
                blocking_rules,
                problem="stock rhetorical question chapter ending detected",
                fix="end on concrete event, choice or consequence rather than dramatic question trope",
            )
            (errors if diagnostic["blocking"] else warnings).append(diagnostic)

    # Flat cadence / burstiness check for longer texts
    sentences = [s.strip() for s in re.split(r"[。！？!?；;\n]+", full_text) if s.strip()]
    if len(sentences) >= 20:
        lengths = [len(s) for s in sentences]
        mean_len = sum(lengths) / len(lengths)
        var = sum((x - mean_len) ** 2 for x in lengths) / len(lengths)
        std_dev = var ** 0.5
        if 14 <= mean_len <= 30 and std_dev < 6.5:
            first_line = full_text.splitlines()[0] if full_text.splitlines() else ""
            diagnostic = _diagnostic(
                "flat-cadence",
                1,
                first_line,
                blocking_rules,
                problem="sentence length distribution is unusually uniform (std dev {:.1f}, mean {:.1f})".format(std_dev, mean_len),
                fix="vary sentence lengths by alternating punchy short phrases (<5 chars) with complex sentences (>35 chars)",
            )
            (errors if diagnostic["blocking"] else warnings).append(diagnostic)

    return {"status": "FAIL" if errors else "PASS", "errors": errors, "warnings": warnings}


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("invalid JSON: {}".format(path)) from exc


def run_blueprint_lint(file_path, project_root=None):
    blueprint = _read_json(file_path)
    errors = []
    if not isinstance(blueprint, dict):
        errors.append({"rule": "blueprint.schema", "problem": "blueprint must be an object"})
    else:
        if not _path_safe_identifier(blueprint.get("id")):
            errors.append({"rule": "blueprint.id", "problem": "blueprint id is required"})
        dependencies = blueprint.get("dependencies")
        if not isinstance(dependencies, dict):
            errors.append({"rule": "blueprint.dependencies", "problem": "dependencies object is required"})
        else:
            allowed = {"entities", "hooks", "relations", "events"}
            unknown = set(dependencies) - allowed
            if unknown:
                errors.append({"rule": "blueprint.dependencies", "problem": "unknown dependency fields: {}".format(sorted(unknown))})
            for key, values in dependencies.items():
                if not isinstance(values, list) or any(not _path_safe_identifier(value) for value in values):
                    errors.append({"rule": "blueprint.dependencies", "problem": "dependency values must be string lists: {}".format(key)})
        if "scene_types" in blueprint and (
            not isinstance(blueprint["scene_types"], list)
            or any(not isinstance(value, str) or not value for value in blueprint["scene_types"])
        ):
            errors.append({"rule": "blueprint.scene_types", "problem": "scene_types must be non-empty strings"})
        if "state" in blueprint and not isinstance(blueprint["state"], dict):
            errors.append({"rule": "blueprint.state", "problem": "state must be an object"})
        if "scenes" in blueprint:
            scenes = blueprint["scenes"]
            if not isinstance(scenes, list):
                errors.append({"rule": "blueprint.scenes", "problem": "scenes must be a list"})
            else:
                for scene in scenes:
                    required = ("id", "location", "characters", "goal", "pressure", "information_change", "exit_state")
                    if (
                        not isinstance(scene, dict)
                        or not _path_safe_identifier(scene.get("id"))
                        or not isinstance(scene.get("location"), str)
                        or not isinstance(scene.get("characters"), list)
                        or any(not isinstance(value, str) for value in scene["characters"])
                        or any(not isinstance(scene.get(key), str) for key in required[3:])
                    ):
                        errors.append({"rule": "blueprint.scenes", "problem": "scene entries are invalid"})
                        break
        if "settlement" in blueprint:
            settlement = blueprint["settlement"]
            if (
                not isinstance(settlement, dict)
                or not isinstance(settlement.get("changes", []), list)
                or not isinstance(settlement.get("next_question", ""), str)
            ):
                errors.append({"rule": "blueprint.settlement", "problem": "settlement is invalid"})
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "warnings": []}


def run_milestone_lint(file_path, project_root=None):
    text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    errors = []
    for heading in ("A", "B"):
        if not re.search(r"^#{1,6}\s*.*\b{}\b".format(heading), text, re.MULTILINE):
            errors.append({"rule": "milestone.sections", "problem": "missing milestone section {}".format(heading)})
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "warnings": []}


def run_hook_lint(file_path, project_root=None):
    text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    errors = []
    if not re.search(r"^---.*?^---", text, re.MULTILINE | re.DOTALL):
        errors.append({"rule": "hook.frontmatter", "problem": "hook frontmatter is required"})
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "warnings": []}


def read_markdown_section(file_path, anchor):
    lines = Path(file_path).read_text(encoding="utf-8", errors="ignore").splitlines()
    target = anchor.strip().lower().replace("-", " ").replace("_", " ")
    start = None
    for index, line in enumerate(lines):
        if line.lstrip().startswith("#") and line.lstrip("# ").strip().lower() == target:
            start = index
            break
    if start is None:
        raise ValueError("markdown section not found: {}".format(anchor))
    end = len(lines)
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("#") and len(lines[index]) - len(lines[index].lstrip("#")) <= level:
            end = index
            break
    return "\n".join(lines[start:end]).strip() + "\n"


def check_project_integrity(project_root):
    root = Path(project_root).resolve()
    required = (".novelforge/state/project.json", ".novelforge/audit.jsonl", "blueprints", "chapters")
    errors = []
    for path in required:
        if not (root / path).exists():
            if path in ("blueprints", "chapters") and (root / "wiki" / path).exists():
                continue
            errors.append({"rule": "project.path", "problem": "missing required path: {}".format(path)})
    project_file = root / ".novelforge/state/project.json"
    if project_file.is_file():
        project = _read_json(project_file)
        if project.get("schema") != 1:
            errors.append({"rule": "project.schema", "problem": "unsupported project schema"})
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "warnings": []}


def load_project_config_for_path(path):
    """Find the nearest project profile for a file or project directory."""
    candidate = Path(path).resolve()
    start = candidate if candidate.is_dir() else candidate.parent
    for directory in (start,) + tuple(start.parents):
        project_file = directory / ".novelforge" / "state" / "project.json"
        if project_file.is_file():
            return _read_json(project_file)
    return {}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Novel text and project diagnostics")
    parser.add_argument("file_path", nargs="?", default="")
    parser.add_argument("--report-dir", default="")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check-project", action="store_true")
    parser.add_argument("--read-section", default="")
    args = parser.parse_args(argv)
    if args.read_section:
        if "#" not in args.read_section:
            parser.error("--read-section requires path.md#heading")
        path, anchor = args.read_section.split("#", 1)
        print(read_markdown_section(path, anchor), end="")
        return 0
    if args.check_project:
        result = check_project_integrity(args.file_path or ".")
    elif not args.file_path:
        parser.error("a file path is required")
    else:
        path = Path(args.file_path)
        config = load_project_config_for_path(path)
        result = run_lint(path, config=config)
    if args.report_dir:
        report = Path(args.report_dir) / (Path(args.file_path or "project").stem + "-lint.json")
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("status: {}".format(result["status"]))
        for item in result.get("errors", []) + result.get("warnings", []):
            print("{}: {}".format(item.get("rule", "diagnostic"), item.get("problem", "")))
    return 0 if result["status"] in ("PASS",) else 1


if __name__ == "__main__":
    sys.exit(main())
