from __future__ import annotations

import re
from collections import Counter

from .schema import PromptIR, ValidationReport


class DeterministicValidator:
    NEGATIONS = ("不", "无", "未", "勿", "禁止", "不得", "不要", "不能", "仅", "只", "not", "no", "never", "without", "only", "mustn't", "don't")
    PARAM_PATTERN = re.compile(
        r"https?://[^\s<>\]\[()，。；、！？]+|"
        r"(?:[$¥€£]\s?)?\d[\d,]*(?:\.\d+)?(?:%|％)?(?:[-/:]\d{1,4}){0,2}(?:[T ][0-9:.+Z-]+)?|"
        r"(?<![\w.-])[\w.@+-]+\.(?:py|md|pdf|docx|xlsx|json|txt|csv|png|jpe?g|yaml|yml|toml|js|ts|tsx|sql)(?!\w)|"
        r"\b[A-Za-z_]\w*\s*\(\s*\)|"
        r"\b(?:v?\d+(?:\.\d+){1,3})\b",
        re.I,
    )

    def validate(self, original: str, optimized: str, ir: PromptIR) -> ValidationReport:
        original_literals = self.extract_literals(original)
        optimized_literals = self.extract_literals(optimized)
        missing = list((Counter(original_literals) - Counter(optimized_literals)).elements())
        additions = list((Counter(optimized_literals) - Counter(original_literals)).elements())

        original_negations = self._negations(original)
        optimized_negations = self._negations(optimized)
        missing.extend(list((Counter(original_negations) - Counter(optimized_negations)).elements()))
        additions.extend(list((Counter(optimized_negations) - Counter(original_negations)).elements()))

        flat_ir = [item for values in ir.to_dict().values() for item in values]
        untraceable = [item for item in flat_ir if not self._traceable(item, original)]
        ledger = " ".join(flat_ir)
        mismatches = [literal for literal in optimized_literals + optimized_negations if literal.lower() not in ledger.lower()]
        scope_mismatches = [clause for clause in self._protected_negation_clauses(original) if not self._contains_normalized(optimized, clause)]
        valid = not (missing or additions or untraceable or mismatches or scope_mismatches)
        return ValidationReport(valid, self._unique(missing), self._unique(additions), self._unique(untraceable), self._unique(mismatches), self._unique(scope_mismatches))

    def extract_literals(self, text: str) -> list[str]:
        return [m.group(0).strip().rstrip(".,，。") for m in self.PARAM_PATTERN.finditer(text)]

    def _negations(self, text: str) -> list[str]:
        lowered = text.lower()
        return [word for word in self.NEGATIONS if word in lowered]

    def _protected_negation_clauses(self, text: str) -> list[str]:
        clauses = [part.strip() for part in re.split(r"[，,。；;！？!?\n]", text) if part.strip()]
        return [clause for clause in clauses if any(word in clause.lower() for word in self.NEGATIONS)]

    @staticmethod
    def _contains_normalized(text: str, clause: str) -> bool:
        norm = lambda value: re.sub(r"[\s，,。；;：:！？!?\"'`]+", "", value).lower()
        return norm(clause) in norm(text)

    @staticmethod
    def _traceable(item: str, original: str) -> bool:
        norm = lambda value: re.sub(r"[\s，,。；;：:！？!?\"'`]+", "", value).lower()
        value = norm(item)
        return bool(value) and value in norm(original)

    @staticmethod
    def _unique(items: list[str]) -> list[str]:
        return list(dict.fromkeys(items))
