/**
 * main.js — ingest_paper Skill 入口
 * 行为由 SKILL.md 驱动；本文件仅提供元信息。
 */
module.exports = {
  name: "ingest_paper",
  version: "1.0.0",
  description:
    "paper-kb 存入文档：arxiv/PDF → 提取 → AI分析 → 查重 → 概念/资源页 → summary → Gitea + 飞书表格",
  entry: "SKILL.md",
  scripts: {
    fetchArxiv: "python3 scripts/fetch_arxiv.py --url <url>",
    processPdf: "python3 scripts/process_pdf.py --pdf_path <path>",
    checkDuplicate:
      "python3 scripts/check_duplicate.py --open_id <id> --title <t> [--arxiv_id <a>] [--text_path <p>]",
    kbRead: "python3 scripts/kb_read.py --open_id <id> --list all | --read <page>",
    savePaper: "python3 scripts/save_paper.py --open_id <id> --title <t> --summary_file <f> ...",
    savePage: "python3 scripts/save_page.py --open_id <id> --kind concept|resource --name <n> --file <f> ...",
  },
};
