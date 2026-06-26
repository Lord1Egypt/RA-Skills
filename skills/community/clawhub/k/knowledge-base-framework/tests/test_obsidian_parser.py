#!/usr/bin/env python3
"""
Tests for Obsidian Parser Module

Tests WikiLink extraction, Tag extraction, Frontmatter parsing, and Embed extraction.
"""

import unittest
import sys
from pathlib import Path

# Add kb_framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.obsidian.parser import (
    WIKILINK_PATTERN,
    EMBED_PATTERN,
    TAG_PATTERN,
    FRONTMATTER_PATTERN,
    parse_frontmatter,
    extract_wikilinks,
    extract_tags,
    extract_embeds,
    extract_context,
)


class TestWikiLinkPattern(unittest.TestCase):
    """Test WikiLink regex pattern directly."""
    
    def test_simple_wikilink(self):
        """Test [[note]] extraction."""
        content = "Siehe [[Test Note]]"
        matches = WIKILINK_PATTERN.findall(content)
        self.assertEqual(len(matches), 1)
        # findall returns tuple of groups
        self.assertEqual(matches[0][0], "Test Note")
    
    def test_wikilink_with_heading(self):
        """Test [[note#heading]] extraction."""
        content = "Link zu [[Test Note#Heading]]"
        matches = WIKILINK_PATTERN.findall(content)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "Test Note")
        self.assertEqual(matches[0][1], "Heading")
    
    def test_wikilink_with_alias(self):
        """Test [[note|alias]] extraction."""
        content = "Link zu [[Test Note|Alias]]"
        matches = WIKILINK_PATTERN.findall(content)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "Test Note")
        self.assertEqual(matches[0][2], "Alias")
    
    def test_wikilink_with_heading_and_alias(self):
        """Test [[note#heading|alias]] extraction."""
        content = "Link zu [[Test Note#Heading|Alias]]"
        matches = WIKILINK_PATTERN.findall(content)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "Test Note")
        self.assertEqual(matches[0][1], "Heading")
        self.assertEqual(matches[0][2], "Alias")
    
    def test_multiple_wikilinks(self):
        """Test multiple links in same content."""
        content = "Siehe [[Note 1]] und [[Note 2|Alias 2]]"
        matches = WIKILINK_PATTERN.findall(content)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0][0], "Note 1")
        self.assertEqual(matches[1][0], "Note 2")
        self.assertEqual(matches[1][2], "Alias 2")


class TestExtractWikiLinks(unittest.TestCase):
    """Test extract_wikilinks function."""
    
    def test_simple_link(self):
        """Test simple [[Target]] extraction."""
        content = "Siehe [[Test Note]]"
        links = extract_wikilinks(content)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]['target'], "Test Note")
        self.assertIsNone(links[0]['heading'])
        self.assertIsNone(links[0]['alias'])
        self.assertFalse(links[0]['is_embed'])
    
    def test_link_with_heading_and_alias(self):
        """Test [[Target#Heading|Alias]] extraction."""
        content = "Siehe [[Test Note#Heading|Alias]]"
        links = extract_wikilinks(content)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]['target'], "Test Note")
        self.assertEqual(links[0]['heading'], "Heading")
        self.assertEqual(links[0]['alias'], "Alias")
    
    def test_multiple_links_different_types(self):
        """Test extracting mixed link types."""
        content = "Siehe [[Test Note]] und [[Test Note#Heading|Alias]]"
        links = extract_wikilinks(content)
        
        self.assertEqual(len(links), 2)
        
        # First link: simple
        self.assertEqual(links[0]['target'], "Test Note")
        self.assertIsNone(links[0]['heading'])
        self.assertIsNone(links[0]['alias'])
        
        # Second link: with heading and alias
        self.assertEqual(links[1]['target'], "Test Note")
        self.assertEqual(links[1]['heading'], "Heading")
        self.assertEqual(links[1]['alias'], "Alias")
    
    def test_sorted_by_position(self):
        """Test that links are sorted by position in content."""
        content = "Zuerst [[B]], dann [[A]], zuletzt [[C]]"
        links = extract_wikilinks(content)
        
        self.assertEqual(len(links), 3)
        self.assertEqual(links[0]['target'], "B")
        self.assertEqual(links[1]['target'], "A")
        self.assertEqual(links[2]['target'], "C")
    
    def test_no_wikilinks(self):
        """Test content without any wikilinks."""
        content = "Keine Links hier, nur normaler Text."
        links = extract_wikilinks(content)
        self.assertEqual(len(links), 0)


