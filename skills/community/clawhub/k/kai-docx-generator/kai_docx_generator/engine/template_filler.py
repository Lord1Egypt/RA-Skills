"""XML 级别模板占位符替换"""

import os
import re
import zipfile
from lxml import etree


# OOXML 命名空间
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkg": "http://schemas.microsoft.com/office/2006/xmlPackage",
}

# XML 目标文件列表
XML_TARGETS = [
    "word/document.xml",
]
XML_PATTERN_HEADERS = [
    "word/header",
    "word/footer",
    "word/comments",
    "word/footnotes",
    "word/endnotes",
]

# 占位符模式：{{变量名}}
PLACEHOLDER_RE = re.compile(r"\{\{([^}]+)\}\}")

# 控制字符模式（保留 \n, \r, \t）
CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# 最大字段长度
MAX_FIELD_LENGTH = 5000


class TemplateFiller:
    """
    XML 级别占位符替换。

    直接操作 .docx 内部的 XML 文件（w:t 节点），
    覆盖正文、表格、页眉、页脚、批注、脚注。
    """

    def __init__(self, template_path: str):
        self.template_path = template_path
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        self._xml_contents = {}  # xml_path -> etree._ElementTree
        self._original_xml = {}  # Store originals for reset
        self._load_template()

    def _load_template(self):
        """解压并加载模板 XML"""
        with zipfile.ZipFile(self.template_path) as z:
            # 加载主要 XML
            for target in XML_TARGETS:
                if target in z.namelist():
                    content = z.read(target)
                    tree = etree.fromstring(content)
                    self._xml_contents[target] = tree
                    self._original_xml[target] = etree.fromstring(content)

            # 加载 header/footer/comments 等
            for name in z.namelist():
                for pattern in XML_PATTERN_HEADERS:
                    if name.startswith(pattern) and name.endswith(".xml"):
                        if name not in self._xml_contents:
                            content = z.read(name)
                            tree = etree.fromstring(content)
                            self._xml_contents[name] = tree
                            self._original_xml[name] = etree.fromstring(content)

    def _reset_xml(self):
        """Reset XML to original state before fill"""
        self._xml_contents = {}
        for xml_path, tree in self._original_xml.items():
            self._xml_contents[xml_path] = etree.fromstring(etree.tostring(tree))

    def _sanitize_value(self, value: str) -> str:
        """清理替换值"""
        if not isinstance(value, str):
            value = str(value)
        # 移除控制字符
        value = CONTROL_CHAR_RE.sub("", value)
        # XML 转义: &, <, >
        value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # 截断
        if len(value) > MAX_FIELD_LENGTH:
            value = value[:MAX_FIELD_LENGTH - 1] + "…"
        return value

    def fill(self, data: dict) -> dict:
        """
        执行占位符替换。

        Args:
            data: {"变量名": "替换值"} （key 不带 {{}}）

        Returns:
            stats: {"replaced": [...], "unreplaced": [...], "extra": [...]}
        """
        # Reset to original XML before each fill
        self._reset_xml()

        # 收集模板中所有占位符
        template_placeholders = set()
        for tree in self._xml_contents.values():
            for text_node in tree.iter("{%s}t" % NS["w"]):
                if text_node.text:
                    matches = PLACEHOLDER_RE.findall(text_node.text)
                    template_placeholders.update(matches)

        replaced = []

        for xml_path, tree in self._xml_contents.items():
            for text_node in tree.iter("{%s}t" % NS["w"]):
                if text_node.text is None:
                    continue

                text = text_node.text
                modified = False

                for key, value in data.items():
                    placeholder = "{{" + key + "}}"
                    if placeholder in text:
                        clean_value = self._sanitize_value(value)
                        text = text.replace(placeholder, clean_value)
                        if key not in replaced:
                            replaced.append(key)
                        modified = True

                if modified:
                    text_node.text = text

        # 计算 unreplaced 和 extra
        unreplaced = sorted(template_placeholders - set(replaced))
        extra = sorted(set(data.keys()) - template_placeholders)

        return {
            "replaced": replaced,
            "unreplaced": unreplaced,
            "extra": extra,
            "total_placeholders": len(template_placeholders),
        }

    def save(self, output_path: str):
        """
        将修改后的 XML 重新打包为 .docx

        Args:
            output_path: 输出文件路径
        """
        # 读取原始 zip 内容
        with zipfile.ZipFile(self.template_path) as z:
            zip_info = {name: z.read(name) for name in z.namelist()}

        # 更新修改过的 XML
        for xml_path, tree in self._xml_contents.items():
            content = etree.tostring(tree, encoding="UTF-8", xml_declaration=True)
            zip_info[xml_path] = content

        # 写入新 zip
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
            for name, content in zip_info.items():
                z.writestr(name, content)
