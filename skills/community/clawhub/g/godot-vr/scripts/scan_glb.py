#!/usr/bin/env python3
"""Scan GLB files for degenerate / stretched triangles.

Use when a mesh renders broken (spikes, hairline streaks, stray far
geometry) and a screenshot can't tell you why: this flags the bad
triangles directly in the binary, before you blame the engine's import.

Usage:
    python scan_glb.py file.glb [more.glb ...] [--ratio 4.0]

A triangle is flagged when any edge exceeds --ratio x the mesh's max
bounding-box extent (a stray vertex / fan artifact), or when two of
its indices are equal (degenerate). Exit 1 if anything is flagged.

GLB layout (per spec): 12-byte header (magic, version, total length),
then chunks of [u32 length][u32 type] — JSON first (0x4E4F534A), BIN
second (0x004E4942), JSON chunk padded to a 4-byte boundary.

Blender 5.3 exporter quirk (benign): the index accessor declares
componentType 5123 (uint32) while the index bufferView holds 2-byte
indices. Godot renders such files fine (it infers the index type from
the bufferView size); this scanner does the same inference, so the
quirk is not flagged.
"""
import json
import struct
import sys

VEC_CNT = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
COMP_BYTES = {5120: 1, 5121: 2, 5122: 4, 5123: 4, 5125: 4, 5126: 8}
COMP_FMT = {5120: "b", 5121: "h", 5122: "i", 5123: "I", 5125: "f", 5126: "d"}


def load(path):
    raw = open(path, "rb").read()
    magic, version, total = struct.unpack_from("<4sII", raw, 0)
    if magic != b"glTF":
        raise SystemExit(f"{path}: not a GLB (bad magic)")
    if total != len(raw):
        print(f"  note: header length {total} != file size {len(raw)}")
    clen, ctype = struct.unpack_from("<II", raw, 12)
    if ctype != 0x4E4F534A:
        raise SystemExit(f"{path}: first chunk is not JSON")
    js = json.loads(raw[20:20 + clen])
    pad = (-clen) % 4
    off = 20 + clen + pad
    blen, btype = struct.unpack_from("<II", raw, off)
    if btype != 0x004E4942:
        raise SystemExit(f"{path}: second chunk is not BIN")
    return js, raw[off + 8:off + 8 + blen]


def read_accessor(js, ai, bin_):
    a = js["accessors"][ai]
    bv = js["bufferViews"][a["bufferView"]]
    off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    cnt, comp, vecs = a["count"], a["componentType"], VEC_CNT[a["type"]]
    cb = COMP_BYTES[comp]
    avail = len(bin_) - off
    if cnt * vecs * cb > avail:
        # Blender 5.3 quirk: uint32 declared, uint16 stored.
        if comp == 5123 and cnt * vecs * 2 <= avail:
            comp, cb = 5121, 2
        else:
            raise SystemExit(
                f"  accessor {ai}: stride {cnt * vecs * cb} exceeds bufferView ({avail} left)")
    flat = struct.unpack_from("<" + COMP_FMT[comp] * cnt * vecs, bin_, off)
    if vecs == 1:  # SCALAR accessors (indices): flat ints, not 1-tuples
        return list(flat)
    return [flat[i * vecs:(i + 1) * vecs] for i in range(cnt)]


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def scan(path, ratio):
    js, bin_ = load(path)
    bad = 0
    for mi, mesh in enumerate(js.get("meshes", [])):
        prims = mesh.get("primitives", [])
        if not prims or not all("indices" in p for p in prims):
            print(f"  note: mesh {mi} has no/missing index accessors — skipped")
            continue
        pos, idx = [], []
        for p in prims:
            base = len(pos)
            pos.extend(read_accessor(js, p["attributes"]["POSITION"], bin_))
            idx.extend(i + base for i in read_accessor(js, p["indices"], bin_))
        if len(pos) < 3:
            continue
        ext = max(max(v[i] for v in pos) - min(v[i] for v in pos) for i in range(3))
        lim = ratio * ext
        for t in range(0, len(idx), 3):
            a, b, c = idx[t], idx[t + 1], idx[t + 2]
            if a == b or b == c or a == c:
                print(f"  MESH {mi} tri {t // 3}: degenerate (indices {a},{b},{c})")
                bad += 1
            else:
                m = max(dist(pos[a], pos[b]), dist(pos[b], pos[c]), dist(pos[a], pos[c]))
                if m > lim:
                    print(f"  MESH {mi} tri {t // 3}: edge {m:.3f} > {lim:.3f} "
                          f"(bbox extent {ext:.3f}); verts {a},{b},{c} "
                          f"= {pos[a]},{pos[b]},{pos[c]}")
                    bad += 1
    print(f"{path}: {bad} flagged triangle(s)" + ("" if bad else " — clean"))
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ratio = 4.0
    for i, a in enumerate(sys.argv[1:]):
        if a.startswith("--ratio"):
            ratio = float(a.split("=", 1)[1]) if "=" in a else float(sys.argv[i + 1])
    if not args:
        raise SystemExit(__doc__)
    total = sum(scan(path, ratio) for path in args)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
