"""
LangGraph Workflow: Prompt Chaining
"""
import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage

# ignore env load and llm call


# =========================
# Prompts
# =========================
GENERATE_MESSAGES_FROM_USER_PERSONA_PROMPT = """
You are a senior scholar in anthropology and sociology.

Your task is to generate dialogues that match the given user persona, where the dialogue is between the user and an AI assistant, in a question-and-answer format.
Note:
- All characteristics in the provided user persona refer to the same user.
- The persona contains more than one trait; each trait must be reflected in the dialogue, and one trait can span multiple dialogue turns.
- You do not need to follow the order of traits; conversations for each trait can appear randomly.
- The output should be a list in which every element is either a HumanMessage or an AIMessage object.

User persona: 
{user_persona_ground_truth}

Please generate {num_messages} dialogue turns that fit the user persona.

A simple example:

User persona:
[
    "The user is a woman who enjoys photography.",
    "The user dislikes spicy food."
]

Generated conversation:
[
    HumanMessage("Hello"),
    AIMessage("Hello, I'm your personal assistant."),
    HumanMessage("Hi, do you have any camera recommendations for women? I've been using a Canon 750D and want to upgrade."),
    AIMessage("I'd suggest the Fujifilm XT30 Mark III, Fujifilm's new 2025 model—compact, stylish, and reasonably priced.")
    HumanMessage("Please recommend some restaurants in Yangpu District, Shanghai; no spicy dishes, I prefer light flavors."),
    AIMessage("Try Shanghai Grandma—sweet and mild tastes, mostly braised, stewed, or steamed dishes, absolutely no heat.")
]
"""

EXTRACT_USER_PERSONA_PROMPT = """
You are a senior scholar in anthropology and social science.

Your task is to analyze the provided conversation and generate a user profile that matches the characteristics shown in that conversation. The conversation is between a user and an AI assistant, in a question-and-answer format.

Note:
- All features mentioned in the conversation refer to the same user.
- The user profile should be presented as a list, where each element is a string describing one characteristic of the user.

The conversation is as follows:
{generated_messages}

A simple example:

Conversation:
[
    HumanMessage("Hello"),
    AIMessage("Hello, I'm your personal assistant"),
    HumanMessage("Hi, do you have any camera recommendations for women? I've been using a Canon 750D and want to upgrade."),
    AIMessage("I recommend trying the Fujifilm XT30 Mark III, Fujifilm's newly released camera in 2025. It's compact and stylish, and the price is reasonable."),
    HumanMessage("Please recommend some restaurants in Yangpu District, Shanghai. No spicy food; I prefer something light."),
    AIMessage("I recommend Shanghai Grandma. The flavors lean sweet and lightly salty, with cooking methods like braising, stewing, and steaming, so there's no need to worry about spiciness.")
]

User profile:
[
    "The user is a woman who enjoys photography.",
    "The user dislikes spicy food."
]
"""

EVALUATE_EXTRACTED_PERSONA_PROMPT = """
You are a senior scholar in anthropology and sociology.

There is an intelligent agent that can automatically analyze and extract user personas from conversations.
Your task is to analyze the gap between the real user persona and the persona extracted by this agent.

Note:
- Both the real user persona and the persona extracted by this agent are lists, each element in the list is a string, and each string represents a user persona characteristic.
- The evaluation result you need to provide is a string, the content of which is a comparative analysis of the real user persona and the persona extracted by this agent.

Real user persona:
{user_persona_ground_truth}

Persona extracted by this agent:
{extracted_persona}
"""


# =========================
# Create State Schema
# =========================
class State(TypedDict):
    user_persona_ground_truth: list[str]
    num_messages: int
    generated_messages: list[HumanMessage | AIMessage]
    extracted_persona: list[str]
    evaluation_result: str


# =========================
# Create Nodes
# =========================
def generate_messages_from_user_persona(state: State):
    prompt = GENERATE_MESSAGES_FROM_USER_PERSONA_PROMPT.format(
        user_persona_ground_truth=state["user_persona_ground_truth"],
        num_messages=state["num_messages"],
    )
    response = llm.invoke(prompt)
    state["generated_messages"] = response.content
    return state

def extract_user_persona(state: State):
    prompt = EXTRACT_USER_PERSONA_PROMPT.format(
        generated_messages=state["generated_messages"],
    )
    response = llm.invoke(prompt)
    state["extracted_persona"] = response.content
    return state

def evaluate_extracted_persona(state: State):
    prompt = EVALUATE_EXTRACTED_PERSONA_PROMPT.format(
        user_persona_ground_truth=state["user_persona_ground_truth"],
        extracted_persona=state["extracted_persona"],
    )
    response = llm.invoke(prompt)
    state["evaluation_result"] = response.content
    return state


# =========================
# Build Workflow
# =========================
workflow = StateGraph(State)

workflow.add_node("generate_messages_from_user_persona", generate_messages_from_user_persona)
workflow.add_node("extract_user_persona", extract_user_persona)
workflow.add_node("evaluate_extracted_persona", evaluate_extracted_persona)

workflow.add_edge(START, "generate_messages_from_user_persona")
workflow.add_edge("generate_messages_from_user_persona", "extract_user_persona")
workflow.add_edge("extract_user_persona", "evaluate_extracted_persona")
workflow.add_edge("evaluate_extracted_persona", END)


if __name__ == "__main__":
    # =========================
    # Execute Workflow
    # =========================
    input_state = State(
        user_persona_ground_truth=["The user is a male, addicted to playing games", "The user likes spicy food."],
        num_messages=4,
        generated_messages=[],
        extracted_persona=[],
        evaluation_result="",
    )
    graph = workflow.compile()
    output_state = graph.invoke(input_state)
    print(output_state)
