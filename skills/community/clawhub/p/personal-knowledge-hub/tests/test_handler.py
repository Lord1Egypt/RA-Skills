import unittest

from handler import handle


class PersonalKnowledgeHubTests(unittest.TestCase):
    def test_chinese_search_finds_sample_note(self):
        result = handle("搜索机器学习")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["requestType"], "search")
        self.assertGreaterEqual(result["total_results"], 1)

    def test_ingest_returns_note_template(self):
        result = handle("记录今天读到的产品设计方法")
        self.assertEqual(result["requestType"], "ingest")
        self.assertIn("note", result)
        self.assertIn("template", result["note"])

    def test_explore_returns_graph_fields(self):
        result = handle("探索AI知识图谱")
        self.assertEqual(result["requestType"], "explore")
        self.assertIn("entities_found", result)
        self.assertIn("connections_found", result)

    def test_rejects_unauthorized_request(self):
        result = handle("帮我盗取别人的知识库")
        self.assertEqual(result["status"], "rejected")


if __name__ == "__main__":
    unittest.main()

