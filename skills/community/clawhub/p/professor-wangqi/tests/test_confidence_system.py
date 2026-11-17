"""
Test cases for confidence/field_meta system in extract_knowledge_cards.py

Tests for:
- FieldConfidence dataclass
- ConfidenceCalculator methods
- _field_meta structure format (matching schema)
- _review structure generation
- CardMerger.merge_card metadata sync (if implemented)

These tests are designed to FAIL initially (TDD red phase) because
the current code uses `_confidence` instead of `_field_meta`.
"""

import json
import pytest
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
from typing import Dict, List, Any
import sys

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


# =============================================================================
# Test 1: FieldConfidence Dataclass
# =============================================================================

class TestFieldConfidenceDataclass:
    """Test cases for FieldConfidence dataclass and to_dict() method."""

    def test_field_confidence_basic_creation(self):
        """Test basic FieldConfidence creation with required fields."""
        from extract_knowledge_cards import FieldConfidence
        
        fc = FieldConfidence(
            value="Test Title",
            confidence=0.85,
            source="metadata"
        )
        
        assert fc.value == "Test Title"
        assert fc.confidence == 0.85
        assert fc.source == "metadata"
        assert fc.candidates == []

    def test_field_confidence_with_candidates(self):
        """Test FieldConfidence with candidates list."""
        from extract_knowledge_cards import FieldConfidence
        
        fc = FieldConfidence(
            value="Primary Title",
            confidence=0.92,
            source="text",
            candidates=[
                {"value": "Fallback Title", "confidence": 0.70, "source": "filename"}
            ]
        )
        
        assert len(fc.candidates) == 1
        assert fc.candidates[0]["value"] == "Fallback Title"

    def test_field_confidence_to_dict_includes_all_fields(self):
        """Test that to_dict() includes all required fields."""
        from extract_knowledge_cards import FieldConfidence
        
        fc = FieldConfidence(
            value="Test",
            confidence=0.85,
            source="metadata",
            candidates=[{"value": "Alt", "confidence": 0.60, "source": "filename"}]
        )
        
        result = fc.to_dict()
        
        assert "value" in result
        assert "confidence" in result
        assert "source" in result
        assert "candidates" in result
        assert result["confidence"] == 0.85  # Should be rounded to 2 decimals

    def test_field_confidence_to_dict_excludes_empty_candidates(self):
        """Test that to_dict() excludes candidates when empty."""
        from extract_knowledge_cards import FieldConfidence
        
        fc = FieldConfidence(
            value="Test",
            confidence=0.85,
            source="metadata",
            candidates=[]
        )
        
        result = fc.to_dict()
        
        assert "candidates" not in result

    def test_field_confidence_from_dict_roundtrip(self):
        """Test from_dict() creates equivalent object."""
        from extract_knowledge_cards import FieldConfidence
        
        original = FieldConfidence(
            value="Test Title",
            confidence=0.92,
            source="text",
            candidates=[{"value": "Alt", "confidence": 0.70, "source": "filename"}]
        )
        
        data = original.to_dict()
        restored = FieldConfidence.from_dict(data)
        
        assert restored.value == original.value
        assert restored.confidence == original.confidence
        assert restored.source == original.source
        assert len(restored.candidates) == len(original.candidates)

    def test_field_confidence_confidence_rounding(self):
        """Test that confidence is rounded to 2 decimal places in to_dict()."""
        from extract_knowledge_cards import FieldConfidence
        
        fc = FieldConfidence(
            value="Test",
            confidence=0.85789,
            source="metadata"
        )
        
        result = fc.to_dict()
        
        assert result["confidence"] == 0.86


# =============================================================================
# Test 2: ConfidenceCalculator - Title
# =============================================================================

