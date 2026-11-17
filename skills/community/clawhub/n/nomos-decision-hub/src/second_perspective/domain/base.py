"""Domain control pack protocol and registry (v0.5)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..models.schemas import DecisionRequest


@dataclass
class DomainViolation:
    pack_id: str
    code: str
    message: str
    severity: str = "warning"  # warning | error


class DomainControlPack(Protocol):
    id: str
    description: str

    def validate(self, request: DecisionRequest) -> list[DomainViolation]: ...


class DomainPackRegistry:
    def __init__(self) -> None:
        self._packs: dict[str, DomainControlPack] = {}

    def register(self, pack: DomainControlPack) -> None:
        self._packs[pack.id] = pack

    def all(self) -> list[DomainControlPack]:
        return list(self._packs.values())

    def validate(self, request: DecisionRequest) -> list[DomainViolation]:
        violations: list[DomainViolation] = []
        for pack in self._packs.values():
            violations.extend(pack.validate(request))
        return violations


_registry = DomainPackRegistry()


def get_registry() -> DomainPackRegistry:
    return _registry
