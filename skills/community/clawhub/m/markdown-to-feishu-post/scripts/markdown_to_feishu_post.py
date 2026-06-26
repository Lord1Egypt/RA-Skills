#!/usr/bin/env python3
"""
Markdown to Feishu Post Message JSON Converter

Converts standard Markdown text to Feishu rich text message (post) JSON structure.
Supports: headers, bold, italic, underline, strikethrough, links, @mentions,
ordered/unordered lists, code blocks, blockquotes, and horizontal rules.
"""

import re
import json
import sys
from typing import List, Dict, Any


def parse_inline_elements(text: str, inherited_styles: List[str] = None) -> List[Dict[str, Any]]:
    """Parse inline markdown elements and return Feishu post elements.
    
    Args:
        text: The text to parse
        inherited_styles: Styles inherited from parent elements (for nested formatting)
    """
    if inherited_styles is None:
        inherited_styles = []
    
    if not text:
        return []
    
    elements = []
    pos = 0
    length = len(text)
    
    while pos < length:
        # Check for @mention: <at user_id="xxx">name</at>
        at_match = re.match(r'<at\s+user_id=["\']([^"\']+)["\']\s*>([^<]*)</at>', text[pos:])
        if at_match:
            elem = {"tag": "at", "user_id": at_match.group(1)}
            if inherited_styles:
                elem["style"] = list(set(inherited_styles))
            elements.append(elem)
            pos += at_match.end()
            continue
        
        # Check for image: ![alt](image_key)
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', text[pos:])
        if img_match:
            elements.append({"tag": "img", "image_key": img_match.group(2)})
            pos += img_match.end()
            continue
        
        # Check for link: [text](url)
        link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', text[pos:])
        if link_match:
            elem = {"tag": "a", "text": link_match.group(1), "href": link_match.group(2)}
            if inherited_styles:
                elem["style"] = list(set(inherited_styles))
            elements.append(elem)
            pos += link_match.end()
            continue
        
        # Check for bold+italic: ***text*** (must check before bold and italic)
        bold_italic_match = re.match(r'\*\*\*(.+?)\*\*\*', text[pos:])
        if bold_italic_match:
            content = bold_italic_match.group(1)
            new_styles = list(set(inherited_styles + ["bold", "italic"]))
            inner_elements = parse_inline_elements(content, new_styles)
            elements.extend(inner_elements)
            pos += bold_italic_match.end()
            continue
        
        # Check for bold: **text**
        bold_match = re.match(r'\*\*(.+?)\*\*', text[pos:])
        if bold_match:
            content = bold_match.group(1)
            new_styles = list(set(inherited_styles + ["bold"]))
            inner_elements = parse_inline_elements(content, new_styles)
            elements.extend(inner_elements)
            pos += bold_match.end()
            continue
        
        # Check for strikethrough: ~~text~~
        strike_match = re.match(r'~~(.+?)~~', text[pos:])
        if strike_match:
            content = strike_match.group(1)
            new_styles = list(set(inherited_styles + ["lineThrough"]))
            inner_elements = parse_inline_elements(content, new_styles)
            elements.extend(inner_elements)
            pos += strike_match.end()
            continue
        
        # Check for italic: *text* (must check after bold)
        italic_match = re.match(r'\*([^*]+)\*', text[pos:])
        if italic_match:
            content = italic_match.group(1)
            new_styles = list(set(inherited_styles + ["italic"]))
            inner_elements = parse_inline_elements(content, new_styles)
            elements.extend(inner_elements)
            pos += italic_match.end()
            continue
        
        # Check for underline: ~text~ (Feishu specific, must check after strikethrough)
        underline_match = re.match(r'~([^~]+)~', text[pos:])
        if underline_match:
            content = underline_match.group(1)
            new_styles = list(set(inherited_styles + ["underline"]))
            inner_elements = parse_inline_elements(content, new_styles)
            elements.extend(inner_elements)
            pos += underline_match.end()
            continue
        
        # Check for inline code: `code`
        code_match = re.match(r'`([^`]+)`', text[pos:])
        if code_match:
            elem = {"tag": "text", "text": code_match.group(1)}
            if inherited_styles:
                elem["style"] = list(set(inherited_styles))
            elements.append(elem)
            pos += code_match.end()
            continue
        
        # Plain text - collect until next special character
        plain_text = ""
        while pos < length:
            char = text[pos]
            if char in '*~`[<!':
                remaining = text[pos:]
                # Check for any pattern that starts here
                if (re.match(r'\*\*\*.+?\*\*\*', remaining) or
                    re.match(r'\*\*.+?\*\*', remaining) or
                    re.match(r'\*[^*]+\*', remaining) or
                    re.match(r'~~.+?~~', remaining) or
                    re.match(r'~[^~]+~', remaining) or
                    re.match(r'`[^`]+`', remaining) or
                    re.match(r'\[[^\]]+\]\([^)]+\)', remaining) or
                    re.match(r'!\[[^\]]*\]\([^)]+\)', remaining) or
                    re.match(r'<at\s+user_id=', remaining)):
                    break
            plain_text += char
            pos += 1
        
        if plain_text:
            elem = {"tag": "text", "text": plain_text}
            if inherited_styles:
                elem["style"] = list(set(inherited_styles))
            elements.append(elem)
    
    # Merge adjacent text elements with same styles
    merged = []
    for elem in elements:
        if elem.get("tag") == "text" and merged and merged[-1].get("tag") == "text":
            prev_style = set(merged[-1].get("style", []))
            curr_style = set(elem.get("style", []))
            if prev_style == curr_style:
                merged[-1]["text"] += elem["text"]
                continue
        merged.append(elem)
    
    return merged


