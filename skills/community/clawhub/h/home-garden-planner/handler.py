"""Home Garden Planner - 家庭花园规划师"""
import json
import re

PLANTS = {
    "入门推荐": [
        {"name": "绿萝", "difficulty": "★☆☆☆☆", "light": "耐阴", "water": "土干浇水", "suitable": "新手/室内"},
        {"name": "吊兰", "difficulty": "★☆☆☆☆", "light": "散射光", "water": "保持湿润", "suitable": "新手/室内"},
        {"name": "薄荷", "difficulty": "★★☆☆☆", "light": "充足光照", "water": "每天浇水", "suitable": "阳台/可食用"},
    ],
    "阳台推荐": [
        {"name": "月季", "difficulty": "★★★☆☆", "light": "全日照", "water": "见干见湿", "suitable": "有阳台/观花"},
        {"name": "茉莉", "difficulty": "★★★☆☆", "light": "充足光照", "water": "保持湿润", "suitable": "阳台/芳香"},
        {"name": "小番茄", "difficulty": "★★☆☆☆", "light": "全日照", "water": "每天浇水", "suitable": "阳台/可食用"},
    ],
    "露台/庭院": [
        {"name": "绣球", "difficulty": "★★★☆☆", "light": "半阴", "water": "保持湿润", "suitable": "露台/观花"},
        {"name": "铁线莲", "difficulty": "★★★★☆", "light": "充足光照", "water": "见干见湿", "suitable": "庭院/攀援"},
    ]
}

def parse_garden_input(text: str) -> dict:
    result = {"space": None, "location": None, "experience": "新手", "purpose": []}
    if any(k in text for k in ["室内", "客厅", "卧室", "书房"]): result["space"] = "室内"
    if any(k in text for k in ["阳台", "封闭阳台"]): result["space"] = "阳台"
    if any(k in text for k in ["露台", "庭院", "院子", "花园"]): result["space"] = "露台/庭院"
    if any(k in text for k in ["南向", "阳光充足"]): result["location"] = "南向"
    if any(k in text for k in ["北向", "光线一般"]): result["location"] = "北向"
    if any(k in text for k in ["新手", "第一次", "不会", "没经验"]): result["experience"] = "新手"
    if any(k in text for k in ["食用", "蔬菜", "香草", "调料"]): result["purpose"].append("可食用")
    if any(k in text for k in ["观花", "开花", "好看", "漂亮"]): result["purpose"].append("观花")
    return result

def recommend_plants(parsed: dict) -> list:
    if parsed["space"] == "室内":
        return PLANTS["入门推荐"]
    elif parsed["space"] == "阳台":
        return PLANTS["阳台推荐"]
    else:
        return PLANTS["入门推荐"] + PLANTS["阳台推荐"]

def generate_garden_plan(parsed: dict) -> dict:
    plants = recommend_plants(parsed)
    return {
        "recommendedPlants": plants[:4],
        "layout_suggestion": f"{parsed['space'] or '阳台'}空间，建议采用'高低错落'布局：高处放喜光植物，低处放耐阴植物",
        "seasonal_tips": {"春季": "换盆、施肥、病虫害预防", "夏季": "增加浇水频率、遮阴", "秋季": "修剪、准备越冬", "冬季": "减少浇水、入室保温"}
    }

def handle(text: str) -> dict:
    parsed = parse_garden_input(text)
    plan = generate_garden_plan(parsed)
    return {
        "spaceType": parsed["space"] or "阳台（默认）",
        "location": parsed.get("location", "南向（假设）"),
        "experienceLevel": parsed["experience"],
        "gardenPlan": plan,
        "tools": {"基础工具": ["花铲", "浇水壶", "手套"], "进阶工具": ["枝剪", "喷雾器", "土壤检测仪"]},
        "commonMistakes": ["浇水过多（最常见死因）", "光照不对（买前先了解朝向）", "频繁换盆（植物需要适应期）"]
    }

if __name__ == "__main__":
    for tc in ["我想在封闭阳台种点东西，新手推荐", "南向露台可以种什么花"]:
        r = handle(tc)
        plants = [p["name"] for p in r["gardenPlan"]["recommendedPlants"]]
        print(f"Input: {tc}\n  -> 空间: {r['spaceType']} | 经验: {r['experienceLevel']}\n  -> 推荐: {plants}\n  -> 常见错误: {r['commonMistakes'][0]}\n")
