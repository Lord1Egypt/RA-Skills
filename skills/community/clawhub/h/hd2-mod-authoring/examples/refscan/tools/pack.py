"""Pack refscan.lua into the Addon patch_0 + build the zip."""
import struct, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDON = b"mods/dsh/refscan"
LUA_TYPE = 0xA14E8DFA2CD117E2
PATCH = "9ba626afa44a3aa3.patch_0"


def murmur64(data):
    mask = (1 << 64) - 1
    m = 0xc6a4a7935bd1e995
    h = (len(data) * m) & mask
    end = len(data) // 8 * 8
    for offset in range(0, end, 8):
        k = int.from_bytes(data[offset:offset + 8], "little")
        k = k * m & mask
        k ^= k >> 47
        k = k * m & mask
        h = ((h ^ k) * m) & mask
    if end < len(data):
        h ^= int.from_bytes(data[end:], "little")
        h = h * m & mask
    h ^= h >> 47
    h = h * m & mask
    return h ^ (h >> 47)


def archive(source: bytes) -> bytes:
    marker = ("-- HD2-Addon: " + ADDON.decode() + "\n").encode()
    assert source.startswith(marker), "marker missing"
    assert b"\0" not in source
    payload = struct.pack("<II", len(source), 2) + source
    offset = 192
    length = offset + len(payload)
    header = struct.pack("<III20sQQ24s", 0xF0000011, 1, 1, b"", length, 0, b"")
    type_entry = struct.pack("<IIQIIII", 0, 0, LUA_TYPE, 1, 0, 16, 16)
    resource_entry = struct.pack("<7Q6I", murmur64(ADDON), LUA_TYPE, offset,
                                 0, 0, 0, 0, len(payload), 0, 0, 16, 16, 0)
    result = header + type_entry + resource_entry
    result += b"\0" * (offset - len(result)) + payload
    return result


def main():
    addon_dir = ROOT / "Addon"
    addon_dir.mkdir(exist_ok=True)
    src = (ROOT / "refscan.lua").read_bytes()
    data = archive(src)
    (addon_dir / PATCH).write_bytes(data)
    # round-trip verify
    assert struct.unpack_from("<III", data) == (0xF0000011, 1, 1)
    identity, type_id, start = struct.unpack_from("<QQQ", data, 104)
    size = struct.unpack_from("<I", data, 160)[0]
    length, version = struct.unpack_from("<II", data, start)
    assert identity == murmur64(ADDON) and type_id == LUA_TYPE
    assert size == length + 8 and version == 2
    assert data[start + 8:start + 8 + length] == src
    print(f"packed Addon/{PATCH} ({len(data)} bytes)")

    # empty sidecars
    (addon_dir / (PATCH + ".gpu_resources")).write_bytes(b"")
    (addon_dir / (PATCH + ".stream")).write_bytes(b"")

    # zip
    out = ROOT.parent / "refscan_diag.zip"
    with zipfile.ZipFile(out, "w") as z:
        for name in ("manifest.json", "thumbnail.png"):
            p = ROOT / name
            zi = zipfile.ZipInfo(name, (2026, 10, 5, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            z.writestr(zi, p.read_bytes())
        for name in (f"Addon/{PATCH}", f"Addon/{PATCH}.gpu_resources", f"Addon/{PATCH}.stream"):
            p = ROOT / name
            zi = zipfile.ZipInfo(name, (2026, 10, 5, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            z.writestr(zi, p.read_bytes())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
    print(f"{out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