def parse_markdown(markdown_text: str) -> Dict[str, Any]:
    """Parse markdown text and return Feishu post JSON structure."""
    lines = markdown_text.split('\n')
    content: List[List[Dict[str, Any]]] = []
    title = ""
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # Headers: # ## ### etc.
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            header_level = len(header_match.group(1))
            header_text = header_match.group(2)
            
            # First # header becomes title
            if header_level == 1 and not title:
                title = header_text
            else:
                # Convert header to styled text
                elements = parse_inline_elements(header_text)
                for elem in elements:
                    if elem.get("tag") == "text":
                        styles = elem.get("style", [])
                        if "bold" not in styles:
                            styles.append("bold")
                        elem["style"] = styles
                content.append(elements)
            i += 1
            continue
        
        # Horizontal rule: --- or *** or ___
        if re.match(r'^[-*_]{3,}\s*$', line.strip()):
            content.append([{"tag": "hr"}])
            i += 1
            continue
        
        # Code block: ```language\ncode\n```
        code_match = re.match(r'^```(\w*)$', line.strip())
        if code_match:
            language = code_match.group(1).upper() or ""
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```
            
            code_text = '\n'.join(code_lines)
            content.append([{
                "tag": "code_block",
                "language": language,
                "text": code_text
            }])
            continue
        
        # Blockquote: > text (supports multi-line)
        if line.strip().startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_text = lines[i].strip()[1:].strip()
                quote_lines.append(quote_text)
                i += 1
            # Combine multi-line quotes with newline, add quote marker for md syntax
            combined_quote = '> ' + '\n> '.join(quote_lines)
            # Use md tag for proper blockquote rendering
            content.append([{
                "tag": "md",
                "text": combined_quote
            }])
            continue
        
        # Unordered list: - item or * item
        if re.match(r'^[-*]\s+', line.strip()):
            list_text = re.sub(r'^[-*]\s+', '', line.strip())
            elements = parse_inline_elements(list_text)
            # Add bullet prefix
            if elements and elements[0].get("tag") == "text":
                elements[0]["text"] = "• " + elements[0]["text"]
            else:
                elements.insert(0, {"tag": "text", "text": "• "})
            content.append(elements)
            i += 1
            continue
        
        # Ordered list: 1. item
        ordered_match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
        if ordered_match:
            num = ordered_match.group(1)
            list_text = ordered_match.group(2)
            elements = parse_inline_elements(list_text)
            # Add number prefix
            if elements and elements[0].get("tag") == "text":
                elements[0]["text"] = f"{num}. " + elements[0]["text"]
            else:
                elements.insert(0, {"tag": "text", "text": f"{num}. "})
            content.append(elements)
            i += 1
            continue
        
        # Image only line: ![alt](image_key)
        if re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip()):
            img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip())
            if img_match:
                content.append([{"tag": "img", "image_key": img_match.group(2)}])
            i += 1
            continue
        
        # Regular paragraph
        elements = parse_inline_elements(line)
        if elements:
            content.append(elements)
        i += 1
    
    result = {"zh_cn": {"content": content}}
    if title:
        result["zh_cn"]["title"] = title
    
    return result


def convert(markdown_text: str, output_format: str = "json") -> str:
    """Convert markdown to Feishu post message JSON."""
    result = parse_markdown(markdown_text)
    if output_format == "compact":
        return json.dumps(result, ensure_ascii=False, separators=(',', ':'))
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_feishu_post.py <markdown_text_or_file>")
        print("       python markdown_to_feishu_post.py --file <markdown_file>")
        print("       python markdown_to_feishu_post.py --compact <markdown_text>")
        sys.exit(1)
    
    compact = "--compact" in sys.argv
    use_file = "--file" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    
    if use_file and args:
        with open(args[0], 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    elif args:
        markdown_text = args[0]
    else:
        print("Error: No input provided")
        sys.exit(1)
    
    output_format = "compact" if compact else "json"
    print(convert(markdown_text, output_format))


if __name__ == "__main__":
    main()