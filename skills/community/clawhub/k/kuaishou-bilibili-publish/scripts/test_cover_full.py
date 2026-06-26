#!/usr/bin/env python3
"""完整测试快手封面上传流程"""

from kbs.cdp import Browser
from kbs.types import load_publish_config
import time
import json

def test_full_flow():
    cfg = load_publish_config('../test_data/描述.txt')
    browser = Browser(host='127.0.0.1', port=9222)
    browser.connect()
    page = browser.get_or_create_page()
    
    print("=" * 60)
    print("步骤 1: 上传视频")
    print("=" * 60)
    page.navigate('https://cp.kuaishou.com/article/publish/video')
    page.wait_for_load()
    time.sleep(3)
    
    page.set_file_input('input[type="file"]', [cfg.video_path])
    print("✓ 视频文件已设置")
    time.sleep(15)
    print("✓ 视频上传完成\n")
    
    print("=" * 60)
    print("步骤 2: 点击封面设置")
    print("=" * 60)
    page.click_by_inner_text_then_center('封面设置')
    time.sleep(2)
    print("✓ 已点击封面设置\n")
    
    print("=" * 60)
    print("步骤 3: 上传封面文件")
    print("=" * 60)
    # 直接使用索引 1 设置封面文件
    page.set_file_input_by_index(1, [cfg.cover_path])
    print("✓ 封面文件已设置")
    time.sleep(5)
    
    # 检查封面是否已上传
    has_blob = page.evaluate('document.querySelector("img[src*=\\\\\\"blob\\\\\\"]") !== null')
    print(f"✓ 有 blob 图片：{has_blob}\n")
    
    print("=" * 60)
    print("步骤 4: 查找并点击确定按钮")
    print("=" * 60)
    
    # 查找确定按钮
    confirm_btn_info = page.evaluate('''
    () => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            const text = btn.innerText || btn.textContent;
            if (text && text.includes('确定')) {
                return {
                    text: text.trim(),
                    disabled: btn.disabled || btn.classList.contains('is-disabled'),
                    className: btn.className
                };
            }
        }
        return null;
    }
    ''')
    
    print(f"确定按钮信息：{json.dumps(confirm_btn_info, indent=2, ensure_ascii=False)}")
    
    # 尝试点击确定按钮
    clicked = page.click_by_inner_text_then_center('确定')
    print(f"点击确定按钮：{clicked}")
    time.sleep(2)
    
    print("\n" + "=" * 60)
    print("步骤 5: 验证封面是否应用")
    print("=" * 60)
    
    # 获取页面文本
    body_text = page.body_text()
    lines = body_text.split('\n')
    cover_lines = [l.strip() for l in lines if '封面' in l]
    print("封面相关文本:")
    for line in cover_lines[:10]:
        print(f"  - {line}")
    
    browser.close()
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_full_flow()
