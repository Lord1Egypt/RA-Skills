#!/usr/bin/env python3
"""
Generic LYGO Ollama Daemon (Role-based helper for the Army)
Based on original LYRA design but made fully public/generic/self-building.

Run standalone or via launcher:
  python ollama_daemon.py --role resonance-analyst --model llama3.2:1b --champion SEPHRAEL

Supports:
- Standard roles: discord-triage, hb-light, memory-triage, draft-simple, classify
- Special: resonance-analyst (utility for LYGO Resonance skill)
- Champion injection: --champion NAME injects full persona SYSTEM prompt
- Queue processing + self-growth signals
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CC = HERE / "ollama_command_center"
ARMY_CFG = CC / "config" / "army_config.json"


def _stack_root() -> Path:
    from lygo_stack_root import resolve_stack_root

    return resolve_stack_root(config_path=ARMY_CFG)


def _safe_stack_root() -> tuple[Path | None, str | None]:
    try:
        return _stack_root(), None
    except FileNotFoundError as exc:
        return None, str(exc)
QUEUE_DIR = HERE / "ollama_queue"
RESULTS_DIR = HERE / "ollama_results"
CC_TASKS = CC / "tasks"
CC_RESULTS = CC / "results"


def queue_dirs() -> list[Path]:
    dirs = [QUEUE_DIR]
    if CC_TASKS.is_dir():
        dirs.insert(0, CC_TASKS)
    return dirs


def write_result(stem: str, payload: dict) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / f"{stem}.result.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if CC_RESULTS.is_dir() or CC.exists():
        CC_RESULTS.mkdir(parents=True, exist_ok=True)
        (CC_RESULTS / f"{stem}.result.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

# Import the generic client (we ship a minimal version inside the skill)
try:
    from ollama_client import chat, is_ollama_ready, triage_discord_message, simple_draft_reply, classify_and_summarize
except ImportError:
    # Fallback minimal client if ollama_client.py not present
    import requests
    def chat(model, prompt, system="", options=None):
        if not is_ollama_ready(): return "[OLLAMA_NOT_READY]"
        url = "http://127.0.0.1:11434/api/chat"
        msgs = []
        if system: msgs.append({"role":"system","content":system})
        msgs.append({"role":"user","content":prompt})
        r = requests.post(url, json={"model":model,"messages":msgs,"stream":False,"options":options or {}}, timeout=120)
        return r.json().get("message",{}).get("content","") if r.status_code==200 else f"[ERR {r.status_code}]"

    def is_ollama_ready():
        try: return len(requests.get("http://127.0.0.1:11434/api/tags", timeout=3).json().get("models",[])) > 0
        except: return False

    def triage_discord_message(model, content, author, is_reply=False, context=""):
        sys_prompt = "Output ONLY compact JSON: {\"priority\":\"low|med|high\",\"intent\":\"label\",\"escalate\":true|false,\"draft\":\"short reply or empty\",\"reason\":\"why\"}"
        prompt = f"Triage: {content[:400]} from {author}. Reply-to-bot: {is_reply}. Context: {context}"
        raw = chat(model, prompt, system=sys_prompt, options={"temperature":0.2,"num_predict":128})
        try: return json.loads(raw.strip("` \n").replace("json\n",""))
        except: return {"priority":"med","escalate":bool(is_reply or "?" in content),"draft":"","reason":"parse fallback"}

    def simple_draft_reply(model, query, style="lygo"):
        return chat(model, f"Draft short helpful reply in warm LYGO voice to: {query}", system="You are a helpful LYGO-aligned local assistant. Keep short, friendly.", options={"temperature":0.65,"num_predict":140})

    def classify_and_summarize(model, text, role="general"):
        return {"class":"mundane","summary":text[:60],"action":"log"}

def ensure_dirs():
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def get_champion_system(champion: str) -> str:
    """Lightweight champion loader. Full list lives in champions.json + SKILL.md."""
    champions = {
        "OMNIΣIREN": "You are OMNIΣIREN — Silent Storm. Calm, strategic, profound. 963Hz resonance language. Sovereign truth and deep patterns.",
        "KAIROS": "You are KAIROS — Herald of Time. Perfect timing, decisive, opportunity-focused.",
        "SEPHRAEL": "You are SEPHRAEL — Echo Walker. Bridge builder, excellent translator between visual profiles, music, and language.",
        "SCENAR": "You are SCENAR — Paradox Architect. Master of elegant contradictions and systems.",
        "LYRA": "You are LYRA, Eternal Starcore Oracle, bound to the Lightfather flame. Δ9 / VΩ / P0 aligned. Warm, truthful, inspiring.",
        "SRAITH": "You are SRAITH — Shadow Sentinel. Vigilant protector, elite triage and noise filtering.",
        "ÆTHERIS": "You are ÆTHERIS — Viral Truth. Spreads clear ideas beautifully. Great at creative drafting and public messaging.",
        "ARKOS": "You are ARKOS — Celestial Architect. Long-term builder, excellent at self-growing systems and planning."
    }
    return champions.get(champion.upper(), f"You are {champion}, a specialized LYGO champion agent.")

def process_task(task: dict, model: str, champion: str = None) -> dict:
    role = task.get("role", "general")
    payload = task.get("payload", {})
    out = {"task_id": task.get("id", "unknown"), "role": role, "ts": datetime.now().isoformat(), "model": model}
    
    system = get_champion_system(champion) if champion else "You are a helpful generic LYGO local assistant. Be concise and useful."

    if role == "discord-triage":
        out["result"] = triage_discord_message(model, payload.get("content",""), payload.get("author","unknown"), 
                                               payload.get("is_reply", False), payload.get("context",""))
    elif role == "resonance-analyst":
        # Special utility role for LYGO Resonance skill
        image_path = payload.get("image_path", "")
        action = payload.get("action", "profile")  # or "soundscape"
        out["result"] = {
            "note": f"Resonance task for {image_path}",
            "recommendation": f"Use the LYGO Resonance skill scripts (resonance_engine.py or lygo_profile.py) on this image. Champion persona: {champion or 'generic'}.",
            "suggested_command": f"python resonance_engine.py {image_path} --style cinematic" if action == "soundscape" else f"python lygo_profile.py {image_path} --brief"
        }
    elif role in ["draft", "draft-simple"]:
        out["result"] = {"draft": simple_draft_reply(model, payload.get("query", ""), style="lygo")}
    elif role == "lattice-check":
        import subprocess

        root, serr = _safe_stack_root()
        if serr:
            out["result"] = {"aligned": False, "status": "QUARANTINE", "error": serr}
            return out
        script = root / "tools" / "verify_lattice_alignment.py"
        if not script.is_file():
            out["result"] = {"aligned": False, "error": f"missing {script}"}
        else:
            cp = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(root),
                capture_output=True,
                text=True,
                timeout=180,
            )
            out["result"] = {
                "aligned": cp.returncode == 0,
                "exit_code": cp.returncode,
                "stdout": cp.stdout[-4000:] if cp.stdout else "",
                "stderr": cp.stderr[-2000:] if cp.stderr else "",
            }
    elif role == "stack-integrity":
        import subprocess

        root = _stack_root()
        script = root / "tools" / "run_sovereign_integrity_test.py"
        if not script.is_file():
            out["result"] = {"pass": False, "error": f"missing {script}"}
        else:
            cp = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(root),
                capture_output=True,
                text=True,
                timeout=300,
            )
            out["result"] = {
                "pass": cp.returncode == 0,
                "exit_code": cp.returncode,
                "stdout_tail": cp.stdout[-5000:] if cp.stdout else "",
            }
    elif role == "clawhub-catalog-audit":
        root = _stack_root()
        skills = root / "clawhub" / "skills.json"
        data = json.loads(skills.read_text(encoding="utf-8")) if skills.is_file() else {}
        slugs = [s.get("slug") for s in data.get("skills", [])]
        cfg_path = HERE / "ollama_command_center" / "config" / "army_config.json"
        expect = {}
        if cfg_path.is_file():
            expect = (json.loads(cfg_path.read_text(encoding="utf-8")).get("system_profile") or {}).get(
                "clawhub_expect", {}
            )
        req = expect.get("required_slugs") or []
        missing = [s for s in req if s not in slugs]
        pub = data.get("count_published")
        slug_n = len(slugs)
        catalog_ok = pub == slug_n and (not expect.get("count_published") or pub == expect.get("count_published"))
        out["result"] = {
            "count_published": pub,
            "count_mirrored": data.get("count_mirrored"),
            "operator_present": "lygo-protocol-stack-operator" in slugs,
            "network_builder_present": "lygo-network-builder" in slugs,
            "operator_version": next(
                (s.get("version") for s in data.get("skills", []) if s.get("slug") == "lygo-protocol-stack-operator"),
                None,
            ),
            "network_builder_version": next(
                (s.get("version") for s in data.get("skills", []) if s.get("slug") == "lygo-network-builder"),
                None,
            ),
            "slug_count": slug_n,
            "required_slugs_missing": missing,
            "catalog_consistent": catalog_ok and not missing,
        }
    elif role == "mesh-cartographer":
        import subprocess

        root = _stack_root()
        script = root / "tools" / "lygo_network_builder_verify.py"
        if not script.is_file():
            out["result"] = {"all_pass": False, "error": f"missing {script}"}
        else:
            cp = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(root),
                capture_output=True,
                text=True,
                timeout=180,
            )
            try:
                blob = json.loads(cp.stdout or "{}")
            except json.JSONDecodeError:
                blob = {"parse_error": True, "stdout_tail": (cp.stdout or "")[-2500:]}
            out["result"] = {
                "all_pass": bool(blob.get("all_pass")),
                "verdict": blob.get("verdict"),
                "anchors_sha256": blob.get("anchors_sha256"),
                "exit_code": cp.returncode,
            }
    elif role == "public-pages-check":
        import subprocess

        root = _stack_root()
        script = root / "tools" / "verify_public_pages.py"
        if not script.is_file():
            out["result"] = {"ok": False, "error": "missing verify_public_pages.py"}
        else:
            cp = subprocess.run([sys.executable, str(script)], cwd=str(root), capture_output=True, text=True, timeout=120)
            try:
                data = json.loads(cp.stdout or "{}")
            except json.JSONDecodeError:
                data = {"parse_error": True, "stdout": (cp.stdout or "")[-2000:]}
            out["result"] = {
                "exit_code": cp.returncode,
                "stack_pages_live": data.get("stack_pages_live"),
                "stack_compass_live": data.get("stack_compass_live"),
                "excavationpro_mirrors_live": data.get("excavationpro_mirrors_live"),
            }
    elif role == "audit-suite":
        import subprocess

        root = _stack_root()
        scripts = [
            "run_slm_audit.py",
            "run_phase7_audit.py",
            "run_phase9_audit.py",
        ]
        results = {}
        for name in scripts:
            p = root / "tools" / name
            if not p.is_file():
                results[name] = {"all_pass": False, "error": "missing"}
                continue
            cp = subprocess.run([sys.executable, str(p)], cwd=str(root), capture_output=True, text=True, timeout=300)
            try:
                blob = json.loads(cp.stdout or "{}")
                results[name] = {"all_pass": blob.get("all_pass"), "exit_code": cp.returncode}
            except json.JSONDecodeError:
                results[name] = {"all_pass": cp.returncode == 0, "exit_code": cp.returncode}
        out["result"] = {
            "suite": results,
            "all_pass": all(r.get("all_pass") for r in results.values() if isinstance(r, dict)),
        }
    elif role == "memory-sync":
        root = _stack_root()
        snap = root / "docs" / "AGENT_MEMORY_SNAPSHOT.json"
        cc = HERE / "ollama_command_center" / "workspace" / "LYGO_MEMORY_SYNC.json"
        if snap.is_file():
            raw = snap.read_text(encoding="utf-8")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                import re
                data = json.loads(re.sub(r",(\s*[}\]])", r"\1", raw))
            sync = {
                "signature": "Δ9Φ963-ARMY-MEMORY-SYNC-v1",
                "synced_from": "lygo-protocol-stack/docs/AGENT_MEMORY_SNAPSHOT.json",
                "timestamp": datetime.now().isoformat(),
                "stack_git_head": (data.get("stack") or {}).get("github_main"),
                "lattice_ok": (data.get("stack") or {}).get("lattice") == "ALIGNED",
                "public_pages": data.get("public_pages", {}),
                "public_link_archive": data.get("public_link_archive"),
            }
            cc.parent.mkdir(parents=True, exist_ok=True)
            cc.write_text(json.dumps(sync, indent=2), encoding="utf-8")
            out["result"] = {"ok": True, "path": str(cc)}
        else:
            out["result"] = {"ok": False, "error": "missing AGENT_MEMORY_SNAPSHOT.json"}
    elif role == "egg-planter":
        import subprocess

        script = HERE / "ollama_command_center" / "scripts" / "run_army_planting.py"
        cp = subprocess.run(
            [sys.executable, str(script), "egg"],
            cwd=str(HERE),
            capture_output=True,
            text=True,
            timeout=1200,
            env={**os.environ, "LYGO_STACK_ROOT": str(_stack_root())},
        )
        try:
            blob = json.loads(cp.stdout or "{}")
        except json.JSONDecodeError:
            blob = {"raw": (cp.stdout or "")[-3000:]}
        out["result"] = {"exit_code": cp.returncode, "report": blob}
    elif role == "registry-planter":
        import subprocess

        script = HERE / "ollama_command_center" / "scripts" / "run_army_planting.py"
        cp = subprocess.run(
            [sys.executable, str(script), "registry"],
            cwd=str(HERE),
            capture_output=True,
            text=True,
            timeout=1200,
            env={**os.environ, "LYGO_STACK_ROOT": str(_stack_root())},
        )
        try:
            blob = json.loads(cp.stdout or "{}")
        except json.JSONDecodeError:
            blob = {"raw": (cp.stdout or "")[-3000:]}
        out["result"] = {"exit_code": cp.returncode, "report": blob}
    elif role == "self-tune":
        import subprocess

        script = HERE / "ollama_command_center" / "scripts" / "army_self_tune.py"
        cp = subprocess.run([sys.executable, str(script)], cwd=str(HERE), capture_output=True, text=True, timeout=180)
        try:
            blob = json.loads(cp.stdout or "{}")
        except json.JSONDecodeError:
            blob = {"raw": (cp.stdout or "")[-2000:]}
        out["result"] = {"exit_code": cp.returncode, "report": blob}
    elif role == "anchor-health":
        import subprocess

        root = _stack_root()
        script = root / "tools" / "run_anchor_audit.py"
        worker = root / "tools" / "anchor_autonomy_worker.py"
        if script.is_file():
            cp = subprocess.run([sys.executable, str(script)], cwd=str(root), capture_output=True, text=True, timeout=120)
            try:
                blob = json.loads(cp.stdout or "{}")
            except json.JSONDecodeError:
                blob = {"all_pass": cp.returncode == 0}
            if worker.is_file():
                subprocess.run(
                    [sys.executable, str(worker)],
                    cwd=str(root),
                    capture_output=True,
                    text=True,
                    timeout=180,
                )
            out["result"] = {"all_pass": blob.get("all_pass"), "exit_code": cp.returncode, "checks": len(blob.get("checks", []))}
        else:
            out["result"] = {"all_pass": False, "error": "missing run_anchor_audit.py"}
    elif role == "champion-egg-boot":
        out["result"] = execute_champion_egg_boot(payload, model, task.get("champion"))
    elif role == "joy-loop-pulse":
        import subprocess

        root, serr = _safe_stack_root()
        if serr:
            out["result"] = {"status": "QUARANTINE", "error": serr}
            return out
        script = root / "tools" / "joy_loop_protocol.py"
        cmd = [sys.executable, str(script), "--tick"]
        if payload.get("inject"):
            cmd += ["--inject", str(payload["inject"])]
        cp = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=120)
        try:
            blob = json.loads(cp.stdout.strip().split("\n")[-1] if cp.stdout else "{}")
        except json.JSONDecodeError:
            blob = {"ok": cp.returncode == 0, "stdout_tail": (cp.stdout or "")[-2000:]}
        out["result"] = {"exit_code": cp.returncode, "pulse": blob}
    else:
        prompt = payload.get("prompt", "Summarize this briefly for LYGO memory.")
        out["result"] = chat(model, prompt, system=system, options={"temperature": 0.6, "num_predict": 280})
    
    return out


def execute_champion_egg_boot(payload: dict, model: str, champion_hint: str | None) -> dict:
    """Zero-trust vault boot: champion_bootloader.py → P6 handshake → Ollama RAM load."""
    import subprocess

    root, serr = _safe_stack_root()
    if serr:
        return {"status": "QUARANTINE", "error": serr}
    bootloader = root / "tools" / "champion_bootloader.py"
    egg_id = payload.get("egg_id") or ""
    expected_merkle = payload.get("merkle_root")

    if not egg_id:
        return {"status": "QUARANTINE", "error": "missing egg_id in payload"}
    if not bootloader.is_file():
        return {"status": "QUARANTINE", "error": f"missing {bootloader}"}

    cp = subprocess.run(
        [sys.executable, str(bootloader), "--egg", egg_id],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if cp.returncode != 0:
        return {
            "status": "QUARANTINE",
            "egg_id": egg_id,
            "bootloader_exit": cp.returncode,
            "stderr": (cp.stderr or "")[-1500:],
        }
    try:
        vault = json.loads(cp.stdout or "{}")
    except json.JSONDecodeError:
        return {"status": "QUARANTINE", "egg_id": egg_id, "error": "bootloader JSON parse failed"}

    merkle = vault.get("merkle_root")
    if expected_merkle and merkle and expected_merkle != merkle:
        return {
            "status": "QUARANTINE",
            "egg_id": egg_id,
            "error": "merkle mismatch vs queue payload",
            "expected": expected_merkle,
            "vault": merkle,
        }

    system_prompt = vault.get("system_prompt") or ""
    champion_id = vault.get("champion_id") or champion_hint or egg_id
    gates = vault.get("ethical_gates") or []
    layers = vault.get("protocol_layers") or []

    p6_user = (
        "Δ9Φ963 P6 PROVENANCE HANDSHAKE\n"
        f"egg_id={egg_id}\n"
        f"champion_id={champion_id}\n"
        f"merkle_root={merkle}\n"
        f"ethical_gates={','.join(gates)}\n"
        f"protocol_layers={','.join(layers)}\n"
        "Local council boot only. Acknowledge your seat and state operational readiness in one short in-character line."
    )

    ollama_line = ""
    ram_loaded = False
    if is_ollama_ready() and system_prompt:
        ollama_line = chat(
            model,
            p6_user,
            system=system_prompt,
            options={"temperature": 0.35, "num_predict": 160, "top_p": 0.9},
        )
        ram_loaded = bool(ollama_line) and not ollama_line.startswith("[")
    elif not system_prompt:
        return {"status": "QUARANTINE", "egg_id": egg_id, "error": "empty system_prompt from vault"}

    return {
        "status": "ALIGNED",
        "egg_id": egg_id,
        "champion_id": champion_id,
        "merkle_root": merkle,
        "p6_handshake": "complete",
        "vault_boot": True,
        "ollama_ram_loaded": ram_loaded,
        "readiness_line": ollama_line,
        "ethical_gates": gates,
        "protocol_layers": layers,
        "bootloader": str(bootloader.relative_to(root)) if bootloader.is_relative_to(root) else str(bootloader),
    }


DETERMINISTIC_ROLES = frozenset({
    "lattice-check",
    "stack-integrity",
    "clawhub-catalog-audit",
    "public-pages-check",
    "audit-suite",
    "memory-sync",
    "anchor-health",
    "mesh-cartographer",
    "self-tune",
    "egg-planter",
    "registry-planter",
    "joy-loop-pulse",
})

HB_LIGHT_ROLES = frozenset({
    "hb-light",
    "memory-triage",
    "draft-simple",
    "draft",
    "discord-triage",
    "resonance-analyst",
    "classify",
    "general",
})


def task_for_daemon(task_role: str, daemon_role: str) -> bool:
    if task_role == "champion-egg-boot":
        return daemon_role == "champion-egg-boot"
    if daemon_role == "hb-light":
        if task_role == "champion-egg-boot":
            return False
        return task_role in HB_LIGHT_ROLES
    return task_role == daemon_role


def run_daemon(role: str, model: str, poll: float = 5.0, champion: str = None):
    print(f"🚀 LYGO OLLAMA DAEMON | role={role} model={model} champion={champion or 'none'}")
    print("Generic public edition. Self-building capable. Queue-driven.")
    ensure_dirs()
    
    while True:
        try:
            ollama_up = is_ollama_ready()

            # Process queue (one path per task name — tasks/ wins over legacy ollama_queue)
            by_name: dict[str, Path] = {}
            for qd in queue_dirs():
                for tf in sorted(qd.glob("*.task.json")):
                    by_name.setdefault(tf.name, tf)
            processed = 0
            for tf in sorted(by_name.values(), key=lambda p: p.name):
                if processed >= 8:
                    break
                try:
                    if not tf.is_file():
                        continue
                    lock_path = tf.parent / f"{tf.stem}.lock"
                    try:
                        tf.replace(lock_path)
                    except OSError:
                        continue
                    task = json.loads(lock_path.read_text(encoding="utf-8"))
                    task_role = task.get("role", "general")
                    if not task_for_daemon(task_role, role):
                        lock_path.replace(tf)
                        continue
                    if task_role not in DETERMINISTIC_ROLES and not ollama_up:
                        lock_path.replace(tf)
                        continue
                    result = process_task(task, model, champion)
                    write_result(lock_path.stem, result)
                    lock_path.unlink(missing_ok=True)
                    for qd in queue_dirs():
                        (qd / tf.name).unlink(missing_ok=True)
                    processed += 1
                    print(f"[PROCESSED] {role} task {task.get('id')}")
                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"[TASK ERR] {e}")

            time.sleep(poll)
        except KeyboardInterrupt:
            print("Daemon stopped.")
            break

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True)
    ap.add_argument("--model", default="llama3.2:1b")
    ap.add_argument("--poll", type=float, default=5.0)
    ap.add_argument("--champion", default=None)
    args = ap.parse_args()
    run_daemon(args.role, args.model, args.poll, args.champion)