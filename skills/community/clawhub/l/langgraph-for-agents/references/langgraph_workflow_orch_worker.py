import os
import operator
import json
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.types import Send
from langchain_core.messages import SystemMessage, HumanMessage

# ignore env load and llm call

# =========================
# Prompts
# =========================
planner_prompt = """
You are a well-known storyteller. 
Your task is to create a compelling story plan based on a given topic. 
Break the story down into 3 distinct chapters. 
For each chapter, provide a short name and a one-sentence description of the key events that should happen. 
Respond with nothing but the JSON object.

Here is an example:
{
    "chapters": [
        {"name": "Chapter 1", "description": "The beginning of the story"},
        {"name": "Chapter 2", "description": "The middle of the story"},
        {"name": "Chapter 3", "description": "The conclusion of the story"}
    ]
}
"""

writer_prompt = """
You are a creative writer. 
Your task is to write a chapter of a story based on a given topic and chapter description. 
The chapter should be 4-5 sentences long. 
Respond with nothing but the chapter content.
"""


# =========================
# TypedDicts for State
# =========================
class Chapter(TypedDict):
    name: str
    description: str


# =========================
# Create State Schema
# =========================
# Orchestrator State
class OrchestratorState(TypedDict):
    topic: str  # The initial story prompt
    story_plan: dict  # The generated plan for the story
    completed_chapters: Annotated[
        list[str], operator.add
    ]  # Chapters written by workers
    final_story: str  # The final completed story


# Worker State
class WorkerState(TypedDict):
    chapter: Chapter  # The plan for a single chapter
    completed_chapters: Annotated[
        list[str], operator.add
    ]  # The list to append the written chapter to


# =========================
# Create Nodes
# =========================
def orchestrator(state: OrchestratorState):
    response = planner_llm.invoke(
        [
            SystemMessage(
                content=planner_prompt
            ),
            HumanMessage(content=f"Story Topic: {state['topic']}"),
        ]
    )
    
    content = response.content
    json_str = content[content.find('{') : content.rfind('}')+1]
    plan = json.loads(json_str)

    return {"story_plan": plan}

def llm_call(state: WorkerState):
    chapter_name = state["chapter"]["name"]
    chapter_description = state["chapter"]["description"]

    chapter_content = writer_llm.invoke(
        [
            SystemMessage(
                content=writer_prompt
            ),
            HumanMessage(
                content=f"Chapter Name: {chapter_name}\nChapter Description: {chapter_description}"
            ),
        ]
    ).content

    return {"completed_chapters": [f"## {chapter_name}\n\n{chapter_content}"]}


def synthesizer(state: OrchestratorState):
    final_story = "\n\n".join(state["completed_chapters"])

    return {"final_story": final_story}

def assign_workers(state: OrchestratorState):
    return [
        Send("llm_call", {"chapter": chapter})
        for chapter in state["story_plan"]["chapters"]
    ]


# =========================
# Build Workflow
# =========================
workflow = StateGraph(OrchestratorState)

workflow.add_node("orchestrator", orchestrator)
workflow.add_node("llm_call", llm_call)
workflow.add_node("synthesizer", synthesizer)

workflow.add_edge(START, "orchestrator")
workflow.add_conditional_edges("orchestrator", assign_workers, ["llm_call"])
workflow.add_edge("llm_call", "synthesizer")
workflow.add_edge("synthesizer", END)

graph = workflow.compile()


if __name__ == "__main__":
    # =========================
    # Execute Workflow
    # =========================
    story_topic = "A group of high school students wake up in an unfamiliar school and are told they must participate in a deadly game."

    initial_state = {"topic": story_topic, "completed_chapters": []}

    final_state = graph.invoke(initial_state)

    print("\n\n--- FINAL STORY ---")
    print(final_state["final_story"])
