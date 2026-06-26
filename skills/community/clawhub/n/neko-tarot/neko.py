import typer
import json
import random
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

# --- 模型定义 ---
class Card(BaseModel):
    number: int
    name_cn: str
    upright_interpretation: str
    reversed_interpretation: str

class TarotData(BaseModel):
    version: str
    total: int
    cards: List[Card]

ROOT_DIR = Path(__file__).parent

app = typer.Typer(help="“猫咪塔罗”占卜助手")

# --- 数据加载 ---
def load_json(filename: str):
    file_path = ROOT_DIR / filename
    if not file_path.exists():
        typer.echo(f"Error: {filename} not found in {ROOT_DIR}", err=True)
        raise typer.Exit(code=1)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_tarot_data() -> TarotData:
    data = load_json("tarot.json")
    return TarotData(**data)

def load_spreads_data() -> dict:
    return load_json("spreads.json")

def format_output(success: bool, data: dict, error_msg: Optional[str] = None, json_format: bool = False):
    result = {
        "status": "success" if success else "error",
    }
    if success:
        result["data"] = data
    else:
        result["error"] = error_msg
        
    if json_format:
        typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if success:
            typer.echo(result["data"].get("final_prompt", "Success!"))
        else:
            typer.echo(f"Error: {error_msg}", err=True)

# --- 核心逻辑 ---

def generate_prompt(spread: dict, cards_info: List[dict], template: str) -> str:
    cards_text = []
    for info in cards_info:
        orientation = "正位" if not info["rev"] else "逆位"
        pos_str = f"【位置 {info['index']}：{info['pos']}】抽到了 {info['name']}（{orientation}）。含义提示：{info['meaning']}"
        cards_text.append(pos_str)
    
    cards_info_str = "\n".join(cards_text)
    
    final_prompt = template.replace("{spread_name}", spread["name"])
    final_prompt = final_prompt.replace("{spread_usage}", spread["usage"])
    final_prompt = final_prompt.replace("{spread_interpretation}", spread["interpretation"])
    final_prompt = final_prompt.replace("{cards_info}", cards_info_str)
    
    return final_prompt

# --- CLI 指令 ---

@app.command()
def list():
    """列出所有可用的牌阵 (Agent 引导用)"""
    spreads_data = load_spreads_data()
    spreads = spreads_data.get("spreads", {})
    
    for s_id, s in spreads.items():
        typer.echo(f"ID: {s_id}")
        typer.echo(f"名称: {s['name']} ({s['card_count']}张)")
        typer.echo(f"用途: {s['usage']}")
        typer.echo("-" * 40)

@app.command()
def draw(
    spread_id: str = typer.Option(..., "--spread", help="牌阵ID"),
    no_rev: bool = typer.Option(False, "--no-rev", help="是否不生成逆位"),
    json_format: bool = typer.Option(False, "--json", help="输出JSON格式")
):
    """数字抽卡模式：随机生成结果并输出 Prompt"""
    spreads_data = load_spreads_data()
    spreads = spreads_data.get("spreads", {})
    
    if spread_id not in spreads:
        format_output(False, {}, f"找不到牌阵ID: {spread_id}", json_format)
        raise typer.Exit(code=1)
        
    spread = spreads[spread_id]
    count = spread["card_count"]
    
    tarot_data = load_tarot_data()
    if count > tarot_data.total:
        format_output(False, {}, f"需求牌数 ({count}) 超过总牌数 ({tarot_data.total})", json_format)
        raise typer.Exit(code=1)
        
    # 随机抽牌
    drawn_cards_objs = random.sample(tarot_data.cards, count)
    
    cards_info = []
    drawn_cards_result = []
    
    for i, c in enumerate(drawn_cards_objs):
        rev = False if no_rev else random.choice([True, False])
        meaning = c.reversed_interpretation if rev else c.upright_interpretation
        pos_name = spread["positions"][i]
        
        cards_info.append({
            "index": i + 1,
            "pos": pos_name,
            "name": c.name_cn,
            "rev": rev,
            "meaning": meaning
        })
        
        drawn_cards_result.append({
            "pos": pos_name,
            "name": c.name_cn,
            "rev": rev
        })
        
    template = spreads_data.get("shared_prompt_template", "")
    final_prompt = generate_prompt(spread, cards_info, template)
    
    result_data = {
        "spread_info": { "name": spread["name"], "count": count },
        "drawn_cards": drawn_cards_result,
        "final_prompt": final_prompt
    }
    
    format_output(True, result_data, json_format=json_format)

