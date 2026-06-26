#!/usr/bin/env python3
"""
Resume Tailoring Script
Takes the base resume.json + a job description, outputs a tailored LaTeX resume.
The actual tailoring logic (reordering bullets, emphasizing skills) is done by the
calling agent — this script handles JSON→LaTeX conversion and PDF compilation.
"""

import json
import subprocess
import sys
import os
import argparse
from pathlib import Path

TEMPLATE = r"""\documentclass[a4paper]{{article}}
    \usepackage{{fullpage}}
    \usepackage{{amsmath}}
    \usepackage{{amssymb}}
    \usepackage{{textcomp}}
    \usepackage[utf8]{{inputenc}}
    \usepackage[T1]{{fontenc}}
    \textheight=10in
    \pagestyle{{empty}}
    \raggedright
    \usepackage[left=0.8in,right=0.8in,bottom=0.8in,top=0.8in]{{geometry}}

\def\bull{{\vrule height 0.8ex width .7ex depth -.1ex }}

\newcommand{{\lineunder}} {{
    \vspace*{{-8pt}} \\
    \hspace*{{-18pt}} \hrulefill \\
}}

\newcommand{{\header}} [1] {{
    {{\hspace*{{-18pt}}\vspace*{{6pt}} \textsc{{#1}}}}
    \vspace*{{-6pt}} \lineunder
}}

\newenvironment{{achievements}}{{
    \begin{{list}}
        {{$\bullet$}}{{\topsep 0pt \itemsep -2pt}}}}{{\vspace*{{4pt}}
    \end{{list}}
}}

    \begin{{document}}
\vspace*{{-40pt}}

%==== Profile ====%
\vspace*{{-10pt}}
\begin{{center}}
	{{\Huge \scshape {{{name}}}}}\\
	{contact_line}\\
\end{{center}}

%==== Education ====%
\header{{Education}}
{education_block}

%==== Experience ====%
\header{{Work Experience}}
\vspace{{1mm}}
{work_block}

\header{{Skills}}
\begin{{tabular}}{{ l l }}
{skills_block}
\end{{tabular}}
\vspace{{2mm}}

\header{{Honors and Awards}}
{awards_block}

\header{{Projects}}
{projects_block}

\end{{document}}"""


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    if not text:
        return ""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def build_contact_line(basics: dict) -> str:
    parts = []
    if basics.get("location", {}).get("address"):
        parts.append(escape_latex(basics["location"]["address"]))
    if basics.get("email"):
        parts.append(escape_latex(basics["email"]))
    if basics.get("phone"):
        parts.append(escape_latex(basics["phone"]))
    if basics.get("website"):
        parts.append(escape_latex(basics["website"]))
    return " $\\cdot$ ".join(parts)


def build_education(education: list) -> str:
    blocks = []
    for edu in education:
        block = f"\\textbf{{{escape_latex(edu.get('institution', ''))}}}\\hfill {escape_latex(edu.get('location', ''))}\\\\\\n"
        block += f"{escape_latex(edu.get('studyType', ''))} {escape_latex(edu.get('area', ''))} \\hfill {escape_latex(edu.get('startDate', ''))} - {escape_latex(edu.get('endDate', ''))}\\\\\\n"
        block += "\\vspace{2mm}"
        blocks.append(block)
    return "\n".join(blocks)


def build_work(work: list) -> str:
    blocks = []
    for job in work:
        block = f"\\textbf{{{escape_latex(job.get('company', ''))}}} \\hfill {escape_latex(job.get('location', ''))}\\\\\\n"
        block += f"\\textit{{{escape_latex(job.get('position', ''))}}} \\hfill {escape_latex(job.get('startDate', ''))} - {escape_latex(job.get('endDate', ''))}\\\\\\n"
        highlights = [h for h in job.get("highlights", []) if h.strip()]
        if highlights:
            block += "\\vspace{-1mm}\n\\begin{itemize} \\itemsep 1pt\n"
            for h in highlights:
                block += f"\t\\item {escape_latex(h)}\n"
            block += "\\end{itemize}\n"
        blocks.append(block)
    return "\n".join(blocks)


