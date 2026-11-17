"""
记事本技能 - 数据操作工具层
WorkBuddy v2.0.1

本文件是 records.json 的操作工具。
AI 仅通过 MemoSkill 实例方法操作，禁止直接读写 records.json——
去重检查和自动化同步逻辑均依赖实例方法，绕过会导致重复记录和提醒失效。

v2.0.1 更新：
- ID唯一性修复：add_record() 生成ID增加毫秒精度（%Y%m%d%H%M%S + 毫秒3位 + 序号），杜绝同秒内多次添加ID重复
- timestamp 字段统一使用 ID 生成时的时间变量（之前误用旧 now 变量）
- 修复历史29条重复ID记录

v2.0.0 更新：
- 写入安全：save_records() 增加重试机制（3次，间隔0.3s），解决并发写入 PermissionError
- 回复规范：add_record() 返回值增加 confirmation 字段，确保AI回复时展示具体内容+事件ID
- 查询推荐：文档明确优先使用 filter_by_date() 而非 search() 进行日期范围查询
- 字段优化：_extract_contacts() 扩展人名识别规则，增加"给X""找X""与X"等模式

v1.13.0 更新：
- 数据安全防护：save_records() 增加三层防护（写入前自动备份、记录数对比警告、AUTO-MERGE自动合并）
- 移除未实现的图标安装功能
"""

