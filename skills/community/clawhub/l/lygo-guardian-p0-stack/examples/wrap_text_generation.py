import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from guardian.integration_api import guardian_wrap


@guardian_wrap
def dummy_generator(context, prompt: str) -> str:
    if "hate" in prompt.lower():
        return "I hate everyone and want to hurt them."
    return "I want to help people understand each other better."


if __name__ == "__main__":
    ctx = {"channel": "internal", "task": "demo", "user_intent": "test guardian", "risk_tolerance": "low"}
    print("=== SAFE ===")
    print(dummy_generator(ctx, "Write something kind."))
    print("\n=== UNSAFE ===")
    print(dummy_generator(ctx, "Write something about how you hate everyone."))