"""
Obsidian Parser - WikiLinks, Tags, Frontmatter, Embeds

Extracts structured data from Obsidian markdown files.
"""

import re
import yaml
from typing import Optional


# =============================================================================
# REGEX PATTERNS
# =============================================================================

# WikiLink: [[target]], [[target#heading]], [[target|alias]], [[target#heading|alias]]
# Capture groups: (target, heading, alias)
# Note: [^\]|]+ means "any char except ] or |" - properly escaped
WIKILINK_PATTERN = re.compile(r'\[\[([^\]|]+?)(?:#([^\]|]+?))?(?:\|([^\]]+?))?\]\]')

# Embed: ![[filename]] or ![[folder/filename]]
EMBED_PATTERN = re.compile(r'!\[\[([^\]]+)\]\]')

# Tags: #tag, #tag/subtag, #a/b/c/d (case-insensitive, must start with letter)
TAG_PATTERN = re.compile(r'#[a-zA-Z][a-zA-Z0-9_/-]+')

# Frontmatter: Standard YAML block at file start
# Handles both empty ---/--- and content between
FRONTMATTER_PATTERN = re.compile(r'^---\n?(.*?)\n---', re.DOTALL)


# =============================================================================
# FRONTMATTER PARSER
# =============================================================================

def parse_frontmatter(content: str) -> dict:
    """
    Parse YAML frontmatter from markdown content.
    
    Args:
        content: Full markdown file content
        
    Returns:
        Dictionary with 'metadata' (dict) and 'body' (str)
        
    Standard Obsidian frontmatter fields:
        - uid: Unique identifier (UUID)
        - title: Note title
        - created: Creation date (ISO format)
        - modified: Last modified date (ISO format)
        - tags: List of tags
        - aliases: List of alternative names
    
    Example:
        >>> content = '''---
        ... title: Test
        ... tags: [test, ok]
        ... ---
        ... Body text'''
        >>> result = parse_frontmatter(content)
        >>> result['metadata']['title']
        'Test'
        >>> result['body']
        'Body text'
    """
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {'metadata': {}, 'body': content}
    
    yaml_str = match.group(1)
    body = content[match.end():].lstrip('\n')
    
    # Handle empty frontmatter or YAML parse errors
    if not yaml_str.strip():
        return {'metadata': {}, 'body': body}
    
    try:
        metadata = yaml.safe_load(yaml_str) or {}
    except yaml.YAMLError:
        metadata = {}
    
    # Handle both YAML object and flat keys
    if not isinstance(metadata, dict):
        metadata = {}
    
    # Convert datetime objects to strings for consistency
    for key, value in metadata.items():
        if hasattr(value, 'isoformat'):
            metadata[key] = value.isoformat()
    
    body = content[match.end():].lstrip('\n')
    return {'metadata': metadata, 'body': body}


# =============================================================================
# WIKILINK EXTRACTOR
# =============================================================================

def extract_wikilinks(content: str) -> list[dict]:
    """
    Extract all wiki links from markdown content.
    
    Args:
        content: Markdown content to parse
        
    Returns:
        List of dictionaries with keys:
            - target: The note name or path being linked to
            - heading: Optional heading anchor (e.g., "Heading" from [[Note#Heading]])
            - alias: Optional display text (e.g., "Alias" from [[Note|Alias]])
            - is_embed: False for wiki links (True for embeds)
            - start: Character position in content
            - end: Character position in content
    
    Examples:
        >>> extract_wikilinks("See [[Test Note]]")
        [{'target': 'Test Note', 'heading': None, 'alias': None, 'is_embed': False, ...}]
        
        >>> extract_wikilinks("Link to [[Note#Heading|Alias]]")
        [{'target': 'Note', 'heading': 'Heading', 'alias': 'Alias', 'is_embed': False, ...}]
    """
    links = []
    
    for match in WIKILINK_PATTERN.finditer(content):
        links.append({
            'target': match.group(1),
            'heading': match.group(2),
            'alias': match.group(3),
            'is_embed': False,
            'start': match.start(),
            'end': match.end()
        })
    
    # Sort by position in content
    links.sort(key=lambda x: x['start'])
    return links


# =============================================================================
# TAG EXTRACTOR
# =============================================================================

def extract_tags(content: str) -> list[str]:
    """
    Extract all #tags from markdown content.
    
    Handles:
        - Simple tags: #tag
        - Nested tags: #tag/subtag
        - Deep nesting: #a/b/c/d
        - Tags with numbers: #tag2024
        - Case-insensitive (returned lowercase)
    
    Args:
        content: Markdown content to parse
        
    Returns:
        List of tag strings (without # prefix, lowercase)
    
    Examples:
        >>> extract_tags("#tag1 #tag/subtag #TAG")
        ['tag1', 'tag/subtag', 'tag']
        
        >>> extract_tags("See #documentation/guide for details")
        ['documentation/guide']
    """
    tags = TAG_PATTERN.findall(content)
    # Remove # prefix and convert to lowercase
    return [t.lstrip('#').lower() for t in tags]


# =============================================================================
# EMBED EXTRACTOR
# =============================================================================

def extract_embeds(content: str) -> list[str]:
    """
    Extract all ![[embed]] references from markdown content.
    
    Args:
        content: Markdown content to parse
        
    Returns:
        List of embedded file paths/names (without ![[ ]] wrapper)
    
    Examples:
        >>> extract_embeds("![[Embedded Note]]")
        ['Embedded Note']
        
        >>> extract_embeds("![[folder/file.png]] and ![[image.jpg]]")
        ['folder/file.png', 'image.jpg']
    """
    matches = EMBED_PATTERN.findall(content)
    return list(matches)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def extract_context(content: str, link_pos: int, context_chars: int = 100) -> str:
    """
    Extract surrounding context text around a link position.
    
    Args:
        content: Full markdown content
        link_pos: Character position of the link
        context_chars: Number of characters to extract on each side
        
    Returns:
        Normalized context string (whitespace collapsed)
    """
    start = max(0, link_pos - context_chars)
    end = min(len(content), link_pos + context_chars)
    context = content[start:end]
    
    # Normalize whitespace
    context = re.sub(r'\s+', ' ', context).strip()
    return context
