from langgraph.graph import StateGraph, END, START
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.search_node import search_node
from graphs.nodes.image_gen_node import image_gen_node
from graphs.nodes.clean_data_node import clean_data_node
from graphs.nodes.analysis_node import analysis_node

# Create state graph
builder = StateGraph(
    GlobalState,
    input_schema=GraphInput,
    output_schema=GraphOutput
)

# ========== Add Nodes ==========

# Search node
builder.add_node("search", search_node)

# Image generation node
builder.add_node("image_gen", image_gen_node)

# Data cleaning node
builder.add_node("clean_data", clean_data_node)

# Analysis node
builder.add_node(
    "analysis",
    analysis_node,
    metadata={
        "type": "agent",
        "llm_cfg": "config/analysis_llm_cfg.json"
    }
)

# ========== Set Edges ==========

# Start search and image generation in parallel from START
builder.add_edge(START, "search")
builder.add_edge(START, "image_gen")

# Clean data after search completes
builder.add_edge("search", "clean_data")

# Converge to analysis node after data cleaning and image generation complete
builder.add_edge(["clean_data", "image_gen"], "analysis")

# End after analysis completes
builder.add_edge("analysis", END)

# ========== Compile Graph ==========
main_graph = builder.compile()
