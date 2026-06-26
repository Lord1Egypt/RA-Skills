"""kai-docx-generator: 沙箱环境 Word 文档生成器"""

from kai_docx_generator.engine.docx_engine import DocxEngine
from kai_docx_generator.engine.template_filler import TemplateFiller
from kai_docx_generator.parser.md_to_ast import parse_markdown_to_docspec
from kai_docx_generator.styles.standard import STANDARD_CONFIG


def generate(markdown: str, output_path: str, style: str = "standard") -> str:
    """
    新建模式：Markdown → .docx

    Args:
        markdown: Markdown 文本
        output_path: 输出 .docx 路径
        style: Style 预设名称

    Returns:
        输出文件路径
    """
    spec = parse_markdown_to_docspec(markdown)
    engine = DocxEngine(style_config=STANDARD_CONFIG)
    doc = engine.generate_from_spec(spec)
    doc.save(output_path)
    return output_path


def fill_template(template_path: str, data: dict, output_path: str) -> tuple[str, dict]:
    """
    模板填充模式

    Args:
        template_path: 模板 .docx 路径
        data: 数据字典 {"变量名": "值"}
        output_path: 输出 .docx 路径

    Returns:
        (输出文件路径, stats 字典)
    """
    filler = TemplateFiller(template_path)
    stats = filler.fill(data)
    filler.save(output_path)
    return output_path, stats


__all__ = ["generate", "fill_template", "DocxEngine", "TemplateFiller", "parse_markdown_to_docspec"]