class TestTagPattern(unittest.TestCase):
    """Test TAG regex pattern directly."""
    
    def test_simple_tag(self):
        """Test #tag extraction."""
        content = "#tag1"
        tags = TAG_PATTERN.findall(content)
        self.assertEqual(tags, ["#tag1"])
    
    def test_nested_tag(self):
        """Test #tag/subtag extraction."""
        content = "#tag/subtag"
        tags = TAG_PATTERN.findall(content)
        self.assertEqual(tags, ["#tag/subtag"])
    
    def test_deep_nested_tag(self):
        """Test #a/b/c/d extraction."""
        content = "#a/b/c/d"
        tags = TAG_PATTERN.findall(content)
        self.assertEqual(tags, ["#a/b/c/d"])
    
    def test_mixed_tags(self):
        """Test multiple tags in content."""
        content = "#tag1 #tag/subtag #TAG"
        tags = TAG_PATTERN.findall(content)
        self.assertEqual(len(tags), 3)
        self.assertIn("#tag1", tags)
        self.assertIn("#tag/subtag", tags)
        self.assertIn("#TAG", tags)


class TestExtractTags(unittest.TestCase):
    """Test extract_tags function."""
    
    def test_simple_tag(self):
        """Test single simple tag."""
        content = "#tag1"
        tags = extract_tags(content)
        self.assertEqual(tags, ["tag1"])
    
    def test_nested_tag(self):
        """Test nested tag."""
        content = "#tag/subtag"
        tags = extract_tags(content)
        self.assertEqual(tags, ["tag/subtag"])
    
    def test_case_insensitive(self):
        """Test that tags are returned lowercase."""
        content = "#TAG"
        tags = extract_tags(content)
        self.assertEqual(tags, ["tag"])
    
    def test_mixed_case_tags(self):
        """Test multiple tags with different cases."""
        content = "#tag1 #tag/subtag #TAG"
        tags = extract_tags(content)
        # All should be lowercase
        self.assertEqual(sorted(tags), ["tag", "tag/subtag", "tag1"])
    
    def test_no_tags(self):
        """Test content without tags."""
        content = "Keine Tags hier."
        tags = extract_tags(content)
        self.assertEqual(len(tags), 0)
    
    def test_tag_in_sentence(self):
        """Test tag embedded in sentence."""
        content = "Siehe #documentation/guide für Details."
        tags = extract_tags(content)
        self.assertEqual(tags, ["documentation/guide"])


class TestEmbedPattern(unittest.TestCase):
    """Test EMBED regex pattern directly."""
    
    def test_simple_embed(self):
        """Test ![[embed]] extraction."""
        content = "![[Embedded Note]]"
        matches = EMBED_PATTERN.findall(content)
        self.assertEqual(matches, ["Embedded Note"])
    
    def test_embed_with_path(self):
        """Test ![[folder/file]] extraction."""
        content = "![[folder/file.png]]"
        matches = EMBED_PATTERN.findall(content)
        self.assertEqual(matches, ["folder/file.png"])
    
    def test_multiple_embeds(self):
        """Test multiple embeds."""
        content = "![[image1.jpg]] and ![[image2.png]]"
        matches = EMBED_PATTERN.findall(content)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0], "image1.jpg")
        self.assertEqual(matches[1], "image2.png")


