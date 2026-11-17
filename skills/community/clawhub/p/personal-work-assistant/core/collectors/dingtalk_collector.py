import subprocess
import json
import datetime

class DingTalkCollector:
    def __init__(self, config):
        self.config = config
        self.user_cfg = config.get('user', {})
        self.rules = config.get('rules', {})
        self.focused_groups = self.rules.get('focused_groups', [])
        self.ignored_keywords = self.rules.get('ignored_group_keywords', [])
        self.direct_messages_cfg = self.rules.get('direct_messages', {})

    def _run_dws_cmd(self, cmd_args):
        p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        try:
            return json.loads(out.decode('utf-8', errors='ignore'))
        except Exception:
            return {}

    def fetch_focused_groups_messages(self, start_time_str):
        """全量拉取重点群（HK小队、HelpKnow小分队、HK问题反馈等）的近24小时消息"""
        all_msgs = []
        for g in self.focused_groups:
            gid = g.get('id')
            gname = g.get('name')
            profile = g.get('profile')
            
            cmd = ['dws', 'chat', '+messages-list', '--group', gid, '--time', start_time_str, '--limit', '100', '-y']
            if profile:
                cmd.extend(['--profile', profile])
                
            res = self._run_dws_cmd(cmd)
            msgs = res.get('messages', [])
            for m in msgs:
                m['group_name'] = gname
                m['group_id'] = gid
                m['source_type'] = 'dingtalk_group'
            all_msgs.extend(msgs)
        return all_msgs

    def fetch_at_me_messages(self, start_time_str):
        """拉取其他群中 @我 的消息（自动过滤报警群、忽略群）"""
        all_at_mes = []
        profiles = self.direct_messages_cfg.get('profiles', [None])
        focused_group_ids = {g.get('id') for g in self.focused_groups}
        
        for profile in profiles:
            cmd = ['dws', 'chat', '+at-me', '--page-all', '-y']
            if profile:
                cmd.extend(['--profile', profile])
            res = self._run_dws_cmd(cmd)
            items = res.get('items', [])
            
            for it in items:
                conv_name = it.get('conversation', {}).get('name', '')
                conv_id = it.get('conversationId', '')
                msg_time = it.get('time', '')
                
                # 过滤条件
                # 1. 如果是重点群已全量拉取，避免重复
                if conv_id in focused_group_ids:
                    continue
                # 2. 报警群/监控群忽略
                if any(kw in conv_name for kw in self.ignored_keywords):
                    continue
                # 3. 时间窗口过滤（24小时内）
                if msg_time and msg_time < start_time_str:
                    continue
                
                it['source_type'] = 'dingtalk_at_me'
                it['group_name'] = conv_name
                all_at_mes.append(it)
        return all_at_mes

    def fetch_direct_messages(self, start_time_str):
        """拉取 1 对 1 私聊消息"""
        if not self.direct_messages_cfg.get('enabled', True):
            return []
            
        all_dms = []
        profiles = self.direct_messages_cfg.get('profiles', [None])
        
        for profile in profiles:
            cmd = ['dws', 'chat', '+dm', '--limit', '50', '-y']
            if profile:
                cmd.extend(['--profile', profile])
            res = self._run_dws_cmd(cmd)
            dms = res.get('conversations', []) or res.get('items', []) or []
            
            for dm in dms:
                target_user = dm.get('userName') or dm.get('name') or '私聊'
                last_msg_time = dm.get('lastMessageTime') or dm.get('updatedAt') or ''
                if last_msg_time and str(last_msg_time) >= start_time_str:
                    dm['source_type'] = 'dingtalk_dm'
                    dm['sender_name'] = target_user
                    all_dms.append(dm)
        return all_dms
