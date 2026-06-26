"""
Self-Improving Governance for hawk-bridge

Tracks memory quality metrics and logs improvement events.
Monitors: extraction rate, noise ratio, recall hit rate, importance distribution.

Logs to: ~/.hawk/governance.log (JSONL format)
"""

import os
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class GovernanceEvent:
    timestamp: int
    event_type: str  # extraction | noise_filter | recall_hit | recall_miss | importance_dist
    count: int
    details: dict


class Governance:
    """
    Self-improving governance for hawk memory system.
    Tracks metrics and writes JSONL logs.
    """

    def __init__(self, log_path: str = "~/.hawk/governance.log"):
        self.log_path = os.path.expanduser(log_path)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, event_type: str, count: int = 1, details: dict = None):
        """Append a governance event"""
        event = GovernanceEvent(
            timestamp=int(time.time()),
            event_type=event_type,
            count=count,
            details=details or {},
        )
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(asdict(event), ensure_ascii=False) + '\n')

    def log_extraction(self, total: int, stored: int, skipped: int):
        """Log memory extraction results"""
        self.log('extraction', total, {
            'stored': stored,
            'skipped': skipped,
            'store_rate': round(stored / total, 3) if total else 0,
        })

    def log_noise_filter(self, filtered_count: int, total: int):
        """Log noise filtering results"""
        self.log('noise_filter', filtered_count, {
            'total': total,
            'noise_ratio': round(filtered_count / total, 3) if total else 0,
        })

    def log_recall(self, hits: int, total: int, query: str = ""):
        """Log recall results"""
        self.log('recall_hit' if hits else 'recall_miss', hits, {
            'total': total,
            'hit_rate': round(hits / total, 3) if total else 0,
            'query_preview': query[:100],
        })

    def get_stats(self, hours: int = 24) -> dict:
        """Get governance statistics over the last N hours"""
        if not os.path.exists(self.log_path):
            return {}

        cutoff = time.time() - hours * 3600
        stats = {
            'extractions': 0,
            'noise_filtered': 0,
            'recalls': 0,
            'recall_hits': 0,
            'avg_importance': 0,
            'importance_sum': 0,
            'importance_count': 0,
        }

        with open(self.log_path) as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event['timestamp'] < cutoff:
                        continue
                    et = event['event_type']
                    if et == 'extraction':
                        stats['extractions'] += event['count']
                        d = event.get('details', {})
                        stats['importance_sum'] += d.get('stored', 0)
                    elif et == 'noise_filter':
                        stats['noise_filtered'] += event['count']
                    elif et in ('recall_hit', 'recall_miss'):
                        stats['recalls'] += 1
                        if et == 'recall_hit':
                            stats['recall_hits'] += event['count']
                except json.JSONDecodeError:
                    continue

        if stats['importance_sum']:
            stats['avg_importance'] = round(stats['importance_sum'] / stats['extractions'], 3)
        if stats['recalls']:
            stats['recall_hit_rate'] = round(stats['recall_hits'] / stats['recalls'], 3)

        return stats

    def learn_noise_prototype(self, text: str, embedding: list[float]):
        """
        Learn a new noise prototype when extraction yields zero memories.
        Saves to noise_prototypes.json for next boot.
        """
        proto_path = os.path.expanduser('~/.hawk/noise_prototypes.json')
        protos = []
        if os.path.exists(proto_path):
            with open(proto_path) as f:
                protos = json.load(f)
        protos.append({'text': text[:100], 'embedding': embedding, 'learned_at': datetime.now().isoformat()})
        with open(proto_path, 'w') as f:
            json.dump(protos, f)
        return len(protos)
