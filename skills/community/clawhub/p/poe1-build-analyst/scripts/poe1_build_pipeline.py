#!/usr/bin/env python3
"""PoE1 build analysis pipeline around qpooqp777/pob-cli.

The script treats PoE Ninja as an input source, not as a stable HTML API. Supply
--ninja-json with a permitted local export or confirmed JSON endpoint. It never
uploads a build and can emit a clearly provisional three-stage starter plan.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path_or_url: str) -> Any:
    if path_or_url.startswith(("http://", "https://")):
        req = urllib.request.Request(path_or_url, headers={"User-Agent": "poe1-build-analyst/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    return json.loads(Path(path_or_url).read_text(encoding="utf-8"))


def rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("builds", "results", "characters", "data", "rows"):
        value = payload.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    return []


def score_row(row: dict[str, Any]) -> float:
    for key in ("score", "dps", "totalDps", "TotalDPS", "depth", "rank"):
        value = row.get(key)
        try:
            number = float(value)
            return number if key != "rank" else -number
        except (TypeError, ValueError):
            pass
    return 0.0


MAX_POB_OUTPUT = 2_000_000


def resolve_pob_command() -> str:
    """Resolve only the intended `pob` executable; never execute user-supplied commands."""
    command = shutil.which("pob")
    if not command or Path(command).name != "pob" or not os.access(command, os.X_OK):
        raise RuntimeError("找不到受信任的 pob 執行檔；本 skill 不接受自訂或任意外部命令")
    return str(Path(command).resolve())


def run_pob(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    """Run the fixed PoB CLI with bounded runtime and captured output."""
    command = resolve_pob_command()
    if not args or Path(args[0]).name != "pob":
        raise ValueError("拒絕執行非 pob 命令")
    safe_args = [command, *args[1:]]
    try:
        completed = subprocess.run(
            safe_args, text=True, capture_output=True, check=False,
            timeout=max(1, min(timeout, 600)), cwd=os.getcwd()
        )
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "")[-MAX_POB_OUTPUT:]
        stderr = (exc.stderr or "")[-MAX_POB_OUTPUT:]
        raise RuntimeError(f"pob-cli 執行逾時：stdout={stdout!r} stderr={stderr!r}") from exc
    return completed.returncode, completed.stdout[-MAX_POB_OUTPUT:], completed.stderr[-MAX_POB_OUTPUT:]


def parse_pob_json(stdout: str) -> dict[str, Any]:
    """Accept only a bounded JSON object from PoB; reject arbitrary output."""
    if len(stdout) > MAX_POB_OUTPUT:
        raise ValueError("PoB 輸出超過安全大小上限")
    value = json.loads(stdout)
    if not isinstance(value, dict):
        raise ValueError("PoB 輸出不是 JSON object；拒絕注入非預期資料")
    return value


def validate_tree_connectivity(build_path: str, pob_root: str) -> dict[str, Any]:
    """Mandatory PoB TreeData gate for every XML entering official analysis."""
    build_file = Path(build_path).resolve()
    root = ET.parse(build_file).getroot()
    spec = root.find("Tree/Spec")
    if spec is None:
        raise ValueError("PoB XML 缺少 Tree/Spec；拒絕進入計算")
    tree_version = spec.get("treeVersion") or spec.get("tree_version")
    if not tree_version:
        raise ValueError("Tree/Spec 缺少 treeVersion；拒絕進入計算")
    nodes = [int(value) for value in spec.get("nodes", "").replace("\\n", ",").split(",") if value.strip()]
    class_value = spec.get("classId")
    class_id = int(class_value) if class_value not in (None, "") else None
    cli_root = os.environ.get("POB_CLI_ROOT", "/home/ubuntu/poe1-pob-cli")
    if cli_root not in sys.path:
        sys.path.insert(0, cli_root)
    from pob_cli.treedata import validate_tree_selection
    result = validate_tree_selection(pob_root, tree_version, nodes, class_id=class_id)
    if not result.get("valid"):
        raise ValueError("天賦連通性驗證失敗：" + "; ".join(result.get("errors", [])))
    return result


def starter_stages(skill: str, character_class: str, ascendancy: str) -> dict[str, dict[str, Any]]:
    """Return a conservative, explicitly provisional 3-stage starter plan."""
    return {
        "early": {
            "stage": "early",
            "level_range": "1-72",
            "main_skill": skill,
            "skill_links": [f"{skill} + controlled damage support", "movement + guard", "curse/defence utility"],
            "utility_and_defence": ["cap elemental resistances before maps", "life on every rare slot", "movement skill", "guard skill"],
            "passive_plan": "Path toward the class-appropriate damage and life clusters; delay expensive cluster jewels and reservation investments.",
            "equipment_targets": ["wand or sceptre with relevant spell damage", "life/resistance rares", "four-link or five-link body armour"],
            "stat_thresholds": {"elemental_resistances": "75% before maps", "life": "prioritize life on every rare"},
            "upgrade_triggers": ["enter maps after resistance cap", "switch only when the required gem or item is available"],
            "pob_metrics": {"status": "not_verified"},
            "assumptions": [f"class={character_class}", f"ascendancy={ascendancy}", "SC Trade league-start context"],
            "warnings": ["generic starter links require manual gem and patch verification"],
        },
        "mid": {
            "stage": "mid",
            "level_range": "72-90",
            "main_skill": skill,
            "skill_links": [f"six-link {skill} setup", "exposure/curse package", "movement, guard, and recovery package"],
            "utility_and_defence": ["life or ES recovery", "spell suppression or block plan", "ailment mitigation", "chaos resistance upgrade"],
            "passive_plan": "Complete the core damage route and add jewel or reservation nodes only after the defensive baseline is stable.",
            "equipment_targets": ["five-link then six-link", "weapon upgrade with required damage tags", "life/resistance rares with crafted suffixes"],
            "stat_thresholds": {"elemental_resistances": "75%", "chaos_resistance": "positive preferred", "spell_suppression": "scale if the tree supports it"},
            "upgrade_triggers": ["core skill package is online", "replace the weakest rare slot before buying luxury uniques"],
            "pob_metrics": {"status": "not_verified"},
            "assumptions": ["stable yellow/red maps", "prices are snapshots, not SSF availability"],
            "warnings": ["DPS depends on PoB configuration and uptime"],
        },
        "endgame": {
            "stage": "endgame",
            "level_range": "90+",
            "main_skill": skill,
            "skill_links": [f"final six-link {skill} setup", "bossing configuration", "mapping configuration"],
            "utility_and_defence": ["layered mitigation", "recovery under sustained hits", "ailment and curse mitigation", "pinnacle-boss configuration review"],
            "passive_plan": "Finish the verified tree, then compare luxury damage nodes against survivability using separate PoB XML candidates.",
            "equipment_targets": ["high-tier rare weapon", "influenced or crafted rares", "jewels only after core resistance and life/ES targets"],
            "stat_thresholds": {"elemental_resistances": "75%+ with map penalties accounted for", "defence": "verify with PoB, not estimates"},
            "upgrade_triggers": ["only purchase high-budget upgrades after the PoB delta is measured", "keep a boss and mapping configuration separately"],
            "pob_metrics": {"status": "not_verified"},
            "assumptions": ["high-budget or mature mapping context"],
            "warnings": ["no endgame number is official until pob calc succeeds on a compatible XML"],
        },
    }


def decode_pob_code(code: str) -> bytes:
    normalized = code.strip()
    if normalized.startswith(('https://pobb.in/', 'http://pobb.in/')):
        raise ValueError('請提供完整 PoB character code，不要提供短 pobb.in 網址；短網址不是可直接解碼的 code。')
    normalized += "=" * (-len(normalized) % 4)
    encoded = base64.urlsafe_b64decode(normalized)
    for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS):
        try:
            return zlib.decompress(encoded, wbits)
        except zlib.error:
            continue
    raise ValueError('PoB character code 不是可解壓縮的 zlib/raw-deflate XML code')


def load_code_argument(value: str) -> str:
    candidate = Path(value).expanduser()
    if candidate.exists():
        return candidate.read_text(encoding='utf-8').strip()
    return value.strip()


def endgame_stage(skill: str, character_class: str, ascendancy: str) -> dict[str, Any]:
    return {
        'stage': 'endgame',
        'level_range': '90+',
        'main_skill': skill,
        'skill_links': ['fixed from the supplied Ninja/character-data source'],
        'utility_and_defence': ['fixed from the supplied Ninja/character-data source'],
        'passive_plan': 'Do not optimize or rewrite the passive tree; preserve the supplied endgame character data.',
        'equipment_targets': ['fixed from the supplied Ninja/character-data source'],
        'stat_thresholds': {'source': 'PoE Ninja DB or supplied public character data', 'verification': 'official PoB calc'},
        'upgrade_triggers': ['compare a new Ninja character code or DB snapshot; do not silently mutate the imported build'],
        'pob_metrics': {'status': 'not_verified'},
        'assumptions': [f'class={character_class}', f'ascendancy={ascendancy}', 'Endgame-only workflow'],
        'warnings': ['Early and Mid are intentionally not generated in this mode.'],
    }


def endgame_analyze_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description='Analyze one fixed PoE1 Endgame character from a PoB code.')
    parser.add_argument('--pob-code', required=True, help='完整 PoB share/character code，或包含 code 的文字檔')
    parser.add_argument('--pob-root', default=os.environ.get('POB_ROOT'), required=True)
    # Deliberately no --pob-command: only the trusted executable named `pob` is allowed.
    parser.add_argument('--skill', required=True)
    parser.add_argument('--class', dest='character_class', default='Witch')
    parser.add_argument('--ascendancy', default='Occultist')
    parser.add_argument('--league', default='Curse of the Allflame')
    parser.add_argument('--build-name', default='Endgame character-code analysis')
    parser.add_argument('--ninja-source', help='optional Ninja DB JSON/character source for provenance only')
    parser.add_argument('--xml-output', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args(argv)
    try:
        xml = decode_pob_code(load_code_argument(args.pob_code))
        if not xml.lstrip().startswith(b'<?xml') and b'<PathOfBuilding' not in xml[:512]:
            raise ValueError('解碼結果不是 PathOfBuilding XML')
        Path(args.xml_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.xml_output).write_bytes(xml)
        analyze = run_pob(['pob', 'analyze', args.xml_output, '--pob-root', args.pob_root, '--skill', args.skill, '--format', 'json', '--timeout', str(args.timeout)], args.timeout)
        calc = run_pob(['pob', 'calc', args.xml_output, '--pob-root', args.pob_root, '--skill', args.skill, '--format', 'json', '--timeout', str(args.timeout)], args.timeout)
        if analyze[0] != 0 or calc[0] != 0:
            raise RuntimeError(f'pob-cli analyze/calc 失敗：analyze={analyze[2] or analyze[1]} calc={calc[2] or calc[1]}')
        report = {
            'schema_version': 3, 'mode': 'endgame-only', 'league': args.league,
            'build_name': args.build_name,
            'concept': {'class': args.character_class, 'ascendancy': args.ascendancy, 'main_skill': args.skill},
            'source': {'pob_code': 'provided', 'ninja_source': args.ninja_source, 'xml': str(Path(args.xml_output).resolve())},
            'stages': {'endgame': endgame_stage(args.skill, args.character_class, args.ascendancy)},
            'fixed_source_policy': {'tree': 'preserve imported character code', 'gems': 'preserve imported character code', 'items': 'preserve imported character code', 'early_mid': 'not generated'},
            'pob_verification': {'status': 'verified', 'analyze': parse_pob_json(analyze[1]), 'calc': parse_pob_json(calc[1])},
            'warnings': ['PoE Ninja DB/source is provenance only; imported character data is the fixed build authority.'],
        }
    except Exception as exc:
        report = {'schema_version': 3, 'mode': 'endgame-only', 'pob_verification': {'status': 'blocked', 'error': str(exc)}, 'stages': {}}
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'output': args.output, 'status': 'blocked', 'error': str(exc)}, ensure_ascii=False))
        return 2
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': args.output, 'xml': args.xml_output, 'status': 'verified', 'mode': 'endgame-only'}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and verify a PoE1 build report")
    parser.add_argument("--league", required=True)
    parser.add_argument("--skill", required=True, help="主技能，例如 Creeping Frost 或 Vortex")
    parser.add_argument("--class", dest="character_class", default="Witch")
    parser.add_argument("--ascendancy", default="Elementalist")
    parser.add_argument("--build-name", required=True)
    parser.add_argument("--ninja-json", help="本地 JSON 或允許的 JSON URL")
    parser.add_argument("--build", help="PoB XML；若提供則執行官方 PoB 分析")
    parser.add_argument("--pob-root", default=os.environ.get("POB_ROOT"))
    # Deliberately no --pob-command: only the trusted executable named `pob` is allowed.
    parser.add_argument("--output", required=True)
    parser.add_argument("--share-code", help="已由 pob share --dry-run 產生的 code；本腳本不會上傳")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    report: dict[str, Any] = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "league": args.league,
        "build_name": args.build_name,
        "concept": {"class": args.character_class, "ascendancy": args.ascendancy, "main_skill": args.skill},
        "source": {"ninja": args.ninja_json, "pob_xml": args.build},
        "ninja_candidates": [],
        "stages": {"endgame": endgame_stage(args.skill, args.character_class, args.ascendancy)},
        "pob_verification": {"status": "not_run", "warnings": []},
        "character_code": {"format": "pobb.in-compatible", "code": args.share_code, "uploaded": False},
        "warnings": [],
    }

    if args.ninja_json:
        try:
            rows = rows_from_payload(load_json(args.ninja_json))
            rows.sort(key=score_row, reverse=True)
            report["ninja_candidates"] = rows[: max(0, args.limit)]
        except Exception as exc:  # keep report usable for manual correction
            report["warnings"].append(f"Ninja JSON 讀取失敗：{exc}")
    else:
        report["warnings"].append("未提供 Ninja JSON；請先以允許的資料匯出或公開 JSON 來源取得推薦 Build。")

    if args.build:
        if not args.pob_root:
            report["pob_verification"] = {"status": "blocked", "warnings": ["缺少 --pob-root 或 POB_ROOT；天賦連通性閘門未執行"]}
        else:
            try:
                tree_report = validate_tree_connectivity(args.build, args.pob_root)
                report["tree_connectivity"] = {"status": "verified", **tree_report}
            except Exception as exc:
                report["tree_connectivity"] = {"status": "failed", "error": str(exc)}
                report["pob_verification"] = {"status": "blocked", "warnings": ["天賦連通性驗證失敗；拒絕執行 PoB 官方分析", str(exc)]}
                report["warnings"].append("PoB XML 未通過強制 TreeData 連通性閘門。")
                Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
                print(json.dumps({"output": args.output, "pob_status": "blocked", "tree_status": "failed"}, ensure_ascii=False))
                return 2
            base = ["pob", "analyze", args.build, "--pob-root", args.pob_root, "--skill", args.skill, "--format", "json"]
            rc, stdout, stderr = run_pob(base)
            if rc == 0:
                try:
                    report["pob_verification"] = {"status": "verified", "analysis": parse_pob_json(stdout), "stderr": stderr}
                except (json.JSONDecodeError, ValueError):
                    report["pob_verification"] = {"status": "failed", "stdout": stdout, "stderr": stderr}
            else:
                report["pob_verification"] = {"status": "failed", "returncode": rc, "stdout": stdout, "stderr": stderr}
                report["warnings"].append("PoB 官方計算未成功；不得把未驗證數字當成正式結論。")
    else:
        report["warnings"].append("未提供 PoB XML；本次只保存推薦資料與待驗證配置。")
        report["tree_connectivity"] = {"status": "not_run", "warning": "未提供 PoB XML；自動產生流程不得宣稱天賦已驗證。"}

    if not args.share_code:
        report["warnings"].append("未提供角色 code；先使用 pob share BUILD --dry-run 產生 code，再回填或重新執行。")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": args.output, "pob_status": report["pob_verification"]["status"], "candidate_count": len(report["ninja_candidates"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "optimize-tree":
        from poe1_tree_optimizer import main as optimize_tree_main
        sys.exit(optimize_tree_main(sys.argv[2:]))
    if len(sys.argv) > 1 and sys.argv[1] == "endgame-analyze":
        sys.exit(endgame_analyze_main(sys.argv[2:]))
    sys.exit(main())
