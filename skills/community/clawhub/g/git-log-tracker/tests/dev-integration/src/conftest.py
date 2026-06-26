"""dev-integration 阶段特化 fixture。

本阶段使用真实临时 git 仓库 + 真实 SQLite 文件，验证 Controller → 逻辑 → 持久化
的完整链路。git 是本地子进程、SQLite 是本地文件，均属 §4 允许的进程内/本地范围。

关键：cli.py 通过 `from db import ... DEFAULT_DB_PATH` 把常量复制进自身命名空间，
因此隔离时必须同时 patch cli 与 db（及 hook/config）各自命名空间的路径常量。
"""

import subprocess

import pytest


@pytest.fixture
def isolated_home(tmp_path, monkeypatch):
    """把所有指向 ~/.commit-logs、~/.git-templates 的全局常量重定向到 tmp_path。

    覆盖 db / cli / hook / config 四个模块各自命名空间内的别名常量，
    返回常用路径字典。
    """
    import cli
    import config
    import db
    import hook

    data_dir = tmp_path / ".commit-logs"
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "index.db"
    cfg_path = data_dir / "config.toml"
    labels_path = data_dir / "labels.json"
    template_dir = tmp_path / ".git-templates"

    # db 模块（get_connection 默认参数在调用时查 db.DEFAULT_DB_PATH）
    monkeypatch.setattr(db, "DEFAULT_DB_DIR", data_dir)
    monkeypatch.setattr(db, "DEFAULT_DB_PATH", db_path)
    # cli 模块的别名副本
    monkeypatch.setattr(cli, "DEFAULT_DB_DIR", data_dir)
    monkeypatch.setattr(cli, "DEFAULT_DB_PATH", db_path)
    monkeypatch.setattr(cli, "DEFAULT_CONFIG_DIR", data_dir)
    monkeypatch.setattr(cli, "DEFAULT_CONFIG_PATH", cfg_path)
    monkeypatch.setattr(cli, "TEMPLATE_DIR", template_dir)
    # config 模块
    monkeypatch.setattr(config, "DEFAULT_CONFIG_DIR", data_dir)
    monkeypatch.setattr(config, "DEFAULT_CONFIG_PATH", cfg_path)
    monkeypatch.setattr(config, "DEFAULT_LABELS_PATH", labels_path)
    # hook 模块（record_commit 用 hook.DEFAULT_DB_DIR 推导 db 路径）
    monkeypatch.setattr(hook, "DEFAULT_DB_DIR", data_dir)

    return {
        "data_dir": data_dir,
        "db_path": db_path,
        "config_path": cfg_path,
        "labels_path": labels_path,
        "template_dir": template_dir,
    }


@pytest.fixture
def temp_db(isolated_home):
    """返回隔离后的 db 路径，并触发建库（Alembic upgrade + 建表）。"""
    import db

    conn = db.get_connection(isolated_home["db_path"])
    conn.close()
    return isolated_home["db_path"]


@pytest.fixture
def git_repo(tmp_path):
    """在临时目录创建一个带一次提交的真实 git 仓库，返回仓库根 Path。"""
    repo = tmp_path / "repo"
    repo.mkdir()

    def run(*args):
        subprocess.run(
            ["git", *args], cwd=repo, check=True,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )

    run("init")
    run("config", "user.name", "Tester")
    run("config", "user.email", "tester@example.com")
    run("config", "commit.gpgsign", "false")
    (repo / "README.md").write_text("hello\n", encoding="utf-8")
    run("add", ".")
    run("commit", "-m", "feat: 初始提交\n\n正文说明")
    return repo
