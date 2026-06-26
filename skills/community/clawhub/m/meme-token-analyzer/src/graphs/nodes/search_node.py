import json
import logging
import re
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
        # Input validation
        if not state.token_name or not isinstance(state.token_name, str):
            raise ValueError("Invalid token_name: must be a non-empty string")
        
        # Sanitize token name for search query (remove special characters)
        safe_token_name = re.sub(r'[^\w\s-]', '', state.token_name.strip())
        if not safe_token_name:
            raise ValueError("Token name contains only invalid characters")
        
        # Initialize search client
        client = SearchClient(ctx=ctx)
        
        # Build search query with recent time filter
        query = f"{safe_token_name} token news twitter sentiment"
        
        logger.info(f"Searching for: {query} (time_range: 1 month)")
        
        # Execute search with AI summary and time range filter
        response = client.search(
            query=query,
            search_type="web",
            count=10,
            need_summary=True,
            time_range="1m"  # Filter results from last 1 month for fresh data
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
                    "publish_time": item.publish_time,
                    "auth_info_des": item.auth_info_des
                })
        
        # Extract summary
        summary = response.summary if response.summary else ""
        
        logger.info(f"Found {len(search_results)} results, summary length: {len(summary)}")
        
        return SearchNodeOutput(
            search_results=search_results,
            search_summary=summary
        )
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}", exc_info=True)
        # Return empty results on failure
        return SearchNodeOutput(
            search_results=[],
            search_summary=f"Search failed: {str(e)}"
        )
