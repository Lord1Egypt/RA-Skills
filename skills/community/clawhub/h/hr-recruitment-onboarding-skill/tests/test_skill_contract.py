"""Contract tests for the conversational Skill and its distribution archive."""

from pathlib import Path
from zipfile import ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _skill_text() -> str:
    return (PROJECT_ROOT / "SKILL.md").read_text(encoding="utf-8")


def test_skill_has_discoverable_minimal_frontmatter():
    text = _skill_text()
    _, frontmatter, _ = text.split("---", 2)
    metadata = {
        key.strip(): value.strip()
        for key, value in (
            line.split(":", 1)
            for line in frontmatter.strip().splitlines()
            if ":" in line
        )
    }

    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "hr-recruitment-jd-generator"
    assert metadata["description"].startswith("Use when")
    description = metadata["description"].lower()
    assert all(
        trigger in description for trigger in ("configure", "jd generator", "model")
    )


def test_skill_defines_the_complete_conversational_workflow():
    text = _skill_text()

    assert "自然语言" in text
    assert all(
        field in text
        for field in (
            "mode",
            "job_id",
            "job_title",
            "department",
            "location",
            "description",
        )
    )
    assert "python main.py" in text
    assert "generated_files" in text and "warnings" in text
    assert "工作区相对路径" in text
    assert "本地规则" in text and "可选" in text
    assert "HR" in text and "岗位相关" in text


def test_skill_and_readme_use_chinese_facing_documentation():
    skill_text = _skill_text()
    readme_text = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert "# OPIE Engine 职位 JD 生成 Skill" in skill_text
    assert "## 核心工作流程" in skill_text
    assert "# OPIE Engine 职位 JD 生成 Skill" in readme_text
    assert "## 安装与运行环境" in readme_text


def test_skill_guides_secure_model_setup():
    text = _skill_text()

    assert all(key in text for key in ("LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY"))
    assert "OPIE Engine" in text and "安全环境变量" in text
    assert "不得" in text and "普通聊天" in text and "API Key" in text
    assert "持久化" in text and "文件" in text


def test_readme_documents_installation_invocation_and_fallback():
    text = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert "Python 3.11" in text
    assert "pip install -r requirements.txt" in text
    assert all(key in text for key in ("LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY"))
    assert "--request" in text and "stdin" in text
    assert "本地规则" in text
    assert "ClawHub" in text
    assert "hr_recruitment_onboarding_skill" in text
    assert "无需生成 ZIP" in text


def test_package_excludes_runtime_secret_and_distribution_files(tmp_path):
    from hr_recruitment_onboarding_skill.package_skill import package_skill

    source_root = tmp_path / "source"
    source_root.mkdir()
    retained_files = ("keep.txt", "environment.py", "dotenv_loader.py")
    for relative in retained_files:
        (source_root / relative).write_text("keep", encoding="utf-8")
    excluded_files = (
        ".env",
        ".env.local",
        ".env.production",
        ".env.production.local",
        "secret.env",
        ".git/config",
        "workspace/result.json",
        "__pycache__/module.pyc",
        ".pytest_cache/state",
        "dist/old.zip",
    )
    for relative in excluded_files:
        path = source_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("exclude", encoding="utf-8")

    archive = package_skill(source_root, tmp_path / "output")

    with ZipFile(archive) as bundle:
        names = bundle.namelist()
    assert names == sorted(retained_files)


def test_project_archive_contains_installable_skill(tmp_path):
    from hr_recruitment_onboarding_skill.package_skill import package_skill

    archive = package_skill(PROJECT_ROOT, tmp_path)

    assert archive.name == "hr-recruitment-jd-skill.zip"
    with ZipFile(archive) as bundle:
        names = set(bundle.namelist())
    assert {"SKILL.md", "README.md", "main.py"}.issubset(names)
    assert all(
        any(name.startswith(f"{directory}/") for name in names)
        for directory in ("app", "services", "prompts", "samples")
    )
    assert not any(
        part in {".git", "workspace", "__pycache__", ".pytest_cache", "dist"}
        for name in names
        for part in Path(name).parts
    )
    assert not any(
        Path(name).name == ".env"
        or Path(name).name.startswith(".env.")
        or Path(name).suffix == ".env"
        for name in names
    )
