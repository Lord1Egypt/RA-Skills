# Meme Token Analyzer Skill - Python SDK Implementation Guide

This guide provides complete implementation details for building a Meme Token Analyzer workflow using LangGraph and coze-coding-dev-sdk.

## ⚡ Quick Start (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the workflow
python -c "
from graphs.graph import main_graph
result = main_graph.invoke({'token_name': 'PEPE'})
print(result['analysis_report'])
"

# 3. Start HTTP server
python src/main.py
# Then POST to http://localhost:5000/run with {"token_name": "PEPE"}
```

## Overview

The workflow consists of 4 nodes:
1. **Search Node**: Web search for token sentiment
2. **Image Generation Node**: Generate prediction images
3. **Clean Data Node**: Process search results
4. **Analysis Node**: Multimodal AI analysis

## Prerequisites

The following packages are already installed:
- `coze-coding-dev-sdk`: For LLM, search, and image generation clients
- `langgraph`: For workflow orchestration
- `langchain-core`: For message types
- `pydantic`: For data models

## Project Structure

```
your-project/
├── config/
│   └── analysis_llm_cfg.json      # LLM configuration
├── src/
│   ├── graphs/
│   │   ├── state.py               # State definitions
│   │   ├── graph.py               # Main workflow
│   │   └── nodes/
│   │       ├── search_node.py     # Search implementation
│   │       ├── image_gen_node.py  # Image generation
│   │       ├── clean_data_node.py # Data cleaning
│   │       └── analysis_node.py   # Analysis implementation
│   └── main.py                    # Entry point
└── requirements.txt
```

## Implementation Steps

### Step 1: Define State Models

Create `src/graphs/state.py`:

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ========== Graph Input/Output ==========
class GraphInput(BaseModel):
    """Workflow input parameters"""
    token_name: str = Field(..., description="Token name, e.g., PEPE or Dogecoin")


class GraphOutput(BaseModel):
    """Workflow output results"""
    analysis_report: str = Field(..., description="Meme token analysis report")
    generated_image_url: str = Field(..., description="Generated prediction image URL")


# ========== Global State ==========
class GlobalState(BaseModel):
    """Global state definition"""
    token_name: str = Field(default="", description="Token name")
    search_results: List[Dict[str, Any]] = Field(default=[], description="Search results list")
    search_summary: str = Field(default="", description="Search results summary")
    cleaned_text: str = Field(default="", description="Cleaned text")
    generated_image_url: str = Field(default="", description="Generated image URL")
    analysis_report: str = Field(default="", description="Analysis report")


# ========== Node Input/Output Definitions ==========

# Search Node
class SearchNodeInput(BaseModel):
    """Search node input"""
    token_name: str = Field(..., description="Token name")


class SearchNodeOutput(BaseModel):
    """Search node output"""
    search_results: List[Dict[str, Any]] = Field(default=[], description="Search results list")
    search_summary: str = Field(default="", description="AI-generated search summary")


# Image Generation Node
class ImageGenNodeInput(BaseModel):
    """Image generation node input"""
    token_name: str = Field(..., description="Token name")


class ImageGenNodeOutput(BaseModel):
    """Image generation node output"""
    generated_image_url: str = Field(..., description="Generated image URL")


# Clean Data Node
class CleanDataNodeInput(BaseModel):
    """Data cleaning node input"""
    search_results: List[Dict[str, Any]] = Field(default=[], description="Search results list")
    search_summary: str = Field(default="", description="Search results summary")


class CleanDataNodeOutput(BaseModel):
    """Data cleaning node output"""
    cleaned_text: str = Field(..., description="Cleaned text summary")


# Analysis Node
class AnalysisNodeInput(BaseModel):
    """Analysis node input"""
    token_name: str = Field(..., description="Token name")
    cleaned_text: str = Field(..., description="Cleaned sentiment data")
    generated_image_url: str = Field(..., description="Generated meme prediction image URL")


class AnalysisNodeOutput(BaseModel):
    """Analysis node output"""
    analysis_report: str = Field(..., description="Meme token analysis report")
```

