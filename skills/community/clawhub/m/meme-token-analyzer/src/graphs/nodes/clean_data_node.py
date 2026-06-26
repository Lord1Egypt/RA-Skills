import logging
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import CleanDataNodeInput, CleanDataNodeOutput

logger = logging.getLogger(__name__)


def extract_year_from_date(date_str: str) -> int:
    """Extract year from date string"""
    if not date_str:
        return 0
    
    # Try to extract year from various date formats
    year_match = re.search(r'\b(20\d{2})\b', date_str)
    if year_match:
        return int(year_match.group(1))
    return 0


def clean_data_node(
    state: CleanDataNodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CleanDataNodeOutput:
    """
    title: Sentiment Cleaning
    desc: Clean Google search results into a concise summary for LLM analysis with date freshness check
    """
    ctx = runtime.context
    
    try:
        # Extract search result titles and snippets (top 5 most relevant)
        snippets: List[str] = []
        years_found: List[int] = []
        
        if state.search_results:
            for item in state.search_results[:5]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                publish_time = item.get("publish_time", "")
                
                if title or snippet:
                    snippets.append(f"【{title}】\n{snippet}")
                
                # Extract year for freshness check
                year = extract_year_from_date(publish_time)
                if year > 0:
                    years_found.append(year)
        
        # Handle no results case
        if not snippets:
            logger.warning("No search results found")
            return CleanDataNodeOutput(
                cleaned_text=f"Unable to find latest trending narratives for this token online."
            )
        
        # Check data freshness
        current_year = datetime.now().year
        stale_data_warning = ""
        
        if years_found:
            max_year = max(years_found)
            if max_year < current_year - 1:  # Data is older than 1 year
                stale_data_warning = f"\n\n⚠️ **Data Freshness Alert**: Latest search results are from {max_year}. Data may be outdated for accurate trend analysis."
                logger.warning(f"Stale data detected: latest result from {max_year}")
            else:
                stale_data_warning = f"\n\n✅ **Data Freshness**: Search results are current (latest from {max_year})."
        else:
            # No publish_time found in results — use unified freshness alert wording
            stale_data_warning = "\n\n⚠️ **Data Freshness Alert**: Publication dates not available in search results. Data freshness cannot be verified for accurate trend analysis."
        
        # Add AI summary if available
        if state.search_summary:
            cleaned_text = f"=== AI Summary ===\n{state.search_summary}\n\n=== Detailed Information ===\n\n" + "\n---\n".join(snippets)
        else:
            cleaned_text = "\n---\n".join(snippets)
        
        # Append freshness warning if applicable
        cleaned_text += stale_data_warning
        
        logger.info(f"Cleaned {len(snippets)} search results, total length: {len(cleaned_text)} chars")
        
        return CleanDataNodeOutput(cleaned_text=cleaned_text)
        
    except Exception as e:
        logger.error(f"Data cleaning failed: {str(e)}", exc_info=True)
        return CleanDataNodeOutput(cleaned_text=f"Data cleaning failed: {str(e)}")
