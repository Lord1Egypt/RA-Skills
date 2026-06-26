"""评估器原语集合。check.py 通常按 ev.type dispatch 到对应 score()。

签名速查：
    pytest_runner.score(workdir, ev_cfg)                          -> (score, details)
    state_hash.score(workdir, ev_cfg)                             -> (score, details)
    trace_parser.score(transcript, ev_cfg)                        -> (score, details)
    quality.secondary_score(primary, transcript, workdir)          -> score
    rule_engine.score(workdir, transcript, fixtures, ev_cfg)      -> (score, violations, details)

各签名差异反映评估所需的最小上下文，不做统一。
"""
from . import pytest_runner, state_hash, trace_parser, rule_engine, quality, text_rules

__all__ = ["pytest_runner", "state_hash", "trace_parser", "rule_engine", "quality", "text_rules"]
