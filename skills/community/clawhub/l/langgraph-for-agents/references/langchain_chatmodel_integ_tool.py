import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, ToolMessage

# ignore env load and llm call


# =========================
# Create Tavily Search Tool
# =========================
tavily_tool = TavilySearch(
    max_results=3,
    topic="general",
)


if __name__ == "__main__":
    llm_with_tools = llm.bind_tools([tavily_tool])
    prompt = "Please tell me the latest AI news."
    
    messages = [HumanMessage(content=prompt)]
    response = llm_with_tools.invoke(prompt)
    
    while response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            tool_result = tavily_tool.invoke(tool_call["args"])
            print(
                f"====Search result:====\n {tool_result['results'][0]['content'][:200]}..."
            )

            tool_message = ToolMessage(
                content=str(tool_result["results"]), tool_call_id=tool_call["id"]
            )
            messages.append(tool_message)
        response = llm_with_tools.invoke(messages)

    print("======Answer:======\n", response.content)
