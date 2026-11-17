#!/usr/bin/env python3
"""Standalone release and fixture checks; no network or sibling Skill required."""
from pathlib import Path
import re, struct, sys
ROOT = Path(__file__).resolve().parents[1]
required = ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "fixtures/success.md", "fixtures/failure.md", "README.md", "README.en.md", "LICENSE", "icon-512.png", "assets/promo-1600x900.png"]
errors = [f"missing: {name}" for name in required if not (ROOT / name).is_file()]
def read(name):
    path = ROOT / name
    return path.read_text(encoding="utf-8") if path.exists() else ""
def png_size(path):
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n": raise ValueError(f"{path.name} is not PNG")
    return struct.unpack(">II", data[16:24])
for name, expected in [("icon-512.png", (512, 512)), ("assets/promo-1600x900.png", (1600, 900))]:
    try:
        if png_size(ROOT / name) != expected: errors.append(f"{name} must be {expected[0]}x{expected[1]}")
    except (OSError, ValueError) as exc: errors.append(str(exc))
skill, manifest, agent = read("SKILL.md"), read("manifest.yaml"), read("agents/openai.yaml")
success, failure = read("fixtures/success.md"), read("fixtures/failure.md")
if not re.search(r"(?m)^name: novel-world-rule-check-cn$", skill): errors.append("SKILL frontmatter name mismatch")
if not re.search(r"(?m)^name: novel-world-rule-check-cn$", manifest) or not re.search(r"(?m)^slug: novel-world-rule-check-cn$", manifest): errors.append("manifest name/slug mismatch")
if not re.search(r"(?m)^repository: https://github\.com/xxjrq/novel-world-rule-check-cn$", manifest): errors.append("repository mismatch")
for field in ("display_name", "short_description", "default_prompt", "icon_small", "icon_large"):
    if not re.search(rf'(?m)^  {field}: ".+"$', agent): errors.append(f"openai interface.{field} must be a quoted string")
if len(re.search(r'(?m)^  short_description: "(.*)"$', agent).group(1)) not in range(25, 65): errors.append("short_description length must be 25..64")
if "$novel-world-rule-check-cn" not in agent: errors.append("default_prompt must mention $novel-world-rule-check-cn")
if "allow_implicit_invocation: true" not in agent: errors.append("implicit invocation policy missing")
if "../" in agent: errors.append("agent icon path must be relative to Skill root")
for filename in re.findall(r'(?m)^  icon_(?:small|large): "\./?([^"]+)"$', agent):
    if not (ROOT / filename).is_file(): errors.append(f"missing agent icon: {filename}")
if "| R-01 |" not in success or "冲突" not in success or "待补充信息：无" not in success: errors.append("success fixture lacks concrete conflict delivery")
if "不能判定" not in failure or "请补充正式规则清单" not in failure or "没有追加任何例外" not in failure: errors.append("failure fixture lacks missing-rule request")
if "fixtures/success.md" not in read("README.md") or "fixtures/failure.md" not in read("README.md"): errors.append("Chinese README must link both fixtures")
if "assets/promo-1600x900.png" not in read("README.md"): errors.append("Chinese README must show promo")
if not re.search(r"(?m)^## 使用$", read("README.md")): errors.append("Chinese README must include a usage section")
if errors: print("SELF-TEST FAILED\n" + "\n".join(errors)); sys.exit(1)
print("SELF-TEST PASSED: standalone release contract, image dimensions, icon references, and success/failure reference deliveries verified.")
