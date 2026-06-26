import os
import json
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
        # Read image generation config
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH", ""), "config/image_gen_cfg.json")
        with open(cfg_file, 'r', encoding='utf-8') as fd:
            img_cfg = json.load(fd)
        
        # Build prompt from template
        prompt_template = img_cfg.get("prompt_template", 
            "A dynamic, high-quality photograph of a cartoon {token_name} character launching into space on a rocket, cinematic lighting, trending on ArtStation")
        prompt = prompt_template.format(token_name=state.token_name)
        
        # Get image size from config
        size = img_cfg.get("size", "2K")
        
        logger.info(f"Generating image with prompt: {prompt}")
        
        # Initialize image generation client
        client = ImageGenerationClient(ctx=ctx)
        
        # Generate image
        response = client.generate(
            prompt=prompt,
            size=size
        )
        
        # Extract image URL
        if response.success and response.image_urls:
            image_url = response.image_urls[0]
            logger.info(f"Image generated successfully: {image_url}")
            return ImageGenNodeOutput(generated_image_url=image_url)
        else:
            error_msg = "; ".join(response.error_messages) if response.error_messages else "Unknown error"
            logger.warning(f"Image generation returned no URL: {error_msg}")
            # Degrade gracefully: return empty URL instead of raising
            return ImageGenNodeOutput(generated_image_url="")
            
    except Exception as e:
        # Degrade gracefully: return empty URL instead of raising
        # This prevents the entire workflow from crashing when image generation fails
        logger.error(f"Image generation failed, degrading to text-only analysis: {str(e)}", exc_info=True)
        return ImageGenNodeOutput(generated_image_url="")