class TestExtractEmbeds(unittest.TestCase):
    """Test extract_embeds function."""
    
    def test_simple_embed(self):
        """Test simple embed extraction."""
        content = "![[Embedded Note]]"
        embeds = extract_embeds(content)
        self.assertEqual(embeds, ["Embedded Note"])
    
    def test_multiple_embeds(self):
        """Test multiple embeds."""
        content = "![[folder/file.png]] and ![[image.jpg]]"
        embeds = extract_embeds(content)
        self.assertEqual(len(embeds), 2)
        self.assertIn("folder/file.png", embeds)
        self.assertIn("image.jpg", embeds)
    
    def test_no_embeds(self):
        """Test content without embeds."""
        content = "Keine Embeds hier."
        embeds = extract_embeds(content)
        self.assertEqual(len(embeds), 0)
    
    def test_wikilink_not_embed(self):
        """Test that regular wikilinks are not captured as embeds."""
        content = "[[Regular Link]]"
        embeds = extract_embeds(content)
        self.assertEqual(len(embeds), 0)


class TestParseFrontmatter(unittest.TestCase):
    """Test parse_frontmatter function."""
    
    def test_simple_frontmatter(self):
        """Test basic frontmatter parsing."""
        content = """---
title: Test
tags: [test, ok]
---
Body text"""
        result = parse_frontmatter(content)
        
        self.assertEqual(result['metadata']['title'], "Test")
        self.assertEqual(result['metadata']['tags'], ["test", "ok"])
        self.assertEqual(result['body'], "Body text")
    
    def test_full_frontmatter(self):
        """Test complete frontmatter with all standard fields."""
        content = """---
uid: abc123
title: Full Test
created: 2024-01-15
modified: 2024-01-16
tags: [tag1, tag2, nested/tag3]
aliases: ["Alias1", "Alias2"]
publish: true
---
Note body content."""
        result = parse_frontmatter(content)
        
        self.assertEqual(result['metadata']['uid'], "abc123")
        self.assertEqual(result['metadata']['title'], "Full Test")
        self.assertEqual(result['metadata']['created'], "2024-01-15")
        self.assertEqual(result['metadata']['modified'], "2024-01-16")
        self.assertEqual(result['metadata']['tags'], ["tag1", "tag2", "nested/tag3"])
        self.assertEqual(result['metadata']['aliases'], ["Alias1", "Alias2"])
        self.assertTrue(result['metadata']['publish'])
        self.assertEqual(result['body'], "Note body content.")
    
    def test_no_frontmatter(self):
        """Test content without frontmatter."""
        content = "Just plain content without frontmatter."
        result = parse_frontmatter(content)
        
        self.assertEqual(result['metadata'], {})
        self.assertEqual(result['body'], content)
    
    def test_empty_frontmatter(self):
        """Test empty frontmatter block."""
        content = """---
---
Body"""
        result = parse_frontmatter(content)
        
        self.assertEqual(result['metadata'], {})
        self.assertEqual(result['body'], "Body")
    
    def test_frontmatter_multiline_yaml(self):
        """Test frontmatter with multiline YAML values."""
        content = """---
title: Test
description: |
  This is a multiline
  description.
tags:
  - tag1
  - tag2
---
Body"""
        result = parse_frontmatter(content)
        
        self.assertEqual(result['metadata']['title'], "Test")
        self.assertIn("multiline", result['metadata']['description'])
        self.assertEqual(result['metadata']['tags'], ["tag1", "tag2"])


class TestExtractContext(unittest.TestCase):
    """Test extract_context function."""
    
    def test_context_extraction(self):
        """Test basic context extraction."""
        content = "Prefix text [[Link]] suffix text"
        # Find link position
        match = WIKILINK_PATTERN.search(content)
        context = extract_context(content, match.start())
        
        self.assertIn("Prefix text", context)
        self.assertIn("[[Link]]", context)
        self.assertIn("suffix text", context)
    
    def test_context_truncation(self):
        """Test that context is truncated at content boundaries."""
        content = "[[Link]] at start"
        match = WIKILINK_PATTERN.search(content)
        context = extract_context(content, match.start(), context_chars=10)
        
        # Should not exceed content boundaries
        self.assertTrue(len(context) <= 20 + 10)  # ~10 chars on each side


if __name__ == '__main__':
    unittest.main()
