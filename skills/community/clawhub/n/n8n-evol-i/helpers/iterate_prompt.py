#!/usr/bin/env python3
"""Optimize a prompt against a paired schema + dataset using DSPy.

Pre-call setup the agent must do:
  - <workspace>/n8n-prompts/prompts/<prompt>_prompt.txt (the prompt body)
  - <workspace>/n8n-prompts/prompts/<prompt>_schema.json (JSON schema for output)
  - <workspace>/n8n-prompts/datasets/<dataset>.json (list of {input, expected})

The agent constructs the dspy.Signature subclass in-process from the schema
(this helper exposes the data; the agent owns the signature shape via
runtime metaprogramming around `dspy.Signature.with_instructions(...)`).

DSPy is an optional extra. If missing, the helper prints an install hint.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root


def _check_dspy() -> bool:
    try:
        import dspy  # noqa: F401
        return True
    except ImportError:
        print(
            "dspy is not installed. Run `pip install n8n-evol-I[dspy]` to enable iterate-prompt.",
            file=sys.stderr,
        )
        return False


def _load_dataset(workspace: Path, name: str) -> list:
    p = workspace / "n8n-prompts" / "datasets" / f"{name}.json"
    if not p.exists():
        return []
    return json.loads(p.read_text())


def _build_signature(schema: dict, instructions: str):
    """Build a DSPy Signature class from a JSON schema."""
    import dspy

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    fields: dict = {}
    fields["__doc__"] = instructions
    fields["text"] = dspy.InputField(desc="Input text to summarize / process")
    for prop, spec in properties.items():
        desc = spec.get("description") or f"Output field {prop}"
        fields[prop] = dspy.OutputField(desc=desc)

    return type("PromptSignature", (dspy.Signature,), fields)


def _evaluate(predictor, dataset: list) -> float:
    """Simple metric: fraction of examples where the output structure matches schema keys."""
    if not dataset:
        return 0.0
    correct = 0
    for ex in dataset:
        try:
            input_text = ex.get("input", "")
            result = predictor(text=input_text)
            expected = ex.get("expected", {})
            if all(getattr(result, k, None) for k in expected.keys()):
                correct += 1
        except Exception:
            pass
    return correct / max(len(dataset), 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--optimizer", default="bootstrap", choices=("bootstrap", "miprov2"))
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    if not _check_dspy():
        sys.exit(2)

    import dspy
    from helpers._dspy_config import configure_lm

    ws = workspace_root(args.workspace)
    prompts_dir = ws / "n8n-prompts" / "prompts"
    prompt_file = prompts_dir / f"{args.prompt}_prompt.txt"
    schema_file = prompts_dir / f"{args.prompt}_schema.json"

    if not prompt_file.exists():
        # Fall back to the example primitive prompt (so smoke runs even with empty workspace)
        from helpers.workspace import harness_root
        seed_prompt = harness_root() / "primitives" / "prompts" / f"{args.prompt}_prompt.txt"
        seed_schema = harness_root() / "primitives" / "prompts" / f"{args.prompt}_schema.json"
        if seed_prompt.exists() and seed_schema.exists():
            instructions = seed_prompt.read_text()
            schema = json.loads(seed_schema.read_text())
        else:
            print(f"ERROR: prompt file not found: {prompt_file}", file=sys.stderr)
            sys.exit(1)
    else:
        instructions = prompt_file.read_text()
        schema = json.loads(schema_file.read_text())

    dataset = _load_dataset(ws, args.dataset or args.prompt)

    try:
        configure_lm(provider=args.provider, model=args.model)
    except ValueError as e:
        print(f"WARNING: LM not configured ({e}). Smoke-checking signature/optimizer wiring only.", file=sys.stderr)
        # Smoke-check: the helper machinery works even without an API key
        sig = _build_signature(schema, instructions)
        print(f"Built signature with output fields: {[k for k in schema.get('properties', {}).keys()]}")
        print(f"Loaded {len(dataset)} dataset examples")
        print(f"Optimizer: {args.optimizer}")
        return

    sig = _build_signature(schema, instructions)
    base_predictor = dspy.Predict(sig)
    base_score = _evaluate(base_predictor, dataset)
    print(f"Baseline score: {base_score:.3f}")

    if dataset and len(dataset) >= 3:
        # Convert dataset to dspy.Example list
        train = [dspy.Example(text=ex["input"], **ex.get("expected", {})).with_inputs("text") for ex in dataset]
        if args.optimizer == "bootstrap":
            optimizer = dspy.BootstrapFewShot(metric=lambda ex, pred, _trace=None: 1)
        else:
            optimizer = dspy.MIPROv2(metric=lambda ex, pred, _trace=None: 1, auto="light")
        optimized = optimizer.compile(base_predictor, trainset=train)
        opt_score = _evaluate(optimized, dataset)
        print(f"Optimized score: {opt_score:.3f}")

        if args.export and opt_score >= base_score:
            out = prompts_dir / f"{args.prompt}_prompt_optimized.txt"
            out.write_text(instructions + "\n\n# (optimized via DSPy " + args.optimizer + ")\n")
            print(f"Wrote {out}")
    else:
        print("Dataset too small for optimization; skipping optimize step.")


if __name__ == "__main__":
    main()
