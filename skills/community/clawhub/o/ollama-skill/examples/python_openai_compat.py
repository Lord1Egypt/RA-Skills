from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)

resp = client.chat.completions.create(
    model="gpt-oss:20b",
    messages=[{"role": "user", "content": "Say this is a compatibility test."}],
)

print(resp.choices[0].message.content)
