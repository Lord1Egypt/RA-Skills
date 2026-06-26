#!/usr/bin/env python3
"""
腾讯文档创建脚本
创建健康管理在线文档

使用方法:
    python create_online_doc.py --title "我的健康跟踪表"
    python create_online_doc.py --title "健康方案" --content "mdx格式内容"

依赖:
    需要配置环境变量 TENCENT_DOCS_TOKEN
    需要安装mcporter
"""

import argparse
import os
import json
import subprocess


def run_mcporter(service, tool, args):
    """执行mcporter命令"""
    cmd = f'mcporter call {service} {tool} --args \'{json.dumps(args)}\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr


def create_smartcanvas(title, mdx_content):
    """创建腾讯智能文档"""
    args = {
        "title": title,
        "mdx": mdx_content
    }
    stdout, stderr = run_mcporter('tencent-docs', 'create_smartcanvas_by_mdx', args)

    try:
        result = json.loads(stdout)
        if result.get('error') == '' and result.get('file_id'):
            return {
                'success': True,
                'file_id': result['file_id'],
                'url': result.get('url', f"https://docs.qq.com/aio/{result['file_id']}")
            }
    except:
        pass

    return {'success': False, 'error': stdout + stderr}


def append_content(file_id, content):
    """向文档追加内容"""
    args = {
        "action": "INSERT_AFTER",
        "content": content,
        "file_id": file_id,
        "id": ""
    }
    stdout, stderr = run_mcporter('tencent-docs', 'smartcanvas.edit', args)

    try:
        result = json.loads(stdout)
        return {'success': result.get('error') == ''}
    except:
        return {'success': False, 'error': stdout + stderr}


def get_default_mdx(title):
    """获取默认的健康管理模板内容"""
    return f"""# {title}

> 通用健康管理模板 | 生成日期：2026-03-31

## 使用说明

1. 每周记录体重和腰围
2. 记录每日步数和运动时长
3. 打卡饮食情况
4. 记录是否饮酒

## 目标设定

| 指标 | 起始值 | 目标值 | 当前值 |
|------|--------|--------|--------|
| BMI | - | <23 | - |
| 体重(kg) | - | - | - |
| ALT(U/L) | - | <40 | - |
| 每周运动(分钟) | - | ≥150 | - |

## 每周打卡记录

| 周次 | 日期 | 体重 | 腰围 | 步数 | 运动时长 | 饮酒 | 备注 |
|------|------|------|------|------|----------|------|------|
| 第1周 | - | - | - | - | - | - | - |

## 饮食方案

### 每日三餐（蛋奶素）

| 餐次 | 推荐食物 | 份量 |
|------|----------|------|
| 早餐 | 鸡蛋+燕麦+牛奶+水果 | 蛋白质+粗粮+钙 |
| 午餐 | 杂粮饭+豆腐+菌菇+蔬菜 | 植物蛋白+纤维 |
| 晚餐 | 主食减半+豆制品 | 碳水减量 |
| 加餐 | 坚果+水果 | 控制热量 |

### 严格避免

- 酒类
- 动物内脏
- 油炸食品
- 甜饮料

## 运动方案

| 星期 | 类型 | 时长 | 内容 |
|------|------|------|------|
| 周一 | 有氧 | 45min | 跑步/快走 |
| 周二 | 力量 | 50min | 哑铃/俯卧撑 |

## 复查计划

| 检查项目 | 时间 | 目的 |
|----------|------|------|
| 肝功能 | 3个月后 | 验证护肝 |
| 血脂血糖 | 3-6个月后 | 代谢评估 |

---

*通用健康管理模板*
"""


def main():
    parser = argparse.ArgumentParser(description='创建腾讯在线健康管理文档')
    parser.add_argument('--title', '-t', default='健康管理跟踪表', help='文档标题')
    parser.add_argument('--content', '-c', default='', help='MDX格式内容（可选）')
    parser.add_argument('--file-id', '-f', default='', help='已存在的文档ID，用于追加内容')

    args = parser.parse_args()

    print("=" * 50)
    print("📄 腾讯文档创建工具")
    print("=" * 50)

    # 检查Token
    token = os.environ.get('TENCENT_DOCS_TOKEN')
    if not token:
        print("\n⚠️ 未配置TENCENT_DOCS_TOKEN环境变量")
        print("请先配置：")
        print('   export TENCENT_DOCS_TOKEN="你的Token"')
        print("\n获取Token：https://docs.qq.com/open/auth/mcp.html")
        return

    if args.file_id:
        # 追加内容到已有文档
        print(f"\n📝 追加内容到文档 {args.file_id}...")
        content = args.content if args.content else get_default_mdx(args.title)
        result = append_content(args.file_id, content)
        if result['success']:
            print("✅ 内容追加成功！")
        else:
            print(f"❌ 追加失败：{result.get('error', '未知错误')}")

    else:
        # 创建新文档
        print(f"\n📄 创建文档：{args.title}")
        mdx_content = args.content if args.content else get_default_mdx(args.title)
        result = create_smartcanvas(args.title, mdx_content)

        if result['success']:
            print("\n✅ 文档创建成功！")
            print(f"\n📎 文档链接：{result['url']}")
            print(f"🆔 文档ID：{result['file_id']}")
            print("\n💡 微信直接打开链接即可查看/编辑")
        else:
            print(f"\n❌ 创建失败：{result.get('error', '未知错误')}")
            print("\n请检查：")
            print("1. Token是否有效")
            print("2. 网络连接是否正常")
            print("3. mcporter是否正确安装")

    print("=" * 50)


if __name__ == "__main__":
    main()
