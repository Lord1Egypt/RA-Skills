"""
Memo-记事本技能 - 数据操作工具层
WorkBuddy v2.0.0

本文件作为 records.json 的操作辅助工具。
AI 可直接调用，也可直接读写 JSON 文件。
"""

import json
import os
import re
from datetime import datetime, timedelta

# 数据文件路径（与本脚本同目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORD_FILE = os.path.join(BASE_DIR, 'records.json')


class MemoSkill:
    def __init__(self):
        self.records = self.load_records()

    # ──────────────────────────────────────────
    # 数据读写
    # ──────────────────────────────────────────

    def load_records(self) -> list:
        """读取所有记录"""
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_records(self):
        """保存所有记录"""
        with open(RECORD_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    # ──────────────────────────────────────────
    # 添加记录
    # ──────────────────────────────────────────

    def add_record(self, content: str, work_date: str = None, extra_fields: dict = None) -> dict:
        """
        添加一条工作记录。
        
        Args:
            content: 工作内容原文
            work_date: 工作日期，格式 'yyyy-MM-dd'，None 则用今天
            extra_fields: AI 预解析的字段（可选），会覆盖自动识别结果
        
        Returns:
            新增的记录 dict
        """
        now = datetime.now()
        today_str = work_date or now.strftime('%Y-%m-%d')

        # 去重检查
        for r in self.records:
            if r.get('content') == content and r.get('work_date') == today_str:
                return r  # 已存在，直接返回

        # 生成唯一 ID
        seq = sum(1 for r in self.records if r.get('timestamp', '').startswith(now.strftime('%Y%m%d')))
        record_id = now.strftime('%Y%m%d%H%M%S') + f'_{seq:02d}'

        record = {
            'id': record_id,
            'content': content,
            'timestamp': now.isoformat(),
            'work_date': today_str,
            'work_type': self._get_work_type(content),
            'planning': self._get_planning(content),
            'importance': self._get_importance(content),
            'urgency': self._get_urgency(content),
            'quality': self._get_quality(content),
            'contacts': self._extract_contacts(content),
            'contact_count': 0,
            'time_info': self._extract_time_info(content),
            'is_todo': self._is_todo(content),
            'todo_done': False,
        }
        record['contact_count'] = len(record['contacts'])

        # AI 预解析字段覆盖
        if extra_fields:
            record.update(extra_fields)

        self.records.append(record)
        self.save_records()
        return record

    # ──────────────────────────────────────────
    # 查询与筛选
    # ──────────────────────────────────────────

    def filter_by_date(self, start_date: str, end_date: str) -> list:
        """
        按工作日期范围筛选记录。
        
        Args:
            start_date: 开始日期，格式 'yyyy-MM-dd'
            end_date: 结束日期，格式 'yyyy-MM-dd'
        
        Returns:
            筛选后的记录列表（按 work_date 升序）
        """
        result = []
        for r in self.records:
            wd = r.get('work_date', '')
            if start_date <= wd <= end_date:
                result.append(r)
        return sorted(result, key=lambda x: x.get('work_date', ''))

    def get_todos(self) -> list:
        """获取所有未完成的待办记录"""
        return [r for r in self.records if r.get('is_todo') and not r.get('todo_done')]

    def mark_todo_done(self, record_id: str) -> bool:
        """将指定 ID 的待办标记为已完成"""
        for r in self.records:
            if r.get('id') == record_id:
                r['todo_done'] = True
                self.save_records()
                return True
        return False

    def search(self, keyword: str) -> list:
        """按关键词搜索内容"""
        return [r for r in self.records if keyword in r.get('content', '')]

    # ──────────────────────────────────────────
    # 导出报告
    # ──────────────────────────────────────────

    def export_report(self, start_date: str, end_date: str, output_path: str = None) -> str:
        """
        生成 Markdown 格式报告并写入文件。
        
        Args:
            start_date: 开始日期 'yyyy-MM-dd'
            end_date: 结束日期 'yyyy-MM-dd'
            output_path: 输出文件路径，None 则自动生成到 BASE_DIR
        
        Returns:
            输出文件的绝对路径
        """
        records = self.filter_by_date(start_date, end_date)
        now = datetime.now()

        if not output_path:
            filename = f"工作记录导出_{now.strftime('%Y-%m-%d')}.md"
            output_path = os.path.join(BASE_DIR, filename)

        content = self._build_report_md(records, start_date, end_date, now)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_path

    def _build_report_md(self, records: list, start_date: str, end_date: str, now: datetime) -> str:
        """构建报告 Markdown 文本"""
        lines = []
        lines.append('# 工作记录导出\n')
        lines.append(f'**导出时间**：{now.strftime("%Y年%m月%d日 %H:%M")}  ')
        lines.append(f'**记录期间**：{start_date} - {end_date}  ')
        lines.append(f'**记录总数**：{len(records)}条\n')
        lines.append('---\n')
        lines.append('## 记录明细\n')

        for i, r in enumerate(records, 1):
            date_label = r.get('work_date', '')
            time_info = r.get('time_info', '未标注')
            if time_info and time_info != '未标注':
                date_label += f' {time_info}'

            lines.append(f'### {i}. {date_label}')
            lines.append('| 字段 | 内容 |')
            lines.append('|------|------|')
            lines.append(f'| **工作内容** | {r.get("content", "")} |')
            lines.append(f'| **工作类型** | {r.get("work_type", "其他")} |')
            lines.append(f'| **事务性质** | {r.get("planning", "临时")} |')

            if r.get('importance', '未标注') != '未标注':
                lines.append(f'| **重要性** | {r["importance"]} |')
            if r.get('urgency', '未标注') != '未标注':
                lines.append(f'| **紧迫性** | {r["urgency"]} |')
            if r.get('quality', '未标注') != '未标注':
                lines.append(f'| **完成质量** | {r["quality"]} |')

            contacts = r.get('contacts', [])
            lines.append(f'| **对接人员** | {", ".join(contacts) if contacts else "无"} |')
            lines.append(f'| **对接人数** | {r.get("contact_count", 0)}人 |')
            lines.append(f'| **时间信息** | {r.get("time_info", "未标注")} |')
            lines.append('\n---\n')

        # 统计汇总
        total = len(records)
        planned = sum(1 for r in records if r.get('planning') == '计划内')
        temp = total - planned
        total_contacts = sum(r.get('contact_count', 0) for r in records)

        lines.append('## 统计汇总\n')
        lines.append('| 统计维度 | 数量/占比 |')
        lines.append('|----------|-----------|')
        lines.append(f'| **总记录数** | {total}条 |')
        if total > 0:
            lines.append(f'| **计划内事务** | {planned}条 ({planned*100//total}%) |')
            lines.append(f'| **临时事务** | {temp}条 ({temp*100//total}%) |')
        lines.append(f'| **总对接人数** | {total_contacts}人 |')
        lines.append('')

        # 工作类型分布
        type_dist = {}
        for r in records:
            wt = r.get('work_type', '其他')
            type_dist[wt] = type_dist.get(wt, 0) + 1

        lines.append('### 工作类型分布')
        lines.append('| 工作类型 | 数量 | 占比 |')
        lines.append('|----------|------|------|')
        for wt, cnt in sorted(type_dist.items(), key=lambda x: -x[1]):
            pct = cnt * 100 // total if total > 0 else 0
            lines.append(f'| {wt} | {cnt}条 | {pct}% |')
        lines.append('')

        # 待办事项
        todos = [r for r in records if r.get('is_todo') and not r.get('todo_done')]
        if todos:
            lines.append('---\n')
            lines.append('## 待办事项\n')
            for t in todos:
                lines.append(f'- [ ] {t.get("content", "")}')
            lines.append('')

        lines.append('---\n')
        lines.append('*本报告由工作记录助手自动生成*\n')

        return '\n'.join(lines)

    # ──────────────────────────────────────────
    # 自动识别辅助方法
    # ──────────────────────────────────────────

    def _get_work_type(self, content: str) -> str:
        rules = [
            ('会议', ['会议', '开会', '研讨', '评审', '汇报']),
            ('沟通', ['联系', '对接', '沟通', '交流', '讨论', '反馈', '说', '问', '回复']),
            ('文档', ['文档', '写', '报告', '材料', '总结', '整理', '台账']),
            ('设计', ['设计', '规划', '方案', '蓝图']),
            ('测试', ['测试', '验证', '检查', '调试', '排查']),
            ('编程', ['编程', '编码', '开发', '写代码', '技能', '部署']),
            ('调研', ['调研', '研究', '调查', '了解']),
        ]
        for wt, keywords in rules:
            if any(k in content for k in keywords):
                return wt
        return '其他'

    def _get_planning(self, content: str) -> str:
        if any(k in content for k in ['临时', '突然', '插', '紧急插']):
            return '临时'
        if any(k in content for k in ['计划', '原本安排', '安排', '原定']):
            return '计划内'
        return '临时'

    def _get_importance(self, content: str) -> str:
        if any(k in content for k in ['重要', '关键', '核心', '必须']):
            return '重要'
        if any(k in content for k in ['不重要', '次要']):
            return '不重要'
        return '未标注'

    def _get_urgency(self, content: str) -> str:
        if any(k in content for k in ['紧急', '尽快', '马上', '立刻', '急需', '急']):
            return '紧急'
        if any(k in content for k in ['不紧急', '稍后', '以后']):
            return '不紧急'
        return '未标注'

    def _get_quality(self, content: str) -> str:
        if any(k in content for k in ['完成了', '搞定', '解决', '顺利', '成功', '正常了']):
            return '高质量'
        if any(k in content for k in ['完成得不错', '还行', '一般', '凑合', '完成']):
            return '中等'
        if any(k in content for k in ['有问题', '没弄好', '卡住', '失败', '需要改进']):
            return '待改进'
        return '未标注'

    def _extract_contacts(self, content: str) -> list:
        """简单提取中文人名（2-4字）和常见角色词"""
        contacts = []
        # 常见角色词
        roles = ['产品经理', '运维', '保安', '领导', '同事', '客户', '用户']
        for role in roles:
            if role in content:
                contacts.append(role)
        # 匹配"X找我"、"和X"、"联系X"、"通知X"等前后的中文姓名（2-4字）
        name_patterns = [
            r'(?:和|与|联系|通知|找|告知|协调)([^\s，,。.！!？?、\d]{2,4})',
        ]
        for pattern in name_patterns:
            matches = re.findall(pattern, content)
            for m in matches:
                if m not in roles and m not in contacts:
                    contacts.append(m)
        return contacts

    def _extract_time_info(self, content: str) -> str:
        for word in ['上午', '下午', '晚上', '早上', '凌晨']:
            if word in content:
                return word
        match = re.search(r'(\d{1,2})[点:](\d{2})?', content)
        if match:
            return match.group(0)
        return '未标注'

    def _is_todo(self, content: str) -> bool:
        todo_signals = ['下周', '明天', '待处理', '要去', '需要', '再去', '等上班', '上班后', '下次']
        done_signals = ['已完成', '搞定', '解决了', '完成了', '处理了', '正常了']
        if any(s in content for s in done_signals):
            return False
        return any(s in content for s in todo_signals)
