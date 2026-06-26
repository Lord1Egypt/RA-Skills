#!/usr/bin/env python3
"""
定款商品原图无损下载&规范归档 Skill - 主程序
版本：1.0.0

安全声明：
- 仅支持人工输入款号和链接
- 禁止批量自动操作
- 100% 保留原图，不做任何修改
- 自动标注侵权风险
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv

load_dotenv()

log_dir = Path('logs')
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_dir / 'archiver.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

from image_downloader import ImageDownloader
from folder_manager import FolderManager
from risk_detector import RiskDetector
from integrity_checker import IntegrityChecker
from report_generator import ReportGenerator


class ProductArchiver:
    """商品归档器 - 仅人工触发"""
    
    def __init__(self):
        self.downloader = ImageDownloader()
        self.folder_manager = FolderManager()
        self.risk_detector = RiskDetector()
        self.integrity_checker = IntegrityChecker()
        self.report_generator = ReportGenerator()
        
        logger.info("商品归档 Skill v1.0.0 已初始化（人工触发模式）")
    
    def archive_product(self, product_id: str, product_url: str) -> str:
        """归档单款商品 - 核心功能"""
        logger.info(f"开始归档商品（人工触发）：款号={product_id}, 链接={product_url}")
        
        # Step 1: 抓取商品信息
        logger.info("Step 1: 抓取商品信息...")
        product_info = self._fetch_product_info(product_url)
        if not product_info:
            raise Exception("商品信息抓取失败")
        
        product_name = product_info.get('title', '未知商品')
        product_name_short = self._truncate_name(product_name)
        
        # Step 2: 创建归档文件夹
        logger.info("Step 2: 创建归档文件夹...")
        folder_name = f"{product_id}_{product_name_short}"
        archive_path = self.folder_manager.create_archive_folders(folder_name)
        print(f"\n📁 正在创建归档文件夹...")
        print(f"   主文件夹：{folder_name}")
        print(f"   ├── 01-网商园原图归档/")
        print(f"   ├── 02-淘宝上架素材待匹配/")
        print(f"   └── 03-商品资质档案/")
        
        # Step 3: 下载原图（无损模式）
        logger.info("Step 3: 下载原图（无损模式）...")
        print(f"\n📥 正在下载原图（无损模式）...")
        image_urls = product_info.get('images', [])
        download_results = self.downloader.download_images(
            image_urls=image_urls,
            output_dir=archive_path / "01-网商园原图归档"
        )
        
        # Step 4: 侵权风险检测
        logger.info("Step 4: 侵权风险检测...")
        print(f"\n🔍 正在进行侵权风险检测...")
        risk_results = self.risk_detector.detect_all_images(
            image_dir=archive_path / "01-网商园原图归档"
        )
        
        # Step 5: 完整性校验
        logger.info("Step 5: 完整性校验...")
        print(f"\n✅ 正在进行完整性校验...")
        integrity_result = self.integrity_checker.check_all_images(
            image_dir=archive_path / "01-网商园原图归档",
            expected_count=len(image_urls)
        )
        
        # Step 6: 生成归档清单
        logger.info("Step 6: 生成归档清单...")
        print(f"\n📄 正在生成归档清单...")
        manifest_path = self.report_generator.generate_manifest(
            archive_path=archive_path,
            product_info=product_info,
            download_results=download_results,
            risk_results=risk_results,
            integrity_result=integrity_result
        )
        print(f"   ✅ 原图素材归档清单.xlsx")
        
        # 输出总结
        print(f"\n✅ 归档完成！")
        print(f"   位置：{archive_path}")
        print(f"   应下载：{integrity_result['expected_count']} 张")
        print(f"   实下载：{integrity_result['actual_count']} 张")
        print(f"   损坏：{integrity_result['damaged_count']} 张")
        print(f"   风险标注：{len([r for r in risk_results if r['risk_level'] != '无'])} 张")
        
        return str(archive_path)
    
    def _fetch_product_info(self, url: str) -> Optional[Dict]:
        """抓取商品信息"""
        from sources.wsy_source import WSYSource
        from sources.source_1688 import Source1688
        
        if 'wsy.com' in url:
            source = WSYSource()
        elif '1688.com' in url:
            source = Source1688()
        else:
            logger.error(f"不支持的货源网站：{url}")
            return None
        
        product_data = source.fetch_product(url, download_images=False)
        return product_data
    
    def _truncate_name(self, name: str, max_length: int = 20) -> str:
        """截断商品名称"""
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            name = name.replace(char, '')
        
        if len(name) > max_length:
            name = name[:max_length]
        
        return name.strip()


def main():
    """主函数 - 命令行入口（仅人工触发）"""
    parser = argparse.ArgumentParser(
        description='定款商品原图无损下载&规范归档 Skill（人工触发）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例（仅人工触发）:
  # 单款商品归档
  python archiver.py archive --款号 KZ20260326 --链接 "https://www.wsy.com/item/12345.html"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    archive_parser = subparsers.add_parser('archive', help='单款商品归档')
    archive_parser.add_argument('--款号', required=True, help='商品款号（人工提供）')
    archive_parser.add_argument('--链接', required=True, help='商品链接（人工提供）')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    archiver = ProductArchiver()
    
    if args.command == 'archive':
        print(f"正在归档商品：款号={args.款号}")
        print("请稍候，正在进行原图无损下载...")
        print()
        
        try:
            archive_path = archiver.archive_product(args.款号，args.链接)
            print(f"\n✅ 归档完成！文件夹位置：{archive_path}")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ 归档失败：{str(e)}")
            sys.exit(1)


if __name__ == '__main__':
    main()
