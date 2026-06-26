#!/usr/bin/env python3
"""
PDF Vision Extraction Skill - Enhanced with Multiple Model Support
Extracts text from image-based/scanned PDFs using multiple vision APIs with fallback
"""

import os
import sys
import json
import base64
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional

class PDFVisionExtractor:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.base_urls = {}
        self.api_keys = {}
        self._load_config()
    
    def _load_config(self):
        """Load API configuration from OpenClaw config"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            models = config.get('models', {})
            providers = models.get('providers', {})
            
            # Load OpenAI/Xflow provider
            if 'openai' in providers:
                openai_config = providers['openai']
                self.base_urls['openai'] = openai_config.get('baseUrl')
                self.api_keys['openai'] = openai_config.get('apiKey')
            
            # Load ZhipuAI/GLM provider  
            if 'zhipuai' in providers:
                zhipuai_config = providers['zhipuai']
                self.base_urls['zhipuai'] = zhipuai_config.get('baseUrl')
                self.api_keys['zhipuai'] = zhipuai_config.get('apiKey')
                
        except Exception as e:
            raise FileNotFoundError(f"Could not load config from {self.config_path}: {e}")
    
    def convert_pdf_to_image(self, pdf_path: str, page_number: int = 0, temp_dir: str = "/tmp") -> str:
        """Convert PDF page to PNG image using pypdfium2"""
        import pypdfium2 as pdfium
        
        pdf = pdfium.PdfDocument(str(pdf_path))
        page_count = len(pdf)
        
        # Handle page numbering (0-indexed internally)
        if page_number == 0:
            target_page = 0
        else:
            target_page = page_number - 1
        
        if target_page >= page_count or target_page < 0:
            raise ValueError(f"Invalid page number. PDF has {page_count} pages.")
        
        page = pdf[target_page]
        pil_image = page.render(scale=2, rotation=0).to_pil()
        
        image_path = Path(temp_dir) / "pdf_vision_page.png"
        pil_image.save(image_path)
        
        return str(image_path)
    
    def call_api(self, provider: str, model: str, image_path: str, prompt: str, temp_dir: str = "/tmp") -> str:
        """Call specified API with image and prompt"""
        if provider not in self.base_urls or provider not in self.api_keys:
            raise ValueError(f"Provider {provider} not configured")
        
        base_url = self.base_urls[provider]
        api_key = self.api_keys[provider]
        
        if not base_url or not api_key:
            raise ValueError(f"Missing configuration for provider {provider}")
        
        # Encode image
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Create payload based on provider
        if provider == "openai":
            # Xflow/OpenAI format
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                        ]
                    }
                ],
                "max_tokens": 2000
            }
            api_endpoint = f"{base_url}/chat/completions"
            
        elif provider == "zhipuai":
            # ZhipuAI/GLM format (same as OpenAI)
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                        ]
                    }
                ],
                "max_tokens": 2000
            }
            api_endpoint = f"{base_url}/chat/completions"
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        payload_path = Path(temp_dir) / f"pdf_vision_payload_{provider}_{model.replace('/', '_')}.json"
        response_path = Path(temp_dir) / f"pdf_vision_response_{provider}_{model.replace('/', '_')}.json"
        
        with open(payload_path, 'w') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        
        # Call API using curl
        curl_cmd = [
            "curl", "-X", "POST", api_endpoint,
            "-H", f"Authorization: Bearer {api_key}",
            "-H", "Content-Type: application/json",
            "-d", f"@{payload_path}",
            "-o", str(response_path),
            "--fail",
            "--silent",
            "--show-error"
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else result.stdout
            raise RuntimeError(f"API call failed for {provider}/{model}: {error_msg}")
        
        # Parse response
        with open(response_path, 'r') as f:
            response = json.load(f)
        
        if 'choices' not in response or len(response['choices']) == 0:
            raise RuntimeError(f"Invalid API response from {provider}/{model}")
        
        extracted_text = response['choices'][0]['message']['content']
        return extracted_text
    
    def extract_with_fallback(self, image_path: str, prompt: str, temp_dir: str = "/tmp") -> tuple[str, str]:
        """Try multiple models with fallback"""
        # Define model priority order
        model_configs = [
            ("openai", "qwen3-vl-plus"),
            ("zhipuai", "glm-4.6v-flash"),
            ("zhipuai", "glm-5")  # glm-5 may not have vision, but worth trying
        ]
        
        for provider, model in model_configs:
            try:
                print(f"Trying {provider}/{model}...")
                result = self.call_api(provider, model, image_path, prompt, temp_dir)
                print(f"✅ Success with {provider}/{model}")
                return result, f"{provider}/{model}"
            except Exception as e:
                print(f"❌ Failed with {provider}/{model}: {e}")
                continue
        
        raise RuntimeError("All vision models failed")
    
    def extract_with_specific_model(self, image_path: str, prompt: str, model_spec: str, temp_dir: str = "/tmp") -> str:
        """Extract using a specific model"""
        if '/' in model_spec:
            provider, model = model_spec.split('/', 1)
        else:
            # Default to zhipuai for GLM models
            if model_spec.startswith('glm') or model_spec.startswith('cogview'):
                provider = 'zhipuai'
            else:
                provider = 'openai'
            model = model_spec
        
        return self.call_api(provider, model, image_path, prompt, temp_dir)

def main():
    parser = argparse.ArgumentParser(description='Extract text from scanned PDFs using multiple vision APIs')
    parser.add_argument('--pdf-path', required=True, help='Path to the PDF file')
    parser.add_argument('--page', type=int, default=0, help='Page number (0 for first page, 1 for second, etc.)')
    parser.add_argument('--prompt', default='Extract all text content from this PDF document, preserving structure and formatting as much as possible.', 
                       help='Prompt for the vision model')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--config', default=os.path.expanduser('~/.openclaw/openclaw.json'), 
                       help='OpenClaw config file path')
    parser.add_argument('--temp-dir', default='/tmp', help='Temporary directory for intermediate files')
    parser.add_argument('--model', help='Specific model to use (e.g., "openai/qwen3-vl-plus", "zhipuai/glm-4.6v-flash", "glm-4.6v-flash")')
    parser.add_argument('--fallback', action='store_true', help='Use automatic fallback between models (default)')
    
    args = parser.parse_args()
    
    try:
        # Validate PDF exists
        if not os.path.exists(args.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {args.pdf_path}")
        
        print(f"PDF Vision Extraction Skill (Enhanced)")
        print(f"=====================================")
        print(f"PDF: {os.path.basename(args.pdf_path)}")
        print(f"Page: {args.page if args.page > 0 else 'first'}")
        print(f"Prompt: {args.prompt}")
        if args.model:
            print(f"Model: {args.model}")
        else:
            print(f"Mode: Automatic fallback")
        print()
        
        # Initialize extractor
        extractor = PDFVisionExtractor(args.config)
        
        # Convert PDF to image
        print("Converting PDF to image...")
        image_path = extractor.convert_pdf_to_image(args.pdf_path, args.page, args.temp_dir)
        print(f"Image created: {image_path}")
        
        # Extract text
        if args.model:
            print(f"Using specific model: {args.model}")
            extracted_text = extractor.extract_with_specific_model(image_path, args.prompt, args.model, args.temp_dir)
            used_model = args.model
        else:
            print("Using automatic fallback...")
            extracted_text, used_model = extractor.extract_with_fallback(image_path, args.prompt, args.temp_dir)
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                f.write(extracted_text)
            print(f"Results saved to: {args.output}")
        else:
            print("=== EXTRACTED CONTENT ===")
            print(extracted_text)
            print("=== END CONTENT ===")
        
        print(f"\n✅ PDF Vision Extraction completed successfully!")
        print(f"Used model: {used_model}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()