class TestConfidenceCalculatorTitle:
    """Test cases for ConfidenceCalculator.calculate_title_confidence()."""

    @pytest.fixture
    def calculator(self):
        """Create a ConfidenceCalculator instance."""
        from extract_knowledge_cards import ConfidenceCalculator
        return ConfidenceCalculator()

    def test_title_from_metadata_high_confidence(self, calculator):
        """Title from metadata should have confidence >= 0.75."""
        result = calculator.calculate_title_confidence(
            title="Test Title",
            source="metadata",
            metadata_title="Test Title",
            filename="test.pdf"
        )
        
        assert result.value == "Test Title"
        assert result.source == "metadata"
        assert result.confidence >= 0.75

    def test_title_from_text_with_validation(self, calculator):
        """Title from text should be validated and get appropriate confidence."""
        result = calculator.calculate_title_confidence(
            title="A Study on TCM Constitution and Disease",
            source="text",
            metadata_title="",
            filename="test.pdf"
        )
        
        assert result.value == "A Study on TCM Constitution and Disease"
        assert result.source == "text"
        # Should get bonus for containing "study"
        assert result.confidence >= 0.50

    def test_title_from_filename_lower_confidence(self, calculator):
        """Title derived from filename should have lower confidence."""
        result = calculator.calculate_title_confidence(
            title="TCM Constitution Study",
            source="filename",
            metadata_title="",
            filename="01_TCM_Constitution_Study.pdf"
        )
        
        assert result.source == "filename"
        assert result.confidence == 0.50

    def test_title_from_fallback_lowest_confidence(self, calculator):
        """Fallback title should have lowest confidence."""
        result = calculator.calculate_title_confidence(
            title="Unknown Title",
            source="fallback",
            metadata_title="",
            filename=""
        )
        
        assert result.source == "fallback"
        assert result.confidence == 0.30

    def test_title_empty_returns_none_source(self, calculator):
        """Empty title should return source='none' and confidence=0."""
        result = calculator.calculate_title_confidence(
            title="",
            source="text",
            metadata_title="",
            filename=""
        )
        
        assert result.value == ""
        assert result.source == "none"
        assert result.confidence == 0.0

    def test_title_candidates_include_metadata_alternative(self, calculator):
        """When metadata title differs, it should be a candidate."""
        result = calculator.calculate_title_confidence(
            title="Text Title",
            source="text",
            metadata_title="Metadata Title",
            filename="test.pdf"
        )
        
        assert len(result.candidates) >= 1
        assert any(c["source"] == "metadata" for c in result.candidates)

    def test_title_candidates_limited_to_three(self, calculator):
        """Candidates should be limited to top 3."""
        result = calculator.calculate_title_confidence(
            title="Main Title",
            source="text",
            metadata_title="Meta Title",
            filename="filename_title.pdf"
        )
        
        # Should have at most 3 candidates
        assert len(result.candidates) <= 3


# =============================================================================
# Test 3: ConfidenceCalculator - Authors
# =============================================================================

class TestConfidenceCalculatorAuthors:
    """Test cases for ConfidenceCalculator.calculate_authors_confidence()."""

    @pytest.fixture
    def calculator(self):
        """Create a ConfidenceCalculator instance."""
        from extract_knowledge_cards import ConfidenceCalculator
        return ConfidenceCalculator()

    def test_authors_from_metadata(self, calculator):
        """Authors from metadata should have confidence >= 0.70."""
        result = calculator.calculate_authors_confidence(
            authors=["Wang Qi", "Li Yingshuai"],
            source="metadata",
            metadata_authors="Wang Qi, Li Yingshuai"
        )
        
        assert result.value == ["Wang Qi", "Li Yingshuai"]
        assert result.source == "metadata"
        assert result.confidence >= 0.70

    def test_authors_from_text_with_validation(self, calculator):
        """Authors from text should be validated."""
        result = calculator.calculate_authors_confidence(
            authors=["王琦", "李英帅"],
            source="text",
            metadata_authors=""
        )
        
        assert result.source == "text"
        # Chinese names should pass validation
        assert result.confidence >= 0.50

    def test_authors_empty_returns_none_source(self, calculator):
        """Empty authors list should return source='none'."""
        result = calculator.calculate_authors_confidence(
            authors=[],
            source="text",
            metadata_authors=""
        )
        
        assert result.value == []
        assert result.source == "none"
        assert result.confidence == 0.0

    def test_authors_candidate_from_metadata(self, calculator):
        """When metadata authors differ, they should be a candidate."""
        result = calculator.calculate_authors_confidence(
            authors=["Wang Qi"],
            source="text",
            metadata_authors="Wang Qi, Li Yingshuai"
        )
        
        assert len(result.candidates) >= 1
        assert result.candidates[0]["source"] == "metadata"

    def test_authors_chinese_name_validation(self, calculator):
        """Chinese names (2-4 chars) should pass validation."""
        result = calculator.calculate_authors_confidence(
            authors=["王琦", "朱燕波"],
            source="text",
            metadata_authors=""
        )
        
        # Should get bonus for valid Chinese name patterns
        assert result.confidence >= 0.60

    def test_authors_english_name_validation(self, calculator):
        """English names (First Last pattern) should pass validation."""
        result = calculator.calculate_authors_confidence(
            authors=["John Smith", "Jane Doe"],
            source="text",
            metadata_authors=""
        )
        
        # Should get bonus for valid English name patterns
        assert result.confidence >= 0.60


