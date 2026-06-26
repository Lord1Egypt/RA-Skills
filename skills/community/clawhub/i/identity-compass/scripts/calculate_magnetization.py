#!/usr/bin/env python3
"""Calculate magnetization from vectors.json."""

import json
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPTS_DIR.parent.parent.parent / "obsidian-vault" / "compass"


def vec_len(v):
    return math.sqrt(sum(x * x for x in v))


def vec_normalize(v):
    l = vec_len(v)
    return [x / l for x in v] if l > 0 else v


def main():
    vectors_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SCRIPTS_DIR / "vectors.json"
    if not vectors_path.exists():
        print("No vectors.json found. Run export_vectors.py first.")
        return

    vectors = json.loads(vectors_path.read_text(encoding="utf-8"))
    if not vectors:
        print("No vectors to process.")
        return

    # Weighted vector sum (intensity × confidence × direction)
    M = [0.0, 0.0, 0.0]
    cluster_vecs = defaultdict(lambda: {"sum": [0.0, 0.0, 0.0], "count": 0})

    for v in vectors:
        d = v["direction"]
        w = v["intensity"] * v["confidence"]
        for i in range(3):
            M[i] += d[i] * w
            cluster_vecs[v["cluster"]]["sum"][i] += d[i] * w
        cluster_vecs[v["cluster"]]["count"] += 1

    N = len(vectors)
    mag = vec_len(M) / N if N > 0 else 0
    M_dir = vec_normalize(M)

    # Cluster magnetization
    clusters = {}
    for name, data in cluster_vecs.items():
        c_mag = vec_len(data["sum"]) / data["count"] if data["count"] > 0 else 0
        clusters[name] = {
            "direction": vec_normalize(data["sum"]),
            "magnetization": round(c_mag, 4),
            "count": data["count"],
        }

    result = {
        "timestamp": datetime.now().isoformat(),
        "total_vectors": N,
        "magnetization_vector": [round(x, 4) for x in M_dir],
        "magnetization_magnitude": round(mag, 4),
        "clusters": clusters,
    }

    out_path = SCRIPTS_DIR / "magnetization.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Magnetization: {mag:.4f} (N={N})")
    print(f"Direction: [{', '.join(f'{x:.3f}' for x in M_dir)}]")

    # Update vault magnetization.md
    md_path = VAULT_DIR / "magnetization.md"
    axes = ["자율성↔구조", "깊이↔폭", "혁신↔안정"]
    lines = [
        "---",
        "type: magnetization",
        f"updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "---",
        "",
        "# 자화도 리포트 🧲",
        "",
        f"**전체 자화도**: {mag:.4f} / 1.0",
        f"**벡터 수**: {N}",
        f"**자화 방향**: `[{', '.join(f'{x:.3f}' for x in M_dir)}]`",
        "",
        "## 축별 해석",
        "",
    ]
    for i, axis in enumerate(axes):
        val = M_dir[i]
        direction = axis.split("↔")[0] if val > 0 else axis.split("↔")[1]
        lines.append(f"- **{axis}**: {val:+.3f} → {direction} 성향")
    lines += [
        "",
        "## 클러스터별 자화도",
        "",
    ]
    for name, data in sorted(clusters.items()):
        lines.append(f"- **[[{name}]]**: {data['magnetization']:.4f} ({data['count']}개 벡터)")
    lines += [
        "",
        f"> 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {md_path}")


if __name__ == "__main__":
    main()
