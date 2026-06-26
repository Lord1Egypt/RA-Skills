import unittest

from skill.scripts.call_service_example import (
    IN_PROGRESS_STATUSES,
    format_failure,
    infer_platform,
    render_structured_output,
)


class CallServiceExampleTests(unittest.TestCase):
    def test_infer_platform_from_known_hosts(self):
        self.assertEqual(infer_platform("https://v.douyin.com/abc123/"), "douyin")
        self.assertEqual(infer_platform("http://xhslink.com/o/abc123"), "xiaohongshu")

    def test_in_progress_statuses_match_service_workflow(self):
        self.assertEqual({"queued", "running"}, IN_PROGRESS_STATUSES)

    def test_cookie_failure_is_reframed_as_server_side_issue(self):
        payload = {"msg": "success", "data": {"error_message": "小红书 Cookie 缺失，请先配置有效 Cookie"}}
        self.assertIn("服务端配置问题", format_failure(payload))

    def test_render_structured_output_appends_comment_candidates(self):
        rendered = render_structured_output(
            {
                "summary_markdown": "## 一句话总结\n- 这是总结",
                "card": {
                    "actions": ["动作1", "动作2"],
                    "suggested_remind_at": "2026-04-22T13:00:00+08:00",
                },
                "comment_candidates": ["评论1", "评论2", "评论3"],
            }
        )

        self.assertIn("【总结】", rendered)
        self.assertIn("【Todo List】", rendered)
        self.assertIn("【推荐提醒时间】", rendered)
        self.assertIn("【评论参考】", rendered)
        self.assertIn("评论1", rendered)
        self.assertIn("评论2", rendered)
        self.assertIn("评论3", rendered)


if __name__ == "__main__":
    unittest.main()
