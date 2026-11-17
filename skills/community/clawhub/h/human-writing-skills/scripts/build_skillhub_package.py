"""Build a SkillHub-compatible copy of the tracked skill files."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


DISPLAY_NAME = "增强版去 AI 写作 Skill｜高级 AI 写作工具"
SUMMARY = (
    "增强版去 AI 写作 Skill：用于去AI味、AI文本润色、小说续写、人物对白审查、AI式结尾审查和长文一致性审校；"
    "内含可执行 lint、fix、verify、分阶段审稿及按需加载模块。"
)
DESCRIPTION = (
    "高级 AI 写作工具与多语言 AI humanizer。可自然化改写小说、网文、自媒体、新闻、论文和公文，"
    "检查 AI 写作痕迹、生硬结尾、无意义升华、漏字、人物口吻、对话生硬、场景空间、关系、战力与长篇上下文连续性；"
    "Python CLI 提供确定性文本扫描、保守修复、不可改内容校验、提示词编译和流水线审稿。"
)
TAGS = [
    "去AI味",
    "去AI写作",
    "消除AI腔",
    "AI写作工具",
    "AI文本润色",
    "小说润色",
    "人物对白审查",
    "ai-humanizer",
    "AI式结尾审查",
    "生硬结尾审查",
]

SKILLHUB_OVERVIEW_PATH = Path("marketplaces/skillhub-overview.zh-CN.md")
EXCLUDED_PATHS = {
    "MANIFEST.in",
    "assets/icon.webp",
    ".gitattributes",
    ".gitignore",
    "package.json",
    "pnpm-lock.yaml",
    SKILLHUB_OVERVIEW_PATH.as_posix(),
}
EXCLUDED_PREFIXES = ("plugins/", ".cursor/", "assets/")


def project_version(root: Path) -> str:
    pyproject = root.joinpath("pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
    if not match:
        raise ValueError("Could not read the project version from pyproject.toml")
    return match.group(1)


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    files = []
    for raw_path in result.stdout.decode("utf-8").split("\0"):
        if (
            not raw_path
            or raw_path in EXCLUDED_PATHS
            or raw_path.startswith(".github/")
            or raw_path.startswith(EXCLUDED_PREFIXES)
        ):
            continue
        path = root.joinpath(raw_path)
        if path.is_file():
            files.append(Path(raw_path))
    return files


def skillhub_frontmatter(version: str) -> str:
    tags = ", ".join(TAGS)
    return (
        "---\n"
        "name: human-writing-skills\n"
        "slug: human-writing-skills\n"
        f"version: {version}\n"
        f"displayName: {DISPLAY_NAME}\n"
        f"summary: {SUMMARY}\n"
        f"description: {DESCRIPTION}\n"
        f"tags: [{tags}]\n"
        "license: MIT\n"
        "homepage: https://github.com/whh110112/human-writing-skills\n"
        "---\n"
    )


def skillhub_skill(root: Path, version: str) -> str:
    overview = root.joinpath(SKILLHUB_OVERVIEW_PATH).read_text(encoding="utf-8")
    return skillhub_frontmatter(version) + "\n" + overview.lstrip()


def build_package(root: Path, output: Path, version: str | None = None) -> Path:
    root = root.resolve()
    output = output.resolve()
    if output == root:
        raise ValueError("Output directory must not replace the repository root")
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    resolved_version = version or project_version(root)
    for relative in tracked_files(root):
        source = root.joinpath(relative)
        # SkillHub rejects extensionless uploads; retain the full license under
        # an accepted Markdown name without changing the source repository.
        destination = output.joinpath("LICENSE.md" if relative.as_posix() == "LICENSE" else relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if relative.as_posix() == "SKILL.md":
            with destination.open("w", encoding="utf-8", newline="\n") as skill_file:
                skill_file.write(skillhub_skill(root, resolved_version))
        elif relative.suffix.lower() == ".md":
            text = source.read_text(encoding="utf-8")
            text = re.sub(r"(\]\((?:\.\./)*)LICENSE(\))", r"\1LICENSE.md\2", text)
            # SkillHub accepts text uploads, not bundled image files.
            text = text.replace('src="assets/',
                'src="https://raw.githubusercontent.com/whh110112/human-writing-skills/main/assets/')
            with destination.open("w", encoding="utf-8", newline="\n") as document:
                document.write(text)
        else:
            destination.write_bytes(source.read_bytes())
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version")
    args = parser.parse_args()
    package = build_package(args.root, args.output, args.version)
    print(package)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
