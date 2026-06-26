import os
import uuid

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore

# ignore env load and llm call


# =========================
# Create Nodes
# =========================
def chat_node_with_memories(state: MessagesState, config: RunnableConfig, *, store: BaseStore):
    user_id = config["configurable"]["user_id"]

    namespace = (user_id, "memories")

    memories = store.search(
        namespace,
    )
    
    messages = state["messages"]
    additional_prompt = f"""
    You are a helpful assistant.
    You can refer to the following memories:
    {memories}
    """
    messages.append(SystemMessage(content=additional_prompt))
    result = llm.invoke(messages)
    return {"messages": [result]}


# =========================
# Build Workflow
# =========================
def build_graph():
    graph = StateGraph(MessagesState)
    
    graph.add_node("one chat node", chat_node_with_memories)
    
    graph.add_edge(START, "one chat node")
    graph.add_edge("one chat node", END)
    return graph


if __name__ == "__main__":
    # Create in-memory store and checkpointer
    in_memory_store = InMemoryStore()
    checkpointer = InMemorySaver()
    workflow = build_graph().compile(checkpointer=checkpointer, store=in_memory_store)
    
    # Manually add memories
    user_id = "1"
    namespace_for_memory = (user_id, "memories")
    
    config_1 = {"configurable": {"thread_id": "1", "user_id": user_id}}
    config_2 = {"configurable": {"thread_id": "2", "user_id": user_id}}
    
    memory_id = str(uuid.uuid4())
    memory = {"game_preference": "I like JRPG"}

    in_memory_store.put(namespace_for_memory, memory_id, memory)
    
    # Test long-term memory(Store)
    messages_1 = [HumanMessage(content="What is my game preference?")]
    response_1 = workflow.invoke({"messages": messages_1}, config=config_1)
    print("Response 1:", response_1["messages"][-1].content)
    
    messages_2 = [HumanMessage(content="What is my game preference?")]
    response_2 = workflow.invoke({"messages": messages_2}, config=config_2)
    print("Response 2:", response_2["messages"][-1].content)
    