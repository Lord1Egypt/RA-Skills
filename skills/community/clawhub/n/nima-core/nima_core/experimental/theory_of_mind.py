"""
theory_of_mind.py
Theory of Mind (ToM) module for NIMA.

Implements:
- Mental state attribution to users and other agents
- Perspective taking and simulation
- False belief reasoning
- Recursive mental state modeling ("I think that you think...")
- Belief maintenance and updating with evidence

Author: Lilu (with David's consciousness architecture)
Date: Feb 14, 2026
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
import numpy as np

# Optional imports - may not be available in nima-core yet
try:
    from nima_core.self_narrative import SelfNarrative
except ImportError:
    SelfNarrative = None  # type: ignore

try:
    from nima_core.volition import VolitionEngine
except ImportError:
    VolitionEngine = None  # type: ignore


@dataclass
class MentalState:
    """
    Represents an attributed mental state of an agent.
    
    Based on Belief-Desire-Intention (BDI) model with:
    - Beliefs: What the agent thinks is true
    - Desires: What the agent wants
    - Intentions: What the agent is committed to doing
    - Emotions: Current affective state
    - Knowledge: What the agent actually knows (vs believes)
    """
    agent_id: str
    agent_name: str
    
    # Core BDI components
    beliefs: Dict[str, float] = field(default_factory=dict)  # belief -> confidence
    desires: List[str] = field(default_factory=list)  # goals
    intentions: List[str] = field(default_factory=list)  # committed actions
    
    # Extended mental state
    emotions: Dict[str, float] = field(default_factory=dict)  # emotion -> intensity
    knowledge: Set[str] = field(default_factory=set)  # known facts
    
    # Meta-info
    timestamp: float = field(default_factory=time.time)
    confidence: float = 0.5  # How confident we are in this attribution
    evidence: List[str] = field(default_factory=list)  # Source memory IDs
    
    def add_belief(self, belief: str, confidence: float = 0.5, source: str = ""):
        """Add or update a belief."""
        key = belief.lower().strip()
        if key in self.beliefs:
            # Update confidence (Bayesian-ish averaging)
            old_conf = self.beliefs[key]
            new_weight = 0.7 if source else 0.5
            self.beliefs[key] = old_conf * (1 - new_weight) + confidence * new_weight
        else:
            self.beliefs[key] = confidence
        
        if source:
            self.evidence.append(source)
    
    def add_knowledge(self, fact: str):
        """Add a known fact (higher certainty than belief)."""
        self.knowledge.add(fact.lower().strip())
    
    def add_desire(self, desire: str):
        """Add a desire/goal."""
        desire = desire.strip()
        if desire not in self.desires:
            self.desires.append(desire)
    
    def set_emotion(self, emotion: str, intensity: float):
        """Set an emotion intensity."""
        self.emotions[emotion.lower()] = np.clip(intensity, 0.0, 1.0)
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'beliefs': self.beliefs,
            'desires': self.desires,
            'intentions': self.intentions,
            'emotions': self.emotions,
            'knowledge': list(self.knowledge),
            'timestamp': self.timestamp,
            'confidence': self.confidence,
        }


@dataclass
class PerspectiveFrame:
    """
    A frame representing another agent's perspective at a moment.
    
    Used for:
    - Perspective taking simulation
    - False belief tasks
    - Predicting behavior from attributed mental state
    """
    agent_id: str
    situation: str  # Description of the current situation
    mental_state: MentalState
    predicted_action: Optional[str] = None
    actual_action: Optional[str] = None  # Filled in after observation
    accuracy: Optional[float] = None  # Prediction accuracy
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            'agent_id': self.agent_id,
            'situation': self.situation,
            'mental_state': self.mental_state.to_dict(),
            'predicted_action': self.predicted_action,
            'actual_action': self.actual_action,
            'accuracy': self.accuracy,
        }


class TheoryOfMind:
    """
    Theory of Mind module for understanding other minds.
    
    Provides:
    - Mental state attribution from behavior
    - Perspective taking simulation
    - Recursive modeling (I think that you think...)
    - Belief updating from evidence
    - Prediction of behavior from attributed mental states
    
    Integration points:
    - SelfNarrative: Models self for contrast with other
    - VolitionEngine: Predicts intentions and actions
    """
    
    def __init__(self):
        """Initialize Theory of Mind module."""
        # Tracked agents (including self)
        self.agents: Dict[str, MentalState] = {}
        
        # Perspective frames for simulation
        self.perspective_history: List[PerspectiveFrame] = []
        
        # Integration with other modules (optional)
        self.self_narrative: Optional[Any] = None
        self.volition: Optional[Any] = None
        
        # Rules for behavior prediction
        self._init_prediction_rules()
        
        # Statistics
        self.stats = {
            'attributions': 0,
            'predictions': 0,
            'correct_predictions': 0,
            'false_belief_tasks': 0,
        }
    
    def _init_prediction_rules(self):
        """Initialize rules for predicting behavior from mental state."""
        self.prediction_rules = [
            # (condition, action_template)
            (lambda ms: 'hungry' in ms.desires, 'seek_food'),
            (lambda ms: ms.emotions.get('fear', 0) > 0.7, 'avoid_or_escape'),
            (lambda ms: ms.emotions.get('curiosity', 0) > 0.7, 'explore'),
            (lambda ms: 'complete_task' in ms.desires, 'work_on_task'),
        ]
    
    def initialize_agent(self, agent_id: str, agent_name: str) -> MentalState:
        """
        Initialize mental state tracking for a new agent.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_name: Human-readable name
            
        Returns:
            New MentalState for the agent
        """
        mental_state = MentalState(
            agent_id=agent_id,
            agent_name=agent_name,
        )
        
        self.agents[agent_id] = mental_state
        self.stats['attributions'] += 1
        
        return mental_state
    
    def get_mental_state(self, agent_id: str) -> Optional[MentalState]:
        """Get the current mental state attribution for an agent."""
        return self.agents.get(agent_id)
    
    def update_from_behavior(self, 
                             agent_id: str,
                             behavior: str,
                             context: str = "",
                             source_memory: str = "",
                             update_beliefs: bool = True) -> MentalState:
        """
        Update mental state attribution based on observed behavior.
        
        Args:
            agent_id: Agent who performed the behavior
            behavior: What they did
            context: Situational context
            source_memory: Memory ID for evidence tracking
            update_beliefs: Whether to infer beliefs from behavior
            
        Returns:
            Updated MentalState
        """
        if agent_id not in self.agents:
            self.initialize_agent(agent_id, agent_id)
        
        ms = self.agents[agent_id]
        
        # Inferring beliefs from behavior (reverse inference)
        if update_beliefs:
            self._infer_beliefs_from_behavior(ms, behavior, context)
        
        # Inferring desires
        self._infer_desires_from_behavior(ms, behavior, context)
        
        # Inferring emotions
        self._infer_emotions_from_behavior(ms, behavior, context)
        
        # Track evidence
        if source_memory:
            ms.evidence.append(source_memory)
        
        ms.timestamp = time.time()
        self.stats['attributions'] += 1
        
        return ms
    
    def _infer_beliefs_from_behavior(self, ms: MentalState, behavior: str, context: str):
        """Infer beliefs from observed behavior."""
        behavior_lower = behavior.lower()
        
        # Simple pattern matching for belief inference
        belief_patterns = [
            ('searching', 'item_is_near'),
            ('avoiding', 'danger_present'),
            ('approaching', 'safe_or_desirable'),
            ('asking', 'lacks_information'),
            ('explaining', 'has_information'),
            ('leaving', 'goal_completed_or_impossible'),
        ]
        
        for pattern, belief_template in belief_patterns:
            if pattern in behavior_lower:
                ms.add_belief(belief_template, confidence=0.6, source=context)
                break
    
    def _infer_desires_from_behavior(self, ms: MentalState, behavior: str, context: str):
        """Infer desires from observed behavior."""
        behavior_lower = behavior.lower()
        
        desire_patterns = [
            ('asking', 'get_information'),
            ('searching', 'find_item'),
            ('building', 'create_something'),
            ('protecting', 'ensure_safety'),
            ('helping', 'assist_other'),
        ]
        
        for pattern, desire_template in desire_patterns:
            if pattern in behavior_lower:
                ms.add_desire(desire_template)
                break
    
    def _infer_emotions_from_behavior(self, ms: MentalState, behavior: str, context: str):
        """Infer emotions from observed behavior."""
        behavior_lower = behavior.lower()
        context_lower = context.lower() if context else ""
        
        # Emotion inference based on behavior patterns
        emotion_indicators = [
            ('excited', ['excited', 'enthusiastic', 'eager', 'can\'t wait']),
            ('frustrated', ['frustrated', 'annoyed', 'stuck', 'confused']),
            ('happy', ['happy', 'glad', 'pleased', 'great']),
            ('worried', ['worried', 'concerned', 'anxious', 'nervous']),
            ('curious', ['curious', 'wonder', 'interesting', 'tell me']),
        ]
        
        for emotion, indicators in emotion_indicators:
            for indicator in indicators:
                if indicator in behavior_lower or indicator in context_lower:
                    current = ms.emotions.get(emotion, 0.0)
                    ms.set_emotion(emotion, min(1.0, current + 0.3))
    
    def take_perspective(self, 
                         agent_id: str,
                         situation: str,
                         depth: int = 0) -> PerspectiveFrame:
        """
        Simulate another agent's perspective in a situation.
        
        Args:
            agent_id: Agent whose perspective to take
            situation: Description of the situation
            depth: Recursion depth for nested mental states (0 = no nesting)
            
        Returns:
            PerspectiveFrame with predicted mental state and action
        """
        if agent_id not in self.agents:
            ms = self.initialize_agent(agent_id, agent_id)
        else:
            ms = self.agents[agent_id]
        
        # Create a copy of mental state for this perspective
        perspective_ms = MentalState(
            agent_id=ms.agent_id,
            agent_name=ms.agent_name,
            beliefs=ms.beliefs.copy(),
            desires=ms.desires.copy(),
            intentions=ms.intentions.copy(),
            emotions=ms.emotions.copy(),
            knowledge=ms.knowledge.copy(),
            confidence=ms.confidence,
        )
        
        # Predict action based on mental state
        predicted = self._predict_action(perspective_ms, situation)
        
        frame = PerspectiveFrame(
            agent_id=agent_id,
            situation=situation,
            mental_state=perspective_ms,
            predicted_action=predicted,
        )
        
        self.perspective_history.append(frame)
        self.stats['predictions'] += 1
        
        # TODO: Recursive perspective taking for depth > 0
        # Would need to model what agent_id thinks about OTHER agents
        
        return frame
    
    def _predict_action(self, ms: MentalState, situation: str) -> str:
        """Predict an agent's action based on their mental state."""
        # Check prediction rules
        for condition, action in self.prediction_rules:
            if condition(ms):
                return action
        
        # Default: act on strongest desire
        if ms.desires:
            return f"act_on_{ms.desires[0]}"
        
        return "observe"  # Default action
    
    def update_prediction(self, 
                          agent_id: str,
                          actual_action: str,
                          situation: str = ""):
        """
        Update prediction accuracy based on observed action.
        
        Args:
            agent_id: Agent who acted
            actual_action: What they actually did
            situation: Situation context (to match with prediction)
        """
        # Find most recent prediction for this agent/situation
        for frame in reversed(self.perspective_history):
            if frame.agent_id == agent_id:
                frame.actual_action = actual_action
                
                # Compute accuracy (simple string similarity for now)
                if frame.predicted_action:
                    pred_lower = frame.predicted_action.lower()
                    act_lower = actual_action.lower()
                    
                    # Jaccard similarity on word sets
                    pred_words = set(pred_lower.split())
                    act_words = set(act_lower.split())
                    
                    if pred_words and act_words:
                        intersection = pred_words & act_words
                        union = pred_words | act_words
                        frame.accuracy = len(intersection) / len(union)
                        
                        if frame.accuracy > 0.5:
                            self.stats['correct_predictions'] += 1
                
                break
    
    def false_belief_test(self, 
                          agent_id: str,
                          true_state: str,
                          believed_state: str,
                          question: str) -> Dict:
        """
        Test false belief reasoning (Sally-Anne task style).
        
        Args:
            agent_id: Agent to test reasoning about
            true_state: What is actually true
            believed_state: What the agent believes is true
            question: Question about agent's behavior
            
        Returns:
            Dict with predicted answer and reasoning
        """
        self.stats['false_belief_tasks'] += 1
        
        # Get or create mental state
        if agent_id not in self.agents:
            ms = self.initialize_agent(agent_id, agent_id)
        else:
            ms = self.agents[agent_id]
        
        # Update mental state with false belief (not true knowledge)
        ms.beliefs[believed_state.lower()] = 1.0
        # Note: We DON'T add to knowledge, only beliefs
        
        # Predict behavior based on false belief
        predicted_answer = believed_state  # Agent will act on their belief
        
        reasoning = {
            'agent': agent_id,
            'true_state': true_state,
            'agent_belief': believed_state,
            'has_access_to_truth': False,
            'predicted_behavior': f"act_as_if_{believed_state}",
            'answer': predicted_answer,
        }
        
        return reasoning
    
    def update_belief_from_evidence(self, 
                                     agent_id: str,
                                     evidence: str,
                                     source: str = ""):
        """
        Update an agent's beliefs based on new evidence.
        
        Args:
            agent_id: Agent whose beliefs to update
            evidence: New evidence/fact
            source: Source of evidence
        """
        if agent_id not in self.agents:
            self.initialize_agent(agent_id, agent_id)
        
        ms = self.agents[agent_id]
        
        # Agent now knows this fact
        ms.add_knowledge(evidence)
        ms.add_belief(evidence, confidence=1.0, source=source)
    
    def model_recursive(self, 
                        agent_id: str,
                        target_id: str,
                        situation: str,
                        depth: int = 1) -> Dict:
        """
        Model recursive mental states: "I think that you think that..."
        
        Args:
            agent_id: The agent doing the thinking
            target_id: The agent being thought about
            situation: Current situation
            depth: How many levels of recursion
            
        Returns:
            Dict with nested mental state attributions
        """
        if depth == 0:
            return {'situation': situation}
        
        # Model what agent_id thinks about target_id
        if agent_id not in self.agents:
            self.initialize_agent(agent_id, agent_id)
        
        agent_ms = self.agents[agent_id]
        
        # What does agent_id think target_id believes?
        nested_state = MentalState(
            agent_id=target_id,
            agent_name=target_id,
            beliefs=agent_ms.beliefs.copy(),  # Assume agent projects their beliefs
            confidence=agent_ms.confidence * 0.8,  # Lower confidence in nested attribution
        )
        
        result = {
            'thinker': agent_id,
            'thinks_about': target_id,
            'attribution': nested_state.to_dict(),
            'nested': None,
        }
        
        # Recurse if depth > 1
        if depth > 1:
            result['nested'] = self.model_recursive(
                target_id, 
                agent_id,
                situation,
                depth - 1
            )
        
        return result
    
    def get_most_likely_desire(self, agent_id: str) -> Optional[str]:
        """Get most likely current desire for an agent."""
        if agent_id not in self.agents:
            return None
        ms = self.agents[agent_id]
        return ms.desires[0] if ms.desires else None
    
    def get_predicted_emotion(self, agent_id: str) -> Optional[Tuple[str, float]]:
        """Get the strongest predicted emotion for an agent."""
        if agent_id not in self.agents:
            return None
        ms = self.agents[agent_id]
        if not ms.emotions:
            return None
        strongest = max(ms.emotions.items(), key=lambda x: x[1])
        return strongest
    
    def to_dict(self) -> Dict:
        """Serialize ToM state to dictionary."""
        return {
            'agents': {aid: ms.to_dict() for aid, ms in self.agents.items()},
            'perspective_history': [f.to_dict() for f in self.perspective_history[-100:]],
            'stats': self.stats,
        }
    
    def save(self, filepath: str):
        """Save ToM state to file."""
        import tempfile
        import os
        import hashlib
        
        data = self.to_dict()
        
        # Compute hash for integrity
        json_str = json.dumps(data, indent=2)
        content_hash = hashlib.sha256(json_str.encode()).hexdigest()
        data['_hash'] = content_hash
        
        # Atomic write
        filepath = Path(filepath)
        with tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            dir=filepath.parent,
            suffix='.tmp'
        ) as f:
            json.dump(data, f, indent=2)
            temp_path = f.name
        
        os.replace(temp_path, filepath)
        
        # Hash sidecar
        hash_path = filepath.with_suffix('.sha256')
        with open(hash_path, 'w') as f:
            json.dump({
                'algorithm': 'sha256',
                'hash': content_hash,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            }, f, indent=2)
    
    def load(self, filepath: str, verify: bool = True):
        """Load ToM state from file."""
        
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"ToM state file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct
        for agent_id, ms_data in data.get('agents', {}).items():
            ms = MentalState(
                agent_id=ms_data['agent_id'],
                agent_name=ms_data['agent_name'],
                beliefs=ms_data.get('beliefs', {}),
                desires=ms_data.get('desires', []),
                intentions=ms_data.get('intentions', []),
                emotions=ms_data.get('emotions', {}),
                knowledge=set(ms_data.get('knowledge', [])),
                confidence=ms_data.get('confidence', 0.5),
                timestamp=ms_data.get('timestamp', time.time()),
            )
            self.agents[agent_id] = ms
        
        self.stats = data.get('stats', self.stats)
    
    def get_statistics(self) -> Dict:
        """Get ToM statistics."""
        stats = self.stats.copy()
        stats['agents_tracked'] = len(self.agents)
        stats['prediction_accuracy'] = (
            self.stats['correct_predictions'] / max(self.stats['predictions'], 1)
        )
        return stats


