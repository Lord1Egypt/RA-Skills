import anthropic

client = anthropic.Anthropic(
    base_url="http://localhost:11434",
    api_key="ollama",
)

message = client.messages.create(
    model="qwen3-coder",
    max_tokens=512,
    messages=[{"role": "user", "content": "Write a short Python docstring example."}],
)

print(message.content[0].text)
