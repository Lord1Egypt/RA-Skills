#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球财报智能下载器 v2.2 (2026-04-12)
- ✅ 自动识别市场（A 股/港股/美股）
- ✅ 自动选择合适的爬虫
- ✅ 港股使用东方财富 + 同花顺 API（无需认证）
- ✅ 支持股票代码/公司名称
- ✅ subprocess 替代 os.system（错误检查 + 输出捕获）
- ✅ 报告类型大小写保护（10-K 不会被转成 10-k）
- ✅ 下载后自动验证结果
- ✅ --dry-run 模式预览
"""

import sys
import os
import json
import argparse
import subprocess
from typing import Dict, List, Optional, Tuple

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# HK downloader 路径
HK_DOWNLOADER = '/root/.openclaw/workspace/skills/hk-financial-downloader/scripts/hk_downloader.py'

# Python 可执行文件路径（统一使用 python3）
PYTHON = sys.executable or 'python3'

# 美股外国公司（ADR / Foreign Private Issuers）— 使用 20-F/6-K 而非 10-K/10-Q
US_FOREIGN_TICKERS = {
    # 中国 ADR
    'BABA', 'BIDU', 'JD', 'PDD', 'NIO', 'XPEV', 'LI', 'TME', 'BILI', 'IQ',
    'WB', 'NTES', 'VIPS', 'HTHT', 'YUMC', 'ZTO', 'BEKE', 'ATHM', 'DOYU', 'HUYA',
    # 日本
    'SONY', 'TM', 'HMC',
    # 欧洲
    'SAP', 'NVS', 'AZN', 'GSK',
    # 加拿大
    'RY', 'TD', 'BMO', 'BNS', 'CM', 'SHOP', 'CP', 'CNI', 'ENB',
    # 拉美
    'VALE', 'PBR', 'ABEV', 'ITUB', 'AMX',
}


class GlobalFinancialDownloader:
    """全球财报智能下载器"""
    
    def __init__(self):
        # 加载外部映射配置（使用 Skill 目录内的配置文件）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.mapping_file = os.path.join(script_dir, 'stock_mapping.json')
        self.stock_market_map = {}
        self.name_stock_map = {}
        self.report_type_map = {
            # v2.2: 区分 US 本土 (10-K/10-Q) 和 US 外国 (20-F/6-K)
            'annual':   {'cn': 'annual',  'hk': '年报',   'us': '10-K', 'us_foreign': '20-F'},
            '年报':     {'cn': 'annual',  'hk': '年报',   'us': '10-K', 'us_foreign': '20-F'},
            'interim':  {'cn': 'interim', 'hk': '中报',   'us': '10-Q', 'us_foreign': '6-K'},
            '中报':     {'cn': 'interim', 'hk': '中报',   'us': '10-Q', 'us_foreign': '6-K'},
            '半年报':   {'cn': 'interim', 'hk': '中报',   'us': '10-Q', 'us_foreign': '6-K'},
            'quarterly':{'cn': 'regular', 'hk': '季报',   'us': '10-Q', 'us_foreign': '6-K'},
            '季报':     {'cn': 'regular', 'hk': '季报',   'us': '10-Q', 'us_foreign': '6-K'},
            '10-K':     {'cn': 'annual',  'hk': '年报',   'us': '10-K', 'us_foreign': '20-F'},
            '10-Q':     {'cn': 'regular', 'hk': '季报',   'us': '10-Q', 'us_foreign': '6-K'},
            '20-F':     {'cn': 'annual',  'hk': '年报',   'us': '20-F', 'us_foreign': '20-F'},
            '6-K':      {'cn': 'regular', 'hk': 'all',    'us': '6-K',  'us_foreign': '6-K'},
            'all':      {'cn': 'regular', 'hk': 'all',    'us': 'all',  'us_foreign': 'all'},
            '全部':     {'cn': 'regular', 'hk': 'all',    'us': 'all',  'us_foreign': 'all'},
        }
        self.script_paths = {
            'cninfo_api_scraper': '/root/.openclaw/workspace/scripts/cninfo_api_scraper.py',
            'hk_financial_downloader': HK_DOWNLOADER,
            'sec_edgar_scraper': '/root/.openclaw/workspace/scripts/sec_edgar_scraper.py',
        }
        self.load_mapping()
    
    def load_mapping(self):
        """加载股票映射配置"""
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # A 股
            for stock in data.get('cn_stocks', {}).get('stocks', []):
                code, cn_name, en_name = stock[0], stock[1], stock[2]
                self.stock_market_map[code] = {'market': 'CN', 'name': en_name, 'script': 'cninfo_api_scraper'}
                self.name_stock_map[cn_name] = code
                self.name_stock_map[en_name] = code
            
            # 港股 — 使用 hk_downloader (v2 新增)
            for stock in data.get('hk_stocks', {}).get('stocks', []):
                code, cn_name, en_name = stock[0], stock[1], stock[2]
                self.stock_market_map[code] = {'market': 'HK', 'name': en_name, 'script': 'hk_financial_downloader'}
                self.name_stock_map[cn_name] = code
                self.name_stock_map[en_name] = code
            
            # 美股
            for stock in data.get('us_stocks', {}).get('stocks', []):
                code, cn_name, en_name = stock[0], stock[1], stock[2]
                self.stock_market_map[code] = {'market': 'US', 'name': en_name, 'script': 'sec_edgar_scraper'}
                self.name_stock_map[cn_name] = code
                self.name_stock_map[en_name] = code
            
            print(f"✅ 加载映射：{len(self.stock_market_map)} 家公司")
            
        except Exception as e:
            print(f"⚠️ 加载映射失败：{e}，使用默认映射")
            self.load_default_mapping()
    
    def load_default_mapping(self):
        """加载默认映射（硬编码）"""
        self.stock_market_map = {
            '600519': {'market': 'CN', 'name': 'kweichow_moutai', 'script': 'cninfo_api_scraper'},
            '00700': {'market': 'HK', 'name': 'tencent', 'script': 'hk_financial_downloader'},
            'AAPL': {'market': 'US', 'name': 'apple', 'script': 'sec_edgar_scraper'},
        }
        self.name_stock_map = {
            '贵州茅台': '600519',
            '腾讯': '00700',
            '苹果': 'AAPL',
        }
    
    def identify_stock(self, identifier: str) -> Optional[Dict]:
        """识别股票代码和市场
        
        支持多种代码格式：
        - A 股：600519, 000858（6 位数字）
        - 港股：00700, 0700, 700, HK0700（3-5 位数字，可选 HK 前缀）
        - 美股：AAPL, MSFT（字母）
        """
        identifier = identifier.strip()
        
        # 1. 直接匹配
        if identifier in self.stock_market_map:
            return self.stock_market_map[identifier]
        
        # 2. 公司名称匹配
        if identifier in self.name_stock_map:
            stock_code = self.name_stock_map[identifier]
            return self.stock_market_map.get(stock_code)
        
        # 3. 规范化代码后匹配
        normalized = self._normalize_code(identifier)
        if normalized and normalized in self.stock_market_map:
            return self.stock_market_map[normalized]
        
        return None
    
    def _normalize_code(self, code: str) -> str:
        """规范化股票代码
        
        港股：700 → 00700 → 补到 5 位
        A 股：600519 → 600519（已是 6 位）
        美股：AAPL → AAPL（字母不变）
        """
        code = code.upper().strip()
        
        # 去除 HK/SH/SZ 前缀
        for prefix in ['HK', 'SH', 'SZ']:
            if code.startswith(prefix):
                code = code[len(prefix):]
                break
        
        # 纯数字 → 按市场补齐位数
        if code.isdigit():
            if len(code) <= 5:
                # 港股：补到 5 位
                return code.zfill(5)
            elif len(code) == 6:
                # A 股：保持 6 位
                return code
        
        # 字母代码（美股）
        return code
    
    def resolve_stock_code(self, identifier: str) -> Optional[str]:
        """解析股票代码（返回标准格式）"""
        info = self.identify_stock(identifier)
        if not info:
            return None
        
        # 反向查找标准代码
        for code, val in self.stock_market_map.items():
            if val == info:
                return code
        return None
    
    def get_report_type(self, report_type: str, market: str, stock_code: str = '') -> str:
        """获取对应市场的报告类型
        
        v2.2 新增: 美股外国公司（ADR）使用 20-F/6-K 而非 10-K/10-Q
        v2.1 修复:
        1. market key 统一转小写 (HK → hk)
        2. 大小写不敏感匹配 report_type (10-k → 10-K)
        """
        market_key = market.lower()
        
        # 美股外国公司（ADR）使用 20-F/6-K
        if market.upper() == 'US' and stock_code.upper() in US_FOREIGN_TICKERS:
            market_key = 'us_foreign'
        
        # 1. 精确匹配
        if report_type in self.report_type_map:
            return self.report_type_map[report_type].get(market_key, report_type)
        
        # 2. 大小写不敏感匹配（返回 map 中的标准值）
        for key, val in self.report_type_map.items():
            if key.lower() == report_type.lower():
                return val.get(market_key, key)
        
        # 3. 未知类型，原样返回
        return report_type
    
    def run_command(self, cmd: str, timeout: int = 600) -> Tuple[bool, str]:
        """执行命令并捕获输出（替代 os.system）
        
        Returns:
            (success: bool, output: str)
        """
        print(f"执行: {cmd}")
        print()
        
        try:
            result = subprocess.run(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=timeout
            )
            
            # 实时输出
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            
            return result.returncode == 0, result.stdout + result.stderr
            
        except subprocess.TimeoutExpired:
            print(f"❌ 命令超时（{timeout}s）")
            return False, "Command timed out"
        except Exception as e:
            print(f"❌ 执行失败: {e}")
            return False, str(e)
    
    def verify_result(self, market: str, stock_code: str, output_dir: str) -> Dict:
        """下载后验证结果"""
        result = {
            'market': market,
            'stock_code': stock_code,
            'output_dir': output_dir,
            'json_files': [],
            'csv_files': [],
            'pdf_count': 0,
            'valid': False,
            'message': '',
        }
        
        if not os.path.exists(output_dir):
            result['message'] = f'输出目录不存在: {output_dir}'
            return result
        
        # 扫描输出文件
        for f in os.listdir(output_dir):
            full = os.path.join(output_dir, f)
            if f.endswith('.json'):
                result['json_files'].append(f)
            elif f.endswith('.csv'):
                result['csv_files'].append(f)
        
        pdf_dir = os.path.join(output_dir, 'pdfs')
        if os.path.exists(pdf_dir):
            result['pdf_count'] = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
        
        # 验证逻辑
        if len(result['json_files']) > 0 or len(result['csv_files']) > 0:
            result['valid'] = True
            result['message'] = f'✅ 验证通过: {len(result["json_files"])} JSON, {len(result["csv_files"])} CSV, {result["pdf_count"]} PDF'
        else:
            result['message'] = f'⚠️ 未找到输出文件'
        
        return result
    
    def download(self, stock_identifier: str, from_year: int, to_year: int,
                report_type: str = '年报', download_pdf: bool = True,
                dry_run: bool = False) -> bool:
        """智能下载财报"""
        print("=" * 80)
        print("🌍 全球财报智能下载器 v2.2")
        print("=" * 80)
        print()
        
        # Step 1: 识别股票
        print(f"📝 识别股票：{stock_identifier}")
        stock_info = self.identify_stock(stock_identifier)
        
        if not stock_info:
            print(f"❌ 无法识别股票：{stock_identifier}")
            print("💡 使用股票代码（而非名称）可支持任何公司")
            return False
        
        market = stock_info['market']
        stock_code = self.resolve_stock_code(stock_identifier) or stock_identifier
        company_name = stock_info['name']
        script = stock_info['script']
        
        print(f"   ✅ 市场：{market}")
        print(f"   ✅ 代码：{stock_code}")
        print(f"   ✅ 公司：{company_name}")
        print(f"   ✅ 脚本：{script}")
        print()
        
        # Step 2: 转换报告类型
        is_foreign = stock_code.upper() in US_FOREIGN_TICKERS if market == 'US' else False
        target_type = self.get_report_type(report_type, market, stock_code)
        type_label = ' (ADR→20-F/6-K)' if is_foreign else ''
        print(f"📊 报告类型：{report_type} → {target_type} ({market}{type_label})")
        print(f"📅 年份范围：{from_year} - {to_year}")
        print(f"📄 PDF 下载：{'是' if download_pdf else '否'}")
        print()
        
        if dry_run:
            print("🔍 [Dry Run] 预览模式，不执行下载")
            return True
        
        # Step 3: 按市场调用对应下载器
        if market == 'HK':
            return self._download_hk(stock_code, from_year, to_year, target_type, download_pdf)
        
        script_path = self.script_paths.get(script)
        if not script_path or not os.path.exists(script_path):
            print(f"❌ 脚本不存在：{script_path}")
            return False
        
        if market == 'CN':
            cmd = f"{PYTHON} {script_path} --stock={stock_code} --name={company_name} --from={from_year} --to={to_year} --type={target_type}"
            if download_pdf:
                cmd += " --pdf"
            success, output = self.run_command(cmd)
            output_dir = f"/root/.openclaw/workspace/exports/cninfo_{company_name}"
        
        elif market == 'US':
            cmd = f"{PYTHON} {script_path} --ticker={stock_code} --name={company_name} --from={from_year} --to={to_year} --type={target_type}"
            if download_pdf:
                cmd += " --pdf"
            success, output = self.run_command(cmd)
            output_dir = f"/root/.openclaw/workspace/exports/sec_{company_name}"
        
        else:
            print(f"❌ 未知市场：{market}")
            return False
        
        # Step 4: 验证结果
        print()
        print("=" * 80)
        print("🔍 验证下载结果...")
        verification = self.verify_result(market, stock_code, output_dir)
        print(f"   {verification['message']}")
        print("=" * 80)
        
        return success and verification['valid']

    def _download_hk(self, stock_code: str, from_year: int, to_year: int,
                     report_type: str, download_pdf: bool) -> bool:
        """港股下载 (v2 新增 — 使用 hk_financial_downloader)"""
        script_path = self.script_paths.get('hk_financial_downloader')
        if not script_path or not os.path.exists(script_path):
            print(f"❌ HK 下载器不存在：{script_path}")
            return False
        
        # 报告类型映射到 hk_downloader 格式
        hk_type_map = {
            '年报': '年报',
            '中报': '中报',
            '半年报': '中报',
            '季报': '季报',
            'all': 'all',
        }
        hk_type = hk_type_map.get(report_type, 'all')
        
        cmd = f"python3 {script_path} --stock={stock_code} --from={from_year} --to={to_year} --type={hk_type}"
        if download_pdf:
            cmd += " --pdf"
        
        success, output = self.run_command(cmd)
        
        # 港股输出目录
        output_dir = f"/root/.openclaw/workspace/archive/{stock_code}"
        
        print()
        print("=" * 80)
        print("🔍 验证港股下载结果...")
        verification = self.verify_result('HK', stock_code, output_dir)
        print(f"   {verification['message']}")
        print("=" * 80)
        
        return success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='全球财报智能下载器 v2.2')
    parser.add_argument('stock', type=str, help='股票代码或公司名称')
    parser.add_argument('--from', dest='from_year', type=int, default=2020, help='开始年份')
    parser.add_argument('--to', dest='to_year', type=int, default=2026, help='结束年份')
    parser.add_argument('--type', dest='report_type', type=str, default='年报',
                       help='报告类型：年报/中报/季报/annual/interim/quarterly/10-K/10-Q/20-F/6-K')
    parser.add_argument('--pdf', dest='download_pdf', action='store_true', default=True,
                       help='下载 PDF 文件（默认下载）')
    parser.add_argument('--no-pdf', dest='download_pdf', action='store_false',
                       help='不下载 PDF 文件')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true',
                       help='预览模式，不执行下载')
    
    args = parser.parse_args()
    
    downloader = GlobalFinancialDownloader()
    
    downloader.download(
        stock_identifier=args.stock,
        from_year=args.from_year,
        to_year=args.to_year,
        report_type=args.report_type,
        download_pdf=args.download_pdf,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
