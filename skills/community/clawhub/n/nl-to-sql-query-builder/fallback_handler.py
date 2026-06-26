#!/usr/bin/env python3
"""
Fallback Handler - Route low-confidence queries to human review
Part of NL-to-SQL Query Builder skill
"""
from enum import Enum
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json
import threading


class FallbackReason(Enum):
    LOW_CONFIDENCE = "low_confidence"
    AMBIGUOUS_SCHEMA = "ambiguous_schema"
    COMPLEX_QUERY = "complex_query"
    SAFETY_VIOLATION = "safety_violation"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class FallbackDecision:
    """Result of fallback handling decision"""
    should_fallback: bool
    reason: Optional[FallbackReason]
    confidence: float
    recommended_action: str  # 'auto_execute', 'clarify', 'human_review', 'reject'
    fallback_queue: Optional[str]  # Queue name for human review


class FallbackHandler:
    """Route queries based on confidence thresholds"""
    
    # Confidence thresholds
    AUTO_EXECUTE_THRESHOLD = 0.85
    CLARIFY_THRESHOLD = 0.60
    
    def __init__(
        self,
        auto_execute_threshold: float = 0.85,
        clarify_threshold: float = 0.60,
        fallback_queue: str = "nl-to-sql-review",
        notification_callback: Optional[Callable] = None
    ):
        self.auto_execute_threshold = auto_execute_threshold
        self.clarify_threshold = clarify_threshold
        self.fallback_queue = fallback_queue
        self.notification_callback = notification_callback
        self.fallback_log = []
        self._lock = threading.Lock()
        
    def decide(
        self,
        confidence: float,
        query: str,
        schema_match: float,
        ambiguity_detected: bool,
        safety_check_passed: bool
    ) -> FallbackDecision:
        """Make fallback decision based on confidence and factors"""
        
        # Check safety first
        if not safety_check_passed:
            return FallbackDecision(
                should_fallback=True,
                reason=FallbackReason.SAFETY_VIOLATION,
                confidence=confidence,
                recommended_action='reject',
                fallback_queue=None
            )
        
        # Auto-execute if high confidence
        if confidence >= self.auto_execute_threshold and not ambiguity_detected:
            return FallbackDecision(
                should_fallback=False,
                reason=None,
                confidence=confidence,
                recommended_action='auto_execute',
                fallback_queue=None
            )
        
        # Clarify if medium confidence or ambiguity detected
        if confidence >= self.clarify_threshold or ambiguity_detected:
            return FallbackDecision(
                should_fallback=True,
                reason=FallbackReason.AMBIGUOUS_SCHEMA if ambiguity_detected else None,
                confidence=confidence,
                recommended_action='clarify',
                fallback_queue=None
            )
        
        # Human review for low confidence
        reason = self._determine_low_confidence_reason(
            confidence, schema_match, ambiguity_detected
        )
        return FallbackDecision(
            should_fallback=True,
            reason=reason,
            confidence=confidence,
            recommended_action='human_review',
            fallback_queue=self.fallback_queue
        )
    
    def _determine_low_confidence_reason(
        self,
        confidence: float,
        schema_match: float,
        ambiguity_detected: bool
    ) -> FallbackReason:
        """Determine specific reason for low confidence"""
        if schema_match < 0.5:
            return FallbackReason.AMBIGUOUS_SCHEMA
        if ambiguity_detected:
            return FallbackReason.AMBIGUOUS_SCHEMA
        return FallbackReason.LOW_CONFIDENCE
    
    def route_to_human_review(
        self,
        query: str,
        confidence: float,
        reason: FallbackReason,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Route query to human review queue"""
        review_item = {
            'query': query,
            'confidence': confidence,
            'reason': reason.value,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'context': context or {},
            'status': 'pending'
        }
        
        with self._lock:
            self.fallback_log.append(review_item)
        
        # Notify via callback if configured
        if self.notification_callback:
            self.notification_callback(review_item)
        
        return review_item
    
    def get_pending_reviews(self, user_id: Optional[str] = None) -> list:
        """Get pending human reviews"""
        with self._lock:
            reviews = [r for r in self.fallback_log if r['status'] == 'pending']
            if user_id:
                reviews = [r for r in reviews if r['user_id'] == user_id]
            return reviews
    
    def approve_and_execute(
        self,
        review_id: int,
        modified_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """Mark review as approved, return for execution"""
        with self._lock:
            if review_id >= len(self.fallback_log):
                return {'error': 'Review not found'}
            
            review = self.fallback_log[review_id]
            review['status'] = 'approved'
            review['modified_query'] = modified_query
            
            return {
                'status': 'ready_for_execution',
                'query': modified_query or review['query'],
                'context': review['context']
            }
    
    def reject(self, review_id: int, reason: str) -> Dict[str, Any]:
        """Reject a query from human review"""
        with self._lock:
            if review_id >= len(self.fallback_log):
                return {'error': 'Review not found'}
            
            review = self.fallback_log[review_id]
            review['status'] = 'rejected'
            review['rejection_reason'] = reason
            
            return {'status': 'rejected', 'reason': reason}
    
    def export_log(self, filepath: str):
        """Export fallback log to JSON file"""
        with self._lock:
            with open(filepath, 'w') as f:
                json.dump(self.fallback_log, f, indent=2)


# CLI for testing
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fallback handler CLI')
    parser.add_argument('--confidence', type=float, required=True, help='Confidence score')
    parser.add_argument('--query', required=True, help='User query')
    parser.add_argument('--schema-match', type=float, default=0.8, help='Schema match score')
    parser.add_argument('--ambiguous', action='store_true', help='Ambiguity detected')
    
    args = parser.parse_args()
    
    handler = FallbackHandler()
    decision = handler.decide(
        args.confidence,
        args.query,
        args.schema_match,
        args.ambiguous,
        True  # safety check passed
    )
    
    print(f"Decision: {decision.recommended_action}")
    print(f"Should fallback: {decision.should_fallback}")
    if decision.reason:
        print(f"Reason: {decision.reason.value}")


if __name__ == '__main__':
    main()