#!/usr/bin/env python3
"""
Cost Watchdog - Optimized Cost Calculator
Token-efficient, accurate cost calculations with caching.
"""

import re
import sys
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass

# Ensure sibling `_pricing` is importable regardless of CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pricing

_TOKENIZER_CACHE: Dict[str, any] = {}

DATA_DIR = Path.home() / ".cost-watchdog"
DATA_DIR.mkdir(exist_ok=True)

# Default fallback for unknown models (Sonnet-tier).
_DEFAULT_INPUT_PRICE = 3.0
_DEFAULT_OUTPUT_PRICE = 15.0


def _prices_for(model: str) -> tuple:
    """Return (input_per_1M, output_per_1M, note). Exact match, no substring."""
    price = _pricing.get_price(model)
    if price is None:
        return (
            _DEFAULT_INPUT_PRICE,
            _DEFAULT_OUTPUT_PRICE,
            f"Unknown model {model!r}; using default ${_DEFAULT_INPUT_PRICE}/${_DEFAULT_OUTPUT_PRICE} per 1M",
        )
    return price.input_per_1m, price.output_per_1m, ""


@dataclass
class CostResult:
    """Structured cost calculation result."""
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float
    model: str
    confidence: str
    notes: list


def count_tokens(text: str, model: str = "default") -> int:
    """
    Count tokens for `text` under `model`. Routes through tokenizer.py
    which picks the correct strategy per provider family (tiktoken for
    OpenAI-family, calibrated heuristics for Claude/Gemini/others).
    Use tokenizer.count_tokens() directly if you need the method label.
    """
    import tokenizer
    return tokenizer.count(text, model)


def estimate_cost(text: str, model: str,
                  is_output: bool = False) -> CostResult:
    """Estimate cost for a single text block."""
    input_price, output_price, lookup_note = _prices_for(model)
    tokens = count_tokens(text, model)

    if is_output:
        cost = (tokens / 1_000_000) * output_price
        notes = [f"Output: {tokens:,} tokens"]
        if lookup_note:
            notes.insert(0, lookup_note)
        return CostResult(
            input_tokens=0, output_tokens=tokens,
            input_cost=0, output_cost=cost, total_cost=cost,
            model=model,
            confidence="high" if tokens < 10000 else "medium",
            notes=notes,
        )

    cost = (tokens / 1_000_000) * input_price
    notes = [f"Input: {tokens:,} tokens"]
    if lookup_note:
        notes.insert(0, lookup_note)
    return CostResult(
        input_tokens=tokens, output_tokens=0,
        input_cost=cost, output_cost=0, total_cost=cost,
        model=model, confidence="high",
        notes=notes,
    )


def estimate_batch_cost(num_items: int,
                        avg_input_tokens: int,
                        avg_output_tokens: int,
                        model: str,
                        use_batch_api: bool = False) -> CostResult:
    """Estimate cost for batch processing, optionally with batch-API discount."""
    input_price, output_price, lookup_note = _prices_for(model)
    batch_discount = 0.5

    total_input = num_items * avg_input_tokens
    total_output = num_items * avg_output_tokens

    base_input_cost = (total_input / 1_000_000) * input_price
    base_output_cost = (total_output / 1_000_000) * output_price

    if use_batch_api:
        input_cost = base_input_cost * batch_discount
        output_cost = base_output_cost * batch_discount
        notes = [f"Batch API discount: {batch_discount*100:.0%}"]
    else:
        input_cost = base_input_cost
        output_cost = base_output_cost
        notes = []

    if lookup_note:
        notes.insert(0, lookup_note)

    return CostResult(
        input_tokens=total_input,
        output_tokens=total_output,
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=input_cost + output_cost,
        model=model,
        confidence="medium",
        notes=notes + [
            f"Items: {num_items}",
            f"Avg input: {avg_input_tokens:,} tokens",
            f"Avg output: {avg_output_tokens:,} tokens",
        ],
    )


def compare_models(input_tokens: int, output_tokens: int,
                   models: list) -> list:
    """Compare costs across multiple models. Returns list sorted by total cost."""
    results = []
    for model in models:
        input_price, output_price, _ = _prices_for(model)
        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price
        results.append({
            'model': model,
            'input_cost': round(input_cost, 4),
            'output_cost': round(output_cost, 4),
            'total_cost': round(input_cost + output_cost, 4),
            'input_price': input_price,
            'output_price': output_price,
        })
    results.sort(key=lambda x: x['total_cost'])
    return results


