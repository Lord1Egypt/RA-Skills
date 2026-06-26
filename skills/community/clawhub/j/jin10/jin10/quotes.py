"""
行情报价模块
支持获取品种代码列表、实时行情和 K 线数据
"""

from typing import List, Dict, Optional
from .client import BaseClient


class Quote(Dict):
    """行情数据"""
    pass


class QuoteCode(Dict):
    """品种代码"""
    pass


class Kline(Dict):
    """单条 K 线数据"""
    pass


class KlineResult(Dict):
    """K 线响应"""
    pass


# 常用品种代码
COMMON_QUOTES = {
    'XAUUSD': '现货黄金',
    'XAGUSD': '现货白银',
    'USOIL': 'WTI原油',
    'UKOIL': '布伦特原油',
    'COPPER': '现货铜',
    'USDJPY': '美元/日元',
    'EURUSD': '欧元/美元',
    'USDCNH': '美元/人民币',
    'GBPUSD': '英镑/美元',
    'AUDUSD': '澳元/美元',
    'NZDUSD': '新西兰元/美元',
    'USDCHF': '美元/瑞士法郎',
    'USDCAD': '美元/加元',
    'DXY': '美元指数',
    'BTCUSD': '比特币/美元',
    'ETHUSD': '以太坊/美元',
}


class QuotesClient(BaseClient):
    """行情报价客户端"""

    def get_codes(self) -> Dict:
        """获取支持的报价品种代码列表"""
        return self.read_resource('quote://codes')

    def get_quote(self, code: str) -> Dict:
        """获取指定品种实时行情"""
        return self.call_tool('get_quote', {'code': code})

    def get_kline(
        self,
        code: str,
        time: Optional[str] = None,
        count: Optional[int] = None,
    ) -> KlineResult:
        """获取指定品种 K 线数据。"""
        params = {'code': code}
        if time is not None:
            params['time'] = time
        if count is not None:
            params['count'] = count
        return self.call_tool('get_kline', params)

    async def get_quote_async(self, code: str) -> Dict:
        """异步获取指定品种实时行情"""
        return self.call_tool('get_quote', {'code': code})

    def get_quotes(self, codes: List[str]) -> List[Quote]:
        """批量获取多个品种行情"""
        return [self.get_quote(code)['data'] for code in codes]

    @staticmethod
    def format_quote(quote: Quote) -> str:
        """格式化报价为可读字符串"""
        data = quote.get('data', quote)
        ups_price = float(data.get('ups_price', 0))
        ups_percent = float(data.get('ups_percent', 0))
        sign = '+' if ups_price >= 0 else ''

        return (
            f"{data.get('name', '')} ({data.get('code', '')})\n"
            f"当前价: {data.get('close', 'N/A')}\n"
            f"涨跌: {sign}{ups_price} ({sign}{ups_percent}%)\n"
            f"开盘: {data.get('open', 'N/A')} | "
            f"最高: {data.get('high', 'N/A')} | "
            f"最低: {data.get('low', 'N/A')}\n"
            f"时间: {data.get('time', 'N/A')}"
        )

    @staticmethod
    def format_kline(result: KlineResult) -> str:
        """格式化 K 线结果为可读字符串。"""
        data = result.get('data', result)
        code = data.get('code', '')
        name = data.get('name', '')
        klines = data.get('klines', [])

        header = f"{name} ({code}) K线"
        if not klines:
            return f"{header}\n没有返回K线数据"

        lines = [header]
        for item in klines:
            lines.append(
                f"[{item.get('time', 'N/A')}] "
                f"O:{item.get('open', 'N/A')} "
                f"H:{item.get('high', 'N/A')} "
                f"L:{item.get('low', 'N/A')} "
                f"C:{item.get('close', 'N/A')} "
                f"V:{item.get('volume', 'N/A')}"
            )

        return '\n'.join(lines)
