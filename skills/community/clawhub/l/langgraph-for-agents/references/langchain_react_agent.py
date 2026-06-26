import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI 
from langchain.messages import SystemMessage, HumanMessage, AIMessage

# ignore env load and llm call


# =========================
# Create Tools
# =========================
def get_weather(city):
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# =========================
# Prompts
# =========================
def langchain_format_msg():
    messages = [
        HumanMessage("Hello, I am K. What is the weather in San Francisco?"),
    ]
    return messages

def openai_format_msg():
    messages = [{"role": "user", "content": "What is my name?"}]
    return messages


# =========================
# Build ReAct Agent
# =========================
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": langchain_format_msg()}
)
print("===Response of agent===")
print(result)

test_memory = agent.invoke(
    {"messages": openai_format_msg()}
)
print("\n===Test the memory of agent===")
print(test_memory)
