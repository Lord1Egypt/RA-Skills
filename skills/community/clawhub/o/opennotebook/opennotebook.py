#!/usr/bin/env python3
"""
OpenNotebook CLI - OpenNotebook 知识管理平台命令行客户端

用法:
    python3 opennotebook.py health
    python3 opennotebook.py notebooks list
    python3 opennotebook.py notebooks create --name "名称" --description "描述"
    python3 opennotebook.py sources upload --file /path/to/file.pdf --notebook <id>
    python3 opennotebook.py search query "关键词" --limit 10
    python3 opennotebook.py notes create --content "内容" --title "标题"
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    import requests
except ImportError:
    print("错误: 需要安装 requests 库")
    print("请运行: pip install requests")
    sys.exit(1)

# 配置文件路径
CONFIG_FILE = Path.home() / ".openclaw" / "opennotebook.env"


class Config:
    """配置管理"""

    def __init__(self):
        self.base_url: str = "http://localhost:8000"
        self.api_key: str = ""
        self.timeout: int = 30

    def load(self) -> bool:
        """加载配置文件"""
        if not CONFIG_FILE.exists():
            return False

        with open(CONFIG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    if key == "OPENNOTEBOOK_BASE_URL":
                        self.base_url = value
                    elif key == "OPENNOTEBOOK_API_KEY":
                        self.api_key = value
                    elif key == "OPENNOTEBOOK_TIMEOUT":
                        try:
                            self.timeout = int(value)
                        except ValueError:
                            pass

        return True

    def save(self):
        """保存配置文件"""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            f.write("# OpenNotebook 配置\n")
            f.write(f"OPENNOTEBOOK_BASE_URL={self.base_url}\n")
            if self.api_key:
                f.write(f"OPENNOTEBOOK_API_KEY={self.api_key}\n")
            f.write(f"OPENNOTEBOOK_TIMEOUT={self.timeout}\n")


class OpenNotebookError(Exception):
    """API 错误"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class OpenNotebookClient:
    """OpenNotebook API 客户端"""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.config.base_url.rstrip('/')}{path}"
        headers = self._headers()

        if "files" in kwargs:
            headers.pop("Content-Type", None)

        kwargs.setdefault("timeout", self.config.timeout)

        response = self.session.request(method, url, headers=headers, **kwargs)

        if response.status_code >= 400:
            try:
                error_data = response.json()
            except:
                error_data = {"detail": response.text}
            raise OpenNotebookError(
                f"API Error: {response.status_code} - {error_data}",
                status_code=response.status_code
            )

        if response.status_code == 204:
            return None

        try:
            return response.json()
        except:
            return response.content

    def _get(self, path: str, params: Optional[Dict] = None) -> Any:
        return self._request("GET", path, params=params)

    def _post(self, path: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Any:
        if files:
            return self._request("POST", path, data=data, files=files)
        return self._request("POST", path, json=data)

    def _put(self, path: str, data: Optional[Dict] = None) -> Any:
        return self._request("PUT", path, json=data)

    def _delete(self, path: str, params: Optional[Dict] = None) -> Any:
        return self._request("DELETE", path, params=params)

    # Health
    def health(self) -> Dict:
        return self._get("/health")

    # Notebooks
    def notebooks_list(self, archived: Optional[bool] = None, order_by: Optional[str] = None) -> List[Dict]:
        params = {}
        if archived is not None:
            params["archived"] = archived
        if order_by:
            params["order_by"] = order_by
        return self._get("/api/notebooks", params=params)

    def notebooks_get(self, notebook_id: str) -> Dict:
        return self._get(f"/api/notebooks/{notebook_id}")

    def notebooks_create(self, name: str, description: Optional[str] = None) -> Dict:
        data = {"name": name}
        if description:
            data["description"] = description
        return self._post("/api/notebooks", data=data)

    def notebooks_update(self, notebook_id: str, **kwargs) -> Dict:
        return self._put(f"/api/notebooks/{notebook_id}", data=kwargs)

    def notebooks_delete(self, notebook_id: str, delete_exclusive_sources: bool = False) -> None:
        params = {"delete_exclusive_sources": delete_exclusive_sources}
        return self._delete(f"/api/notebooks/{notebook_id}", params=params)

    # Sources
    def sources_list(self, notebook_id: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict:
        params = {"limit": limit, "offset": offset}
        if notebook_id:
            params["notebook_id"] = notebook_id
        return self._get("/api/sources", params=params)

    def sources_get(self, source_id: str) -> Dict:
        return self._get(f"/api/sources/{source_id}")

    def sources_create(self, type: str, **kwargs) -> Dict:
        data = {"type": type}
        data.update(kwargs)
        return self._post("/api/sources/json", data=data)

    def sources_upload(self, file_path: str, notebook_id: Optional[str] = None,
                       title: Optional[str] = None, embed: bool = True) -> Dict:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        data = {}
        if notebook_id:
            data["notebook_id"] = notebook_id
        if title:
            data["title"] = title
        data["embed"] = str(embed).lower()

        with open(path, "rb") as f:
            files = {"file": (path.name, f)}
            return self._post("/api/sources", data=data, files=files)

    def sources_status(self, source_id: str) -> Dict:
        return self._get(f"/api/sources/{source_id}/status")

    def sources_retry(self, source_id: str) -> Dict:
        return self._post(f"/api/sources/{source_id}/retry")

    def sources_delete(self, source_id: str) -> None:
        return self._delete(f"/api/sources/{source_id}")

    # Notes
    def notes_list(self, notebook_id: Optional[str] = None) -> List[Dict]:
        params = {}
        if notebook_id:
            params["notebook_id"] = notebook_id
        return self._get("/api/notes", params=params)

    def notes_get(self, note_id: str) -> Dict:
        return self._get(f"/api/notes/{note_id}")

    def notes_create(self, content: str, title: Optional[str] = None,
                     note_type: Optional[str] = None, notebook_id: Optional[str] = None) -> Dict:
        data = {"content": content}
        if title:
            data["title"] = title
        if note_type:
            data["note_type"] = note_type
        if notebook_id:
            data["notebook_id"] = notebook_id
        return self._post("/api/notes", data=data)

    def notes_update(self, note_id: str, **kwargs) -> Dict:
        return self._put(f"/api/notes/{note_id}", data=kwargs)

    def notes_delete(self, note_id: str) -> None:
        return self._delete(f"/api/notes/{note_id}")

    # Search
    def search_query(self, query: str, limit: int = 10, search_sources: bool = True,
                     search_notes: bool = True) -> Dict:
        data = {
            "query": query,
            "limit": limit,
            "search_sources": search_sources,
            "search_notes": search_notes
        }
        return self._post("/api/search", data=data)

    def search_ask(self, question: str, strategy_model: str, answer_model: str,
                   final_answer_model: str) -> Dict:
        data = {
            "question": question,
            "strategy_model": strategy_model,
            "answer_model": answer_model,
            "final_answer_model": final_answer_model
        }
        return self._post("/api/search/ask/simple", data=data)

    # Transformations
    def transformations_list(self) -> List[Dict]:
        return self._get("/api/transformations")

    def transformations_get(self, transformation_id: str) -> Dict:
        return self._get(f"/api/transformations/{transformation_id}")

    def transformations_execute(self, transformation_id: str, input_text: str, model_id: str) -> Dict:
        data = {
            "transformation_id": transformation_id,
            "input_text": input_text,
            "model_id": model_id
        }
        return self._post("/api/transformations/execute", data=data)

    # Models
    def models_list(self, type: Optional[str] = None) -> List[Dict]:
        params = {}
        if type:
            params["type"] = type
        return self._get("/api/models", params=params)

    def models_defaults(self) -> Dict:
        return self._get("/api/models/defaults")

    def models_providers(self) -> List[str]:
        return self._get("/api/models/providers")

    def models_sync(self, provider: Optional[str] = None) -> Dict:
        if provider:
            return self._post(f"/api/models/sync/{provider}")
        return self._post("/api/models/sync")

    def models_test(self, model_id: str) -> Dict:
        return self._post(f"/api/models/{model_id}/test")

    # Embeddings
    def embeddings_embed(self, item_id: str, item_type: str) -> Dict:
        data = {"item_id": item_id, "item_type": item_type}
        return self._post("/api/embed", data=data)

    def embeddings_rebuild(self, mode: str = "full") -> Dict:
        data = {"mode": mode}
        return self._post("/api/embeddings/rebuild", data=data)

    def embeddings_status(self, command_id: str) -> Dict:
        return self._get(f"/api/embeddings/rebuild/{command_id}/status")

    # Chat
    def chat_sessions(self) -> List[Dict]:
        return self._get("/api/chat/sessions")

    def chat_create_session(self, **kwargs) -> Dict:
        return self._post("/api/chat/sessions", data=kwargs)

    def chat_execute(self, **kwargs) -> Dict:
        return self._post("/api/chat/execute", data=kwargs)

    # Podcasts
    def podcasts_episodes(self) -> List[Dict]:
        return self._get("/api/podcasts/episodes")

    def podcasts_get(self, episode_id: str) -> Dict:
        return self._get(f"/api/podcasts/episodes/{episode_id}")

    def podcasts_audio(self, episode_id: str) -> bytes:
        return self._get(f"/api/podcasts/episodes/{episode_id}/audio")


def output_json(data: Any):
    """输出 JSON 格式"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="OpenNotebook CLI - 知识管理平台客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 opennotebook.py health
  python3 opennotebook.py notebooks list
  python3 opennotebook.py notebooks create --name "我的笔记本"
  python3 opennotebook.py sources upload --file doc.pdf --notebook <id>
  python3 opennotebook.py search query "机器学习"
        """
    )

    # 全局选项
    parser.add_argument("--base-url", help="API 基础 URL")
    parser.add_argument("--api-key", help="API 密钥")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # health
    subparsers.add_parser("health", help="检查 API 连接状态")

    # notebooks
    nb_parser = subparsers.add_parser("notebooks", help="笔记本操作")
    nb_sub = nb_parser.add_subparsers(dest="action")

    nb_list = nb_sub.add_parser("list", help="列出笔记本")
    nb_list.add_argument("--archived", action="store_true", help="只显示已归档")
    nb_list.add_argument("--order-by", help="排序字段")

    nb_get = nb_sub.add_parser("get", help="获取笔记本")
    nb_get.add_argument("--id", required=True, help="笔记本 ID")

    nb_create = nb_sub.add_parser("create", help="创建笔记本")
    nb_create.add_argument("--name", required=True, help="笔记本名称")
    nb_create.add_argument("--description", help="描述")

    nb_update = nb_sub.add_parser("update", help="更新笔记本")
    nb_update.add_argument("--id", required=True, help="笔记本 ID")
    nb_update.add_argument("--name", help="新名称")
    nb_update.add_argument("--description", help="新描述")
    nb_update.add_argument("--archived", type=lambda x: x.lower() == "true", help="是否归档")

    nb_delete = nb_sub.add_parser("delete", help="删除笔记本")
    nb_delete.add_argument("--id", required=True, help="笔记本 ID")
    nb_delete.add_argument("--delete-sources", action="store_true", help="同时删除专属源")

    # sources
    src_parser = subparsers.add_parser("sources", help="源文件操作")
    src_sub = src_parser.add_subparsers(dest="action")

    src_list = src_sub.add_parser("list", help="列出源文件")
    src_list.add_argument("--notebook", help="笔记本 ID")
    src_list.add_argument("--limit", type=int, default=50, help="数量限制")
    src_list.add_argument("--offset", type=int, default=0, help="偏移量")

    src_get = src_sub.add_parser("get", help="获取源文件")
    src_get.add_argument("--id", required=True, help="源文件 ID")

    src_upload = src_sub.add_parser("upload", help="上传文件")
    src_upload.add_argument("--file", required=True, help="文件路径")
    src_upload.add_argument("--notebook", help="笔记本 ID")
    src_upload.add_argument("--title", help="标题")

    src_url = src_sub.add_parser("create-url", help="从 URL 创建")
    src_url.add_argument("--url", required=True, help="URL 地址")
    src_url.add_argument("--notebook", help="笔记本 ID")

    src_text = src_sub.add_parser("create-text", help="从文本创建")
    src_text.add_argument("--content", required=True, help="文本内容")
    src_text.add_argument("--notebook", help="笔记本 ID")
    src_text.add_argument("--title", help="标题")

    src_status = src_sub.add_parser("status", help="获取处理状态")
    src_status.add_argument("--id", required=True, help="源文件 ID")

    src_retry = src_sub.add_parser("retry", help="重试处理")
    src_retry.add_argument("--id", required=True, help="源文件 ID")

    src_delete = src_sub.add_parser("delete", help="删除源文件")
    src_delete.add_argument("--id", required=True, help="源文件 ID")

    # notes
    note_parser = subparsers.add_parser("notes", help="笔记操作")
    note_sub = note_parser.add_subparsers(dest="action")

    note_list = note_sub.add_parser("list", help="列出笔记")
    note_list.add_argument("--notebook", help="笔记本 ID")

    note_get = note_sub.add_parser("get", help="获取笔记")
    note_get.add_argument("--id", required=True, help="笔记 ID")

    note_create = note_sub.add_parser("create", help="创建笔记")
    note_create.add_argument("--content", required=True, help="内容")
    note_create.add_argument("--title", help="标题")
    note_create.add_argument("--notebook", help="笔记本 ID")

    note_update = note_sub.add_parser("update", help="更新笔记")
    note_update.add_argument("--id", required=True, help="笔记 ID")
    note_update.add_argument("--content", help="内容")
    note_update.add_argument("--title", help="标题")

    note_delete = note_sub.add_parser("delete", help="删除笔记")
    note_delete.add_argument("--id", required=True, help="笔记 ID")

    # search
    search_parser = subparsers.add_parser("search", help="搜索操作")
    search_sub = search_parser.add_subparsers(dest="action")

    search_query = search_sub.add_parser("query", help="搜索知识库")
    search_query.add_argument("query", help="搜索关键词")
    search_query.add_argument("--limit", type=int, default=10, help="结果数量")
    search_query.add_argument("--no-sources", action="store_true", help="不搜索源文件")
    search_query.add_argument("--no-notes", action="store_true", help="不搜索笔记")

    search_ask = search_sub.add_parser("ask", help="提问")
    search_ask.add_argument("--question", required=True, help="问题")
    search_ask.add_argument("--strategy-model", required=True, help="策略模型 ID")
    search_ask.add_argument("--answer-model", required=True, help="回答模型 ID")
    search_ask.add_argument("--final-model", required=True, help="最终模型 ID")

    # transformations
    trans_parser = subparsers.add_parser("transformations", help="转换操作")
    trans_sub = trans_parser.add_subparsers(dest="action")

    trans_sub.add_parser("list", help="列出转换")
    trans_get = trans_sub.add_parser("get", help="获取转换")
    trans_get.add_argument("--id", required=True, help="转换 ID")

    trans_exec = trans_sub.add_parser("execute", help="执行转换")
    trans_exec.add_argument("--id", required=True, help="转换 ID")
    trans_exec.add_argument("--input", required=True, help="输入文本")
    trans_exec.add_argument("--model", required=True, help="模型 ID")

    # models
    model_parser = subparsers.add_parser("models", help="模型操作")
    model_sub = model_parser.add_subparsers(dest="action")

    model_list = model_sub.add_parser("list", help="列出模型")
    model_list.add_argument("--type", help="模型类型")

    model_sub.add_parser("defaults", help="获取默认模型")
    model_sub.add_parser("providers", help="获取提供商列表")

    model_sync = model_sub.add_parser("sync", help="同步模型")
    model_sync.add_argument("--provider", help="提供商名称")

    model_test = model_sub.add_parser("test", help="测试模型")
    model_test.add_argument("--id", required=True, help="模型 ID")

    # embeddings
    emb_parser = subparsers.add_parser("embeddings", help="嵌入操作")
    emb_sub = emb_parser.add_subparsers(dest="action")

    emb_embed = emb_sub.add_parser("embed", help="创建嵌入")
    emb_embed.add_argument("--id", required=True, help="项目 ID")
    emb_embed.add_argument("--type", required=True, choices=["source", "note", "insight"], help="项目类型")

    emb_rebuild = emb_sub.add_parser("rebuild", help="重建嵌入")
    emb_rebuild.add_argument("--mode", default="full", choices=["full", "incremental"], help="重建模式")

    emb_status = emb_sub.add_parser("status", help="重建状态")
    emb_status.add_argument("--command-id", required=True, help="命令 ID")

    # chat
    chat_parser = subparsers.add_parser("chat", help="聊天操作")
    chat_sub = chat_parser.add_subparsers(dest="action")

    chat_sub.add_parser("sessions", help="列出会话")
    chat_sub.add_parser("create-session", help="创建会话")

    # podcasts
    pod_parser = subparsers.add_parser("podcasts", help="播客操作")
    pod_sub = pod_parser.add_subparsers(dest="action")

    pod_sub.add_parser("episodes", help="列出剧集")
    pod_get = pod_sub.add_parser("get", help="获取剧集")
    pod_get.add_argument("--id", required=True, help="剧集 ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 加载配置
    config = Config()
    config.load()

    # 命令行参数覆盖配置
    if args.base_url:
        config.base_url = args.base_url
    if args.api_key:
        config.api_key = args.api_key

    client = OpenNotebookClient(config)

    try:
        # Health
        if args.command == "health":
            result = client.health()
            output_json(result)

        # Notebooks
        elif args.command == "notebooks":
            if args.action == "list":
                result = client.notebooks_list(archived=args.archived, order_by=args.order_by)
            elif args.action == "get":
                result = client.notebooks_get(args.id)
            elif args.action == "create":
                result = client.notebooks_create(name=args.name, description=args.description)
            elif args.action == "update":
                kwargs = {}
                if args.name:
                    kwargs["name"] = args.name
                if args.description:
                    kwargs["description"] = args.description
                if args.archived is not None:
                    kwargs["archived"] = args.archived
                result = client.notebooks_update(args.id, **kwargs)
            elif args.action == "delete":
                result = client.notebooks_delete(args.id, delete_exclusive_sources=args.delete_sources)
                print("✅ 笔记本已删除")
                sys.exit(0)
            else:
                nb_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Sources
        elif args.command == "sources":
            if args.action == "list":
                result = client.sources_list(notebook_id=args.notebook, limit=args.limit, offset=args.offset)
            elif args.action == "get":
                result = client.sources_get(args.id)
            elif args.action == "upload":
                result = client.sources_upload(args.file, notebook_id=args.notebook, title=args.title)
            elif args.action == "create-url":
                result = client.sources_create(type="url", url=args.url, notebook_id=args.notebook)
            elif args.action == "create-text":
                result = client.sources_create(type="text", content=args.content, notebook_id=args.notebook, title=args.title)
            elif args.action == "status":
                result = client.sources_status(args.id)
            elif args.action == "retry":
                result = client.sources_retry(args.id)
            elif args.action == "delete":
                result = client.sources_delete(args.id)
                print("✅ 源文件已删除")
                sys.exit(0)
            else:
                src_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Notes
        elif args.command == "notes":
            if args.action == "list":
                result = client.notes_list(notebook_id=args.notebook)
            elif args.action == "get":
                result = client.notes_get(args.id)
            elif args.action == "create":
                result = client.notes_create(content=args.content, title=args.title, notebook_id=args.notebook)
            elif args.action == "update":
                kwargs = {}
                if args.content:
                    kwargs["content"] = args.content
                if args.title:
                    kwargs["title"] = args.title
                result = client.notes_update(args.id, **kwargs)
            elif args.action == "delete":
                result = client.notes_delete(args.id)
                print("✅ 笔记已删除")
                sys.exit(0)
            else:
                note_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Search
        elif args.command == "search":
            if args.action == "query":
                result = client.search_query(
                    query=args.query,
                    limit=args.limit,
                    search_sources=not args.no_sources,
                    search_notes=not args.no_notes
                )
            elif args.action == "ask":
                result = client.search_ask(
                    question=args.question,
                    strategy_model=args.strategy_model,
                    answer_model=args.answer_model,
                    final_answer_model=args.final_model
                )
            else:
                search_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Transformations
        elif args.command == "transformations":
            if args.action == "list":
                result = client.transformations_list()
            elif args.action == "get":
                result = client.transformations_get(args.id)
            elif args.action == "execute":
                result = client.transformations_execute(args.id, args.input, args.model)
            else:
                trans_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Models
        elif args.command == "models":
            if args.action == "list":
                result = client.models_list(type=args.type)
            elif args.action == "defaults":
                result = client.models_defaults()
            elif args.action == "providers":
                result = client.models_providers()
            elif args.action == "sync":
                result = client.models_sync(provider=args.provider)
            elif args.action == "test":
                result = client.models_test(args.id)
            else:
                model_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Embeddings
        elif args.command == "embeddings":
            if args.action == "embed":
                result = client.embeddings_embed(args.id, args.type)
            elif args.action == "rebuild":
                result = client.embeddings_rebuild(mode=args.mode)
            elif args.action == "status":
                result = client.embeddings_status(args.command_id)
            else:
                emb_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Chat
        elif args.command == "chat":
            if args.action == "sessions":
                result = client.chat_sessions()
            elif args.action == "create-session":
                result = client.chat_create_session()
            else:
                chat_parser.print_help()
                sys.exit(1)
            output_json(result)

        # Podcasts
        elif args.command == "podcasts":
            if args.action == "episodes":
                result = client.podcasts_episodes()
            elif args.action == "get":
                result = client.podcasts_get(args.id)
            else:
                pod_parser.print_help()
                sys.exit(1)
            output_json(result)

        else:
            parser.print_help()

    except OpenNotebookError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到 {config.base_url}")
        sys.exit(1)


if __name__ == "__main__":
    main()