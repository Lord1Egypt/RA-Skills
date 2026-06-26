#!/usr/bin/env python3
"""
Meeting Assistant 依赖安装脚本
"""

import subprocess
import sys
import shutil


def check_command(cmd):
    return shutil.which(cmd) is not None


def main():
    print("=" * 50)
    print("  Meeting Assistant — 依赖检查与安装")
    print("=" * 50)

    issues = []
    ok = []

    # 1. ffmpeg
    print("\n[1/4] Checking ffmpeg...")
    if check_command("ffmpeg"):
        ok.append("ffmpeg")
        print("  ✓ ffmpeg found")
    else:
        issues.append("ffmpeg")
        print("  ✗ ffmpeg not found")
        print("    Install: sudo apt install ffmpeg")

    # 2. PulseAudio utilities
    print("\n[2/4] Checking PulseAudio...")
    if check_command("pactl"):
        ok.append("pulseaudio-utils")
        print("  ✓ pactl found")
    else:
        issues.append("pulseaudio-utils")
        print("  ✗ pactl not found")
        print("    Install: sudo apt install pulseaudio-utils")

    # 3. Whisper
    print("\n[3/4] Checking Whisper...")
    if check_command("whisper"):
        ok.append("whisper")
        print("  ✓ whisper found")
    else:
        issues.append("whisper")
        print("  ✗ whisper not found")
        print("    Install: pip install openai-whisper")

    # 4. Python dependencies
    print("\n[4/4] Checking Python packages...")
    required_packages = []
    for pkg in required_packages:
        try:
            __import__(pkg)
            ok.append(pkg)
            print(f"  ✓ {pkg}")
        except ImportError:
            issues.append(pkg)
            print(f"  ✗ {pkg}")

    # Summary
    print(f"\n{'=' * 50}")
    print(f"  Results: {len(ok)} OK, {len(issues)} missing")
    print(f"{'=' * 50}")

    if issues:
        print("\nTo install missing dependencies:")
        apt_pkgs = [p for p in issues if p in ("ffmpeg", "pulseaudio-utils")]
        pip_pkgs = [p for p in issues if p not in apt_pkgs]

        if apt_pkgs:
            print(f"  sudo apt install {' '.join(apt_pkgs)}")
        if pip_pkgs:
            print(f"  pip install {' '.join(pip_pkgs)}")

        resp = input("\nInstall automatically? [y/N]: ").strip().lower()
        if resp == "y":
            if apt_pkgs:
                print(f"\nInstalling: {' '.join(apt_pkgs)}")
                subprocess.run(["sudo", "apt", "install", "-y"] + apt_pkgs)
            if pip_pkgs:
                print(f"\nInstalling: {' '.join(pip_pkgs)}")
                subprocess.run([sys.executable, "-m", "pip", "install"] + pip_pkgs)
            print("\nDone! Run this script again to verify.")
        else:
            print("Skipped. Install manually when ready.")
    else:
        print("\nAll dependencies satisfied! Meeting Assistant is ready.")

    return len(issues) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
