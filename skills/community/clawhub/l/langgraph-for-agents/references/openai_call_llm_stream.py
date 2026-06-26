import os
from openai import OpenAI
from dotenv import load_dotenv

# ignore env load

def stream_response():
    client = OpenAI() # ignore params

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a coding assistant."},
            {"role": "user", "content": "Please give me a simple C++ example."}
        ],
        stream=True,
        stream_options={"include_usage": True}
    )

    for chunk in response:
        if hasattr(chunk, "choices") and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            if hasattr(choice, "delta") and hasattr(choice.delta, "content"):
                print(choice.delta.content, end='', flush=True)

if __name__ == "__main__":
    stream_response()
