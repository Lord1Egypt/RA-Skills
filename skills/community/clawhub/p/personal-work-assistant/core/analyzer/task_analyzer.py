import os
import json
import urllib.request
import datetime

class TaskAnalyzer:
    def __init__(self, config):
        self.config = config
        self.user_name = config.get('user', {}).get('name', 'Azusa')
        self.aliases = config.get('user', {}).get('aliases', [])

    def _call_llm(self, prompt, system_prompt="你是一位专业、敏锐的个人工作助理。"):
        """调用本地/网关统一 LLM 接口"""
        import requests
        api_url = "https://ss-newapi.xmp.one/v1/chat/completions"
        api_key = "REDACTED-SECRET"

        headers = {
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "deepseek-v4-flash",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        try:
            resp = requests.post(api_url, headers=headers, json=payload, timeout=45)
            if resp.status_code == 200:
                res_data = resp.json()
                content = res_data['choices'][0]['message']['content']
                return json.loads(content)
            else:
                print(f"[TaskAnalyzer] LLM Error Status {resp.status_code}: {resp.text}")
                return {}
        except Exception as e:
            print(f"[TaskAnalyzer] LLM Call Error: {e}")
            return {}

    def analyze_dingtalk_events(self, messages, at_mes, dms):
        """
        输入近 24 小时的钉钉对话，让 AI 智能提取：
        1. 需要用户处理/跟进的任务 (action_items)
        2. @所有人 中的待办与需知悉公告 (announcements / at_all_tasks)
        3. 对已有事项的进展更新或已解决确认 (progress_updates)
        """
        if not messages and not at_mes and not dms:
            return {"action_items": [], "announcements": [], "progress_updates": []}

        prompt = f"""
你正在为用户【{self.user_name}】（别名：{', '.join(self.aliases)}）梳理其近 24 小时的钉钉工作消息。
用户角色为产品经理，负责 HelpKnow / SaleSmartly 的 AI 模块。

以下是收集到的三类消息源：
1. 【重点监控群消息】：{json.dumps(messages, ensure_ascii=False)}
2. 【其他群 @我 的消息】：{json.dumps(at_mes, ensure_ascii=False)}
3. 【个人私聊消息】：{json.dumps(dms, ensure_ascii=False)}

请严格以【{self.user_name}】为主视角进行分析提取，输出严格的 JSON 格式，结构如下：
{{
  "action_items": [
    {{
      "id": "生成的稳定唯一ID或msgId",
      "source_name": "群名或私聊人名",
      "title": "任务或问题一句话简述",
      "detail": "核心诉求/涉及项目ID/具体问题",
      "priority": "urgent|high|normal",
      "due_date": "YYYY-MM-DD 或 null",
      "reason": "为什么需要该用户跟进（如：用户在群里被要求确认、私聊派活、@所有人要求在某日前完成）"
    }}
  ],
  "announcements": [
    {{
      "id": "msgId",
      "source_name": "群名",
      "content": "需知悉的公告/放假/规范/全员通知（无需用户执行具体任务，仅供知悉）"
    }}
  ],
  "progress_updates": [
    {{
      "related_topic_or_id": "关联的Bug、项目ID或需求名称",
      "status": "in_progress|done",
      "resolution_note": "群内讨论给出的进展或闭环说明（如：开发已回退模型、已上线灰度、开发已确认解决）"
    }}
  ]
}}

过滤原则：
- 排除纯闲聊、无意义的表情包、已明显闭环且不需要该用户介入的技术细节。
- 如果是 @所有人 且带有具体行动与截止时间（如提交OKR、报名），放入 action_items；如果是纯通知，放入 announcements。
- 只要涉及用户负责的业务模块（HelpKnow/AI员工/模型/知识库/语言识别等）且需要产品拍板或跟进的，务必纳入 action_items。
"""
        return self._call_llm(prompt)
