import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage

class WritingState(TypedDict):
    topic: str
    outline: str
    draft: str
    final: str

# ignore env load and llm call

def creating_outline(state: WritingState):
    writer = get_stream_writer()
    writer({"event": "start", "node": "create_outline"})
    prompt = f"Give me a tight 4-bullet outline for a short piece about: {state['topic']}"
    messages = [
        SystemMessage("You are a concise writer."),
        HumanMessage(prompt),
    ]
    result = llm.invoke(messages)
    writer({"event": "end", "node": "create_outline", "progress": 33})
    return {"outline": result.content}

def writing_draft(state: WritingState):
    writer = get_stream_writer()
    writer({"event": "start", "node": "write_draft"})
    prompt = (
        "Write a short piece based on this outline. Keep it natural and varied.\n"
        f"Topic: {state['topic']}\n"
        f"Outline:\n{state['outline']}"
    )
    messages = [
        SystemMessage("You are a professional writer."),
        HumanMessage(prompt),
    ]
    result = llm.invoke(messages)
    writer({"event": "end", "node": "write_draft", "progress": 66})
    return {"draft": result.content}

def polishing_draft(state: WritingState):
    writer = get_stream_writer()
    writer({"event": "start", "node": "polish"})
    prompt = (
        "Polish the draft to be clear and engaging in about 200 words.\n"
        f"Draft:\n{state['draft']}"
    )
    messages = [
        SystemMessage("You are a professional editor."),
        HumanMessage(prompt),
    ]
    result = llm.invoke(messages)
    writer({"event": "end", "node": "polish", "progress": 100})
    return {"final": result.content}

def build_graph():
    graph = StateGraph(WritingState)
    graph.add_node("create_outline", creating_outline)
    graph.add_node("write_draft", writing_draft)
    graph.add_node("polish", polishing_draft)
    graph.add_edge(START, "create_outline")
    graph.add_edge("create_outline", "write_draft")
    graph.add_edge("write_draft", "polish")
    graph.add_edge("polish", END)
    return graph.compile()

if __name__ == "__main__":
    graph = build_graph()
    initial_state: WritingState = {
        "topic": "The impact of AI",
        "outline": "",
        "draft": "",
        "final": "",
    }

    token_counts = {"values": 0, "updates": 0, "messages": 0, "custom": 0}
    in_messages = False

    for chunk in graph.stream(
        initial_state,
        # values: full state snapshot after each node finishes
        # updates: only the keys updated by each node
        # messages: LLM tokens
        # custom: arbitrary events emitted via get_stream_writer()
        stream_mode=["values", "updates", "messages", "custom"],
        version="v2",
    ):
        if isinstance(chunk, tuple):
            mode, data = chunk
            if mode == "messages":
                message, metadata = data
                content = getattr(message, "content", "")
                if content:
                    if not in_messages:
                        token_counts["messages"] += 1
                        print(f"\n=== [messages #{token_counts['messages']}] ===")
                        in_messages = True
                    print(content, end="", flush=True)
            else:
                if in_messages:
                    print()
                    in_messages = False
                token_counts[mode] += 1
                print(f"\n=== [{mode} #{token_counts[mode]}] ===")  
                print(data)
