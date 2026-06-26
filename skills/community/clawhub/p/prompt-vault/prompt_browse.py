#!/usr/bin/env python3
"""
PromptVault HTML Browse Interface Generator
Generate static HTML for easy prompt browsing

Author: Shadow Rose
License: MIT
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import html

import os as _os, types as _types
def _load_config():
    _defaults = {"VAULT_PATH": "./prompt_vault.json"}
    for _p in ("config.json", "config_example.json"):
        if _os.path.exists(_p):
            try:
                import json as _j
                with open(_p, "r", encoding="utf-8") as _f:
                    _defaults.update(_j.load(_f))
                    return _types.SimpleNamespace(**_defaults)
            except Exception:
                pass
    return _types.SimpleNamespace(**_defaults)
config = _load_config()


def generate_html(vault_data, output_path, title="Prompt Vault"):
    """Generate static HTML browse interface"""
    
    prompts = vault_data.get('prompts', [])
    
    # Sort by rating (desc) then name
    prompts_sorted = sorted(
        prompts,
        key=lambda p: (-(p.get('rating') or 0), p.get('name', ''))
    )
    
    # Group by category
    by_category = {}
    for p in prompts_sorted:
        cat = p.get('category', 'uncategorized')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(p)
    
    # Get all tags
    all_tags = set()
    for p in prompts:
        all_tags.update(p.get('tags', []))
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        
        header {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 2.5em;
        }}
        
        .stats {{
            display: flex;
            gap: 30px;
            margin: 20px 0;
            padding: 15px;
            background: #ecf0f1;
            border-radius: 5px;
        }}
        
        .stat {{
            flex: 1;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .search-bar {{
            margin: 20px 0;
            padding: 15px;
            background: #fff;
            border: 2px solid #ddd;
            border-radius: 5px;
        }}
        
        #searchInput {{
            width: 100%;
            padding: 10px;
            font-size: 1em;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        
        .filters {{
            margin: 20px 0;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 8px 15px;
            background: #ecf0f1;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s;
        }}
        
        .filter-btn:hover {{
            background: #3498db;
            color: white;
        }}
        
        .filter-btn.active {{
            background: #2980b9;
            color: white;
        }}
        
        .category-section {{
            margin: 30px 0;
        }}
        
        .category-header {{
            font-size: 1.5em;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-transform: capitalize;
        }}
        
        .prompt-card {{
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            transition: box-shadow 0.3s;
        }}
        
        .prompt-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .prompt-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .prompt-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .prompt-rating {{
            color: #f39c12;
            font-size: 1.2em;
        }}
        
        .prompt-meta {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        
        .prompt-text {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        
        .tags {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin: 10px 0;
        }}
        
        .tag {{
            background: #3498db;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        
        .notes {{
            margin-top: 10px;
            padding: 10px;
            background: #fff9e6;
            border-left: 4px solid #f39c12;
            font-size: 0.9em;
        }}
        
        .copy-btn {{
            background: #27ae60;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.3s;
        }}
        
        .copy-btn:hover {{
            background: #229954;
        }}
        
        .copy-btn:active {{
            background: #1e8449;
        }}
        
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .hidden {{
            display: none !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{html.escape(title)}</h1>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{len(prompts)}</div>
                    <div class="stat-label">Total Prompts</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(by_category)}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(all_tags)}</div>
                    <div class="stat-label">Tags</div>
                </div>
            </div>
        </header>
        
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="Search prompts by name, text, or notes..." />
        </div>
        
        <div class="filters">
            <button class="filter-btn active" data-category="all">All Categories</button>
"""
    
    # Add category filter buttons
    for cat in sorted(by_category.keys()):
        html_content += f'            <button class="filter-btn" data-category="{html.escape(cat)}">{html.escape(cat.title())} ({len(by_category[cat])})</button>\n'
    
    html_content += """        </div>
        
        <div id="promptsContainer">
"""
    
    # Add prompt cards by category
    for cat in sorted(by_category.keys()):
        html_content += f'            <div class="category-section" data-category="{html.escape(cat)}">\n'
        html_content += f'                <h2 class="category-header">{html.escape(cat)}</h2>\n'
        
        for p in by_category[cat]:
            prompt_id = p.get('id', '')
            name = p.get('name', 'Untitled')
            text = p.get('text', '')
            rating = p.get('rating', 0)
            stars = '⭐' * rating if rating else '☆☆☆☆☆'
            tags = p.get('tags', [])
            author = p.get('author', 'Unknown')
            usage_count = p.get('usage_count', 0)
            notes = p.get('notes', '')
            models = p.get('model_compat', '')
            
            # Build tags HTML
            tags_html = ''.join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags)
            
            html_content += f"""                <div class="prompt-card" data-tags="{html.escape(','.join(tags))}">
                    <div class="prompt-header">
                        <div class="prompt-name">{html.escape(name)}</div>
                        <div class="prompt-rating">{stars}</div>
                    </div>
                    <div class="prompt-meta">
                        <span>ID: <code>{html.escape(prompt_id)}</code></span>
                        <span>By: {html.escape(author)}</span>
                        <span>Used: {usage_count} times</span>
"""
            
            if models:
                html_content += f'                        <span>Models: {html.escape(models)}</span>\n'
            
            html_content += '                    </div>\n'
            
            if tags:
                html_content += f'                    <div class="tags">{tags_html}</div>\n'
            
            html_content += f'                    <div class="prompt-text">{html.escape(text)}</div>\n'
            
            if notes:
                html_content += f'                    <div class="notes">{html.escape(notes)}</div>\n'
            
            html_content += f'                    <button class="copy-btn" onclick="copyPrompt(\'{prompt_id}\')">Copy to Clipboard</button>\n'
            html_content += '                </div>\n'
        
        html_content += '            </div>\n'
    
    html_content += f"""        </div>
        
        <footer>
            <p>Generated by PromptVault on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p>Total prompts: {len(prompts)} | Categories: {len(by_category)} | Tags: {len(all_tags)}</p>
        </footer>
    </div>
    
    <script>
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const promptCards = document.querySelectorAll('.prompt-card');
        
        searchInput.addEventListener('input', function() {{
            const query = this.value.toLowerCase();
            
            promptCards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }});
        
        // Category filtering
        const filterBtns = document.querySelectorAll('.filter-btn');
        const categorySections = document.querySelectorAll('.category-section');
        
        filterBtns.forEach(btn => {{
            btn.addEventListener('click', function() {{
                // Remove active from all
                filterBtns.forEach(b => b.classList.remove('active'));
                // Add active to clicked
                this.classList.add('active');
                
                const category = this.dataset.category;
                
                if (category === 'all') {{
                    categorySections.forEach(section => section.classList.remove('hidden'));
                }} else {{
                    categorySections.forEach(section => {{
                        if (section.dataset.category === category) {{
                            section.classList.remove('hidden');
                        }} else {{
                            section.classList.add('hidden');
                        }}
                    }});
                }}
            }});
        }});
        
        // Copy to clipboard functionality
        function copyPrompt(promptId) {{
            // Find the prompt card
            const cards = document.querySelectorAll('.prompt-card');
            let promptText = '';
            
            cards.forEach(card => {{
                if (card.textContent.includes(promptId)) {{
                    const textDiv = card.querySelector('.prompt-text');
                    if (textDiv) {{
                        promptText = textDiv.textContent;
                    }}
                }}
            }});
            
            if (promptText) {{
                navigator.clipboard.writeText(promptText).then(() => {{
                    // Visual feedback
                    const btn = event.target;
                    const originalText = btn.textContent;
                    btn.textContent = 'Copied!';
                    btn.style.background = '#27ae60';
                    
                    setTimeout(() => {{
                        btn.textContent = originalText;
                        btn.style.background = '';
                    }}, 2000);
                }}).catch(err => {{
                    alert('Failed to copy to clipboard');
                }});
            }}
        }}
    </script>
</body>
</html>
"""
    
    # Write to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding='utf-8')
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Generate HTML browse interface for PromptVault',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate HTML from default vault
  python prompt_browse.py -o browse.html
  
  # Custom vault and title
  python prompt_browse.py --vault team_prompts.json -o team_browse.html --title "Team Prompts"
        """
    )
    
    parser.add_argument('--vault', default=config.VAULT_PATH, help='Vault JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output HTML file')
    parser.add_argument('--title', default='Prompt Vault', help='Page title')
    
    args = parser.parse_args()
    
    try:
        vault_path = Path(args.vault)
        if not vault_path.exists():
            print(f"Error: Vault file not found: {args.vault}")
            sys.exit(1)
        
        with open(vault_path, 'r', encoding='utf-8') as f:
            vault_data = json.load(f)
        
        output_path = generate_html(vault_data, args.output, args.title)
        print(f"HTML browse interface generated: {output_path}")
        print(f"Open in browser: file://{output_path.absolute()}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