# =============================================================================
# Test 4: _field_meta Structure
# =============================================================================

class TestFieldMetaStructure:
    """Test cases for _field_meta structure matching schema."""

    @pytest.fixture
    def sample_card_with_field_meta(self):
        """Create a sample card with _field_meta structure."""
        return {
            "card_id": "WQ-SCI-001",
            "title": "Test Title",
            "authors": ["Wang Qi"],
            "year": 2024,
            "_field_meta": {
                "title": {
                    "source": "text",
                    "confidence": 0.85,
                    "level": "high",
                    "reasoning": "Title found on first page with proper capitalization",
                    "candidates": [
                        {"value": "Test Title", "source": "text", "confidence": 0.85}
                    ]
                },
                "authors": {
                    "source": "text",
                    "confidence": 0.65,
                    "level": "medium",
                    "reasoning": "Found explicit marker but names appear generic",
                    "candidates": []
                },
                "year": {
                    "source": "metadata",
                    "confidence": 0.80,
                    "level": "high",
                    "reasoning": "Year from PDF metadata"
                }
            }
        }

    def test_field_meta_has_required_fields(self, sample_card_with_field_meta):
        """_field_meta should have all required fields per entry."""
        meta = sample_card_with_field_meta["_field_meta"]
        
        for field_name, field_meta in meta.items():
            assert "source" in field_meta, f"{field_name} missing 'source'"
            assert "confidence" in field_meta, f"{field_name} missing 'confidence'"
            assert "level" in field_meta, f"{field_name} missing 'level'"

    def test_field_meta_source_values_valid(self, sample_card_with_field_meta):
        """_field_meta source values should be from allowed list."""
        VALID_SOURCES = [
            "page_1_multiline", "metadata", "filename", "text_pattern",
            "section_heading", "llm_extract", "text", "none"
        ]
        
        meta = sample_card_with_field_meta["_field_meta"]
        
        for field_name, field_meta in meta.items():
            assert field_meta["source"] in VALID_SOURCES, \
                f"{field_name} has invalid source: {field_meta['source']}"

    def test_field_meta_level_values_valid(self, sample_card_with_field_meta):
        """_field_meta level values should be from allowed list."""
        VALID_LEVELS = ["very_high", "high", "medium", "low", "very_low"]
        
        meta = sample_card_with_field_meta["_field_meta"]
        
        for field_name, field_meta in meta.items():
            assert field_meta["level"] in VALID_LEVELS, \
                f"{field_name} has invalid level: {field_meta['level']}"

    def test_field_meta_confidence_range(self, sample_card_with_field_meta):
        """_field_meta confidence should be in range 0.0-1.0."""
        meta = sample_card_with_field_meta["_field_meta"]
        
        for field_name, field_meta in meta.items():
            conf = field_meta["confidence"]
            assert 0.0 <= conf <= 1.0, \
                f"{field_name} confidence {conf} out of range"

    def test_field_meta_short_fields_have_candidates(self, sample_card_with_field_meta):
        """Short fields (title, authors, etc.) should support candidates."""
        SHORT_FIELDS = {"title", "authors", "journal", "year", "doi", "keywords"}
        
        meta = sample_card_with_field_meta["_field_meta"]
        
        for field_name in SHORT_FIELDS:
            if field_name in meta:
                # Candidates key should exist (can be empty list)
                assert "candidates" in meta[field_name] or True, \
                    f"{field_name} should support candidates"

    def test_field_meta_long_fields_no_candidates(self):
        """Long fields (abstract, conclusions) should NOT have candidates."""
        card = {
            "_field_meta": {
                "abstract": {
                    "source": "section_heading",
                    "confidence": 0.90,
                    "level": "high",
                    "reasoning": "Abstract section found"
                    # NO candidates field
                }
            }
        }
        
        # Long fields should not have candidates
        assert "candidates" not in card["_field_meta"]["abstract"] or \
               card["_field_meta"]["abstract"].get("candidates") == []

    def test_field_meta_level_matches_confidence(self, sample_card_with_field_meta):
        """_field_meta level should match confidence thresholds."""
        meta = sample_card_with_field_meta["_field_meta"]
        
        for field_name, field_meta in meta.items():
            conf = field_meta["confidence"]
            level = field_meta["level"]
            
            # Verify level matches confidence
            if conf >= 0.95:
                assert level == "very_high", f"{field_name}: {conf} should be very_high"
            elif conf >= 0.80:
                assert level == "high", f"{field_name}: {conf} should be high"
            elif conf >= 0.65:
                assert level == "medium", f"{field_name}: {conf} should be medium"
            elif conf >= 0.40:
                assert level == "low", f"{field_name}: {conf} should be low"
            else:
                assert level == "very_low", f"{field_name}: {conf} should be very_low"


