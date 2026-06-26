import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage, AIMessage

# ignore env load and llm call


# =========================
# Prompts
# =========================
def text_prompts_msg():
    message = "Hello, I am K. What is your name?"
    return message

def langchain_format_msg():
    messages = [
        SystemMessage("You are a helpful assistant."),
        HumanMessage("Hello, I am K. What is your name?"),
        AIMessage("My name is DeepSeek.")
    ]
    return messages


def openai_format_msg():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is your name?"},
        {"role": "assistant", "content": "My name is DeepSeek."},
        {"role": "user", "content": "What is my name?"}
    ]
    return messages


response_text_prompts = llm.invoke(text_prompts_msg())
print("===response_text_prompts===")
print(response_text_prompts.content)

response_langchain_format_messages = llm.invoke(langchain_format_msg())
print("\n===langchain_format_messages===")
print(response_langchain_format_messages.content)

response_openai_format_messages = llm.invoke(openai_format_msg())
print("\n===openai_format_messages===")
print(response_openai_format_messages.content)

