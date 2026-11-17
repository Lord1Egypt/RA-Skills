import json
import urllib.request
import urllib.parse

class TeambitionCollector:
    def __init__(self, config):
        self.tb_cfg = config.get('rules', {}).get('teambition', {})
        self.user_token = self.tb_cfg.get('user_token')
        self.org_id = self.tb_cfg.get('org_id')
        self.role_types = self.tb_cfg.get('role_types', 'executor')

    def fetch_my_tasks(self):
        """获取我是执行人、且未完成的所有 TB 任务"""
        if not self.tb_cfg.get('enabled', False) or not self.user_token:
            return []

        # tql: isDone = false
        params = urllib.parse.urlencode({
            'roleTypes': self.role_types,
            'tql': 'isDone = false',
            'pageSize': 50
        })
        url = f'https://open.teambition.com/api/v3/usertasks/search?{params}'
        req = urllib.request.Request(url, headers={
            'Authorization': f'Bearer {self.user_token}',
            'x-tenant-id': self.org_id,
            'User-Agent': 'PersonalWorkAssistant/1.0'
        })
        
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get('result', [])
        except Exception as e:
            print(f"[TeambitionCollector] Error fetching tasks: {e}")
            return []
