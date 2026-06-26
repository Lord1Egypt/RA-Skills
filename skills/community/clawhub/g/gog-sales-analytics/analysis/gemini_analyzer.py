import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_sales_data(sales_file_path):
    with open(sales_file_path, "r") as f:
        sales_data = json.load(f)

    total_deals = len(sales_data)

    # Process the FULL set of discounted games, not just the first 20.
    # Compact each record to the fields needed for analysis so the entire
    # dataset fits comfortably in the model context.
    compact_data = []
    for game in sales_data:
        if not isinstance(game, dict):
            continue
        compact_data.append({
            k: game.get(k)
            for k in (
                "title", "price", "original_price", "discount",
                "discount_percent", "rating", "genre", "category", "url",
            )
            if k in game
        })

    payload = compact_data if compact_data else sales_data

    prompt = f"""
    Analyze this GOG weekly sales data. The dataset contains ALL {total_deals}
    discounted games for the week (the complete set, not a sample). Base every
    insight on the full dataset below:
    {json.dumps(payload, indent=2, ensure_ascii=False)}

    Provide:
    1. Top 5 best value deals (highest discount percentage with good ratings)
    2. Price trend comparison for popular AAA titles
    3. Category breakdown of discounted games
    4. Recommendations for budget gamers (<$10)
    
    Format output as markdown report.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    report_path = sales_file_path.replace(".json", "_analysis.md")
    with open(report_path, "w") as f:
        f.write(response.text)
    
    return report_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        report_path = analyze_sales_data(sys.argv[1])
        print(f"Analysis report generated: {report_path}")
