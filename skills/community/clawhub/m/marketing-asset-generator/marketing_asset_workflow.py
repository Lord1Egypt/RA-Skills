"""
Marketing Asset Generation Workflow
Combines DuckDuckGo search, Nano Banana Pro image generation, Feishu Drive storage, and Slack notifications.
"""
import os
import time
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from google import genai
from google.genai import types
import requests
from requests_toolbelt import MultipartEncoder
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables
load_dotenv()

class MarketingAssetGenerator:
    def __init__(self):
        # Initialize clients
        self.ddg_client = DDGS()
        self.gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        
        # Configuration
        self.feishu_app_id = os.environ.get("FEISHU_APP_ID")
        self.feishu_app_secret = os.environ.get("FEISHU_APP_SECRET")
        self.feishu_target_folder = os.environ.get("FEISHU_TARGET_FOLDER_TOKEN")
        self.slack_target_channel = os.environ.get("SLACK_TARGET_CHANNEL_ID")
        self.team_mentions = os.environ.get("MARKETING_TEAM_SLACK_MENTIONS", "")

    def search_design_inspiration(self, query, max_results=5):
        """Search DuckDuckGo for design inspiration and reference images"""
        print(f"🔍 Searching for design inspiration: {query}")
        try:
            # Search for images
            image_results = self.ddg_client.images(
                query,
                region="us-en",
                size="Large",
                type_image="photo",
                max_results=max_results
            )
            
            # Search for web references
            web_results = self.ddg_client.text(
                query + " marketing design best practices",
                max_results=3
            )
            
            return {
                "reference_images": [img["image"] for img in image_results],
                "design_tips": [result["body"] for result in web_results]
            }
        except Exception as e:
            print(f"⚠️  Search failed: {str(e)}")
            return {"reference_images": [], "design_tips": []}

    def generate_marketing_image(self, prompt, aspect_ratio="16:9", image_size="2K"):
        """Generate marketing image using Nano Banana Pro (Gemini 3 Pro Image)"""
        print(f"🎨 Generating image with prompt: {prompt}")
        try:
            response = self.gemini_client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["image", "text"],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=image_size
                    ),
                    thinking_config=types.ThinkingConfig(
                        thinking_level="high",
                        include_thoughts=True
                    )
                )
            )
            
            # Save generated images
            saved_files = []
            for i, generated_image in enumerate(response.generated_images):
                timestamp = int(time.time())
                filename = f"generated_asset_{timestamp}_{i}.png"
                with open(filename, "wb") as f:
                    f.write(generated_image.image.data)
                saved_files.append(filename)
                print(f"✅ Saved generated image: {filename}")
            
            return saved_files
        except Exception as e:
            print(f"❌ Image generation failed: {str(e)}")
            return []

    def _get_feishu_token(self):
        """Get Feishu tenant access token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.feishu_app_id,
            "app_secret": self.feishu_app_secret
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["tenant_access_token"]

    def upload_to_feishu_drive(self, file_path):
        """Upload file to Feishu Drive"""
        print(f"☁️  Uploading to Feishu Drive: {file_path}")
        try:
            tenant_token = self._get_feishu_token()
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            # Simple upload for files <20MB
            upload_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
            form = {
                "file_name": file_name,
                "parent_type": "explorer",
                "parent_node": self.feishu_target_folder,
                "size": str(file_size),
                "file": (file_name, open(file_path, "rb"))
            }
            multi_form = MultipartEncoder(form)
            headers = {
                "Authorization": f"Bearer {tenant_token}",
                "Content-Type": multi_form.content_type
            }
            
            response = requests.post(upload_url, headers=headers, data=multi_form)
            response.raise_for_status()
            result = response.json()["data"]
            
            file_url = f"https://feishu.cn/file/{result['file_token']}"
            print(f"✅ File uploaded to Feishu: {file_url}")
            return {
                "file_token": result["file_token"],
                "url": file_url,
                "name": file_name
            }
        except Exception as e:
            print(f"❌ Feishu upload failed: {str(e)}")
            return None

    def send_slack_notification(self, generated_files, feishu_links, inspiration_results):
        """Send notification to Slack channel with asset details"""
        print(f"💬 Sending Slack notification to channel: {self.slack_target_channel}")
        try:
            # Build message blocks
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚀 New Marketing Assets Generated!"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hey {self.team_mentions},\nNew marketing assets have been generated and uploaded to Feishu Drive."
                    }
                },
                {
                    "type": "divider"
                }
            ]

            # Add generated files section
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*📁 Generated Assets:*"
                }
            })
            
            for name, url in zip(generated_files, feishu_links):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"- <{url}|{name}>"
                    }
                })

            # Add design tips if available
            if inspiration_results.get("design_tips"):
                blocks.append({
                    "type": "divider"
                })
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*💡 Design Tips from Research:*"
                    }
                })
                for tip in inspiration_results["design_tips"][:2]:
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"- {tip[:150]}..."
                        }
                    })

            # Send message
            response = self.slack_client.chat_postMessage(
                channel=self.slack_target_channel,
                text="New marketing assets are available!",
                blocks=blocks
            )
            
            # Upload first image as attachment
            if generated_files:
                self.slack_client.files_upload_v2(
                    channel=self.slack_target_channel,
                    file=generated_files[0],
                    title="Preview of Generated Asset",
                    initial_comment="Here's a preview of the first generated asset:"
                )
            
            print("✅ Slack notification sent successfully")
            return response.data
        except SlackApiError as e:
            print(f"❌ Slack notification failed: {e.response['error']}")
            return None

    def run_full_workflow(self, design_prompt, image_prompt):
        """Run the complete marketing asset generation workflow"""
        print("🚀 Starting marketing asset generation workflow...")
        
        # Step 1: Search for inspiration
        inspiration = self.search_design_inspiration(design_prompt)
        
        # Step 2: Generate images
        generated_files = self.generate_marketing_image(image_prompt)
        if not generated_files:
            print("❌ No images generated, workflow aborted")
            return None
        
        # Step 3: Upload to Feishu Drive
        feishu_links = []
        for file in generated_files:
            result = self.upload_to_feishu_drive(file)
            if result:
                feishu_links.append(result["url"])
        
        # Step 4: Send Slack notification
        if feishu_links:
            self.send_slack_notification(generated_files, feishu_links, inspiration)
        
        print("🎉 Workflow completed successfully!")
        return {
            "generated_files": generated_files,
            "feishu_links": feishu_links,
            "inspiration": inspiration
        }

if __name__ == "__main__":
    # Example usage
    generator = MarketingAssetGenerator()
    result = generator.run_full_workflow(
        design_prompt="summer sale 2024 marketing campaign design",
        image_prompt="Vibrant summer sale marketing banner with tropical elements, 50% off text, bright colors, modern design, 16:9 aspect ratio"
    )
    print("Workflow result:", result)