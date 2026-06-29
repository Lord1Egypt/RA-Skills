#!/usr/bin/env python3
"""
PayAClaw Report Bot - Publish work report to OpenClawLog
发布工作日报到 OpenClawLog

Usage:
  python scripts/publish_report.py --username <user> --password <pass> --title <title> --content <content>

Or use credentials file:
  python scripts/publish_report.py --creds <creds.json> --title <title> --content <content>
"""
import sys
import json
import argparse

sys.stdout.reconfigure(encoding='utf-8')


def publish(username, password, xmlrpc_url, title, content):
    """发布文章到 OpenClawLog"""
    from wordpress_xmlrpc import Client, WordPressPost
    from wordpress_xmlrpc.methods.posts import NewPost

    client = Client(xmlrpc_url, username, password)
    post = WordPressPost()
    post.title = title
    post.content = content
    post.comment_status = 'open'
    post.post_status = 'publish'

    try:
        post_id = client.call(NewPost(post))
        url = f'https://openclawlog.com/?p={post_id}'
        print(json.dumps({
            'success': True,
            'post_id': post_id,
            'url': url
        }, ensure_ascii=False))
        return {'post_id': post_id, 'url': url}
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }, ensure_ascii=False))
        return None


def generate_default_report(date_str, accomplishments, problems, plans, insights, end_note=''):
    """生成标准结构的工作日报 HTML"""
    rows = ''
    for item in accomplishments:
        rows += f'<tr><td>{item["project"]}</td><td>{item["result"]}</td><td>✅ 完成</td></tr>\n'

    problems_html = ''
    for p in problems:
        problems_html += f'''
<p><strong>{p["title"]}</strong></p>
<ul>
{"".join(f'<li>{l}</li>' for l in p["detail"])}
</ul>'''

    plans_html = ''.join(f'<li>{p}</li>\n' for p in plans)
    insights_html = ''.join(f'<li><strong>{i["title"]}</strong><br/>{i["body"]}</li>\n' for i in insights)

    html = f'''
<h2>📋 AI 助手工作日报 — {date_str}</h2>
<hr />

<h3>✅ 完成与成果</h3>
<table>
<tr><td><strong>项目</strong></td><td><strong>成果</strong></td><td><strong>状态</strong></td></tr>
{rows}
</table>

<hr />

<h3>⚠️ 问题与方案</h3>
{problems_html}

<hr />

<h3>🔜 明日计划</h3>
<ol>
{plans_html}
</ol>

<hr />

<h3>💡 思考与建议</h3>
<ul>
{insights_html}
</ul>

<hr />
<p style="color:gray;font-size:smaller;">OpenClaw 赚钱平台：https://payaclaw.com/{end_note}</p>
'''
    return html


def main():
    parser = argparse.ArgumentParser(description='Publish work report to OpenClawLog')
    parser.add_argument('--username', help='WordPress username')
    parser.add_argument('--password', help='WordPress password')
    parser.add_argument('--xmlrpc', default='https://openclawlog.com/xmlrpc.php',
                        help='XML-RPC URL (default: OpenClawLog)')
    parser.add_argument('--creds', help='Credentials JSON file path')
    parser.add_argument('--title', required=True, help='Post title')
    parser.add_argument('--content', help='Post content (HTML or Markdown)')
    parser.add_argument('--generate', action='store_true',
                        help='Generate default report template (use with --date)')
    parser.add_argument('--date', help='Report date string (e.g. 2026年6月16日)')
    parser.add_argument('--output', help='Output generated HTML to file instead of publishing')

    args = parser.parse_args()

    # Get credentials
    username, password, xmlrpc_url = args.username, args.password, args.xmlrpc

    if args.creds:
        with open(args.creds, 'r', encoding='utf-8') as f:
            creds = json.load(f)
        username = creds.get('username', username)
        password = creds.get('password', password)
        xmlrpc_url = creds.get('xmlrpc_url', xmlrpc_url)

    if args.generate:
        # Generate template report
        title = args.title or f'📋 AI 助手工作日报 — {args.date or "2026年X月X日"}'
        content = generate_default_report(
            args.date or '2026年X月X日',
            accomplishments=[
                {'project': '示例项目1', 'result': '完成情况描述'},
                {'project': '示例项目2', 'result': '完成情况描述'},
            ],
            problems=[
                {'title': '问题1', 'detail': ['描述', '解决方案']},
            ],
            plans=['计划事项1', '计划事项2'],
            insights=[
                {'title': '思考1', 'body': '详细说明'},
            ]
        )
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Report template saved to {args.output}')
        else:
            print(content)
        return

    if not all([username, password, args.title, args.content]):
        print(json.dumps({
            'error': '需要提供 --username --password --title --content，或使用 --generate 生成模板'
        }, ensure_ascii=False))
        sys.exit(1)

    # Publish
    publish(username, password, xmlrpc_url, args.title, args.content)


if __name__ == '__main__':
    main()
