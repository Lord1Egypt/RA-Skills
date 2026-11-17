"""
JY_Knowledge_Skill - 主控脚本
知识库智能文件分类与数据集自动生成系统

用法：
  python main.py --file D:/docs/example.pdf       # 处理单个文件
  python main.py --dir D:/docs/                    # 批量处理目录
  python main.py --test                            # 测试所有连接
  python main.py --categories                      # 查看分类树
  python main.py --config                          # 查看/修改配置
"""

import sys
import os

# 修复 Windows GBK 编码问题（确保中文输出正常）
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import os
import sys
import json
import argparse
import hashlib
import shutil
from datetime import datetime

# 确保能找到同目录下的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager
from easy_dataset_client import EasyDatasetClient
from file_preprocessor import FilePreprocessor, VisionLLMClient
from mongo_manager import MongoManager
from classifier import LLMClassifier


class KnowledgeSkill:
    """知识库技能主控器"""

    def __init__(self, config_path: str = None):
        # 初始化各组件
        self.config_mgr = ConfigManager(config_path)
        self.config = self.config_mgr.config

        # EasyDataset 客户端
        ed = self.config.get("easy_dataset", {})
        self.ed_client = EasyDatasetClient(base_url=ed.get("base_url", "http://localhost:1717"))

        # MongoDB 管理器
        mongo = self.config.get("mongodb", {})
        self.mongo = MongoManager(
            uri=mongo.get("uri", "mongodb://localhost:27017"),
            database=mongo.get("database", "knowledge_skill")
        )
        self._mongo_initialized = False

        # LLM 分类器
        llm = self.config.get("llm", {})
        self.classifier = LLMClassifier(
            base_url=llm.get("base_url", ""),
            api_key=llm.get("api_key", ""),
            model=llm.get("model", "")
        )

        # 视觉LLM客户端
        self.vision_llm = VisionLLMClient(
            base_url=llm.get("base_url", ""),
            api_key=llm.get("api_key", ""),
            model=llm.get("vision_model", llm.get("model", ""))
        )

        # 文件预处理器
        vision_limit = min(self.config.get("llm", {}).get("vision_concurrency_limit", 10), 20)
        self.preprocessor = FilePreprocessor(
            vision_llm_client=self.vision_llm,
            temp_dir=self.config.get("output", {}).get("processed_dir", "D:/knowledge_skill/processed"),
            max_vision_concurrency=vision_limit
        )

        # 文件路径配置
        self.datasets_dir = self.config.get("output", {}).get("datasets_dir", "D:/knowledge_skill/datasets")
        self.uploads_dir = self.config.get("output", {}).get("uploads_dir", "D:/knowledge_skill/uploads")

    def init(self, init_mongo: bool = True):
        """初始化系统"""
        if init_mongo:
            self.mongo.init_indexes()
            self._mongo_initialized = True
        print("[INIT] 系统初始化完成")

    def test_connections(self) -> bool:
        """测试所有连接"""
        return self.config_mgr.test_and_report()

    def show_categories(self):
        """显示分类树"""
        tree = self.mongo.get_category_tree_json()
        print("\n当前分类体系：")
        print(json.dumps(tree, ensure_ascii=False, indent=2))

    def _extract_text_sample(self, file_path: str, max_chars: int = 4000) -> str:
        """提取文件文本样本"""
        ext = os.path.splitext(file_path)[1].lower()

        if ext in (".md", ".txt"):
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                return f.read(max_chars)

        elif ext == ".pdf":
            try:
                import pdfplumber
                texts = []
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages[:3]:
                        text = page.extract_text()
                        if text:
                            texts.append(text)
                        if sum(len(t) for t in texts) >= max_chars:
                            break
                return "\n".join(texts)[:max_chars]
            except Exception:
                return ""

        elif ext == ".docx":
            try:
                import mammoth
                with open(file_path, "rb") as f:
                    result = mammoth.extract_raw_text(f)
                return result.value[:max_chars]
            except Exception:
                return ""

        # 图片等不可直接提取文本的格式
        return ""

    def _copy_to_uploads(self, file_path: str) -> str:
        """复制文件到 uploads 目录（失败时返回原路径）"""
        try:
            os.makedirs(self.uploads_dir, exist_ok=True)
            file_hash = self._md5(file_path)[:8]
            ext = os.path.splitext(file_path)[1]
            dest = os.path.join(self.uploads_dir, f"{file_hash}{ext}")
            if not os.path.exists(dest):
                shutil.copy2(file_path, dest)
            return dest
        except (PermissionError, OSError):
            return file_path  # 无法复制时直接使用原路径

    def _md5(self, file_path: str) -> str:
        """计算 MD5"""
        h = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def process_file(self, file_path: str,
                     skip_value_check: bool = False,
                     interactive: bool = True) -> dict:
        """
        处理单个文件的完整流程

        流程：
        1. 文件预处理 → Markdown
        2. 价值评估（LLM）
        3. 智能分类（LLM + MongoDB）
        4. 参数确认（对话式）
        5. EasyDataset 生成数据集
        6. 导出 JSON → 归档到 MongoDB

        返回处理结果 dict
        """
        file_path = os.path.normpath(file_path)
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}

        original_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        file_md5 = self._md5(file_path)

        print(f"\n{'='*60}")
        print(f"  Processing: {original_name}")
        print(f"  Size: {file_size:,} bytes | MD5: {file_md5[:16]}...")
        print(f"{'='*60}")

        result = {
            "file": original_name,
            "md5": file_md5,
            "status": "pending",
            "steps": {}
        }

        # ========== Step 0: Dedup check ==========
        existing = self.mongo.get_file_by_md5(file_md5)
        if existing:
            print(f"\n[SKIP] File already processed: {existing.get('original_name')}")
            result["status"] = "skipped"
            result["existing_record"] = existing
            return result

        # ========== Step 1: 文件预处理 ==========
        print("\n[Step 1] 文件预处理...")
        try:
            # 复制到 uploads
            uploaded_path = self._copy_to_uploads(file_path)

            # 预处理为 Markdown
            markdown_path = self.preprocessor.process(uploaded_path)
            with open(markdown_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()

            print(f"  预处理完成 → {markdown_path}")
            print(f"  Markdown 长度: {len(markdown_content)} 字符")
            result["steps"]["preprocess"] = {
                "markdown_path": markdown_path,
                "content_length": len(markdown_content)
            }
        except Exception as e:
            result["status"] = "failed"
            result["error"] = f"预处理失败: {e}"
            print(f"  [失败] {e}")
            return result

        # ========== Step 2: 价值评估 ==========
        if not skip_value_check:
            print("\n[Step 2] 价值评估 (LLM)...")
            try:
                sample = self._extract_text_sample(file_path) or markdown_content[:2000]
                value_result = self.classifier.evaluate_value(sample)
                has_value = value_result.get("has_value", False)
                score = value_result.get("score", 0)
                reason = value_result.get("reason", "")

                print(f"  价值评分: {score:.2f} | 有价值: {has_value}")
                print(f"  理由: {reason}")

                threshold = self.config.get("file_filter", {}).get("value_threshold", 0.4)
                if not has_value or score < threshold:
                    print(f"  [跳过] 文件价值不足 (阈值: {threshold})")
                    result["status"] = "low_value"
                    result["value_result"] = value_result
                    return result

                result["value_result"] = value_result
            except Exception as e:
                print(f"  [警告] 价值评估失败: {e}，继续处理...")
                value_result = {"has_value": True, "score": 0.5, "reason": "评估失败，默认通过"}
        else:
            value_result = {"has_value": True, "score": 0.5, "reason": "跳过评估"}

        # ========== Step 3: 智能分类 ==========
        print("\n[Step 3] 智能分类 (LLM + MongoDB)...")
        try:
            category_tree = self.mongo.get_category_tree_json()
            sample = self._extract_text_sample(file_path) or markdown_content[:2000]

            classify_result = self.classifier.classify(
                sample, category_tree,
                threshold=self.config.get("file_filter", {}).get("classification_confidence_threshold", 0.7)
            )

            if classify_result.get("is_new"):
                # 需要创建新分类
                new_cat = classify_result.get("new_category", {})
                name = new_cat.get("name", "未命名分类")
                parent_path = new_cat.get("parent_path", "")
                description = new_cat.get("description", "")
                keywords = new_cat.get("keywords", [])

                print(f"  未匹配现有分类，创建新分类: {name}")
                if interactive:
                    confirm = input(f"  确认创建分类 '{name}'? (Y/n): ").strip().lower()
                    if confirm and confirm != 'y':
                        name = input("  请输入分类名称: ") or name

                cat = self.mongo.create_category(
                    name=name, parent_path=parent_path,
                    description=description, keywords=keywords
                )
                category_id = cat.get("_id", cat.get("_id_str"))
                category_path = cat.get("path", f"/{name}")
                category_created = True
            else:
                category_path = classify_result.get("category_path", "/未分类")
                category_slug = classify_result.get("category_slug", "")

                cat = self.mongo.get_category_by_slug(category_slug) if category_slug else None
                if cat:
                    category_id = str(cat.get("_id", ""))
                    category_created = False
                    print(f"  匹配分类: {category_path} (置信度: {classify_result.get('confidence', 0):.2f})")
                else:
                    # slug 不匹配，当作新分类处理
                    suggested_name = classify_result.get("category_path", "").strip("/").split("/")[-1] or "未命名分类"
                    print(f"  分类 '{suggested_name}' 不存在，自动创建")
                    cat = self.mongo.create_category(name=suggested_name)
                    category_id = cat.get("_id", cat.get("_id_str"))
                    category_path = cat.get("path", f"/{suggested_name}")
                    category_created = True

            result["classification"] = {
                "category_path": category_path,
                "category_created": category_created,
                "confidence": classify_result.get("confidence", 0)
            }

            # 提取 GA 判断结果
            use_ga = self.config.get("dataset_generation", {}).get("include_ga_pairs", True)
            if use_ga and classify_result.get("suggest_ga"):
                ga_info = {
                    "genre": classify_result.get("ga_genre", "起草者"),
                    "audience": classify_result.get("ga_audience", "审核者")
                }
                print(f"  GA增强: 已启用 ({ga_info['genre']} / {ga_info['audience']})")
            else:
                ga_info = None
                if use_ga:
                    print(f"  GA增强: LLM判断不适合，跳过")
        except Exception as e:
            print(f"  [错误] 分类失败: {e}")
            category_path = "/未分类"
            category_id = None
            category_created = False
            ga_info = None

        # ========== Step 4: 参数确认 ==========
        print("\n[Step 4] 参数确认...")
        if interactive:
            self.config_mgr.print_params_confirm_list()
            print("\n  输入 'ok' 确认所有参数，或输入 'edit' 修改参数")
            choice = input("  > ").strip().lower()
            if choice == 'edit':
                self._interactive_edit_params()

        # ========== Step 5: 注册文件到 MongoDB ==========
        file_record = self.mongo.register_file(
            original_name=original_name,
            stored_path=uploaded_path,
            file_size=file_size,
            file_type=file_ext[1:],
            md5_hash=file_md5,
            category_id=category_id or "",
            category_path=category_path,
            value_score=value_result.get("score", 0),
            value_reason=value_result.get("reason", ""),
            category_created=category_created
        )
        file_id = file_record.get("_id", "")

        # ========== Step 6: EasyDataset 生成数据集 ==========
        print("\n[Step 6] EasyDataset 数据集生成...")
        llm_config = self.config.get("llm", {})

        model_config = {
            "providerId": llm_config.get("provider", "openai"),
            "endpoint": llm_config.get("base_url", ""),
            "apiKey": llm_config.get("api_key", ""),
            "modelId": llm_config.get("model", ""),
            "modelName": llm_config.get("model", ""),
            "type": "chat",
            "temperature": llm_config.get("temperature", 0.7),
            "maxTokens": llm_config.get("max_tokens", 4096)
        }

        import time
        short_name = os.path.splitext(original_name)[0][:20]
        project_name = f"JYKG_{short_name}_{int(time.time())}"
        language = self.config.get("dataset_generation", {}).get("language", "中文")

        try:
            task_timeout = self.config.get("dataset_generation", {}).get("task_timeout_minutes", 720) * 60
            datasets = self.ed_client.run_full_pipeline(
                markdown_path=markdown_path,
                model_config=model_config,
                project_name=project_name,
                language=language,
                ga_info=ga_info,
                task_timeout=task_timeout,
                progress_callback=lambda step, msg, data=None: print(f"  [{step}] {msg}")
            )

            # Step 7: 问题去重（重复问题删除整条数据集）
            if datasets:
                seen_questions = set()
                deduped = []
                dup_count = 0
                for ds in datasets:
                    q = ds.get("instruction", ds.get("question", "")).strip()
                    if q and q in seen_questions:
                        dup_count += 1
                        continue
                    seen_questions.add(q)
                    deduped.append(ds)
                if dup_count:
                    print(f"  去重: 移除 {dup_count} 条重复问题，保留 {len(deduped)} 条")
                datasets = deduped

            # Step 8: 导出到本地（移除 COT 字段）
            print(f"\n[Step 7] 导出数据集到本地...")
            for ds in datasets:
                ds.pop('cot', None)
            print(f"  COT 已移除")
            cat_dir = category_path.strip("/").replace("/", os.sep)
            export_dir = os.path.join(self.datasets_dir, cat_dir, os.path.splitext(original_name)[0])
            try:
                os.makedirs(export_dir, exist_ok=True)
            except PermissionError:
                import tempfile
                export_dir = os.path.join(tempfile.gettempdir(), "knowledge_skill_datasets",
                                          cat_dir, os.path.splitext(original_name)[0])
                os.makedirs(export_dir, exist_ok=True)

            export_format = self.config.get("dataset_generation", {}).get("export_format", "alpaca")
            export_file = os.path.join(export_dir, f"{original_name}_{export_format}.json")

            with open(export_file, "w", encoding="utf-8") as f:
                json.dump(datasets, f, ensure_ascii=False, indent=2)

            print(f"  数据集已导出: {export_file}")
            print(f"  共 {len(datasets)} 条")

            # 数据集入库（按分类存储到 MongoDB）
            cat_slug = category_path.strip("/").split("/")[-1]
            stored_count = self.mongo.store_datasets(cat_slug, category_path, original_name, datasets)
            print(f"  数据集入库: {stored_count} 条")

            # 更新 MongoDB 文件记录
            self.mongo.update_file_status(
                file_id, "completed",
                dataset_export_path=export_file,
                chunk_count=len(datasets)
            )

            result["status"] = "completed"
            result["datasets_count"] = len(datasets)
            result["export_path"] = export_file

        except Exception as e:
            print(f"  [失败] 数据集生成失败: {e}")
            self.mongo.update_file_status(file_id, "failed", error=str(e))
            result["status"] = "failed"
            result["error"] = str(e)

        print(f"\n{'='*60}")
        print(f"  处理完成: {result['status']}")
        print(f"{'='*60}")
        return result

    def process_directory(self, dir_path: str, interactive: bool = False):
        """批量处理目录中的文件"""
        supported = self.config.get("file_filter", {}).get("supported_types", [])
        results = []

        for root, dirs, files in os.walk(dir_path):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext[1:] in supported or ext in supported:
                    file_path = os.path.join(root, f)
                    r = self.process_file(file_path, interactive=interactive)
                    results.append(r)

        # 汇总报告
        completed = sum(1 for r in results if r.get("status") == "completed")
        failed = sum(1 for r in results if r.get("status") == "failed")
        skipped = sum(1 for r in results if r.get("status") in ("skipped", "low_value"))

        print(f"\n{'='*60}")
        print(f"  批量处理完成")
        print(f"  总数: {len(results)} | 成功: {completed} | 失败: {failed} | 跳过: {skipped}")
        print(f"{'='*60}")

        return results

    def _interactive_edit_params(self):
        """交互式编辑参数"""
        params = self.config_mgr.get_params_for_confirm()
        ds = self.config.get("dataset_generation", {})
        key_map = [
            "chunk_min_length", "chunk_max_length", "chunk_overlap",
            "question_generation_length", "question_count_per_chunk",
            "concurrency_limit", "export_format", "export_file_type",
            "task_timeout_minutes"
        ]

        for i, (name, value, unit) in enumerate(params):
            new_val = input(f"  [{name}] 当前值 {value}{f' {unit}' if unit else ''}, 回车确认或输入新值: ").strip()
            if new_val:
                key = key_map[i]
                # 类型转换
                if key in ("chunk_min_length", "chunk_max_length", "chunk_overlap",
                           "question_generation_length", "question_count_per_chunk",
                           "concurrency_limit", "task_timeout_minutes"):
                    try:
                        new_val = int(new_val)
                    except ValueError:
                        print(f"    无效输入，保持原值")
                        continue
                ds[key] = new_val
                print(f"    已更新为: {new_val}")

        self.config["dataset_generation"] = ds
        self.config_mgr.save()

    def cleanup(self):
        """清理资源"""
        self.mongo.close()


def main():
    parser = argparse.ArgumentParser(description="JY_Knowledge_Skill - 知识库智能文件分类与数据集生成")
    parser.add_argument("--file", "-f", help="处理单个文件")
    parser.add_argument("--dir", "-d", help="批量处理目录")
    parser.add_argument("--test", "-t", action="store_true", help="测试所有连接")
    parser.add_argument("--categories", "-c", action="store_true", help="查看分类树")
    parser.add_argument("--config", action="store_true", help="查看/修改配置")
    parser.add_argument("--skip-value-check", action="store_true", help="跳过价值评估")
    parser.add_argument("--yes", "-y", action="store_true", help="跳过交互确认")
    parser.add_argument("--query", "-q", help="搜索知识库（按问题关键词检索）")
    parser.add_argument("--overview", action="store_true", help="知识库总览")

    args = parser.parse_args()

    skill = KnowledgeSkill()
    skill.init()

    try:
        if args.test:
            skill.test_connections()

        elif args.categories:
            skill.show_categories()

        elif args.config:
            skill.config_mgr.print_params_confirm_list()

        elif args.file:
            result = skill.process_file(
                args.file,
                skip_value_check=args.skip_value_check,
                interactive=not args.yes
            )
            if result.get("status") == "completed":
                print(f"\n[OK] 数据集导出路径: {result.get('export_path')}")
            elif result.get("status") == "failed":
                print(f"\n[FAIL] 处理失败: {result.get('error')}")

        elif args.dir:
            skill.process_directory(args.dir, interactive=not args.yes)

        elif args.query:
            answers_text = skill.mongo.search_knowledge_answers(args.query, max_chars=45000)
            print(answers_text)

        elif args.overview:
            overview = skill.mongo.get_knowledge_overview()
            total_ds = skill.mongo.count_datasets()
            print(f"\n知识库总览 ({len(overview)} 个分类, {total_ds} 条数据集):\n")
            for cat in overview:
                print(f"  [{cat['dataset_count']}条] {cat['path']}")
                if cat['description']:
                    print(f"          {cat['description'][:60]}")
            print()

        else:
            parser.print_help()

    finally:
        skill.cleanup()


if __name__ == "__main__":
    main()
