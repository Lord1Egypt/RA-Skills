"""
integrate_report.py - 整合报告生成器 v3
=========================================
本模块现已重构为 facade（兼容旧接口），实际逻辑在 src/ 包中：

  from src.config import get_chapters_dir, load_plan, ...
  from src.engine import generate_with_accurate_toc, batch_convert_txt_to_docx, ...
  from src.cli import main

向后兼容：from integrate_report import CHAPTERS_DIR, load_plan, generate_with_accurate_toc, ...
CLI 入口：python integrate_report.py [命令]
"""

# ---- 委托给 src 包（向后兼容）----
from src.config import (
    get_chapters_dir as get_chapters_dir,
    get_output_dir as get_output_dir,
    get_mermaid_cli as get_mermaid_cli,
    load_config as load_config,
    save_config as save_config,
    load_plan as load_plan,
    save_plan as save_plan,
    make_default_plan as make_default_plan,
    load_glossary as load_glossary,
    generate_glossary as generate_glossary,
    glossary_to_prompt_text as glossary_to_prompt_text,
    load_reference as load_reference,
    save_reference as save_reference,
    load_progress as load_progress,
    save_outline_snapshot as save_outline_snapshot,
    save_batch_snapshot as save_batch_snapshot,
    CHARS_PER_PAGE as CHARS_PER_PAGE,
    _p as _p,
    _load_paths as _load_paths,
)
from src.engine import (
    compute_content_hash as compute_content_hash,
    load_hashes as load_hashes,
    save_hashes as save_hashes,
    get_changed_chapters as get_changed_chapters,
    process_mermaid_blocks as process_mermaid_blocks,
    add_toc_entry as add_toc_entry,
    md_to_paragraphs as md_to_paragraphs,
    safe_parse_chapter as safe_parse_chapter,
    parse_chapters as parse_chapters,
    count_chars as count_chars,
    check_cross_chapter_consistency as check_cross_chapter_consistency,
    generate_final_doc as generate_final_doc,
    generate_with_accurate_toc as generate_with_accurate_toc,
    convert_single_chapter_inline as convert_single_chapter_inline,
    batch_convert_txt_to_docx as batch_convert_txt_to_docx,
)

# ---- CLI 入口（兼容 python integrate_report.py 用法）----
if __name__ == '__main__':
    from src.cli import main as _cli_main
    _cli_main()
