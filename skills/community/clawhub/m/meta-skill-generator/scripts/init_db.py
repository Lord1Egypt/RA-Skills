"""
Meta-Skill Generator - Simplified init script
"""
import chromadb
import os
import sys
from pathlib import Path

# Fix encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 技能库根目录
# 获取项目根目录（相对于当前文件位置）
SKILLS_ROOT = Path(__file__).parent.parent / "skills"
VECTOR_STORE_PATH = SKILLS_ROOT / "meta-skill-generator" / "vector_store"

def init_vector_store():
    """初始化向量存储"""
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
    
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_PATH))
    
    # 创建或获取 collection
    collection = client.get_or_create_collection(
        "skills_library",
        metadata={"description": "Skills vector store for meta-skill-generator"}
    )
    
    print(f"[OK] Vector store: {VECTOR_STORE_PATH}")
    print(f"[OK] Collection: {collection.name}")
    print(f"[OK] Skills count: {collection.count()}")
    
    return collection

def register_skill(skill_name: str, description: str, code_lines: int = 0):
    """注册技能到向量库"""
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_PATH))
    collection = client.get_or_create_collection("skills_library")
    
    # 构建描述文本
    doc = f"""
    Skill: {skill_name}
    Description: {description}
    Code Lines: {code_lines}
    """
    
    # 存入向量库
    collection.add(
        ids=[skill_name],
        documents=[doc],
        metadatas=[{
            "name": skill_name,
            "lines": code_lines,
            "type": "workspace_skill"
        }]
    )
    
    print(f"[OK] Registered: {skill_name}")

def search_skills(query: str, top_k: int = 3):
    """检索技能"""
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_PATH))
    collection = client.get_or_create_collection("skills_library")
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    return results

if __name__ == "__main__":
    # Initialize
    collection = init_vector_store()
    
    # Skills to register
    skills_to_register = [
        ("truthfulness", "Truthfulness principle - never deceive user", 80),
        ("skill-manager", "Skills management assistant", 50),
        ("energy-productivity", "Energy productivity system", 150),
        ("daily-digest", "Daily digest skill", 100),
    ]
    
    print("\nRegistering skills:")
    for name, desc, lines in skills_to_register:
        register_skill(name, desc, lines)
    
    # Test search
    print("\nTest query 'how to ensure truthfulness':")
    results = search_skills("how to ensure truthfulness")
    print(f"Found {len(results['ids'][0])} related skills:")
    for i, name in enumerate(results['ids'][0]):
        print(f"  {i+1}. {name}")
