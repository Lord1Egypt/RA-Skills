"""
lobsterai-report-agent - 超长可研报告多Agent协作撰写系统
========================================================
"""

from .config import (
    get_chapters_dir,
    get_output_dir,
    get_mermaid_cli,
    load_config,
    save_config,
    load_plan,
    save_plan,
    make_default_plan,
    load_glossary,
    generate_glossary,
    glossary_to_prompt_text,
    load_reference,
    save_reference,
    load_progress,
    save_outline_snapshot,
    save_batch_snapshot,
    CHARS_PER_PAGE,
)
from .engine import (
    compute_content_hash,
    load_hashes,
    save_hashes,
    get_changed_chapters,
    process_mermaid_blocks,
    add_toc_entry,
    md_to_paragraphs,
    safe_parse_chapter,
    parse_chapters,
    count_chars,
    check_cross_chapter_consistency,
    generate_final_doc,
    generate_with_accurate_toc,
    convert_single_chapter_inline,
    batch_convert_txt_to_docx,
)
from .cli import main as cli_main

__all__ = [
    # config
    'get_chapters_dir', 'get_output_dir', 'get_mermaid_cli',
    'load_config', 'save_config', 'load_plan', 'save_plan', 'make_default_plan',
    'load_glossary', 'generate_glossary', 'glossary_to_prompt_text',
    'load_reference', 'save_reference', 'load_progress',
    'save_outline_snapshot', 'save_batch_snapshot', 'CHARS_PER_PAGE',
    # engine
    'compute_content_hash', 'load_hashes', 'save_hashes', 'get_changed_chapters',
    'process_mermaid_blocks', 'add_toc_entry', 'md_to_paragraphs',
    'safe_parse_chapter', 'parse_chapters', 'count_chars',
    'check_cross_chapter_consistency',
    'generate_final_doc', 'generate_with_accurate_toc',
    'convert_single_chapter_inline', 'batch_convert_txt_to_docx',
    # cli
    'cli_main',
]
