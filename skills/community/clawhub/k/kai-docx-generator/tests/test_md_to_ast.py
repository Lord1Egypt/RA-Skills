from kai_docx_generator.parser.md_to_ast import parse_markdown_to_docspec


def test_heading_parsing():
    md = "# 一级标题\n\n## 二级标题\n\n### 三级标题"
    docspec = parse_markdown_to_docspec(md)

    headings = [b for b in docspec["blocks"] if b["type"] == "heading"]
    assert len(headings) == 3
    assert headings[0]["level"] == 1
    assert headings[0]["text"] == "一级标题"
    assert headings[1]["level"] == 2
    assert headings[1]["text"] == "二级标题"
    assert headings[2]["level"] == 3
    assert headings[2]["text"] == "三级标题"


def test_paragraph_parsing():
    md = "这是第一段。\n\n这是第二段。"
    docspec = parse_markdown_to_docspec(md)

    paragraphs = [b for b in docspec["blocks"] if b["type"] == "paragraph"]
    assert len(paragraphs) == 2
    assert paragraphs[0]["text"] == "这是第一段。"
    assert paragraphs[1]["text"] == "这是第二段。"


def test_bullet_list_parsing():
    md = "- 项目一\n- 项目二\n- 项目三"
    docspec = parse_markdown_to_docspec(md)

    lists = [b for b in docspec["blocks"] if b["type"] == "bullet_list"]
    assert len(lists) == 1
    assert lists[0]["items"] == ["项目一", "项目二", "项目三"]


def test_numbered_list_parsing():
    md = "1. 第一步\n2. 第二步"
    docspec = parse_markdown_to_docspec(md)

    lists = [b for b in docspec["blocks"] if b["type"] == "numbered_list"]
    assert len(lists) == 1
    assert lists[0]["items"] == ["第一步", "第二步"]


def test_table_parsing():
    md = "| 列1 | 列2 |\n| --- | --- |\n| A | B |"
    docspec = parse_markdown_to_docspec(md)

    tables = [b for b in docspec["blocks"] if b["type"] == "table"]
    assert len(tables) == 1
    assert tables[0]["headers"] == ["列1", "列2"]
    assert tables[0]["rows"] == [["A", "B"]]


def test_blockquote_callout():
    md = "> 这是一条提示信息"
    docspec = parse_markdown_to_docspec(md)

    callouts = [b for b in docspec["blocks"] if b["type"] == "callout"]
    assert len(callouts) == 1
    assert callouts[0]["text"] == "这是一条提示信息"
    assert callouts[0]["style"] == "info"


def test_pagebreak_comment():
    md = "第一段\n\n<!-- pagebreak -->\n\n第二段"
    docspec = parse_markdown_to_docspec(md)

    pagebreaks = [b for b in docspec["blocks"] if b["type"] == "page_break"]
    assert len(pagebreaks) == 1


def test_hr_is_not_pagebreak():
    """--- 是分割线，不应被解析为分页"""
    md = "第一段\n\n---\n\n第二段"
    docspec = parse_markdown_to_docspec(md)

    pagebreaks = [b for b in docspec["blocks"] if b["type"] == "page_break"]
    assert len(pagebreaks) == 0
    hrs = [b for b in docspec["blocks"] if b["type"] == "hr"]
    assert len(hrs) == 1


def test_image_parsing():
    md = "![图表1](./chart.png)"
    docspec = parse_markdown_to_docspec(md)

    images = [b for b in docspec["blocks"] if b["type"] == "image"]
    assert len(images) == 1
    assert images[0]["path"] == "./chart.png"
    assert images[0]["caption"] == "图表1"


def test_bold_italic_runs():
    md = "**加粗文本** 和 *斜体文本*"
    docspec = parse_markdown_to_docspec(md)

    paragraphs = [b for b in docspec["blocks"] if b["type"] == "paragraph"]
    assert len(paragraphs) == 1
    assert "runs" in paragraphs[0]
    bold_runs = [r for r in paragraphs[0]["runs"] if r.get("bold")]
    italic_runs = [r for r in paragraphs[0]["runs"] if r.get("italic")]
    assert len(bold_runs) >= 1
    assert len(italic_runs) >= 1


def test_empty_input():
    docspec = parse_markdown_to_docspec("")
    assert docspec["blocks"] == []


