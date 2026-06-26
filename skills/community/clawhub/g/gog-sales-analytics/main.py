import subprocess
import datetime
import os

def run_scraper():
    print("Running GOG sales scraper...")
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    output_file = f"./data/weekly_sales_{date_str}.json"
    os.makedirs("./data", exist_ok=True)
    
    result = subprocess.run([
        "web-scraper", "run", 
        "./scraper/gog_sales_scraper.yaml",
        "--output", output_file
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Scraper failed: {result.stderr}")
    
    return output_file

def run_analysis(sales_file):
    print("Running Gemini sales analysis...")
    result = subprocess.run([
        "python", "./analysis/gemini_analyzer.py", sales_file
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Analysis failed: {result.stderr}")
    
    return sales_file.replace(".json", "_analysis.md")

def sync_to_feishu(report_file):
    print("Syncing report to Feishu Drive...")
    result = subprocess.run([
        "python", "./sync/feishu_upload.py", report_file
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Sync failed: {result.stderr}")
    
    return result.stdout.strip()

def publish_skill_to_clawhub():
    print("Publishing workflow as ClawHub skill...")
    result = subprocess.run([
        "clawhub", "publish", ".",
        "--slug", "gog-sales-analytics",
        "--name", "GOG Weekly Sales Analytics",
        "--version", "1.2.3",
        "--changelog", "Fix Feishu multipart upload + analyze full discount dataset (no 20-item cap)"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Publish failed: {result.stderr}")
    
    return result.stdout.strip()

if __name__ == "__main__":
    try:
        sales_file = run_scraper()
        report_file = run_analysis(sales_file)
        feishu_url = sync_to_feishu(report_file)
        publish_url = publish_skill_to_clawhub()
        
        print(f"Workflow completed successfully!")
        print(f"Sales report: {report_file}")
        print(f"Feishu link: {feishu_url}")
        print(f"ClawHub skill: {publish_url}")
    except Exception as e:
        print(f"Workflow failed: {str(e)}")
        exit(1)
