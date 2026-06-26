import os
from pprint import pprint
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

# ignore env load and llm call

# =========================
# Create Tavily Search Tool
# =========================
tavily_tool = TavilySearch(
    max_results=3,
    topic="general",
)


# =========================
# Create React Agent
# =========================
agent = create_agent(
    model=llm,
    tools=[tavily_tool],
    system_prompt="You are a helpful assistant",
)


# =========================
# Prompts
# =========================
def langchain_format_msg():
    messages = [
        HumanMessage("Please tell me 3~5 latest AI news."),
    ]
    return messages


if __name__ == "__main__":
    # result = agent.invoke({"messages": langchain_format_msg()})
    for step in agent.stream(
        {"messages": langchain_format_msg()},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
