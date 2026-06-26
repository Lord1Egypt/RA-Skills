from typing import Any, Dict, List, Optional

from .base import BaseFormatter


class MemberFormatter(BaseFormatter):
    """会员数据格式化器，将返回的会员列表格式化为中文字段并转换时间戳"""

    FIELD_MAPPINGS: Dict[str, List[str]] = {
        '会员ID': ['id', 'customer_id'],
        '姓名': ['name', 'customer_name'],
        '手机号': ['phone'],
        '积分': ['points'],
        '余额': ['balance'],
        '消费次数': ['consume_count', 'consumes_number'],
        '注册时间': ['register_time', 'create_time'],
        '最近消费时间': ['last_consume_time'],
        '等级': ['level', 'customer_level'],
        '标签': ['tags'],
        '备注': ['remark'],
    }

    TIME_FIELDS = {'注册时间', '最近消费时间'}

    def __init__(self, custom_mappings: Optional[Dict[str, List[str]]] = None):
        # 初始化字段映射，允许通过自定义映射覆盖默认字段
        self.field_mappings: Dict[str, List[str]] = self.FIELD_MAPPINGS.copy()
        if custom_mappings:
            self.field_mappings.update(custom_mappings)

    def format(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        code = raw.get('code', 200)
        message = raw.get('message') or raw.get('msg', '')
        data = raw.get('data')

        customers = self._extract_customers(data)
        if customers:
            formatted = [self._format_member(c) for c in customers]
            total = self._get_total(data, len(formatted))
            return {
                'code': code,
                'message': message or 'success',
                'data': {
                    'customers': formatted,
                    'total': total
                }
            }
        return {'code': code, 'message': message, 'data': data}

    def _extract_customers(self, data: Any) -> Optional[List[Dict[str, Any]]]:
        if isinstance(data, dict):
            if 'data' in data and isinstance(data['data'], list):
                return data['data']
            if 'customers' in data and isinstance(data['customers'], list):
                return data['customers']
        if isinstance(data, list):
            return data
        return None

    def _get_total(self, data: Any, default: int) -> int:
        if isinstance(data, dict):
            return int(data.get('total', default))
        return default

    def _format_member(self, c: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        # 通过字段映射遍历
        for field, keys in self.field_mappings.items():
            value = None
            for k in keys:
                if k in c:
                    value = c[k]
                    break
            if value is None:
                continue
            if field in self.TIME_FIELDS:
                value = self._format_time(value)
            out[field] = value
        # 嵌套字段处理
        if isinstance(c.get('store'), dict):
            out['门店'] = c['store'].get('store_name')
        elif c.get('store_name'):
            out['门店'] = c.get('store_name')
        if isinstance(c.get('card'), dict):
            out['卡号'] = c['card'].get('customer_card_no') or c['card'].get('card_no')
        elif c.get('customer_card_no'):
            out['卡号'] = c.get('customer_card_no')
        return out
