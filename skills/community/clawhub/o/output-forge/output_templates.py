"""
OutputForge Template System
Platform-specific formatting templates

Author: Shadow Rose
License: MIT
"""

import html
import re
from datetime import datetime


def wordpress_template(content, metadata, options):
    """WordPress HTML format with proper structure"""
    title = metadata.get('title', 'Untitled')
    author = metadata.get('author', 'Anonymous')
    date = metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
    tags = metadata.get('tags', [])
    description = metadata.get('description', '')
    
    # Convert markdown-style formatting to HTML
    content = content.replace('\n\n', '</p>\n<p>')
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
    content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
    
    # Handle headers
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # Add image placeholders if requested
    if options.get('image_placeholders'):
        content = content.replace('[IMAGE]', '<!-- wp:image -->\n<figure class="wp-block-image"><img src="" alt=""/></figure>\n<!-- /wp:image -->')
    
    tags_html = ' '.join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags)
    
    return f"""<!-- wp:post-title /-->

<!-- wp:post-meta -->
<div class="post-meta">
    <span class="author">By {html.escape(author)}</span>
    <span class="date">{html.escape(date)}</span>
</div>
<!-- /wp:post-meta -->

<!-- wp:post-content -->
<p>{content}</p>
<!-- /wp:post-content -->

<!-- wp:post-tags -->
<div class="post-tags">
    {tags_html}
</div>
<!-- /wp:post-tags -->
"""


def medium_template(content, metadata, options):
    """Medium-ready Markdown with proper formatting"""
    title = metadata.get('title', 'Untitled')
    author = metadata.get('author', 'Anonymous')
    tags = metadata.get('tags', [])
    
    # Medium supports markdown but prefers clean formatting
    # Add title and subtitle
    output = f"# {title}\n\n"
    
    if metadata.get('description'):
        output += f"## {metadata['description']}\n\n"
    
    output += content
    
    # Add image placeholders if requested
    if options.get('image_placeholders'):
        output = output.replace('[IMAGE]', '![Image description](https://your-image-url-here.com)')
    
    # Add footer with tags
    if tags:
        output += f"\n\n---\n\n**Tags:** {', '.join(tags)}"
    
    return output


def email_template(content, metadata, options):
    """Email newsletter HTML with responsive design"""
    title = metadata.get('title', 'Newsletter')
    author = metadata.get('author', 'Anonymous')
    
    # Convert content to HTML
    content_html = content.replace('\n\n', '</p>\n<p>')
    content_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content_html)
    content_html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content_html)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        p {{
            margin: 16px 0;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 14px;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>{html.escape(title)}</h1>
    <p>{content_html}</p>
    
    <div class="footer">
        <p>—{html.escape(author)}</p>
    </div>
</body>
</html>
"""


def twitter_template(content_list, metadata, options):
    """Twitter thread format with numbering"""
    if isinstance(content_list, str):
        content_list = [content_list]
    
    thread = []
    total = len(content_list)
    
    for i, tweet in enumerate(content_list, 1):
        if total > 1:
            thread.append(f"{i}/{total} {tweet}")
        else:
            thread.append(tweet)
    
    return "\n\n---THREAD BREAK---\n\n".join(thread)


def linkedin_template(content, metadata, options):
    """LinkedIn post format with professional structure"""
    title = metadata.get('title', '')
    
    output = ""
    if title:
        output += f"**{title}**\n\n"
    
    # LinkedIn supports limited markdown
    # Keep paragraphs short for readability
    paragraphs = content.split('\n\n')
    output += '\n\n'.join(paragraphs)
    
    # Add hashtags at the end if tags provided
    tags = metadata.get('tags', [])
    if tags:
        hashtags = ' '.join(f'#{tag.replace(" ", "")}' for tag in tags)
        output += f"\n\n{hashtags}"
    
    return output


def markdown_template(content, metadata, options):
    """Clean Markdown with frontmatter"""
    title = metadata.get('title', 'Untitled')
    author = metadata.get('author', 'Anonymous')
    date = metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
    tags = metadata.get('tags', [])
    description = metadata.get('description', '')
    
    frontmatter = f"""---
title: {title}
author: {author}
date: {date}
tags: [{', '.join(tags)}]
description: {description}
---

"""
    
    return frontmatter + content


def latex_template(content, metadata, options):
    """LaTeX document format"""
    title = metadata.get('title', 'Untitled')
    author = metadata.get('author', 'Anonymous')
    date = metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Escape LaTeX special characters
    def escape_latex(text):
        special = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }
        for char, escaped in special.items():
            text = text.replace(char, escaped)
        return text
    
    content_escaped = escape_latex(content)
    
    # Convert markdown-style to LaTeX
    content_escaped = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', content_escaped)
    content_escaped = re.sub(r'\*(.+?)\*', r'\\textit{\1}', content_escaped)
    content_escaped = re.sub(r'`(.+?)`', r'\\texttt{\1}', content_escaped)
    
    # Handle sections
    content_escaped = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content_escaped, flags=re.MULTILINE)
    content_escaped = re.sub(r'^## (.+)$', r'\\subsection{\1}', content_escaped, flags=re.MULTILINE)
    content_escaped = re.sub(r'^# (.+)$', r'\\section{\1}', content_escaped, flags=re.MULTILINE)
    
    return f"""\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{hyperref}}

\\title{{{escape_latex(title)}}}
\\author{{{escape_latex(author)}}}
\\date{{{escape_latex(date)}}}

\\begin{{document}}

\\maketitle

{content_escaped}

\\end{{document}}
"""


def plain_template(content, metadata, options):
    """Plain text with minimal formatting"""
    title = metadata.get('title', '')
    author = metadata.get('author', '')
    date = metadata.get('date', '')
    
    output = ""
    if title:
        output += f"{title}\n"
        output += "=" * len(title) + "\n\n"
    
    if author or date:
        output += f"By {author}" + (f" • {date}" if date else "") + "\n\n"
    
    output += content
    
    return output


# Template registry
TEMPLATES = {
    'wordpress': wordpress_template,
    'medium': medium_template,
    'email': email_template,
    'twitter': twitter_template,
    'thread': twitter_template,  # Alias
    'linkedin': linkedin_template,
    'markdown': markdown_template,
    'latex': latex_template,
    'plain': plain_template,
}


def apply_template(format_type, content, metadata, options):
    """Apply a template to content"""
    if format_type not in TEMPLATES:
        raise ValueError(f"Unknown template: {format_type}")
    
    return TEMPLATES[format_type](content, metadata, options)
