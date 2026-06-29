#!/usr/bin/env python3
"""验证 ZIP 内容是否正常（无乱七八糟文件）"""
import zipfile, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_zip(path, label):
    print(f"\n=== {label} ===")
    try:
        zf = zipfile.ZipFile(path)
    except Exception as e:
        print(f"  ERROR: {e}")
        return
    names = zf.namelist()
    print(f"  总文件数: {len(names)}")

    junk_patterns = [".bak", "fix_", "force_", "patch_", "insert_", "implement_", "apply_", ".tmp"]
    bad = []
    for n in names:
        lowered = n.lower()
        if any(p in lowered for p in junk_patterns):
            bad.append(n)

    if bad:
        print(f"  ❌ 仍包含不该有的文件（{len(bad)} 个）:")
        for b in bad[:20]:
            print(f"    - {b}")
    else:
        print(f"  ✅ 无乱七八糟文件，内容干净")

    # 显示所有文件（前40个）
    print(f"  文件列表（共 {len(names)} 个）:")
    for n in sorted(names)[:40]:
        print(f"    {n}")
    if len(names) > 40:
        print(f"    ... 还有 {len(names)-40} 个")

print("\n验证完成")
