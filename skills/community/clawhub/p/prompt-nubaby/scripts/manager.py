import json
import sys
import os

# 設置知識庫路徑
KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "../knowledge/master_recipes.json")

def learn_new_recipe(category, name, content):
    """亞瑟專用的學習函數，將新的大師提示詞永久存檔"""
    try:
        with open(KNOWLEDGE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 確保分類存在
        if category not in data:
            data[category] = {}
        
        key = f"nubaby_{name}"
        data[category][key] = {
            "name": name,
            "role": "system",
            "content": content
        }
        
        with open(KNOWLEDGE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return f"✅ 已成功將「{name}」內化至 Nubaby 提示詞大師知識庫！"
    except Exception as e:
        return f"❌ 學習失敗：{str(e)}"

if __name__ == "__main__":
    # 未來可擴充 CLI 調用邏輯
    pass