def test_sections_with_headings():
    md = "# 标题一\n\n段落一\n\n## 子标题\n\n段落二"
    docspec = parse_markdown_to_docspec(md)
    assert "sections" in docspec
    assert len(docspec["sections"]) == 1
    assert docspec["sections"][0]["heading"]["level"] == 1
    assert docspec["sections"][0]["heading"]["text"] == "标题一"
    assert len(docspec["sections"][0]["blocks"]) == 1
    assert docspec["sections"][0]["blocks"][0]["text"] == "段落一"
    # 子标题作为 children
    assert len(docspec["sections"][0]["children"]) == 1
    assert docspec["sections"][0]["children"][0]["heading"]["level"] == 2
    assert docspec["sections"][0]["children"][0]["heading"]["text"] == "子标题"


def test_code_block_with_language():
    md = "```python\nprint('hello')\n```"
    docspec = parse_markdown_to_docspec(md)

    code_blocks = [b for b in docspec["blocks"] if b["type"] == "code_block"]
    assert len(code_blocks) == 1
    assert code_blocks[0]["language"] == "python"
    assert code_blocks[0]["code"] == "print('hello')"


def test_code_block_without_language():
    md = "```\nsome code\n```"
    docspec = parse_markdown_to_docspec(md)

    code_blocks = [b for b in docspec["blocks"] if b["type"] == "code_block"]
    assert len(code_blocks) == 1
    assert code_blocks[0]["language"] == ""
    assert code_blocks[0]["code"] == "some code"


def test_yaml_front_matter_parsing():
    md = """---
title: 测试报告
author: 测试团队
---

# 正文
"""
    docspec = parse_markdown_to_docspec(md)
    assert docspec["metadata"]["title"] == "测试报告"
    assert docspec["metadata"]["author"] == "测试团队"
    # 正文仍应被解析
    headings = [b for b in docspec["blocks"] if b["type"] == "heading"]
    assert len(headings) == 1
    assert headings[0]["text"] == "正文"


def test_yaml_front_matter_malformed_ignored():
    """畸形 YAML 不应导致崩溃，正文仍应被解析"""
    md = """---
invalid yaml content with [bracket
---

# 正文
"""
    docspec = parse_markdown_to_docspec(md)
    # 不崩溃，正文标题应被解析
    headings = [b for b in docspec["blocks"] if b["type"] == "heading" and b["text"] == "正文"]
    assert len(headings) == 1


def test_max_markdown_size_truncation():
    """超过 200KB 的输入应被截断，不会崩溃"""
    from kai_docx_generator.parser.md_to_ast import MAX_MARKDOWN_SIZE
    # 生成超过 200KB 的内容
    large_md = "# 标题\n\n" + "A" * (MAX_MARKDOWN_SIZE + 10000)
    docspec = parse_markdown_to_docspec(large_md)
    # 不崩溃，至少有一个标题
    headings = [b for b in docspec["blocks"] if b["type"] == "heading"]
    assert len(headings) >= 1


def test_max_images_limit():
    """超过 20 张图片应只保留前 20 张"""
    from kai_docx_generator.parser.md_to_ast import MAX_IMAGES
    lines = []
    for i in range(25):
        lines.append(f"![img{i}](./img{i}.png)")
    md = "\n\n".join(lines)
    docspec = parse_markdown_to_docspec(md)
    images = [b for b in docspec["blocks"] if b["type"] == "image"]
    assert len(images) == MAX_IMAGES


def test_max_table_rows_truncation():
    """超过 50 行的表格应被截断"""
    from kai_docx_generator.parser.md_to_ast import MAX_TABLE_ROWS
    lines = ["| 列1 | 列2 |", "| --- | --- |"]
    for i in range(60):
        lines.append(f"| A{i} | B{i} |")
    md = "\n".join(lines)
    docspec = parse_markdown_to_docspec(md)
    tables = [b for b in docspec["blocks"] if b["type"] == "table"]
    assert len(tables) == 1
    assert len(tables[0]["rows"]) == MAX_TABLE_ROWS


def test_max_table_cols_truncation():
    """超过 20 列的表格应被截断"""
    from kai_docx_generator.parser.md_to_ast import MAX_TABLE_COLS
    headers = " | ".join([f"列{i}" for i in range(25)])
    sep = " | ".join(["---"] * 25)
    row = " | ".join([f"值{i}" for i in range(25)])
    md = f"| {headers} |\n| {sep} |\n| {row} |"
    docspec = parse_markdown_to_docspec(md)
    tables = [b for b in docspec["blocks"] if b["type"] == "table"]
    assert len(tables) == 1
    assert len(tables[0]["headers"]) == MAX_TABLE_COLS
    assert len(tables[0]["rows"][0]) == MAX_TABLE_COLS
