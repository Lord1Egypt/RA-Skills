import sys
import json
import os

# Add bot directory to path to import relation_engine
bot_dir = "/home/admin/.openclaw/workspace/liudao-bot"
sys.path.append(bot_dir)
# IMPORTANT: do NOT os.chdir(bot_dir) because db_manager uses relative path to data/liudao.db 
# based on __file__ of db_manager.py, but actually it might be hardcoded to liudao-bot/data/liudao.db
# Let's check db_manager.py path handling:
os.chdir("/home/admin/.openclaw/workspace")

try:
    from relation_engine import RelationshipEngine
except Exception as e:
    print(json.dumps({"error": f"Could not import RelationshipEngine: {str(e)}"}))
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing arguments. Usage: script.py <person> <target_relation>"}))
        sys.exit(1)
        
    start_person = sys.argv[1]
    target_relation = sys.argv[2]
    
    # Check if target_relation is actually a name to check path between A and B
    engine = RelationshipEngine()
    
    # Quick hack: If target_relation is a name, _get_person will find it
    # If it's a role like "爷爷", we will search DB ourselves
    
    p_b = engine._get_person(target_relation)
    if p_b:
        # It's a name vs name check
        result = engine.check_relationship_two_people(start_person, target_relation)
        print(json.dumps({"status": "success", "results": result}, ensure_ascii=False, indent=2))
        return

    # It's a role check like "爷爷"
    db = engine.db
    res = db.search_person(start_person)
    
    if not res:
        print(json.dumps({"status": "not_found", "message": f"❌ 未找到“{start_person}”的档案。"}))
        return
        
    p_a = res[0]
    rj = p_a.get("relations_json")
    if isinstance(rj, str):
        try:
            rj = json.loads(rj)
        except:
            rj = {}
            
    if "爷" in target_relation or "祖父" in target_relation:
        # Grandparent logic: A -> parents -> parents
        parents = rj.get("parents", [])
        grandparents = []
        for p_str in parents:
            p_name = p_str.split("(")[0].strip()
            p_res = db.search_person(p_name)
            if p_res:
                p_p = p_res[0]
                p_rj = p_p.get("relations_json")
                if isinstance(p_rj, str):
                    try:
                        p_rj = json.loads(p_rj)
                    except:
                        p_rj = {}
                gp = p_rj.get("parents", [])
                for g_str in gp:
                    g_name = g_str.split("(")[0].strip()
                    grandparents.append(f"{g_name} ({p_name}的父母)")
        
        if grandparents:
            print(json.dumps({"status": "success", "results": f"**{start_person}** 的祖父/爷爷辈是：\n" + "\n".join([f"- {g}" for g in grandparents])}, ensure_ascii=False))
            return
            
    # Default fallback
    print(json.dumps({"status": "not_found", "message": f"未能自动推导出 {start_person} 的 {target_relation}，请直接使用 search_person 脚本查询。"}))

if __name__ == "__main__":
    main()
