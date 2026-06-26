"""
Example: Basic usage of Poe API client

This example shows how to use the PoeClient for common tasks.
"""

from poe_client import PoeClient

# Initialize client
client = PoeClient()

print("="*80)
print("Example 1: Programming Tasks")
print("="*80)

# Simple programming task
result = client.programming(
    "Write a Python function to sort a list",
    complexity="simple"
)
print(f"Simple task: {result}\n")

# Medium programming task
result = client.programming(
    "Write a REST API with Flask that handles user authentication",
    complexity="medium"
)
print(f"Medium task: {result}\n")

# Complex programming task
result = client.programming(
    "Design a distributed microservices architecture for a large-scale e-commerce platform",
    complexity="complex"
)
print(f"Complex task: {result}\n")

print("="*80)
print("Example 2: UI/UX Design")
print("="*80)

result = client.ui_design(
    "Create a comprehensive design system for a fintech application with dark mode"
)
print(f"Design task: {result}\n")

print("="*80)
print("Example 3: Data Analysis")
print("="*80)

data = """
Sales data:
- January: $100,000
- February: $120,000
- March: $95,000
- April: $140,000
"""

result = client.data_analysis(
    f"Analyze this sales data and identify trends:\n{data}"
)
print(f"Analysis: {result}\n")

print("="*80)
print("Example 4: Web Search")
print("="*80)

result = client.web_search(
    "What are the latest developments in AI in 2026?",
    search_type="complex"
)
print(f"Search result: {result}\n")

print("="*80)
print("Example 5: Creative Tasks")
print("="*80)

# Image
result = client.generate_image(
    "A modern dashboard UI with dark theme and neon accents",
    quality="fast"
)
print(f"Image: {result}\n")

# Video
result = client.generate_video(
    "A cinematic drone shot of a city skyline at sunset",
    style="cinematic"
)
print(f"Video: {result}\n")

# Audio
result = client.generate_audio(
    "Welcome to our application. We're excited to have you here.",
    audio_type="speech"
)
print(f"Audio: {result}\n")

print("="*80)
print("Usage Statistics")
print("="*80)
print(client.get_usage_stats())
