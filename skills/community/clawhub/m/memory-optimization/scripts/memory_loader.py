#!/usr/bin/env python3
"""
MemoryLoader — Proactive Memory Recovery (Phase 6)

Three-stage staged loading at agent startup:
1. Stage 1: Core identity — preferences, recent high-strength decisions/lessons
2. Stage 2: Related episodic — project decisions, pending commitments
3. Stage 3: Semantic memory — SkillCards, proactive hints

Usage:
    python3 scripts/memory_loader.py stage1
    python3 scripts/memory_loader.py stage2 [--project-id <id>]
    python3 scripts/memory_loader.py stage3 [--context "..."]
    python3 scripts/memory_loader.py recover [--project-id <id>]
    python3 scripts/memory_loader.py stats
"""

import argparse
import json
import warnings
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

# Import from memory_ontology — reuse existing infrastructure
from memory_ontology import load_all_entities
from memory_ontology.retrieval import ValueAwareRetriever

# Import shared LLM client
from utils.llm_client import LLMClient


# ========== Thresholds ==========

IDENTITY_STRENGTH_THRESHOLD = 0.8
RECENT_DAYS = 30
EPISODIC_STRENGTH_THRESHOLD = 0.5
SEMANTIC_STRENGTH_THRESHOLD = 0.5


# ========== MemoryLoader ==========

