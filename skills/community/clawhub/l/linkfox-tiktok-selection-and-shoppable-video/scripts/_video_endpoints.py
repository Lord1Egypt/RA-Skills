"""Endpoint registry for linkfox-tiktok-video.

New TikTok Video API definitions are appended here as upstream docs arrive.
Each entry:

VIDEO_ENDPOINTS["api_name"] = {
    "summary": "...",
    "method": "GET" | "POST" | "PUT" | "DELETE",
    "path": "video/...",           # relative path (no tiktok-proxy prefix)
    "required": ["openId", ...],   # openId always required unless ttsAccessToken passed
    "query_fields": [...],         # GET → queryString
    "body_fields": [...],          # POST/PUT → JSON body keys (unless body/requestBody given)
    "defaults": {...},             # optional param defaults applied before required check
    "path_params": [...],          # path template placeholders, e.g. {video_id}
    "response_key": "data",        # key on merged output for parsed upstream JSON
}

Official TikTok docs URL may be stored in "doc_url".
"""

from __future__ import annotations

from typing import Any, Dict, List

VIDEO_ENDPOINTS: Dict[str, Dict[str, Any]] = {
    "get_creator_profile": {
        "summary": "Get Creator Profile — 获取达人主页/档案",
        "method": "GET",
        "path": "affiliate_creator/202508/profiles",
        "required": [],
        "query_fields": [],
        "body_fields": [],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-creator-profile-202508",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
    },
    "upload_shoppable_video_file": {
        "summary": "Upload Shoppable Video File — 上传可购物视频文件（multipart）",
        "method": "POST",
        "path": "affiliate_creator/202505/videos/video_files",
        "required": [],
        "query_fields": [],
        "body_fields": [],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/upload-shoppable-video-file-202505",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
        "multipart": True,
        "proxy_supported": False,
        "proxy_unsupported_reason": (
            "multipart/form-data binary upload; /tiktokVideo/developerProxy body is string-only. "
            "See references/api.md §4. For >10MB use large-file-upload.md."
        ),
    },
    "large_file_upload_init": {
        "summary": "Large File Upload — Step 1 Initialize Upload",
        "method": "POST",
        "path": "open/202505/file/init",
        "required": [],
        "query_fields": [],
        "body_fields": ["file_size", "chunk_size", "file_name", "content_type"],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/shoppable-video-large-file-upload",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d",
        "proxy_supported": False,
        "proxy_unsupported_reason": (
            "Path prefix 'open/' is not in tiktok-video developer-proxy whitelist yet. "
            "See references/large-file-upload.md."
        ),
    },
    "large_file_upload_bind": {
        "summary": "Large File Upload — Step 3 Bind Business Resource",
        "method": "POST",
        "path": "open/202505/file/bind",
        "required": [],
        "query_fields": [],
        "body_fields": ["upload_token"],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/shoppable-video-large-file-upload",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d",
        "proxy_supported": False,
        "proxy_unsupported_reason": (
            "Path prefix 'open/' is not in tiktok-video developer-proxy whitelist yet. "
            "Confirm exact bind path in Lark doc Step 3. See references/large-file-upload.md."
        ),
    },
    "post_shoppable_video": {
        "summary": "Post Shoppable Video — 发布可购物视频",
        "method": "POST",
        "path": "affiliate_creator/202603/videos",
        "required": ["video_info", "product_link_info"],
        "query_fields": [],
        "body_fields": ["video_info", "product_link_info"],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/post-shoppable-video-202603",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
    },
    "get_shoppable_video_status": {
        "summary": "Get Shoppable Video Status — 查询可购物视频发布状态",
        "method": "GET",
        "path": "affiliate_creator/202509/videos/{video_id}/status",
        "path_params": ["video_id"],
        "required": ["video_id"],
        "query_fields": [],
        "body_fields": [],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-shoppable-video-status-202509",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
    },
    "precheck_shoppable_video": {
        "summary": "Pre-check Shoppable Video — 可购物视频内容预检",
        "method": "POST",
        "path": "affiliate_creator/202511/videos/precheck_task",
        "required": ["video_info", "product_link_info"],
        "query_fields": [],
        "body_fields": ["video_info", "product_link_info"],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/precheck-shoppable-video-202511",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
    },
    "get_shoppable_video_precheck_result": {
        "summary": "Get Shoppable Video Pre-check Result — 查询视频预检结果",
        "method": "GET",
        "path": "affiliate_creator/202511/videos/precheck_tasks/{task_id}",
        "path_params": ["task_id"],
        "required": ["task_id"],
        "query_fields": [],
        "body_fields": [],
        "response_key": "data",
        "doc_url": "https://partner.tiktokshop.com/docv2/page/get-shoppable-video-precheck-result-202511",
        "mrd_url": "https://bytedance.sg.larkoffice.com/docx/Os8tdPkaVo2QFBxhSRIlQwBAg9f",
    },
}

LIST_QUERY_FIELDS: List[str] = []

RESERVED_PARAM_KEYS = frozenset({
    "api",
    "openId",
    "ttsAccessToken",
    "region",
    "contentType",
    "body",
    "requestBody",
    "skipDepCheck",
})


def list_api_names() -> List[str]:
    return sorted(VIDEO_ENDPOINTS.keys())
