import argparse
import csv
import os
import json
from datetime import datetime
from collections import defaultdict

def get_csv_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "expenses.csv")

def log_expense(amount, category, desc, date):
    file_path = get_csv_path()
    file_exists = os.path.isfile(file_path)
    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Date", "Category", "Amount", "Description"])
            writer.writerow([date, category.capitalize(), amount, desc])
        print(json.dumps({"status": "success", "message": f"✅ Ghi nhận: {amount:,.0f}đ - {category} ({desc})"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))

def report():
    file_path = get_csv_path()
    if not os.path.exists(file_path):
        print(json.dumps({"status": "error", "message": "Chưa có dữ liệu thu chi."}))
        return
    
    totals = defaultdict(float)
    total_spent = 0
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        df = pd.read_csv(file_path)
        
        # Calculate totals
        for index, row in df.iterrows():
            totals[row['Category']] += float(row['Amount'])
            total_spent += float(row['Amount'])
            
        # Generate chart
        chart_path = os.path.join(os.path.dirname(file_path), "expense_chart.png")
        plt.figure(figsize=(8, 6))
        plt.pie(totals.values(), labels=totals.keys(), autopct='%1.1f%%', startangle=140)
        plt.title(f"Tổng chi tiêu: {total_spent:,.0f} đ")
        plt.savefig(chart_path)
        plt.close()
        
        summary = "\\n".join([f"- {k}: {v:,.0f}đ" for k, v in totals.items()])
        print(json.dumps({
            "status": "success", 
            "message": f"📊 Báo cáo tổng quan:\\n{summary}\\nTổng cộng: {total_spent:,.0f}đ",
            "chart_path": chart_path
        }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Lỗi tạo báo cáo: {e}"}, ensure_ascii=False))

def roast():
    file_path = get_csv_path()
    if not os.path.exists(file_path):
        print(json.dumps({"status": "success", "message": "Chưa có data, tiêu tiền đi rồi chửi."}))
        return
        
    totals = defaultdict(float)
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                totals[row['Category']] += float(row['Amount'])
                
        # Simple roast logic
        food = totals.get('Food', 0)
        other = totals.get('Other', 0)
        drink = totals.get('Drink', 0)
        total = sum(totals.values())
        
        roast_msg = "Chê:"
        if food > total * 0.5:
            roast_msg += " Ăn lắm thế, tính làm food reviewer hay gì?"
        elif drink > 0 or other > 0:
            roast_msg += f" Tiêu linh tinh (Trà đá/Thuốc lá/Đồ lặt vặt) {drink+other:,.0f}đ rồi đấy, tích tiểu thành đại nghèo lúc nào không hay!"
        else:
            roast_msg += " Tiêu cũng có vẻ hợp lý, nhưng nhớ tiết kiệm phòng thân."
            
        print(json.dumps({"status": "success", "message": roast_msg}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["log", "report", "roast", "budget"], help="Action to perform")
    parser.add_argument("--amount", type=float, default=0)
    parser.add_argument("--category", type=str, default="Other")
    parser.add_argument("--desc", type=str, default="")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    if args.action == "log":
        log_expense(args.amount, args.category, args.desc, args.date)
    elif args.action == "report":
        report()
    elif args.action == "roast":
        roast()
    elif args.action == "budget":
        print(json.dumps({"status": "success", "message": f"Đã set ngân sách cho {args.category} là {args.amount:,.0f}đ (Mô phỏng)."}, ensure_ascii=False))

if __name__ == "__main__":
    main()