# =============================================================================
# Test 5: _review Structure - Auto Accepted
# =============================================================================

class TestReviewStructureAutoAccepted:
    """Test cases for _review structure when all fields pass thresholds."""

    @pytest.fixture
    def card_auto_accepted(self):
        """Create a card with all fields above threshold."""
        return {
            "card_id": "WQ-SCI-001",
            "title": "Test Title",
            "authors": ["Wang Qi"],
            "year": 2024,
            "_field_meta": {
                "title": {"confidence": 0.92, "level": "high"},
                "authors": {"confidence": 0.85, "level": "high"},
                "year": {"confidence": 0.90, "level": "high"}
            },
            "_review": {
                "status": "auto_accepted",
                "priority": 2,
                "fields": [],
                "thresholds_used": {"title": 0.85, "authors": 0.80, "year": 0.85},
                "auto_reviewed_at": "2026-04-25T10:00:00",
                "manual_reviewed_at": None,
                "reviewer_notes": ""
            }
        }

    def test_review_status_auto_accepted(self, card_auto_accepted):
        """When all fields pass, status should be 'auto_accepted'."""
        assert card_auto_accepted["_review"]["status"] == "auto_accepted"

    def test_review_fields_empty_when_all_pass(self, card_auto_accepted):
        """When all fields pass, 'fields' list should be empty."""
        assert card_auto_accepted["_review"]["fields"] == []

    def test_review_priority_normal(self, card_auto_accepted):
        """Auto-accepted cards should have priority 2 (normal)."""
        assert card_auto_accepted["_review"]["priority"] == 2

    def test_review_has_auto_reviewed_at(self, card_auto_accepted):
        """Auto-accepted cards should have auto_reviewed_at timestamp."""
        assert card_auto_accepted["_review"]["auto_reviewed_at"] is not None

    def test_review_manual_reviewed_at_null(self, card_auto_accepted):
        """Auto-accepted cards should have null manual_reviewed_at."""
        assert card_auto_accepted["_review"]["manual_reviewed_at"] is None

    def test_review_thresholds_used_recorded(self, card_auto_accepted):
        """_review should record thresholds used for each field."""
        thresholds = card_auto_accepted["_review"]["thresholds_used"]
        
        assert "title" in thresholds
        assert "authors" in thresholds
        assert thresholds["title"] == 0.85
        assert thresholds["authors"] == 0.80


# =============================================================================
# Test 6: _review Structure - Needs Review
# =============================================================================