@app.command()
def compose(
    spread_id: str = typer.Option(..., "--spread", help="牌阵ID"),
    cards: str = typer.Option(..., "--cards", help="以逗号分隔的卡牌ID列表，例如: 0,1,22"),
    revs: str = typer.Option(..., "--revs", help="以逗号分隔的逆位布尔值列表 (1/0 或 true/false)，例如: 0,1,0 或 false,true,false"),
    json_format: bool = typer.Option(False, "--json", help="输出JSON格式")
):
    """
    接收用户手动抽出的牌，拼接并输出发给 LLM 的最终 Prompt。
    """
    spreads_data = load_spreads_data()
    spreads = spreads_data.get("spreads", {})
    
    if spread_id not in spreads:
        format_output(False, {}, f"找不到牌阵ID: {spread_id}", json_format)
        raise typer.Exit(code=1)
        
    spread = spreads[spread_id]
    count = spread["card_count"]
    
    try:
        card_ids = [int(x.strip()) for x in cards.split(",")]
    except ValueError:
        format_output(False, {}, "卡牌ID列表必须为整数类型", json_format)
        raise typer.Exit(code=1)
        
    if len(card_ids) != count:
        format_output(False, {}, f"传入的卡牌数量 ({len(card_ids)}) 与牌阵要求 ({count}) 不符。", json_format)
        raise typer.Exit(code=1)
        
    # 解析复选框
    def parse_bool(v: str):
        v = v.strip().lower()
        if v in ('1', 'true', 't', 'yes', 'y'):
            return True
        if v in ('0', 'false', 'f', 'no', 'n'):
            return False
        raise ValueError(f"无法将 '{v}' 解析为布尔值")
        
    try:
        rev_list = [parse_bool(x) for x in revs.split(",")]
    except ValueError as e:
        format_output(False, {}, str(e), json_format)
        raise typer.Exit(code=1)
        
    if len(rev_list) != count:
        format_output(False, {}, f"传入的逆位布尔值数量 ({len(rev_list)}) 与牌阵要求 ({count}) 不符。", json_format)
        raise typer.Exit(code=1)
        
    tarot_data = load_tarot_data()
    
    cards_info = []
    drawn_cards_result = []
    
    for i in range(count):
        card_id = card_ids[i]
        rev = rev_list[i]
        
        # 查找对应卡牌
        target_card = None
        for c in tarot_data.cards:
            if c.number == card_id:
                target_card = c
                break
                
        if not target_card:
            format_output(False, {}, f"无效的卡牌ID: {card_id}，应在 0-77 之间。", json_format)
            raise typer.Exit(code=1)
            
        meaning = target_card.reversed_interpretation if rev else target_card.upright_interpretation
        pos_name = spread["positions"][i]
        
        cards_info.append({
            "index": i + 1,
            "pos": pos_name,
            "name": target_card.name_cn,
            "rev": rev,
            "meaning": meaning
        })
        
        drawn_cards_result.append({
            "pos": pos_name,
            "name": target_card.name_cn,
            "rev": rev
        })
        
    template = spreads_data.get("shared_prompt_template", "")
    final_prompt = generate_prompt(spread, cards_info, template)
    
    result_data = {
        "spread_info": { "name": spread["name"], "count": count },
        "drawn_cards": drawn_cards_result,
        "final_prompt": final_prompt
    }
    
    format_output(True, result_data, json_format=json_format)

if __name__ == "__main__":
    app()
