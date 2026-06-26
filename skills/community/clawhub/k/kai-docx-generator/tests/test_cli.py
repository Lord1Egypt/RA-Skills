import os
import tempfile
import json
import subprocess
import sys
import zipfile

SCRIPTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "kai_docx_generator", "scripts"
)


class TestGenerateCLI:

    def test_generate_from_markdown(self):
        md = "# 测试标题\n\n正文段落。"
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
            f.write(md)
            md_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "generate.py"), md_path, output_path],
                capture_output=True, text=True
            )
            assert result.returncode == 0
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            os.unlink(md_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_generate_missing_input_file(self):
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "generate.py"), "/nonexistent/file.md", output_path],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert "错误" in result.stderr
        os.unlink(output_path)


class TestFillTemplateCLI:

    TEMPLATE_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "templates", "contract.docx"
    )

    def test_fill_from_json(self):
        data = {
            "合同标题": "测试合同",
            "甲方": "公司A",
            "乙方": "公司B",
            "金额": "50万",
            "日期": "2025-01-01",
        }
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            data_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "fill_template.py"), self.TEMPLATE_PATH,
                 "--data", data_path, "--output", output_path],
                capture_output=True, text=True
            )
            assert result.returncode == 0
            assert os.path.exists(output_path)
        finally:
            os.unlink(data_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_fill_missing_template(self):
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "fill_template.py"), "/nonexistent.docx",
             "--data", "/tmp/test.json", "--output", "/tmp/out.docx"],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert "错误" in result.stderr

    def test_fill_strict_mode(self):
        """--strict 模式下存在未替换占位符应退出 1"""
        data = {"甲方": "公司A"}
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            data_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "fill_template.py"),
                 self.TEMPLATE_PATH, "--data", data_path, "--output", output_path, "--strict"],
                capture_output=True, text=True
            )
            assert result.returncode == 1
        finally:
            os.unlink(data_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_fill_invalid_json(self):
        """畸形 JSON 应退出 1"""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f:
            f.write("{invalid json!!!")
            data_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "fill_template.py"),
                 self.TEMPLATE_PATH, "--data", data_path,
                 "--output", "/tmp/out_invalid.docx"],
                capture_output=True, text=True
            )
            assert result.returncode == 1
            assert "错误" in result.stderr
        finally:
            os.unlink(data_path)

    def test_fill_yaml_data(self):
        """YAML 数据文件应正常工作"""
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False, encoding="utf-8") as f:
            f.write("合同标题: YAML测试合同\n甲方: 公司A\n乙方: 公司B\n金额: 10万\n日期: 2025-01-01\n")
            data_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "fill_template.py"),
                 self.TEMPLATE_PATH, "--data", data_path, "--output", output_path],
                capture_output=True, text=True
            )
            assert result.returncode == 0
            assert os.path.exists(output_path)
        finally:
            os.unlink(data_path)
            os.unlink(output_path)

    def test_fill_yaml_frontmatter_data(self):
        """YAML Front Matter 格式的数据文件应正常工作"""
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
            f.write("---\n合同标题: FM测试合同\n甲方: 公司A\n乙方: 公司B\n金额: 20万\n日期: 2025-06-01\n---\n")
            data_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "fill_template.py"),
                 self.TEMPLATE_PATH, "--data", data_path, "--output", output_path],
                capture_output=True, text=True
            )
            assert result.returncode == 0
            assert os.path.exists(output_path)
        finally:
            os.unlink(data_path)
            os.unlink(output_path)

    def test_fill_missing_data_file(self):
        """数据文件不存在应退出 1"""
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "fill_template.py"),
             self.TEMPLATE_PATH, "--data", "/nonexistent.json",
             "--output", "/tmp/out.docx"],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert "错误" in result.stderr


class TestValidateCLI:

    def test_validate_valid_docx(self):
        template = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "templates", "contract.docx"
        )
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "validate.py"), template],
            capture_output=True, text=True
        )
        assert result.returncode == 0

    def test_validate_missing_file(self):
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "validate.py"), "/nonexistent.docx"],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert "错误" in result.stderr or "invalid" in result.stderr.lower()

    def test_validate_corrupt_zip(self):
        """损坏的 ZIP 文件应被检测"""
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False, mode="wb") as f:
            f.write(b"this is not a zip file at all")
            corrupt_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "validate.py"), corrupt_path],
                capture_output=True, text=True
            )
            assert result.returncode == 1
        finally:
            os.unlink(corrupt_path)

    def test_validate_empty_docx(self):
        """空 ZIP 文件（缺少必需结构）应被标记"""
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False, mode="wb") as f:
            # 创建一个合法但空的 ZIP
            with zipfile.ZipFile(f.name, "w") as z:
                pass

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "validate.py"), f.name],
                capture_output=True, text=True
            )
            assert result.returncode == 1
        finally:
            os.unlink(f.name)

    def test_generate_unknown_style(self):
        """未知的 --style 应退出 1"""
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
            f.write("# test")
            md_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "generate.py"),
                 "--style", "nonexistent", md_path, output_path],
                capture_output=True, text=True
            )
            assert result.returncode == 1
            assert "错误" in result.stderr
        finally:
            os.unlink(md_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_generate_empty_markdown(self):
        """空 Markdown 应生成空 docx，不崩溃"""
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
            f.write("")
            md_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "generate.py"), md_path, output_path],
                capture_output=True, text=True
            )
            assert result.returncode == 0
            assert os.path.exists(output_path)
        finally:
            os.unlink(md_path)
            os.unlink(output_path)

    def test_generate_output_dir_creation(self):
        """输出目录不存在时应自动创建"""
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False, encoding="utf-8") as f:
            f.write("# test")
            md_path = f.name

        output_dir = tempfile.mkdtemp()
        output_path = os.path.join(output_dir, "subdir", "nested", "output.docx")

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(SCRIPTS_DIR, "generate.py"), md_path, output_path],
                capture_output=True, text=True
            )
            assert result.returncode == 0
            assert os.path.exists(output_path)
        finally:
            os.unlink(md_path)
            import shutil
            shutil.rmtree(output_dir)
