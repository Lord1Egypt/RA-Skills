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


def _build_fallback_report(token_name: str, cleaned_text: str, error_msg: str) -> str:
    """Build a fallback report when LLM analysis fails"""
    return (
        f"🧬 Meme Token Wealth Gene Detection Report - {token_name}\n"
        f"{'=' * 50}\n\n"
        f"⚠️ AI analysis service is temporarily unavailable. Below is a summary based on search data.\n\n"
        f"📊 Search Data Summary:\n{cleaned_text[:500]}\n\n"
        f"⚠️ Technical Note: Full analysis failed due to: {error_msg}\n"
        f"Please try again later for the complete wealth gene detection report."
    )


def analysis_node(
    state: AnalysisNodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnalysisNodeOutput:
    """
    title: Deep Analysis
    desc: Use multimodal LLM to analyze sentiment data and prediction image, generate comprehensive report
    integrations: llm
    """
    ctx = runtime.context
    
    try:
        # Read config file
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH", ""), config['metadata']['llm_cfg'])
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
        
        logger.info(f"Analysis for token: {state.token_name}, has_image: {bool(state.generated_image_url)}")
        
        # Initialize LLM client
        client = LLMClient(ctx=ctx)
        
        # Build message content — guard against empty image URL
        # If image generation failed/degraded, skip the image block to avoid LLM API 400/422
        if state.generated_image_url:
            # Multimodal path: text + image
            human_content = [
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
            ]
        else:
            # Text-only fallback path: skip image block entirely
            logger.warning("No image URL available, falling back to text-only analysis")
            human_content = [
                {
                    "type": "text",
                    "text": user_prompt_content + "\n\n[Note: Image generation was unavailable. Please perform text-only analysis based on the sentiment data above.]"
                }
            ]
        
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=human_content)
        ]
        
        # Invoke model
        response = client.invoke(
            messages=messages,
            model=llm_config.get("model", "doubao-seed-1-6-vision-250815"),
            temperature=llm_config.get("temperature", 0.7),
            max_completion_tokens=llm_config.get("max_completion_tokens", 4096)
        )
        
        # Extract response content
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
        
        # Prepend image-unavailable notice if image generation failed
        if not state.generated_image_url:
            analysis_report = "⚠️ Note: Prediction image generation was unavailable. Below is a text-only analysis.\n\n" + analysis_report
        
        logger.info(f"Analysis report generated, length: {len(analysis_report)}")
        
        return AnalysisNodeOutput(analysis_report=analysis_report)
        
    except Exception as e:
        # Degrade gracefully: return fallback report instead of raising
        # This prevents users from seeing a blank page or 500 error
        error_msg = str(e)
        logger.error(f"Analysis failed, returning fallback report: {error_msg}", exc_info=True)
        fallback_report = _build_fallback_report(state.token_name, state.cleaned_text, error_msg)
        return AnalysisNodeOutput(analysis_report=fallback_report)
