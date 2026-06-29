"""
🌀 Example 3: Cross-harness adapters (Claude, OpenAI, LangChain, AutoGen, Hermes, custom).

The guard exposes a uniform interface regardless of the LLM harness you use.
"""

from anti_loop import AntiLoop
from anti_loop.adapters import CrossHarnessAdapters


# Simulated responses from different harnesses
class FakeAnthropicResponse:
    """Mimics: anthropic.Anthropic().messages.create(...)"""
    content = [type("Block", (), {"text": "I should look up file X again."})()]


class FakeOpenAIResponse:
    """Mimics: openai.OpenAI().chat.completions.create(...)"""
    class Choice:
        class Message:
            content = "Searching for X..."
        message = Message()
    choices = [Choice()]


# LangChain, AutoGen, Hermes all return dicts or simple objects
fake_langchain = type("LC", (), {"content": "I'll try the same thing."})()
fake_autogen = {"content": "Same again."}
fake_hermes = {"message": "And once more."}


# A response with a custom attribute (your own agent, perhaps)
class MyCustomResponse:
    output = "Last attempt on the same action."


def main():
    guard = AntiLoop(mode="heal", max_iter=5)
    intent = "find file X"

    print("=== Cross-harness demo (5 different LLM APIs, 1 guard) ===\n")

    responses = [
        ("Claude/Anthropic", CrossHarnessAdapters.adapt_anthropic(FakeAnthropicResponse())),
        ("OpenAI", CrossHarnessAdapters.adapt_openai(FakeOpenAIResponse())),
        ("LangChain", CrossHarnessAdapters.adapt_langchain(fake_langchain)),
        ("AutoGen", CrossHarnessAdapters.adapt_autogen(fake_autogen)),
        ("Hermes", CrossHarnessAdapters.adapt_hermes(fake_hermes)),
        ("Custom (yours)", CrossHarnessAdapters.adapt_custom(MyCustomResponse())),
    ]

    for label, text in responses:
        # Feed the same repetitive text 4 times to trigger a loop
        for turn in range(4):
            result = guard.observe(text, intent=intent)
            if result["intervene"]:
                d = result["directive"]
                print(f"  [{label:18s}] turn {turn+1}: 🛑 {d['action']}: {d.get('system_message', d.get('message', ''))[:60]}")
                break
        else:
            print(f"  [{label:18s}] no intervention (4 turns ok)")


if __name__ == "__main__":
    main()
