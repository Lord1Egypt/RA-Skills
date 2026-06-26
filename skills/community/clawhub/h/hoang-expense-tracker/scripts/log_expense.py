import argparse
import csv
import os
from datetime import datetime
import json

def main():
    parser = argparse.ArgumentParser(description="AI Expense Tracker - Log a daily expense")
    parser.add_argument("--amount", type=float, required=True, help="Amount spent (numeric, e.g., 50000)")
    parser.add_argument("--category", type=str, required=True, help="Category (e.g., Food, Transport, Shopping)")
    parser.add_argument("--desc", type=str, required=True, help="Short description of the expense")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Date of expense (YYYY-MM-DD)")
    
    args = parser.parse_args()

    # Lưu file expenses.csv ra ngoài workspace root cho dễ quản lý
    workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(workspace_dir, "expenses.csv")
    
    file_exists = os.path.isfile(file_path)
    
    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Date", "Category", "Amount", "Description"])
            writer.writerow([args.date, args.category.capitalize(), args.amount, args.desc])
        
        print(json.dumps({
            "status": "success",
            "message": f"✅ Đã ghi nhận: {args.amount:,.0f}đ - {args.category} ({args.desc})",
            "file": file_path
        }, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False))

if __name__ == "__main__":
    main()