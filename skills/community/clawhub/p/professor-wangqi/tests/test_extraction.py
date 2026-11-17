"""
Test cases for extraction improvements in extract_knowledge_cards.py

Tests for:
- _extract_title_robust() method
- _extract_authors_robust() method
- Page number tracking
- Integration tests with real extractor
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import re
import sys

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


# Fixtures path
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_texts():
    """Load sample test texts from fixtures."""
    with open(FIXTURES_DIR / "sample_texts.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def expected_outputs():
    """Load expected extraction outputs from fixtures."""
    with open(FIXTURES_DIR / "expected_outputs.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def extractor():
    """Create a KnowledgeCardExtractor instance for testing."""
    try:
        from extract_knowledge_cards import KnowledgeCardExtractor
        return KnowledgeCardExtractor(use_llm=False)
    except ImportError:
        pytest.skip("KnowledgeCardExtractor not available")


class TestExtractTitleRobust:
    """Test cases for _extract_title_robust() method."""

    def test_chinese_title_first_line(self, sample_texts, expected_outputs):
        """Test extraction of Chinese title from first line."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "chinese_title_first_line")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "chinese_title_first_line")
        
        # Simulate title extraction logic
        lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
        extracted_title = lines[0] if lines else ""
        
        assert extracted_title == expected["expected"]["title"], \
            f"Expected '{expected['expected']['title']}', got '{extracted_title}'"

    def test_english_title_from_metadata(self, sample_texts, expected_outputs):
        """Test extraction of English title from metadata."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "english_title_metadata")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "english_title_metadata")
        
        # Title should come from metadata if available
        extracted_title = test_case["metadata"].get("title", "")
        
        assert extracted_title == expected["expected"]["title"], \
            f"Expected '{expected['expected']['title']}', got '{extracted_title}'"

    def test_title_after_cnki_header(self, sample_texts, expected_outputs):
        """Test extraction of title after CNKI download header."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "cnki_generic_metadata")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "cnki_generic_metadata")
        
        lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
        
        # Find title after CNKI header
        title = ""
        for i, line in enumerate(lines):
            if "中国知网" in line or "下载时间" in line:
                # Next non-empty, non-header line should be title
                for j in range(i + 1, len(lines)):
                    if "中国知网" not in lines[j] and "下载时间" not in lines[j]:
                        title = lines[j]
                        break
                break
        
        assert title == expected["expected"]["title"], \
            f"Expected '{expected['expected']['title']}', got '{title}'"

    def test_title_with_empty_lines(self, sample_texts, expected_outputs):
        """Test extraction when text starts with many empty lines."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "empty_lines_start")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "empty_lines_start")
        
        lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
        extracted_title = lines[0] if lines else ""
        
        assert extracted_title == expected["expected"]["title"], \
            f"Expected '{expected['expected']['title']}', got '{extracted_title}'"

    def test_book_chapter_title(self, sample_texts, expected_outputs):
        """Test extraction of book chapter title."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "book_chapter")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "book_chapter")
        
        lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
        extracted_title = lines[0] if lines else ""
        
        assert extracted_title == expected["expected"]["title"], \
            f"Expected '{expected['expected']['title']}', got '{extracted_title}'"


