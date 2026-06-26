import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
FIXTURE_RECIPES = Path(__file__).resolve().parent / "fixtures" / "recipes"

sys.path.insert(0, str(SCRIPTS_DIR))


def _run(cmd, env=None):
    return subprocess.run(cmd, cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=True)


@pytest.fixture
def data_root(tmp_path):
    root = tmp_path / "kc-data"
    _run([sys.executable, str(SCRIPTS_DIR / "setup_household.py"), "--data-root", str(root)])
    for recipe in sorted(FIXTURE_RECIPES.glob("*.md")):
        shutil.copy(recipe, root / "recipes" / recipe.name)
    return root


@pytest.fixture
def data_root_indexed(data_root):
    _run([sys.executable, str(SCRIPTS_DIR / "build_recipe_query_index.py"), "--data-root", str(data_root)])
    return data_root


@pytest.fixture
def run_cmd():
    def _invoke(script, *args, env=None, check=True):
        cmd = [sys.executable, str(SCRIPTS_DIR / script), *args]
        return subprocess.run(cmd, cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=check)
    return _invoke
