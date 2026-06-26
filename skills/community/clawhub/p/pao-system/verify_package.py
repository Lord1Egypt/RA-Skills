#!/usr/bin/env python3
"""验证打包结果"""
import tarfile
import os

dist_dir = "dist"
tar_file = os.path.join(dist_dir, "pao_system-0.1.0.tar.gz")

if not os.path.exists(tar_file):
    print(f"[ERROR] {tar_file} not found")
    exit(1)

print(f"[INFO] Checking {tar_file}...")
print("-" * 50)

with tarfile.open(tar_file, "r:gz") as tar:
    members = tar.getmembers()
    
    # 检查 requirements.txt
    has_requirements = False
    for m in members:
        if "requirements.txt" in m.name:
            has_requirements = True
            print(f"[OK] Found: {m.name}")
    
    if not has_requirements:
        print("[ERROR] requirements.txt NOT found in package!")
    else:
        print("\n[SUCCESS] requirements.txt is included")
    
    # 列出所有文件（前20个）
    print("\n[INFO] Package contents (first 20 files):")
    for i, m in enumerate(members[:20]):
        print(f"  {m.name}")
    
    if len(members) > 20:
        print(f"  ... and {len(members) - 20} more files")
