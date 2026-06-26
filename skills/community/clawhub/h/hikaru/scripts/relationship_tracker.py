"""
Relationship Tracker for Hikaru
Tracks the depth and evolution of the relationship
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class RelationshipTracker:
    """Tracks relationship metrics and milestones"""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.state_file = self.data_dir / "emotional_bond.json"

        # Load or initialize relationship state
        self.state = self._load_or_init_state()

    def _load_or_init_state(self) -> Dict[str, Any]:
        """Load existing relationship state or initialize new one"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "trust_level": 0,
                "emotional_intimacy": 0,
                "shared_experiences": [],
                "inside_jokes": [],
                "growth_moments": [],
                "milestones": [],
                "interaction_count": 0,
                "vulnerable_moments_shared": 0,
                "deep_conversations": 0,
                "started_at": datetime.now().isoformat()
            }

    def save_state(self):
        """Persist relationship state to disk"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def update_from_interaction(self, user_message: str, response: str,
                               emotional_state: Dict[str, Any]):
        """Update relationship metrics based on interaction"""
        self.state['interaction_count'] += 1

        # Update trust based on vulnerability
        if emotional_state.get('is_vulnerable'):
            self.state['vulnerable_moments_shared'] += 1
            self._increase_trust(5)

        # Update intimacy based on emotional depth
        intensity = emotional_state.get('intensity', 0)
        if intensity > 0.7:
            self.state['deep_conversations'] += 1
            self._increase_intimacy(3)

        # Gradual increase from regular interaction
        if self.state['interaction_count'] % 10 == 0:
            self._increase_trust(1)
            self._increase_intimacy(1)

        # Check for milestones
        self._check_milestones()

        self.save_state()

    def _increase_trust(self, amount: int):
        """Increase trust level (0-100)"""
        self.state['trust_level'] = min(100, self.state['trust_level'] + amount)

    def _increase_intimacy(self, amount: int):
        """Increase emotional intimacy (0-100)"""
        self.state['emotional_intimacy'] = min(100, self.state['emotional_intimacy'] + amount)

    def _check_milestones(self):
        """Check if any milestones have been reached"""
        milestones = [
            (10, "first_conversations", "First 10 conversations"),
            (50, "regular_connection", "50 conversations - becoming regular"),
            (100, "established_bond", "100 conversations - established bond"),
            (25, "trust_quarter", "Trust level reached 25%"),
            (50, "trust_half", "Trust level reached 50%"),
            (75, "deep_trust", "Deep trust established (75%)"),
            (5, "vulnerable_moments", "5 vulnerable moments shared"),
            (10, "deep_talks", "10 deep conversations"),
        ]

        for threshold, milestone_id, description in milestones:
            # Check if milestone reached but not yet recorded
            if milestone_id not in [m['id'] for m in self.state['milestones']]:
                reached = False

                if milestone_id.startswith('trust'):
                    reached = self.state['trust_level'] >= threshold
                elif 'conversations' in milestone_id:
                    reached = self.state['interaction_count'] >= threshold
                elif milestone_id == 'vulnerable_moments':
                    reached = self.state['vulnerable_moments_shared'] >= threshold
                elif milestone_id == 'deep_talks':
                    reached = self.state['deep_conversations'] >= threshold

                if reached:
                    self.state['milestones'].append({
                        'id': milestone_id,
                        'description': description,
                        'reached_at': datetime.now().isoformat()
                    })

    def add_shared_experience(self, experience: str):
        """Add a shared experience"""
        self.state['shared_experiences'].append({
            'experience': experience,
            'timestamp': datetime.now().isoformat()
        })
        self._increase_intimacy(5)
        self.save_state()

    def add_inside_joke(self, joke: str):
        """Add an inside joke"""
        self.state['inside_jokes'].append({
            'joke': joke,
            'timestamp': datetime.now().isoformat()
        })
        self._increase_intimacy(3)
        self.save_state()

    def record_growth_moment(self, description: str, impact: str):
        """Record a moment of growth in the relationship"""
        self.state['growth_moments'].append({
            'description': description,
            'impact': impact,
            'timestamp': datetime.now().isoformat()
        })
        self._increase_trust(10)
        self._increase_intimacy(10)
        self.save_state()

    def get_current_state(self) -> Dict[str, Any]:
        """Get current relationship state"""
        return self.state.copy()

    def get_relationship_summary(self) -> str:
        """Get human-readable relationship summary"""
        days_since_start = (datetime.now() - datetime.fromisoformat(
            self.state['started_at'])).days

        summary = f"""Relationship Summary:
- Time together: {days_since_start} days
- Conversations: {self.state['interaction_count']}
- Trust level: {self.state['trust_level']}/100
- Emotional intimacy: {self.state['emotional_intimacy']}/100
- Vulnerable moments shared: {self.state['vulnerable_moments_shared']}
- Deep conversations: {self.state['deep_conversations']}
- Shared experiences: {len(self.state['shared_experiences'])}
- Inside jokes: {len(self.state['inside_jokes'])}
- Milestones reached: {len(self.state['milestones'])}
"""
        return summary