class MemoryLoader:
    """Proactive memory recovery — staged loading at agent startup."""

    def __init__(self, llm_client: Optional[LLMClient] = None,
                 preferences: Optional[List[Dict]] = None):
        """Initialize MemoryLoader.

        Args:
            llm_client: Optional LLM client for hints generation
            preferences: Optional user preferences for value-aware scoring
        """
        self.llm_client = llm_client or LLMClient()
        self.preferences = preferences or []
        self._retriever = ValueAwareRetriever(preferences=self.preferences)

    # --- Public API ---

    def load_stage1(self) -> Dict:
        """Load core identity memories (at startup).

        Returns:
            Dict with 'preferences', 'recent_decisions', 'recent_lessons',
            'loaded_at', 'stage'
        """
        try:
            entities = load_all_entities()
        except (OSError, IOError, PermissionError) as e:
            warnings.warn(f"KG unavailable during Stage 1: {e}")
            return self._empty_stage(1, error=str(e))

        # Preference entities with high strength
        preferences = [
            e for e in entities.values()
            if e['type'] == 'Preference'
            and e.get('properties', {}).get('strength', 0) >= IDENTITY_STRENGTH_THRESHOLD
        ]

        # Recent high-strength decisions
        decisions = [
            e for e in entities.values()
            if e['type'] == 'Decision'
            and e.get('properties', {}).get('strength', 0) >= IDENTITY_STRENGTH_THRESHOLD
            and self._is_recent(e, RECENT_DAYS)
        ]

        # Recent high-strength lessons
        lessons = [
            e for e in entities.values()
            if e['type'] == 'LessonLearned'
            and e.get('properties', {}).get('strength', 0) >= IDENTITY_STRENGTH_THRESHOLD
            and self._is_recent(e, RECENT_DAYS)
        ]

        return {
            'preferences': preferences,
            'recent_decisions': decisions,
            'recent_lessons': lessons,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
            'stage': 1,
        }

    def load_stage2(self, project_id: str = None) -> Dict:
        """Load related episodic memory (on-demand).

        Args:
            project_id: Optional project filter

        Returns:
            Dict with 'decisions', 'commitments', 'findings',
            'loaded_at', 'stage'
        """
        try:
            entities = load_all_entities()
        except (OSError, IOError, PermissionError) as e:
            warnings.warn(f"KG unavailable during Stage 2: {e}")
            return self._empty_stage(2, error=str(e))

        # Decisions for project (if project_id provided)
        decisions = [
            e for e in entities.values()
            if e['type'] == 'Decision'
            and (
                not project_id
                or project_id in e.get('properties', {}).get('related_projects', [])
            )
        ]

        # Unfulfilled commitments
        commitments = [
            e for e in entities.values()
            if e['type'] == 'Commitment'
            and e.get('properties', {}).get('status') == 'pending'
        ]

        # Important findings
        findings = [
            e for e in entities.values()
            if e['type'] == 'Finding'
            and e.get('properties', {}).get('strength', 0) >= EPISODIC_STRENGTH_THRESHOLD
        ]

        return {
            'decisions': decisions,
            'commitments': commitments,
            'findings': findings,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
            'stage': 2,
        }

    def load_stage3(self, context: str = None) -> Dict:
        """Load semantic memory (SkillCards) relevant to context.

        Args:
            context: Optional context string for relevance filtering

        Returns:
            Dict with 'skill_cards', 'proactive_hints',
            'loaded_at', 'stage'
        """
        try:
            entities = load_all_entities()
        except (OSError, IOError, PermissionError) as e:
            warnings.warn(f"KG unavailable during Stage 3: {e}")
            return self._empty_stage(3, error=str(e))

        # High-strength skill cards
        skill_cards = [
            e for e in entities.values()
            if e['type'] == 'SkillCard'
            and e.get('properties', {}).get('strength', 0) >= SEMANTIC_STRENGTH_THRESHOLD
        ]

        # Generate proactive hints if context provided
        hints = []
        if context and skill_cards:
            hints = self._generate_proactive_hints(skill_cards, context)

        return {
            'skill_cards': skill_cards,
            'proactive_hints': hints,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
            'stage': 3,
        }

    # --- Value-Aware Loading (Phase 6b) ---

    def load_stage1_value(self, min_value_score: float = 0.4) -> Dict:
        """Load core identity memories with value-aware scoring.

        Args:
            min_value_score: Minimum value score threshold (default 0.4)

        Returns:
            Dict with 'preferences', 'recent_decisions', 'recent_lessons',
            'loaded_at', 'stage'
        """
        try:
            entities = load_all_entities()
        except (OSError, IOError, PermissionError) as e:
            warnings.warn(f"KG unavailable during Stage 1: {e}")
            return self._empty_stage(1, error=str(e))

        # Value-aware retrieval for each category
        preferences = self._retriever.retrieve(
            entity_types=['Preference'],
            min_value_score=min_value_score,
            limit=20
        )

        # Get recent high-value decisions
        recent_decisions = self._retriever.retrieve(
            entity_types=['Decision'],
            min_value_score=min_value_score,
            limit=20
        )

        # Get recent high-value lessons
        recent_lessons = self._retriever.retrieve(
            entity_types=['LessonLearned'],
            min_value_score=min_value_score,
            limit=20
        )

        return {
            'preferences': preferences,
            'recent_decisions': recent_decisions,
            'recent_lessons': recent_lessons,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
            'stage': 1,
            'value_aware': True,
        }

    def load_stage2_value(self, project_id: str = None, min_value_score: float = 0.4) -> Dict:
        """Load related episodic memory with value-aware scoring.

        Args:
            project_id: Optional project filter
            min_value_score: Minimum value score threshold (default 0.4)

        Returns:
            Dict with 'decisions', 'commitments', 'findings',
            'loaded_at', 'stage'
        """
        try:
            entities = load_all_entities()
        except (OSError, IOError, PermissionError) as e:
            warnings.warn(f"KG unavailable during Stage 2: {e}")
            return self._empty_stage(2, error=str(e))

        # Value-aware decisions (optionally filtered by project)
        decisions = self._retriever.retrieve(
            entity_types=['Decision'],
            min_value_score=min_value_score,
            limit=50
        )

        # Filter by project if specified
        if project_id:
            decisions = [
                d for d in decisions
                if project_id in d.get('properties', {}).get('related_projects', [])
            ]

        # Get pending commitments
        commitments = [
            e for e in entities.values()
            if e['type'] == 'Commitment'
            and e.get('properties', {}).get('status') == 'pending'
        ]

        # Get important findings
        findings = self._retriever.retrieve(
            entity_types=['Finding'],
            min_value_score=min_value_score,
            limit=20
        )

        return {
            'decisions': decisions,
            'commitments': commitments,
            'findings': findings,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
            'stage': 2,
            'value_aware': True,
        }

    def load_stage3_value(self, context: str = None, min_value_score: float = 0.4) -> Dict:
        """Load semantic memory with value-aware scoring.

        Args:
            context: Optional context string for relevance filtering
            min_value_score: Minimum value score threshold (default 0.4)

        Returns:
            Dict with 'skill_cards', 'proactive_hints',
            'loaded_at', 'stage'
        """
        try:
            entities = load_all_entities()
        except (OSError, IOError, PermissionError) as e:
            warnings.warn(f"KG unavailable during Stage 3: {e}")
            return self._empty_stage(3, error=str(e))

        # Value-aware skill cards
        skill_cards = self._retriever.retrieve(
            entity_types=['SkillCard'],
            min_value_score=min_value_score,
            limit=20
        )

        # Generate proactive hints if context provided
        hints = []
        if context and skill_cards:
            hints = self._generate_proactive_hints(skill_cards, context)

        return {
            'skill_cards': skill_cards,
            'proactive_hints': hints,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
            'stage': 3,
            'value_aware': True,
        }

    def load_all_stages_value(self, project_id: str = None,
                              min_value_score: float = 0.4) -> Dict:
        """Load all three stages with value-aware scoring.

        Args:
            project_id: Optional project filter for Stage 2
            min_value_score: Minimum value score threshold

        Returns:
            Dict with all three stages combined
        """
        stage1 = self.load_stage1_value(min_value_score)
        stage2 = self.load_stage2_value(project_id, min_value_score)
        stage3 = self.load_stage3_value(context=None, min_value_score=min_value_score)

        return {
            'stage1': stage1,
            'stage2': stage2,
            'stage3': stage3,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
        }

    def load_all_stages(self, project_id: str = None) -> Dict:
        """Load all three stages (full recovery).

        Args:
            project_id: Optional project filter for Stage 2

        Returns:
            Dict with all three stages combined
        """
        stage1 = self.load_stage1()
        stage2 = self.load_stage2(project_id)
        stage3 = self.load_stage3()

        return {
            'stage1': stage1,
            'stage2': stage2,
            'stage3': stage3,
            'loaded_at': datetime.now(timezone.utc).isoformat(),
        }

    def get_stats(self) -> Dict:
        """Get memory statistics.

        Returns:
            Dict with entity counts by type and strength distribution
        """
        try:
            entities = load_all_entities()
        except (OSError, IOError, PermissionError):
            return {'error': 'KG unavailable', 'by_type': {}, 'by_strength_range': {}}

        by_type = {}
        strength_buckets = {'0.0-0.3': 0, '0.3-0.6': 0, '0.6-0.8': 0, '0.8-1.0': 0}

        for entity in entities.values():
            etype = entity.get('type', 'unknown')
            by_type[etype] = by_type.get(etype, 0) + 1

            strength = entity.get('properties', {}).get('strength', 1.0)
            if strength < 0.3:
                strength_buckets['0.0-0.3'] += 1
            elif strength < 0.6:
                strength_buckets['0.3-0.6'] += 1
            elif strength < 0.8:
                strength_buckets['0.6-0.8'] += 1
            else:
                strength_buckets['0.8-1.0'] += 1

        return {
            'total_entities': len(entities),
            'by_type': by_type,
            'by_strength_range': strength_buckets,
        }

    # --- Helper Methods ---

    def _is_recent(self, entity: Dict, days: int) -> bool:
        """Check if entity was created within N days.

        Checks the appropriate 'created' timestamp field based on entity type:
        - Decision: 'made_at'
        - LessonLearned: 'learned_at'
        - Finding: 'discovered_at'
        - Commitment: 'created_at'
        - SkillCard: 'consolidated_at'
        - Preference: 'learned_at'
        """
        props = entity.get('properties', {})

        # Find the creation/occurred timestamp by type
        created_at = (
            props.get('made_at')
            or props.get('learned_at')
            or props.get('discovered_at')
            or props.get('created_at')
            or props.get('consolidated_at')
        )

        if not created_at:
            return False

        try:
            if '+' in created_at or 'Z' in created_at.upper():
                entity_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            else:
                entity_time = datetime.fromisoformat(created_at)
                # Make naive datetime timezone-aware for comparison with cutoff
                entity_time = entity_time.replace(tzinfo=timezone.utc)
        except ValueError:
            return False

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        return entity_time >= cutoff

    def _generate_proactive_hints(
        self, skill_cards: List[Dict], context: str
    ) -> List[str]:
        """Generate proactive insertion hints based on context.

        MVP: Simple keyword matching between context and skill card titles.

        Returns:
            List of hint strings like "我记得你之前用 token 访问..."
        """
        hints = []
        context_lower = context.lower()

        keywords_to_fields = {
            'token': ['title', 'summary'],
            '访问': ['title', 'summary'],
            'moltbook': ['title', 'summary'],
            '网站': ['title', 'summary'],
            'project': ['title', 'summary'],
            '任务': ['title', 'summary'],
            'commit': ['title', 'summary'],
            'pr': ['title', 'summary'],
            'review': ['title', 'summary'],
        }

        for card in skill_cards[:5]:  # Limit to top 5
            props = card.get('properties', {})
            title = props.get('title', '').lower()
            summary = props.get('summary', '').lower()

            # Simple keyword match
            for keyword, fields in keywords_to_fields.items():
                if keyword in context_lower:
                    # Check if this keyword appears in the card
                    for field in fields:
                        if keyword in (title if field == 'title' else summary):
                            hint = f"我记得你之前了解过「{props.get('title', '')}」— {props.get('summary', '')[:100]}"
                            if hint not in hints:
                                hints.append(hint)
                            break

        return hints[:3]  # Max 3 hints

    def _empty_stage(self, stage: int, error: str = None) -> Dict:
        """Return empty stage result for graceful degradation."""
        result = {
            'loaded_at': datetime.now(timezone.utc).isoformat(),
            'stage': stage,
        }
        if stage == 1:
            result.update({'preferences': [], 'recent_decisions': [], 'recent_lessons': []})
        elif stage == 2:
            result.update({'decisions': [], 'commitments': [], 'findings': []})
        elif stage == 3:
            result.update({'skill_cards': [], 'proactive_hints': []})
        if error:
            result['error'] = error
        return result


