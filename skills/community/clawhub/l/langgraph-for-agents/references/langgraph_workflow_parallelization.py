"""
LangGraph Workflow: Parallelization
"""
import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# ignore env load and llm call

# =========================
# Prompts
# =========================
POSITIVE_VIEW_PROMPT = """
You are an optimist.
Please give a positive, optimistic view about the following topic:
{topic}
"""

NEGATIVE_VIEW_PROMPT = """
You are a pessimist.
Please give a negative, pessimistic view about the following topic:
{topic}
"""

SYNTHESIS_PROMPT = """
You are an objective rational decision-maker.
Please synthesize the following two distinct views about “{topic}” into a balanced, rational conclusion.

【Positive View】:
{positive_view}

【Negative View】:
{negative_view}
"""

# =========================
# Create State Schema
# =========================
class State(TypedDict):
    topic: str
    positive_view: str
    negative_view: str
    conclusion: str

# =========================
# Create Nodes
# =========================
def generate_positive_view(state: State):
    prompt = POSITIVE_VIEW_PROMPT.format(topic=state["topic"])
    response = llm.invoke(prompt)
    return {"positive_view": response.content}

def generate_negative_view(state: State):
    prompt = NEGATIVE_VIEW_PROMPT.format(topic=state["topic"])
    response = llm.invoke(prompt)
    return {"negative_view": response.content}

def synthesize_views(state: State):
    prompt = SYNTHESIS_PROMPT.format(
        topic=state["topic"],
        positive_view=state["positive_view"],
        negative_view=state["negative_view"]
    )
    response = llm.invoke(prompt)
    return {"conclusion": response.content}

# =========================
# Build Workflow
# =========================
workflow = StateGraph(State)

workflow.add_node("generate_positive_view", generate_positive_view)
workflow.add_node("generate_negative_view", generate_negative_view)
workflow.add_node("synthesize_views", synthesize_views)

workflow.add_edge(START, "generate_positive_view")
workflow.add_edge(START, "generate_negative_view")

workflow.add_edge("generate_positive_view", "synthesize_views")
workflow.add_edge("generate_negative_view", "synthesize_views")

workflow.add_edge("synthesize_views", END)

if __name__ == "__main__":
    # =========================
    # Execute Workflow
    # =========================
    input_state = State(
        topic="The Future of Artificial Intelligence",
        positive_view="",
        negative_view="",
        conclusion=""
    )
    
    graph = workflow.compile()
    output_state = graph.invoke(input_state)
    
    print("=" * 30)
    print(f"Topic: {output_state['topic']}")
    print("=" * 30)
    print("\nPositive View:")
    print(output_state['positive_view'])
    print("\nNegative View:")
    print(output_state['negative_view'])
    print("\n" + "=" * 30)
    print("Conclusion:")
    print(output_state['conclusion'])
