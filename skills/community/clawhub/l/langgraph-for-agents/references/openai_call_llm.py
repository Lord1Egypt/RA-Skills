import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# ignore env load

client = OpenAI() # ignore params

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a coding assistant."},
        {"role": "user", "content": "Please give me a simple C++ example."}
    ],
)

# ***************************
# OpenAI API Response structure
# ***************************
def print_response_structure(response):
    print("===Actual Content===\n")
    print(response.choices[0].message.content)
    
    print(f"Response Type: {type(response)}")
    print(f"Response ID: {response.id}")
    print(f"Model Used: {response.model}")
    print(f"Created At: {response.created}")
    print(f"Object Type: {response.object}")

    print(f"Prompt Tokens: {response.usage.prompt_tokens}")
    print(f"Completion Tokens: {response.usage.completion_tokens}")
    print(f"Total Tokens: {response.usage.total_tokens}")

    print(f"Number of Choices: {len(response.choices)}")

    for i, choice in enumerate(response.choices):
        print(f"\n--- Choice {i} ---")
        print(f"Index: {choice.index}")
        print(f"Finish Reason: {choice.finish_reason}")
        print(f"Message Role: {choice.message.role}")
        print(f"Message Content Length: {len(choice.message.content)} characters")

    print(f"Tool Calls: {response.choices[0].message.tool_calls}")

    print("===Raw JSON Structure===\n")
    response_json = response.model_dump()
    print(json.dumps(response_json, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print_response_structure(response)
