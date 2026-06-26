#!/usr/bin/env python3
"""Multimodal content creation workflow orchestrator."""

import os
import sys
from wacli import WhatsAppClient
from transcribe import transcribe_audio
from generate_images import generate_image


def process_whatsapp_request(message: dict) -> bool:
    """Process an incoming WhatsApp request."""
    print(f"Processing message from {message['from']}...")
    
    # Step 1: Get prompt from message
    prompt = None
    if message["type"] == "text":
        prompt = message["content"]
    elif message["type"] == "audio":
        # Transcribe audio to get prompt
        print(f"Transcribing audio file: {message['content']}")
        prompt = transcribe_audio(message["content"])
        if message.get("caption"):
            prompt += " " + message["caption"]
    else:
        print(f"Unsupported message type: {message['type']}")
        return False
    
    if not prompt:
        print("No prompt extracted from message")
        return False
    
    print(f"Extracted prompt: {prompt}")
    
    # Step 2: Generate image from prompt
    print("Generating image...")
    result = generate_image(prompt)
    if not result:
        print("Failed to generate image")
        return False
    
    # Step 3: Send image back to customer
    print("Sending result back to customer...")
    wa_client = WhatsAppClient()
    caption = f"Here's your generated image!\nPrompt used: {result['revised_prompt']}"
    wa_client.send_message(message["from"], caption, result["image_path"])
    
    print("Request processed successfully!")
    return True

def process_all_unread() -> None:
    """Process all unread WhatsApp messages"""
    wa_client = WhatsAppClient()
    messages = wa_client.list_messages()
    
    for msg in messages:
        # In production, track read/unread status
        process_whatsapp_request(msg)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "process-all":
        process_all_unread()
    else:
        print("Content Creator Workflow")
        print("Usage:")
        print("  python workflow.py process-all - Process all unread requests")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Logged into wacli with `python wacli.py login <your-token>`")