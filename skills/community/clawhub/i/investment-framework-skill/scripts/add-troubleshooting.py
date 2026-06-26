#!/usr/bin/env python3
"""
P2 优化：为所有技能添加故障排查章节
"""

import os

BASE_DIR = '/home/admin/.openclaw/workspace/investment-framework-skill'

TROUBLESHOOTING_SECTION = """
---

## 🔧 故障排查

| 问题 | 检查项 | 解决方案 |
|------|--------|---------|
| 不触发 | description 是否包含触发词？ | 将关键词加入 description |
| 运行失败 | 脚本有执行权限吗？ | `chmod +x scripts/*.py` |
| 数据获取失败 | 网络连接正常吗？ | 检查网络或 API 状态 |
| 数据不足 | Tushare 积分足够吗？ | 签到获取更多积分或使用免费数据源 |
| 输出异常 | 输入格式正确吗？ | 检查股票代码格式（如 600519.SH） |

"""

def add_troubleshooting(filepath):
    """添加故障排查章节"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有故障排查章节
    if '## 🔧 故障排查' in content or '## 🔧' in content:
        return False
    
    # 在文件末尾添加
    content = content.rstrip() + TROUBLESHOOTING_SECTION
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    optimized = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        if '__pycache__' in root or '.git' in root:
            continue
        
        if 'SKILL.md' in files:
            filepath = os.path.join(root, 'SKILL.md')
            if add_troubleshooting(filepath):
                optimized += 1
                print(f"✅ {os.path.basename(os.path.dirname(filepath))}: 添加故障排查")
    
    print(f"\n🎉 故障排查章节添加完成：{optimized} 个技能")

if __name__ == '__main__':
    main()
