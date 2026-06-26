"""
Meta-Skill Generator - 向量嵌入搜索 (使用镜像源)
"""
import os
import json
from pathlib import Path

# 设置镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Paths
# 获取项目根目录（相对于当前文件位置）
SKILLS_ROOT = Path(__file__).parent.parent / "skills"
VECTOR_DB = SKILLS_ROOT / "meta-skill-generator" / "vector_db.json"

# 全局模型
_model = None

def get_model():
    global _model
    if _model is None:
        print("[OK] Loading model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("[OK] Model loaded!")
    return _model

def load_skills():
    """加载技能数据"""
    skills_db = SKILLS_ROOT / "meta-skill-generator" / "skills_db.json"
    if skills_db.exists():
        with open(skills_db, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"skills": []}

def generate_embeddings():
    """生成向量嵌入"""
    model = get_model()
    skills_data = load_skills()
    skills = skills_data.get("skills", [])
    
    if not skills:
        print("[ERROR] No skills found")
        return None
    
    print(f"[OK] Found {len(skills)} skills")
    
    # 生成向量
    texts = []
    for skill in skills:
        text = f"{skill.get('name', '')} {skill.get('description', '')}"
        texts.append(text)
    
    print("[OK] Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # 保存
    vector_data = {
        "vectors": {skill["name"]: emb.tolist() for skill, emb in zip(skills, embeddings)},
        "skills": skills,
        "model": "all-MiniLM-L6-v2"
    }
    
    with open(VECTOR_DB, "w", encoding="utf-8") as f:
        json.dump(vector_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Saved {len(embeddings)} vectors")
    return vector_data

def search_by_vector(query: str, top_k: int = 5):
    """向量搜索"""
    model = get_model()
    
    # 加载数据库
    if not VECTOR_DB.exists():
        print("[ERROR] No vectors found. Run generate_embeddings() first.")
        return []
    
    with open(VECTOR_DB, "r", encoding="utf-8") as f:
        vector_data = json.load(f)
    
    # 查询向量
    query_vec = model.encode([query])
    
    # 计算相似度
    vectors = list(vector_data["vectors"].values())
    names = list(vector_data["vectors"].keys())
    
    similarities = cosine_similarity(query_vec, vectors)[0]
    
    # 排序
    results = sorted(zip(names, similarities), key=lambda x: x[1], reverse=True)
    
    return results[:top_k]

# Test
if __name__ == "__main__":
    print("=== Vector Search (Mirror) ===\n")
    
    # 生成向量
    print("Step 1: Generate embeddings")
    generate_embeddings()
    
    # 测试搜索
    print("\nStep 2: Test search")
    tests = ["truthfulness", "skill management", "energy productivity"]
    
    for query in tests:
        print(f"\nQuery: '{query}'")
        results = search_by_vector(query)
        for name, score in results:
            print(f"  {name}: {score:.3f}")
