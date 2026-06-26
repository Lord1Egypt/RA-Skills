import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.tools import tool

# ignore env load and llm call

# =========================
# Create Custom Tool
# =========================
@tool("add", description="Adds two numbers. Use this for addition problems.")
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    llm_with_tools = llm.bind_tools([add])
    prompt = "Please add 123 and 9873."
    
    messages = [HumanMessage(content=prompt)]
    response = llm_with_tools.invoke(prompt)
    
    while response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            tool_result = add.invoke(tool_call["args"])
            print(
                f"====Add result:====\n {tool_result}"
            )

            tool_message = ToolMessage(
                content=str(tool_result), tool_call_id=tool_call["id"]
            )
            messages.append(tool_message)
        response = llm_with_tools.invoke(messages)

    print("======Answer:======\n", response.content)
    