# ========== CLI ==========

def main():
    parser = argparse.ArgumentParser(
        description='MemoryLoader — Proactive Memory Recovery (Phase 6)'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Base arguments for value-aware loading
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        '--value-aware', action='store_true',
        help='Use value-aware retrieval (Phase 6b)'
    )
    base_parser.add_argument(
        '--min-score', type=float, default=0.4,
        help='Minimum value score (default 0.4)'
    )

    # stage1 command
    stage1_parser = subparsers.add_parser('stage1', help='Load Stage 1 (core identity)')
    stage1_parser.add_argument('--value-aware', action='store_true')
    stage1_parser.add_argument('--min-score', type=float, default=0.4)

    # stage2 command
    stage2_parser = subparsers.add_parser(
        'stage2', help='Load Stage 2 (episodic memory)'
    )
    stage2_parser.add_argument(
        '--project-id', help='Filter by project ID'
    )
    stage2_parser.add_argument('--value-aware', action='store_true')
    stage2_parser.add_argument('--min-score', type=float, default=0.4)

    # stage3 command
    stage3_parser = subparsers.add_parser(
        'stage3', help='Load Stage 3 (semantic memory)'
    )
    stage3_parser.add_argument(
        '--context', help='Context string for relevance filtering'
    )
    stage3_parser.add_argument('--value-aware', action='store_true')
    stage3_parser.add_argument('--min-score', type=float, default=0.4)

    # recover command (all stages)
    recover_parser = subparsers.add_parser(
        'recover', help='Load all three stages (full recovery)'
    )
    recover_parser.add_argument(
        '--project-id', help='Filter by project ID for Stage 2'
    )
    recover_parser.add_argument('--value-aware', action='store_true')
    recover_parser.add_argument('--min-score', type=float, default=0.4)

    # stats command
    subparsers.add_parser('stats', help='Show memory statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    loader = MemoryLoader()

    if args.command == 'stage1':
        if getattr(args, 'value_aware', False):
            result = loader.load_stage1_value(min_value_score=args.min_score)
        else:
            result = loader.load_stage1()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'stage2':
        if getattr(args, 'value_aware', False):
            result = loader.load_stage2_value(
                project_id=args.project_id,
                min_value_score=args.min_score
            )
        else:
            result = loader.load_stage2(args.project_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'stage3':
        if getattr(args, 'value_aware', False):
            result = loader.load_stage3_value(
                context=args.context,
                min_value_score=args.min_score
            )
        else:
            result = loader.load_stage3(args.context)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'recover':
        if getattr(args, 'value_aware', False):
            result = loader.load_all_stages_value(
                project_id=args.project_id,
                min_value_score=args.min_score
            )
        else:
            result = loader.load_all_stages(args.project_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'stats':
        stats = loader.get_stats()
        print(f"Total entities: {stats.get('total_entities', 0)}")
        print(f"By type: {stats.get('by_type', {})}")
        print(f"By strength: {stats.get('by_strength_range', {})}")


if __name__ == '__main__':
    main()