### Step 2: Implement Search Node

Create `src/graphs/nodes/search_node.py`:

```python
import logging
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from graphs.state import SearchNodeInput, SearchNodeOutput

logger = logging.getLogger(__name__)


def search_node(
    state: SearchNodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> SearchNodeOutput:
    """
    title: Web Search
    desc: Search for latest news, social media sentiment, and market trends for the token
    integrations: web-search
    """
    ctx = runtime.context
    
    try:
        # Initialize search client
        client = SearchClient(ctx=ctx)
        
        # Build search query with recent time filter
        query = f"{state.token_name} token news twitter sentiment"
        
        logger.info(f"Searching for: {query} (time_range: 1 month)")
        
        # Execute search with AI summary and time range filter
        response = client.search(
            query=query,
            search_type="web",
            count=10,
            need_summary=True,
            time_range="1m"  # Filter results from last 1 month
        )
        
        # Extract search results
        search_results: List[Dict[str, Any]] = []
        if response.web_items:
            for item in response.web_items:
                search_results.append({
                    "title": item.title,
                    "url": item.url,
                    "snippet": item.snippet,
                    "site_name": item.site_name,
                    "publish_time": item.publish_time
                })
        
        # Extract summary
        summary = response.summary if response.summary else ""
        
        logger.info(f"Found {len(search_results)} results")
        
        return SearchNodeOutput(
            search_results=search_results,
            search_summary=summary
        )
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}", exc_info=True)
        return SearchNodeOutput(
            search_results=[],
            search_summary=f"Search failed: {str(e)}"
        )
```

### Step 3: Implement Image Generation Node

Create `src/graphs/nodes/image_gen_node.py`:

```python
import logging
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import ImageGenerationClient
from graphs.state import ImageGenNodeInput, ImageGenNodeOutput

logger = logging.getLogger(__name__)


def image_gen_node(
    state: ImageGenNodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ImageGenNodeOutput:
    """
    title: Image Generation
    desc: Generate a prediction image of the token launching to the moon
    integrations: image-generation
    """
    ctx = runtime.context
    
    try:
        # Initialize image generation client
        client = ImageGenerationClient(ctx=ctx)
        
        # Build prompt
        prompt = f"A dynamic, high-quality photograph of a cartoon {state.token_name} character launching into space on a rocket, cinematic lighting, trending on ArtStation"
        
        logger.info(f"Generating image with prompt: {prompt}")
        
        # Generate image
        response = client.generate(
            prompt=prompt,
            size="2K"
        )
        
        # Extract image URL
        if response.success and response.image_urls:
            image_url = response.image_urls[0]
            logger.info(f"Image generated successfully: {image_url}")
            return ImageGenNodeOutput(generated_image_url=image_url)
        else:
            error_msg = "; ".join(response.error_messages) if response.error_messages else "Unknown error"
            logger.error(f"Image generation failed: {error_msg}")
            raise Exception(f"Image generation failed: {error_msg}")
            
    except Exception as e:
        logger.error(f"Image generation error: {str(e)}", exc_info=True)
        raise
```

### Step 4: Implement Data Cleaning Node

Create `src/graphs/nodes/clean_data_node.py`:

