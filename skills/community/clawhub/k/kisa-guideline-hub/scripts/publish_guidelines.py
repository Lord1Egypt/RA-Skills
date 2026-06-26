#!/usr/bin/env python3
"""
가이드라인 발행 스크립트
KISA, Boho 가이드라인 수집 및 Notion 발행
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import argparse

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# Security News Module 경로 추가 (security-news-feed의 modules 사용)
import os
skill_path = Path(__file__).parent.parent.parent / 'security-news-feed'
sys.path.insert(0, str(skill_path))
os.chdir(str(skill_path))  # working directory 변경

from modules.crawlers.kisa import KISACrawler
from modules.crawlers.boho import BohoCrawler
from modules.publisher_service import PublisherService
from config import GUIDE_DATABASE_ID

print("="*70)
print("GUIDELINE PUBLISHER")
print("="*70)

def collect_guidelines():
    """가이드라인 수집"""
    print("\n🔄 가이드라인 수집 시작...")
    
    crawlers = [
        ("KISA", KISACrawler),
        ("Boho", BohoCrawler),
    ]
    
    all_guidelines = []
    
    for name, crawler_class in crawlers:
        print(f"\n{name}...")
        try:
            crawler = crawler_class()
            result = crawler.run(publisher_service=None)
            
            collected = len(result.get('queue', []))
            print(f"  ✅ 수집: {collected}개")
            
            if collected > 0:
                all_guidelines.extend(result['queue'])
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
    
    print(f"\n📊 총 수집: {len(all_guidelines)}개 가이드라인")
    return all_guidelines

def publish_guidelines(guidelines):
    """Notion 발행"""
    if not guidelines:
        print("❌ 발행할 가이드라인이 없습니다.")
        return
    
    print(f"\n🔄 Notion 발행 시작... ({len(guidelines)}개)")
    
    # Publisher Service 초기화
    publisher = PublisherService(
        enable_notion=True,
        enable_tistory=False,
        notion_database_id=GUIDE_DATABASE_ID
    )
    
    success_count = 0
    fail_count = 0
    
    for i, guideline in enumerate(guidelines, 1):
        print(f"\n[{i}/{len(guidelines)}] {guideline['title'][:50]}...")
        
        try:
            # Notion 발행 (LLM 없이 바로 발행)
            pub_result = publisher.publish_article(
                title=guideline['title'],
                content=guideline.get('content', '내용 없음'),
                url=guideline['url'],
                date=guideline['posting_date'].strftime('%Y-%m-%d'),
                category=guideline['category'],
                details="",  # 가이드라인은 details 없음
                files=guideline.get('files', []),  # PDF 파일
                database_id=GUIDE_DATABASE_ID
            )
            
            if pub_result.get('notion'):
                success_count += 1
                print("  ✅ 발행 성공")
            else:
                fail_count += 1
                print("  ❌ 발행 실패")
        
        except Exception as e:
            fail_count += 1
            print(f"  ❌ Error: {str(e)[:50]}")
    
    print("\n" + "="*70)
    print("발행 완료")
    print("="*70)
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {fail_count}개")
    print(f"📊 성공률: {success_count/len(guidelines)*100:.1f}%")

def main():
    parser = argparse.ArgumentParser(description='가이드라인 발행')
    parser.add_argument('--collect', action='store_true', help='가이드라인 수집만')
    parser.add_argument('--publish', action='store_true', help='Notion 발행만')
    parser.add_argument('--full', action='store_true', help='수집 + 발행')
    
    args = parser.parse_args()
    
    if not any([args.collect, args.publish, args.full]):
        parser.print_help()
        return
    
    guidelines = []
    
    if args.collect or args.full:
        guidelines = collect_guidelines()
    
    if args.publish:
        # 발행만 실행할 때는 기존 수집된 데이터 사용
        # (실제로는 DB나 파일에서 로드해야 함)
        print("⚠️ --publish 단독 실행은 아직 구현되지 않았습니다.")
        print("--full을 사용하세요.")
        return
    
    if args.full and guidelines:
        publish_guidelines(guidelines)

if __name__ == '__main__':
    main()