import json
import os
import re
import time
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
        """保存所有记录（写入前自动备份上一版，防止意外覆盖丢失数据；含重试机制防并发写入冲突）"""
        # 安全防护：写入前备份上一版
        if os.path.exists(RECORD_FILE):
            backup_path = RECORD_FILE + '.bak'
            try:
                import shutil
                shutil.copy2(RECORD_FILE, backup_path)
            except Exception:
                pass  # 备份失败不阻断正常写入
        # 安全防护：读取已有文件，合并而非覆盖
        existing = []
        if os.path.exists(RECORD_FILE):
            try:
                with open(RECORD_FILE, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, Exception):
                existing = []
        # 如果 self.records 比已有记录少很多，可能是误操作，发出警告
        if existing and len(self.records) < len(existing) * 0.5:
            import sys
            print(f"WARNING: 即将写入 {len(self.records)} 条记录，但文件中有 {len(existing)} 条。"
                  f"可能存在数据丢失风险！如确认覆盖，请重新调用。", file=sys.stderr)
            # 自动合并：保留已有记录中不在 self.records 里的条目
            existing_ids = {r.get('id') for r in existing}
            self_ids = {r.get('id') for r in self.records}
            missing = [r for r in existing if r.get('id') not in self_ids]
            if missing:
                self.records.extend(missing)
                print(f"AUTO-MERGE: 已自动合并 {len(missing)} 条缺失记录", file=sys.stderr)
        # 重试写入：解决并发访问时 PermissionError（3次重试，间隔0.3秒）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with open(RECORD_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.records, f, ensure_ascii=False, indent=2)
                return  # 写入成功
            except PermissionError as e:
                if attempt < max_retries - 1:
                    import sys
                    print(f"WARNING: 写入被占用，第{attempt+1}次重试（共{max_retries}次）...", file=sys.stderr)
                    time.sleep(0.3)
                else:
                    import sys
                    print(f"ERROR: 写入失败，重试{max_retries}次后仍被占用: {e}", file=sys.stderr)
                    raise

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
        # 优先级：显式参数 > 内容中解析 > 今天
        if work_date:
            today_str = work_date
        else:
            today_str = self._parse_date(content)
            # _parse_date 返回今天时，说明没有日期语义，正常使用今天即可

        # 去重检查
        for r in self.records:
            if r.get('content') == content and r.get('work_date') == today_str:
                return r  # 已存在，直接返回

        # 生成唯一 ID（含毫秒+序号，确保同一秒内多次添加也不重复）
        ts = datetime.now()
        seq = sum(1 for r in self.records if r.get('timestamp', '').startswith(ts.strftime('%Y-%m-%d')))
        record_id = ts.strftime('%Y%m%d%H%M%S') + f'{ts.microsecond // 1000:03d}' + f'_{seq:02d}'

        record = {
            'id': record_id,
            'content': content,
            'timestamp': ts.isoformat(),
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
            'reminder_time': None,   # 自定义提醒时间，格式 "HH:MM"，None 表示使用默认 08:00
        }
        record['contact_count'] = len(record['contacts'])

        # AI 预解析字段覆盖
        if extra_fields:
            record.update(extra_fields)

        self.records.append(record)
        self.save_records()

        # 构建确认信息，确保AI回复时展示具体内容+事件ID
        record['_confirmation'] = {
            'id': record['id'],
            'content': record['content'],
            'work_date': record['work_date'],
            'work_type': record['work_type'],
            'contacts': record['contacts'],
        }
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

    def get_automation_action_after_complete(self, record_id: str) -> dict:
        """
        标记待办完成后，返回需要执行的自动化操作。
        
        Args:
            record_id: 已完成的待办记录 ID
            
        Returns:
            dict: {
                'action': 'delete' | 'update' | 'none',
                'work_date': 'yyyy-MM-dd',
                'automation_name': 'xxx 工作提醒',
                'remaining_todos': [...],  # 如果 action=update，返回剩余待办
                'reason': '说明'
            }
        """
        # 找到被完成的记录
        completed_record = None
        for r in self.records:
            if r.get('id') == record_id:
                completed_record = r
                break
        
        if not completed_record:
            return {'action': 'none', 'reason': '记录未找到'}
        
        work_date = completed_record.get('work_date')
        if not work_date:
            return {'action': 'none', 'reason': '无工作日期'}
        
        # 检查该日期是否还有其他未完成待办
        remaining_todos = self.get_pending_todos_for_date(work_date)
        
        automation_name = self.get_automation_name(work_date)
        
        if not remaining_todos:
            # 没有其他待办，删除自动化
            return {
                'action': 'delete',
                'work_date': work_date,
                'automation_name': automation_name,
                'remaining_todos': [],
                'reason': f'该日期已无其他未完成待办，应删除自动化任务'
            }
        else:
            # 还有其他待办，更新自动化
            todo_contents = [t.get('content', '')[:50] for t in remaining_todos]
            return {
                'action': 'update',
                'work_date': work_date,
                'automation_name': automation_name,
                'remaining_todos': todo_contents,
                'reason': f'该日期还有 {len(remaining_todos)} 项未完成待办，应更新自动化任务'
            }

    def get_automation_action_after_add(self, record_id: str) -> dict:
        """
        添加待办后，返回需要执行的自动化操作。
        
        Args:
            record_id: 新添加的待办记录 ID
            
        Returns:
            dict: {
                'action': 'create' | 'update' | 'none',
                'work_date': 'yyyy-MM-dd',
                'automation_name': 'xxx 工作提醒',
                'all_todos': [...],  # 当天所有待办
                'reminder_time': 'HH:MM',
                'reason': '说明'
            }
        """
        # 找到新添加的记录
        new_record = None
        for r in self.records:
            if r.get('id') == record_id:
                new_record = r
                break
        
        if not new_record:
            return {'action': 'none', 'reason': '记录未找到'}
        
        if not new_record.get('is_todo'):
            return {'action': 'none', 'reason': '非待办记录'}
        
        work_date = new_record.get('work_date')
        if not work_date:
            return {'action': 'none', 'reason': '无工作日期'}
        
        # 检查该日期是否已有自动化任务（需要查询 WorkBuddy，AI 配合）
        # 这里返回创建/更新所需的参数，由 AI 检查是否已存在
        
        all_todos = self.get_pending_todos_for_date(work_date)
        todo_contents = [t.get('content', '')[:50] for t in all_todos]
        
        # 获取最早的通知时间
        reminder_time = new_record.get('reminder_time') or '08:00'
        for t in all_todos:
            rt = t.get('reminder_time')
            if rt:
                if rt < reminder_time:
                    reminder_time = rt
        
        # 判断是否需要设置单次提醒（validFrom/validUntil）
        # 如果用户明确指定了特定日期的提醒，设置生效日期区间为该日期
        is_single_reminder = new_record.get('is_single_reminder', False)
        
        result = {
            'action': 'create_or_update',  # AI 需要检查是否已存在
            'work_date': work_date,
            'automation_name': self.get_automation_name(work_date),
            'all_todos': todo_contents,
            'reminder_time': reminder_time,
            'is_single_reminder': is_single_reminder,
            'reason': f'该日期有 {len(all_todos)} 项待办，应创建或更新自动化任务'
        }
        
        # 如果是单次提醒（用户明确要求某一天提醒，而不是重复任务），添加 validFrom/validUntil
        if is_single_reminder:
            result['validFrom'] = f'{work_date}T00:00:00'
            result['validUntil'] = f'{work_date}T23:59:59'
        
        return result

    def search(self, keyword: str) -> list:
        """
        智能关键词搜索（v1.12.0）。
        
        支持以下匹配模式：
        1. 精确匹配：如果关键词完整出现在内容中，直接返回
        2. 分词匹配：如果精确匹配失败，自动提取2-3字核心词进行匹配
        3. 多关键词OR：支持空格分隔的多关键词，任意一个匹配即返回
        
        Examples:
            - "华夏卡" → 自动拆分为["华夏"]，匹配"华夏银行信用卡"
            - "华夏 注销" → 包含"华夏"或"注销"的记录都会返回
            - "华夏银行信用卡" → 精确匹配
        """
        content_lower = keyword.lower().strip()
        
        # 1. 先尝试精确匹配
        exact_matches = [r for r in self.records if keyword in r.get('content', '')]
        if exact_matches:
            return exact_matches
        
        # 2. 尝试多关键词OR匹配（空格分隔）
        if ' ' in keyword:
            keywords = keyword.split()
            results = []
            seen_ids = set()
            for kw in keywords:
                # 对每个关键词递归调用（但避免无限递归）
                for r in self.records:
                    if kw in r.get('content', '') and r.get('id') not in seen_ids:
                        results.append(r)
                        seen_ids.add(r.get('id'))
            return results
        
        # 3. 分词匹配：提取核心词（2-3字）
        # "华夏卡" → ["华夏", "卡"]
        # "华夏银行" → ["华夏", "银行"]
        core_words = []
        
        # 取前2-3字作为核心词
        if len(keyword) >= 2:
            core_words.append(keyword[:2])
        if len(keyword) >= 3:
            core_words.append(keyword[:3])
        
        # 提取中文词汇（连续2字以上的组合）
        import re
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', keyword)
        for w in chinese_words:
            if w not in core_words:
                core_words.append(w)
        
        # 用核心词进行匹配
        if core_words:
            results = []
            seen_ids = set()
            for r in self.records:
                content = r.get('content', '')
                for cw in core_words:
                    if cw in content and r.get('id') not in seen_ids:
                        results.append(r)
                        seen_ids.add(r.get('id'))
                        break  # 一条记录只添加一次
            return results
        
        # 4. 都没匹配到，返回空列表
        return []

    def update_record(self, record_id: str = None, keyword: str = None, updates: dict = None) -> dict:
        """
        更新已有记录的任意字段。可按 ID 或关键词定位记录。

        Args:
            record_id: 记录 ID（精确匹配，优先使用）
            keyword:   内容关键词（模糊匹配，当 record_id 未提供时使用；若匹配多条则返回列表供选择）
            updates:   要更新的字段字典，例如 {'content': '新内容', 'work_type': '会议'}

        Returns:
            更新后的记录 dict；若未找到返回 None；若关键词匹配多条返回匹配列表
        """
        if not updates:
            return None

        target = None

        # 优先按 ID 精确查找
        if record_id:
            for r in self.records:
                if r.get('id') == record_id:
                    target = r
                    break

        # 按关键词模糊查找
        elif keyword:
            matches = [r for r in self.records if keyword in r.get('content', '')]
            if len(matches) == 0:
                return None
            if len(matches) > 1:
                # 返回匹配列表，由 AI 引导用户进一步确认
                return {'_ambiguous': True, 'matches': matches}
            target = matches[0]

        if target is None:
            return None

        # 执行更新
        target.update(updates)

        # 若更新了 contacts，同步 contact_count
        if 'contacts' in updates:
            target['contact_count'] = len(updates['contacts'])

        self.save_records()
        return target

    def delete_record(self, record_id: str = None, keyword: str = None) -> bool:
        """
        删除一条记录。可按 ID 或关键词定位。

        Args:
            record_id: 记录 ID（精确匹配，优先使用）
            keyword:   内容关键词（模糊匹配；若匹配多条返回列表供确认）

        Returns:
            True 表示删除成功；False 表示未找到；dict 表示匹配多条（含 _ambiguous 标志）
        """
        if record_id:
            for i, r in enumerate(self.records):
                if r.get('id') == record_id:
                    self.records.pop(i)
                    self.save_records()
                    return True
            return False

        if keyword:
            matches = [r for r in self.records if keyword in r.get('content', '')]
            if len(matches) == 0:
                return False
            if len(matches) > 1:
                return {'_ambiguous': True, 'matches': matches}
            self.records.remove(matches[0])
            self.save_records()
            return True

        return False

    # ──────────────────────────────────────────
    # 智能同步辅助（v1.5.0）
    # ──────────────────────────────────────────

    def get_automation_name(self, work_date: str) -> str:
        """返回指定日期对应的自动化任务名称"""
        return f"{work_date} 工作提醒"

    def build_reminder_rrule(self, work_date: str, reminder_time: str = None) -> str:
        """
        根据 work_date 和 reminder_time 生成 rrule 字符串。

        Args:
            work_date:     格式 'yyyy-MM-dd'
            reminder_time: 格式 'HH:MM'，None 则默认 '08:00'

        Returns:
            rrule 字符串，例如 'FREQ=WEEKLY;BYDAY=MO;BYHOUR=8;BYMINUTE=0'
        """
        day_map = {0: 'MO', 1: 'TU', 2: 'WE', 3: 'TH', 4: 'FR', 5: 'SA', 6: 'SU'}
        from datetime import date
        d = date.fromisoformat(work_date)
        byday = day_map[d.weekday()]

        time_str = reminder_time or '08:00'
        try:
            h, m = [int(x) for x in time_str.split(':')]
        except Exception:
            h, m = 8, 0

        return f"FREQ=WEEKLY;BYDAY={byday};BYHOUR={h};BYMINUTE={m}"

    def get_pending_todos_for_date(self, work_date: str) -> list:
        """获取指定日期所有未完成的待办记录"""
        return [
            r for r in self.records
            if r.get('is_todo') and not r.get('todo_done') and r.get('work_date') == work_date
        ]

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
            r'(?:和|与|联系|通知|找|告知|协调|给|跟|帮|给X)([^\s，,。.！!？?、\d]{2,4})',
        ]
        for pattern in name_patterns:
            matches = re.findall(pattern, content)
            for m in matches:
                if m not in roles and m not in contacts:
                    contacts.append(m)
        return contacts

    def _extract_time_info(self, content: str) -> str:
        # 只提取纯时间描述，不含日期语义
        # 日期表达由 _parse_date 处理，写入 work_date
        pure_time_words = ['上午', '下午', '晚上', '早上', '凌晨']
        for word in pure_time_words:
            if word in content:
                return word
        match = re.search(r'(\d{1,2})[点:](\d{2})?', content)
        if match:
            return match.group(0)
        return ''  # 语义日期不在这里，避免误填

    def _parse_date(self, content: str) -> str:
        """
        从内容中解析口语日期，返回标准 'yyyy-MM-dd'。
        若无日期语义或解析失败，返回今天。
        """
        now = datetime.now()
        today = now.date()

        # 精确匹配 "yyyy-MM-dd" 格式
        std_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
        if std_match:
            return std_match.group(1)

        # 匹配 "X月X日" / "X月X号"
        md_match = re.search(r'(\d{1,2})月(\d{1,2})[日号]', content)
        if md_match:
            month, day = int(md_match.group(1)), int(md_match.group(2))
            try:
                return f"{today.year}-{month:02d}-{day:02d}"
            except ValueError:
                pass

        # "今天"
        if '今天' in content:
            return today.isoformat()

        # "明天"
        if '明天' in content:
            return (today + timedelta(days=1)).isoformat()

        # "后天"
        if '后天' in content:
            return (today + timedelta(days=2)).isoformat()

        # "大后天"
        if '大后天' in content:
            return (today + timedelta(days=3)).isoformat()

        # "下周"（下周周一）
        if re.search(r'下周', content):
            days_ahead = 7 - today.weekday()  # 距下周一的天数
            if days_ahead <= 0:
                days_ahead += 7
            next_monday = today + timedelta(days=days_ahead)
            return next_monday.isoformat()

        # "下周X"（下周几）
        weekday_map = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 0, '天': 0}
        weekday_match = re.search(r'下周([一二三四五六日天])', content)
        if weekday_match:
            target_weekday = weekday_map[weekday_match.group(1)]
            days_ahead = 7 - today.weekday() + target_weekday
            if days_ahead <= 7:  # 确保在下周
                days_ahead += 7
            target = today + timedelta(days=days_ahead)
            return target.isoformat()

        # "本周X" / "这周X"
        weekday_match2 = re.search(r'本周([一二三四五六日天])', content)
        if not weekday_match2:
            weekday_match2 = re.search(r'这周([一二三四五六日天])', content)
        if weekday_match2:
            target_weekday = weekday_map[weekday_match2.group(1)]
            days_diff = target_weekday - today.weekday()
            if days_diff < 0:
                days_diff += 7
            target = today + timedelta(days=days_diff)
            return target.isoformat()

        # "下周内" / "近期" / "这段时间" → 今天
        vague_future = ['下周内', '近期', '近期内', '这段时间', '最近', '最近几天']
        for v in vague_future:
            if v in content:
                return today.isoformat()

        # 解析失败，返回今天
        return today.isoformat()

    def _is_todo(self, content: str) -> bool:
        todo_signals = ['下周', '明天', '待处理', '要去', '需要', '再去', '等上班', '上班后', '下次']
        done_signals = ['已完成', '搞定', '解决了', '完成了', '处理了', '正常了']
        if any(s in content for s in done_signals):
            return False
        return any(s in content for s in todo_signals)


