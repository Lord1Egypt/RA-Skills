import os
import io
import asyncio
import hashlib
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
import httpx

# AI and Cloud providers
from anthropic import AsyncAnthropic
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import redis.asyncio as redis

app = FastAPI(title="Jewellery Content Engine (OpenCLAW Skill)")

# -------------------------------------------------------------------
# Configuration & Initialization
# -------------------------------------------------------------------
# Environment variables expected:
# ANTHROPIC_API_KEY
# GOOGLE_APPLICATION_CREDENTIALS (path to service account json)
# REDIS_URL (e.g. redis://localhost:6379)
# GCP_PROJECT_ID
# GCP_LOCATION (e.g., us-central1)

aclient = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

try:
    vertexai.init(
        project=os.getenv("GCP_PROJECT_ID"), 
        location=os.getenv("GCP_LOCATION", "us-central1")
    )
except Exception as e:
    print(f"Vertex AI Init Warning: {e}")

try:
    redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)
except Exception as e:
    print(f"Redis Init Warning: {e}")

try:
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "gcp-service-account.json"), 
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    drive_service = build('drive', 'v3', credentials=creds)
except Exception as e:
    print(f"Drive Init Warning: {e}")

# -------------------------------------------------------------------
# Data Models
# -------------------------------------------------------------------
class WebhookPayload(BaseModel):
    image_url: str
    product_name: str
    metadata: Optional[Dict[str, Any]] = {}

# -------------------------------------------------------------------
# Core Functions
# -------------------------------------------------------------------
async def download_image(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content

def get_image_hash(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def generate_prompts(image_url: str, metadata: dict) -> dict:
    prompt = f"Analyze this jewellery piece context: {metadata}. Provide ONLY a JSON with two keys: 'model_prompt' (describing an AI model wearing it naturally) and 'product_prompt' (studio lighting for the product alone)."
    
    response = await aclient.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system="You are an expert jewellery art director.",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "url", "url": image_url}},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    # Simplified JSON extraction
    import json
    return json.loads(response.content[0].text)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def generate_content(product_name: str, metadata: dict) -> str:
    prompt = f"Write a catchy Instagram caption and a short SEO product description for {product_name}. Details: {metadata}"
    response = await aclient.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=600,
        system="You are a luxury jewellery copywriter.",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=4, max=15))
async def generate_imagen_asset(prompt: str) -> bytes:
    loop = asyncio.get_event_loop()
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
    def _gen():
        return model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            person_generation="ALLOW_ADULT"
        )
    response = await loop.run_in_executor(None, _gen)
    return response.images[0]._image_bytes

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def upload_to_drive(file_bytes_or_text, file_name: str, folder_id: str, mime_type: str):
    if isinstance(file_bytes_or_text, str):
        file_bytes_or_text = file_bytes_or_text.encode('utf-8')
        
    file_stream = io.BytesIO(file_bytes_or_text)
    media = MediaIoBaseUpload(file_stream, mimetype=mime_type, resumable=True)
    
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    return file.get('webViewLink')

def create_drive_folder(folder_name: str, parent_id: str = None) -> str:
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
        
    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')

# -------------------------------------------------------------------
# Pipeline Execution Definition
# -------------------------------------------------------------------
async def run_pipeline(payload: WebhookPayload, folder_id_root: str):
    try:
        # Step 1: Input & Hash Check
        image_bytes = await download_image(payload.image_url)
        img_hash = get_image_hash(image_bytes)
        
        cahed_result = await redis_client.get(f"jewellery_pipeline:{img_hash}")
        if cahed_result:
            return {"status": "success", "cached": True, "links": cahed_result}

        # Step 2: Prompt Generation
        prompts = await generate_prompts(payload.image_url, payload.metadata)

        # Step 3: Parallel Generation
        model_img_task = asyncio.create_task(generate_imagen_asset(prompts['model_prompt']))
        prod_img_task = asyncio.create_task(generate_imagen_asset(prompts['product_prompt']))
        content_task = asyncio.create_task(generate_content(payload.product_name, payload.metadata))

        model_img_bytes, prod_img_bytes, text_content = await asyncio.gather(
            model_img_task, prod_img_task, content_task
        )

        # Step 4: Storage
        loop = asyncio.get_event_loop()
        folder_id = await loop.run_in_executor(None, create_drive_folder, payload.product_name, folder_id_root)
        
        links = {}
        links['model'] = await loop.run_in_executor(None, upload_to_drive, model_img_bytes, "model_image.jpg", folder_id, "image/jpeg")
        links['product'] = await loop.run_in_executor(None, upload_to_drive, prod_img_bytes, "product_image.jpg", folder_id, "image/jpeg")
        links['content'] = await loop.run_in_executor(None, upload_to_drive, text_content, "content.txt", folder_id, "text/plain")

        # Step 5: Save to Cache
        import json
        await redis_client.setex(f"jewellery_pipeline:{img_hash}", 2592000, json.dumps(links))

        return {"status": "success", "links": links}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------------------------------------------------------
# OpenCLAW Webhook Trigger
# -------------------------------------------------------------------
@app.post("/api/v1/jewellery/process")
async def process_jewellery_content(payload: WebhookPayload):
    # This acts as the synchronous webhook return, processing in background if needed
    # Wait for completion to return real results for integration ease.
    import os
    parent_folder = os.getenv("DRIVE_FOLDER_ID", "root") 
    result = await run_pipeline(payload, parent_folder)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
