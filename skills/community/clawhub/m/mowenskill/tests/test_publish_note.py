#!/usr/bin/env python3
"""
publish_note.py 单元测试

通过 mock 替换所有网络调用，测试本地逻辑：
- NoteAtom 构建（各种段落类型）
- 图片上传路由（URL/本地/fileId）
- action_create / action_edit / action_settings 的 payload 构造
- CLI 参数解析
- 标签截断、空内容错误等边界场景
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# 将 scripts 目录添加到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import publish_note as pn


# ── 辅助工具 ────────────────────────────────────────────────────────────────


def mock_api_request(api_key, path, payload):
    """模拟 _api_request，根据 path 返回不同的假数据。"""
    if path == pn.API_NOTE_CREATE:
        return {"noteId": "mock_note_001"}
    elif path == pn.API_NOTE_EDIT:
        return {"noteId": payload.get("noteId", "")}
    elif path == pn.API_NOTE_SET:
        return {}
    elif path == pn.API_UPLOAD_PREPARE:
        return {
            "form": {
                "endpoint": "https://mock-oss.example.com",
                "key": "uploads/test.jpg",
                "policy": "mock_policy",
                "callback": "mock_callback",
                "success_action_status": "200",
                "x:file_id": "mock_file_id_local",
                "x:file_name": payload.get("fileName", "test.jpg"),
                "x:file_uid": "mock_uid",
            }
        }
    elif path == pn.API_UPLOAD_URL:
        return {
            "file": {
                "fileId": "mock_file_id_remote",
                "name": "remote.jpg",
                "path": "https://cdn.mock.com/remote.jpg",
            }
        }
    return {}


# ── 测试类 ──────────────────────────────────────────────────────────────────


class TestBuildTextNode(unittest.TestCase):
    """测试 _build_text_node"""

    def test_plain_text(self):
        node = pn._build_text_node({"text": "hello"})
        self.assertEqual(node, {"type": "text", "text": "hello"})
        self.assertNotIn("marks", node)

    def test_bold(self):
        node = pn._build_text_node({"text": "bold", "bold": True})
        self.assertEqual(node["marks"], [{"type": "bold"}])

    def test_highlight(self):
        node = pn._build_text_node({"text": "hl", "highlight": True})
        self.assertEqual(node["marks"], [{"type": "highlight"}])

    def test_link(self):
        node = pn._build_text_node({"text": "click", "link": "https://example.com"})
        self.assertEqual(len(node["marks"]), 1)
        self.assertEqual(node["marks"][0]["type"], "link")
        self.assertEqual(node["marks"][0]["attrs"]["href"], "https://example.com")

    def test_multiple_marks(self):
        node = pn._build_text_node({
            "text": "all",
            "bold": True,
            "highlight": True,
            "link": "https://x.com",
        })
        mark_types = [m["type"] for m in node["marks"]]
        self.assertIn("bold", mark_types)
        self.assertIn("highlight", mark_types)
        self.assertIn("link", mark_types)

    def test_empty_text(self):
        node = pn._build_text_node({})
        self.assertEqual(node["text"], "")


class TestBuildParagraph(unittest.TestCase):
    """测试 _build_paragraph"""

    def test_string_items(self):
        p = pn._build_paragraph(["hello", "world"])
        self.assertEqual(p["type"], "paragraph")
        self.assertEqual(len(p["content"]), 2)
        self.assertEqual(p["content"][0], {"type": "text", "text": "hello"})
        self.assertEqual(p["content"][1], {"type": "text", "text": "world"})

    def test_dict_items(self):
        p = pn._build_paragraph([{"text": "bold", "bold": True}])
        self.assertEqual(p["content"][0]["marks"], [{"type": "bold"}])

    def test_mixed_items(self):
        p = pn._build_paragraph(["plain", {"text": "bold", "bold": True}])
        self.assertEqual(len(p["content"]), 2)
        self.assertNotIn("marks", p["content"][0])
        self.assertIn("marks", p["content"][1])


class TestBuildNoteAtom(unittest.TestCase):
    """测试 build_note_atom — 各种段落类型"""

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_plain_text_paragraph(self, mock_time, mock_req):
        result = pn.build_note_atom("key", {"paragraphs": ["Hello World"]})
        self.assertEqual(result["type"], "doc")
        self.assertEqual(len(result["content"]), 1)
        para = result["content"][0]
        self.assertEqual(para["type"], "paragraph")
        self.assertEqual(para["content"][0]["text"], "Hello World")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_rich_text_paragraph(self, mock_time, mock_req):
        input_data = {
            "paragraphs": [
                [{"text": "加粗", "bold": True}, "普通"]
            ]
        }
        result = pn.build_note_atom("key", input_data)
        para = result["content"][0]
        self.assertEqual(para["type"], "paragraph")
        self.assertEqual(len(para["content"]), 2)
        self.assertIn("marks", para["content"][0])

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_heading(self, mock_time, mock_req):
        input_data = {
            "paragraphs": [
                {"type": "heading", "level": 2, "text": "标题"}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        h = result["content"][0]
        self.assertEqual(h["type"], "heading")
        self.assertEqual(h["attrs"]["level"], "2")
        self.assertEqual(h["content"][0]["text"], "标题")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_blockquote(self, mock_time, mock_req):
        input_data = {
            "paragraphs": [
                {"type": "blockquote", "text": "引用内容"}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        bq = result["content"][0]
        self.assertEqual(bq["type"], "quote")
        inner_para = bq["content"][0]
        self.assertEqual(inner_para["type"], "paragraph")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_quote_alias(self, mock_time, mock_req):
        """type='quote' 也应生成 quote 节点"""
        input_data = {
            "paragraphs": [
                {"type": "quote", "text": "引用"}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        bq = result["content"][0]
        self.assertEqual(bq["type"], "quote")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_bullet_list(self, mock_time, mock_req):
        input_data = {
            "paragraphs": [
                {"type": "bulletList", "items": ["A", "B", "C"]}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        bl = result["content"][0]
        self.assertEqual(bl["type"], "bulletList")
        self.assertEqual(len(bl["content"]), 3)
        self.assertEqual(bl["content"][0]["type"], "listItem")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_ordered_list(self, mock_time, mock_req):
        input_data = {
            "paragraphs": [
                {"type": "orderedList", "items": ["1st", "2nd"]}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        ol = result["content"][0]
        self.assertEqual(ol["type"], "orderedList")
        self.assertEqual(len(ol["content"]), 2)

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_image_url(self, mock_time, mock_req):
        """URL 图片应调用远程上传"""
        input_data = {
            "paragraphs": [
                {"type": "image", "src": "https://example.com/photo.jpg"}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        img = result["content"][0]
        self.assertEqual(img["type"], "image")
        self.assertEqual(img["attrs"]["uuid"], "mock_file_id_remote")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_image_with_dimensions(self, mock_time, mock_req):
        """图片带尺寸信息"""
        input_data = {
            "paragraphs": [
                {"type": "image", "src": "https://example.com/photo.jpg",
                 "width": 1920, "height": 1080}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        img = result["content"][0]
        self.assertEqual(img["attrs"]["width"], "1920")
        self.assertEqual(img["attrs"]["height"], "1080")
        self.assertEqual(img["attrs"]["ratio"], "1.78")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_image_fileid_passthrough(self, mock_time, mock_req):
        """已有的 fileId 应直接透传"""
        input_data = {
            "paragraphs": [
                {"type": "image", "src": "existing_file_id_123"}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        img = result["content"][0]
        self.assertEqual(img["type"], "image")
        self.assertEqual(img["attrs"]["uuid"], "existing_file_id_123")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_raw_node(self, mock_time, mock_req):
        """raw 类型应直接透传节点"""
        custom_node = {"type": "customWidget", "attrs": {"id": "w1"}}
        input_data = {
            "paragraphs": [
                {"type": "raw", "node": custom_node}
            ]
        }
        result = pn.build_note_atom("key", input_data)
        self.assertEqual(result["content"][0], custom_node)

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_empty_paragraphs_exits(self, mock_time, mock_req):
        """空内容应触发 sys.exit"""
        with self.assertRaises(SystemExit):
            pn.build_note_atom("key", {"paragraphs": []})

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_complex_note(self, mock_time, mock_req):
        """组合多种类型的复杂笔记"""
        input_data = {
            "paragraphs": [
                {"type": "heading", "level": 1, "text": "我的日记"},
                "今天天气很好",
                [{"text": "重要", "bold": True}, "的事情"],
                {"type": "image", "src": "https://example.com/img.jpg"},
                {"type": "blockquote", "text": "名言警句"},
                {"type": "bulletList", "items": ["A", "B"]},
            ]
        }
        result = pn.build_note_atom("key", input_data)
        self.assertEqual(len(result["content"]), 6)
        types = [n["type"] for n in result["content"]]
        self.assertEqual(types, [
            "heading", "paragraph", "paragraph",
            "image", "quote", "bulletList",
        ])


class TestUploadImageRouting(unittest.TestCase):
    """测试 upload_image 路由逻辑"""

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_url_routes_to_remote(self, mock_req):
        fid = pn.upload_image("key", "https://example.com/photo.jpg")
        self.assertEqual(fid, "mock_file_id_remote")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_http_url_routes_to_remote(self, mock_req):
        fid = pn.upload_image("key", "http://example.com/photo.jpg")
        self.assertEqual(fid, "mock_file_id_remote")

    def test_fileid_passthrough(self):
        """不含路径分隔符且不以 http 开头的字符串视为 fileId"""
        fid = pn.upload_image("key", "abc123_file_id")
        self.assertEqual(fid, "abc123_file_id")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "_multipart_upload", return_value=b"ok")
    @patch("time.sleep")
    def test_local_path_routes_to_local(self, mock_sleep, mock_upload, mock_req):
        """真实本地文件路径走本地上传"""
        # 创建一个临时图片文件
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\xff\xd8\xff\xe0" + b"\x00" * 100)  # 最小 JPEG 头
            tmp_path = f.name
        try:
            fid = pn.upload_image("key", tmp_path)
            self.assertEqual(fid, "mock_file_id_local")
        finally:
            os.unlink(tmp_path)


class TestActionCreate(unittest.TestCase):
    """测试 action_create"""

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_basic_create(self, mock_time, mock_req):
        input_data = {
            "paragraphs": ["Hello"],
            "tags": ["test"],
            "autoPublish": True,
        }
        result = pn.action_create("key", input_data)
        self.assertEqual(result["noteId"], "mock_note_001")
        self.assertEqual(result["action"], "create")

        # 验证最后一次 _api_request 的调用参数（创建调用）
        last_call = mock_req.call_args_list[-1]
        path = last_call[0][1]
        payload = last_call[0][2]
        self.assertEqual(path, pn.API_NOTE_CREATE)
        self.assertIn("body", payload)
        self.assertIn("settings", payload)
        self.assertEqual(payload["settings"]["tags"], ["test"])
        self.assertTrue(payload["settings"]["autoPublish"])

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_create_no_settings(self, mock_time, mock_req):
        """不传 tags/autoPublish，settings 应不存在"""
        input_data = {"paragraphs": ["Simple note"]}
        result = pn.action_create("key", input_data)
        self.assertEqual(result["action"], "create")

        # payload 中不应有 settings
        create_call = [c for c in mock_req.call_args_list if c[0][1] == pn.API_NOTE_CREATE]
        payload = create_call[0][0][2]
        self.assertNotIn("settings", payload)

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_tags_truncation(self, mock_time, mock_req):
        """超过 10 个标签应被截断"""
        input_data = {
            "paragraphs": ["text"],
            "tags": [f"tag{i}" for i in range(15)],
        }
        result = pn.action_create("key", input_data)
        # 验证 payload 中 tags 被截断
        create_call = [c for c in mock_req.call_args_list if c[0][1] == pn.API_NOTE_CREATE]
        payload = create_call[0][0][2]
        self.assertEqual(len(payload["settings"]["tags"]), 10)

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_long_tag_truncation(self, mock_time, mock_req):
        """超过 30 字符的标签应被截断"""
        long_tag = "a" * 50
        input_data = {
            "paragraphs": ["text"],
            "tags": [long_tag],
        }
        pn.action_create("key", input_data)
        create_call = [c for c in mock_req.call_args_list if c[0][1] == pn.API_NOTE_CREATE]
        payload = create_call[0][0][2]
        self.assertEqual(len(payload["settings"]["tags"][0]), 30)


class TestActionEdit(unittest.TestCase):
    """测试 action_edit"""

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_basic_edit(self, mock_time, mock_req):
        input_data = {"paragraphs": ["Updated content"]}
        result = pn.action_edit("key", "note_123", input_data)
        self.assertEqual(result["noteId"], "note_123")
        self.assertEqual(result["action"], "edit")

        edit_call = [c for c in mock_req.call_args_list if c[0][1] == pn.API_NOTE_EDIT]
        payload = edit_call[0][0][2]
        self.assertEqual(payload["noteId"], "note_123")
        self.assertIn("body", payload)
        self.assertEqual(payload["body"]["type"], "doc")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_edit_without_note_id_exits(self, mock_time, mock_req):
        """编辑操作无 noteId 应退出"""
        with self.assertRaises(SystemExit):
            pn.action_edit("key", "", {"paragraphs": ["text"]})


class TestActionSettings(unittest.TestCase):
    """测试 action_settings — 使用 section + privacy 格式"""

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_privacy_public(self, mock_req):
        result = pn.action_settings("key", "note_123", {"privacyType": "public"})
        self.assertEqual(result["noteId"], "note_123")
        self.assertEqual(result["action"], "settings")

        payload = mock_req.call_args[0][2]
        self.assertEqual(payload["noteId"], "note_123")
        self.assertEqual(payload["section"], 1)
        self.assertEqual(payload["settings"]["privacy"]["type"], "public")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_privacy_private(self, mock_req):
        pn.action_settings("key", "note_123", {"privacyType": "private"})
        payload = mock_req.call_args[0][2]
        self.assertEqual(payload["settings"]["privacy"]["type"], "private")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_rule_with_no_share(self, mock_req):
        pn.action_settings("key", "note_123", {
            "privacyType": "rule",
            "noShare": True,
        })
        payload = mock_req.call_args[0][2]
        self.assertEqual(payload["settings"]["privacy"]["type"], "rule")
        self.assertTrue(payload["settings"]["privacy"]["rule"]["noShare"])

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_rule_with_expire(self, mock_req):
        pn.action_settings("key", "note_123", {
            "privacyType": "rule",
            "expireAt": 1700000000,
        })
        payload = mock_req.call_args[0][2]
        self.assertEqual(payload["settings"]["privacy"]["type"], "rule")
        self.assertEqual(payload["settings"]["privacy"]["rule"]["expireAt"], "1700000000")

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_rule_with_all_options(self, mock_req):
        pn.action_settings("key", "note_123", {
            "privacyType": "rule",
            "noShare": True,
            "expireAt": 1800000000,
        })
        payload = mock_req.call_args[0][2]
        privacy = payload["settings"]["privacy"]
        self.assertEqual(privacy["type"], "rule")
        self.assertTrue(privacy["rule"]["noShare"])
        self.assertEqual(privacy["rule"]["expireAt"], "1800000000")

    def test_no_privacy_exits(self):
        """无 privacy 参数应退出"""
        with self.assertRaises(SystemExit):
            pn.action_settings("key", "note_123", {})

    def test_no_note_id_exits(self):
        """无 noteId 应退出"""
        with self.assertRaises(SystemExit):
            pn.action_settings("key", "", {"privacyType": "public"})

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    def test_api_path_is_note_set(self, mock_req):
        """应调用 /api/open/api/v1/note/set 端点"""
        pn.action_settings("key", "note_123", {"privacyType": "public"})
        path = mock_req.call_args[0][1]
        self.assertEqual(path, pn.API_NOTE_SET)


class TestCLIParsing(unittest.TestCase):
    """测试 CLI 参数解析"""

    def test_create_action(self):
        with patch("sys.argv", ["prog", "--action", "create", "--api-key", "test_key", "--input", "note.json"]):
            args = pn.parse_args()
            self.assertEqual(args.action, "create")
            self.assertEqual(args.api_key, "test_key")
            self.assertEqual(args.input, "note.json")

    def test_edit_action(self):
        with patch("sys.argv", ["prog", "--action", "edit", "--api-key", "k", "--note-id", "n1", "--input", "e.json"]):
            args = pn.parse_args()
            self.assertEqual(args.action, "edit")
            self.assertEqual(args.note_id, "n1")

    def test_settings_action(self):
        with patch("sys.argv", ["prog", "--action", "settings", "--api-key", "k",
                                 "--note-id", "n1", "--privacy", "public"]):
            args = pn.parse_args()
            self.assertEqual(args.action, "settings")
            self.assertEqual(args.privacy, "public")

    def test_settings_rule_no_share(self):
        with patch("sys.argv", ["prog", "--action", "settings", "--api-key", "k",
                                 "--note-id", "n1", "--privacy", "rule", "--no-share"]):
            args = pn.parse_args()
            self.assertEqual(args.privacy, "rule")
            self.assertTrue(args.no_share)

    def test_settings_expire_at(self):
        with patch("sys.argv", ["prog", "--action", "settings", "--api-key", "k",
                                 "--note-id", "n1", "--privacy", "rule", "--expire-at", "1700000000"]):
            args = pn.parse_args()
            self.assertEqual(args.expire_at, 1700000000)

    def test_invalid_action_exits(self):
        with patch("sys.argv", ["prog", "--action", "invalid"]):
            with self.assertRaises(SystemExit):
                pn.parse_args()

    def test_invalid_privacy_exits(self):
        with patch("sys.argv", ["prog", "--action", "settings", "--privacy", "unknown"]):
            with self.assertRaises(SystemExit):
                pn.parse_args()

    def test_api_key_from_env(self):
        with patch.dict(os.environ, {"MOWEN_API_KEY": "env_key"}):
            with patch("sys.argv", ["prog", "--action", "create", "--input", "n.json"]):
                args = pn.parse_args()
                self.assertEqual(args.api_key, "env_key")


class TestEndToEndCreate(unittest.TestCase):
    """端到端测试：从 JSON 文件到 action_create"""

    @patch.object(pn, "_api_request", side_effect=mock_api_request)
    @patch.object(pn, "time")
    def test_create_from_json_file(self, mock_time, mock_req):
        input_data = {
            "paragraphs": [
                {"type": "heading", "level": 1, "text": "测试标题"},
                "这是一段测试文字",
                {"type": "image", "src": "https://example.com/test.jpg", "width": 800, "height": 600},
                {"type": "blockquote", "text": "引用"},
                {"type": "bulletList", "items": ["项1", "项2"]},
            ],
            "tags": ["测试", "单元测试"],
            "autoPublish": True,
        }

        # 写入临时文件
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(input_data, f, ensure_ascii=False)
            tmp_path = f.name

        try:
            # 读取并执行
            with open(tmp_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)

            result = pn.action_create("test_key", loaded)
            self.assertEqual(result["noteId"], "mock_note_001")
            self.assertEqual(result["action"], "create")

            # 验证 API 被调用了（至少有远程图片上传 + 创建）
            paths_called = [c[0][1] for c in mock_req.call_args_list]
            self.assertIn(pn.API_UPLOAD_URL, paths_called)
            self.assertIn(pn.API_NOTE_CREATE, paths_called)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