# ──────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='记事本技能 CLI')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # 添加记录
    p_add = sub.add_parser('add', help='添加一条记录')
    p_add.add_argument('content', help='记录内容')
    p_add.add_argument('--date', '-d', default=None, help='工作日期 YYYY-MM-DD，默认今天')
    p_add.add_argument('--type', '-t', default=None, help='工作类型')
    p_add.add_argument('--todo', action='store_true', help='标记为待办')
    p_add.add_argument('--done', action='store_true', help='标记已完成')
    p_add.add_argument('--reminder', default=None, help='提醒时间 HH:MM')

    # 标记完成
    p_done = sub.add_parser('done', help='标记待办完成')
    p_done.add_argument('id', help='记录ID')
    p_done.add_argument('--keyword', '-k', default=None, help='关键词（替代ID）')

    # 查询
    p_search = sub.add_parser('search', help='关键词搜索')
    p_search.add_argument('keyword', help='搜索关键词')

    # 待办列表
    sub.add_parser('todos', help='列出所有未完成待办')

    # 统计
    p_stat = sub.add_parser('stat', help='统计')
    p_stat.add_argument('--start', default=None, help='开始日期 YYYY-MM-DD')
    p_stat.add_argument('--end', default=None, help='结束日期 YYYY-MM-DD')

    # 导出
    p_exp = sub.add_parser('export', help='导出报告')
    p_exp.add_argument('start', help='开始日期 YYYY-MM-DD')
    p_exp.add_argument('end', help='结束日期 YYYY-MM-DD')
    p_exp.add_argument('--out', '-o', default=None, help='输出文件路径')

    args = parser.parse_args()
    s = MemoSkill()

    if args.cmd == 'add':
        extra = {}
        if args.type:
            extra['work_type'] = args.type
        if args.todo:
            extra['is_todo'] = True
        if args.done:
            extra['todo_done'] = True
        if args.reminder:
            extra['reminder_time'] = args.reminder
        r = s.add_record(args.content, work_date=args.date, extra_fields=extra or None)
        print(f"OK: {r['id']}")

    elif args.cmd == 'done':
        if args.keyword:
            results = s.search(args.keyword)
            if len(results) == 1:
                rid = results[0]['id']
            else:
                print(f"找到 {len(results)} 条记录，请用ID精确指定：")
                for r in results:
                    print(f"  {r['id']}  {r['content'][:40]}")
                exit(1)
        else:
            rid = args.id
        ok = s.mark_todo_done(rid)
        print('OK' if ok else 'FAIL: 未找到记录')

    elif args.cmd == 'search':
        for r in s.search(args.keyword):
            print(f"{r['id']}  [{r['work_date']}] {r['content'][:50]}")

    elif args.cmd == 'todos':
        for r in s.get_todos():
            print(f"{r['id']}  [{r['work_date']}] {r['content'][:50]}")

    elif args.cmd == 'stat':
        from datetime import date, timedelta
        today = date.today()
        start = args.start or (today - timedelta(days=30)).strftime('%Y-%m-%d')
        end = args.end or today.strftime('%Y-%m-%d')
        recs = s.filter_by_date(start, end)
        todos = [r for r in recs if r.get('is_todo')]
        done = [r for r in todos if r.get('todo_done')]
        print(f"统计区间：{start} ~ {end}")
        print(f"总记录：{len(recs)} 条")
        print(f"待办总数：{len(todos)}，已完成：{len(done)}，未完成：{len(todos)-len(done)}")

    elif args.cmd == 'export':
        path = s.export_report(args.start, args.end, args.out)
        print(f"已导出：{path}")
