"""TTS 配音（Seed-TTS）."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
# _shared/ 定位：优先 bundled（scripts/_shared/），fallback monorepo 根
for _cand in (HERE.parent / "_shared", HERE.parents[2] / "_shared"):
    if (_cand / "config.py").exists():
        sys.path.insert(0, str(_cand))
        break

from ark_api import ArkClient
from config import PRICING, VOICE_PRESETS
from cost_guard import CostGuard
from checkpoint import Checkpoint


def auto_voice(char: dict) -> str:
    """根据 name/age 启发式选音色，用豆包大模型（_conversation_wvae_bigtts）."""
    if char.get("voice"):
        return char["voice"]
    name = char.get("name", "")
    age = str(char.get("age", "18"))
    is_female = any(k in name for k in ["妃", "娘", "女", "姬", "仙子", "娥", "媛"])
    is_elder = age.isdigit() and int(age) > 45
    is_mature = age.isdigit() and 30 < int(age) <= 45
    if is_female:
        if is_elder: return VOICE_PRESETS["female_elder"]
        if is_mature: return VOICE_PRESETS["female_mature"]
        return VOICE_PRESETS["female_young"]
    if is_elder: return VOICE_PRESETS["male_elder"]
    if is_mature: return VOICE_PRESETS["male_mature"]
    return VOICE_PRESETS["male_young"]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    script = json.loads(pathlib.Path(args.script).read_text())
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    project_dir = out_dir.parent
    guard = CostGuard.load(project_dir)
    cp = Checkpoint(project_dir)

    char_voice = {c["id"]: auto_voice(c) for c in script.get("characters", [])}

    client = ArkClient()
    manifest: dict = {}

    for scene in script.get("scenes", []):
        sid = scene["id"]
        scene_manifest = []
        for idx, d in enumerate(scene.get("dialogue", [])):
            cid = d.get("char")
            text = d.get("text", "").strip()
            if not text:
                continue
            out_path = out_dir / f"{sid}_{cid}_{idx}.wav"
            key = f"{sid}_{cid}_{idx}"
            if out_path.exists() or cp.sub_done("dubs", key):
                print(f"  ⏭️  {key} 已存在")
                scene_manifest.append({"path": str(out_path), "char": cid, "text": text})
                continue

            voice = char_voice.get(cid, VOICE_PRESETS["male_young"])
            print(f"  🎤 {key} [{voice}]: {text[:30]}")
            client.tts(text=text, voice=voice, out_path=out_path)
            guard.charge("dubs", key, len(text) * PRICING["tts_per_char"])
            cp.sub_mark("dubs", key)
            scene_manifest.append({
                "path": str(out_path), "char": cid, "text": text, "voice": voice,
            })
        if scene_manifest:
            manifest[sid] = scene_manifest

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    print(f"✅ 配音: {sum(len(v) for v in manifest.values())} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
