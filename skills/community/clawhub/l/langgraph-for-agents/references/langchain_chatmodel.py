import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# ignore env load and llm call
text_prompts = "Please give me a simple C programming example."

response = llm.invoke(text_prompts)

# ***************************
# LangChain ChatModel Response Structure
# ***************************
def print_langchain_response_structure(response):
    print("===Actual Content===\n")
    print(response.content)
    
    print(f"Response Type: {type(response)}")
    print(f"Response Class: {response.__class__.__name__}")
    print(f"Response Module: {response.__class__.__module__}")

    print(f"\nContent Type: {type(response.content)}")
    print(f"Content Length: {len(response.content)} characters")
    
    print(f"\nAdditional Kwargs: {response.additional_kwargs}")
    print(f"\nResponse Metadata: {response.response_metadata}")
    
    print(f"\nTool Calls: {response.tool_calls}")
    print(f"\nInvalid Tool Calls: {response.invalid_tool_calls}")

    metadata = response.response_metadata
    if 'token_usage' in metadata:
        usage = metadata['token_usage']
        print(f"Prompt Tokens: {usage.get('prompt_tokens', 'N/A')}")
        print(f"Completion Tokens: {usage.get('completion_tokens', 'N/A')}")
        print(f"Total Tokens: {usage.get('total_tokens', 'N/A')}")

    print(f"Model Name: {metadata.get('model_name', 'N/A')}")
    print(f"System Fingerprint: {metadata.get('system_fingerprint', 'N/A')}")
    print(f"Finish Reason: {metadata.get('finish_reason', 'N/A')}")
        
    print("===Content blocks - text===\n")
    print(response.content_blocks[0]['text'])

    print("===Raw JSON Structure===\n")
    response_json = response.model_dump()
    print(json.dumps(response_json, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print_langchain_response_structure(response)
