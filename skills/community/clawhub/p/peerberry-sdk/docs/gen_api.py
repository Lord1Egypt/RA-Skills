from pathlib import Path

try:
    import mkdocs_gen_files
except ModuleNotFoundError:
    mkdocs_gen_files = None


PACKAGE_NAME = "peerberry_sdk"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src" / PACKAGE_NAME
OUTPUT_PATH = "api/reference.md"


def iter_modules() -> list[str]:
    modules = []

    for path in sorted(SOURCE_ROOT.rglob("*.py")):
        if path.name == "__main__.py":
            continue

        rel = path.relative_to(PROJECT_ROOT / "src").with_suffix("")
        module = ".".join(rel.parts)

        if module.endswith(".__init__"):
            module = module[: -len(".__init__")]

        modules.append(module)

    return modules


def write_reference_page(modules: list[str]) -> None:
    with _open_output(OUTPUT_PATH) as fd:
        fd.write("# API Reference\n\n")
        fd.write("This page is generated automatically from source modules.\n\n")
        fd.write("For practical method usage and parameter guidance, use ")
        fd.write("[API Client Reference (Generated)](client.md).\n\n")

        for module in modules:
            fd.write(f"## `{module}`\n\n")
            fd.write(f"::: {module}\n")
            fd.write("    options:\n")
            fd.write("      show_root_heading: false\n\n")


def _open_output(path: str):
    if mkdocs_gen_files is not None:
        return mkdocs_gen_files.open(path, "w")

    target_path = PROJECT_ROOT / "docs" / path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    return target_path.open("w", encoding="utf-8")


write_reference_page(iter_modules())
