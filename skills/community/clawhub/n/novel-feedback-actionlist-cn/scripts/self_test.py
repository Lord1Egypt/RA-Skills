#!/usr/bin/env python3
"""独立检查本 Skill 的发布结构与样例内容。"""
from pathlib import Path
import struct
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []

def need(relative, phrase=None):
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"缺少文件：{relative}")
        return ""
    text = path.read_text(encoding="utf-8")
    if phrase and phrase not in text:
        errors.append(f"{relative} 缺少：{phrase}")
    return text

skill = need("SKILL.md", "name: novel-feedback-actionlist-cn")
manifest = need("manifest.yaml", "slug: novel-feedback-actionlist-cn")
agent = need("agents/openai.yaml", "allow_implicit_invocation: true")
for file in ("README.md", "README.en.md", "fixtures/success.md", "fixtures/failure.md", "LICENSE"):
    need(file)
for phrase in ("name: novel-feedback-actionlist-cn", "icon: icon-512.png", "self_test: python3 scripts/self_test.py", "repository: https://github.com/xxjrq/novel-feedback-actionlist-cn"):
    if phrase not in manifest:
        errors.append(f"manifest.yaml 缺少：{phrase}")
for phrase in ("display_name:", "short_description:", "default_prompt:", 'icon_small: "./icon-512.png"', 'icon_large: "./icon-512.png"'):
    if phrase not in agent:
        errors.append(f"agents/openai.yaml 缺少：{phrase}")
for line in agent.splitlines():
    if "short_description:" in line:
        short = line.split(":", 1)[1].strip().strip('"')
        if not 25 <= len(short) <= 64:
            errors.append(f"short_description 长度不在 25–64：{len(short)}")
for metadata in (agent, manifest):
    for field in ("display_name", "short_description", "default_prompt", "icon_small", "icon_large"):
        found = re.search(r'^  ' + field + r': "([^"\n]+)"$', metadata, re.M)
        if not found:
            errors.append(f"interface 字符串未加引号：{field}")
            continue
        value = found.group(1)
        if field == "default_prompt" and "$novel-feedback-actionlist-cn" not in value:
            errors.append("default_prompt 未包含本 Skill 调用词")
        if field.startswith("icon_"):
            target = (ROOT / value).resolve()
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                errors.append("interface 图标必须在 Skill 根目录内且真实存在")
if skill.count("name: novel-feedback-actionlist-cn") != 1:
    errors.append("SKILL.md 的 name 不唯一或不正确")
icon = ROOT / "icon-512.png"
if icon.is_file():
    data = icon.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
        errors.append("icon-512.png 不是有效 PNG")
    else:
        width, height = struct.unpack(">II", data[16:24])
        if (width, height) != (512, 512):
            errors.append(f"图标尺寸不是 512×512：{width}×{height}")
else:
    errors.append("缺少文件：icon-512.png")
promo = ROOT / "assets/promo-1600x900.png"
if not promo.is_file():
    errors.append("缺少推广图：assets/promo-1600x900.png")
if errors:
    print("SELF-TEST FAILED")
    print("\n".join(f"- {item}" for item in errors))
    sys.exit(1)
print("SELF-TEST PASSED: 结构、样例、图标与推广图均已就绪")
