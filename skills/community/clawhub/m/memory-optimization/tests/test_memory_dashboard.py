#!/usr/bin/env python3
"""
Tests for Memory Health Dashboard
"""

import json
import pytest
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))


class TestMemoryDashboardHealthScore:
    """Tests for Health Score computation"""

    def test_health_score_all_strong(self):
        """All strong entities → Grade A"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'strength': 0.9}},
            'e2': {'type': 'Finding', 'properties': {'strength': 0.85}},
        }
        dash._loaded = True

        result = dash.compute_health_score()
        assert result['grade'] == 'A'
        assert result['score'] == 100.0
        assert result['factors']['total'] == 2

    def test_health_score_all_weak(self):
        """All weak entities → Grade F"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'strength': 0.3}},
            'e2': {'type': 'Finding', 'properties': {'strength': 0.2}},
        }
        dash._loaded = True

        result = dash.compute_health_score()
        assert result['grade'] == 'F'
        assert result['factors']['weak'] == 2

    def test_health_score_mixed(self):
        """Mixed strength → Grade B-C range"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'strength': 0.9}},   # strong
            'e2': {'type': 'Finding', 'properties': {'strength': 0.6}},    # medium
            'e3': {'type': 'Decision', 'properties': {'strength': 0.3}},   # weak
        }
        dash._loaded = True

        result = dash.compute_health_score()
        # score = (1/3*1.0 + 1/3*0.5 + 1/3*0.1) * 100 ≈ 53.3
        assert 40 <= result['score'] <= 60
        assert result['factors']['strong'] == 1
        assert result['factors']['medium'] == 1
        assert result['factors']['weak'] == 1

    def test_health_score_empty(self):
        """No entities → Grade F, score 0"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {}
        dash._loaded = True

        result = dash.compute_health_score()
        assert result['grade'] == 'F'
        assert result['score'] == 0


class TestStrengthHistogram:
    """Tests for strength histogram"""

    def test_histogram_buckets(self):
        """Entities placed in correct strength buckets"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'strength': 0.95}},
            'e2': {'type': 'Decision', 'properties': {'strength': 0.45}},
            'e3': {'type': 'Finding', 'properties': {'strength': 0.05}},
        }
        dash._loaded = True

        hist = dash.get_strength_histogram()
        assert hist['avg'] == pytest.approx((0.95 + 0.45 + 0.05) / 3, rel=0.01)
        assert hist['buckets']['90-100'] == 1
        assert hist['buckets']['40-50'] == 1
        assert hist['buckets']['0-10'] == 1


class TestConsolidationProgress:
    """Tests for consolidation progress"""

    def test_counts_skill_cards(self):
        """Correctly counts SkillCard entities"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'sc1': {'type': 'SkillCard', 'properties': {}},
            'sc2': {'type': 'SkillCard', 'properties': {}},
            'dec1': {'type': 'Decision', 'properties': {}},
        }
        dash._loaded = True

        result = dash.get_consolidation_progress()
        assert result['skill_cards'] == 2

    def test_counts_conflict_reviews(self):
        """Correctly counts ConflictReview entities"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'cr1': {'type': 'ConflictReview', 'properties': {}},
            'cr2': {'type': 'ConflictReview', 'properties': {}},
        }
        dash._loaded = True

        result = dash.get_consolidation_progress()
        assert result['conflict_reviews'] == 2


class TestStorageStats:
    """Tests for storage statistics"""

    def test_counts_by_type(self):
        """Correctly counts entities by type"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {}},
            'e2': {'type': 'Decision', 'properties': {}},
            'e3': {'type': 'Finding', 'properties': {}},
        }
        dash._loaded = True

        stats = dash.get_storage_stats()
        assert stats['entity_count'] == 3
        assert stats['by_type']['Decision'] == 2
        assert stats['by_type']['Finding'] == 1


class TestDecayForecast:
    """Tests for decay forecasting"""

    def test_no_risk_when_strong(self):
        """No warnings when entities are strong"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'strength': 0.9, 'decay_rate': 0.95}},
        }
        dash._loaded = True

        warnings = dash.get_decay_forecast()
        assert len(warnings) == 0

    def test_warns_when_will_decay(self):
        """Warns when entity will decay to danger level"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        # Entity with high decay rate will drop below 0.15 in 30 days
        # strength=0.2, decay_rate=0.5 → after 30 days: 0.2 * 0.5 = 0.1 < 0.15
        dash.entities = {
            'e1': {'id': 'dec_001', 'type': 'Decision', 'properties': {
                'title': 'High Decay Entity',
                'strength': 0.2,
                'decay_rate': 0.5
            }},
        }
        dash._loaded = True

        warnings = dash.get_decay_forecast()
        assert len(warnings) == 1
        assert warnings[0]['id'] == 'dec_001'
        assert warnings[0]['current_strength'] == 0.2

    def test_days_to_strength_calculation(self):
        """Correctly calculates days to reach target strength"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()

        # strength=0.5, decay_rate=0.9
        # target=0.15: 0.5 * 0.9^(days/30) = 0.15
        # days = 30 * log(0.15/0.5) / log(0.9) ≈ 343
        days = dash._days_to_strength(0.5, 0.9, 0.15)
        assert days is not None
        assert 330 <= days <= 360

    def test_days_to_strength_wont_decay(self):
        """Returns None when decay_rate >= 1.0"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        days = dash._days_to_strength(0.5, 1.0, 0.15)
        assert days is None


class TestTagCloud:
    """Tests for tag cloud"""

    def test_extracts_tags(self):
        """Correctly extracts and counts tags"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'tags': ['#decision', '#test']}},
            'e2': {'type': 'Decision', 'properties': {'tags': ['#decision']}},
            'e3': {'type': 'Finding', 'properties': {'tags': ['#test']}},
        }
        dash._loaded = True

        tags = dash.get_tag_cloud()
        assert tags['#decision'] == 2
        assert tags['#test'] == 2
        assert len(tags) == 2


class TestAgeDistribution:
    """Tests for age distribution"""

    def test_no_created_field(self):
        """Handles entities without created field"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {}},  # no 'created'
        }
        dash._loaded = True

        ages = dash.get_age_distribution()
        # Entity with no created is skipped, but bucket is 0
        assert sum(ages.values()) == 0


class TestProvenanceBreakdown:
    """Tests for provenance breakdown"""

    def test_normalizes_provenance_keys(self):
        """Normalizes provenance to source type"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {
                'provenance': ['inference:preference_engine', 'session:abc123']
            }},
        }
        dash._loaded = True

        prov = dash.get_provenance_breakdown()
        assert prov['inference'] == 1
        assert prov['session'] == 1


class TestRenderViews:
    """Tests for rendering methods"""

    def test_render_compact(self):
        """Compact view produces single line"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'strength': 0.9}},
        }
        dash._loaded = True

        result = dash.render_compact()
        assert 'Memory Health:' in result
        assert 'A' in result

    def test_render_json(self):
        """JSON view produces valid JSON"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {
            'e1': {'type': 'Decision', 'properties': {'strength': 0.9}},
        }
        dash._loaded = True

        result = dash.render_json()
        data = json.loads(result)
        assert 'health_score' in data
        assert 'storage' in data
        assert 'consolidation' in data


class TestEmptyKG:
    """Tests for empty knowledge graph"""

    def test_health_score_empty_kg(self):
        """Empty KG returns score 0, grade F"""
        from memory_dashboard import MemoryDashboard

        dash = MemoryDashboard()
        dash.entities = {}
        dash._loaded = True

        result = dash.compute_health_score()
        assert result['score'] == 0
        assert result['grade'] == 'F'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
