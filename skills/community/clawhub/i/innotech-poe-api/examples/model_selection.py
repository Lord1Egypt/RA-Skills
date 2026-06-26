"""
Example: Model Selection Logic

This example demonstrates how to choose the right model for different tasks.
Read MODEL_SELECTION_GUIDE.md for detailed guidance.
"""

from poe_client import PoeClient

client = PoeClient()

print("="*80)
print("Model Selection Examples")
print("="*80)

# Example 1: Programming task with different complexity
print("\n1. Programming Tasks")
print("-" * 80)

tasks = [
    ("Sort this list: [3, 1, 2]", "simple"),
    ("Write a REST API", "medium"),
    ("Design distributed system", "complex")
]

for task, complexity in tasks:
    result = client.query_for_task("programming", task, complexity=complexity)
    if result["success"]:
        selection = result["model_selection"]
        print(f"Task: {task}")
        print(f"  Selected: {selection['selected_model']}")
        print(f"  Reason: {selection['reason']}")
        print()

# Example 2: UI/UX Design (uses Gemini for 1M context)
print("\n2. UI/UX Design")
print("-" * 80)

result = client.query_for_task(
    "ui_design",
    "Create a complete design system with components, colors, and typography"
)
if result["success"]:
    selection = result["model_selection"]
    print(f"Task: Design system")
    print(f"  Selected: {selection['selected_model']}")
    print(f"  Reason: {selection['reason']}")

# Example 3: Data Analysis with huge dataset
print("\n3. Data Analysis")
print("-" * 80)

# Regular dataset
result = client.query_for_task("data_analysis", "Analyze sales trends")
if result["success"]:
    print(f"Regular data: {result['model_selection']['selected_model']}")

# Huge dataset (>200K tokens)
result = client.query_for_task("data_analysis", "Analyze huge dataset", complexity="huge_data")
if result["success"]:
    print(f"Huge data: {result['model_selection']['selected_model']}")

# Example 4: Web Search types
print("\n4. Web Search")
print("-" * 80)

search_types = ["simple", "complex", "deep"]
for search_type in search_types:
    result = client.query_for_task("web_search", "AI developments", complexity=search_type)
    if result["success"]:
        print(f"{search_type}: {result['model_selection']['selected_model']}")

# Example 5: Creative tasks
print("\n5. Creative Tasks")
print("-" * 80)

# Image
result = client.query_for_task("image_generation", "Modern UI", complexity="fast")
print(f"Image (fast): {result['model_selection']['selected_model']}")

# Video
result = client.query_for_task("video_generation", "City sunset", complexity="best")
print(f"Video (best): {result['model_selection']['selected_model']}")

# Audio
result = client.query_for_task("audio_generation", "Welcome message", complexity="speech")
print(f"Audio (speech): {result['model_selection']['selected_model']}")

print("\n" + "="*80)
print("Key Takeaways")
print("="*80)
print("""
1. Programming:
   - Simple → claude-haiku-4.5 (fast)
   - Medium → claude-sonnet-4.6 (balanced)
   - Complex → claude-opus-4.6 (deep reasoning)

2. UI/UX Design:
   - Default → gemini-3.1-pro (1M context for design systems)

3. Data Analysis:
   - Regular → claude-sonnet-4.6
   - Huge (>200K) → gemini-3.1-pro

4. Web Search:
   - Simple → perplexity-search
   - Complex → perplexity-sonar-pro
   - Deep → o3-deep-research

5. Creative:
   - Image → nano-banana-2 (fast) or imagen-4-ultra (best)
   - Video → veo-3.1 (best + audio)
   - Audio → elevenlabs-v3 (realistic speech)
""")
