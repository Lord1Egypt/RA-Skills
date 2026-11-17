"""
MongoDB 分类管理器
管理文件分类体系，支持 LLM 自行生成数据库命令进行增删改查。
"""

import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict


def _serialize_doc(doc: dict) -> dict:
    """将 MongoDB 文档转为 JSON 可序列化格式"""
    if doc is None:
        return None
    result = {}
    for k, v in doc.items():
        if k == "_id":
            result[k] = str(v)
        elif isinstance(v, datetime):
            result[k] = v.isoformat()
        elif isinstance(v, dict):
            result[k] = _serialize_doc(v)
        elif isinstance(v, list):
            result[k] = [_serialize_doc(i) if isinstance(i, dict) else i for i in v]
        else:
            result[k] = v
    return result


@dataclass
class Category:
    """分类数据结构"""
    name: str
    slug: str
    parent_id: str = None
    path: str = ""
    description: str = ""
    keywords: List[str] = None
    level: int = 0
    children_count: int = 0
    file_count: int = 0
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


class MongoManager:
    """
    MongoDB 分类管理器
    提供分类的增删改查操作，同时支持执行 LLM 生成的命令。
    """

    def __init__(self, uri: str = "mongodb://localhost:27017", database: str = "knowledge_skill"):
        self.uri = uri
        self.database_name = database
        self._db = None
        self._client = None

    @property
    def db(self):
        """懒加载数据库连接"""
        if self._db is None:
            from pymongo import MongoClient
            self._client = MongoClient(self.uri)
            self._db = self._client[self.database_name]
        return self._db

    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    # ==================== 分类 CRUD ====================

    def get_all_categories(self, as_tree: bool = False) -> list:
        """获取所有分类，可选返回树形结构"""
        cats = list(self.db.categories.find({}).sort("path", 1))
        cats = [_serialize_doc(c) for c in cats]
        if as_tree:
            return self._build_tree(cats)
        return cats

    def get_category_tree_json(self) -> list:
        """获取树形结构，适合发给 LLM"""
        cats = list(self.db.categories.find({}).sort("path", 1))
        cats = [_serialize_doc(c) for c in cats]
        return self._build_tree(cats)

    def get_category_by_slug(self, slug: str) -> Optional[dict]:
        """根据 slug 查找分类"""
        cat = self.db.categories.find_one({"slug": slug})
        return _serialize_doc(cat) if cat else None

    def get_category_by_id(self, cat_id: str) -> Optional[dict]:
        """根据 ID 查找分类"""
        from bson import ObjectId
        return self.db.categories.find_one({"_id": ObjectId(cat_id)}, {"_id": 0})

    def get_children(self, parent_slug: str) -> list:
        """获取子分类"""
        parent = self.get_category_by_slug(parent_slug)
        if not parent:
            return []
        children = list(self.db.categories.find(
            {"parent_id": str(parent["_id"])}
        ).sort("name", 1))
        return [_serialize_doc(c) for c in children]

    def create_category(self, name: str, parent_path: str = "",
                        description: str = "", keywords: list = None) -> dict:
        """
        创建新分类
        parent_path: 父分类路径，如 "/法律法规"，空字符串表示一级分类
        """
        slug = self._slugify(name)
        now = datetime.utcnow()

        # 检查是否已存在
        existing = self.db.categories.find_one({"slug": slug})
        if existing:
            return existing

        parent_id = None
        level = 0
        path = f"/{name}"

        if parent_path:
            parent_slug = parent_path.strip("/").split("/")[-1]
            parent = self.db.categories.find_one({"slug": parent_slug})
            if parent:
                parent_id = str(parent["_id"])
                level = parent.get("level", 0) + 1
                path = f"{parent.get('path', '')}/{name}"
                # 更新父分类的 children_count
                self.db.categories.update_one(
                    {"_id": parent["_id"]},
                    {"$inc": {"children_count": 1}, "$set": {"updated_at": now}}
                )

        cat = {
            "name": name,
            "slug": slug,
            "parent_id": parent_id,
            "path": path,
            "description": description,
            "keywords": keywords or [],
            "level": level,
            "children_count": 0,
            "file_count": 0,
            "created_at": now,
            "updated_at": now
        }

        result = self.db.categories.insert_one(cat)
        cat["_id"] = str(result.inserted_id)
        return _serialize_doc(cat)

    def update_category(self, slug: str, updates: dict) -> dict:
        """更新分类"""
        now = datetime.utcnow()
        updates["updated_at"] = now

        if "name" in updates:
            updates["slug"] = self._slugify(updates["name"])
            # 更新路径
            cat = self.db.categories.find_one({"slug": slug})
            if cat:
                old_name = cat["name"]
                new_path = cat.get("path", "").replace(f"/{old_name}", f"/{updates['name']}")
                updates["path"] = new_path

        self.db.categories.update_one({"slug": slug}, {"$set": updates})
        return self.get_category_by_slug(updates.get("slug", slug))

    def move_category(self, slug: str, new_parent_slug: str) -> dict:
        """移动分类到新的父分类下"""
        # 更新 parent_id 和 level
        parent = self.get_category_by_slug(new_parent_slug)
        if not parent:
            raise ValueError(f"父分类不存在: {new_parent_slug}")

        cat = self.get_category_by_slug(slug)
        if not cat:
            raise ValueError(f"分类不存在: {slug}")

        new_path = f"{parent['path']}/{cat['name']}"
        new_level = parent.get("level", 0) + 1

        self.db.categories.update_one(
            {"slug": slug},
            {"$set": {
                "parent_id": str(parent["_id"]),
                "path": new_path,
                "level": new_level,
                "updated_at": datetime.utcnow()
            }}
        )
        return self.get_category_by_slug(slug)

    def delete_category(self, slug: str, force: bool = False) -> bool:
        """删除分类"""
        cat = self.get_category_by_slug(slug)
        if not cat:
            return False

        # 检查是否有子分类
        children = list(self.db.categories.find({"parent_id": str(cat["_id"])}))
        if children and not force:
            raise ValueError(f"分类 '{slug}' 下有 {len(children)} 个子分类，请先处理子分类或以 force=True 强制删除")

        # 强制删除子分类
        if force and children:
            for child in children:
                self.delete_category(child["slug"], force=True)

        # 更新父分类的 children_count
        if cat.get("parent_id"):
            from bson import ObjectId
            self.db.categories.update_one(
                {"_id": ObjectId(cat["parent_id"])},
                {"$inc": {"children_count": -1}}
            )

        self.db.categories.delete_one({"slug": slug})
        return True

    def search_categories(self, query: str) -> list:
        """搜索分类（名称或关键词匹配）"""
        cats = list(self.db.categories.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"keywords": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }))
        return [_serialize_doc(c) for c in cats]

    # ==================== 文件操作 ====================

    def register_file(self, original_name: str, stored_path: str,
                      file_size: int, file_type: str, md5_hash: str,
                      category_id: str, category_path: str,
                      value_score: float, value_reason: str,
                      category_created: bool = False) -> dict:
        """注册新文件记录"""
        now = datetime.utcnow()
        record = {
            "original_name": original_name,
            "stored_path": stored_path,
            "file_size": file_size,
            "file_type": file_type,
            "md5_hash": md5_hash,
            "value_score": value_score,
            "value_reason": value_reason,
            "category_id": category_id,
            "category_path": category_path,
            "category_created": category_created,
            "status": "pending",
            "easy_dataset_project_id": None,
            "dataset_export_path": None,
            "chunk_count": 0,
            "created_at": now,
            "updated_at": now
        }
        result = self.db.files.insert_one(record)

        # 更新分类文件计数
        from bson import ObjectId
        try:
            self.db.categories.update_one(
                {"_id": ObjectId(category_id)},
                {"$inc": {"file_count": 1}}
            )
        except Exception:
            pass

        record["_id"] = str(result.inserted_id)
        return _serialize_doc(record)

    def update_file_status(self, file_id: str, status: str, **kwargs):
        """更新文件状态"""
        from bson import ObjectId
        kwargs["status"] = status
        kwargs["updated_at"] = datetime.utcnow()
        self.db.files.update_one({"_id": ObjectId(file_id)}, {"$set": kwargs})

    def get_file_by_md5(self, md5_hash: str) -> Optional[dict]:
        """检查文件是否已存在（去重）"""
        doc = self.db.files.find_one({"md5_hash": md5_hash})
        return _serialize_doc(doc) if doc else None

    def get_files_by_category(self, category_slug: str) -> list:
        """获取某分类下的所有文件"""
        cat = self.get_category_by_slug(category_slug)
        if not cat:
            return []
        files = list(self.db.files.find(
            {"category_id": str(cat["_id"])}
        ).sort("created_at", -1))
        return [_serialize_doc(f) for f in files]

    def get_all_files(self, status: str = None) -> list:
        """获取所有文件"""
        query = {}
        if status:
            query["status"] = status
        files = list(self.db.files.find(query).sort("created_at", -1))
        return [_serialize_doc(f) for f in files]

    # ==================== 数据集入库 ====================

    def _dataset_collection_name(self, category_slug: str) -> str:
        """数据集集合名：ds_{slug}"""
        return f"ds_{category_slug}"

    def store_datasets(self, category_slug: str, category_path: str,
                       file_name: str, datasets: List[dict]) -> int:
        """
        将数据集批量入库，每个分类一张表（ds_{slug}）
        datasets: [{question, answer, questionLabel, chunkName}, ...]
        返回入库数量
        """
        coll_name = self._dataset_collection_name(category_slug)
        now = datetime.utcnow()
        stored = 0
        for ds in datasets:
            doc = {
                "question": ds.get("question", ds.get("instruction", "")),
                "answer": ds.get("answer", ds.get("output", "")),
                "category_slug": category_slug,
                "category_path": category_path,
                "source_file": file_name,
                "question_label": ds.get("questionLabel", ""),
                "chunk_name": ds.get("chunkName", ""),
                "created_at": now
            }
            try:
                self.db[coll_name].insert_one(doc)
                stored += 1
            except Exception as e:
                print(f"  [WARN] MongoDB 写入失败 (collection={coll_name}): {e}")
        return stored

    def count_datasets(self, category_slug: str = None):
        """统计数据集数量，不传 slug 则统计全部"""
        if category_slug:
            return self.db[self._dataset_collection_name(category_slug)].count_documents({})
        # 统计所有 ds_* 集合
        total = 0
        for name in self.db.list_collection_names():
            if name.startswith("ds_"):
                total += self.db[name].count_documents({})
        return total

    # ==================== 知识库检索 ====================

    def get_knowledge_overview(self) -> list:
        """获取知识库总览：所有分类及其描述、数据集数量"""
        cats = self.get_all_categories()
        overview = []
        for cat in cats:
            slug = cat.get("slug", "")
            overview.append({
                "name": cat.get("name", ""),
                "slug": slug,
                "path": cat.get("path", ""),
                "description": cat.get("description", ""),
                "keywords": cat.get("keywords", []),
                "dataset_count": self.count_datasets(slug),
                "file_count": cat.get("file_count", 0)
            })
        return overview

    def search_knowledge(self, query: str, top_k: int = 5) -> list:
        """
        根据用户问题检索知识库中的相关内容

        策略：
        1. 先在所有分类中搜索匹配的（根据名称、描述、关键词）
        2. 在匹配的分类对应的 ds_* 集合中用 $regex 搜索问题
        3. 返回匹配的 Q&A 对
        """
        results = []

        # Step 1: 搜索匹配的分类
        matched_cats = self.search_categories(query)
        if not matched_cats:
            # 宽泛匹配：所有分类都搜，取标题最相似的
            matched_cats = self.get_all_categories()[:5]

        # Step 2: 在每个匹配分类的数据集集合中搜索
        import re
        query_words = re.split(r'[\s,，。；;]+', query.strip())
        seen = set()

        for cat in matched_cats:
            slug = cat.get("slug", "")
            coll_name = self._dataset_collection_name(slug)
            if coll_name not in self.db.list_collection_names():
                continue

            # 构建搜索条件：问题中包含任意关键词
            search_terms = [re.escape(w) for w in query_words if len(w) >= 2]
            # 对于中文查询词，同时添加单字搜索提高召回率
            if not search_terms:
                search_terms = [re.escape(query.strip()[:10])]
            # 对于中文字符串，拆分为2字词组进行搜索
            cjk_terms = []
            for term in search_terms:
                chars = re.findall(r'[\u4e00-\u9fff]{2}', term)
                cjk_terms.extend(chars)
            if cjk_terms:
                search_terms = list(set(cjk_terms + search_terms))

            regex_pattern = '|'.join(search_terms[:10])

            try:
                cursor = self.db[coll_name].find(
                    {"question": {"$regex": regex_pattern, "$options": "i"}},
                    {"_id": 0}
                ).limit(5)

                for doc in cursor:
                    q = doc.get("question", "")
                    if q not in seen:
                        seen.add(q)
                        results.append({
                            "question": q,
                            "answer": doc.get("answer", ""),
                            "category": cat.get("name", ""),
                            "category_path": cat.get("path", ""),
                            "source_file": doc.get("source_file", "")
                        })
            except Exception:
                pass

            if len(results) >= top_k:
                break

        return results[:top_k]

    def search_knowledge_answers(self, query: str, max_chars: int = 45000) -> str:
        """
        检索知识库并返回纯 answer 拼接文本（作为对话中的知识凭证）

        流程：
        1. 从用户问题中提取关键词
        2. 在匹配分类的 ds_* 集合中搜索问题
        3. 只保留 answer 字段，拼接为一段连续文本
        4. 总字数 ≤ max_chars（默认45000），超出则截断

        返回：拼接后的 answer 文本
        """
        full_results = self.search_knowledge(query, top_k=20)
        answers = [r["answer"] for r in full_results if r.get("answer")]

        combined = "\n\n---\n\n".join(answers)  # 分隔符
        if len(combined) > max_chars:
            combined = combined[:max_chars]
            # 优先在中文句号处截断，其次英文句号+空格
            last_cn = combined.rfind("。")
            last_en = combined.rfind(". ")
            last_punct = max(last_cn, last_en)
            if last_punct > max_chars * 0.8:
                combined = combined[:last_punct + 1] + "\n\n...[已截断至45000字]"
        return combined

    # ==================== LLM 命令执行 ====================

    def execute_llm_command(self, command: str) -> dict:
        """
        执行 LLM 生成的 MongoDB 命令

        支持格式：
        - "db.categories.insertOne({...})"
        - "db.categories.updateOne({...}, {...})"
        - "db.categories.deleteOne({...})"
        - "db.categories.find({...})"

        返回：{"success": True/False, "result": ..., "error": ...}
        """
        import re

        # 安全检查：禁止危险命令
        dangerous = ["drop", "remove(", "deleteMany({}", "updateMany({}",
                      "deleteMany({ })", "updateMany({ })"]
        for d in dangerous:
            if d in command.lower().replace(" ", ""):
                return {"success": False, "error": f"危险命令被拦截: {d}"}

        try:
            # 解析命令
            match = re.match(r'db\.(\w+)\.(\w+)\((.*)\)$', command.strip(), re.DOTALL)
            if not match:
                return {"success": False, "error": f"无法解析命令格式: {command}"}

            collection_name = match.group(1)
            method = match.group(2)
            args_str = match.group(3)

            # 解析参数（简单 JSON 解析）
            args = self._parse_mongo_args(args_str)

            collection = self.db[collection_name]

            # 执行操作
            if method == "insertOne":
                result = collection.insert_one(args[0])
                return {"success": True, "result": {"inserted_id": str(result.inserted_id)}}

            elif method == "insertMany":
                result = collection.insert_many(args[0])
                return {"success": True, "result": {"inserted_count": len(result.inserted_ids)}}

            elif method == "updateOne":
                result = collection.update_one(args[0], args[1])
                return {"success": True, "result": {"matched": result.matched_count, "modified": result.modified_count}}

            elif method == "updateMany":
                result = collection.update_many(args[0], args[1])
                return {"success": True, "result": {"matched": result.matched_count, "modified": result.modified_count}}

            elif method == "deleteOne":
                result = collection.delete_one(args[0])
                return {"success": True, "result": {"deleted_count": result.deleted_count}}

            elif method == "find":
                filter_doc = args[0] if args else {}
                projection = args[1] if len(args) > 1 else None
                results = list(collection.find(filter_doc, projection))
                # 转换 ObjectId
                for r in results:
                    if "_id" in r:
                        r["_id_str"] = str(r["_id"])
                return {"success": True, "result": results}

            elif method == "findOne":
                result = collection.find_one(args[0] if args else {})
                if result and "_id" in result:
                    result["_id_str"] = str(result["_id"])
                return {"success": True, "result": result}

            elif method == "countDocuments":
                result = collection.count_documents(args[0] if args else {})
                return {"success": True, "result": result}

            else:
                return {"success": False, "error": f"不支持的方法: {method}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== 索引初始化 ====================

    def init_indexes(self):
        """初始化数据库索引"""
        self.db.categories.create_index("slug", unique=True)
        self.db.categories.create_index("parent_id")
        self.db.categories.create_index("path")
        self.db.files.create_index("md5_hash", unique=True)
        self.db.files.create_index("category_id")
        self.db.files.create_index("status")
        self.db.files.create_index("created_at")

    # ==================== 辅助方法 ====================

    def _slugify(self, name: str) -> str:
        """生成 slug（确定性哈希，避免 Python hash() 随机化问题）"""
        import re, hashlib
        name = name.strip()
        # 如果包含英文，直接取英文部分
        english = re.sub(r'[^\x00-\x7F]+', '', name).strip().lower()
        if english:
            return re.sub(r'[^a-z0-9]+', '-', english).strip('-')
        # 纯中文：使用确定性 MD5 哈希
        h = hashlib.md5(name.encode('utf-8')).hexdigest()[:6]
        return f"cat_{h}"

    def _build_tree(self, cats: list) -> list:
        """构建分类树"""
        root = [c for c in cats if not c.get("parent_id")]
        node_map = {c.get("_id", ""): {**c, "children": []} for c in cats}

        tree = []
        for c in cats:
            pid = c.get("parent_id")
            if pid and pid in node_map:
                node_map[pid]["children"].append(node_map[c.get("_id", "")])
            elif not pid:
                tree.append(node_map[c.get("_id", "")])

        return tree

    def _parse_mongo_args(self, args_str: str) -> list:
        """解析 MongoDB 命令参数字符串"""
        import re
        # 简单处理：尝试按 JSON 分割
        args = []
        depth = 0
        current = ""
        for char in args_str:
            if char == '{':
                depth += 1
                current += char
            elif char == '}':
                depth -= 1
                current += char
                if depth == 0:
                    try:
                        args.append(json.loads(current))
                    except json.JSONDecodeError:
                        args.append(current)
                    current = ""
            elif depth > 0:
                current += char

        return args