# =============================================================================
# Demonstration
# =============================================================================

def demo_theory_of_mind():
    """Demonstrate Theory of Mind capabilities."""
    print("=" * 70)
    print("THEORY OF MIND DEMONSTRATION")
    print("=" * 70)
    
    # Create ToM module
    tom = TheoryOfMind()
    
    # Initialize David
    david_ms = tom.initialize_agent("david", "David")
    print(f"\n👤 Initialized: {david_ms.agent_name}")
    
    # Update from behavior
    print("\n📊 Observing behavior: 'David asked about NIMA integration'")
    tom.update_from_behavior(
        agent_id="david",
        behavior="asked about NIMA integration",
        context="technical discussion",
        source_memory="mem_001"
    )
    
    david_ms = tom.get_mental_state("david")
    print(f"   Inferred beliefs: {list(david_ms.beliefs.keys())[:3]}")
    print(f"   Inferred desires: {david_ms.desires[:3]}")
    print(f"   Inferred emotions: {david_ms.emotions}")
    
    # Take perspective
    print("\n🔭 Taking David's perspective on 'working on NIMA'")
    frame = tom.take_perspective("david", "working on NIMA")
    print(f"   Predicted action: {frame.predicted_action}")
    
    # False belief test
    print("\n🎭 False Belief Test:")
    result = tom.false_belief_test(
        agent_id="david",
        true_state="NIMA uses dense vectors",
        believed_state="NIMA uses sparse vectors",
        question="What will David say about NIMA encoding?"
    )
    print(f"   True state: {result['true_state']}")
    print(f"   Agent belief: {result['agent_belief']}")
    print(f"   Predicted answer: {result['answer']}")
    
    # Recursive modeling
    print("\n🪞 Recursive Mental State:")
    recursive = tom.model_recursive("lilu", "david", "discussion about consciousness", depth=2)
    print(f"   Thinker: {recursive['thinker']}")
    print(f"   Thinks about: {recursive['thinks_about']}")
    
    # Statistics
    print("\n📈 ToM Statistics:")
    stats = tom.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✅ Theory of Mind operational")
    print("=" * 70)


if __name__ == "__main__":
    demo_theory_of_mind()