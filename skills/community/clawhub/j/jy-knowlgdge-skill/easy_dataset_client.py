"""
EasyDataset API Client
封装 EasyDataset 的 HTTP API，实现从项目创建到数据集导出的完整自动化管线。
EasyDataset 运行在 Docker 中，默认端口 1717。
"""

import requests
import time
import json
import os
from typing import Optional, Dict, Any, List
from urllib.parse import quote


class EasyDatasetClient:
    """EasyDataset HTTP API 客户端"""

    def __init__(self, base_url: str = "http://localhost:1717", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _post(self, path: str, data: Any = None, headers: dict = None, timeout: int = None) -> dict:
        url = f"{self.base_url}{path}"
        h = headers or {}
        t = timeout or self.timeout
        if isinstance(data, dict) and "Content-Type" not in h:
            h["Content-Type"] = "application/json"
            resp = self.session.post(url, json=data, headers=h, timeout=t)
        elif isinstance(data, bytes):
            resp = self.session.post(url, data=data, headers=h, timeout=t)
        else:
            h["Content-Type"] = "application/json"
            resp = self.session.post(url, json=data or {}, headers=h, timeout=t)
        resp.raise_for_status()
        return resp.json()

    def _get(self, path: str, params: dict = None) -> Any:
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _put(self, path: str, data: dict) -> dict:
        url = f"{self.base_url}{path}"
        resp = self.session.put(url, json=data, headers={"Content-Type": "application/json"}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _delete(self, path: str, params: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        resp = self.session.delete(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _patch(self, path: str, data: dict) -> dict:
        url = f"{self.base_url}{path}"
        resp = self.session.patch(url, json=data, headers={"Content-Type": "application/json"}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    # ==================== 项目管理 ====================

    def create_project(self, name: str, description: str = "") -> str:
        """
        创建项目，返回 projectId
        """
        resp = self._post("/api/projects", {"name": name, "description": description})
        return resp.get("id", resp.get("projectId"))

    def get_project(self, project_id: str) -> dict:
        """获取项目详情"""
        return self._get(f"/api/projects/{project_id}")

    def delete_project(self, project_id: str) -> bool:
        """删除项目"""
        self._delete(f"/api/projects/{project_id}")
        return True

    def list_projects(self) -> list:
        """获取所有项目列表"""
        return self._get("/api/projects")

    # ==================== 模型配置 ====================

    def configure_model(self, project_id: str, config: dict) -> str:
        """
        配置 LLM 模型
        策略：先获取已有配置列表，找到 providerId 为 "openai" 的配置，
        使用其 id 进行 upsert 更新自定义端点。

        config: { providerId, endpoint, apiKey, modelId, modelName, type, temperature?, maxTokens?, topP? }
        返回 modelConfigId
        """
        # Step 1: 获取已有配置
        existing = self.get_model_config(project_id)
        existing_list = existing.get("data", existing if isinstance(existing, list) else [])

        # Step 2: 找到 openai provider 的配置，获取其 id
        provider_id = config.get("providerId", "openai")
        model_config_id = None
        for mc in existing_list:
            if mc.get("providerId") == provider_id:
                model_config_id = mc.get("id")
                break

        if not model_config_id and existing_list:
            model_config_id = existing_list[0].get("id")

        # Step 3: 构建配置数据
        payload = {
            "projectId": project_id,
            "providerId": provider_id,
            "providerName": config.get("providerName", "Custom"),
            "endpoint": config.get("endpoint", ""),
            "apiKey": config.get("apiKey", ""),
            "modelId": config.get("modelId", config.get("modelName", "")),
            "modelName": config.get("modelName", config.get("modelId", "")),
            "type": config.get("type", "chat"),
            "temperature": config.get("temperature", 0.7),
            "maxTokens": config.get("maxTokens", 4096),
            "topP": config.get("topP", 0.9),
            "topK": config.get("topK", 0),
            "status": 1
        }

        if model_config_id:
            payload["id"] = model_config_id

        resp = self._post(f"/api/projects/{project_id}/model-config", payload)
        return resp.get("id", model_config_id or "")

    def get_model_config(self, project_id: str) -> list:
        """获取项目的模型配置列表"""
        return self._get(f"/api/projects/{project_id}/model-config")

    def set_default_model(self, project_id: str, model_config_id: str) -> bool:
        """设置项目默认模型"""
        self._put(f"/api/projects/{project_id}", {"defaultModelConfigId": model_config_id})
        return True

    def get_llm_providers(self) -> list:
        """获取 LLM 提供商列表"""
        return self._get("/api/llm/providers")

    # ==================== 文件上传 ====================

    def upload_file(self, project_id: str, file_path: str) -> str:
        """
        上传文件到项目
        file_path: 本地文件路径（仅支持 .md / .pdf）
        返回 fileId
        """
        file_name = os.path.basename(file_path)
        encoded_name = quote(file_name, safe="")
        headers = {"x-file-name": encoded_name}

        with open(file_path, "rb") as f:
            file_data = f.read()

        resp = self._post(
            f"/api/projects/{project_id}/files",
            data=file_data,
            headers=headers
        )
        return resp.get("fileId")

    def list_files(self, project_id: str, page: int = 0, page_size: int = 100) -> dict:
        """获取文件列表"""
        return self._get(f"/api/projects/{project_id}/files", {"page": page, "pageSize": page_size})

    def delete_file(self, project_id: str, file_id: str, model: dict = None, language: str = "中文") -> bool:
        """删除文件"""
        self._delete(
            f"/api/projects/{project_id}/files",
            {"fileId": file_id, "model": model or {}, "language": language, "domainTreeAction": "keep"}
        )
        return True

    # ==================== 文本分割 ====================

    def split_files(self, project_id: str, file_list: list, model: dict, language: str = "中文",
                    domain_tree_action: str = "rebuild", timeout: int = 180) -> dict:
        """
        批量分割文件
        file_list: [{fileName, fileId}, ...]
        timeout: HTTP 超时秒数（大文件需要更长）
        """
        return self._post(f"/api/projects/{project_id}/split", {
            "fileNames": file_list,
            "model": model,
            "language": language,
            "domainTreeAction": domain_tree_action
        }, timeout=timeout)

    def get_chunks(self, project_id: str) -> dict:
        """获取所有文本块和标签"""
        return self._get(f"/api/projects/{project_id}/split")

    def generate_ga_pairs(self, project_id: str, file_ids: list, model_config_id: str,
                          language: str = "中文") -> dict:
        """
        为文件批量生成 GA（Genre-Audience）对
        file_ids: 文件ID列表
        model_config_id: 模型配置ID（configure_model 返回值）
        """
        return self._post(f"/api/projects/{project_id}/batch-generateGA", {
            "fileIds": file_ids,
            "modelConfigId": model_config_id,
            "language": language
        })

    # ==================== 任务管理（核心） ====================

    def _build_model_info(self, model_config: dict) -> dict:
        """从模型配置构建 modelInfo"""
        return {
            "providerId": model_config.get("providerId", ""),
            "endpoint": model_config.get("endpoint", ""),
            "apiKey": model_config.get("apiKey", ""),
            "modelId": model_config.get("modelId", ""),
            "modelName": model_config.get("modelName", ""),
            "type": model_config.get("type", "chat"),
            "temperature": model_config.get("temperature", 0.7),
            "maxTokens": model_config.get("maxTokens", 4096),
            "topP": model_config.get("topP", 0.9),
            "topK": model_config.get("topK", 0),
            "status": 1
        }

    def create_task(self, project_id: str, task_type: str, model_config: dict,
                    language: str = "中文", note: dict = None) -> str:
        """
        创建异步任务，返回 taskId

        task_type 可选值:
        - "file-processing": 文件处理（PDF转换 + 文本分割 + 领域树）
        - "question-generation": 问题生成
        - "answer-generation": 答案生成
        - "data-cleaning": 数据清洗
        - "dataset-evaluation": 数据集评估
        - "data-distillation": 自动蒸馏
        """
        model_info = self._build_model_info(model_config)
        body = {
            "taskType": task_type,
            "modelInfo": model_info,
            "language": language,
            "totalCount": 0
        }
        if note:
            body["note"] = json.dumps(note) if isinstance(note, dict) else note

        resp = self._post(f"/api/projects/{project_id}/tasks", body)
        # 响应格式: { code: 0, data: { id, ... }, message: "..." }
        task_data = resp.get("data", resp)
        return task_data.get("id")

    def get_task(self, project_id: str, task_id: str) -> dict:
        """获取单个任务状态（自动解包 {code, data} 响应格式）"""
        resp = self._get(f"/api/projects/{project_id}/tasks/{task_id}")
        # EasyDataset API 返回 {code: 0, data: {...}}
        return resp.get("data", resp)

    def list_tasks(self, project_id: str, task_type: str = None,
                   status: int = None, page: int = 0, limit: int = 10) -> dict:
        """获取任务列表"""
        params = {"page": page, "limit": limit}
        if task_type:
            params["taskType"] = task_type
        if status is not None:
            params["status"] = status
        return self._get(f"/api/projects/{project_id}/tasks/list", params)

    def cancel_task(self, project_id: str, task_id: str) -> bool:
        """取消任务"""
        self._patch(f"/api/projects/{project_id}/tasks/{task_id}", {"status": 3})
        return True

    def poll_task(self, project_id: str, task_id: str,
                  timeout_seconds: int = 1800, interval: int = 5,
                  on_progress=None) -> dict:
        """
        轮询任务直到完成/失败/超时

        task.status: 0=处理中, 1=已完成, 2=失败, 3=已中断

        on_progress(task): 进度回调函数

        返回最终任务对象，超时则抛出 TimeoutError
        """
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout_seconds:
                raise TimeoutError(f"Task {task_id} timed out after {timeout_seconds}s")

            task = self.get_task(project_id, task_id)
            status = task.get("status", -1)

            if on_progress:
                completed = task.get("completedCount", 0)
                total = task.get("totalCount", 0)
                on_progress(task_type=task.get("taskType"), completed=completed,
                           total=total, elapsed=int(elapsed))

            if status == 1:  # COMPLETED
                return task
            elif status == 2:  # FAILED
                detail = task.get("detail", "Unknown error")
                raise RuntimeError(f"Task {task_id} failed: {detail}")
            elif status == 3:  # CANCELLED
                raise RuntimeError(f"Task {task_id} was cancelled")

            time.sleep(interval)

    # ==================== 问题与数据集 ====================

    def generate_questions(self, project_id: str, model_config: dict,
                          chunk_ids: list = None, language: str = "中文",
                          enable_ga: bool = False) -> dict:
        """批量生成问题"""
        return self._post(f"/api/projects/{project_id}/generate-questions", {
            "model": self._build_model_info(model_config),
            "chunkIds": chunk_ids or [],
            "language": language,
            "enableGaExpansion": enable_ga
        })

    def generate_dataset(self, project_id: str, question_id: str,
                        model_config: dict, language: str = "中文") -> dict:
        """为单个问题生成数据集（答案）"""
        return self._post(f"/api/projects/{project_id}/datasets", {
            "questionId": question_id,
            "model": self._build_model_info(model_config),
            "language": language
        })

    def get_datasets(self, project_id: str, page: int = 0, page_size: int = 100,
                    confirmed: bool = None) -> dict:
        """获取数据集列表"""
        params = {"page": page, "pageSize": page_size}
        if confirmed is not None:
            params["confirmed"] = str(confirmed).lower()
        return self._get(f"/api/projects/{project_id}/datasets", params)

    def confirm_dataset(self, project_id: str, dataset_id: str, confirmed: bool = True) -> dict:
        """确认数据集（id 通过 query string 传递）"""
        return self._patch(f"/api/projects/{project_id}/datasets?id={dataset_id}", {
            "confirmed": confirmed
        })

    def confirm_all_datasets(self, project_id: str) -> int:
        """确认所有待确认的数据集"""
        count = 0
        page = 0
        while True:
            datasets = self.get_datasets(project_id, page=page, page_size=100, confirmed=False)
            items = datasets.get("datasets", datasets.get("data", []))
            if not items:
                break
            for ds in items:
                ds_id = ds.get("id", ds.get("_id"))
                self.confirm_dataset(project_id, ds_id, True)
                count += 1
            page += 1
        return count

    # ==================== 数据集导出 ====================

    def export_dataset(self, project_id: str, status: str = "confirmed",
                       batch_mode: bool = False, offset: int = 0,
                       batch_size: int = 1000) -> list:
        """
        导出数据集
        status: "confirmed" | "all"
        返回数据集 JSON 数组
        """
        body = {"status": status}
        if batch_mode:
            body["batchMode"] = "true"
            body["offset"] = offset
            body["batchSize"] = batch_size
        resp = self._post(f"/api/projects/{project_id}/datasets/export", body)
        return resp.get("datasets", resp.get("data", []))

    def export_all_datasets_batched(self, project_id: str,
                                     batch_size: int = 1000) -> list:
        """分批导出所有已确认数据集，返回完整列表"""
        all_datasets = []
        offset = 0
        while True:
            batch = self.export_dataset(
                project_id, status="confirmed",
                batch_mode=True, offset=offset, batch_size=batch_size
            )
            if not batch:
                break
            all_datasets.extend(batch)
            offset += batch_size
            if len(batch) < batch_size:
                break
        return all_datasets

    # ==================== HuggingFace 上传（可选） ====================

    def upload_to_huggingface(self, project_id: str, token: str, dataset_name: str,
                              format_type: str = "alpaca", file_format: str = "json",
                              is_private: bool = False, confirmed_only: bool = True,
                              include_cot: bool = True) -> dict:
        """上传到 HuggingFace Hub"""
        return self._post(f"/api/projects/{project_id}/huggingface/upload", {
            "token": token,
            "datasetName": dataset_name,
            "isPrivate": is_private,
            "formatType": format_type,
            "fileFormat": file_format,
            "confirmedOnly": confirmed_only,
            "includeCOT": include_cot
        })

    # ==================== 项目配置 ====================

    def get_project_config(self, project_id: str) -> dict:
        """获取项目提示词配置"""
        return self._get(f"/api/projects/{project_id}/config")

    def update_project_config(self, project_id: str, config: dict) -> dict:
        """更新项目提示词配置"""
        return self._put(f"/api/projects/{project_id}/config", config)

    def get_task_config(self, project_id: str) -> dict:
        """获取任务配置文件"""
        return self._get(f"/api/projects/{project_id}/tasks")

    def update_task_config(self, project_id: str, config: dict) -> dict:
        """更新任务配置"""
        return self._put(f"/api/projects/{project_id}/tasks", config)

    # ==================== 工具方法 ====================

    def check_health(self) -> bool:
        """检查 EasyDataset 服务是否可用"""
        try:
            resp = self.session.get(f"{self.base_url}/", timeout=5)
            return resp.status_code < 500
        except Exception:
            return False

    def wait_for_ready(self, max_wait: int = 60) -> bool:
        """等待 EasyDataset 服务就绪"""
        start = time.time()
        while time.time() - start < max_wait:
            if self.check_health():
                return True
            time.sleep(2)
        return False

    # ==================== 完整管线 ====================

    def run_full_pipeline(self, markdown_path: str, model_config: dict,
                          project_name: str, chunk_settings: dict = None,
                          language: str = "中文", ga_info: dict = None,
                          task_timeout: int = 43200,
                          progress_callback=None) -> List[dict]:
        """
        一键执行完整管线：
        1. 创建项目
        2. 配置模型
        3. 上传文件
        4. 文件处理（异步任务）
        5. 问题生成（异步任务）
        6. 答案生成（异步任务）
        7. 导出数据集

        progress_callback(step, message, data=None): 进度回调
        返回完整数据集 JSON 列表
        """

        def _progress(step, msg, data=None):
            if progress_callback:
                progress_callback(step, msg, data)
            else:
                print(f"[{step}] {msg}")

        # Step 1: 创建项目
        _progress(1, f"创建项目: {project_name}")
        project_id = self.create_project(project_name, "Auto-generated by JY_Knowledge_Skill")
        _progress(1, f"项目已创建: {project_id}")

        # Step 2: 配置模型
        _progress(2, "配置 LLM 模型")
        model_config_id = self.configure_model(project_id, model_config)
        self.set_default_model(project_id, model_config_id)
        _progress(2, f"模型已配置: {model_config_id}")

        try:
            # Step 3: 上传文件
            _progress(3, f"上传文件: {os.path.basename(markdown_path)}")
            file_id = self.upload_file(project_id, markdown_path)
            _progress(3, f"文件已上传: {file_id}")

            # Step 4: 分割文件（.md 使用 split API 直接分割，避免 PDF 处理逻辑报错）
            _progress(4, "分割文件...")
            file_name = os.path.basename(markdown_path)
            file_ext = os.path.splitext(markdown_path)[1].lower()

            if file_ext == '.md':
                # .md 文件直接使用 split API（domain_tree_action="keep" 跳过LLM领域树，避免输出格式不兼容）
                split_resp = self.split_files(
                    project_id,
                    [{"fileName": file_name, "fileId": file_id}],
                    self._build_model_info(model_config),
                    language,
                    domain_tree_action="keep",
                    timeout=180
                )
                _progress(4, f"文件分割完成")
            else:
                # .pdf 使用 file-processing 任务
                task_id = self.create_task(
                    project_id, "file-processing",
                    model_config, language,
                    note={"fileList": [{"fileName": file_name, "fileId": file_id}], "strategy": "default"}
                )
                _progress(4, f"文件处理任务已创建: {task_id}, 等待完成...")
                self.poll_task(project_id, task_id, timeout_seconds=task_timeout,
                              on_progress=lambda **kw: _progress(4, f"文件处理中... {kw.get('completed',0)}/{kw.get('total',0)}"))

            # GA增强：如果LLM判断合适，先生成GA对
            enable_ga = False
            if ga_info:
                _progress("4.5", f"生成 GA 对 ({ga_info.get('genre','')} / {ga_info.get('audience','')})...")
                try:
                    ga_resp = self.generate_ga_pairs(project_id, [file_id], model_config_id, language)
                    if ga_resp.get("success"):
                        enable_ga = True
                        _progress("4.5", f"GA 对生成成功")
                    else:
                        _progress("4.5", f"GA 对生成失败: {ga_resp.get('error','')}, 跳过")
                except Exception as e:
                    _progress("4.5", f"GA 对生成出错: {e}, 跳过")

            # Step 5: 问题生成任务（含重试逻辑，最多3次）
            for step_name, task_type, note in [
                ("问题生成", "question-generation", {"chunkIds": [], "enableGaExpansion": enable_ga}),
                ("答案生成", "answer-generation", None),
            ]:
                step_num = 5 if "问题" in step_name else 6
                max_retries = 3
                for attempt in range(1, max_retries + 1):
                    _progress(step_num, f"创建{step_name}任务 (尝试 {attempt}/{max_retries})...")
                    task_id = self.create_task(
                        project_id, task_type,
                        model_config, language,
                        note=note
                    )
                    _progress(step_num, f"{step_name}任务已创建: {task_id}, 等待完成...")
                    try:
                        self.poll_task(project_id, task_id, timeout_seconds=task_timeout,
                                      on_progress=lambda **kw: _progress(step_num, f"{step_name}中... {kw.get('completed',0)}/{kw.get('total',0)}"))
                        _progress(step_num, f"{step_name}完成")
                        break  # 成功，跳出重试
                    except RuntimeError as e:
                        _progress(step_num, f"{step_name}失败 (尝试 {attempt}/{max_retries}): {e}")
                        if attempt >= max_retries:
                            _progress(step_num, f"{step_name}已达最大重试次数，跳过")
                            break

            # Step 7: 确认所有数据集
            _progress(7, "确认数据集...")
            count = self.confirm_all_datasets(project_id)
            _progress(7, f"已确认 {count} 条数据集")

            # Step 8: 导出
            _progress(8, "导出数据集...")
            datasets = self.export_all_datasets_batched(project_id)
            _progress(8, f"导出完成，共 {len(datasets)} 条数据集")

            return datasets

        except Exception as e:
            _progress(-1, f"管线执行失败: {e}")
            # 清理残留（可选，默认保留方便排查）
            # self.delete_project(project_id)
            raise

    def cleanup_project(self, project_id: str) -> bool:
        """清理项目"""
        try:
            self.delete_project(project_id)
            return True
        except Exception:
            return False