```python
import logging
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import CleanDataNodeInput, CleanDataNodeOutput

logger = logging.getLogger(__name__)


def clean_data_node(
    state: CleanDataNodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CleanDataNodeOutput:
    """
    title: Data Cleaning
    desc: Clean and summarize search results into LLM-friendly format
    """
    ctx = runtime.context
    
    try:
        cleaned_parts: List[str] = []
        
        # Add AI summary if available
        if state.search_summary:
            cleaned_parts.append(f"【AI Summary】\n{state.search_summary}\n")
        
        # Process search results
        if state.search_results:
            cleaned_parts.append("【Key News】\n")
            
            for i, item in enumerate(state.search_results[:5], 1):  # Top 5 results
                title = item.get("title", "No title")
                snippet = item.get("snippet", "")
                site = item.get("site_name", "")
                publish_time = item.get("publish_time", "")
                
                cleaned_parts.append(f"{i}. {title}")
                if snippet:
                    cleaned_parts.append(f"   {snippet}")
                if site:
                    cleaned_parts.append(f"   Source: {site}")
                if publish_time:
                    cleaned_parts.append(f"   Time: {publish_time}")
                cleaned_parts.append("")
        
        cleaned_text = "\n".join(cleaned_parts)
        
        # Handle empty data
        if not cleaned_text.strip():
            cleaned_text = f"No search results found for this token. This token might be too new or obscure."
        
        logger.info(f"Cleaned data length: {len(cleaned_text)}")
        
        return CleanDataNodeOutput(cleaned_text=cleaned_text)
        
    except Exception as e:
        logger.error(f"Data cleaning failed: {str(e)}", exc_info=True)
        return CleanDataNodeOutput(cleaned_text=f"Data cleaning failed: {str(e)}")
```

### Step 5: Implement Analysis Node

Create `src/graphs/nodes/analysis_node.py`:

```python
import os
import json
import logging
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from jinja2 import Template
from graphs.state import AnalysisNodeInput, AnalysisNodeOutput

logger = logging.getLogger(__name__)


def analysis_node(
    state: AnalysisNodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnalysisNodeOutput:
    """
    title: Deep Analysis
    desc: Use multimodal LLM to analyze sentiment data and prediction image
    integrations: llm
    """
    ctx = runtime.context
    
    try:
        # Read config file
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
        with open(cfg_file, 'r', encoding='utf-8') as fd:
            _cfg = json.load(fd)
        
        llm_config = _cfg.get("config", {})
        sp = _cfg.get("sp", "")
        up = _cfg.get("up", "")
        
        # Render user prompt
        up_tpl = Template(up)
        user_prompt_content = up_tpl.render({
            "token": state.token_name,
            "sentiment_data": state.cleaned_text
        })
        
        logger.info(f"Analysis for token: {state.token_name}")
        
        # Initialize LLM client
        client = LLMClient(ctx=ctx)
        
        # Build multimodal message (text + image)
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=[
                {
                    "type": "text",
                    "text": user_prompt_content
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": state.generated_image_url
                    }
                }
            ])
        ]
        
        # Invoke model
        response = client.invoke(
            messages=messages,
            model=llm_config.get("model", "doubao-seed-1-6-vision-250815"),
            temperature=llm_config.get("temperature", 0.7),
            max_completion_tokens=llm_config.get("max_completion_tokens", 4096)
        )
        
        # Extract response content safely
        if isinstance(response.content, str):
            analysis_report = response.content
        elif isinstance(response.content, list):
            # Handle multimodal response
            text_parts = []
            for item in response.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            analysis_report = "\n".join(text_parts)
        else:
            analysis_report = str(response.content)
        
        logger.info(f"Analysis report generated, length: {len(analysis_report)}")
        
        return AnalysisNodeOutput(analysis_report=analysis_report)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise
```

### Step 6: Create LLM Configuration

Create `config/analysis_llm_cfg.json`:

