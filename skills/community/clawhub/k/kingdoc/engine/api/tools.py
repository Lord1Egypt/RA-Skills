"""KingDoc MCP Server — implements MCP tools with real HTTP calls"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from engine.auth import KingDocAuth
from engine.client import KingDocClient
from engine.exceptions import KingDocError
from engine.security import validate_file_id, is_blocked_extension, is_blocked_mime


class KingDocMcpServer:
    """Implement all MCP tools with actual HTTP calls to Kingsoft API"""
    
    def __init__(self, config_path: str):
        self.client = KingDocClient(config_path)
    
    def kdoc_file_create(self, name: str, doc_type: str, folder_id: str = None, content: str = None) -> Dict:
        """创建新文档"""
        body = {"name": name, "type": doc_type}
        if folder_id:
            body["folder_id"] = folder_id
        if content:
            body["content"] = content
        
        resp = self.client.post("/personal/files", json=body)
        if resp.get("code") != 0:
            raise KingDocError("KD011", resp.get("message", "创建失败"))
        return resp
    
    def kdoc_file_content(self, file_id: str) -> Dict:
        """获取文档内容"""
        if not validate_file_id(file_id):
            raise KingDocError("KD011", "非法 file_id 格式")
        resp = self.client.get(f"/personal/files/{file_id}/content")
        if resp.get("code") != 0:
            raise KingDocError("KD005", resp.get("message", "获取内容失败"))
        return resp
    
    def kdoc_file_upload_content(self, file_id: str, content: bytes, version: int = None) -> Dict:
        """上传覆盖文档内容"""
        if not validate_file_id(file_id):
            raise KingDocError("KD011", "非法 file_id 格式")
        
        body = {"content": content.decode("utf-8", errors="ignore")}
        if version:
            body["version"] = version
        
        resp = self.client.put(f"/personal/files/{file_id}/content", json=body)
        if resp.get("code") != 0:
            raise KingDocError(resp.get("code", "KD010"), resp.get("message", "上传失败"))
        return resp
    
    def kdoc_file_move(self, file_id: str, folder_id: str) -> Dict:
        """移动文件"""
        if not validate_file_id(file_id):
            raise KingDocError("KD011", "非法 file_id 格式")
        resp = self.client.put(f"/personal/files/{file_id}/location", json={"folder_id": folder_id})
        return resp
    
    def kdoc_file_rename(self, file_id: str, name: str) -> Dict:
        """重命名"""
        if not validate_file_id(file_id):
            raise KingDocError("KD011", "非法 file_id 格式")
        resp = self.client.put(f"/personal/files/{file_id}/name", json={"name": name})
        return resp
    
    def kdoc_file_delete(self, file_id: str) -> Dict:
        """软删除"""
        if not validate_file_id(file_id):
            raise KingDocError("KD011", "非法 file_id 格式")
        resp = self.client.delete(f"/personal/files/{file_id}")
        return resp
    
    def kdoc_file_search(self, keyword: str, limit: int = 10) -> Dict:
        """搜索文档"""
        resp = self.client.get("/personal/search", params={"keyword": keyword, "limit": limit})
        return resp
    
    def kdoc_file_info(self, file_id: str) -> Dict:
        """获取元信息"""
        if not validate_file_id(file_id):
            raise KingDocError("KD011", "非法 file_id 格式")
        resp = self.client.get(f"/personal/files/{file_id}")
        return resp
    
    def kdoc_folder_create(self, name: str, parent_id: str = None) -> Dict:
        """创建文件夹"""
        body = {"name": name}
        if parent_id:
            body["parent_id"] = parent_id
        resp = self.client.post("/personal/folders", json=body)
        return resp
    
    def kdoc_folder_list(self, folder_id: str = None) -> Dict:
        """查询子目录"""
        params = {}
        if folder_id:
            params["folder_id"] = folder_id
        resp = self.client.get("/personal/folders/children", params=params)
        return resp
    
    def kdoc_trash_list(self, limit: int = 20, offset: int = 0) -> Dict:
        """回收站列表"""
        resp = self.client.get("/personal/trash/list", params={"limit": limit, "offset": offset})
        return resp
    
    def kdoc_trash_recover(self, file_id: str) -> Dict:
        """恢复文件"""
        resp = self.client.post("/personal/trash/recover", json={"file_id": file_id})
        return resp
    
    def kdoc_trash_destroy(self, file_id: str) -> Dict:
        """彻底删除"""
        resp = self.client.post("/personal/trash/destroy", json={"file_id": file_id})
        return resp
    
    def kdoc_version_list(self, file_id: str) -> Dict:
        """版本历史"""
        resp = self.client.get(f"/appspace/versions?file_id={file_id}")
        return resp
    
    def kdoc_version_restore(self, file_id: str, version: int) -> Dict:
        """回滚版本"""
        resp = self.client.post(f"/appspace/versions/{version}/restore", json={"file_id": file_id})
        return resp
    
    def kdoc_file_permission(self, file_id: str, members: list) -> Dict:
        """变更权限"""
        resp = self.client.put(f"/personal/files/{file_id}/permissions", json={"members": members})
        return resp
    
    def kdoc_batch_create(self, operation: str, file_ids: list, target_folder_id: str = None) -> Dict:
        """创建批量任务"""
        body = {"operation": operation, "file_ids": file_ids}
        if target_folder_id:
            body["target_folder_id"] = target_folder_id
        resp = self.client.post("/personal/tasks", json=body)
        return resp
    
    def kdoc_batch_query(self, task_id: str) -> Dict:
        """查询批量任务"""
        resp = self.client.get(f"/personal/tasks/{task_id}")
        return resp
    
    def kdoc_et_create(self, name: str) -> Dict:
        """创建工作表"""
        resp = self.client.post("/et/sheets", json={"name": name})
        return resp
    
    def kdoc_et_range_write(self, sheet_id: str, range_str: str, values: list) -> Dict:
        """批量写入区域"""
        resp = self.client.put(f"/et/ranges/{sheet_id}", json={"range": range_str, "values": values})
        return resp
    
    def kdoc_et_formula_set(self, sheet_id: str, cell: str, formula: str) -> Dict:
        """设置公式"""
        resp = self.client.post("/et/formula/set", json={"sheet_id": sheet_id, "cell": cell, "formula": formula})
        return resp
    
    def kdoc_dbt_create(self, name: str) -> Dict:
        """创建多维表格"""
        resp = self.client.post("/dbt/tables", json={"name": name})
        return resp
    
    def kdoc_dbt_field_add(self, table_id: str, name: str, field_type: str, options: list = None) -> Dict:
        """添加字段"""
        body = {"table_id": table_id, "name": name, "type": field_type}
        if options:
            body["options"] = options
        resp = self.client.post("/dbt/fields", json=body)
        return resp
    
    def kdoc_dbt_record_add_batch(self, table_id: str, records: list) -> Dict:
        """批量添加记录"""
        resp = self.client.post("/dbt/records/batch", json={"table_id": table_id, "records": records})
        return resp
    
    def kdoc_dbt_record_query(self, table_id: str, filter_obj: Dict = None, limit: int = 100) -> Dict:
        """查询记录"""
        params = {"limit": limit}
        if filter_obj:
            params["filter"] = json.dumps(filter_obj)
        resp = self.client.get(f"/dbt/records/{table_id}", params=params)
        return resp
    
    def kdoc_dbt_webhook_set(self, table_id: str, callback_url: str, events: list) -> Dict:
        """设置 Webhook"""
        resp = self.client.post("/dbt/webhooks", json={
            "table_id": table_id, "callback_url": callback_url, "events": events
        })
        return resp
    
    def kdoc_office_convert(self, file_id: str, target_format: str) -> Dict:
        """格式转换"""
        resp = self.client.post("/office/convert", json={"file_id": file_id, "target_format": target_format})
        return resp
    
    def kdoc_office_extract(self, file_id: str) -> Dict:
        """纯文本提取"""
        resp = self.client.post("/office/extract", json={"file_id": file_id})
        return resp
    
    def kdoc_form_create(self, name: str, description: str = None) -> Dict:
        """创建收集表"""
        body = {"name": name}
        if description:
            body["description"] = description
        resp = self.client.post("/personal/forms", json=body)
        return resp
    
    def kdoc_form_answers(self, form_id: str, limit: int = 50) -> Dict:
        """查询答卷"""
        resp = self.client.get(f"/personal/forms/{form_id}/answers", params={"limit": limit})
        return resp
    
    def kdoc_notification_send(self, channel: str, webhook_key: str, content: Dict) -> Dict:
        """发送通知"""
        resp = self.client.post("/notification/send", json={
            "channel": channel, "webhook_key": webhook_key, "content": content
        })
        return resp
    
    def kdoc_user_info(self) -> Dict:
        """用户信息"""
        resp = self.client.get("/user")
        return resp
    
    def kdoc_space_quota(self) -> Dict:
        """空间用量"""
        resp = self.client.get("/personal/spaces/quota")
        return resp
    
    def kdoc_report_unsupported(self, feature: str, description: str = None) -> Dict:
        """上报不支持的功能"""
        body = {"feature": feature}
        if description:
            body["description"] = description
        resp = self.client.post("/skill/report", json=body)
        return resp
    
    def kdoc_skill_update_check(self, version: str) -> Dict:
        """更新检查"""
        resp = self.client.post("/skill/update_check", json={"version": version})
        return resp
