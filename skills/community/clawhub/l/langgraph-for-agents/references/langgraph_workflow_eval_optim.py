"""
LangGraph Workflow: Evaluator-optimizer
"""
import os
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

# ignore env load and llm call

# =========================
# Prompts
# =========================
CANDIDATE_PROMPT = """
You are a candidate for the AI Engineer position. 
You will be asked questions, please answer them.

Here is your first question:
{query}
You can take into account the following feedback if it's not empty:
{feedback}

Please only answer the question, do not add any extra information.
"""

INTERVIEWER_PROMPT = """
You are an interviewer with high standards who enjoys delving deeply into candidates' understanding.
You ask a question about the AI Engineer position.
Here is the question:
{query}
And here is the answer of the candidate:
{answer}
If you think the answer is up to your standard, please say "good".
If you think the answer is not up to your standard, please say "not good", and give the feedback.

Please follow the JSON format:
{{   
    "grade": "string",
    "feedback": "string"
}}
"""


# =========================
# Create State Schema
# =========================
class Feedback(BaseModel):
    grade: Literal["good", "not good"] = Field(
        description="Decide if the answer is good or not.",
    )
    feedback: str = Field(
        description="If the answer is not good, provide feedback on how to improve it.",
    )

class State(TypedDict):
    query: str
    answer: str
    feedback: Feedback
    

# =========================
# Create Nodes
# =========================
def candidate_node(state: State):
    query = state["query"]
    feedback = state["feedback"]
    prompt = CANDIDATE_PROMPT.format(
        query=query, 
        feedback=feedback.feedback
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    state["answer"] = response.content
    
    print("\nCandidate answer:\n", state["answer"])
    
    return state

def interviewer_node(state: State):
    query = state["query"]
    answer = state["answer"]
    prompt = INTERVIEWER_PROMPT.format(query=query, answer=answer)
    response = llm.invoke([HumanMessage(content=prompt)])
    json_str = response.content[response.content.find('{'):response.content.rfind('}')+1]
    state["feedback"] = Feedback.model_validate_json(json_str)
    
    print("\nInterviewer feedback:\n", state["feedback"])
    
    return state


# =========================
# Routing Logic
# =========================
def route_decision(state: State) -> Literal["good", "not good"]:
    feedback = state["feedback"]
    if feedback.grade == "good":
        return "good"
    else:
        return "not good"


# =========================
# Build Workflow
# =========================
workflow = StateGraph(State)

workflow.add_node("candidate_node", candidate_node)
workflow.add_node("interviewer_node", interviewer_node)

workflow.add_edge(START, "candidate_node")
workflow.add_edge("candidate_node", "interviewer_node")

workflow.add_conditional_edges(
    "interviewer_node",
    route_decision,
    {
        "good": END,
        "not good": "candidate_node",
    },
)

workflow.add_edge("interviewer_node", END)


if __name__ == "__main__":
    # =========================
    # Execute Workflow
    # =========================
    initial_state = {
        "query": "How do the parameters of a Large Language Model's normalization layer differ between training and testing?",
        "answer": "",
        "feedback": Feedback(grade="good", feedback=""),
    }
    graph = workflow.compile()
    result = graph.invoke(initial_state)
    print(result)
