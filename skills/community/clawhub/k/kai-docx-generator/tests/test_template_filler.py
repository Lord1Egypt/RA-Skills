import os
import tempfile
import zipfile
from lxml import etree
from kai_docx_generator.engine.template_filler import TemplateFiller


class TestTemplateFiller:

    TEMPLATE_PATH = "templates/contract.docx"

    def _read_xml_from_docx(self, docx_path: str, xml_path: str) -> str:
        """从 .docx 中读取 XML 内容"""
        with zipfile.ZipFile(docx_path) as z:
            return z.read(xml_path).decode("utf-8")

    def test_simple_text_replacement(self):
        """测试简单文本替换"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        result = filler.fill({
            "合同标题": "技术服务合同",
            "甲方": "XX科技公司",
            "乙方": "YY咨询公司",
            "金额": "50万元",
            "日期": "2025-10-15",
        })

        assert result["replaced"] == ["合同标题", "甲方", "乙方", "金额", "日期"]
        assert result["unreplaced"] == []

    def test_unreplaced_placeholders_reported(self):
        """未替换的占位符应被记录到 unreplaced"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        result = filler.fill({
            "甲方": "XX公司",
        })

        assert "甲方" in result["replaced"]
        assert len(result["unreplaced"]) > 0
        assert "合同标题" in result["unreplaced"]

    def test_extra_keys_reported(self):
        """数据中存在但模板中不存在的 key 应记录到 extra"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        result = filler.fill({
            "合同标题": "测试合同",
            "甲方": "XX",
            "乙方": "YY",
            "金额": "50万",
            "日期": "2025-10-15",
            "不存在的字段": "测试",
        })

        assert "不存在的字段" in result["extra"]

    def test_output_is_valid_docx(self):
        """输出应是合法的 .docx 文件"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        filler.save(output_path)
        assert zipfile.is_zipfile(output_path)
        # Verify .docx structure
        with zipfile.ZipFile(output_path) as z:
            names = z.namelist()
            assert "[Content_Types].xml" in names
            assert "word/document.xml" in names
        os.unlink(output_path)

    def test_replacement_in_document_xml(self):
        """替换应反映在 document.xml 中"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        filler.fill({
            "合同标题": "技术服务合同",
            "甲方": "XX公司",
            "乙方": "YY公司",
            "金额": "50万元",
            "日期": "2025-10-15",
        })

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name

        filler.save(output_path)

        xml = self._read_xml_from_docx(output_path, "word/document.xml")
        assert "{{合同标题}}" not in xml
        assert "技术服务合同" in xml
        assert "{{甲方}}" not in xml
        assert "XX公司" in xml

        os.unlink(output_path)

    def test_sanitize_control_characters(self):
        """替换值中的控制字符应被移除"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        filler.fill({
            "合同标题": "测试\x00\x01\x02合同",
            "甲方": "XX",
            "乙方": "YY",
            "金额": "50万",
            "日期": "2025",
        })

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name
        filler.save(output_path)

        xml = self._read_xml_from_docx(output_path, "word/document.xml")
        # Control chars should be removed
        assert "\x00" not in xml
        assert "\x01" not in xml
        assert "\x02" not in xml
        # The text itself should appear
        assert "测试" in xml
        assert "合同" in xml

        os.unlink(output_path)

    def test_long_value_truncation(self):
        """超长文本应被截断（5000 字符）"""
        long_text = "A" * 6000
        filler = TemplateFiller(self.TEMPLATE_PATH)
        result = filler.fill({
            "合同标题": long_text,
            "甲方": "XX",
            "乙方": "YY",
            "金额": "50万",
            "日期": "2025",
        })

        # Verify sanitization directly
        sanitized = filler._sanitize_value(long_text)
        assert len(sanitized) == 5000
        assert sanitized.endswith("…")
        assert "合同标题" in result["replaced"]

    def test_template_not_found(self):
        try:
            filler = TemplateFiller("nonexistent.docx")
            filler.fill({"key": "value"})
            assert False, "Should have raised"
        except FileNotFoundError:
            pass

    def test_sanitize_value_removes_control_chars(self):
        filler = TemplateFiller(self.TEMPLATE_PATH)
        assert filler._sanitize_value("hello\x00world\x01") == "helloworld"

    def test_sanitize_value_truncates_long_text(self):
        filler = TemplateFiller(self.TEMPLATE_PATH)
        result = filler._sanitize_value("A" * 6000)
        assert len(result) == 5000
        assert result[-1] == "…"

    def test_sanitize_value_non_string(self):
        filler = TemplateFiller(self.TEMPLATE_PATH)
        assert filler._sanitize_value(42) == "42"
        assert filler._sanitize_value(None) == "None"

    def test_sanitize_value_empty_string(self):
        filler = TemplateFiller(self.TEMPLATE_PATH)
        assert filler._sanitize_value("") == ""

    def test_multiple_occurrences_of_same_placeholder(self):
        """同一占位符在文本中出现多次，应全部替换"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        result = filler.fill({
            "合同标题": "技术服务合同",
            "甲方": "XX科技公司",
            "乙方": "YY咨询公司",
            "金额": "50万元",
            "日期": "2025-10-15",
        })

        assert result["unreplaced"] == []

    def test_xml_special_chars_escaped(self):
        """XML 特殊字符应被正确转义"""
        filler = TemplateFiller(self.TEMPLATE_PATH)
        filler.fill({
            "合同标题": "测试<b>标签</b> & 符号",
            "甲方": "XX",
            "乙方": "YY",
            "金额": "50万",
            "日期": "2025",
        })

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            output_path = f.name
        filler.save(output_path)

        xml = self._read_xml_from_docx(output_path, "word/document.xml")
        assert "<b>" not in xml
        assert "&amp;" in xml

        os.unlink(output_path)

    def test_multiple_fill_calls_independent(self):
        """多次 fill() 调用应相互独立"""
        filler = TemplateFiller(self.TEMPLATE_PATH)

        result1 = filler.fill({
            "合同标题": "合同A",
            "甲方": "公司A",
            "乙方": "公司B",
            "金额": "10万",
            "日期": "2025-01-01",
        })
        assert result1["unreplaced"] == []

        result2 = filler.fill({
            "合同标题": "合同B",
            "甲方": "公司C",
            "乙方": "公司D",
            "金额": "20万",
            "日期": "2025-02-01",
        })
        assert result2["unreplaced"] == []
        assert "甲方" not in result2["extra"]
