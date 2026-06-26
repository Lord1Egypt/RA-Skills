import os
from pprint import pprint

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver  
from langgraph.graph import StateGraph, START, MessagesState

# ignore env load and llm call


# =========================
# Build Workflow
# =========================
def build_graph():
    graph = StateGraph(MessagesState)
    
    graph.add_node("one chat node", chat_node)
    
    graph.add_edge(START, "one chat node")
    graph.add_edge("one chat node", END)
    return graph


if __name__ == "__main__":
    checkpointer = InMemorySaver()  
    workflow = build_graph().compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "1"}}
    
    print("===Running workflow===\n")
    state_1 = workflow.invoke({
        "messages": [HumanMessage(content="Hi, my name is Jack, please remember it.")]
    }, 
        config
    )
    pprint(state_1["messages"][-1].content)
    
    state_2 = workflow.invoke({
        "messages": [HumanMessage(content="Tell me a joke.")]
    }, 
        config
    )
    pprint(state_2["messages"][-1].content)
    
    print("===Testing memory===\n")
    state_3 = workflow.invoke({
        "messages": [HumanMessage(content="What is my name?")]
    }, 
        config
    )
    pprint(state_3["messages"][-1].content)
