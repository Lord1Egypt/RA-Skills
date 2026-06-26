"""
技能库向量化写入脚本
将技能描述和元数据存入 ChromaDB 向量数据库
"""

import os
import yaml
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import Optional, List, Dict
import hashlib


class SkillLibrary:
    """技能记忆库管理"""
    
    def __init__(self, persist_dir: str = "skills/vector_store"):
        """
        初始化技能库
        
        Args:
            persist_dir: 向量数据库持久化目录
        """
        os.makedirs(persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection = self.client.get_or_create_collection(
            name="skills",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.skills_dir = Path("skills/skill_library")
    
    def load_metadata(self, skill_path: Path) -> Optional[Dict]:
        """加载技能元数据"""
        metadata_file = skill_path / "metadata.yaml"
        
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def build_description(self, metadata: Dict) -> str:
        """构建向量化描述文本"""
        description = f"""
        Skill Name: {metadata.get('name', 'Unnamed')}
        
        Description: {metadata.get('description', '')}
        
        Category: {metadata.get('category', 'general')}
        
        Inputs:
        {chr(10).join(f"- {inp.get('name', '')}: {inp.get('description', '')}" for inp in metadata.get('inputs', []))}
        
        Outputs:
        {chr(10).join(f"- {out.get('name', '')}: {out.get('description', '')}" for out in metadata.get('outputs', []))}
        
        Tags: {', '.join(metadata.get('tags', []))}
        """.strip()
        
        return description
    
    def embed_skill(self, skill_path: str) -> bool:
        """
        将技能向量化存入 ChromaDB
        
        Args:
            skill_path: 技能目录路径
            
        Returns:
            是否成功
        """
        skill_dir = Path(skill_path)
        
        if not skill_dir.exists():
            print(f"❌ 技能目录不存在: {skill_path}")
            return False
        
        metadata = self.load_metadata(skill_dir)
        
        if not metadata:
            print(f"❌ 无法加载元数据: {skill_path}")
            return False
        
        # 生成唯一 ID
        skill_id = metadata.get('id') or self._generate_id(metadata['name'])
        
        # 构建描述
        description = self.build_description(metadata)
        
        try:
            self.collection.add(
                ids=[skill_id],
                documents=[description],
                metadatas=[{
                    "name": metadata.get('name', ''),
                    "path": str(skill_dir),
                    "version": metadata.get('version', '1.0.0'),
                    "category": metadata.get('category', 'general'),
                    "tags": ",".join(metadata.get('tags', []))
                }]
            )
            
            print(f"✅ 技能已注册: {metadata['name']} (ID: {skill_id})")
            return True
            
        except Exception as e:
            print(f"❌ 注册失败: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> Dict:
        """
        语义检索技能
        
        Args:
            query: 查询文本
            top_k: 返回数量
            
        Returns:
            检索结果
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        return results
    
    def get_skill(self, skill_id: str) -> Optional[Dict]:
        """根据 ID 获取技能"""
        try:
            result = self.collection.get(ids=[skill_id])
            if result['ids']:
                return {
                    'id': result['ids'][0],
                    'metadata': result['metadatas'][0],
                    'document': result['documents'][0]
                }
        except Exception as e:
            print(f"❌ 获取技能失败: {e}")
        
        return None
    
    def list_skills(self) -> List[Dict]:
        """列出所有技能"""
        try:
            result = self.collection.get()
            return [
                {
                    'id': r['id'],
                    'metadata': r['metadatas']
                }
                for r in result
            ]
        except:
            return []
    
    def check_duplicate(self, new_description: str, threshold: float = 0.9) -> Optional[str]:
        """
        检查是否重复
        
        Args:
            new_description: 新技能描述
            threshold: 相似度阈值
            
        Returns:
            如果重复，返回相似技能的 ID
        """
        results = self.collection.query(
            query_texts=[new_description],
            n_results=1
        )
        
        if results['distances'] and results['distances'][0]:
            distance = results['distances'][0][0]
            similarity = 1 - distance
            
            if similarity >= threshold:
                return results['ids'][0][0]
        
        return None
    
    def delete_skill(self, skill_id: str) -> bool:
        """删除技能"""
        try:
            self.collection.delete(ids=[skill_id])
            return True
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    def _generate_id(self, name: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(name.encode()).hexdigest()[:12]


def embed_all_skills(skills_dir: str = "skills/skill_library"):
    """批量注册目录下所有技能"""
    library = SkillLibrary()
    
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        print(f"❌ 目录不存在: {skills_dir}")
        return
    
    count = 0
    for skill_dir in skills_path.iterdir():
        if skill_dir.is_dir() and (skill_dir / "metadata.yaml").exists():
            if library.embed_skill(str(skill_dir)):
                count += 1
    
    print(f"\n📊 完成: 共注册 {count} 个技能")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="技能向量化工具")
    parser.add_argument("action", choices=["embed", "search", "list", "check"],
                        help="操作类型")
    parser.add_argument("--path", help="技能路径（embed 时使用）")
    parser.add_argument("--query", help="查询文本（search 时使用）")
    parser.add_argument("--top-k", type=int, default=5, help="返回数量")
    
    args = parser.parse_args()
    
    library = SkillLibrary()
    
    if args.action == "embed":
        if args.path:
            library.embed_skill(args.path)
        else:
            embed_all_skills()
    
    elif args.action == "search":
        if args.query:
            results = library.search(args.query, args.top_k)
            print(f"\n🔍 查询: {args.query}")
            print(f"📊 结果: {results['ids']}")
            for i, (id_, dist) in enumerate(zip(results['ids'][0], results['distances'][0])):
                print(f"  {i+1}. {id_} (相似度: {1-dist:.3f})")
    
    elif args.action == "list":
        skills = library.list_skills()
        print(f"\n📚 共 {len(skills)} 个技能:")
        for s in skills:
            print(f"  - {s['id']}: {s['metadata'].get('name', 'N/A')}")
    
    elif args.action == "check":
        print("请输入技能描述进行重复检查...")