def find_cheaper_alternatives(current_model: str,
                              input_tokens: int,
                              output_tokens: int,
                              min_savings: float = 0.5) -> list:
    """
    Find models that are at least min_savings (0.5 = 50%) cheaper.
    Only compares models with the same billing unit (can't compare tokens
    to images to seconds).
    """
    current_price = _pricing.get_price(current_model)
    if current_price is None:
        return []
    current_unit = current_price.unit

    current_results = compare_models(input_tokens, output_tokens, [current_model])
    if not current_results:
        return []
    current_cost = current_results[0]['total_cost']
    if current_cost <= 0:
        return []

    current_slug = _pricing.canonical_slug(current_model)
    alternatives = []
    for slug, info in _pricing.load_pricing().items():
        if slug == current_slug:
            continue
        if info.unit != current_unit:
            continue
        alt_cost = compare_models(input_tokens, output_tokens, [slug])[0]['total_cost']
        savings = (current_cost - alt_cost) / current_cost
        if savings >= min_savings:
            alternatives.append({
                'model': slug,
                'current_cost': round(current_cost, 4),
                'alternative_cost': round(alt_cost, 4),
                'savings_percent': round(savings * 100, 1),
                'provider': info.provider,
                'unit': info.unit,
            })
    alternatives.sort(key=lambda x: x['savings_percent'], reverse=True)
    return alternatives[:10]


def analyze_code_for_costs(code: str) -> Dict:
    """
    Analyze code for cost risks via AST parsing.
    See code_audit.py for the actual checks.
    """
    import code_audit
    risks = code_audit.audit_source(code)
    as_dicts = [
        {
            "type": r.severity,
            "line": r.line,
            "pattern": r.message,
            "recommendation": r.recommendation,
            "kind": r.kind,
        }
        for r in risks
    ]
    return {
        "risk_count": len(as_dicts),
        "critical": sum(1 for r in as_dicts if r["type"] == "CRITICAL"),
        "high": sum(1 for r in as_dicts if r["type"] == "HIGH"),
        "medium": sum(1 for r in as_dicts if r["type"] == "MEDIUM"),
        "risks": as_dicts,
    }


def main():
    """CLI interface for optimized calculator."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: optimized-calculator.py [command] [args]")
        print("Commands:")
        print("  estimate <text> <model>              - Estimate cost")
        print("  batch <count> <input> <output> <model> - Batch estimate")
        print("  compare <model1> <model2> ...        - Compare models")
        print("  alternatives <model>                 - Find cheaper alternatives")
        print("  analyze <file.py>                    - Analyze code for risks")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "estimate":
        text = sys.argv[2]
        model = sys.argv[3] if len(sys.argv) > 3 else "claude-sonnet-4-6"
        result = estimate_cost(text, model)
        print(f"💰 Cost: ${result.total_cost:.4f}")
        print(f"   Tokens: {result.input_tokens + result.output_tokens:,}")
        print(f"   Confidence: {result.confidence}")
    
    elif command == "batch":
        count = int(sys.argv[2])
        input_tokens = int(sys.argv[3])
        output_tokens = int(sys.argv[4])
        model = sys.argv[5] if len(sys.argv) > 5 else "claude-sonnet-4-6"
        result = estimate_batch_cost(count, input_tokens, output_tokens, model)
        print(f"💰 Batch Cost: ${result.total_cost:.4f}")
        print(f"   Total tokens: {result.input_tokens + result.output_tokens:,}")
        for note in result.notes:
            print(f"   {note}")
    
    elif command == "compare":
        models = sys.argv[2:]
        results = compare_models(100000, 20000, models)
        print("📊 Model Comparison (100K input + 20K output):")
        for r in results:
            print(f"   {r['model']:<25} ${r['total_cost']:.4f}")
    
    elif command == "alternatives":
        model = sys.argv[2]
        alternatives = find_cheaper_alternatives(model, 100000, 20000)
        print(f"💡 Cheaper alternatives to {model}:")
        for alt in alternatives:
            print(f"   • {alt['model']}: Save {alt['savings_percent']}%")
    
    elif command == "analyze":
        file_path = sys.argv[2]
        with open(file_path, 'r') as f:
            code = f.read()
        analysis = analyze_code_for_costs(code)
        print(f"🔍 Code Analysis:")
        print(f"   Critical risks: {analysis['critical']}")
        print(f"   High risks: {analysis['high']}")
        print(f"   Medium risks: {analysis['medium']}")
        for risk in analysis['risks']:
            print(f"   ⚠️  [{risk['type']}] {risk['pattern']}")
            print(f"      → {risk['recommendation']}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
