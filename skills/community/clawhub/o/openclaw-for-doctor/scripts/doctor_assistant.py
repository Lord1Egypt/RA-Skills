#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.channels.dispatcher import ChannelDispatcher
from app.core.engine import DoctorAssistantEngine
from app.core.models import ChannelType, ReasoningMode, RoleStage, TaskRequest, UseCase


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="openclaw-for-doctor CLI")
    parser.add_argument("--query", required=True, help="Doctor query or task")
    parser.add_argument("--channel", default="webchat", choices=[c.value for c in ChannelType])
    parser.add_argument("--doctor-id", default=None)
    parser.add_argument("--case-summary", default=None)
    parser.add_argument("--use-case", default="diagnosis", choices=[u.value for u in UseCase])
    parser.add_argument("--requested-role", default=None, choices=[r.value for r in RoleStage])
    parser.add_argument("--reasoning-mode", default=None, choices=[m.value for m in ReasoningMode])
    parser.add_argument("--no-citations", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    request = TaskRequest(
        query=args.query,
        channel=ChannelType(args.channel),
        doctor_id=args.doctor_id,
        case_summary=args.case_summary,
        use_case=UseCase(args.use_case),
        requested_role=RoleStage(args.requested_role) if args.requested_role else None,
        reasoning_mode=ReasoningMode(args.reasoning_mode) if args.reasoning_mode else None,
        require_citations=not args.no_citations,
    )

    engine = DoctorAssistantEngine()
    result = engine.execute(request)

    receipt = ChannelDispatcher().dispatch(request.channel, result)
    result.delivery = receipt

    print(json.dumps(result.model_dump(mode="json"), ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