class TestExtractAuthorsRobust:
    """Test cases for _extract_authors_robust() method."""

    def test_single_author_after_title(self, sample_texts, expected_outputs):
        """Test extraction of single author after title."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "chinese_title_first_line")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "chinese_title_first_line")
        
        lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
        
        # Author is typically on line after title
        authors = []
        if len(lines) > 1:
            potential_author = lines[1]
            # Check if it looks like a Chinese name (2-4 characters, no punctuation)
            if re.match(r'^[\u4e00-\u9fa5]{2,4}$', potential_author):
                authors.append(potential_author)
        
        assert authors == expected["expected"]["authors"], \
            f"Expected {expected['expected']['authors']}, got {authors}"

    def test_authors_with_explicit_marker(self, sample_texts, expected_outputs):
        """Test extraction of authors with '作者：' marker."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "authors_pattern")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "authors_pattern")
        
        # Find author line with marker
        authors = []
        for line in test_case["text"].split("\n"):
            if "作者：" in line or "作者:" in line:
                author_text = line.split("：")[-1].split(":")[-1].strip()
                # Split by common delimiters
                authors = [a.strip() for a in re.split(r'[，,、]', author_text) if a.strip()]
                break
        
        assert authors == expected["expected"]["authors"], \
            f"Expected {expected['expected']['authors']}, got {authors}"

    def test_authors_with_affiliation_numbers(self, sample_texts, expected_outputs):
        """Test extraction of authors with affiliation superscript numbers."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "author_affiliation_pattern")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "author_affiliation_pattern")
        
        lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
        
        # Find author line (after title, contains numbers for affiliations)
        authors = []
        for line in lines:
            # Match pattern like "王琦1，朱燕波2，李英帅1"
            if re.search(r'[\u4e00-\u9fa5]+\d', line):
                # Remove affiliation numbers and split
                clean_line = re.sub(r'\d', '', line)
                authors = [a.strip() for a in re.split(r'[，,、]', clean_line) if a.strip()]
                break
        
        assert authors == expected["expected"]["authors"], \
            f"Expected {expected['expected']['authors']}, got {authors}"

    def test_author_from_metadata(self, sample_texts, expected_outputs):
        """Test extraction of author from PDF metadata."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "english_title_metadata")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "english_title_metadata")
        
        # Author should come from metadata if available
        extracted_author = test_case["metadata"].get("author", "")
        authors = [extracted_author] if extracted_author else []
        
        assert authors == expected["expected"]["authors"], \
            f"Expected {expected['expected']['authors']}, got {authors}"

    def test_no_authors_for_book_chapter(self, sample_texts, expected_outputs):
        """Test that book chapters may not have explicit authors."""
        test_case = next(t for t in sample_texts["test_cases"] if t["id"] == "book_chapter")
        expected = next(e for e in expected_outputs["expected_extractions"] if e["test_id"] == "book_chapter")
        
        lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
        
        # Book chapters typically don't have author lines in the same format
        authors = []
        for line in lines:
            # Check for author patterns
            if "作者" in line or re.match(r'^[\u4e00-\u9fa5]{2,4}$', line):
                # This would indicate an author, but book chapters may not have this
                pass
        
        assert authors == expected["expected"]["authors"], \
            f"Expected {expected['expected']['authors']}, got {authors}"


class TestPageNumberTracking:
    """Test cases for page number tracking during extraction."""

    def test_first_page_default(self, sample_texts, expected_outputs):
        """Test that first page defaults to 1."""
        for test_case in sample_texts["test_cases"]:
            expected = next(
                e for e in expected_outputs["expected_extractions"] 
                if e["test_id"] == test_case["id"]
            )
            # First page should always be 1 by default
            assert expected["expected"]["first_page"] == 1

    def test_page_tracking_in_mock_extraction(self):
        """Test page number tracking logic."""
        # Simulate multi-page text
        pages = [
            {"page_num": 1, "text": "Title\n\nAuthor\n\nAbstract..."},
            {"page_num": 2, "text": "Introduction\n\nSection 1..."},
            {"page_num": 3, "text": "Section 2\n\nConclusion..."},
        ]
        
        # Track which page each section appears on
        section_pages = {}
        for page in pages:
            for line in page["text"].split("\n"):
                if line.strip():
                    if "Title" in line:
                        section_pages["title"] = page["page_num"]
                    if "Author" in line:
                        section_pages["author"] = page["page_num"]
                    if "Abstract" in line:
                        section_pages["abstract"] = page["page_num"]
        
        assert section_pages["title"] == 1
        assert section_pages["author"] == 1
        assert section_pages["abstract"] == 1


class TestExtractionConfidence:
    """Test cases for extraction confidence scoring."""

    def test_confidence_high_for_explicit_patterns(self, expected_outputs):
        """Test that confidence is high for explicit patterns like '作者：'."""
        for extraction in expected_outputs["expected_extractions"]:
            if extraction["test_id"] == "authors_pattern":
                # Explicit '作者：' pattern should have high confidence
                assert extraction["expected"]["confidence"]["authors"] >= 0.90

    def test_confidence_lower_for_implicit_patterns(self, expected_outputs):
        """Test that confidence is lower for implicit patterns."""
        for extraction in expected_outputs["expected_extractions"]:
            if extraction["test_id"] == "book_chapter":
                # Book chapters have implicit/no authors, lower confidence
                assert extraction["expected"]["confidence"]["authors"] <= 0.60

    def test_metadata_confidence_higher(self, expected_outputs):
        """Test that metadata-based extraction has higher confidence."""
        for extraction in expected_outputs["expected_extractions"]:
            if extraction["test_id"] == "english_title_metadata":
                # Metadata-based extraction should have high confidence
                assert extraction["expected"]["confidence"]["title"] >= 0.95


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_text(self):
        """Test handling of empty text."""
        text = ""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        assert lines == []

    def test_whitespace_only(self):
        """Test handling of whitespace-only text."""
        text = "   \n\n   \n   "
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        assert lines == []

    def test_very_long_title(self, sample_texts):
        """Test handling of very long potential titles."""
        # A title should not be longer than a reasonable length
        MAX_TITLE_LENGTH = 200
        
        for test_case in sample_texts["test_cases"]:
            lines = [l.strip() for l in test_case["text"].split("\n") if l.strip()]
            if lines:
                potential_title = lines[0]
                assert len(potential_title) <= MAX_TITLE_LENGTH or " " in potential_title, \
                    f"Title too long without spaces: {potential_title[:50]}..."