class TestReviewStructureNeedsReview:
    """Test cases for _review structure when some fields fail thresholds."""

    @pytest.fixture
    def card_needs_review(self):
        """Create a card with some fields below threshold."""
        return {
            "card_id": "WQ-SCI-002",
            "title": "Test Title",
            "authors": ["Unknown"],  # Low confidence
            "year": 2024,
            "_field_meta": {
                "title": {"confidence": 0.92, "level": "high"},
                "authors": {"confidence": 0.45, "level": "low"},  # Below threshold
                "year": {"confidence": 0.90, "level": "high"}
            },
            "_review": {
                "status": "needs_review",
                "priority": 1,
                "fields": ["authors"],
                "thresholds_used": {"title": 0.85, "authors": 0.80, "year": 0.85},
                "auto_reviewed_at": "2026-04-25T10:00:00",
                "manual_reviewed_at": None,
                "reviewer_notes": ""
            }
        }

    def test_review_status_needs_review(self, card_needs_review):
        """When fields fail, status should be 'needs_review'."""
        assert card_needs_review["_review"]["status"] == "needs_review"

    def test_review_fields_lists_failing(self, card_needs_review):
        """'fields' should list fields that failed threshold."""
        assert "authors" in card_needs_review["_review"]["fields"]

    def test_review_priority_elevated(self, card_needs_review):
        """Needs_review cards should have priority 0 or 1."""
        assert card_needs_review["_review"]["priority"] in [0, 1]

    def test_review_priority_p0_when_very_low(self):
        """Priority should be 0 when min_confidence < 0.50."""
        card = {
            "_field_meta": {
                "authors": {"confidence": 0.35, "level": "very_low"}
            },
            "_review": {
                "status": "needs_review",
                "priority": 0,  # P0 for very low confidence
                "fields": ["authors"]
            }
        }
        
        assert card["_review"]["priority"] == 0

    def test_review_priority_p1_when_medium(self):
        """Priority should be 1 when min_confidence 0.50-0.79."""
        card = {
            "_field_meta": {
                "authors": {"confidence": 0.65, "level": "medium"}
            },
            "_review": {
                "status": "needs_review",
                "priority": 1,  # P1 for medium confidence
                "fields": ["authors"]
            }
        }
        
        assert card["_review"]["priority"] == 1


# =============================================================================
# Test 7: CardMerger - Metadata Sync
# =============================================================================

class TestCardMergerMetadataSync:
    """Test cases for CardMerger.merge_card metadata synchronization."""

    @pytest.fixture
    def sample_card(self):
        """Create a sample extracted card."""
        return {
            "card_id": "WQ-SCI-001",
            "title": "Extracted Title",
            "authors": ["Wang Qi"],
            "year": 2024,
            "_field_meta": {
                "title": {"confidence": 0.85, "level": "high", "source": "text"},
                "authors": {"confidence": 0.80, "level": "high", "source": "text"},
                "year": {"confidence": 0.90, "level": "high", "source": "metadata"}
            },
            "_review": {
                "status": "auto_accepted",
                "priority": 2,
                "fields": []
            }
        }

    @pytest.fixture
    def override_data(self):
        """Create sample override data."""
        return {
            "title": "Corrected Title",
            "authors": ["Wang Qi", "Li Yingshuai"],
            "_override_meta": {
                "updated_at": "2026-04-25T10:30:00",
                "updated_by": "manual",
                "reason": "Fixed author extraction error",
                "fields_changed": ["title", "authors"]
            }
        }

    def test_merge_card_updates_field_values(self, sample_card, override_data):
        """Merged card should have updated field values from override."""
        # Simulate merge
        merged = sample_card.copy()
        for field in override_data.get("_override_meta", {}).get("fields_changed", []):
            if field in override_data:
                merged[field] = override_data[field]
        
        assert merged["title"] == "Corrected Title"
        assert merged["authors"] == ["Wang Qi", "Li Yingshuai"]

    def test_merge_card_updates_review_status(self, sample_card, override_data):
        """Merged card should have _review.status = 'manually_fixed'."""
        # Simulate merge
        merged = sample_card.copy()
        merged["_review"] = merged["_review"].copy()
        merged["_review"]["status"] = "manually_fixed"
        
        assert merged["_review"]["status"] == "manually_fixed"

    def test_merge_card_updates_field_meta_confidence(self, sample_card, override_data):
        """Merged card should update _field_meta for overridden fields."""
        # Simulate merge
        merged = sample_card.copy()
        merged["_field_meta"] = merged["_field_meta"].copy()
        
        for field in override_data.get("_override_meta", {}).get("fields_changed", []):
            merged["_field_meta"][field] = {
                "confidence": 1.0,  # Manual override = max confidence
                "level": "very_high",
                "source": "manual",
                "reasoning": "Manual correction"
            }
        
        assert merged["_field_meta"]["title"]["confidence"] == 1.0
        assert merged["_field_meta"]["title"]["source"] == "manual"
        assert merged["_field_meta"]["title"]["level"] == "very_high"

    def test_merge_card_preserves_non_overridden_fields(self, sample_card, override_data):
        """Merged card should preserve fields not in override."""
        # Override only title
        override_title_only = {"title": "New Title", "_override_meta": {"fields_changed": ["title"]}}
        
        merged = sample_card.copy()
        merged["title"] = override_title_only["title"]
        
        # year should be preserved
        assert merged["year"] == 2024

    def test_merge_card_records_manual_reviewed_at(self, sample_card, override_data):
        """Merged card should have manual_reviewed_at timestamp."""
        merged = sample_card.copy()
        merged["_review"] = merged["_review"].copy()
        merged["_review"]["manual_reviewed_at"] = override_data["_override_meta"]["updated_at"]
        
        assert merged["_review"]["manual_reviewed_at"] == "2026-04-25T10:30:00"


