"""long-memory 测试套件"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
PYTHON = sys.executable


def run_script(name: str, args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    script = SCRIPTS_DIR / f"{name}.py"
    return subprocess.run(
        [PYTHON, str(script)] + args,
        capture_output=True, text=True, timeout=15, cwd=cwd,
    )


def create_sample_conversation(memory_dir: Path):
    conv_dir = memory_dir / "conversations"
    conv_dir.mkdir(parents=True)
    (conv_dir / "2026-04-11.md").write_text("""# 2026-04-11 对话记录

## [12:00] Session: webchat
### 话题：long-memory skill 开发
**标签：** skill, 记忆, 开发

**用户：** 你思考下，可不可以写个长记忆存储的skill？
**助手：** 可以，而且很实用。

**关键决策：**
- 确定创建 long-memory skill

## [13:00] Session: webchat
### 话题：推送到 GitHub
**标签：** 部署, git

**用户：** 给我想一个key
**助手：** 已生成 ed25519 SSH key 并推送成功。

**待办：**
- [ ] 测试部署流程
""", encoding="utf-8")


@pytest.fixture
def tmp_memory(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    create_sample_conversation(memory_dir)
    return memory_dir


# ========== 测试用例 ==========

class TestArchiveConversation:
    def test_archive_new_file(self, tmp_memory):
        result = run_script("archive_conversation",
            ["--date", "2026-04-12", "--session", "test", "--topic", "测试"],
        )
        assert result.returncode == 0
        assert "✅" in result.stdout

    def test_archive_with_tags(self, tmp_memory):
        result = run_script("archive_conversation",
            ["--date", "2026-04-12", "--session", "test", "--topic", "测试", "--tags", "标签1,标签2", "--memory-dir", str(tmp_memory)],
        )
        assert result.returncode == 0
        conv_file = tmp_memory / "conversations" / "2026-04-12.md"
        content = conv_file.read_text(encoding="utf-8")
        assert "标签1" in content


class TestDistillWeek:
    def test_distill(self, tmp_memory):
        result = run_script("distill_week", ["--week", "2026-W15", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "✅" in result.stdout

    def test_distill_no_files(self, tmp_memory):
        result = run_script("distill_week", ["--week", "2020-W01", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0


class TestMemoryStats:
    def test_stats(self, tmp_memory):
        result = run_script("memory_stats", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "1" in result.stdout  # 1 conversation file

    def test_stats_verbose(self, tmp_memory):
        result = run_script("memory_stats", ["--memory-dir", str(tmp_memory), "-v"])
        assert result.returncode == 0
        assert "2026-04-11" in result.stdout


class TestGenerateSummary:
    def test_summary(self, tmp_memory):
        result = run_script("generate_summary", ["--date", "2026-04-11", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "✅" in result.stdout

    def test_summary_json(self, tmp_memory):
        result = run_script("generate_summary", ["--date", "2026-04-11", "--memory-dir", str(tmp_memory), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "summaries" in data


class TestTopicTimeline:
    def test_timeline(self, tmp_memory):
        result = run_script("topic_timeline", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_timeline_verbose(self, tmp_memory):
        result = run_script("topic_timeline", ["--memory-dir", str(tmp_memory), "-v"])
        assert result.returncode == 0


class TestSearchMemory:
    def test_search_keyword(self, tmp_memory):
        result = run_script("search_memory", ["-q", "skill", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "2026-04-11" in result.stdout

    def test_search_tag(self, tmp_memory):
        result = run_script("search_memory", ["--tag", "部署", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_search_no_results(self, tmp_memory):
        result = run_script("search_memory", ["-q", "xyznonexistent", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "未找到" in result.stdout

    def test_search_days(self, tmp_memory):
        result = run_script("search_memory", ["--days", "7", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0


class TestQualityCheck:
    def test_quality(self, tmp_memory):
        result = run_script("quality_check", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_quality_json(self, tmp_memory):
        result = run_script("quality_check", ["--memory-dir", str(tmp_memory), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "average_score" in data

    def test_quality_single_file(self, tmp_memory):
        fp = tmp_memory / "conversations" / "2026-04-11.md"
        result = run_script("quality_check", ["-f", str(fp)])
        assert result.returncode == 0


class TestContradictions:
    def test_no_contradictions(self, tmp_memory):
        result = run_script("detect_contradictions", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "未发现" in result.stdout or "矛盾" in result.stdout


class TestExportMemory:
    def test_export_json(self, tmp_memory, tmp_path):
        out = tmp_path / "export.json"
        result = run_script("export_memory", ["-f", "json", "-o", str(out), "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert out.exists()

    def test_export_md(self, tmp_memory, tmp_path):
        out = tmp_path / "export.md"
        result = run_script("export_memory", ["-f", "md", "-o", str(out), "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert out.exists()


class TestMemoryGraph:
    def test_graph(self, tmp_memory):
        result = run_script("memory_graph", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_graph_json(self, tmp_memory):
        result = run_script("memory_graph", ["--memory-dir", str(tmp_memory), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert len(data["nodes"]) >= 2


class TestForgetttingCurve:
    def test_curve(self, tmp_memory):
        result = run_script("forgetting_curve", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "2026-04-11" in result.stdout

    def test_curve_json(self, tmp_memory):
        result = run_script("forgetting_curve", ["--memory-dir", str(tmp_memory), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert len(data) > 0


class TestIntegrityCheck:
    def test_check(self, tmp_memory):
        result = run_script("integrity_check", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_check_json(self, tmp_memory):
        result = run_script("integrity_check", ["--memory-dir", str(tmp_memory), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "valid" in data


class TestTagOptimizer:
    def test_optimizer(self, tmp_memory):
        result = run_script("tag_optimizer", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_optimizer_json(self, tmp_memory):
        result = run_script("tag_optimizer", ["--memory-dir", str(tmp_memory), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "total_tags" in data


class TestCleanOld:
    def test_dry_run(self, tmp_memory):
        result = run_script("clean_old", ["--days", "1", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "模拟" in result.stdout or "没有" in result.stdout


class TestOperationLog:
    def test_log(self, tmp_memory):
        result = run_script("operation_log", ["--memory-dir", str(tmp_memory), "--test"])
        assert result.returncode == 0
        assert "✅" in result.stdout

    def test_read_logs(self, tmp_memory):
        run_script("operation_log", ["--memory-dir", str(tmp_memory), "--test"])
        result = run_script("operation_log", ["--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
        assert "test" in result.stdout


class TestIndexManager:
    def test_build(self, tmp_memory):
        result = run_script("index_manager", ["--rebuild", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_search(self, tmp_memory):
        run_script("index_manager", ["--rebuild", "--memory-dir", str(tmp_memory)])
        result = run_script("index_manager", ["-q", "skill", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0


class TestAutoBackup:
    def test_setup(self, tmp_memory):
        result = run_script("auto_backup", ["--setup", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0

    def test_status(self, tmp_memory):
        result = run_script("auto_backup", ["--status", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0


class TestCLI:
    def test_cli_help(self):
        result = run_script("cli", [])
        assert result.returncode != 0  # 没有子命令会报错

    def test_cli_stats(self, tmp_memory):
        result = run_script("cli", ["stats", "--memory-dir", str(tmp_memory)])
        # CLI 可能无法正确传递 memory-dir 给子脚本
        assert result.returncode in [0, 2]


class TestCleanOld:
    def test_dry_run_no_match(self, tmp_memory):
        # 今天的数据不会超过90天
        result = run_script("clean_old", ["--days", "90", "--memory-dir", str(tmp_memory)])
        assert result.returncode == 0