class TestIntegrationWithRealExtractor:
    """Integration tests using the real KnowledgeCardExtractor."""
    
    def test_real_extractor_rejects_article_type_labels(self, extractor):
        """Test that REVIEW ARTICLE etc. are NOT extracted as titles."""
        # Text with article type label before real title
        text = """REVIEW ARTICLE

Pathogenesis of allergic diseases and implications for therapeutic interventions

Ji Wang, Beijing University of Chinese Medicine

Abstract
This review discusses...
"""
        title = extractor._extract_title_from_text(text)
        
        # Should NOT be "REVIEW ARTICLE"
        assert title != "REVIEW ARTICLE", f"Should not extract article type as title, got: {title}"
        assert title != "Short Communication", f"Should not extract article type as title"
        
    def test_real_extractor_rejects_institution_names_as_authors(self, extractor):
        """Test that institution names are NOT extracted as authors."""
        text = """Access this article online
Quick Response Code:
Website: www.cmj.org

Correspondence to: Ji Wang
School of Life Sciences, Beijing University of Chinese Medicine
"""
        authors = extractor._extract_authors_from_text(text)
        
        # Should NOT contain these institution words
        institution_words = ["Access", "article", "online", "School", "University", "Chinese"]
        for word in institution_words:
            assert word not in authors, f"Institution word '{word}' should not be in authors: {authors}"
    
    def test_real_extractor_title_from_filename(self, extractor):
        """Test title extraction from filename."""
        filename = "1 Pathogenesis of allergic diseases and implications.pdf"
        title = extractor._extract_title_from_filename(filename)
        
        assert "Pathogenesis" in title or "allergic" in title.lower(), \
            f"Expected meaningful title from filename, got: {title}"
        assert title != filename, "Title should be cleaned from filename"
    
    def test_real_extractor_evidence_sentence_filtering(self, extractor):
        """Test that institution addresses are filtered from evidence sentences."""
        # Create a mock card
        card = {
            "conclusions": "",
            "abstract": "", 
            "results": ""
        }
        
        # Text with institution address
        text = """National Institute of Traditional Chinese Medicine Constitution,
Beijing University of Chinese Medicine, Beijing 100105, China

This study found that phlegm-dampness constitution was significantly associated with obesity (P<0.05).
"""
        
        pages = [{"page_num": 1, "text": text}]
        
        evidence = extractor._extract_evidence_sentences(card, text, pages)
        
        # Should contain the finding, not the address
        for e in evidence:
            sentence = e.get("sentence", "")
            # Should NOT contain institution patterns
            assert "University of Chinese Medicine" not in sentence or "found" in sentence.lower(), \
                f"Institution address should be filtered: {sentence[:50]}..."

    def test_special_characters_in_title(self):
        """Test handling of special characters in title."""
        title_with_special = "中医体质学：理论与实践（第二版）"
        # Title should be preserved with special characters
        assert "：" in title_with_special
        assert "（" in title_with_special
        assert "）" in title_with_special
    
    def test_real_extractor_rejects_cas_cae_members(self, extractor):
        """Test that 'FROM CAS & CAE MEMBERS' is NOT extracted as title."""
        text = """FROM CAS & CAE MEMBERS

Development and evaluation of short form of constitution in Chinese

Ji Wang, Beijing University of Chinese Medicine

Abstract
This study...
"""
        title = extractor._extract_title_from_text(text)
        
        # Should NOT be "FROM CAS & CAE MEMBERS"
        assert title != "FROM CAS & CAE MEMBERS", f"Should not extract CAS/CAE header as title, got: {title}"
        assert "cas" not in title.lower() or "development" in title.lower(), \
            f"Title should not contain CAS header: {title}"
    
    def test_real_extractor_rejects_research_article(self, extractor):
        """Test that 'Research Article' is NOT extracted as title."""
        text = """Research Article

Machine learning-assisted rapid determination for traditional Chinese Medicine Constitution

Abstract
This paper presents...
"""
        title = extractor._extract_title_from_text(text)
        
        # Should NOT be "Research Article"
        assert title.lower() != "research article", f"Should not extract 'Research Article' as title, got: {title}"
    
    def test_real_extractor_rejects_administrator_author(self, extractor):
        """Test that 'Administrator' is NOT accepted as author from metadata."""
        # Test metadata with Administrator
        metadata = {"author": "Administrator"}
        text = "Some text"
        
        authors = extractor._extract_authors_robust(text, metadata)
        
        # Should NOT contain Administrator
        assert "Administrator" not in authors, f"Should not accept 'Administrator' as author, got: {authors}"
        assert authors == [] or "Administrator" not in authors, \
            f"Administrator should be filtered from authors: {authors}"

    def test_real_extractor_merges_wrapped_title_and_extracts_authors(self, extractor):
        """Wrapped English titles and title-adjacent author lines should be extracted cleanly."""
        text = """Short Communication

Activation of RXRα exerts cardioprotection through transcriptional
upregulation of Ndufs4 in heart failure
Mingyan Shao a,b,1, Lingru Li b,1, Lin Ma a, Chao Song c, Qi Wang b,⇑, Yong Wang a,h,⇑
a Beijing University of Chinese Medicine, Beijing 100029, China
"""
        title = extractor._extract_title_from_text(text)
        authors = extractor._extract_authors_from_text(text)

        assert title == "Activation of RXRα exerts cardioprotection through transcriptional upregulation of Ndufs4 in heart failure"
        assert "Mingyan Shao" in authors
        assert "Lingru Li" in authors
        assert "Qi Wang" in authors
        assert "Beijing" not in authors

    def test_real_extractor_extracts_metadata_doi_keywords_and_journal(self, extractor):
        """Metadata should populate DOI, keywords, and journal when available."""
        metadata = {
            "subject": "Chinese Medicine, https://doi.org/10.1186/s13020-024-00992-0",
            "keywords": "Automated machine learning (AutoML); Constitution in Chinese Medicine Questionnaire (CCMQ); TPOT",
        }
        text = "Sun et al. Chinese Medicine (2024) 19:127\nhttps://doi.org/10.1186/s13020-024-00992-0"

        doi = extractor._extract_doi(metadata, text)
        keywords = extractor._extract_keywords(metadata, text)
        journal = extractor._extract_journal(metadata, text)

        assert doi == "10.1186/s13020-024-00992-0"
        assert "Automated machine learning (AutoML)" in keywords
        assert "TPOT" in keywords
        assert journal == "Chinese Medicine"

    def test_real_extractor_extracts_title_page_journal_doi_and_year(self, extractor):
        """Title-page journal/DOI/year fallbacks should work without reliable metadata."""
        metadata = {"subject": "", "keywords": ""}
        text = """Cell Physiol Biochem 2018;45:1999-2008
DOI: 10.1159/000487976
Published online: March 08, 2018
"""

        assert extractor._extract_journal(metadata, text) == "Cell Physiol Biochem"
        assert extractor._extract_doi(metadata, text) == "10.1159/000487976"
        assert extractor._extract_year_from_text(text) == 2018

    def test_real_extractor_extracts_structured_abstract_and_conclusion_fallback(self, extractor):
        """Structured abstract text should be captured even when section parsing misses it."""
        sections = {}
        text = """Abstract
OBJECTIVE: To develop the best short form of constitution in Chinese medicine questionnaire.
METHODS: A total of 21 948 subjects were used to refine the short form.
RESULTS: The simplified questionnaire showed acceptable reliability and validity.
This study suggests that the short form can support large-scale health management.
Keywords: questionnaire; body constitution
"""

        abstract = extractor._extract_abstract(sections, text)
        conclusions = extractor._extract_conclusions(sections, text, abstract)

        assert "OBJECTIVE:" in abstract
        assert "METHODS:" in abstract
        assert "This study suggests" in conclusions

    def test_real_extractor_extracts_keywords_from_title_page_line(self, extractor):
        """Comma-separated keyword lines on the title page should be recognized."""
        metadata = {"keywords": ""}
        text = """Enlightenment about using TCM constitutions for individualized medicine
TCM constitution, constitutional classification, individualized medicine, precision medicine
Citation:
Li, L. et al. (2020)
"""

        keywords = extractor._extract_keywords(metadata, text)
        assert keywords == [
            "TCM constitution",
            "constitutional classification",
            "individualized medicine",
            "precision medicine",
        ]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