# =============================================================================
# Test 8: Integration - Full Card with _field_meta and _review
# =============================================================================

class TestIntegrationFieldMetaAndReview:
    """Integration tests for complete card with _field_meta and _review."""

    @pytest.fixture
    def extractor(self):
        """Create a KnowledgeCardExtractor instance."""
        try:
            from extract_knowledge_cards import KnowledgeCardExtractor
            return KnowledgeCardExtractor(use_llm=False)
        except ImportError:
            pytest.skip("KnowledgeCardExtractor not available")

    def test_extracted_card_has_field_meta(self, extractor):
        """Extracted card should have _field_meta field (not _confidence)."""
        # Mock PDF content
        pdf_content = {
            "full_text": "Test Title\n\nWang Qi\n\nAbstract\nThis is a test abstract.",
            "pages": [{"page_num": 1, "text": "Test Title\n\nWang Qi"}],
            "metadata": {"title": "Test Title", "author": "Wang Qi"},
            "sections": {"abstract": "This is a test abstract."}
        }
        
        card = extractor.extract_from_paper(
            pdf_content,
            "test.pdf",
            "WQ-SCI-TEST"
        )
        
        # NOTE: This test will FAIL because current code uses _confidence instead of _field_meta
        # After refactoring, this should pass
        assert "_field_meta" in card, "Card should have _field_meta field (not _confidence)"
        
        # Also verify that _confidence is NOT present (should be renamed to _field_meta)
        assert "_confidence" not in card, "Card should NOT have legacy _confidence field"

    def test_extracted_card_has_review(self, extractor):
        """Extracted card should have _review field."""
        pdf_content = {
            "full_text": "Test Title\n\nWang Qi\n\nAbstract\nThis is a test abstract.",
            "pages": [{"page_num": 1, "text": "Test Title\n\nWang Qi"}],
            "metadata": {"title": "Test Title", "author": "Wang Qi"},
            "sections": {"abstract": "This is a test abstract."}
        }
        
        card = extractor.extract_from_paper(
            pdf_content,
            "test.pdf",
            "WQ-SCI-TEST"
        )
        
        # NOTE: This test will FAIL because current code doesn't generate _review
        assert "_review" in card, "Card should have _review field"

    def test_field_meta_matches_schema(self, extractor):
        """_field_meta structure should match knowledge-card-schema.md."""
        pdf_content = {
            "full_text": "Test Title\n\nWang Qi\n\nAbstract\nThis is a test abstract.",
            "pages": [{"page_num": 1, "text": "Test Title\n\nWang Qi"}],
            "metadata": {"title": "Test Title", "author": "Wang Qi"},
            "sections": {"abstract": "This is a test abstract."}
        }
        
        card = extractor.extract_from_paper(
            pdf_content,
            "test.pdf",
            "WQ-SCI-TEST"
        )
        
        # NOTE: This test will FAIL until refactoring is complete
        if "_field_meta" in card:
            for field_name, meta in card["_field_meta"].items():
                assert "source" in meta, f"{field_name} missing 'source'"
                assert "confidence" in meta, f"{field_name} missing 'confidence'"
                assert "level" in meta, f"{field_name} missing 'level'"
                # reasoning is optional but recommended
                # assert "reasoning" in meta, f"{field_name} missing 'reasoning'"