def build_skills(skills: list) -> str:
    lines = []
    for skill in skills:
        kw = ", ".join([escape_latex(k) for k in skill.get("keywords", []) if k.strip()])
        if kw:
            lines.append(f"\t{escape_latex(skill.get('name', ''))}:  & {kw} \\\\")
    return "\n".join(lines)


def build_awards(awards: list) -> str:
    blocks = []
    for award in awards:
        block = f"\\textbf{{{escape_latex(award.get('title', ''))}}} \\hfill {escape_latex(award.get('awarder', ''))}\\\\\\n"
        if award.get("summary"):
            block += f"{escape_latex(award['summary'])} "
        block += f"\\hfill {escape_latex(award.get('date', ''))}\\\\\\n"
        block += "\\vspace*{2mm}"
        blocks.append(block)
    return "\n".join(blocks)


def build_projects(projects: list) -> str:
    blocks = []
    for proj in projects:
        if not proj.get("name"):
            continue
        kw = ", ".join([escape_latex(k) for k in proj.get("keywords", []) if k.strip()])
        url_part = f" \\hfill {escape_latex(proj['url'])}" if proj.get("url") else ""
        block = f"{{\\textbf{{{escape_latex(proj['name'])}}}}} {{\\sl {kw}}}{url_part}\\\\\\n"
        if proj.get("description"):
            block += f"{escape_latex(proj['description'])}\\\\\\n"
        block += "\\vspace*{2mm}"
        blocks.append(block)
    return "\n".join(blocks)


def generate_latex(resume_data: dict) -> str:
    basics = resume_data.get("basics", {})
    return TEMPLATE.format(
        name=escape_latex(basics.get("name", "")),
        contact_line=build_contact_line(basics),
        education_block=build_education(resume_data.get("education", [])),
        work_block=build_work(resume_data.get("work", [])),
        skills_block=build_skills(resume_data.get("skills", [])),
        awards_block=build_awards(resume_data.get("awards", [])),
        projects_block=build_projects(resume_data.get("projects", [])),
    )


def compile_pdf(tex_path: str, output_dir: str) -> str:
    """Compile LaTeX to PDF. Returns path to PDF or raises."""
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
        capture_output=True, text=True, timeout=30
    )
    pdf_path = os.path.join(output_dir, Path(tex_path).stem + ".pdf")
    if os.path.exists(pdf_path):
        return pdf_path
    raise RuntimeError(f"PDF compilation failed:\n{result.stdout}\n{result.stderr}")


def main():
    parser = argparse.ArgumentParser(description="Generate tailored resume PDF from JSON")
    parser.add_argument("input_json", help="Path to resume JSON (base or tailored)")
    parser.add_argument("output_name", help="Output filename without extension (e.g. 'google-swe')")
    parser.add_argument("--output-dir", default="tailored-resumes", help="Output directory")
    parser.add_argument("--tex-only", action="store_true", help="Only generate .tex, skip PDF compilation")
    args = parser.parse_args()

    with open(args.input_json) as f:
        resume_data = json.load(f)

    os.makedirs(args.output_dir, exist_ok=True)

    latex = generate_latex(resume_data)
    tex_path = os.path.join(args.output_dir, f"{args.output_name}.tex")

    with open(tex_path, "w") as f:
        f.write(latex)
    print(f"Generated: {tex_path}")

    if not args.tex_only:
        pdf_path = compile_pdf(tex_path, args.output_dir)
        print(f"Compiled: {pdf_path}")
        # Clean up aux files
        for ext in [".aux", ".log", ".out"]:
            aux = os.path.join(args.output_dir, f"{args.output_name}{ext}")
            if os.path.exists(aux):
                os.remove(aux)


if __name__ == "__main__":
    main()
