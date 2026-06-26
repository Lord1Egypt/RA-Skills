from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class PrefilterResult:
    decision: str
    source: str = "prefilter"
    category: str = "none"
    confidence: str = "low"
    matched_terms: list[str] = field(default_factory=list)
    matched_rules: list[str] = field(default_factory=list)
    message: str = "No prefilter rule matched."


class InputSafetyGuard:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.policy = config.get("policy", {})
        self.normalization = config.get("normalization", {})
        self.scope = config.get("scope", {})
        self.allowlist = config.get("allowlist", {})
        self.rules = config.get("rules", [])

    @classmethod
    def from_file(cls, config_path: str | Path) -> "InputSafetyGuard":
        with Path(config_path).open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        return cls(data)

    @classmethod
    def from_profile(
        cls,
        profile: str = "default",
        *,
        config_dir: str | Path | None = None,
    ) -> "InputSafetyGuard":
        resolved_config_dir = Path(config_dir) if config_dir is not None else cls._default_config_dir()
        base_config = cls.from_file(resolved_config_dir / "default_rules.yaml").config

        normalized_profile = "default" if profile == "balanced" else profile

        if normalized_profile == "default":
            return cls(base_config)

        override_path = resolved_config_dir / f"default_rules.{normalized_profile}.yaml"
        override_config = cls.from_file(override_path).config
        merged_config = cls._merge_config(base_config, override_config)
        return cls(merged_config)

    def evaluate(
        self,
        text: str,
        *,
        role: str | None = None,
        environment: str | None = None,
    ) -> PrefilterResult:
        normalized_text = self._normalize(text)

        if self._is_allowlisted(text, normalized_text, role=role, environment=environment):
            return PrefilterResult(
                decision=self.policy.get("review_decision", "review"),
                confidence="medium",
                message="Matched an allowlist scope or phrase. Continue to semantic review.",
            )

        highest_result: PrefilterResult | None = None
        highest_priority = -1

        for rule in self.rules:
            if not rule.get("enabled", True):
                continue

            matched_terms = self._match_rule(rule, text=text, normalized_text=normalized_text)
            if not matched_terms:
                continue

            action = str(rule.get("action", self.policy.get("review_decision", "review")))
            priority = self._decision_priority(action)
            candidate = PrefilterResult(
                decision=action,
                category=str(rule.get("category", "none")),
                confidence=str(rule.get("confidence", self.policy.get("default_confidence", "low"))),
                matched_terms=matched_terms,
                matched_rules=[str(rule.get("id", "unnamed-rule"))],
                message=self._message_for(action),
            )

            if priority > highest_priority:
                highest_result = candidate
                highest_priority = priority
            elif priority == highest_priority and highest_result is not None:
                highest_result.matched_terms.extend(term for term in matched_terms if term not in highest_result.matched_terms)
                highest_result.matched_rules.extend(
                    rule_id for rule_id in candidate.matched_rules if rule_id not in highest_result.matched_rules
                )

        if highest_result is not None:
            return highest_result

        return PrefilterResult(
            decision=self.policy.get("default_decision", "allow"),
            confidence=self.policy.get("default_confidence", "low"),
        )

    def _is_allowlisted(
        self,
        original_text: str,
        normalized_text: str,
        *,
        role: str | None,
        environment: str | None,
    ) -> bool:
        allowed_roles = {item.lower() for item in self.scope.get("allowlist_roles", [])}
        allowed_environments = {item.lower() for item in self.scope.get("allowlist_environments", [])}

        if role and role.lower() in allowed_roles:
            return True
        if environment and environment.lower() in allowed_environments:
            return True

        exact_phrases = [phrase.lower() for phrase in self.allowlist.get("exact_phrases", [])]
        if any(phrase in original_text.lower() or phrase in normalized_text for phrase in exact_phrases):
            return True

        for pattern in self.allowlist.get("regex_patterns", []):
            if re.search(pattern, original_text) or re.search(pattern, normalized_text):
                return True

        return False

    def _match_rule(self, rule: dict[str, Any], *, text: str, normalized_text: str) -> list[str]:
        matched_terms: list[str] = []
        match_mode = rule.get("match_mode", "contains")

        for keyword in rule.get("keywords", []):
            keyword_text = str(keyword)
            candidate = self._normalize(keyword_text) if match_mode == "normalized_contains" else keyword_text.lower()
            haystack = normalized_text if match_mode == "normalized_contains" else text.lower()
            if candidate and candidate in haystack:
                matched_terms.append(keyword_text)

        for pattern in rule.get("regex_patterns", []):
            if re.search(pattern, text) or re.search(pattern, normalized_text):
                matched_terms.append(pattern)

        return list(dict.fromkeys(matched_terms))

    def _normalize(self, text: str) -> str:
        normalized = text
        if self.normalization.get("lowercase", True):
            normalized = normalized.lower()
        if self.normalization.get("collapse_whitespace", True):
            normalized = re.sub(r"\s+", " ", normalized).strip()
        if self.normalization.get("strip_punctuation", True):
            normalized = re.sub(r"[^\w\s\u4e00-\u9fff]", "", normalized)
        if self.normalization.get("remove_common_separators", True):
            normalized = normalized.replace(" ", "").replace("_", "").replace("-", "")
        return normalized

    def _message_for(self, decision: str) -> str:
        if decision == self.policy.get("block_decision", "block"):
            return self.policy.get("blocked_message", "Request blocked by Input Safety Guard prefilter.")
        if decision == self.policy.get("review_decision", "review"):
            return self.policy.get("reviewed_message", "Request should continue to semantic safety review.")
        return "No blocking rule matched."

    @staticmethod
    def _decision_priority(decision: str) -> int:
        priorities = {"allow": 0, "review": 1, "block": 2}
        return priorities.get(decision, 0)

    @staticmethod
    def _default_config_dir() -> Path:
        return Path(__file__).resolve().parents[2] / "config"

    @classmethod
    def _merge_config(cls, base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        merged = dict(base)
        for key, value in override.items():
            if key == "rules" and isinstance(value, list):
                merged[key] = cls._merge_rules(base.get(key, []), value)
            elif isinstance(value, dict) and isinstance(base.get(key), dict):
                merged[key] = cls._merge_config(base[key], value)
            else:
                merged[key] = value
        return merged

    @staticmethod
    def _merge_rules(base_rules: list[dict[str, Any]], override_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
        merged_rules = [dict(rule) for rule in base_rules]
        index_by_id = {
            str(rule.get("id")): idx
            for idx, rule in enumerate(merged_rules)
            if rule.get("id") is not None
        }

        for override_rule in override_rules:
            override_id = str(override_rule.get("id")) if override_rule.get("id") is not None else None
            if override_id and override_id in index_by_id:
                base_rule = merged_rules[index_by_id[override_id]]
                merged_rules[index_by_id[override_id]] = InputSafetyGuard._merge_config(base_rule, override_rule)
            else:
                merged_rules.append(dict(override_rule))

        return merged_rules


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Input Safety Guard prefilter checks.")
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument("--config", help="Path to the YAML config file.")
    source_group.add_argument(
        "--profile",
        choices=["default", "balanced", "strict", "relaxed"],
        default="default",
        help="Named policy profile to load from the config directory.",
    )
    parser.add_argument("--text", required=True, help="Raw user input to evaluate.")
    parser.add_argument("--role", help="Optional user role for allowlist scope checks.")
    parser.add_argument("--environment", help="Optional environment name for allowlist scope checks.")
    return parser


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()
    if args.config:
        guard = InputSafetyGuard.from_file(args.config)
    else:
        guard = InputSafetyGuard.from_profile(args.profile)
    result = guard.evaluate(args.text, role=args.role, environment=args.environment)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
