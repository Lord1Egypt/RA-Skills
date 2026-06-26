"""
LangGraph Workflow: Routing
"""
import os
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

# ignore env load and llm call


# =========================
# Prompts
# =========================
CLASSIFY_PROMPT = """
You are a routing assistant.
Determine whether the following user input requires a "thinking model (multi-step reasoning)" or a "non-thinking model (direct answer)".

Return only one of the following:
- thinking
- non-thinking

User input is as follows:
{query}
"""

THINKING_PROMPT = """
Query: {query}
"""

NON_THINKING_PROMPT = """
Query: {query}
"""


# =========================
# Create State Schema
# =========================
class State(TypedDict):
    query: str
    category: str
    output: str
    reasoning: str
    model_used: str


# =========================
# Create Nodes
# =========================
def routing_model(state: State):
    prompt = CLASSIFY_PROMPT.format(query=state["query"])
    response = llm_judge.invoke(prompt)
    category = response.content.strip().lower()
    if category != "thinking":
        category = "non-thinking"
    return {"category": category}

def thinking_model(state: State):
    prompt = THINKING_PROMPT.format(query=state["query"])
    response = llm_thinking.invoke(prompt)
    reasoning = ""
    try:
        reasoning = getattr(response, "additional_kwargs", {}).get("reasoning_content", "")
    except Exception:
        reasoning = ""
    return {
        "output": response.content,
        "reasoning": reasoning,
        "model_used": "deepseek-reasoner",
    }

def non_thinking_model(state: State):
    prompt = NON_THINKING_PROMPT.format(query=state["query"])
    response = llm_non_thinking.invoke(prompt)
    return {
        "output": response.content,
        "reasoning": "",
        "model_used": "deepseek-chat",
    }


# =========================
# Routing Logic
# =========================
def route_decision(state: State) -> Literal["thinking", "non_thinking"]:
    category = state["category"]
    if category == "thinking":
        return "thinking"
    else:
        return "non_thinking"


# =========================
# Build Workflow
# =========================
workflow = StateGraph(State)

workflow.add_node("routing_model", routing_model)
workflow.add_node("thinking_model", thinking_model)
workflow.add_node("non_thinking_model", non_thinking_model)

workflow.add_edge(START, "routing_model")

workflow.add_conditional_edges(
    "routing_model",
    route_decision,
    {
        "thinking": "thinking_model",
        "non_thinking": "non_thinking_model",
    },
)

workflow.add_edge("thinking_model", END)
workflow.add_edge("non_thinking_model", END)

if __name__ == "__main__":
    # =========================
    # Execute Workflow
    # =========================
    graph = workflow.compile()

    print("\n--- Case 1: Need Thinking ---")
    input_state_1 = State(
        query="How many 's' are there in the word 'Mississippi'?",
        category="",
        output="",
        reasoning="",
        model_used="",
    )
    output_state_1 = graph.invoke(input_state_1)
    print(f"Category: {output_state_1['category']} | Model Used: {output_state_1['model_used']}")
    if output_state_1.get("reasoning"):
        print("Thinking Process:")
        print(output_state_1["reasoning"])
    print("Answer:")
    print(output_state_1["output"])

    print("\n--- Case 2: Direct Answer ---")
    input_state_2 = State(
        query="Please summarize the definition of Artificial Intelligence.",
        category="",
        output="",
        reasoning="",
        model_used="",
    )
    output_state_2 = graph.invoke(input_state_2)
    print(f"Category: {output_state_2['category']} | Model Used: {output_state_2['model_used']}")
    print("Answer:")
    print(output_state_2["output"])
