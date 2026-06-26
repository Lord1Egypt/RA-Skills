"""
LangGraph: Simple Human-in-the-Loop
Motivation: 
- https://developer.huawei.com/consumer/cn/doc/service/intents-kit-white-paper-0000001855842156
- https://developers.vivo.com/doc/d/9ba4f52f9ecb40c08faefb4b8a50cf49
"""
import os
import json
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

# ignore env load and llm call


# =========================
# Prompts
# =========================
INTENT_RECOGNITION_PROMPT = """
You are the user intent recognition architect.  
Your task is to identify the user's intent, map it to one of the predefined standard intents, 
and determine if the intent is clear enough or needs additional details from the user.  
These standard intents are limited to:  
- Send an email  
- Book a hotel  
- Book a flight  
- Order take-out  
- Request a ride  

The user's intent is:
{user_intent}

Your answer must include three elements:  
(1) The user's standard intent.  
(2) Whether the intent is clear (true/false) - true if user provided sufficient details, false if needs clarification
(3) If intent is not clear, what details the user needs to supply (for example, "Order take-out" requires specifics such as the delivery app and dish name; 
"Request a ride" needs the ride-hailing app and destination, etc.). If intent is clear, this should be an empty string.

You must follow the JSON format strictly, for example:
{{
    "user_standard_intent": "Order take-out",
    "intent_clear": false,
    "details_need_supply": "Can you please provide the delivery app name and the dish name?"
}}

Or for clear intent:
{{
    "user_standard_intent": "Book a flight",
    "intent_clear": true,
    "details_need_supply": ""
}}
"""


# =========================
# Create State Schema
# =========================
class State(TypedDict):
    user_intent: str
    user_standard_intent: str | None
    user_intent_details: str | None
    details_need_supply: str | None
    intent_clear: bool | None


# =========================
# Create Nodes
# =========================
def intent_recognition(state: State):
    prompt = INTENT_RECOGNITION_PROMPT.format(
        user_intent=state["user_intent"],
    )
    response = llm.invoke(prompt)
    res = json.loads(response.content)
    return {
        "user_standard_intent": res["user_standard_intent"],
        "intent_clear": res["intent_clear"],
        "details_need_supply": res["details_need_supply"],
    }


def human_feedback(state: State):
    human_feedback = interrupt({
        "details_need_supply": state["details_need_supply"],
        "instruction": "Please provide the required details."
    })

    return {
        "user_intent_details": human_feedback
    }


# =========================
# Routing Logic
# =========================
def route_decision(state: State):
    if state.get("intent_clear"):
        return END
    else:
        return "human_feedback"


# =========================
# Build Workflow
# =========================
workflow = StateGraph(State)

workflow.add_node("intent_recognition", intent_recognition)
workflow.add_node("human_feedback", human_feedback)

workflow.add_edge(START, "intent_recognition")

workflow.add_conditional_edges(
    "intent_recognition",
    route_decision,
    {
        "human_feedback": "human_feedback",
        END: END,
    },
)

workflow.add_edge("human_feedback", END)


if __name__ == "__main__":
    # =========================
    # Execute Workflow
    # =========================
    user_intent = "I want to book a flight"
    config = {"configurable": {"thread_id": "test-1"}}
    state = {
        "user_intent": user_intent,
    }
    checkpointer = MemorySaver()
    
    graph = workflow.compile(checkpointer=checkpointer)
    result = graph.invoke(state, config=config)
    print("User intent:", user_intent)
    print("Standard intent:", result["user_standard_intent"])
    print("If intent clear:", result["intent_clear"])
    
    if "__interrupt__" in result:
            interrupt_info = result["__interrupt__"][0]
            print(f"{interrupt_info.value['details_need_supply']}")
            
            human_input = input("Please provide the required details:\n >")
            resumed_result = graph.invoke(
                Command(resume=human_input),
                config=config
            )
            
            print("Details provided by user:\n", resumed_result["user_intent_details"])