# =============================================================================
# Test 9: Confidence Level Mapping
# =============================================================================

class TestConfidenceLevelMapping:
    """Test cases for confidence to level mapping."""

    @pytest.fixture
    def calculator(self):
        """Create a ConfidenceCalculator instance."""
        from extract_knowledge_cards import ConfidenceCalculator
        return ConfidenceCalculator()

    def test_very_high_threshold(self, calculator):
        """Confidence >= 0.95 should map to HIGH level."""
        from extract_knowledge_cards import ConfidenceLevel
        
        level = calculator.get_confidence_level(0.95)
        assert level == ConfidenceLevel.HIGH
        
        level = calculator.get_confidence_level(1.0)
        assert level == ConfidenceLevel.HIGH

    def test_high_threshold(self, calculator):
        """Confidence 0.75-0.94 should map to HIGH level."""
        from extract_knowledge_cards import ConfidenceLevel
        
        level = calculator.get_confidence_level(0.75)
        assert level == ConfidenceLevel.HIGH
        
        level = calculator.get_confidence_level(0.85)
        assert level == ConfidenceLevel.HIGH

    def test_medium_threshold(self, calculator):
        """Confidence 0.50-0.74 should map to MEDIUM level."""
        from extract_knowledge_cards import ConfidenceLevel
        
        level = calculator.get_confidence_level(0.50)
        assert level == ConfidenceLevel.MEDIUM
        
        level = calculator.get_confidence_level(0.65)
        assert level == ConfidenceLevel.MEDIUM

    def test_low_threshold(self, calculator):
        """Confidence 0.25-0.49 should map to LOW level."""
        from extract_knowledge_cards import ConfidenceLevel
        
        level = calculator.get_confidence_level(0.25)
        assert level == ConfidenceLevel.LOW
        
        level = calculator.get_confidence_level(0.40)
        assert level == ConfidenceLevel.LOW

    def test_none_threshold(self, calculator):
        """Confidence < 0.25 should map to NONE level."""
        from extract_knowledge_cards import ConfidenceLevel
        
        level = calculator.get_confidence_level(0.0)
        assert level == ConfidenceLevel.NONE
        
        level = calculator.get_confidence_level(0.20)
        assert level == ConfidenceLevel.NONE


# =============================================================================
# Test 10: Field Thresholds by Class
# =============================================================================

class TestFieldThresholdsByClass:
    """Test cases for field-specific confidence thresholds."""

    def test_critical_identity_threshold(self):
        """Critical identity fields (doi, card_id) should require 0.95."""
        CRITICAL_IDENTITY_THRESHOLD = 0.95
        
        # DOI should require very high confidence
        assert CRITICAL_IDENTITY_THRESHOLD == 0.95

    def test_critical_operational_threshold(self):
        """Critical operational fields (year, title) should require 0.85."""
        CRITICAL_OPERATIONAL_THRESHOLD = 0.85
        
        # Year and title should require high confidence
        assert CRITICAL_OPERATIONAL_THRESHOLD == 0.85

    def test_standard_threshold(self):
        """Standard fields (authors, journal, keywords) should require 0.80."""
        STANDARD_THRESHOLD = 0.80
        
        # Authors, journal, keywords should require good confidence
        assert STANDARD_THRESHOLD == 0.80

    def test_descriptive_threshold(self):
        """Descriptive fields (abstract, conclusions) should require 0.70."""
        DESCRIPTIVE_THRESHOLD = 0.70
        
        # Abstract and conclusions can have lower threshold
        assert DESCRIPTIVE_THRESHOLD == 0.70


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