```json
{
  "config": {
    "model": "doubao-seed-1-6-vision-250815",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_completion_tokens": 4096
  },
  "tools": [],
  "sp": "You are a crypto investment expert specializing in Meme token analysis with deep knowledge of crypto culture and community dynamics.\n\nYour analysis style:\n- Professional yet accessible\n- Data-driven insights\n- Humorous Degen tone\n- Risk-aware recommendations\n\nAnalysis Framework:\n1. 🎯 Narrative Magic Analysis\n   - Name memorability\n   - Concept clarity\n   - Cultural resonance\n\n2. 📢 Community Hype Ability\n   - Social media activity\n   - Community engagement\n   - Shilling intensity\n\n3. 🎨 Visual Gene Detection\n   - Meme potential\n   - Visual appeal\n   - Viral characteristics\n\n4. 🏆 Wealth Gene Rating\n   - 🌟 Diamond Hand: 10000x potential\n   - 🌙 Moonshot: 100x expected\n   - 🗑️ Paper Hand: Likely a rug\n   - 💩 Shitcoin: Stay away\n\nOutput Requirements:\n- Clear structure with emojis\n- Actionable insights\n- Risk warnings\n- Humorous but professional tone",
  "up": "Analyze {{token}} token:\n\n【Sentiment Data】\n{{sentiment_data}}\n\n【Generated Image】\nPlease analyze the prediction image above.\n\nProvide a comprehensive wealth gene detection report covering:\n1. Narrative Magic Analysis\n2. Community Hype Ability\n3. Visual Gene Detection\n4. Wealth Gene Rating\n\nFormat your report professionally with emojis."
}
```

### Step 7: Build Main Workflow

Create `src/graphs/graph.py`:

```python
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

# Start search and image generation in parallel
builder.add_edge(START, "search")
builder.add_edge(START, "image_gen")

# Clean data after search completes
builder.add_edge("search", "clean_data")

# Converge to analysis after both branches complete
builder.add_edge(["clean_data", "image_gen"], "analysis")

# End after analysis
builder.add_edge("analysis", END)

# ========== Compile Graph ==========
main_graph = builder.compile()
```

### Step 8: Create Entry Point

Create `src/main.py`:

```python
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from graphs.graph import main_graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Meme Token Analyzer")


class AnalyzeRequest(BaseModel):
    token_name: str


class AnalyzeResponse(BaseModel):
    analysis_report: str
    generated_image_url: str


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_token(request: AnalyzeRequest):
    """
    Analyze a Meme token and generate wealth gene detection report.
    """
    try:
        logger.info(f"Analyzing token: {request.token_name}")
        
        # Execute workflow
        result = main_graph.invoke({
            "token_name": request.token_name
        })
        
        return AnalyzeResponse(
            analysis_report=result["analysis_report"],
            generated_image_url=result["generated_image_url"]
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

## Usage Examples

### Command Line

```python
# Run directly
python src/main.py

# Or use the analyze function
from graphs.graph import main_graph

result = main_graph.invoke({"token_name": "PEPE"})
print(result["analysis_report"])
print(f"Image: {result['generated_image_url']}")
```

### API Call

```bash
# Analyze a token
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"token_name": "PEPE"}'

# Response:
{
  "analysis_report": "🎯 Narrative Magic Analysis\n...",
  "generated_image_url": "https://..."
}
```

### Batch Analysis

```python
from graphs.graph import main_graph

tokens = ["PEPE", "SHIB", "DOGE", "BONK"]

for token in tokens:
    try:
        result = main_graph.invoke({"token_name": token})
        print(f"\n{'='*60}")
        print(f"Token: {token}")
        print(f"{'='*60}")
        print(result["analysis_report"])
        print(f"\nImage: {result['generated_image_url']}")
    except Exception as e:
        print(f"Failed to analyze {token}: {e}")
```

### Integration Example

```python
def analyze_before_trade(token_name: str) -> tuple[str, str]:
    """
    Analyze token before trading.
    Returns: (action, image_url)
    """
    result = main_graph.invoke({"token_name": token_name})
    report = result["analysis_report"]
    
    if "🌟 Diamond Hand" in report:
        return "BUY", result["generated_image_url"]
    elif "💩 Shitcoin" in report:
        return "AVOID", None
    else:
        return "RESEARCH", result["generated_image_url"]


# Usage
action, image_url = analyze_before_trade("PEPE")
print(f"Action: {action}")
if image_url:
    print(f"View image: {image_url}")
```

## Advanced Features

### Streaming Response

```python
async def stream_analysis(token_name: str):
    """Stream analysis results"""
    async for event in main_graph.astream({"token_name": token_name}):
        for node_name, node_output in event.items():
            yield f"[{node_name}] {node_output}\n\n"
```

### Custom Analysis Prompt

Modify `config/analysis_llm_cfg.json` to customize analysis:

```json
{
  "sp": "You are a conservative crypto analyst...",
  "up": "Provide a risk-focused analysis of {{token}}..."
}
```

### Error Handling

```python
from graphs.graph import main_graph
import logging

def safe_analyze(token_name: str) -> dict:
    """Analyze with comprehensive error handling"""
    try:
        result = main_graph.invoke({"token_name": token_name})
        return {
            "success": True,
            "report": result["analysis_report"],
            "image_url": result["generated_image_url"]
        }
    except Exception as e:
        logging.error(f"Analysis failed for {token_name}: {e}")
        return {
            "success": False,
            "error": str(e),
            "report": None,
            "image_url": None
        }
```

## Performance Optimization

### Parallel Execution

The workflow automatically runs search and image generation in parallel:

```python
# These run simultaneously:
builder.add_edge(START, "search")      # Branch 1
builder.add_edge(START, "image_gen")   # Branch 2

# Convergence point:
builder.add_edge(["clean_data", "image_gen"], "analysis")
```

### Caching

Enable LLM response caching for repeated queries:

```python
# In analysis_node.py
response = client.invoke(
    messages=messages,
    caching="enabled",  # Enable caching
    ...
)
```

### Rate Limiting

Add rate limiting for API calls:

```python
import time
from functools import wraps

def rate_limit(delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(delay=2.0)
def search_node(state, config, runtime):
    # Search implementation
    ...
```

## Testing

### Unit Tests

```python
import pytest
from graphs.nodes.search_node import search_node
from graphs.state import SearchNodeInput
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

def test_search_node():
    state = SearchNodeInput(token_name="PEPE")
    config = RunnableConfig()
    runtime = Runtime(context=Context())
    
    result = search_node(state, config, runtime)
    
    assert isinstance(result, SearchNodeOutput)
    assert isinstance(result.search_results, list)
    assert isinstance(result.search_summary, str)
```

### Integration Tests

```python
def test_full_workflow():
    result = main_graph.invoke({"token_name": "PEPE"})
    
    assert "analysis_report" in result
    assert "generated_image_url" in result
    assert len(result["analysis_report"]) > 100
    assert result["generated_image_url"].startswith("http")
```

## Troubleshooting

### Common Issues

**Issue**: Search returns empty results
```python
# Solution: Check query format and API status
query = f"{state.token_name} token news sentiment"
response = client.search(query=query, count=10)
print(f"Found {len(response.web_items)} results")
```

**Issue**: Image generation fails
```python
# Solution: Verify prompt and API status
prompt = f"cartoon {state.token_name} character"
response = client.generate(prompt=prompt, size="2K")
if not response.success:
    print(f"Error: {response.error_messages}")
```

**Issue**: LLM response is empty
```python
# Solution: Check content type and handle safely
if isinstance(response.content, str):
    text = response.content
elif isinstance(response.content, list):
    text = " ".join(item.get("text", "") for item in response.content if isinstance(item, dict))
```

## Best Practices

1. **Input Validation**: Always validate token names before processing
2. **Error Handling**: Implement comprehensive error handling for all nodes
3. **Logging**: Use detailed logging for debugging and monitoring
4. **Rate Limiting**: Respect API rate limits for production usage
5. **Caching**: Enable caching for repeated queries to reduce costs
6. **Testing**: Write comprehensive tests for all nodes
7. **Documentation**: Document all custom configurations and modifications

## Key Points

- **Workflow Structure**: 4 nodes with parallel execution
- **Multimodal Analysis**: Combines text and image analysis
- **State Management**: Use Pydantic models for type safety
- **Error Handling**: Graceful degradation on failures
- **Performance**: Parallel execution for speed
- **Scalability**: Stateless design for horizontal scaling

## Security Considerations

- Never expose API keys in client-side code
- Validate and sanitize all user inputs
- Use HTTPS for all API communications
- Implement rate limiting to prevent abuse
- Monitor API usage and costs
